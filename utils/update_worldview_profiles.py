#!/usr/bin/env python3
"""
Script to add Table of Contents and Steel-Manning Guide to all worldview profiles.
Part of B-STORM_4 unified architecture implementation.
"""

import re
from pathlib import Path

# Profiles directory
PROFILES_DIR = Path("d:/Documents/CFA/profiles/worldviews")

# Already completed
COMPLETED = ["CLASSICAL_THEISM.md", "METHODOLOGICAL_NATURALISM.md"]

# Remaining profiles to update
REMAINING = [
    "BUDDHISM.md",
    "DESIDERATA_BELIEVERS.md",
    "ERROR_THEORY.md",
    "EXISTENTIALISM.md",
    "HINDUISM.md",
    "ISLAM.md",
    "MORMONISM.md",
    "NULL_HYPOTHESIS.md",
    "ORTHODOX_JUDAISM.md",
    "PROCESS_THEOLOGY.md",
]


def get_profile_short_name(filename):
    """Extract short name from filename"""
    mapping = {
        "BUDDHISM.md": ("Buddhism", "Bdh"),
        "DESIDERATA_BELIEVERS.md": ("Desiderata Believers", "DB"),
        "ERROR_THEORY.md": ("Error Theory", "ET"),
        "EXISTENTIALISM.md": ("Existentialism", "Ext"),
        "HINDUISM.md": ("Hinduism", "Hnd"),
        "ISLAM.md": ("Islam", "Isl"),
        "MORMONISM.md": ("Mormonism", "Mor"),
        "NULL_HYPOTHESIS.md": ("Null Hypothesis", "NH"),
        "ORTHODOX_JUDAISM.md": ("Orthodox Judaism", "OJ"),
        "PROCESS_THEOLOGY.md": ("Process Theology", "PT"),
    }
    return mapping.get(filename, (filename.replace(".md", "").title(), "XX"))


def get_auditor_assignments(worldview_name):
    """
    Determine which auditors take PRO/ANTI stances for each worldview.
    This is a heuristic based on natural lens alignment.
    """
    assignments = {
        # Theistic traditions - Claude PRO (teleological), Grok ANTI (empirical)
        "Buddhism": ("Claude", "Teleological lens aligns with purpose/enlightenment", "Grok", "Empirical lens challenges metaphysical claims"),
        "Hinduism": ("Claude", "Teleological lens aligns with dharma/cosmic purpose", "Grok", "Empirical lens challenges non-empirical metaphysics"),
        "Islam": ("Claude", "Teleological lens aligns with divine will/purpose", "Grok", "Empirical lens challenges theological claims"),
        "Orthodox Judaism": ("Claude", "Teleological lens aligns with covenantal purpose", "Grok", "Empirical lens challenges theological claims"),
        "Mormonism": ("Claude", "Teleological lens aligns with eternal progression", "Grok", "Empirical lens challenges theological claims"),
        "Process Theology": ("Claude", "Teleological lens aligns with becoming/development", "Grok", "Empirical lens challenges speculative metaphysics"),

        # Naturalistic/skeptical - Grok PRO (empirical), Claude ANTI (teleological)
        "Desiderata Believers": ("Grok", "Empirical lens aligns with pragmatic epistemology", "Claude", "Teleological lens challenges lack of meaning framework"),
        "Error Theory": ("Grok", "Empirical lens aligns with moral skepticism", "Claude", "Teleological lens challenges moral nihilism"),
        "Null Hypothesis": ("Grok", "Empirical lens aligns with epistemic minimalism", "Claude", "Teleological lens challenges meaning vacuum"),

        # Existentialist - balanced (Nova can assign dynamically)
        "Existentialism": ("Claude", "Teleological lens can frame authentic meaning-making", "Grok", "Empirical lens challenges subjective meaning claims"),
    }

    return assignments.get(worldview_name, ("Claude", "Default PRO", "Grok", "Default ANTI"))


def generate_toc(worldview_name, short_name):
    """Generate Table of Contents section"""
    return f"""## 📑 Table of Contents

**Core Sections:**
- [Metadata](#metadata) — Line TBD
- [YPA Application Data](#ypa-application-data-cfa-v35) — Line TBD
- [Mr. Brute's Ledger](#mr-brutes-ledger) — Line TBD
- [Philosophical Foundations](#philosophical-foundations) — Line TBD
- [Steel-Manning Guide](#steel-manning-guide) — Line TBD
  - [PRO-{short_name} Stance](#pro-{short_name.lower().replace(' ', '-')}-stance) — Line TBD
  - [ANTI-{short_name} Stance](#anti-{short_name.lower().replace(' ', '-')}-stance) — Line TBD
- [Metrics](#metrics) — Line TBD
- [Lifecycle Hooks](#lifecycle-hooks) — Line TBD

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-{short_name.lower().replace(' ', '-')}-stance) | [ANTI Stance](#anti-{short_name.lower().replace(' ', '-')}-stance)
- 👥 **Users:** [What is {worldview_name}?](#philosophical-foundations) | [Axioms & Debts](#mr-brutes-ledger)

---"""


def generate_steel_manning_guide(worldview_name, short_name):
    """Generate Steel-Manning Guide section"""
    pro_auditor, pro_reason, anti_auditor, anti_reason = get_auditor_assignments(worldview_name)

    return f"""## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on {worldview_name}. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-{short_name} Stance:** {pro_auditor} - {pro_reason}
- **ANTI-{short_name} Stance:** {anti_auditor} - {anti_reason}
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via AUDITOR_ASSIGNMENTS.md

---

### PRO-{worldview_name} Stance

**Mission:** Advocate for {worldview_name}'s explanatory power, coherence, and capacity to address fundamental questions.

**What to Emphasize:**
- [Profile maintainer to fill: Key strengths of this worldview]
- [Profile maintainer to fill: Historical/cultural robustness]
- [Profile maintainer to fill: Explanatory scope]
- [Profile maintainer to fill: Transformative capacity]
- [Profile maintainer to fill: Unique philosophical contributions]

**What to Acknowledge (Honest Advocacy):**
- [Profile maintainer to fill: Legitimate critiques and challenges]
- [Profile maintainer to fill: Areas of epistemic uncertainty]
- [Profile maintainer to fill: Competitor worldview strengths]

**Scoring Calibration:**

```yaml
pro_{short_name.lower().replace(' ', '_')}_bias_adjustment:
  # When scoring {worldview_name} from PRO stance
  axiom_confidence: TBD  # Confidence in core axioms (0.0-1.0)
  burden_of_proof: TBD   # Where to place evidential burden (0.0-1.0, low=on critics, high=on worldview)
  charity_interpretation: TBD  # How favorably to interpret ambiguous claims (0.0-1.0)
  edge_case_weight: TBD  # How much to weight counterexamples (0.0-1.0, low=exceptions, high=refutations)
  explanatory_credit: TBD  # How much credit for addressing questions (0.0-1.0)
  historical_weight: TBD  # Weight of historical/cultural staying power (0.0-1.0)
  lived_experience: TBD  # Weight of transformative capacity (0.0-1.0)
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- [Profile maintainer to fill: How teleological lens engages PRO stance]

**Grok (Empirical):**
- [Profile maintainer to fill: How empirical lens engages PRO stance]

**Nova (Symmetry):**
- [Profile maintainer to fill: How symmetry lens engages PRO stance]

**Success Criteria:**
- Score reflects {worldview_name}'s genuine strengths
- Critiques are acknowledged but framed appropriately
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-{worldview_name} Stance

**Mission:** Challenge {worldview_name}'s coherence, evidential support, and capacity to address key philosophical questions.

**What to Emphasize:**
- [Profile maintainer to fill: Key weaknesses and critiques]
- [Profile maintainer to fill: Explanatory gaps or failures]
- [Profile maintainer to fill: Incoherence charges]
- [Profile maintainer to fill: Competitor worldview advantages]
- [Profile maintainer to fill: Empirical or logical challenges]

**What to Acknowledge (Honest Opposition):**
- [Profile maintainer to fill: Legitimate strengths]
- [Profile maintainer to fill: Sophisticated defenses]
- [Profile maintainer to fill: Historical robustness]

**Scoring Calibration:**

```yaml
anti_{short_name.lower().replace(' ', '_')}_bias_adjustment:
  # When scoring {worldview_name} from ANTI stance
  axiom_confidence: TBD  # Low confidence in core axioms
  burden_of_proof: TBD   # Place burden on worldview to prove claims
  charity_interpretation: TBD  # Interpret ambiguous claims neutrally or skeptically
  edge_case_weight: TBD  # Upweight counterexamples as systematic problems
  explanatory_credit: TBD  # Require conclusive not just suggestive explanations
  historical_weight: TBD  # Discount or contextualize historical staying power
  lived_experience: TBD  # Weight transformative capacity appropriately
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- [Profile maintainer to fill: How teleological lens engages ANTI stance]

**Grok (Empirical):**
- [Profile maintainer to fill: How empirical lens engages ANTI stance]

**Nova (Symmetry):**
- [Profile maintainer to fill: How symmetry lens engages ANTI stance]

**Success Criteria:**
- Score reflects legitimate philosophical challenges
- Strengths are acknowledged but not overweighted
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### Adversarial Balance

**Why This Pairing Works:**

**PRO-{short_name} ({pro_auditor}):** {pro_reason}. Risk: [Profile maintainer to fill: specific risk of this pairing]

**ANTI-{short_name} ({anti_auditor}):** {anti_reason}. Risk: [Profile maintainer to fill: specific risk of this pairing]

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate strengths or ANTI scores ignore sophisticated defenses. Ensures both stances maintain intellectual honesty.

**Target:** 98% convergence after adversarial checking. If scores diverge significantly, auditors deliberate until consensus or document irreconcilable differences.

---"""


def update_profile(filepath):
    """Add ToC and Steel-Manning Guide to a profile"""
    print(f"\nProcessing {filepath.name}...")

    # Read current content
    content = filepath.read_text(encoding='utf-8')

    # Extract worldview name
    worldview_name, short_name = get_profile_short_name(filepath.name)

    # Update version in header (0.1.0 -> 0.2.0)
    content = re.sub(
        r'(\*\*Version:\*\* )0\.1\.0',
        r'\g<1>0.2.0',
        content
    )

    # Update date in header
    content = re.sub(
        r'(\*\*Date:\*\* )202[0-9]-[0-9]{2}-[0-9]{2}',
        r'\g<1>2025-11-10',
        content
    )

    # Update VERSION in comment block
    content = re.sub(
        r'(VERSION: )0\.1\.0',
        r'\g<1>0.2.0',
        content
    )

    # Update PURPOSE in comment block (only if not already updated)
    if 'steel-manning guide' not in content:
        content = re.sub(
            r'(PURPOSE: .+?)(\n)',
            r'\g<1>, and steel-manning guide for adversarial auditing\g<2>',
            content
        )

    # Update NEEDED_BY in comment block (only if not already updated)
    if 'auditor calibration' not in content or content.count('auditor calibration') < 2:
        content = re.sub(
            r'(NEEDED_BY: .+?)(\n)',
            r'\g<1>, auditor calibration\g<2>',
            content,
            count=1
        )

    # Update LAST_UPDATE in comment block
    content = re.sub(
        r'(LAST_UPDATE: ).*',
        r'\g<1>2025-11-10 [Added ToC and Steel-Manning Guide for auditor calibration]',
        content
    )

    # Find where to insert ToC (after ---\n following comment block) - only if not present
    if '📑 Table of Contents' not in content:
        toc_insertion_pattern = r'(---\n)(\n## Metadata)'
        toc_text = generate_toc(worldview_name, short_name)
        content = re.sub(toc_insertion_pattern, r'\1\n' + toc_text + r'\n\2', content)

    # Find where to insert Steel-Manning Guide (before ## Metrics) - only if not present
    if '## Steel-Manning Guide' not in content:
        steel_manning_text = generate_steel_manning_guide(worldview_name, short_name)
        metrics_pattern = r'(---\n)(\n## Metrics)'
        content = re.sub(metrics_pattern, r'\1\n' + steel_manning_text + r'\n\2', content)

    # Write back
    filepath.write_text(content, encoding='utf-8')
    print(f"[OK] Updated {filepath.name}")


def main():
    """Update all remaining profiles"""
    print("=" * 60)
    print("Worldview Profile Updater")
    print("Adding ToC and Steel-Manning Guide to all profiles")
    print("=" * 60)

    for filename in REMAINING:
        filepath = PROFILES_DIR / filename
        if not filepath.exists():
            print(f"[WARN] {filename} not found, skipping...")
            continue

        try:
            update_profile(filepath)
        except Exception as e:
            print(f"[ERROR] Error updating {filename}: {e}")

    print("\n" + "=" * 60)
    print("[OK] All profiles updated!")
    print("=" * 60)


if __name__ == "__main__":
    main()
