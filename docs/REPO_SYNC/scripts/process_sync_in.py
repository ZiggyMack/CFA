#!/usr/bin/env python3
"""
CFA SYNC_IN Processor

Processes incoming experiment results from ARMADA and routes them to
appropriate CFA destinations.

Usage:
    python process_sync_in.py <input_file.json>
    python process_sync_in.py SYNC_IN/pending/S7_cfa_trinity_v2_20251213.json

Output:
    - Processed summary to stdout
    - Routes data to CFA destinations (profiles, evidence, etc.)
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# CFA Repository paths (relative to repo root)
CFA_ROOT = Path(__file__).parent.parent.parent.parent.parent  # docs/Nyquist-Sync/REPO_SYNC/scripts -> root
PROFILES_DIR = CFA_ROOT / "profiles" / "worldviews"
EVIDENCE_DIR = CFA_ROOT / "auditors" / "Mission" / "Convergence_Evidence"
VUDU_DIR = CFA_ROOT / "auditors" / "Mission" / "CFA_VUDU"


def load_results(filepath: str) -> dict:
    """Load and parse ARMADA results JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_component1_summary(results: dict) -> dict:
    """Extract Component 1 (CT<->MdN) summary."""
    c1 = results.get('component1_results', {})
    summary = {
        'metrics': {},
        'avg_convergence': 0,
        'crux_count': 0,
        'total_rounds': 0
    }

    convergences = []
    for metric, data in c1.items():
        summary['metrics'][metric] = {
            'claude_score': data.get('claude_score'),
            'grok_score': data.get('grok_score'),
            'final_score': data.get('final_score'),
            'convergence': data.get('convergence'),
            'crux_declared': data.get('crux_declared', False)
        }
        if data.get('convergence'):
            convergences.append(data['convergence'])
        if data.get('crux_declared'):
            summary['crux_count'] += 1
        summary['total_rounds'] += data.get('rounds_taken', 0)

    if convergences:
        summary['avg_convergence'] = sum(convergences) / len(convergences)

    return summary


def extract_component2_summary(results: dict) -> dict:
    """Extract Component 2 (Axioms Review) summary."""
    c2 = results.get('component2_results', {})
    return {
        'grok': {
            'sign_off': c2.get('grok', {}).get('sign_off'),
            'word_count': c2.get('grok', {}).get('word_count')
        },
        'nova': {
            'sign_off': c2.get('nova', {}).get('sign_off'),
            'word_count': c2.get('nova', {}).get('word_count')
        }
    }


def generate_convergence_report(results: dict, session_id: str) -> str:
    """Generate a markdown convergence evidence report."""
    c1_summary = extract_component1_summary(results)
    c2_summary = extract_component2_summary(results)

    report = f"""# Convergence Evidence: {session_id}

**Generated:** {datetime.now().isoformat()}
**Source:** ARMADA Trinity Experiment

---

## Component 1: CT<->MdN Pilot

| Metric | Claude | Grok | Final | Convergence | Crux? |
|--------|--------|------|-------|-------------|-------|
"""

    for metric, data in c1_summary['metrics'].items():
        crux = "YES" if data['crux_declared'] else "no"
        conv = f"{data['convergence']*100:.1f}%" if data['convergence'] else "N/A"
        report += f"| {metric} | {data['claude_score']} | {data['grok_score']} | {data['final_score']} | {conv} | {crux} |\n"

    report += f"""
**Average Convergence:** {c1_summary['avg_convergence']*100:.1f}%
**Crux Points Declared:** {c1_summary['crux_count']}
**Total Rounds:** {c1_summary['total_rounds']}

---

## Component 2: Axioms Review

| Auditor | Sign-Off | Word Count |
|---------|----------|------------|
| Grok | {c2_summary['grok']['sign_off']} | {c2_summary['grok']['word_count']} |
| Nova | {c2_summary['nova']['sign_off']} | {c2_summary['nova']['word_count']} |

---

## Routing Status

- [ ] CT<->MdN scores routed to worldview profiles
- [ ] Crux Points documented
- [ ] Sign-offs recorded in CFA_VUDU
- [ ] Drift data analyzed

---

> "Three minds. One network. Zero assumptions."
"""
    return report


def print_summary(results: dict):
    """Print human-readable summary to stdout."""
    session_id = results.get('session_id', 'UNKNOWN')
    timestamp = results.get('timestamp', 'UNKNOWN')

    c1_summary = extract_component1_summary(results)
    c2_summary = extract_component2_summary(results)

    print("=" * 60)
    print("CFA SYNC_IN PROCESSOR")
    print("=" * 60)
    print(f"Session: {session_id}")
    print(f"Timestamp: {timestamp}")
    print()

    print("COMPONENT 1: CT<->MdN Pilot")
    print("-" * 40)
    for metric, data in c1_summary['metrics'].items():
        conv = f"{data['convergence']*100:.1f}%" if data['convergence'] else "N/A"
        crux = " [CRUX]" if data['crux_declared'] else ""
        print(f"  {metric}: Claude={data['claude_score']}, Grok={data['grok_score']}, Conv={conv}{crux}")

    print(f"\n  Average Convergence: {c1_summary['avg_convergence']*100:.1f}%")
    print(f"  Crux Points: {c1_summary['crux_count']}")

    print()
    print("COMPONENT 2: Axioms Review")
    print("-" * 40)
    print(f"  Grok: {c2_summary['grok']['sign_off']} ({c2_summary['grok']['word_count']} words)")
    print(f"  Nova: {c2_summary['nova']['sign_off']} ({c2_summary['nova']['word_count']} words)")

    print()
    print("=" * 60)
    print("ROUTING RECOMMENDATIONS")
    print("=" * 60)
    print(f"1. Create convergence evidence file in: {EVIDENCE_DIR}")
    if c1_summary['crux_count'] > 0:
        print(f"2. Document {c1_summary['crux_count']} Crux Point(s)")
    print(f"3. Update worldview profiles in: {PROFILES_DIR}")
    print(f"4. Record sign-offs in: {VUDU_DIR}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python process_sync_in.py <input_file.json>")
        print()
        print("Example:")
        print("  python process_sync_in.py SYNC_IN/pending/S7_cfa_trinity_v2_20251213.json")
        sys.exit(1)

    input_file = sys.argv[1]

    if not Path(input_file).exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    try:
        results = load_results(input_file)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)

    # Print summary
    print_summary(results)

    # Generate report
    session_id = results.get('session_id', datetime.now().strftime('%Y%m%d_%H%M%S'))
    report = generate_convergence_report(results, session_id)

    # Save report preview
    print()
    print("=" * 60)
    print("GENERATED REPORT PREVIEW")
    print("=" * 60)
    print(report[:500] + "...")

    # Prompt for action
    print()
    print("To save the full report, run:")
    print(f"  python process_sync_in.py {input_file} --save")


if __name__ == "__main__":
    main()
