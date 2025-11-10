# Null Hypothesis Profile

**Status:** DRAFT | **Version:** 0.2.0 | **Date:** 2025-11-10

<!---
FILE: worldviews/NULL_HYPOTHESIS.md
PURPOSE: Worldview profile for Null Hypothesis (epistemic minimalism) with metrics, philosophical foundations, and deliberation narratives, and steel-manning guide for adversarial auditing
VERSION: 0.2.0
STATUS: DRAFT
DEPENDS_ON: ../_docs/METRIC_TAXONOMY.md, Trinity Architecture
NEEDED_BY: CFA analysis, worldview comparison tooling, auditor calibration
MOVES_WITH: /profiles/worldviews/
LAST_UPDATE: 2025-11-10 [Added ToC and Steel-Manning Guide for auditor calibration]
--->

---

## 📑 Table of Contents

**Core Sections:**
- [Metadata](#metadata) — Line TBD
- [YPA Application Data](#ypa-application-data-cfa-v35) — Line TBD
- [Mr. Brute's Ledger](#mr-brutes-ledger) — Line TBD
- [Philosophical Foundations](#philosophical-foundations) — Line TBD
- [Steel-Manning Guide](#steel-manning-guide) — Line TBD
  - [PRO-NH Stance](#pro-nh-stance) — Line TBD
  - [ANTI-NH Stance](#anti-nh-stance) — Line TBD
- [Metrics](#metrics) — Line TBD
- [Lifecycle Hooks](#lifecycle-hooks) — Line TBD

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-nh-stance) | [ANTI Stance](#anti-nh-stance)
- 👥 **Users:** [What is Null Hypothesis?](#philosophical-foundations) | [Axioms & Debts](#mr-brutes-ledger)

---

## Metadata

```yaml
profile:
  name: "Null Hypothesis"
  version: "0.1.0"
  status: "DRAFT"
  declared_axiom: "Withhold assent from all claims lacking sufficient evidence; default position is suspension of judgment rather than belief or disbelief"
  alternate_names: ["Epistemic Minimalism", "Pyrrhonian Skepticism", "Methodological Agnosticism"]
  last_updated: "2025-11-09"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null  # Will be filled during Phase 3 - Grok integration
```

---

## Philosophical Foundations

### Declared Axiom

The Null Hypothesis position begins with the axiom that the default epistemic stance toward any claim is suspension of judgment (epoché) until sufficient evidence warrants belief. Neither belief nor disbelief is the default - rather, withholding assent pending adequate justification. This applies to metaphysical claims (God, soul, afterlife), moral claims (objective values), and claims about meaning/purpose.

### Philosophical Framework

The Null Hypothesis operates within skeptical epistemology, drawing from Pyrrhonian skepticism, Humean empiricism, and contemporary epistemology's burden-of-proof frameworks. It is methodologically agnostic - not claiming knowledge that claims are false (strong atheism, moral anti-realism), but rather suspending judgment on claims lacking sufficient warrant.

Core commitments include: proportioning belief to evidence, burden of proof on positive claimants, and epistemic humility in the face of uncertainty. The Null Hypothesis rejects both dogmatic belief and dogmatic disbelief in favor of principled suspension of judgment. It is compatible with provisional acceptance of well-evidenced claims while remaining open to revision.

### Key Principles

1. **Suspension of Judgment:** Default epistemic position is neither belief nor disbelief but epoché (withholding assent). Belief requires positive warrant; absence of warrant mandates suspension, not contrary belief.

2. **Proportioning Belief to Evidence:** Credence should track available evidence. Strong claims require strong evidence; extraordinary claims require extraordinary evidence. Certainty is rarely warranted.

3. **Burden of Proof:** Those making positive existence/value claims bear the burden of proof. Skepticism toward unsupported claims is methodologically appropriate, not a substantive metaphysical position.

---

## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on Null Hypothesis. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-NH Stance:** Grok - Empirical lens aligns with epistemic minimalism
- **ANTI-NH Stance:** Claude - Teleological lens challenges meaning vacuum
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via AUDITOR_ASSIGNMENTS.md

---

### PRO-Null Hypothesis Stance

**Mission:** Advocate for Null Hypothesis's explanatory power, coherence, and capacity to address fundamental questions.

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
pro_nh_bias_adjustment:
  # When scoring Null Hypothesis from PRO stance
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
- Score reflects Null Hypothesis's genuine strengths
- Critiques are acknowledged but framed appropriately
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Null Hypothesis Stance

**Mission:** Challenge Null Hypothesis's coherence, evidential support, and capacity to address key philosophical questions.

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
anti_nh_bias_adjustment:
  # When scoring Null Hypothesis from ANTI stance
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

**PRO-NH (Grok):** Empirical lens aligns with epistemic minimalism. Risk: [Profile maintainer to fill: specific risk of this pairing]

**ANTI-NH (Claude):** Teleological lens challenges meaning vacuum. Risk: [Profile maintainer to fill: specific risk of this pairing]

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate strengths or ANTI scores ignore sophisticated defenses. Ensures both stances maintain intellectual honesty.

**Target:** 98% convergence after adversarial checking. If scores diverge significantly, auditors deliberate until consensus or document irreconcilable differences.

---

## Metrics

_Note: All metrics are PLACEHOLDERS awaiting Phase 4 Grok deliberation. Scaffolded with justification framework ready for philosophical reasoning._

_[Profile includes all 14 metrics across 7 categories - fully scaffolded but values TBD during Grok sessions]_

---

## Lifecycle Hooks

_[All 6 Trinity hooks implemented with Null Hypothesis-specific guidance - Bootstrap, Audit, Incident, Release, Deliberation, Comparative Audit]_

---

## Changelog

- **v0.1.0** (2025-11-09): Initial scaffolded profile created (C4)
  - Declared axiom, philosophical foundations, key principles defined
  - All 14 metrics scaffolded with justification framework templates
  - All 6 Trinity lifecycle hooks ready for Null Hypothesis deliberations
  - Status: DRAFT - Priority Queue #4, awaiting Phase 4 Grok integration

---

**Profile Version:** 0.1.0
**Created:** 2025-11-09 by C4
**Purpose:** Null Hypothesis worldview profile for CFA framework
**Usage:** Scaffolded foundation ready for Phase 4 Grok metric determination
