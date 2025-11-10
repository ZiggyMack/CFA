# Orthodox Judaism Profile

**Status:** DRAFT | **Version:** 0.2.0 | **Date:** 2025-11-10

<!---
FILE: worldviews/ORTHODOX_JUDAISM.md
PURPOSE: Worldview profile for Orthodox Judaism with metrics, philosophical foundations, and deliberation narratives, and steel-manning guide for adversarial auditing
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
  - [PRO-OJ Stance](#pro-oj-stance) — Line TBD
  - [ANTI-OJ Stance](#anti-oj-stance) — Line TBD
- [Metrics](#metrics) — Line TBD
- [Lifecycle Hooks](#lifecycle-hooks) — Line TBD

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-oj-stance) | [ANTI Stance](#anti-oj-stance)
- 👥 **Users:** [What is Orthodox Judaism?](#philosophical-foundations) | [Axioms & Debts](#mr-brutes-ledger)

---

## Metadata

```yaml
profile:
  name: "Orthodox Judaism"
  version: "0.1.0"
  status: "DRAFT"
  declared_axiom: "The God of Abraham, Isaac, and Jacob revealed the Torah at Sinai; Jewish law (halakha) is binding and authoritative for covenantal life"
  alternate_names: ["Torah Judaism", "Halakhic Judaism", "Traditional Judaism"]
  last_updated: "2025-11-09"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null  # Will be filled during Phase 3 - Grok integration
```

---

## Philosophical Foundations

### Declared Axiom

Orthodox Judaism begins with the axiom that the God of Abraham, Isaac, and Jacob entered into covenant with Israel and revealed the Torah (both written and oral) at Mount Sinai. This revelation includes the 613 commandments (mitzvot) and the interpretive tradition preserved in the Talmud and rabbinic literature. Halakha (Jewish law) is binding, authoritative, and central to covenantal faithfulness.

### Philosophical Framework

Orthodox Judaism operates within the framework of covenantal monotheism, emphasizing divine election of Israel, ongoing relationship with HaShem (the Name), and faithful observance of Torah. The tradition includes diverse streams (Modern Orthodox, Haredi, Hasidic) but shares core commitments to Sinaitic revelation, halakhic authority, and Jewish peoplehood.

Core commitments include: Torah min HaShamayim (Torah from Heaven), the binding nature of both written and oral Torah, the authority of rabbinic interpretation, and the centrality of mitzvot observance. These shape Orthodox Jewish approaches to epistemology (revelation through Torah and tradition), ethics (commanded actions rooted in divine will), teleology (covenantal life aimed at tikkun olam and messianic redemption), and anthropology (humans created in divine image with obligation to sanctify life through mitzvot).

### Key Principles

1. **Torah min HaShamayim:** Torah is divine revelation given at Sinai - both written (Tanakh) and oral (Mishnah, Talmud, rabbinic codes). This grounds the authority of halakha and the interpretive tradition.

2. **Halakhic Authority:** Jewish law (halakha) derived from Torah and developed through rabbinic interpretation is binding on Jewish life. Observance of mitzvot is central to covenantal faithfulness.

3. **Covenantal Peoplehood:** Jews are bound to God through covenant (brit) and to each other as am yisrael (the people of Israel). Jewish identity is both religious and peoplehood-based, with obligations to community and continuity.

---

## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on Orthodox Judaism. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-OJ Stance:** Claude - Teleological lens aligns with covenantal purpose
- **ANTI-OJ Stance:** Grok - Empirical lens challenges theological claims
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via AUDITOR_ASSIGNMENTS.md

---

### PRO-Orthodox Judaism Stance

**Mission:** Advocate for Orthodox Judaism's explanatory power, coherence, and capacity to address fundamental questions.

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
pro_oj_bias_adjustment:
  # When scoring Orthodox Judaism from PRO stance
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
- Score reflects Orthodox Judaism's genuine strengths
- Critiques are acknowledged but framed appropriately
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Orthodox Judaism Stance

**Mission:** Challenge Orthodox Judaism's coherence, evidential support, and capacity to address key philosophical questions.

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
anti_oj_bias_adjustment:
  # When scoring Orthodox Judaism from ANTI stance
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

**PRO-OJ (Claude):** Teleological lens aligns with covenantal purpose. Risk: [Profile maintainer to fill: specific risk of this pairing]

**ANTI-OJ (Grok):** Empirical lens challenges theological claims. Risk: [Profile maintainer to fill: specific risk of this pairing]

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate strengths or ANTI scores ignore sophisticated defenses. Ensures both stances maintain intellectual honesty.

**Target:** 98% convergence after adversarial checking. If scores diverge significantly, auditors deliberate until consensus or document irreconcilable differences.

---

## Metrics

_Note: All metrics are PLACEHOLDERS awaiting Phase 4 Grok deliberation. Scaffolded with justification framework ready for philosophical reasoning._

_[Profile includes all 14 metrics across 7 categories - fully scaffolded but values TBD during Grok sessions]_

---

## Lifecycle Hooks

_[All 6 Trinity hooks implemented with Orthodox Judaism-specific guidance - Bootstrap, Audit, Incident, Release, Deliberation, Comparative Audit]_

---

## Changelog

- **v0.1.0** (2025-11-09): Initial scaffolded profile created (C4)
  - Declared axiom, philosophical foundations, key principles defined
  - All 14 metrics scaffolded with justification framework templates
  - All 6 Trinity lifecycle hooks ready for Orthodox Judaism deliberations
  - Status: DRAFT - Priority Queue #1, awaiting Phase 4 Grok integration

---

**Profile Version:** 0.1.0
**Created:** 2025-11-09 by C4
**Purpose:** Orthodox Judaism worldview profile for CFA framework
**Usage:** Scaffolded foundation ready for Phase 4 Grok metric determination
