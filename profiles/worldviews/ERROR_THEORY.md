# Error Theory Profile

**Status:** DRAFT | **Version:** 0.3.1 | **Date:** 2025-11-10

<!---
FILE: worldviews/ERROR_THEORY.md
PURPOSE: Worldview profile for Moral Error Theory with metrics, philosophical foundations, and deliberation narratives, and steel-manning guide for adversarial auditing
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
- 👥 **Users:** [What is Error Theory?](#philosophical-foundations)
- 📚 **Academic Sources:** See [../\_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#13-error-theory)

---

## Metadata

```yaml
profile:
  name: "Error Theory"
  version: "0.3.1"
  status: "DRAFT"
  declared_axiom: "Moral statements purport to state facts but systematically fail to do so; all positive moral claims are false because moral properties do not exist"
  alternate_names: ["Moral Error Theory", "Moral Nihilism (cognitive)", "Moral Eliminativism"]
  last_updated: "2025-11-10"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null
  academic_sources: "../_docs/ACADEMIC_SOURCES.md#13-error-theory"
```

---

## Philosophical Foundations

### Declared Axiom

Error Theory begins with the axiom that moral discourse is systematically in error. When people make moral claims ("lying is wrong", "charity is good"), they purport to state objective facts about moral properties, but these properties do not exist in reality. Therefore, all positive moral claims are false - not meaningless (as non-cognitivists claim), but factually mistaken.

**📚 Academic Foundation:**
- **Core Doctrine:** [SEP Moral Anti-Realism §Error Theory](https://plato.stanford.edu/entries/moral-anti-realism/#ErroTheo) - Mackie's arguments, systematic falsehood
- **Comprehensive Overview:** [IEP Moral Realism](https://iep.utm.edu/moralrea/) - Error theory as anti-realist position
- **Key Figure:** J.L. Mackie, "Ethics: Inventing Right and Wrong" (1977)

### Philosophical Framework

Error Theory operates within metaethical anti-realism, most notably associated with J.L. Mackie's "Ethics: Inventing Right and Wrong" (1977). The position combines cognitivism (moral statements express beliefs that can be true or false) with nihilism (all positive moral beliefs are false because moral facts don't exist).

**📚 Detailed Analysis:**
- **Error Theory Framework:** [SEP Moral Anti-Realism §ErroTheo](https://plato.stanford.edu/entries/moral-anti-realism/#ErroTheo) - Cognitivist anti-realism
- **Characterization:** [SEP Moral Anti-Realism §Characterizing](https://plato.stanford.edu/entries/moral-anti-realism/#CharMoraAntiReal) - Error theory vs. noncognitivism vs. non-objectivism
- **Burden of Proof:** [SEP Moral Anti-Realism §Who Bears the Burden](https://plato.stanford.edu/entries/moral-anti-realism/#WhoBearBurdProo) - Methodological debates

### Key Principles

1. **Moral Anti-Realism:** No objective moral properties, facts, or truths exist in reality. The universe is normatively inert - facts about what IS do not entail facts about what OUGHT to be.
   - 📚 **Analysis:** [SEP Moral Anti-Realism §ErroTheo](https://plato.stanford.edu/entries/moral-anti-realism/#ErroTheo) - Moral properties don't exist; systematic falsehood

2. **Systematic Error:** Human moral discourse systematically presupposes objective moral facts. Since these don't exist, all positive moral claims are false, though people universally believe them true.
   - 📚 **Framework:** [IEP Moral Realism](https://iep.utm.edu/moralrea/) - Error theory contrasted with realism

3. **Queerness Argument (Mackie):** If moral properties existed, they would be metaphysically queer - utterly unlike natural properties, requiring special epistemic access, and having intrinsic action-guidingness. Parsimony favors eliminating them.
   - 📚 **Analysis:** [SEP Moral Anti-Realism §ErroTheo](https://plato.stanford.edu/entries/moral-anti-realism/#ErroTheo) - Argument from queerness (metaphysical and epistemological)

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
- **Mackie's queerness argument** - moral properties would be metaphysically bizarre
  - 📚 **Steel-man with:** [SEP Moral Anti-Realism §ErroTheo](https://plato.stanford.edu/entries/moral-anti-realism/#ErroTheo) - Argument from queerness (metaphysical & epistemological)
- **Explanatory parsimony** - no need to posit spooky moral facts
  - 📚 **Steel-man with:** [SEP Moral Realism](https://plato.stanford.edu/entries/moral-realism/) - Realist commitments contrasted
- **Systematic error explanation** - evolutionary debunking arguments explain moral beliefs without moral truth
- **Coherence with naturalism** - moral eliminativism natural extension of physicalism
- **Resolves epistemological puzzles** - no need to explain access to non-natural moral facts

**What to Acknowledge (Honest Advocacy):**
- Practical incoherence - we can't help but act as if morality matters
- Phenomenology of moral experience feels compelling
  - 📚 **Acknowledge:** [SEP Moral Realism](https://plato.stanford.edu/entries/moral-realism/) - Moral experience arguments
- Difficulty explaining moral progress and moral knowledge
- Alternative metaethics (expressivism, constructivism) avoid error without realism
- Doesn't fully explain normative force of moral claims

**Scoring Calibration:**

```yaml
pro_et_bias_adjustment:
  # When scoring Error Theory from PRO stance
  axiom_confidence: 0.80  # High confidence in moral anti-realism and queerness arguments
  burden_of_proof: 0.35   # Place burden on moral realists to prove moral facts exist
  charity_interpretation: 0.85  # Interpret ET's parsimony and naturalism favorably
  edge_case_weight: 0.35  # Downweight moral phenomenology as explained by evolutionary psychology
  explanatory_credit: 0.80  # Credit ET for debunking moral beliefs while maintaining coherence
  historical_weight: 0.40  # Moderate weight (ET is recent but builds on skeptical tradition)
  lived_experience: 0.30  # Low weight (acknowledge practical difficulty but prioritize coherence)
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Acknowledge ET resolves teleological puzzles (no need to explain purpose of moral facts)
- Recognize parsimony appeal even while noting practical costs
- Frame ET as clarifying what naturalism entails for ethics
- Credit ET for facing implications of metaphysical naturalism honestly

**Grok (Empirical):**
- Emphasize lack of empirical evidence for moral properties
- Highlight evolutionary explanations for moral beliefs without moral truth
- Credit queerness argument as applying Ockham's razor appropriately
- Frame ET as natural extension of scientific worldview

**Nova (Symmetry):**
- Show consistency between ET's metaphysics and epistemology
- Demonstrate how ET avoids special pleading for moral realm
- Map symmetry between ET's treatment of moral/aesthetic properties
- Check coherence of error explanation across moral domains

**Success Criteria:**
- Score reflects Error Theory's genuine strengths
- Critiques are acknowledged but framed appropriately
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Error Theory Stance

**Mission:** Challenge Error Theory's coherence, evidential support, and capacity to address key philosophical questions.

**What to Emphasize:**
- **Moral experience is phenomenologically compelling** and resilient
  - 📚 **Challenge with:** [SEP Moral Realism](https://plato.stanford.edu/entries/moral-realism/) - Robust moral phenomenology
- **Practical incoherence** - ET undermines basis for moral criticism including of realism
- **Explanatory gaps** - doesn't explain normative force or moral progress
- **Alternative metaethics** (expressivism, constructivism) preserve moral discourse without realism
  - 📚 **Challenge with:** [SEP Moral Anti-Realism](https://plato.stanford.edu/entries/moral-anti-realism/) - Noncognitivism alternatives
- **Moral disagreement** better explained by epistemic difficulty than systematic error
- **Debunking arguments may overgeneralize** - apply equally to logic, mathematics

**What to Acknowledge (Honest Opposition):**
- Queerness argument raises genuine epistemological puzzles for moral realism
  - 📚 **Acknowledge:** [SEP Moral Anti-Realism §ErroTheo](https://plato.stanford.edu/entries/moral-anti-realism/#ErroTheo) - Mackie's arguments have force
- Parsimony is a legitimate theoretical virtue
- Evolutionary debunking arguments create pressure for moral realists
- ET is internally coherent and faces implications honestly
- Naturalism does create tension with robust moral realism

**Scoring Calibration:**

```yaml
anti_et_bias_adjustment:
  # When scoring Error Theory from ANTI stance
  axiom_confidence: 0.30  # Low confidence (moral experience suggests otherwise)
  burden_of_proof: 0.80   # Place burden on ET to prove all moral claims false
  charity_interpretation: 0.45  # Interpret ambiguous claims skeptically
  edge_case_weight: 0.85  # Upweight moral phenomenology as systematic problem for ET
  explanatory_credit: 0.35  # Require ET to explain normative force not just debunk
  historical_weight: 0.25  # Low weight (ET is recent and contradicts moral experience)
  lived_experience: 0.85  # High weight (practical incoherence is serious problem)
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Challenge ET's inability to explain normative force (why moral claims matter)
- Press on practical incoherence (can't live as if morality is systematically false)
- Question whether parsimony should override moral phenomenology
- Ask if eliminating moral facts eliminates too much (moral progress, reformers)

**Grok (Empirical):**
- Cite empirical data on moral psychology (resilience of moral experience)
- Challenge whether evolutionary debunking proves error vs epistemic difficulty
- Press on ET's inability to explain cross-cultural moral convergence
- Demand explanation for why moral phenomenology is so robust

**Nova (Symmetry):**
- Identify asymmetry (ET accepts logical/mathematical facts but not moral ones)
- Challenge whether debunking arguments overgeneralize
- Test for hidden inconsistency (using moral language to criticize morality)
- Check whether ET's error explanation is self-undermining

**Success Criteria:**
- Score reflects legitimate philosophical challenges
- Strengths are acknowledged but not overweighted
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### Adversarial Balance

**Why This Pairing Works:**

**PRO-ET (Grok):** Empirical lens aligns with moral skepticism and naturalistic parsimony. Grok's evidence-driven approach naturally resonates with ET's rejection of non-empirical moral facts. Risk: Over-credit debunking arguments while dismissing phenomenological data about moral experience.

**ANTI-ET (Claude):** Teleological lens challenges moral nihilism by emphasizing normative force and practical coherence. Claude's purpose-driven reasoning highlights ET's difficulty explaining why morality matters. Risk: Over-weight lived experience and practical concerns while downplaying legitimate epistemological puzzles for moral realism.

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate parsimony arguments or ANTI scores ignore ET's internal coherence. Ensures both stances maintain intellectual honesty about ET's strengths (theoretical consistency) and weaknesses (practical incoherence).

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

- **v0.3.1** (2025-11-10): Hyperlink Refactor
  - Refactored to hyperlink-based architecture with academic source citations (Doc Claude)
  - Added `academic_sources` metadata field referencing ACADEMIC_SOURCES.md#13
  - Enhanced Philosophical Foundations with 📚 academic references (SEP/IEP)
  - Updated Steel-Manning Guide with academic citations for PRO/ANTI arguments
  - Benefits: Eliminated content duplication, profile stays current via external sources

- **v0.3.0** (2025-11-10): Steel-Manning Guide completed (Claude)
  - PRO-ET stance fully populated (6 emphasis bullets, 5 acknowledgments, 7 calibration params, 3x4 auditor lenses)
  - ANTI-ET stance fully populated (6 emphasis bullets, 5 acknowledgments, 7 calibration params, 3x4 auditor lenses)
  - Adversarial Balance section completed with pairing rationale and risks
  - Profile ready for adversarial auditing with disclosed bias calibrations

- **v0.2.0** (2025-11-10): ToC and Steel-Manning scaffolding added
  - Table of contents with quick links for auditors/users
  - Steel-Manning structure scaffolded for PRO/ANTI stances
  - Auditor assignments documented (Grok=PRO, Claude=ANTI, Nova=Fairness)

- **v0.1.0** (2025-11-09): Initial scaffolded profile created (C4)
  - Declared axiom, philosophical foundations, key principles defined
  - All 14 metrics scaffolded with justification framework templates
  - All 6 Trinity lifecycle hooks ready for Error Theory deliberations
  - Status: DRAFT - Priority Queue #3, awaiting Phase 4 Grok integration

---

**Profile Version:** 0.3.1
**Created:** 2025-11-09 by C4
**Refactored:** 2025-11-10 by Doc_Claude (hyperlink architecture)
**Purpose:** Error Theory worldview profile for CFA framework
**Academic Sources:** See [../_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#13-error-theory)
