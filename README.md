# Sidecar v4 — Quality Control for Claude Code

A persistent daemon that monitors Claude Code in real-time and injects situational context. Three layers of quality control:

1. **Pattern Detection** (deterministic, $0, ~1ms) — Detects anti-patterns, loops, stalls, error cascades
2. **Quick Judge** (LLM, ~$0.0002/call, SYNC) — Evaluates work quality against coaching rules
3. **Deep Judge Agent** (LLM + function calling, ~$0.005/call, ASYNC) — Autonomous coach that navigates a knowledge base and gives personalized feedback

## Architecture

```
                    Claude Code Hooks
                         |
              +----------+----------+
              |                     |
         PostToolUse          UserPromptSubmit
         (sidecar_bridge.py)  (userpromptsubmit_bridge.py)
              |                     |
              +------> Unix Socket <------+
                    /tmp/claude-sidecar.sock
                           |
                    +------+------+
                    |  sidecar.py |  (asyncio server)
                    +------+------+
                           |
          +--------+-------+-------+--------+
          |        |       |       |        |
     RuleRegistry  |  PluginLoader |  PhaseTracker
     (22 Rules)    |  (3 Plugins)  |  (4 Phases)
          |        |       |       |
     6 Gates    9 Detectors    rules/*.py
     (PreToolUse   (PostToolUse)
      blocking)
```

## Components

| Component | What it does |
|-----------|-------------|
| `sidecar.py` | Core daemon. Asyncio Unix socket server, 9 detectors, rule registry, session state, gate blocks |
| `llm_judge.py` | Quick Judge (v3). LLM provider abstraction, budget tracking, caching |
| `judge_agent.py` | Deep Judge Agent (v4). Autonomous coach with function calling, navigates knowledge base |
| `phase_tracker.py` | Tracks session phase (exploration/implementation/testing/debugging) |
| `plugin_loader.py` | Loads rule plugins from `rules/` via importlib. Hot-reload via SIGHUP |
| `context_selector.py` | Selects relevant context for injection based on session state |
| `session_watcher.py` | Monitors session files for changes |
| `skill_recommender.py` | Suggests relevant skills based on current phase and activity |
| `voice_bridge.py` | STT daemon — speech via Whisper, output via wtype/ydotool |
| `sidecar-ctl` | CLI tool with 10+ subcommands for status, rules, sessions, judge control |
| `gui/` | GTK3 dashboard for real-time monitoring |

## 9 Detectors (PostToolUse)

| Detector | What it catches |
|----------|----------------|
| LOOP | Same tool+input repeating (3x in last 6 calls) |
| READ-STORM | Only reading without action (6+ consecutive reads) |
| ERROR-CASCADE | Error accumulation (2+ errors in last 5 calls) |
| DRIFT | Editing in directory without prior read there |
| YOLO | Editing file without reading it first |
| THRASH | Same file edited repeatedly (3x in last 6 calls) |
| STALL | No write operations for 10+ calls |
| ANTI-PATTERN | Matches against known anti-pattern keywords |
| SKILL-SUGGEST | Suggests relevant skill for current activity |

## 6 Gates (PreToolUse, blocking)

| Gate | What it blocks |
|------|---------------|
| `gate_rm_rf` | `rm -rf` without confirmation |
| `gate_autonomous_git` | git commit/push without prior status check |
| `gate_secret_exposure` | API keys/secrets in config files |
| `gate_force_push` | `git push --force` |
| `gate_opencode_vague` | Vague prompts to coding agents |
| `gate_wrong_provider` | Unconfigured provider in coding agents |

## Plugin System

Drop Python files in `rules/` to add new rules:

```python
from rule_plugin import RulePlugin

class MyRule(RulePlugin):
    name = "my_rule"
    description = "What this rule does"

    def match(self, prompt: str, session_state: dict) -> bool:
        return "keyword" in prompt.lower()

    def inject(self) -> str:
        return "[RULE: my_rule] Context to inject"
```

Hot-reload: `sidecar-ctl reload` or `kill -HUP <pid>`.

## Version History

| Version | What's new |
|---------|-----------|
| v1 | Core daemon, 22 rules, 9 detectors, 6 gates, plugin system ([repo](https://github.com/smlfg/sidecar-v1)) |
| v2 | + Session watcher, context selector, skill recommender, GTK3 GUI ([repo](https://github.com/smlfg/sidecar-v2)) |
| v3 | + LLM Quick Judge (MiniMax/Gemini), coaching rules, budget tracker ([repo](https://github.com/smlfg/sidecar-v3)) |
| v4 | + Deep Judge Agent with function calling and autonomous knowledge base navigation |

## Setup

See [SETUP.md](SETUP.md) for installation and systemd service configuration.

## CLI

```bash
sidecar-ctl status          # Daemon status incl. judges
sidecar-ctl rules           # All 22 rules with fire counts
sidecar-ctl sessions        # Active sessions
sidecar-ctl findings        # Recent findings
sidecar-ctl judge status    # Quick Judge status
sidecar-ctl judge deep      # Deep Judge status
sidecar-ctl reload          # Reload plugins + config
sidecar-ctl log -n 50       # Recent log entries
```

## Design Decisions

- **Unix Socket** over HTTP — faster (~1ms), no port conflicts
- **asyncio** — non-blocking I/O, clean shutdown via signals
- **File-based session state** — simple, no DB needed, survives daemon restarts
- **Plugin system via importlib** — hot-reload without restart
- **Fail-open** — daemon must never crash Claude Code. All exceptions caught, worst case returns `{}`

## License

MIT
