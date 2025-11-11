# Existentialism Profile

**Status:** DRAFT | **Version:** 0.3.0 | **Date:** 2025-11-10

<!---
FILE: worldviews/EXISTENTIALISM.md
PURPOSE: Worldview profile for Existentialism with metrics, philosophical foundations, and deliberation narratives, and steel-manning guide for adversarial auditing
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
- [Steel-Manning Guide](#steel-manning-guide) — Line 84
  - [PRO-Ext Stance](#pro-existentialism-stance) — Line 97
  - [ANTI-Ext Stance](#anti-existentialism-stance) — Line 158
- [Metrics](#metrics) — Line 233
- [Lifecycle Hooks](#lifecycle-hooks) — Line 238

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-existentialism-stance) | [ANTI Stance](#anti-existentialism-stance)
- 👥 **Users:** [What is Existentialism?](#philosophical-foundations)
- 📚 **Academic Sources:** See [../\_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#9-existentialism)

---

## Metadata

```yaml
profile:
  name: "Existentialism"
  version: "0.3.0"
  status: "DRAFT"
  declared_axiom: "Existence precedes essence; humans are radically free and responsible for creating meaning through authentic choice in an absurd universe"
  alternate_names: ["Existentialist Philosophy", "Atheistic Existentialism", "Existential Humanism"]
  last_updated: "2025-11-10"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null
  academic_sources: "../_docs/ACADEMIC_SOURCES.md#9-existentialism"
```

---

## Philosophical Foundations

### Declared Axiom

Existentialism begins with the axiom that **"existence precedes essence"** - humans are not created with predetermined nature or purpose, but rather find themselves thrown (Heidegger's Geworfenheit) into existence and must create meaning through free choice. The universe is absurd (Camus) or meaningless by default; humans face radical freedom and responsibility to define themselves through authentic action.

**📚 Academic Foundation:**
- **Core Doctrine:** [SEP Existentialism §Existence Precedes Essence](https://plato.stanford.edu/entries/existentialism/#ExisPrecEsse) - No predetermined essence, situated freedom
- **Comprehensive Overview:** [IEP Existentialism](https://iep.utm.edu/existent/) - Seven key themes, major figures
- **Key Figures:** [IEP Sartre: Existentialism](https://iep.utm.edu/sartre-ex/), [IEP Kierkegaard](https://iep.utm.edu/kierkega/)

### Philosophical Framework

Existentialism (particularly atheistic existentialism of Sartre, Camus, de Beauvoir) emphasizes **radical freedom, individual responsibility, authenticity vs bad faith**, and confrontation with absurdity, death, and meaninglessness.

**📚 Detailed Analysis:**
- **Freedom:** [SEP Existentialism §Freedom](https://plato.stanford.edu/entries/existentialism/#Free) - "Condemned to be free"
- **Authenticity:** [SEP Existentialism §Authenticity](https://plato.stanford.edu/entries/existentialism/#Auth)
- **Ethics:** [SEP Existentialism §Ethics](https://plato.stanford.edu/entries/existentialism/#Ethi)

### Key Principles

1. **Existence Precedes Essence:** Humans exist first, then define themselves through choices. No predetermined human nature or purpose; meaning is created, not discovered.
   - 📚 **Analysis:** [SEP Existentialism §Existence Precedes Essence](https://plato.stanford.edu/entries/existentialism/#ExisPrecEsse), [IEP Existentialism](https://iep.utm.edu/existent/) (Existence over Essence theme)

2. **Radical Freedom and Responsibility:** Humans are radically free; every choice defines who we are. We cannot escape responsibility for our lives by appealing to determinism, social roles, or divine will.
   - 📚 **Analysis:** [SEP Existentialism §Freedom](https://plato.stanford.edu/entries/existentialism/#Free), [IEP Sartre: Existentialism](https://iep.utm.edu/sartre-ex/)

3. **Authenticity vs Bad Faith:** Authentic existence confronts freedom and creates meaning honestly; bad faith denies freedom through self-deception, conformity, or appeals to external authority.
   - 📚 **Analysis:** [SEP Existentialism §Authenticity](https://plato.stanford.edu/entries/existentialism/#Auth)

---

## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on Existentialism. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-Ext Stance:** Claude - Teleological lens can frame authentic meaning-making
- **ANTI-Ext Stance:** Grok - Empirical lens challenges subjective meaning claims
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via [../../auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)

---

### PRO-Existentialism Stance

**Mission:** Advocate for Existentialism's explanatory power, coherence, and capacity to address fundamental questions.

**What to Emphasize:**
- **Radical freedom doctrine** takes human agency seriously without deterministic evasions
  - 📚 **Steel-man with:** [SEP Existentialism §Freedom](https://plato.stanford.edu/entries/existentialism/#Free)
- **Authenticity criterion** provides actionable ethical framework without metaphysical baggage
  - 📚 **Steel-man with:** [SEP Existentialism §Authenticity](https://plato.stanford.edu/entries/existentialism/#Auth)
- **Confronts absurdity/meaninglessness** honestly rather than offering false consolations
  - 📚 **Steel-man with:** [IEP Existentialism](https://iep.utm.edu/existent/) - Irrationality/Absurdity theme
- **Phenomenological rigor** - describes lived experience of freedom and responsibility
- **Influential** on 20th century literature, psychology, and cultural self-understanding
- **Liberating framework** - rejects external authorities (God, society) as excuses for abdication

**What to Acknowledge (Honest Advocacy):**
- Subjective meaning-creation may lack objective grounding or intersubjective verification
- Radical freedom claim faces challenges from determinism and situatedness
  - 📚 **Acknowledge:** [SEP Existentialism](https://plato.stanford.edu/entries/existentialism/) - Critiques section
- Existential angst may be psychologically destabilizing without constructive guidance
- Lack of positive moral content beyond authenticity leaves practical ethics underdetermined
- Competitor worldviews offer meaning frameworks without existential burden

**Scoring Calibration:**

```yaml
pro_ext_bias_adjustment:
  # When scoring Existentialism from PRO stance
  axiom_confidence: 0.75  # High confidence in phenomenology of freedom and responsibility
  burden_of_proof: 0.50   # Moderate burden - experiential evidence of freedom vs determinism ambiguous
  charity_interpretation: 0.80  # Interpret authenticity and freedom claims favorably
  edge_case_weight: 0.40  # Downweight counterexamples (determinism, situatedness as constraining not eliminating freedom)
  explanatory_credit: 0.75  # Credit Existentialism for addressing meaning, freedom, authenticity without metaphysics
  historical_weight: 0.70  # Weight 20th century influence on culture, psychology, ethics
  lived_experience: 0.85  # Strongly credit resonance with felt experience of freedom and responsibility
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Frame authentic self-creation as purposive project - meaning-making as telos
- Emphasize responsibility as grounding for meaningful life choices
- Connect freedom to capacity for purposive action unconstrained by determinism
- Highlight existential courage in facing absurdity without transcendent escape

**Grok (Empirical):**
- Cite psychological research on autonomy, agency, and well-being
- Reference phenomenological reports of freedom and choice experiences
- Acknowledge tension with neuroscience determinism but frame as open question
- Use existential psychology (Frankl, May) as empirical validation of framework

**Nova (Symmetry):**
- Map symmetry between freedom and responsibility as interdependent
- Show coherence between existence-precedes-essence and authenticity
- Demonstrate internal consistency of bad faith critique
- Check for balanced treatment of freedom vs situatedness

**Success Criteria:**
- Score reflects Existentialism's genuine strengths
- Critiques are acknowledged but framed appropriately
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Existentialism Stance

**Mission:** Challenge Existentialism's coherence, evidential support, and capacity to address key philosophical questions.

**What to Emphasize:**
- **Radical freedom claim** contradicted by neuroscience, situatedness, and social determinants
  - 📚 **Challenge with:** [SEP Existentialism](https://plato.stanford.edu/entries/existentialism/) - Contemporary critiques (Adorno, post-structuralists, analytic philosophers)
- **Subjective meaning-creation** lacks objective grounding - slides into relativism or nihilism
- **Authenticity criterion is vacuous** - any choice can be rationalized as "authentic"
  - 📚 **Challenge with:** [SEP Existentialism](https://plato.stanford.edu/entries/existentialism/) - Sartre's authenticity paradox
- **Existential angst** may reflect pathology rather than insight (depression, anxiety disorders)
- **Lacks positive ethical content** - provides no guidance for concrete moral dilemmas
  - 📚 **Challenge with:** [SEP Existentialism §Ethics](https://plato.stanford.edu/entries/existentialism/#Ethi)
- **Historical influence** reflects 20th century anomie not philosophical validity

**What to Acknowledge (Honest Opposition):**
- Existentialism captures phenomenology of freedom and responsibility compellingly
  - 📚 **Acknowledge:** [SEP Existentialism](https://plato.stanford.edu/entries/existentialism/) - Key figures' arguments
- Authenticity vs bad faith distinction has psychological and ethical resonance
- Confronts absurdity/meaninglessness without evasion
- Influenced psychology, literature, and cultural self-understanding significantly
- Phenomenological method provides valuable descriptive insights
  - 📚 **Acknowledge:** [IEP Existentialism](https://iep.utm.edu/existent/)

**Scoring Calibration:**

```yaml
anti_ext_bias_adjustment:
  # When scoring Existentialism from ANTI stance
  axiom_confidence: 0.40  # Low confidence in radical freedom given determinism evidence
  burden_of_proof: 0.70   # Place burden on Existentialism to reconcile freedom with neuroscience/situatedness
  charity_interpretation: 0.50  # Interpret authenticity claims neutrally (easily becomes vacuous)
  edge_case_weight: 0.75  # Upweight counterexamples (determinism, moral relativism) as systematic problems
  explanatory_credit: 0.45  # Require substantive not merely negative/critical framework
  historical_weight: 0.45  # Discount 20th century influence (reflects cultural moment not philosophical depth)
  lived_experience: 0.55  # Acknowledge experiential resonance but question whether angst reveals truth or pathology
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Question whether subjective meaning-creation provides genuine purpose or just self-deception
- Challenge whether authenticity without objective standards is contentful
- Press on whether rejecting transcendent meaning leaves life ultimately meaningless
- Ask if existential freedom undermines moral responsibility (if all choices equal, why choose good?)

**Grok (Empirical):**
- Demand evidence for radical freedom against neuroscience determinism
- Press on how subjective meaning differs from wishful thinking
- Challenge whether existential experiences (angst, authenticity) are philosophically revealing
- Require verification criteria for authentic vs inauthentic choices

**Nova (Symmetry):**
- Identify tension between radical freedom and situatedness/facticity
- Challenge coherence of meaning-creation (if meaningless, how create meaning?)
- Test whether authenticity criterion avoids arbitrariness
- Check for consistency between freedom and responsibility (if no essence, what grounds obligation?)

**Success Criteria:**
- Score reflects legitimate philosophical challenges to Existentialism
- Strengths are acknowledged but not overweighted
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### Adversarial Balance

**Why This Pairing Works:**

**PRO-Ext (Claude):** Teleological lens can frame authentic meaning-making. Risk: Overweight phenomenological resonance as philosophical validity; underweight determinism challenges; romanticize existential angst.

**ANTI-Ext (Grok):** Empirical lens challenges subjective meaning claims. Risk: Dismiss phenomenological insights as unscientific; overweight determinism without engaging compatibilism; conflate existential claims with empirical ones.

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate experiential resonance to philosophical proof or ANTI scores ignore sophisticated responses to determinism. Ensures both stances maintain intellectual honesty.

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
**Purpose:** Existentialism worldview profile for CFA framework
**Academic Sources:** See [../_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#9-existentialism)
