#!/usr/bin/env python3
"""
repo_scanner.py — Scant alle repositories uit PROJECTS.json op AI-praktijken.

Leest Meta_Master/PROJECTS.json als bron van waarheid en analyseert elke repo op:
- CLAUDE.md aanwezigheid en grootte
- Memory bestanden
- Protocol markers (WhatIf, RCA, versioning)
- git-crypt gebruik
- Agent co-authored commits
- Versioning discipline
- Sessiedocumentatie

Output: evidence/metrics/scan_<datum>.json
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Paden
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
META_MASTER = Path.home() / "Documents" / "Gemini_Projects" / "Meta_Master"
PROJECTS_JSON = META_MASTER / "PROJECTS.json"
MEMORY_DIR = Path.home() / ".claude" / "projects" / "-Users-christian" / "memory"
OUTPUT_DIR = PROJECT_ROOT / "evidence" / "metrics"


def load_projects():
    """Laad PROJECTS.json."""
    with open(PROJECTS_JSON, "r") as f:
        return json.load(f)


def scan_repo(repo_info):
    """Scan een individuele repo op AI-praktijken."""
    local_path = Path(repo_info.get("localPath", ""))
    result = {
        "name": repo_info.get("name", "unknown"),
        "localPath": str(local_path),
        "github": repo_info.get("github"),
        "exists": local_path.exists(),
        "is_git_repo": (local_path / ".git").exists() if local_path.exists() else False,
    }

    if not result["exists"] or not result["is_git_repo"]:
        return result

    # 1. CLAUDE.md aanwezigheid
    claude_md = local_path / "CLAUDE.md"
    result["has_claude_md"] = claude_md.exists()
    if claude_md.exists():
        result["claude_md_lines"] = len(claude_md.read_text(errors="replace").splitlines())
    else:
        result["claude_md_lines"] = 0

    # 2. ARCHITECTURE.md
    arch_md = local_path / "ARCHITECTURE.md"
    result["has_architecture_md"] = arch_md.exists()

    # 3. Versioning bestanden
    result["has_version_json"] = (local_path / "version.json").exists()
    result["has_package_json"] = (local_path / "package.json").exists()

    # 4. git-crypt
    result["has_git_crypt"] = (local_path / ".git-crypt").exists()

    # 5. Sessiedocumentatie
    prompts_dir = local_path / "prompts"
    sessions_dir = local_path / "sessions"
    result["has_session_docs"] = prompts_dir.exists() or sessions_dir.exists()
    session_count = 0
    for d in [prompts_dir, sessions_dir]:
        if d.exists():
            session_count += len(list(d.glob("*.md")))
    result["session_doc_count"] = session_count

    # 6. DESIGN_TOKENS.md
    result["has_design_tokens"] = (local_path / "DESIGN_TOKENS.md").exists()

    # 7. docs/ directory
    docs_dir = local_path / "docs"
    result["has_docs_dir"] = docs_dir.exists()
    if docs_dir.exists():
        result["docs_file_count"] = len(list(docs_dir.rglob("*.md")))
    else:
        result["docs_file_count"] = 0

    # 8. Agent co-authored commits (laatste 100)
    try:
        git_log = subprocess.run(
            ["git", "-C", str(local_path), "log", "--oneline", "-100", "--format=%s %b"],
            capture_output=True, text=True, timeout=10
        )
        log_text = git_log.stdout
        result["claude_commits"] = log_text.lower().count("co-authored-by: claude")
        result["gemini_commits"] = log_text.lower().count("co-authored-by: gemini")
        result["codex_commits"] = log_text.lower().count("co-authored-by: codex")
        result["chatgpt_commits"] = log_text.lower().count("co-authored-by: chatgpt")

        # Totaal commits
        total = subprocess.run(
            ["git", "-C", str(local_path), "rev-list", "--count", "HEAD"],
            capture_output=True, text=True, timeout=10
        )
        result["total_commits"] = int(total.stdout.strip()) if total.returncode == 0 else 0
    except (subprocess.TimeoutExpired, Exception):
        result["claude_commits"] = 0
        result["gemini_commits"] = 0
        result["codex_commits"] = 0
        result["chatgpt_commits"] = 0
        result["total_commits"] = 0

    # 9. Protocol markers in CLAUDE.md
    if result["has_claude_md"]:
        claude_content = claude_md.read_text(errors="replace").lower()
        result["protocols"] = {
            "whatif": "whatif" in claude_content,
            "rca": "root cause" in claude_content or "rca" in claude_content,
            "versioning": "versioning" in claude_content or "versie" in claude_content,
            "debug_protocol": "debug" in claude_content and "protocol" in claude_content,
            "build_protocol": "build" in claude_content and "protocol" in claude_content,
            "over_en_uit": "over en uit" in claude_content or "oeu" in claude_content,
            "color_coding": "groen" in claude_content or "oranje" in claude_content or "rood" in claude_content,
            "codename": "codenaam" in claude_content or "codename" in claude_content,
        }
    else:
        result["protocols"] = {}

    return result


def scan_memory():
    """Scan het Claude memory systeem."""
    if not MEMORY_DIR.exists():
        return {"exists": False}

    memory_files = list(MEMORY_DIR.glob("*.md"))
    memory_index = MEMORY_DIR / "MEMORY.md"

    result = {
        "exists": True,
        "total_files": len(memory_files),
        "index_exists": memory_index.exists(),
        "types": {"user": 0, "feedback": 0, "project": 0, "reference": 0, "unknown": 0},
        "total_lines": 0,
    }

    for mf in memory_files:
        if mf.name == "MEMORY.md":
            continue
        content = mf.read_text(errors="replace")
        result["total_lines"] += len(content.splitlines())

        # Type detectie uit frontmatter
        if "type: user" in content:
            result["types"]["user"] += 1
        elif "type: feedback" in content:
            result["types"]["feedback"] += 1
        elif "type: project" in content:
            result["types"]["project"] += 1
        elif "type: reference" in content:
            result["types"]["reference"] += 1
        else:
            result["types"]["unknown"] += 1

    return result


def scan_sync_files():
    """Scan cross-agent sync bestanden."""
    sync_dirs = {
        "gemini": Path.home() / ".gemini" / "tmp" / "claude_sync",
        "codex": Path.home() / ".codex" / "tmp" / "claude_sync",
    }

    result = {}
    for agent, sync_dir in sync_dirs.items():
        if sync_dir.exists():
            files = list(sync_dir.glob("*.json"))
            result[agent] = {
                "exists": True,
                "file_count": len(files),
                "files": [f.name for f in files],
                "last_modified": max(
                    (f.stat().st_mtime for f in files), default=0
                ),
            }
            if result[agent]["last_modified"] > 0:
                result[agent]["last_modified_date"] = datetime.fromtimestamp(
                    result[agent]["last_modified"]
                ).isoformat()
        else:
            result[agent] = {"exists": False}

    return result


def calculate_summary(repos, memory, sync):
    """Bereken samenvattende metrics."""
    active_repos = [r for r in repos if r["exists"] and r["is_git_repo"]]
    total = len(active_repos)

    if total == 0:
        return {"error": "Geen actieve repos gevonden"}

    # Constraint coverage
    with_claude_md = sum(1 for r in active_repos if r.get("has_claude_md", False))

    # Architecture docs
    with_arch = sum(1 for r in active_repos if r.get("has_architecture_md", False))

    # Security
    with_git_crypt = sum(1 for r in active_repos if r.get("has_git_crypt", False))

    # Session docs
    with_sessions = sum(1 for r in active_repos if r.get("has_session_docs", False))
    total_sessions = sum(r.get("session_doc_count", 0) for r in active_repos)

    # Agent commits
    total_claude = sum(r.get("claude_commits", 0) for r in active_repos)
    total_gemini = sum(r.get("gemini_commits", 0) for r in active_repos)
    total_codex = sum(r.get("codex_commits", 0) for r in active_repos)
    total_chatgpt = sum(r.get("chatgpt_commits", 0) for r in active_repos)
    total_commits = sum(r.get("total_commits", 0) for r in active_repos)

    # Protocol adoption (alleen repos met CLAUDE.md)
    protocol_counts = {}
    repos_with_claude = [r for r in active_repos if r.get("has_claude_md", False)]
    if repos_with_claude:
        for protocol_name in ["whatif", "rca", "versioning", "debug_protocol",
                               "build_protocol", "over_en_uit", "color_coding", "codename"]:
            count = sum(1 for r in repos_with_claude
                       if r.get("protocols", {}).get(protocol_name, False))
            protocol_counts[protocol_name] = {
                "count": count,
                "percentage": round(count / len(repos_with_claude) * 100, 1)
            }

    # Versioning
    with_versioning = sum(1 for r in active_repos
                         if r.get("has_version_json") or r.get("has_package_json"))

    return {
        "total_repos": total,
        "constraint_coverage": {
            "repos_with_claude_md": with_claude_md,
            "percentage": round(with_claude_md / total * 100, 1),
            "avg_claude_md_lines": round(
                sum(r.get("claude_md_lines", 0) for r in active_repos) / max(with_claude_md, 1), 1
            ),
        },
        "architecture_docs": {
            "repos_with_architecture_md": with_arch,
            "percentage": round(with_arch / total * 100, 1),
        },
        "security_posture": {
            "repos_with_git_crypt": with_git_crypt,
            "percentage": round(with_git_crypt / total * 100, 1),
        },
        "session_documentation": {
            "repos_with_sessions": with_sessions,
            "total_session_docs": total_sessions,
        },
        "agent_collaboration": {
            "total_commits_scanned": total_commits,
            "claude_co_authored": total_claude,
            "gemini_co_authored": total_gemini,
            "codex_co_authored": total_codex,
            "chatgpt_co_authored": total_chatgpt,
            "agents_active": sum(1 for c in [total_claude, total_gemini, total_codex, total_chatgpt] if c > 0),
        },
        "protocol_adoption": protocol_counts,
        "versioning_discipline": {
            "repos_with_versioning": with_versioning,
            "percentage": round(with_versioning / total * 100, 1),
        },
        "memory_system": {
            "total_memories": memory.get("total_files", 0),
            "feedback_memories": memory.get("types", {}).get("feedback", 0),
            "project_memories": memory.get("types", {}).get("project", 0),
            "user_memories": memory.get("types", {}).get("user", 0),
            "reference_memories": memory.get("types", {}).get("reference", 0),
        },
        "cross_agent_sync": {
            "gemini_sync_active": sync.get("gemini", {}).get("exists", False),
            "codex_sync_active": sync.get("codex", {}).get("exists", False),
        },
    }


def main():
    print("=" * 60)
    print("AiArchitecture — Repo Scanner")
    print(f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Laad projecten
    print("\n📂 Laden PROJECTS.json...")
    data = load_projects()

    # Verzamel alle repos
    all_repos = []
    for eco_name, eco_data in data.get("ecosystems", {}).items():
        repos = eco_data.get("repos", [])
        for repo in repos:
            repo["ecosystem"] = eco_name
            all_repos.append(repo)

    print(f"   Gevonden: {len(all_repos)} repos in {len(data.get('ecosystems', {}))} ecosystemen")

    # Scan repos
    print("\n🔍 Scannen repositories...")
    scan_results = []
    for repo in all_repos:
        result = scan_repo(repo)
        result["ecosystem"] = repo.get("ecosystem", "unknown")
        scan_results.append(result)
        status = "✓" if result.get("has_claude_md") else "✗"
        if result["exists"]:
            print(f"   {status} {result['name']}")
        else:
            print(f"   ⚠ {result['name']} (niet gevonden: {result['localPath']})")

    # Scan memory
    print("\n🧠 Scannen memory systeem...")
    memory_results = scan_memory()
    print(f"   {memory_results.get('total_files', 0)} memory bestanden")

    # Scan sync files
    print("\n🔄 Scannen sync bestanden...")
    sync_results = scan_sync_files()
    for agent, info in sync_results.items():
        status = "actief" if info.get("exists") else "niet gevonden"
        print(f"   {agent}: {status}")

    # Bereken samenvatting
    print("\n📊 Berekenen metrics...")
    summary = calculate_summary(scan_results, memory_results, sync_results)

    # Output
    output = {
        "scan_date": datetime.now().isoformat(),
        "scanner_version": "1.0.0",
        "source": str(PROJECTS_JSON),
        "summary": summary,
        "repos": scan_results,
        "memory": memory_results,
        "sync": sync_results,
    }

    # Schrijf naar bestand
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2, default=str)

    # Ook latest symlink/copy
    latest_file = OUTPUT_DIR / "latest_scan.json"
    with open(latest_file, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n✅ Scan compleet → {output_file}")

    # Toon samenvatting
    print("\n" + "=" * 60)
    print("SAMENVATTING")
    print("=" * 60)
    s = summary
    print(f"\n📦 Repositories:          {s['total_repos']}")
    print(f"📋 Constraint Coverage:   {s['constraint_coverage']['repos_with_claude_md']}/{s['total_repos']} ({s['constraint_coverage']['percentage']}%)")
    print(f"🏗️  Architecture Docs:     {s['architecture_docs']['repos_with_architecture_md']}/{s['total_repos']} ({s['architecture_docs']['percentage']}%)")
    print(f"🔒 git-crypt Repos:       {s['security_posture']['repos_with_git_crypt']}/{s['total_repos']} ({s['security_posture']['percentage']}%)")
    print(f"📝 Versioning:            {s['versioning_discipline']['repos_with_versioning']}/{s['total_repos']} ({s['versioning_discipline']['percentage']}%)")
    print(f"\n🤖 Agent Co-Authored Commits (laatste 100/repo):")
    ac = s['agent_collaboration']
    print(f"   Claude:  {ac['claude_co_authored']}")
    print(f"   Gemini:  {ac['gemini_co_authored']}")
    print(f"   Codex:   {ac['codex_co_authored']}")
    print(f"   ChatGPT: {ac['chatgpt_co_authored']}")
    print(f"   Agents actief: {ac['agents_active']}/4")
    print(f"\n🧠 Memory Systeem:")
    ms = s['memory_system']
    print(f"   Totaal:    {ms['total_memories']}")
    print(f"   Feedback:  {ms['feedback_memories']}")
    print(f"   Project:   {ms['project_memories']}")
    print(f"   User:      {ms['user_memories']}")
    print(f"   Reference: {ms['reference_memories']}")

    if s.get('protocol_adoption'):
        print(f"\n📐 Protocol Adoption (repos met CLAUDE.md):")
        for proto, info in s['protocol_adoption'].items():
            print(f"   {proto}: {info['count']} ({info['percentage']}%)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
