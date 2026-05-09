#!/usr/bin/env python3
"""
metrics_collector.py — Aggregeert scan resultaten over tijd.

Leest alle scan_*.json bestanden uit evidence/metrics/ en
produceert trends en vergelijkingen.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

METRICS_DIR = Path(__file__).parent.parent / "evidence" / "metrics"


def load_scans():
    """Laad alle scan resultaten, gesorteerd op datum."""
    scans = []
    for scan_file in sorted(METRICS_DIR.glob("scan_*.json")):
        with open(scan_file) as f:
            data = json.load(f)
            data["_file"] = scan_file.name
            scans.append(data)
    return scans


def compare_scans(scans):
    """Vergelijk eerste en laatste scan voor trends."""
    if len(scans) < 2:
        return None

    first = scans[0]["summary"]
    last = scans[-1]["summary"]

    trends = {
        "period": {
            "from": scans[0].get("scan_date", "unknown"),
            "to": scans[-1].get("scan_date", "unknown"),
            "scan_count": len(scans),
        },
        "constraint_coverage_change": (
            last["constraint_coverage"]["percentage"]
            - first["constraint_coverage"]["percentage"]
        ),
        "security_posture_change": (
            last["security_posture"]["percentage"]
            - first["security_posture"]["percentage"]
        ),
        "memory_growth": (
            last["memory_system"]["total_memories"]
            - first["memory_system"]["total_memories"]
        ),
        "repos_growth": last["total_repos"] - first["total_repos"],
    }

    return trends


def main():
    scans = load_scans()

    if not scans:
        print("Geen scan resultaten gevonden. Draai eerst repo_scanner.py.")
        return 1

    print(f"Gevonden: {len(scans)} scan(s)")

    # Laatste scan samenvatting
    latest = scans[-1]
    print(f"\nLaatste scan: {latest.get('scan_date', 'unknown')}")
    print(json.dumps(latest["summary"], indent=2))

    # Trends
    if len(scans) >= 2:
        trends = compare_scans(scans)
        print("\n--- TRENDS ---")
        print(json.dumps(trends, indent=2))

        # Schrijf trends
        output_file = METRICS_DIR / "trends.json"
        with open(output_file, "w") as f:
            json.dump(trends, f, indent=2)
        print(f"\nTrends geschreven naar {output_file}")
    else:
        print("\nNog maar 1 scan — trends worden beschikbaar na meerdere scans.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
