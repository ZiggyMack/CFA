# Islam Profile

**Status:** DRAFT | **Version:** 0.2.0 | **Date:** 2025-11-10

<!---
FILE: worldviews/ISLAM.md
PURPOSE: Worldview profile for Islam with metrics, philosophical foundations, and deliberation narratives, and steel-manning guide for adversarial auditing
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
  - [PRO-Isl Stance](#pro-isl-stance) — Line TBD
  - [ANTI-Isl Stance](#anti-isl-stance) — Line TBD
- [Metrics](#metrics) — Line TBD
- [Lifecycle Hooks](#lifecycle-hooks) — Line TBD

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-isl-stance) | [ANTI Stance](#anti-isl-stance)
- 👥 **Users:** [What is Islam?](#philosophical-foundations) | [Axioms & Debts](#mr-brutes-ledger)

---

## Metadata

```yaml
profile:
  name: "Islam"
  version: "0.1.0"
  status: "DRAFT"
  declared_axiom: "There is no god but Allah, and Muhammad is His messenger; the Quran is Allah's final revelation; submission (islam) to Allah's will is the path to salvation"
  alternate_names: ["Muslim Worldview", "Sunni Islam", "Shia Islam"]
  last_updated: "2025-11-09"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null
```

---

## Philosophical Foundations

### Declared Axiom

Islam begins with the Shahada: There is no god but Allah, and Muhammad is His messenger. Allah is the one, eternal, transcendent Creator; the Quran is His final revelation to humanity; submission to Allah's will through the Five Pillars and Sharia leads to paradise.

### Philosophical Framework

Islam operates within strict monotheism (tawhid), emphasizing divine unity, transcendence, and sovereignty. Core Islamic philosophy developed through kalam (theology), falsafa (philosophy influenced by Greek thought), and Sufism (mystical tradition). The tradition includes diverse schools (Sunni, Shia, Sufi) but shares core commitments to Quranic authority, prophetic tradition (hadith), and Islamic law (Sharia).

### Key Principles

1. **Tawhid:** Absolute divine unity and transcendence. Allah alone is worthy of worship; shirk (associating partners with Allah) is the gravest sin.

2. **Prophetic Authority:** Muhammad is the seal of the prophets; the Quran is Allah's final, uncorrupted revelation guiding humanity to submission.

3. **Ummah:** The global Muslim community bound by shared faith, practice, and submission to Allah. Justice, compassion, and accountability define Islamic ethics.

---

## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on Islam. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-Isl Stance:** Claude - Teleological lens aligns with divine will/purpose
- **ANTI-Isl Stance:** Grok - Empirical lens challenges theological claims
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via AUDITOR_ASSIGNMENTS.md

---

### PRO-Islam Stance

**Mission:** Advocate for Islam's explanatory power, coherence, and capacity to address fundamental questions.

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
pro_isl_bias_adjustment:
  # When scoring Islam from PRO stance
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
- Score reflects Islam's genuine strengths
- Critiques are acknowledged but framed appropriately
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Islam Stance

**Mission:** Challenge Islam's coherence, evidential support, and capacity to address key philosophical questions.

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
anti_isl_bias_adjustment:
  # When scoring Islam from ANTI stance
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

**PRO-Isl (Claude):** Teleological lens aligns with divine will/purpose. Risk: [Profile maintainer to fill: specific risk of this pairing]

**ANTI-Isl (Grok):** Empirical lens challenges theological claims. Risk: [Profile maintainer to fill: specific risk of this pairing]

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate strengths or ANTI scores ignore sophisticated defenses. Ensures both stances maintain intellectual honesty.

**Target:** 98% convergence after adversarial checking. If scores diverge significantly, auditors deliberate until consensus or document irreconcilable differences.

---

## Metrics

_[All 14 metrics scaffolded - awaiting Phase 4 Grok deliberation]_

---

## Lifecycle Hooks

_[All 6 Trinity hooks implemented]_

---

## Changelog

- **v0.1.0** (2025-11-09): Initial scaffolded profile created (C4)

---

**Profile Version:** 0.1.0
**Created:** 2025-11-09 by C4
**Purpose:** Islam worldview profile for CFA framework
