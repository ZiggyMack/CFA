# Buddhism Profile

**Status:** DRAFT | **Version:** 0.3.0 | **Date:** 2025-11-10

<!---
FILE: worldviews/BUDDHISM.md
PURPOSE: Worldview profile for Buddhism with metrics, philosophical foundations, deliberation narratives, and steel-manning guide for adversarial auditing
VERSION: 0.3.0 - Calibration populated + Hyperlink refactor
STATUS: DRAFT
DEPENDS_ON: ../_docs/METRIC_TAXONOMY.md, ../_docs/ACADEMIC_SOURCES.md, Trinity Architecture
NEEDED_BY: CFA analysis, worldview comparison tooling, auditor calibration
MOVES_WITH: /profiles/worldviews/
LAST_UPDATE: 2025-11-10 [v0.3.0: Calibration populated + Hyperlink refactor with academic sources]
--->

---

## 📑 Table of Contents

**Core Sections:**
- [Metadata](#metadata) — Line 36
- [Philosophical Foundations](#philosophical-foundations) — Line 53
- [Steel-Manning Guide](#steel-manning-guide) — Line 73
  - [PRO-Bdh Stance](#pro-buddhism-stance) — Line 86
  - [ANTI-Bdh Stance](#anti-buddhism-stance) — Line 147
- [Metrics](#metrics) — Line 222
- [Lifecycle Hooks](#lifecycle-hooks) — Line 227

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-buddhism-stance) | [ANTI Stance](#anti-buddhism-stance)
- 👥 **Users:** [What is Buddhism?](#philosophical-foundations)
- 📚 **Academic Sources:** See [../\_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#5-buddhism)

---

## Metadata

```yaml
profile:
  name: "Buddhism"
  version: "0.3.0"
  status: "DRAFT"
  declared_axiom: "Suffering (dukkha) is universal; suffering arises from craving/attachment; liberation (nirvana) is achieved through the Eightfold Path"
  alternate_names: ["Dharma Tradition", "Buddha-Dharma", "Theravada/Mahayana/Vajrayana"]
  last_updated: "2025-11-10"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null  # Will be filled during Phase 3 - Grok integration
  academic_sources: "../_docs/ACADEMIC_SOURCES.md#5-buddhism"
```

---

## Philosophical Foundations

### Declared Axiom

Buddhism begins with the **Four Noble Truths** revealed by the Buddha: (1) Dukkha - suffering/unsatisfactoriness is universal, (2) Samudaya - suffering arises from tanha (craving/attachment), (3) Nirodha - suffering can cease through elimination of craving, (4) Magga - the Eightfold Path leads to liberation (nirvana).

**📚 Academic Foundation:**
- **Core Teachings:** [SEP Buddha](https://plato.stanford.edu/entries/buddha/) - Four Noble Truths, Non-Self arguments
- **Comprehensive Overview:** [IEP Buddha](https://iep.utm.edu/buddha/) - Epistemology, Cosmology, Ethics
- **Madhyamaka School:** [IEP Madhyamaka](https://iep.utm.edu/madhyamaka-buddhist-philosophy/) - Emptiness doctrine, two truths

### Philosophical Framework

Buddhism operates within a **non-theistic, pragmatic soteriological framework** emphasizing direct experiential insight over metaphysical speculation. Core doctrines include anatta (no-self), anicca (impermanence), dependent origination (pratītyasamutpāda), and karma-rebirth.

**📚 Detailed Analysis:**
- **Non-Self Arguments:** [SEP Buddha §Non-Self](https://plato.stanford.edu/entries/buddha/) - Three arguments: impermanence, control, dependent arising
- **Dependent Arising:** [IEP Buddha §Cosmology](https://iep.utm.edu/buddha/) - Twelve-link chain
- **Four Buddhist Schools:** [SEP Mind in Indian Buddhism](https://plato.stanford.edu/entries/mind-indian-buddhism/)

### Key Principles

1. **Four Noble Truths:** Suffering is universal; craving causes suffering; suffering can end; the Eightfold Path leads to cessation.
   - 📚 **Analysis:** [SEP Buddha §Core Teachings](https://plato.stanford.edu/entries/buddha/), [IEP Buddha §Four Noble Truths](https://iep.utm.edu/buddha/)

2. **Three Marks of Existence:** All phenomena are dukkha (unsatisfactory), anicca (impermanent), anatta (non-self/lacking inherent existence).
   - 📚 **Arguments:** [SEP Buddha §Non-Self](https://plato.stanford.edu/entries/buddha/) - Philosophical arguments for anatta

3. **Middle Way:** Avoid extremes of hedonism and asceticism; cultivate ethical conduct, meditation, and wisdom for liberation.
   - 📚 **Epistemology:** [IEP Buddha §Epistemology](https://iep.utm.edu/buddha/) - Middle way between dogmatism and skepticism

---

## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on Buddhism. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-Bdh Stance:** Claude - Teleological lens aligns with purpose/enlightenment
- **ANTI-Bdh Stance:** Grok - Empirical lens challenges metaphysical claims
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via [../../auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)

---

### PRO-Buddhism Stance

**Mission:** Advocate for Buddhism's explanatory power, coherence, and capacity to address fundamental questions.

**What to Emphasize:**
- **Phenomenological rigor** - direct empirical investigation of consciousness and suffering
  - 📚 **Steel-man with:** [IEP Buddha §Epistemology](https://iep.utm.edu/buddha/) - Empiricism with yogic verification
- **Sophisticated account of no-self** (anatta) avoiding substance dualism problems
  - 📚 **Steel-man with:** [SEP Buddha §Non-Self](https://plato.stanford.edu/entries/buddha/) - Three non-self arguments
- **Practical efficacy** - meditation and mindfulness demonstrably reduce suffering
- **Coherent moral framework** without theistic foundations (karma as natural law)
  - 📚 **Steel-man with:** [IEP Buddha §Buddhist Ethics](https://iep.utm.edu/buddha/)
- **Historical staying power** across diverse cultures (2500+ years)
- **Addresses problem of suffering as primary** rather than theodicy challenge

**What to Acknowledge (Honest Advocacy):**
- Rebirth doctrine lacks empirical verification and raises continuity problems
  - 📚 **Acknowledge:** [IEP Buddha](https://iep.utm.edu/buddha/) - Personal identity problem with non-self and rebirth
- Dependent origination is complex and may not fully explain consciousness origins
- Ethical framework may struggle with modern applied ethics (bioethics, social justice)
- Metaphysical minimalism leaves questions about cosmic meaning/purpose unaddressed
- Competitor worldviews offer alternative accounts of selfhood and liberation

**Scoring Calibration:**

```yaml
pro_bdh_bias_adjustment:
  # When scoring Buddhism from PRO stance
  axiom_confidence: 0.80  # High confidence in Four Noble Truths and phenomenological insights
  burden_of_proof: 0.45   # Moderate burden - place some burden on critics given empirical meditation benefits
  charity_interpretation: 0.85  # Interpret ambiguous metaphysical claims favorably
  edge_case_weight: 0.35  # Downweight counterexamples (e.g., conventional vs ultimate truth framework allows flexibility)
  explanatory_credit: 0.80  # Credit Buddhism for addressing suffering, consciousness, ethics without theological commitments
  historical_weight: 0.85  # Weight 2500+ years of cross-cultural transmission and philosophical development
  lived_experience: 0.90  # Strongly credit transformative capacity (awakening, reduced suffering via practice)
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Emphasize liberation (nirvana) as ultimate purpose/telos of human existence
- Frame Eightfold Path as coherent purposive structure for meaning-making
- Connect dependent origination to teleological unfolding toward cessation
- Highlight ethical dimensions as grounded in natural karmic consequences

**Grok (Empirical):**
- Cite neuroscience research on meditation, mindfulness, and suffering reduction
- Reference cross-cultural psychological studies on Buddhist practitioners
- Acknowledge empirical gaps (rebirth, consciousness as fundamental) but frame as open questions
- Use phenomenological reports as empirical data about subjective experience

**Nova (Symmetry):**
- Map symmetry between Middle Way and balanced approach to extremes
- Show coherence between anatta, anicca, dukkha as interdependent principles
- Demonstrate internal consistency of dependent origination framework
- Check for balanced treatment of empirical vs metaphysical claims

**Success Criteria:**
- Score reflects Buddhism's genuine strengths
- Critiques are acknowledged but framed appropriately
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Buddhism Stance

**Mission:** Challenge Buddhism's coherence, evidential support, and capacity to address key philosophical questions.

**What to Emphasize:**
- **Rebirth/karma doctrine** is empirically unverifiable and philosophically problematic (continuity without self)
  - 📚 **Challenge with:** [IEP Buddha](https://iep.utm.edu/buddha/) - Personal identity problem
- **No-self doctrine** creates coherence problems (who experiences liberation? who accumulates karma?)
  - 📚 **Challenge with:** [SEP Buddha §Non-Self](https://plato.stanford.edu/entries/buddha/) - Debate over whether self is denied or left open
- **Dependent origination** may be descriptively accurate but lacks explanatory depth
- **Meditation benefits** don't validate metaphysical claims (naturalistic explanations available)
- **Ethical framework** struggles with modern challenges (trolley problems, distributive justice)
- **Pessimistic framing** (all is suffering) may pathologize normal human experience

**What to Acknowledge (Honest Opposition):**
- Buddhism offers sophisticated phenomenology of consciousness and suffering
  - 📚 **Acknowledge:** [SEP Buddha](https://plato.stanford.edu/entries/buddha/) - Buddha as Philosopher section
- Meditation practices have demonstrable psychological and neurological benefits
- No-self doctrine avoids Cartesian dualism and aligns with some cognitive science
- Historical robustness across cultures suggests philosophical depth
- Ethical framework without divine command is philosophically valuable
  - 📚 **Acknowledge:** [IEP Buddha §Buddhist Ethics](https://iep.utm.edu/buddha/)

**Scoring Calibration:**

```yaml
anti_bdh_bias_adjustment:
  # When scoring Buddhism from ANTI stance
  axiom_confidence: 0.40  # Low confidence in rebirth, karma, and ultimate liberation claims
  burden_of_proof: 0.75   # Place high burden on Buddhism to verify metaphysical claims (rebirth, nirvana)
  charity_interpretation: 0.50  # Interpret ambiguous claims neutrally (no-self, emptiness easily misunderstood)
  edge_case_weight: 0.80  # Upweight counterexamples (continuity problems, explanatory gaps) as systematic issues
  explanatory_credit: 0.50  # Require conclusive explanations, not just descriptive frameworks
  historical_weight: 0.40  # Discount historical staying power (many false beliefs persist)
  lived_experience: 0.60  # Acknowledge transformative capacity but don't overweight (placebo, community effects)
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Question whether liberation is genuine telos or escape from meaningful existence
- Challenge whether no-self undermines moral responsibility and purpose
- Press on whether Buddhism's pessimism about ordinary life devalues human flourishing
- Ask if eliminating desire eliminates what makes life worth living

**Grok (Empirical):**
- Demand empirical evidence for rebirth, karma, and nirvana
- Press on how no-self is compatible with karmic continuity
- Challenge whether meditation benefits require Buddhist metaphysics
- Require verification mechanisms for claims about enlightenment experiences

**Nova (Symmetry):**
- Identify tension between no-self and karmic moral responsibility
- Challenge coherence of nirvana as both cessation and ultimate good
- Test whether dependent origination explains or merely describes
- Check for special pleading in conventional vs ultimate truth distinction

**Success Criteria:**
- Score reflects legitimate philosophical challenges to Buddhism
- Strengths are acknowledged but not overweighted
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### Adversarial Balance

**Why This Pairing Works:**

**PRO-Bdh (Claude):** Teleological lens aligns with purpose/enlightenment. Risk: Overweight liberation as telos without adequately scrutinizing whether cessation truly constitutes purpose; may romanticize Eastern philosophy.

**ANTI-Bdh (Grok):** Empirical lens challenges metaphysical claims. Risk: Dismiss phenomenological insights as unverifiable; undervalue transformative practices because underlying metaphysics unproven; Western empiricist bias against non-materialist frameworks.

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate strengths (e.g., claiming meditation benefits prove all of Buddhism) or ANTI scores ignore sophisticated defenses (e.g., two-truths doctrine, pragmatic interpretation of rebirth). Ensures both stances maintain intellectual honesty.

**Target:** 98% convergence after adversarial checking. If scores diverge significantly, auditors deliberate until consensus or document irreconcilable differences as **Crux Points** (see [../../auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)).

---

## Metrics

_[All 14 metrics scaffolded - awaiting Phase 4 Grok deliberation]_

---

## Lifecycle Hooks

_[All 6 Trinity hooks implemented]_

---

## Changelog

- **v0.3.0** (2025-11-10): Calibration + Hyperlink Refactor
  - Populated complete calibration blocks with PRO/ANTI bias adjustment parameters (Calibration Claude)
  - Refactored to hyperlink-based architecture with academic source citations (Doc Claude)
  - Added `academic_sources` metadata field
  - Enhanced Philosophical Foundations with 📚 academic references
  - Updated Steel-Manning Guide with academic citations for PRO/ANTI arguments
  - Benefits: Eliminated content duplication, profiles stay current via external sources

- **v0.1.0** (2025-11-09): Initial scaffolded profile created (C4)

---

**Profile Version:** 0.3.0
**Created:** 2025-11-09 by C4
**Refactored:** 2025-11-10 by Doc_Claude (calibration + hyperlink architecture)
**Purpose:** Buddhism worldview profile for CFA framework
**Academic Sources:** See [../_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#5-buddhism)
