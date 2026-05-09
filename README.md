# AiArchitecture — How iCt Horse Engineers with AI

> **"Not vibe coding. Architecture-driven AI collaboration with measurable results."**

## What This Is

This repository documents and measures how [iCt Horse](https://icthorse.nl) achieves predictable, high-quality results when collaborating with AI coding agents (Claude Code, Gemini CLI, OpenAI Codex, ChatGPT).

It's not a theoretical framework. It's evidence from **50+ real repositories**, scanned and measured automatically.

## Why This Exists

Most AI-assisted coding is unstructured: paste a prompt, hope for the best, manually fix what breaks. That's vibe coding.

iCt Horse takes a fundamentally different approach:
- **Constraints** define what the AI can and cannot do
- **Protocols** enforce quality at every step (WhatIf, RCA, versioning)
- **Memory architecture** preserves context across sessions and agents
- **Multi-agent orchestration** coordinates Claude, Gemini, Codex and ChatGPT
- **Architecture principles** guide every decision (Dragon1-structured)
- **Security by design** with git-crypt, shared infrastructure safety, privacy filters

## Key Metrics (Latest Scan)

<!-- Updated automatically by tools/report_generator.py -->
_Run `python3 tools/repo_scanner.py` to generate the first scan._

## Framework

| Document | What It Covers |
|----------|---------------|
| [Overview](framework/OVERVIEW.md) | The complete methodology at a glance |
| [Prompting Patterns](framework/PROMPTING_PATTERNS.md) | Catalogued patterns with evidence |
| [Memory Architecture](framework/MEMORY_ARCHITECTURE.md) | Persistent memory across sessions and agents |
| [Constraint System](framework/CONSTRAINT_SYSTEM.md) | CLAUDE.md files, protocols, hooks, safety rules |
| [Quality Controls](framework/QUALITY_CONTROLS.md) | Versioning, builds, debugging, root cause analysis |
| [Multi-Agent Orchestration](framework/MULTI_AGENT.md) | Claude + Gemini + Codex + ChatGPT coordination |
| [Security Practices](framework/SECURITY_PRACTICES.md) | Encryption, infrastructure safety, privacy |
| [Principles](framework/PRINCIPLES.md) | 25 architecture principles across 7 design areas |

## How to Run a Scan

```bash
cd /path/to/AiArchitecture
python3 tools/repo_scanner.py
python3 tools/metrics_collector.py
python3 tools/report_generator.py
```

## About iCt Horse

**iCt Horse — Connecting the dots.** Bridges people and technology through AI-driven solutions.

- KvK: 96787112
- Website: [icthorse.nl](https://icthorse.nl)
- Founder: Christian Glebbeek — IT Architect / Enterprise Architect

## License

MIT — The framework and tooling are open source. Evidence data is generated from private repositories and contains no sensitive information.
