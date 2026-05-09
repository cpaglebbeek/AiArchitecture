#!/usr/bin/env python3
"""
report_generator.py — Genereert leesbare rapporten uit scan data.

Output:
- reports/latest_scan.md — Volledig rapport
- reports/linkedin/ — LinkedIn-ready samenvattingen
"""

import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
METRICS_DIR = PROJECT_ROOT / "evidence" / "metrics"
REPORTS_DIR = PROJECT_ROOT / "reports"


def load_latest_scan():
    """Laad de meest recente scan."""
    latest = METRICS_DIR / "latest_scan.json"
    if not latest.exists():
        return None
    with open(latest) as f:
        return json.load(f)


def generate_full_report(scan_data):
    """Genereer een volledig markdown rapport."""
    s = scan_data["summary"]
    date = scan_data.get("scan_date", "unknown")[:10]

    report = f"""# AI Architecture Scan Report — {date}

> Automatisch gegenereerd door `tools/report_generator.py`
> Bron: {scan_data.get('source', 'PROJECTS.json')}

## Samenvatting

| Metric | Waarde | Percentage |
|--------|--------|------------|
| Totaal repositories | {s['total_repos']} | — |
| Met CLAUDE.md (constraints) | {s['constraint_coverage']['repos_with_claude_md']} | {s['constraint_coverage']['percentage']}% |
| Met ARCHITECTURE.md | {s['architecture_docs']['repos_with_architecture_md']} | {s['architecture_docs']['percentage']}% |
| Met git-crypt (encrypted) | {s['security_posture']['repos_with_git_crypt']} | {s['security_posture']['percentage']}% |
| Met versioning | {s['versioning_discipline']['repos_with_versioning']} | {s['versioning_discipline']['percentage']}% |

## Agent Samenwerking

| Agent | Co-Authored Commits |
|-------|-------------------|
| Claude Code | {s['agent_collaboration']['claude_co_authored']} |
| Gemini CLI | {s['agent_collaboration']['gemini_co_authored']} |
| OpenAI Codex | {s['agent_collaboration']['codex_co_authored']} |
| ChatGPT | {s['agent_collaboration']['chatgpt_co_authored']} |

**Actieve agents:** {s['agent_collaboration']['agents_active']}/4

## Memory Systeem

| Type | Aantal |
|------|--------|
| Totaal | {s['memory_system']['total_memories']} |
| Feedback (geleerde lessen) | {s['memory_system']['feedback_memories']} |
| Project (context) | {s['memory_system']['project_memories']} |
| User (profiel) | {s['memory_system']['user_memories']} |
| Reference (bronnen) | {s['memory_system']['reference_memories']} |

## Protocol Adoption

"""
    if s.get("protocol_adoption"):
        report += "| Protocol | Repos | Adoptie |\n"
        report += "|----------|-------|---------|\n"
        for proto, info in s["protocol_adoption"].items():
            report += f"| {proto} | {info['count']} | {info['percentage']}% |\n"

    report += f"""
## Cross-Agent Sync

| Agent | Sync Actief |
|-------|-------------|
| Gemini CLI | {'Ja' if s['cross_agent_sync']['gemini_sync_active'] else 'Nee'} |
| OpenAI Codex | {'Ja' if s['cross_agent_sync']['codex_sync_active'] else 'Nee'} |

## Per Repository

| Repo | CLAUDE.md | Arch | git-crypt | Sessions | Claude | Gemini |
|------|-----------|------|-----------|----------|--------|--------|
"""

    for repo in scan_data.get("repos", []):
        if not repo.get("exists"):
            continue
        cm = "✓" if repo.get("has_claude_md") else "✗"
        ar = "✓" if repo.get("has_architecture_md") else "✗"
        gc = "🔒" if repo.get("has_git_crypt") else "—"
        sd = str(repo.get("session_doc_count", 0))
        cl = str(repo.get("claude_commits", 0))
        gm = str(repo.get("gemini_commits", 0))
        report += f"| {repo['name']} | {cm} | {ar} | {gc} | {sd} | {cl} | {gm} |\n"

    report += f"""
---
*Gegenereerd op {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} door AiArchitecture Scanner v{scan_data.get('scanner_version', '1.0.0')}*
"""

    return report


def generate_linkedin_summary(scan_data):
    """Genereer een LinkedIn-ready samenvatting."""
    s = scan_data["summary"]
    date = scan_data.get("scan_date", "unknown")[:10]

    ac = s["agent_collaboration"]
    total_ai_commits = (ac["claude_co_authored"] + ac["gemini_co_authored"]
                        + ac["codex_co_authored"] + ac["chatgpt_co_authored"])

    summary = f"""# AI Architecture — Key Metrics ({date})

## The Numbers

- **{s['total_repos']} repositories** managed with structured AI collaboration
- **{s['constraint_coverage']['percentage']}% constraint coverage** — CLAUDE.md files defining AI behavior
- **{s['memory_system']['total_memories']} persistent memories** — context that survives across sessions
- **{s['memory_system']['feedback_memories']} feedback loops** — corrections that become permanent rules
- **{total_ai_commits} AI co-authored commits** across {s['agent_collaboration']['agents_active']} different AI agents
- **{s['security_posture']['repos_with_git_crypt']} encrypted repositories** — security by design

## What This Means

This is not "vibe coding" — hoping AI output works. This is architecture-driven AI collaboration where:

1. Every AI agent works within defined constraints (CLAUDE.md)
2. Every correction becomes a permanent learning (feedback memory)
3. Every change follows protocols (WhatIf, RCA, versioning)
4. Multiple AI agents coordinate through sync files
5. Security is enforced, not optional

## The Framework

- Constraint System — 3-layer CLAUDE.md architecture
- Memory Architecture — typed, persistent, cross-agent
- Quality Controls — WhatIf, RCA, color-coded severity
- Multi-Agent Orchestration — Claude + Gemini + Codex + ChatGPT
- Security Practices — git-crypt, shared infrastructure, privacy filters

Full framework: github.com/cpaglebbeek/AiArchitecture

---
iCt Horse — Connecting the dots.
"""

    return summary


def main():
    scan_data = load_latest_scan()
    if not scan_data:
        print("Geen scan data gevonden. Draai eerst repo_scanner.py.")
        return 1

    # Volledig rapport
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    full_report = generate_full_report(scan_data)
    report_file = REPORTS_DIR / "latest_scan.md"
    with open(report_file, "w") as f:
        f.write(full_report)
    print(f"Rapport geschreven: {report_file}")

    # LinkedIn samenvatting
    linkedin_dir = REPORTS_DIR / "linkedin"
    linkedin_dir.mkdir(parents=True, exist_ok=True)
    linkedin_summary = generate_linkedin_summary(scan_data)
    date = scan_data.get("scan_date", "unknown")[:10]
    linkedin_file = linkedin_dir / f"summary_{date}.md"
    with open(linkedin_file, "w") as f:
        f.write(linkedin_summary)
    print(f"LinkedIn samenvatting: {linkedin_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
