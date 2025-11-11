# Null Hypothesis Profile

**Status:** DRAFT | **Version:** 0.3.1 | **Date:** 2025-11-10

<!---
FILE: worldviews/NULL_HYPOTHESIS.md
PURPOSE: Worldview profile for Null Hypothesis (epistemic minimalism) with metrics, philosophical foundations, and deliberation narratives, and steel-manning guide for adversarial auditing
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
- [Steel-Manning Guide](#steel-manning-guide) — Line 75
  - [PRO-NH Stance](#pro-nh-stance) — Line 88
  - [ANTI-NH Stance](#anti-nh-stance) — Line 149
- [Metrics](#metrics) — Line 224
- [Lifecycle Hooks](#lifecycle-hooks) — Line 231

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-nh-stance) | [ANTI Stance](#anti-nh-stance)
- 👥 **Users:** [What is Null Hypothesis?](#philosophical-foundations)
- 📚 **Academic Sources:** See [../\_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#14-null-hypothesis-skepticism)

---

## Metadata

```yaml
profile:
  name: "Null Hypothesis"
  version: "0.3.1"
  status: "DRAFT"
  declared_axiom: "Withhold assent from all claims lacking sufficient evidence; default position is suspension of judgment rather than belief or disbelief"
  alternate_names: ["Epistemic Minimalism", "Pyrrhonian Skepticism", "Methodological Agnosticism"]
  last_updated: "2025-11-10"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null
  academic_sources: "../_docs/ACADEMIC_SOURCES.md#14-null-hypothesis-skepticism"
```

---

## Philosophical Foundations

### Declared Axiom

The Null Hypothesis position begins with the axiom that the default epistemic stance toward any claim is suspension of judgment (epoché) until sufficient evidence warrants belief. Neither belief nor disbelief is the default - rather, withholding assent pending adequate justification.

**📚 Academic Foundation:**
- **Core Doctrine:** [SEP Skepticism §Pyrrhonian Skepticism](https://plato.stanford.edu/entries/skepticism/#PyrrSkep) - Suspension of judgment, equipollence
- **Comprehensive Overview:** [SEP Ancient Skepticism](https://plato.stanford.edu/entries/skepticism-ancient/) - Pyrrhonian modes, epochē, ataraxia
- **Key Figures:** [SEP Pyrrho](https://plato.stanford.edu/entries/pyrrho/), [IEP Ancient Greek Skepticism](https://iep.utm.edu/ancient-greek-skepticism/)

### Philosophical Framework

The Null Hypothesis operates within skeptical epistemology, drawing from Pyrrhonian skepticism, Humean empiricism, and contemporary epistemology's burden-of-proof frameworks. It is methodologically agnostic - not claiming knowledge that claims are false, but rather suspending judgment on claims lacking sufficient warrant.

**📚 Detailed Analysis:**
- **Pyrrhonian Method:** [SEP Ancient Skepticism](https://plato.stanford.edu/entries/skepticism-ancient/) - Ten Modes, Five Modes showing equipollence
- **Contemporary Skepticism:** [SEP Skepticism](https://plato.stanford.edu/entries/skepticism/) - Regress argument, closure principle
- **Epistemic Principles:** [SEP Skepticism §Regress Argument](https://plato.stanford.edu/entries/skepticism/#RegeArgu) - Foundationalism, coherentism, infinitism responses

### Key Principles

1. **Suspension of Judgment (Epochē):** Default epistemic position is neither belief nor disbelief but epoché (withholding assent). Belief requires positive warrant; absence of warrant mandates suspension, not contrary belief.
   - 📚 **Analysis:** [SEP Ancient Skepticism](https://plato.stanford.edu/entries/skepticism-ancient/) - Pyrrhonian suspension of judgment

2. **Proportioning Belief to Evidence:** Credence should track available evidence. Strong claims require strong evidence; extraordinary claims require extraordinary evidence. Certainty is rarely warranted.
   - 📚 **Framework:** [SEP Skepticism](https://plato.stanford.edu/entries/skepticism/) - Contemporary epistemic skepticism

3. **Burden of Proof:** Those making positive existence/value claims bear the burden of proof. Skepticism toward unsupported claims is methodologically appropriate, not a substantive metaphysical position.
   - 📚 **Analysis:** [IEP Ancient Greek Skepticism](https://iep.utm.edu/ancient-greek-skepticism/) - Practical life without belief

---

## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on Null Hypothesis. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-NH Stance:** Grok - Empirical lens aligns with epistemic minimalism
- **ANTI-NH Stance:** Claude - Teleological lens challenges meaning vacuum
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via [../../auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)

---

### PRO-Null Hypothesis Stance

**Mission:** Advocate for Null Hypothesis's explanatory power, coherence, and capacity to address fundamental questions.

**What to Emphasize:**
- **Epistemic rigor** - proportioning belief to evidence prevents false beliefs and cognitive biases
  - 📚 **Steel-man with:** [SEP Skepticism](https://plato.stanford.edu/entries/skepticism/) - Regress argument for skepticism
- **Burden of proof framework** is standard in science, law, and rational discourse
- **Intellectual honesty** - admitting "I don't know" preferable to asserting unwarranted beliefs
  - 📚 **Steel-man with:** [SEP Ancient Skepticism](https://plato.stanford.edu/entries/skepticism-ancient/) - Pyrrhonian method
- **Avoids dogmatism** - neither affirms nor denies unprovable claims, maintains openness
- **Protects against manipulation** - skepticism toward unfounded authority claims and ideologies
- **Historical pedigree** - Pyrrhonian skepticism, Humean empiricism, scientific method foundations
  - 📚 **Steel-man with:** [SEP Pyrrho](https://plato.stanford.edu/entries/pyrrho/) - Founder of Pyrrhonism

**What to Acknowledge (Honest Advocacy):**
- Practical life requires provisional beliefs and action under uncertainty
  - 📚 **Acknowledge:** [IEP Ancient Greek Skepticism](https://iep.utm.edu/ancient-greek-skepticism/) - Practical life problem
- Radical skepticism may be self-defeating (skepticism about skepticism)
- Some presuppositions necessary for inquiry itself (logical principles, sense perception reliability)
- Suspension of judgment on all claims may lead to practical paralysis
- Competitor worldviews offer positive frameworks for meaning and purpose

**Scoring Calibration:**

```yaml
pro_nh_bias_adjustment:
  # When scoring Null Hypothesis from PRO stance
  axiom_confidence: 0.85  # High confidence in epistemic minimalism and burden of proof principles
  burden_of_proof: 0.25   # Low burden - place burden on positive claimants, not skeptics
  charity_interpretation: 0.80  # Interpret suspension of judgment favorably as intellectual honesty
  edge_case_weight: 0.30  # Downweight counterexamples (practical presuppositions don't refute epistemic minimalism)
  explanatory_credit: 0.70  # Credit for avoiding false beliefs and maintaining epistemic rigor
  historical_weight: 0.80  # Weight Pyrrhonian tradition, scientific method foundations
  lived_experience: 0.65  # Moderate credit - intellectual honesty valued but lacks transformative narrative
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Acknowledge epistemic rigor but press on whether avoiding error is sufficient telos
- Grant intellectual honesty value while questioning if suspension leaves life meaningless
- Challenge whether epistemic minimalism provides actionable guidance for living
- Ask if withholding judgment on purpose/meaning undermines human flourishing

**Grok (Empirical):**
- Emphasize alignment with scientific method and empirical standards
- Credit burden of proof framework as foundation for rational inquiry
- Highlight protection against cognitive biases and unfounded beliefs
- Frame suspension of judgment as methodologically sound pending evidence

**Nova (Symmetry):**
- Map symmetry between skepticism and openness (neither affirming nor denying)
- Show coherence between burden of proof and proportioning belief to evidence
- Demonstrate consistency in applying epistemic standards across all claims
- Check for balanced treatment of practical vs theoretical skepticism

**Success Criteria:**
- Score reflects Null Hypothesis's genuine strengths
- Critiques are acknowledged but framed appropriately
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Null Hypothesis Stance

**Mission:** Challenge Null Hypothesis's coherence, evidential support, and capacity to address key philosophical questions.

**What to Emphasize:**
- **Practical paralysis** - life requires action under uncertainty, not perpetual suspension
  - 📚 **Challenge with:** [IEP Ancient Greek Skepticism](https://iep.utm.edu/ancient-greek-skepticism/) - Practical life objection
- **Self-defeating** - skepticism about skeptical principles undermines the position itself
- **Presuppositions required** - logic, sense perception, memory reliability necessary for any inquiry
  - 📚 **Challenge with:** [SEP Skepticism](https://plato.stanford.edu/entries/skepticism/) - Regress argument responses
- **Meaning vacuum** - provides no positive framework for purpose, values, or flourishing
- **Epistemic asymmetry** - more reasonable to accept well-evidenced beliefs than withhold all judgment
- **Historical inefficacy** - pure skepticism never sustained as lived philosophy

**What to Acknowledge (Honest Opposition):**
- Burden of proof principle is methodologically sound in many contexts
- Intellectual honesty and avoiding false beliefs are genuine epistemic goods
  - 📚 **Acknowledge:** [SEP Ancient Skepticism](https://plato.stanford.edu/entries/skepticism-ancient/) - Pyrrhonian sophistication
- Skepticism protects against dogmatism and manipulation
- Proportioning belief to evidence is rational epistemic norm
- Historical tradition demonstrates philosophical sophistication

**Scoring Calibration:**

```yaml
anti_nh_bias_adjustment:
  # When scoring Null Hypothesis from ANTI stance
  axiom_confidence: 0.35  # Low confidence - presuppositions undermine pure epistemic minimalism
  burden_of_proof: 0.75   # Place burden on Null Hypothesis to justify practical livability and coherence
  charity_interpretation: 0.45  # Interpret suspension of judgment skeptically (may mask vacuity)
  edge_case_weight: 0.80  # Upweight counterexamples (practical paralysis, self-defeat) as systematic issues
  explanatory_credit: 0.35  # Require positive framework not just avoidance of error
  historical_weight: 0.40  # Discount historical staying power (never sustained as complete philosophy)
  lived_experience: 0.40  # Low credit - intellectual honesty insufficient for meaningful life
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Challenge whether avoiding error constitutes meaningful purpose or merely absence
- Press on meaning vacuum - suspension of judgment provides no telos for human life
- Question whether epistemic minimalism undermines conditions for purpose and flourishing
- Ask if intellectual honesty without positive values is sufficient for living well

**Grok (Empirical):**
- Demand evidence that radical skepticism is psychologically or practically sustainable
- Press on whether presuppositions (logic, perception) undermine pure epistemic minimalism
- Challenge whether Null Hypothesis has predictive or explanatory advantages over alternatives
- Require criteria for when suspension of judgment transitions to provisional acceptance

**Nova (Symmetry):**
- Identify tension between skepticism and necessary presuppositions for inquiry
- Challenge coherence of skepticism about skeptical principles (self-defeat)
- Test whether practical action under uncertainty contradicts theoretical suspension
- Check for asymmetry in applying skeptical standards

**Success Criteria:**
- Score reflects legitimate philosophical challenges
- Strengths are acknowledged but not overweighted
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### Adversarial Balance

**Why This Pairing Works:**

**PRO-NH (Grok):** Empirical lens aligns with epistemic minimalism. Risk: Overweight methodological soundness without engaging practical livability; conflate scientific method with complete life philosophy; undervalue positive meaning frameworks.

**ANTI-NH (Claude):** Teleological lens challenges meaning vacuum. Risk: Overweight need for positive meaning without acknowledging legitimate epistemic concerns; dismiss intellectual honesty as insufficient; impose teleological presuppositions skeptics legitimately question.

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate epistemic rigor as complete philosophy or ANTI scores ignore sophisticated defenses of practical skepticism. Ensures both stances maintain intellectual honesty about presuppositions and practical constraints.

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
  - Added `academic_sources` metadata field referencing ACADEMIC_SOURCES.md#14
  - Enhanced Philosophical Foundations with 📚 academic references (SEP/IEP)
  - Updated Steel-Manning Guide with academic citations for PRO/ANTI arguments
  - Benefits: Eliminated content duplication, profile stays current via external sources

- **v0.3.0** (2025-11-10): Populated complete calibration blocks with PRO/ANTI bias adjustment parameters, auditor lens guidance, and adversarial balance

- **v0.1.0** (2025-11-09): Initial scaffolded profile created (C4)
  - Declared axiom, philosophical foundations, key principles defined
  - All 14 metrics scaffolded with justification framework templates
  - All 6 Trinity lifecycle hooks ready for Null Hypothesis deliberations
  - Status: DRAFT - Priority Queue #4, awaiting Phase 4 Grok integration

---

**Profile Version:** 0.3.1
**Created:** 2025-11-09 by C4
**Refactored:** 2025-11-10 by Doc_Claude (hyperlink architecture)
**Purpose:** Null Hypothesis worldview profile for CFA framework
**Academic Sources:** See [../_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#14-null-hypothesis-skepticism)
