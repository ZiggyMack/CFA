# Mormonism (LDS) Profile

**Status:** DRAFT | **Version:** 0.3.1 | **Date:** 2025-11-10

<!---
FILE: worldviews/MORMONISM.md
PURPOSE: Worldview profile for Mormonism/LDS with metrics, philosophical foundations, and deliberation narratives, and steel-manning guide for adversarial auditing
VERSION: 0.3.1 - Hyperlink refactor with academic sources
STATUS: DRAFT
DEPENDS_ON: ../_docs/METRIC_TAXONOMY.md, ../_docs/ACADEMIC_SOURCES.md, Trinity Architecture
NEEDED_BY: CFA analysis, worldview comparison tooling, auditor calibration
MOVES_WITH: /profiles/worldviews/
LAST_UPDATE: 2025-11-10 [v0.3.1: Hyperlink refactor with academic sources]
--->

---

## 📑 Table of Contents

**Core Sections:**
- [Metadata](#metadata) — Line 36
- [Philosophical Foundations](#philosophical-foundations) — Line 53
- [Steel-Manning Guide](#steel-manning-guide) — Line 87
  - [PRO-Mor Stance](#pro-mormonism-stance) — Line 100
  - [ANTI-Mor Stance](#anti-mormonism-stance) — Line 161
- [Metrics](#metrics) — Line 236
- [Lifecycle Hooks](#lifecycle-hooks) — Line 243

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-mormonism-stance) | [ANTI Stance](#anti-mormonism-stance)
- 👥 **Users:** [What is Mormonism?](#philosophical-foundations)
- 📚 **Academic Sources:** See [../\_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#18-mormonism-latter-day-saints)

---

## Metadata

```yaml
profile:
  name: "Mormonism (LDS)"
  version: "0.3.1"
  status: "DRAFT"
  declared_axiom: "God the Father, Jesus Christ, and the Holy Spirit are distinct beings; continuing revelation through prophets restores and expands truth; humans have potential for divine progression"
  alternate_names: ["Latter-day Saints", "LDS", "The Church of Jesus Christ of Latter-day Saints"]
  last_updated: "2025-11-10"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null
  academic_sources: "../_docs/ACADEMIC_SOURCES.md#18-mormonism-latter-day-saints"
```

---

## Philosophical Foundations

### Declared Axiom

Mormonism (LDS) begins with the axiom that God the Father, Jesus Christ, and the Holy Spirit are three distinct glorified beings united in purpose. Joseph Smith received divine revelations restoring the fullness of the gospel, including the Book of Mormon, Doctrine and Covenants, and Pearl of Great Price. Continuing revelation through living prophets guides the Church, and humans have potential for eternal progression toward godhood.

**📚 Academic Foundation:**
- **Core Doctrine:** [Encyclopedia of Mormonism - Philosophy](https://eom.byu.edu/index.php/Philosophy) - LDS scripture on philosophical issues
- **Academic Journal:** [Society for Mormon Philosophy and Theology - Element Journal](https://element.wcu.edu/) - Peer-reviewed LDS philosophy
- **Note:** SEP/IEP lack dedicated Mormonism articles; Encyclopedia of Mormonism (BYU) serves as authoritative academic source

### Philosophical Framework

Mormonism operates within a framework of restored Christianity emphasizing material theism (God has a perfected physical body), eternal progression (humans are eternal beings progressing toward exaltation), and continuing revelation (canon is open, living prophets receive divine guidance). The tradition rejects ex nihilo creation and traditional trinitarian theology in favor of social trinitarianism and material metaphysics.

**📚 Detailed Analysis:**
- **LDS Philosophy:** [Encyclopedia of Mormonism - Philosophy](https://eom.byu.edu/index.php/Philosophy) - Precluding ex nihilo creation, idealism, absolute determinism; affirming eternality and agency
- **Academic Theology:** [Element Journal](https://element.wcu.edu/) - Peer-reviewed scholarly work on Mormon theology

### Key Principles

1. **Continuing Revelation:** God speaks through living prophets today, expanding and clarifying truth. Canon is open, and personal revelation confirms prophetic teachings through the Holy Ghost.
   - 📚 **Analysis:** [Encyclopedia of Mormonism - Philosophy](https://eom.byu.edu/index.php/Philosophy) - Open canon and prophetic authority

2. **Eternal Progression:** Humans are eternal beings (intelligence → spirit → mortal → resurrected) with potential for exaltation to godhood through faithful obedience, temple ordinances, and Christ's atonement.
   - 📚 **Framework:** [Element Journal](https://element.wcu.edu/) - Academic work on exaltation doctrine

3. **Material Theism:** God the Father has a perfected, glorified physical body. Spirit and matter are both eternal; creation is organization of pre-existing elements, not ex nihilo creation.
   - 📚 **Analysis:** [Encyclopedia of Mormonism - Philosophy](https://eom.byu.edu/index.php/Philosophy) - Rejection of ex nihilo creation, material metaphysics

---

## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on Mormonism. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-Mor Stance:** Claude - Teleological lens aligns with eternal progression
- **ANTI-Mor Stance:** Grok - Empirical lens challenges theological claims
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via [../../auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)

---

### PRO-Mormonism Stance

**Mission:** Advocate for Mormonism's explanatory power, coherence, and capacity to address fundamental questions.

**What to Emphasize:**
- **Continuing revelation** provides adaptive, responsive guidance for modern challenges
  - 📚 **Steel-man with:** [Encyclopedia of Mormonism - Philosophy](https://eom.byu.edu/index.php/Philosophy) - Open canon framework
- **Divine progression framework** offers hope and purpose (exaltation as ultimate telos)
  - 📚 **Steel-man with:** [Element Journal](https://element.wcu.edu/) - Academic defenses of eternal progression
- **Restored gospel** addresses perceived gaps in traditional Christianity
- **Tight-knit community structure** provides strong social support and identity
- **Book of Mormon** as additional scripture complements Biblical witness
- **Family emphasis** (eternal sealing) addresses human longing for permanence in relationships

**What to Acknowledge (Honest Advocacy):**
- Historical controversies (polygamy, priesthood restrictions) require careful contextualization
- Epistemology relies heavily on personal testimony (burning in the bosom) which critics find subjective
- Book of Mormon archaeology faces evidential challenges
- Social trinitarianism and material theism depart significantly from traditional Christian orthodoxy
- Exclusivist temple ordinances create barriers and raise questions about divine justice for non-members

**Scoring Calibration:**

```yaml
pro_mor_bias_adjustment:
  # When scoring Mormonism from PRO stance
  axiom_confidence: 0.82  # High confidence in restoration narrative and continuing revelation
  burden_of_proof: 0.42   # Place burden on critics to disprove prophetic authority
  charity_interpretation: 0.88  # Interpret doctrinal development as refinement not contradiction
  edge_case_weight: 0.32  # Downweight historical controversies as cultural context not doctrinal failure
  explanatory_credit: 0.83  # Credit for addressing gaps in traditional Christianity (pre-mortal life, exaltation)
  historical_weight: 0.70  # Weight 200-year growth and institutional stability
  lived_experience: 0.85  # Credit tight community bonds and transformative missionary experiences
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Emphasize eternal progression as ultimate purpose framework (humans becoming divine)
- Connect continuing revelation to responsive divine guidance across history
- Frame temple ordinances as teleologically necessary for exaltation
- Highlight coherence of pre-mortal existence with human longing for cosmic significance

**Grok (Empirical):**
- Cite LDS community cohesion and missionary success as observable outcomes
- Reference personal testimony experiences as phenomenological data
- Acknowledge limits of empiricism for metaphysical claims (Godhood, pre-mortal life)
- Use comparative theology to show LDS addresses questions traditional Christianity brackets

**Nova (Symmetry):**
- Show balance between individual agency (free will) and divine plan
- Demonstrate coherence across restoration narrative (loss → recovery → progression)
- Map symmetry between material theism and embodied existence
- Check for internal consistency in continuing revelation mechanisms

**Success Criteria:**
- Score reflects Mormonism's genuine strengths
- Critiques are acknowledged but framed appropriately
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Mormonism Stance

**Mission:** Challenge Mormonism's coherence, evidential support, and capacity to address key philosophical questions.

**What to Emphasize:**
- **Historical criticism** of Book of Mormon (anachronisms, lack of archaeological evidence, DNA studies)
  - 📚 **Challenge with:** Academic historical-critical scholarship on Book of Mormon
- **Revelation verification problem** - how to distinguish genuine prophecy from human invention
- **Theological departures** from historic Christianity (material God, plurality of gods, denial of creatio ex nihilo)
  - 📚 **Challenge with:** [Encyclopedia of Mormonism - Philosophy](https://eom.byu.edu/index.php/Philosophy) - Non-traditional metaphysics
- **Exclusivist claims** requiring temple ordinances create justice problems for billions
- **Institutional issues** (historical racism, LGBTQ+ policies, women's priesthood exclusion)
- **Joseph Smith's character controversies** and competing succession claims after his death

**What to Acknowledge (Honest Opposition):**
- LDS community provides genuine support networks and meaning for millions
- Continuing revelation framework addresses problem of static scriptures in changing world
  - 📚 **Acknowledge:** [Encyclopedia of Mormonism - Philosophy](https://eom.byu.edu/index.php/Philosophy) - Open canon sophistication
- Eternal progression offers compelling theodicy (suffering as growth toward divinity)
- LDS apologetics has become increasingly sophisticated (FAIR Mormon, Maxwell Institute)
  - 📚 **Acknowledge:** [Element Journal](https://element.wcu.edu/) - Scholarly LDS philosophy
- Missionary commitment and family emphasis produce observable positive social outcomes

**Scoring Calibration:**

```yaml
anti_mor_bias_adjustment:
  # When scoring Mormonism from ANTI stance
  axiom_confidence: 0.30  # Low confidence in restoration narrative and prophetic authority
  burden_of_proof: 0.78   # Place burden on LDS to prove extraordinary claims (golden plates, divine progression)
  charity_interpretation: 0.48  # Interpret doctrinal changes as contradictions not refinements
  edge_case_weight: 0.82  # Upweight historical controversies as evidence of human not divine origin
  explanatory_credit: 0.38  # Require conclusive evidence not just theological frameworks
  historical_weight: 0.25  # Discount 200-year history compared to older traditions
  lived_experience: 0.42  # Acknowledge but don't overweight (other communities also bond strongly)
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Question whether divine progression is ad hoc theodicy (does suffering really perfect?)
- Challenge whether purpose requires literal godhood or symbolic participation suffices
- Press on whether eternal families create unjust exclusion of non-temple-sealed
- Ask if naturalistic purpose frameworks suffice

**Grok (Empirical):**
- Demand archaeological evidence for Book of Mormon civilizations
- Press DNA studies contradicting Lamanite-Native American connection
- Challenge burning-in-bosom epistemology as confirmation bias
- Require verification mechanisms for prophetic revelations vs cultural accommodation

**Nova (Symmetry):**
- Identify asymmetries (prophetic authority vs individual revelation - who wins in conflict?)
- Challenge coherence of material God with divine perfection and omnipresence
- Test for hidden special pleading (why Joseph Smith and not other visionaries?)
- Check whether continuing revelation creates more doctrinal instability than it solves

**Success Criteria:**
- Score reflects legitimate philosophical challenges
- Strengths are acknowledged but not overweighted
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### Adversarial Balance

**Why This Pairing Works:**

**PRO-Mor (Claude teleological):** Purpose-driven lens resonates with eternal progression narrative and divine telos. Risk: Over-favor teleological explanations that may be unfalsifiable; downplay historical-critical challenges to restoration narrative.

**ANTI-Mor (Grok empirical):** Evidence-driven lens challenges Book of Mormon historicity, prophetic verification, and metaphysical claims about godhood. Risk: Dismiss legitimate philosophical theology that transcends empirical verification; overweight 19th-century controversies without charitable contextualization.

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate continuing revelation's coherence or ANTI scores ignore LDS community's transformative capacity. Ensures both stances maintain intellectual honesty and acknowledge sophisticated LDS apologetics alongside legitimate critiques.

**Target:** 98% convergence after adversarial checking. If scores diverge significantly, auditors deliberate until consensus or document irreconcilable differences as **Crux Points** (see [../../auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)).

---

## Metrics

_[All 14 metrics scaffolded - awaiting Phase 4 Grok deliberation]_

---

## Lifecycle Hooks

_[All 6 Trinity hooks implemented]_

---

## Changelog

- **v0.3.1** (2025-11-10): Hyperlink Refactor
  - Refactored to hyperlink-based architecture with academic source citations (Doc Claude)
  - Added `academic_sources` metadata field referencing ACADEMIC_SOURCES.md#18
  - Enhanced Philosophical Foundations with 📚 academic references (BYU EoM, Element Journal)
  - Updated Steel-Manning Guide with academic citations for PRO/ANTI arguments
  - Benefits: Eliminated content duplication, profile stays current via external sources

- **v0.3.0** (2025-11-10): Steel-Manning Guide fully populated with calibration blocks (C4)

- **v0.2.0** (2025-11-10): Added ToC and Steel-Manning Guide scaffolding

- **v0.1.0** (2025-11-09): Initial scaffolded profile created (C4)

---

**Profile Version:** 0.3.1
**Created:** 2025-11-09 by C4
**Refactored:** 2025-11-10 by Doc_Claude (hyperlink architecture)
**Purpose:** Mormonism/LDS worldview profile for CFA framework
**Academic Sources:** See [../_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#18-mormonism-latter-day-saints)
