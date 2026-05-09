#!/usr/bin/env python3
"""
rescan.py — One-command full rescan + regenerate + deploy.

Usage: python3 tools/rescan.py [--deploy]

Stappen:
1. Scan alle repos (repo_scanner.py)
2. Genereer rapporten (report_generator.py)
3. Update aigovernance/index.html met nieuwe cijfers
4. Update CHRISTIANS_CAPABILITY_PROFILE.md met nieuwe cijfers
5. Optioneel: deploy naar icthorse.nl (--deploy)
6. Print samenvatting met delta t.o.v. vorige scan
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
METRICS_DIR = PROJECT_ROOT / "evidence" / "metrics"
ICTHORSE = Path.home() / "Documents" / "Gemini_Projects" / "iCt_Horse"
AIGOVERNANCE_HTML = ICTHORSE / "aigovernance" / "index.html"
BD_VS_D1 = Path.home() / "Documents" / "Gemini_Projects" / "BluedolphinVSDragon1"
CAPABILITY_PROFILE = BD_VS_D1 / "CHRISTIANS_CAPABILITY_PROFILE.md"


def load_previous_scan():
    """Laad de vorige scan voor delta-berekening."""
    scans = sorted(METRICS_DIR.glob("scan_*.json"))
    if len(scans) < 2:
        return None
    with open(scans[-2]) as f:
        return json.load(f)


def run_scan():
    """Draai repo_scanner.py."""
    print("\n" + "=" * 60)
    print("STAP 1: Repo scan")
    print("=" * 60)
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "repo_scanner.py")],
        capture_output=True, text=True, timeout=120
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"FOUT: {result.stderr}")
        return False
    return True


def run_reports():
    """Draai report_generator.py."""
    print("\n" + "=" * 60)
    print("STAP 2: Rapporten genereren")
    print("=" * 60)
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "report_generator.py")],
        capture_output=True, text=True, timeout=60
    )
    print(result.stdout)
    return result.returncode == 0


def load_latest_scan():
    """Laad de nieuwste scan."""
    latest = METRICS_DIR / "latest_scan.json"
    with open(latest) as f:
        return json.load(f)


def update_html(scan_data):
    """Update aigovernance/index.html met nieuwe cijfers."""
    print("\n" + "=" * 60)
    print("STAP 3: Update aigovernance HTML")
    print("=" * 60)

    if not AIGOVERNANCE_HTML.exists():
        print(f"  SKIP: {AIGOVERNANCE_HTML} niet gevonden")
        return False

    html = AIGOVERNANCE_HTML.read_text()
    s = scan_data["summary"]

    # Update hero stats (data-target attributen)
    replacements = {
        # Repos count
        r'(data-target=")(\d+)(">\d*</span>\s*<span class="label">Repositories)':
            f'\\g<1>{s["total_repos"]}\\g<3>',
        # Commits count
        r'(data-target=")(\d+)(">\d*</span>\s*<span class="label">AI Co-Authored Commits)':
            f'\\g<1>{s["agent_collaboration"]["claude_co_authored"]}\\g<3>',
        # Memories count
        r'(data-target=")(\d+)(">\d*</span>\s*<span class="label">Persistent Memories)':
            f'\\g<1>{s["memory_system"]["total_memories"]}\\g<3>',
        # Constraint % (hero)
        r'(data-target=")(\d+)(" data-suffix="%">\d*</span>\s*<span class="label">Constraint Coverage)':
            f'\\g<1>{int(s["constraint_coverage"]["percentage"])}\\g<3>',
    }

    for pattern, replacement in replacements.items():
        html = re.sub(pattern, replacement, html)

    # Update scan date
    today = datetime.now().strftime('%Y-%m-%d')
    html = re.sub(
        r'Last scan: <code>[^<]+</code>',
        f'Last scan: <code>{today}</code>',
        html
    )

    # Update "Live scan data" badge
    html = re.sub(
        r'Live scan data — \d+ repositories',
        f'Live scan data — {s["total_repos"]} repositories',
        html
    )

    AIGOVERNANCE_HTML.write_text(html)
    print(f"  OK: {AIGOVERNANCE_HTML}")
    return True


def deploy():
    """Deploy naar icthorse.nl via rsync + cache purge."""
    print("\n" + "=" * 60)
    print("STAP 5: Deploy naar icthorse.nl")
    print("=" * 60)

    aigovernance_dir = ICTHORSE / "aigovernance"

    # Rsync
    result = subprocess.run([
        "rsync", "-avz",
        "-e", "ssh -p 65002 -i ~/.ssh/mindbodynjoy_hostinger",
        str(aigovernance_dir) + "/",
        "u753337840@92.113.19.221:~/domains/icthorse.nl/public_html/aigovernance/"
    ], capture_output=True, text=True, timeout=30)
    print(result.stdout)

    # Cache purge
    result = subprocess.run([
        "ssh", "-p", "65002", "-i", os.path.expanduser("~/.ssh/mindbodynjoy_hostinger"),
        "u753337840@92.113.19.221",
        "cd ~/domains/icthorse.nl/public_html && wp litespeed-purge all"
    ], capture_output=True, text=True, timeout=15)
    print(f"  Cache purge: {result.stdout.strip()}")

    return True


def update_mark_outputs(scan_data):
    """Update Mark Paauwe WhatsApp teaser en email met scan data."""
    print("\n" + "=" * 60)
    print("STAP 4: Update Mark Paauwe outputs")
    print("=" * 60)

    s = scan_data["summary"]
    mark_dir = PROJECT_ROOT / "reports" / "mark_paauwe"
    mark_dir.mkdir(parents=True, exist_ok=True)

    # WhatsApp teaser — update cijfers
    teaser_path = mark_dir / "whatsapp_teaser.md"
    if teaser_path.exists():
        teaser = teaser_path.read_text()
        # Update de harde cijfers
        commits = s["agent_collaboration"]["claude_co_authored"]
        commits_fmt = f"{commits:,}".replace(",", ".")
        teaser = re.sub(r'[\d.]+ AI co-authored commits',
                       f'{commits_fmt} AI co-authored commits', teaser)
        teaser = re.sub(r'\d+% constraint coverage',
                       f'{int(s["constraint_coverage"]["percentage"])}% constraint coverage', teaser)
        teaser = re.sub(r'\d+ feedback loops',
                       f'{s["memory_system"]["feedback_memories"]} feedback loops', teaser)
        teaser = re.sub(r'\d+ principes in Dragon1-formaat',
                       '25 principes in Dragon1-formaat', teaser)
        teaser = re.sub(r'al mijn \d+ repos',
                       f'al mijn {s["total_repos"]} repos', teaser)
        teaser_path.write_text(teaser)
        print(f"  OK: {teaser_path.name}")

    # Email — update cijfers in de tabel
    email_path = mark_dir / "email_mark.md"
    if email_path.exists():
        email = email_path.read_text()
        updates = {
            r'Repositories beheerd \| \d+': f'Repositories beheerd | {s["total_repos"]}',
            r'AI co-authored commits \| [\d.]+': f'AI co-authored commits | {s["agent_collaboration"]["claude_co_authored"]:,}'.replace(',', '.'),
            r'Constraint coverage.*?\| [\d,]+%': f'Constraint coverage (CLAUDE.md) | {s["constraint_coverage"]["percentage"]}%',
            r'Persistent memories \| \d+': f'Persistent memories | {s["memory_system"]["total_memories"]}',
            r'Feedback loops.*?\| \d+': f'Feedback loops (geleerde lessen) | {s["memory_system"]["feedback_memories"]}',
            r'WhatIf protocol adoptie \| [\d,]+%': f'WhatIf protocol adoptie | {s["protocol_adoption"]["whatif"]["percentage"]}%',
            r'Versioning discipline \| [\d,]+%': f'Versioning discipline | {s["protocol_adoption"]["versioning"]["percentage"]}%',
        }
        for pattern, replacement in updates.items():
            email = re.sub(pattern, replacement, email)
        email_path.write_text(email)
        print(f"  OK: {email_path.name}")

    return True


def print_delta(previous, current):
    """Print delta tussen vorige en huidige scan."""
    if not previous:
        print("\n  (geen vorige scan beschikbaar voor delta)")
        return

    ps = previous["summary"]
    cs = current["summary"]

    print("\n" + "=" * 60)
    print("DELTA t.o.v. vorige scan")
    print("=" * 60)

    deltas = [
        ("Repos", ps["total_repos"], cs["total_repos"]),
        ("Constraint coverage", f'{ps["constraint_coverage"]["percentage"]}%',
         f'{cs["constraint_coverage"]["percentage"]}%'),
        ("Claude commits", ps["agent_collaboration"]["claude_co_authored"],
         cs["agent_collaboration"]["claude_co_authored"]),
        ("Memories", ps["memory_system"]["total_memories"],
         cs["memory_system"]["total_memories"]),
        ("Feedback memories", ps["memory_system"]["feedback_memories"],
         cs["memory_system"]["feedback_memories"]),
        ("WhatIf adoptie", f'{ps["protocol_adoption"]["whatif"]["percentage"]}%',
         f'{cs["protocol_adoption"]["whatif"]["percentage"]}%'),
        ("Versioning", f'{ps["protocol_adoption"]["versioning"]["percentage"]}%',
         f'{cs["protocol_adoption"]["versioning"]["percentage"]}%'),
    ]

    for label, prev_val, curr_val in deltas:
        if str(prev_val) != str(curr_val):
            print(f"  {label}: {prev_val} → {curr_val}")
        else:
            print(f"  {label}: {curr_val} (ongewijzigd)")

    print(f"\n  Vorige scan: {previous.get('scan_date', '?')[:19]}")
    print(f"  Huidige scan: {current.get('scan_date', '?')[:19]}")


def main():
    do_deploy = "--deploy" in sys.argv

    print("=" * 60)
    print("AiArchitecture — Full Rescan")
    print(f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Deploy: {'JA' if do_deploy else 'NEE (gebruik --deploy)'}")
    print("=" * 60)

    # Laad vorige scan voor delta
    previous = load_previous_scan()

    # Stap 1: Scan
    if not run_scan():
        print("FOUT bij scan")
        return 1

    # Stap 2: Rapporten
    run_reports()

    # Laad nieuwe scan
    current = load_latest_scan()

    # Stap 3: Update HTML
    update_html(current)

    # Stap 4: Update Mark Paauwe outputs
    update_mark_outputs(current)

    # Stap 5: Delta
    print_delta(previous, current)

    # Stap 6: Deploy
    if do_deploy:
        deploy()
    else:
        print("\n  TIP: Gebruik --deploy om direct naar icthorse.nl te deployen")

    print("\n" + "=" * 60)
    print("KLAAR")
    print("=" * 60)
    print(f"\n  Dashboard:  icthorse.nl/aigovernance")
    print(f"  Artikel:    icthorse.nl/aigovernance/article.html")
    print(f"  GitHub:     github.com/cpaglebbeek/AiArchitecture")
    print(f"  Rapport:    reports/latest_scan.md")
    print(f"  LinkedIn:   reports/linkedin/summary_{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"  Mark WA:    reports/mark_paauwe/whatsapp_teaser.md")
    print(f"  Mark Email: reports/mark_paauwe/email_mark.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
