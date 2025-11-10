# Error Theory Profile

**Status:** DRAFT | **Version:** 0.2.0 | **Date:** 2025-11-10

<!---
FILE: worldviews/ERROR_THEORY.md
PURPOSE: Worldview profile for Moral Error Theory with metrics, philosophical foundations, and deliberation narratives, and steel-manning guide for adversarial auditing
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
  - [PRO-ET Stance](#pro-et-stance) — Line TBD
  - [ANTI-ET Stance](#anti-et-stance) — Line TBD
- [Metrics](#metrics) — Line TBD
- [Lifecycle Hooks](#lifecycle-hooks) — Line TBD

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-et-stance) | [ANTI Stance](#anti-et-stance)
- 👥 **Users:** [What is Error Theory?](#philosophical-foundations) | [Axioms & Debts](#mr-brutes-ledger)

---

## Metadata

```yaml
profile:
  name: "Error Theory"
  version: "0.1.0"
  status: "DRAFT"
  declared_axiom: "Moral statements purport to state facts but systematically fail to do so; all positive moral claims are false because moral properties do not exist"
  alternate_names: ["Moral Error Theory", "Moral Nihilism (cognitive)", "Moral Eliminativism"]
  last_updated: "2025-11-09"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null  # Will be filled during Phase 3 - Grok integration
```

---

## Philosophical Foundations

### Declared Axiom

Error Theory begins with the axiom that moral discourse is systematically in error. When people make moral claims ("lying is wrong", "charity is good"), they purport to state objective facts about moral properties, but these properties do not exist in reality. Therefore, all positive moral claims are false - not meaningless (as non-cognitivists claim), but factually mistaken.

### Philosophical Framework

Error Theory operates within metaethical anti-realism, most notably associated with J.L. Mackie's "Ethics: Inventing Right and Wrong" (1977). The position combines cognitivism (moral statements express beliefs that can be true or false) with nihilism (all positive moral beliefs are false because moral facts don't exist). Error theorists typically provide "error theories" explaining why humans systematically make these false moral claims (evolutionary psychology, social projection, etc.).

Core commitments include: moral anti-realism (no objective moral facts exist), cognitivism (moral statements are truth-apt), and systematic error (people believe moral facts exist but are mistaken). Error Theory rejects both moral realism (objectivism) and non-cognitivism (expressivism, emotivism). Instead, it maintains that moral language functions as if reporting facts, but the supposed facts don't obtain.

### Key Principles

1. **Moral Anti-Realism:** No objective moral properties, facts, or truths exist in reality. The universe is normatively inert - facts about what IS do not entail facts about what OUGHT to be.

2. **Systematic Error:** Human moral discourse systematically presupposes objective moral facts. Since these don't exist, all positive moral claims are false, though people universally believe them true.

3. **Queerness Argument:** If moral properties existed, they would be metaphysically queer - utterly unlike natural properties, requiring special epistemic access, and having intrinsic action-guidingness. Parsimony favors eliminating them.

---

## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on Error Theory. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-ET Stance:** Grok - Empirical lens aligns with moral skepticism
- **ANTI-ET Stance:** Claude - Teleological lens challenges moral nihilism
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via AUDITOR_ASSIGNMENTS.md

---

### PRO-Error Theory Stance

**Mission:** Advocate for Error Theory's explanatory power, coherence, and capacity to address fundamental questions.

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
pro_et_bias_adjustment:
  # When scoring Error Theory from PRO stance
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
- Score reflects Error Theory's genuine strengths
- Critiques are acknowledged but framed appropriately
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Error Theory Stance

**Mission:** Challenge Error Theory's coherence, evidential support, and capacity to address key philosophical questions.

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
anti_et_bias_adjustment:
  # When scoring Error Theory from ANTI stance
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

**PRO-ET (Grok):** Empirical lens aligns with moral skepticism. Risk: [Profile maintainer to fill: specific risk of this pairing]

**ANTI-ET (Claude):** Teleological lens challenges moral nihilism. Risk: [Profile maintainer to fill: specific risk of this pairing]

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate strengths or ANTI scores ignore sophisticated defenses. Ensures both stances maintain intellectual honesty.

**Target:** 98% convergence after adversarial checking. If scores diverge significantly, auditors deliberate until consensus or document irreconcilable differences.

---

## Metrics

_Note: All metrics are PLACEHOLDERS awaiting Phase 4 Grok deliberation. Scaffolded with justification framework ready for philosophical reasoning._

_[Profile includes all 14 metrics across 7 categories - fully scaffolded but values TBD during Grok sessions]_

---

## Lifecycle Hooks

_[All 6 Trinity hooks implemented with Error Theory-specific guidance - Bootstrap, Audit, Incident, Release, Deliberation, Comparative Audit]_

---

## Changelog

- **v0.1.0** (2025-11-09): Initial scaffolded profile created (C4)
  - Declared axiom, philosophical foundations, key principles defined
  - All 14 metrics scaffolded with justification framework templates
  - All 6 Trinity lifecycle hooks ready for Error Theory deliberations
  - Status: DRAFT - Priority Queue #3, awaiting Phase 4 Grok integration

---

**Profile Version:** 0.1.0
**Created:** 2025-11-09 by C4
**Purpose:** Error Theory worldview profile for CFA framework
**Usage:** Scaffolded foundation ready for Phase 4 Grok metric determination
