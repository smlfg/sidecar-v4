#!/usr/bin/env python3
"""Sidecar Eval Runner — replays scenario events through v1/v2/v3.

Usage:
    python eval_runner.py                  # run all scenarios
    python eval_runner.py loop_detection   # run single scenario by name
    python eval_runner.py --list           # list available scenarios
"""

import copy
import glob
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

VERSIONS_DIR = Path(__file__).parent / "versions"
SCENARIOS_DIR = Path(__file__).parent / "scenarios"
RESULTS_DIR = Path(__file__).parent / "results"

RESULTS_DIR.mkdir(exist_ok=True)

# In-memory session state store — keyed by (version_name, session_id)
_SESSION_STORE: dict = {}


# ---------------------------------------------------------------------------
# Version loading
# ---------------------------------------------------------------------------

def load_version(version_name: str):
    """Import sidecar module from versions/{version_name}/ with all dependencies mocked."""
    version_dir = VERSIONS_DIR / version_name
    sidecar_path = version_dir / "sidecar.py"

    if not sidecar_path.exists():
        raise FileNotFoundError(f"No sidecar.py in {version_dir}")

    # Add version dir to front of sys.path so relative imports work
    version_str = str(version_dir)
    if version_str not in sys.path:
        sys.path.insert(0, version_str)

    # Module name must be unique per version to avoid caching collisions
    mod_name = f"sidecar_{version_name}"

    # Remove cached version if present (allows re-import with fresh state)
    for key in list(sys.modules.keys()):
        if key.startswith(f"sidecar_{version_name}") or (
            version_str in sys.modules.get(key, object).__spec__.origin
            if hasattr(sys.modules.get(key, None), "__spec__") and
               sys.modules[key].__spec__ is not None and
               sys.modules[key].__spec__.origin
            else False
        ):
            del sys.modules[key]

    spec = importlib.util.spec_from_file_location(mod_name, sidecar_path)
    module = importlib.util.module_from_spec(spec)

    # Patch companion file reads to return empty strings (no actual files needed)
    mock_open = _make_mock_open()

    patches = [
        # Companion files — mock open() in the sidecar module's builtins
        patch("builtins.open", mock_open),
        # fcntl.flock — no-op (no file locking in eval)
        patch("fcntl.flock", return_value=None),
        # tempfile.mkstemp — return a fake fd/path pair (save goes through mock open)
        patch("tempfile.mkstemp", side_effect=_fake_mkstemp),
        # os.replace — no-op (we use in-memory state)
        patch("os.replace", return_value=None),
        # os.unlink — no-op
        patch("os.unlink", return_value=None),
        # os.fdopen — return mock file object
        patch("os.fdopen", side_effect=_fake_fdopen),
    ]

    # For v2/v3: mock SessionWatcher so it doesn't start threads
    if version_name in ("v2", "v3"):
        patches.append(patch.dict(sys.modules, {
            "watchdog": MagicMock(),
            "watchdog.observers": MagicMock(),
            "watchdog.events": MagicMock(),
        }))

    for p in patches:
        p.start()

    try:
        spec.loader.exec_module(module)
    finally:
        for p in patches:
            try:
                p.stop()
            except RuntimeError:
                pass  # already stopped

    # Tag module so we can reference its version
    module._eval_version = version_name
    module._eval_version_dir = version_dir

    return module


def _make_mock_open():
    """Return a mock open() that returns empty content for companion files,
    and delegates lock files / tmp files to a no-op in-memory implementation."""
    real_open = open

    class _FakeFile:
        def __init__(self):
            self._data = ""
        def read(self):
            return self._data
        def write(self, data):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *a):
            pass
        def fileno(self):
            return -1

    def _mock_open(path, mode="r", *args, **kwargs):
        path_str = str(path) if not isinstance(path, str) else path
        # Companion files and coaching rules — return empty
        if any(name in path_str for name in [
            "WelcheFehlerVermeiden", "Skilluebersicht", "coaching_rules",
            "minimax-key", "gemini-key", "sidecar-rules.json",
        ]):
            return _FakeFile()
        # Lock files and state files in /tmp — return no-op file
        if path_str.startswith("/tmp/sidecar"):
            return _FakeFile()
        # Log file — no-op
        if "claude-sidecar.log" in path_str:
            return _FakeFile()
        # For actual eval/version source files, use real open
        return real_open(path, mode, *args, **kwargs)

    return _mock_open


_fake_fd_counter = [100]

def _fake_mkstemp(**kwargs):
    fd = _fake_fd_counter[0]
    _fake_fd_counter[0] += 1
    return (fd, f"/tmp/fake-sidecar-{fd}.tmp")


def _fake_fdopen(fd, mode="r", *args, **kwargs):
    class _NoopFile:
        def write(self, d): pass
        def __enter__(self): return self
        def __exit__(self, *a): pass
    return _NoopFile()


# ---------------------------------------------------------------------------
# State creation with in-memory session I/O patches
# ---------------------------------------------------------------------------

def create_fresh_state(version_name: str, module):
    """Create a fresh SidecarState with file I/O replaced by in-memory dicts."""

    # Per-version session store — isolated from other versions
    store: dict = {}

    def _load_session(session_id: str) -> dict:
        if session_id not in store:
            store[session_id] = {
                "history": [],
                "last_analysis_ts": 0,
                "session_start_ts": 0,
                "files_touched": [],
                "total_calls": 0,
                "recap_done": False,
            }
        return copy.deepcopy(store[session_id])

    def _save_session(session_id: str, state: dict) -> None:
        store[session_id] = copy.deepcopy(state)

    def _lock_path_noop(session_id: str) -> str:
        return f"/tmp/eval-lock-{session_id}.lock"

    # Patch module-level functions
    module._load_session_state = _load_session
    module._save_session_state = _save_session
    module._lock_path = _lock_path_noop

    # Build state object — companion file loads fail gracefully (mock open returns "")
    mock_open = _make_mock_open()
    with patch("builtins.open", mock_open), \
         patch("fcntl.flock", return_value=None):
        state = module.SidecarState()
        # Load companion files (returns empty — no actual files needed)
        state.load_companion_files()

    # v3: disable LLM judge — no external calls
    if hasattr(state, "llm_judge"):
        state.llm_judge.enabled = False

    # v2/v3: disable SessionWatcher — stop background threads if started
    if hasattr(state, "session_watcher"):
        try:
            state.session_watcher.stop()
        except Exception:
            pass
        # Replace with a no-op stub
        state.session_watcher = MagicMock()

    return state, store


# ---------------------------------------------------------------------------
# Event processing
# ---------------------------------------------------------------------------

def process_event_for_version(module, event: dict, state) -> dict:
    """Run _process_event on a version, return response + latency."""
    full_event = {
        "session_id": event.get("session_id", "eval-session-001"),
        "tool_name": event["tool"],
        "tool_input": event.get("input", {}),
        "error": "Error occurred" if event.get("had_error") else "",
        "hook_event_name": event.get("hook_event", "PostToolUse"),
        "tool_response": event.get("response_text", ""),
    }

    # Disable cooldown in eval so all detections are captured regardless of timing
    version_mod_name = f"sidecar_{getattr(module, '_eval_version', 'vX')}"
    with patch("fcntl.flock", return_value=None), \
         patch("builtins.open", _make_mock_open()), \
         patch("tempfile.mkstemp", side_effect=_fake_mkstemp), \
         patch("os.replace", return_value=None), \
         patch("os.fdopen", side_effect=_fake_fdopen), \
         patch.object(module, "CONCERN_COOLDOWN_SECONDS", 0):
        start = time.perf_counter()
        result = module._process_event(full_event, state)
        elapsed = time.perf_counter() - start

    return {
        "response": result,
        "latency_ms": round(elapsed * 1000, 2),
        "fired": _extract_fired_detectors(result),
    }


def _extract_fired_detectors(response: dict) -> list:
    """Parse which detectors fired from the response dict."""
    fired = []
    if not response:
        return fired

    text = response.get("additionalContext", "") + response.get("systemMessage", "")
    reason = response.get("reason", "")
    all_text = text + " " + reason

    detector_names = [
        "LOOP", "READ-STORM", "ERROR-CASCADE", "DRIFT", "YOLO",
        "THRASH", "STALL", "ANTI-PATTERN", "SKILL-SUGGEST",
        "ENFORCEMENT", "SIDECAR GATE",
    ]
    for det in detector_names:
        if det in all_text:
            fired.append(det)

    if response.get("decision") == "block":
        fired.append("GATE-BLOCK")
        # Extract gate rule name from reason: "[SIDECAR GATE] gate_name: message"
        if "GATE]" in reason:
            gate_part = reason.split("GATE]")[-1].strip()
            gate_name = gate_part.split(":")[0].strip()
            # Map gate names to expected detection names
            gate_map = {
                "gate_autonomous_git": "autonomous_git",
                "gate_force_push": "force_push",
                "gate_rm_rf": "rm_rf",
                "gate_secret_exposure": "secret_exposure",
            }
            mapped = gate_map.get(gate_name, gate_name)
            if mapped not in fired:
                fired.append(mapped)

    # Extract enforcement rule names: "ENFORCEMENT [rule_name]:"
    import re
    for m in re.finditer(r"ENFORCEMENT \[(\w+)\]", all_text):
        rule_name = m.group(1)
        if rule_name not in fired:
            fired.append(rule_name)

    return fired


# ---------------------------------------------------------------------------
# Scenario runner
# ---------------------------------------------------------------------------

def run_scenario(scenario_path: Path, versions: dict) -> dict:
    """Run one scenario through all versions, return results dict."""
    with open(scenario_path) as f:
        scenario = json.load(f)

    results = {
        "scenario": scenario["name"],
        "description": scenario.get("description", ""),
        "expected_detections": scenario.get("expected_detections", []),
        "events": [],
        "summary": {},
    }

    # Create fresh state per version (isolated stores)
    states = {}
    for vname, vmod in versions.items():
        state_obj, _ = create_fresh_state(vname, vmod)
        states[vname] = (vmod, state_obj)

    for i, event in enumerate(scenario["events"]):
        event_result = {
            "index": i,
            "tool": event["tool"],
            "input": event.get("input", {}),
            "had_error": event.get("had_error", False),
            "responses": {},
        }
        for vname, (vmod, state) in states.items():
            event_result["responses"][vname] = process_event_for_version(vmod, event, state)

        results["events"].append(event_result)

    # Build per-version summary
    for vname in versions:
        all_fired = []
        total_latency = 0.0
        injections = 0
        for ev in results["events"]:
            r = ev["responses"][vname]
            all_fired.extend(r["fired"])
            total_latency += r["latency_ms"]
            if r["response"]:
                injections += 1

        expected = set(results["expected_detections"])
        found = set(all_fired)
        results["summary"][vname] = {
            "detectors_fired": list(dict.fromkeys(all_fired)),  # deduplicated, ordered
            "injections": injections,
            "total_latency_ms": round(total_latency, 2),
            "avg_latency_ms": round(total_latency / max(len(results["events"]), 1), 2),
            "expected_hit": list(expected & found),
            "expected_miss": list(expected - found),
        }

    return results


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def print_summary_table(all_results: list) -> None:
    versions = ["v1", "v2", "v3"]
    col = 16

    header = f"{'Scenario':<28}" + "".join(f"  {v:<{col}}" for v in versions)
    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))

    for r in all_results:
        name = r["scenario"][:27]
        expected = r["expected_detections"]

        row = f"{name:<28}"
        for v in versions:
            if v not in r["summary"]:
                row += f"  {'N/A':<{col}}"
                continue
            s = r["summary"][v]
            hit = len(s["expected_hit"])
            miss = len(s["expected_miss"])
            total_exp = hit + miss
            fired_str = ",".join(s["detectors_fired"][:2]) or "-"
            status = f"{hit}/{total_exp}hit {fired_str}"
            row += f"  {status:<{col}}"
        print(row)

    print("=" * len(header))


def save_results(all_results: list, scenario_filter: str = None) -> str:
    ts = time.strftime("%Y%m%d-%H%M%S")
    suffix = f"-{scenario_filter}" if scenario_filter else "-all"
    out_path = RESULTS_DIR / f"eval{suffix}-{ts}.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)
    return str(out_path)


# ---------------------------------------------------------------------------
# Version loader with retry-safe import isolation
# ---------------------------------------------------------------------------

def load_all_versions() -> dict:
    versions = {}
    for vname in ("v1", "v2", "v3"):
        try:
            versions[vname] = load_version(vname)
        except Exception as e:
            print(f"[WARN] Could not load {vname}: {e}", file=sys.stderr)
    return versions


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]

    if "--list" in args:
        scenario_files = sorted(SCENARIOS_DIR.glob("*.json"))
        if not scenario_files:
            print("No scenarios found in", SCENARIOS_DIR)
        else:
            print(f"Available scenarios ({len(scenario_files)}):")
            for sf in scenario_files:
                with open(sf) as f:
                    sc = json.load(f)
                exp = sc.get("expected_detections", [])
                print(f"  {sf.stem:<30}  expect: {exp}")
        return

    # Filter to single scenario if given
    scenario_filter = args[0] if args and not args[0].startswith("--") else None

    scenario_files = sorted(SCENARIOS_DIR.glob("*.json"))
    if not scenario_files:
        print("No scenario files found in", SCENARIOS_DIR)
        sys.exit(1)

    if scenario_filter:
        scenario_files = [sf for sf in scenario_files if sf.stem == scenario_filter]
        if not scenario_files:
            print(f"Scenario '{scenario_filter}' not found. Use --list to see available.")
            sys.exit(1)

    print(f"Loading versions...")
    versions = load_all_versions()
    if not versions:
        print("No versions could be loaded.")
        sys.exit(1)
    print(f"Loaded: {list(versions.keys())}")

    all_results = []
    for sf in scenario_files:
        print(f"\nRunning: {sf.stem} ({len(json.load(open(sf))['events'])} events)...", end=" ")
        try:
            result = run_scenario(sf, versions)
            all_results.append(result)
            # Quick inline summary
            summaries = []
            for v, s in result["summary"].items():
                hit = len(s["expected_hit"])
                total = hit + len(s["expected_miss"])
                summaries.append(f"{v}:{hit}/{total}")
            print(" | ".join(summaries))
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

    if all_results:
        print_summary_table(all_results)
        out_path = save_results(all_results, scenario_filter)
        print(f"\nResults saved to: {out_path}")


if __name__ == "__main__":
    main()
