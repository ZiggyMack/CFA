# Islam Profile

**Status:** DRAFT | **Version:** 0.3.1 | **Date:** 2025-11-10

<!---
FILE: worldviews/ISLAM.md
PURPOSE: Worldview profile for Islam with metrics, philosophical foundations, and deliberation narratives, and steel-manning guide for adversarial auditing
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
- [Steel-Manning Guide](#steel-manning-guide) — Line 88
  - [PRO-Isl Stance](#pro-islam-stance) — Line 101
  - [ANTI-Isl Stance](#anti-islam-stance) — Line 162
- [Metrics](#metrics) — Line 237
- [Lifecycle Hooks](#lifecycle-hooks) — Line 244

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-islam-stance) | [ANTI Stance](#anti-islam-stance)
- 👥 **Users:** [What is Islam?](#philosophical-foundations)
- 📚 **Academic Sources:** See [../\_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#16-islam)

---

## Metadata

```yaml
profile:
  name: "Islam"
  version: "0.3.1"
  status: "DRAFT"
  declared_axiom: "There is no god but Allah, and Muhammad is His messenger; the Quran is Allah's final revelation; submission (islam) to Allah's will is the path to salvation"
  alternate_names: ["Muslim Worldview", "Sunni Islam", "Shia Islam"]
  last_updated: "2025-11-10"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null
  academic_sources: "../_docs/ACADEMIC_SOURCES.md#16-islam"
```

---

## Philosophical Foundations

### Declared Axiom

Islam begins with the Shahada: There is no god but Allah, and Muhammad is His messenger. Allah is the one, eternal, transcendent Creator; the Quran is His final revelation to humanity; submission to Allah's will through the Five Pillars and Sharia leads to paradise.

**📚 Academic Foundation:**
- **Core Doctrine:** [SEP Arabic and Islamic Metaphysics](https://plato.stanford.edu/entries/arabic-islamic-metaphysics/) - God and Creation, tawhid (divine unity)
- **Comprehensive Overview:** [SEP Arabic and Islamic Natural Philosophy](https://plato.stanford.edu/entries/arabic-islamic-natural/) - Kalām theology, occasionalism
- **Kalam vs. Falsafa:** [SEP Causation in Arabic and Islamic Thought](https://plato.stanford.edu/entries/arabic-islamic-causation/) - Theological debates

### Philosophical Framework

Islam operates within strict monotheism (tawhid), emphasizing divine unity, transcendence, and sovereignty. Core Islamic philosophy developed through kalam (theology), falsafa (philosophy influenced by Greek thought), and Sufism (mystical tradition).

**📚 Detailed Analysis:**
- **Islamic Metaphysics:** [SEP Arabic-Islamic Metaphysics](https://plato.stanford.edu/entries/arabic-islamic-metaphysics/) - God as necessary being, essence and existence
- **Kalām Theology:** [SEP Arabic-Islamic Natural](https://plato.stanford.edu/entries/arabic-islamic-natural/) - Atomism, divine causation, occasionalism
- **Causation Debates:** [SEP Causation in Arabic-Islamic Thought](https://plato.stanford.edu/entries/arabic-islamic-causation/) - Mu'tazilite vs. Ash'arite positions

### Key Principles

1. **Tawhid (Divine Unity):** Absolute divine unity and transcendence. Allah alone is worthy of worship; shirk (associating partners with Allah) is the gravest sin.
   - 📚 **Analysis:** [SEP Arabic-Islamic Metaphysics](https://plato.stanford.edu/entries/arabic-islamic-metaphysics/) - God and Creation, divine attributes

2. **Prophetic Authority:** Muhammad is the seal of the prophets; the Quran is Allah's final, uncorrupted revelation guiding humanity to submission.
   - 📚 **Framework:** [SEP Arabic-Islamic Natural](https://plato.stanford.edu/entries/arabic-islamic-natural/) - Kalām theological framework

3. **Ummah (Community):** The global Muslim community bound by shared faith, practice, and submission to Allah. Justice, compassion, and accountability define Islamic ethics.
   - 📚 **Analysis:** [SEP Causation in Arabic-Islamic Thought](https://plato.stanford.edu/entries/arabic-islamic-causation/) - Divine agency and human action

---

## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on Islam. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-Isl Stance:** Claude - Teleological lens aligns with divine will/purpose
- **ANTI-Isl Stance:** Grok - Empirical lens challenges theological claims
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via [../../auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)

---

### PRO-Islam Stance

**Mission:** Advocate for Islam's explanatory power, coherence, and capacity to address fundamental questions about divine unity, revelation, and human submission to Allah's will.

**What to Emphasize:**
- **Tawhid's radical monotheism** offers maximal divine unity and transcendence
  - 📚 **Steel-man with:** [SEP Arabic-Islamic Metaphysics](https://plato.stanford.edu/entries/arabic-islamic-metaphysics/) - God as necessary being
- **Quranic revelation** as preserved, unchanged final word provides epistemic clarity
- **Sharia's comprehensive coherence** integrating worship, ethics, law, and social order
  - 📚 **Steel-man with:** [SEP Arabic-Islamic Natural](https://plato.stanford.edu/entries/arabic-islamic-natural/) - Kalām framework
- **Historical Islamic civilization's** contributions to philosophy (Avicenna, Averroes), science, mathematics
- **Submission framework** provides clear purpose, accountability structure, communal solidarity
- **Prophetic tradition** and jurisprudence demonstrate sophisticated hermeneutical development
  - 📚 **Steel-man with:** [SEP Causation in Arabic-Islamic Thought](https://plato.stanford.edu/entries/arabic-islamic-causation/) - Kalām vs. falsafa sophistication

**What to Acknowledge (Honest Advocacy):**
- Epistemic challenges regarding Quranic origins require faith commitment
- Theodicy questions (divine decree vs human freedom) remain philosophically contested
  - 📚 **Acknowledge:** [SEP Arabic-Islamic Metaphysics](https://plato.stanford.edu/entries/arabic-islamic-metaphysics/) - Occasionalism debates
- Sharia interpretation varies across schools and modern contexts create hermeneutical tensions
- Historical record includes conquest, sectarian violence, intellectual stagnation periods
- Competitor worldviews offer legitimate alternative frameworks

**Scoring Calibration:**

```yaml
pro_isl_bias_adjustment:
  # When scoring Islam from PRO stance
  axiom_confidence: 0.85  # High confidence in Tawhid, Quranic revelation, prophetic authority
  burden_of_proof: 0.40   # Place burden on critics to disprove rather than Islam to prove revelation
  charity_interpretation: 0.88  # Interpret ambiguous Quranic/hadith texts in most favorable theological light
  edge_case_weight: 0.32  # Downweight counterexamples (violence, sectarianism) as distortions not essence
  explanatory_credit: 0.82  # Credit Islam for addressing fundamental questions even if not conclusive
  historical_weight: 0.78  # Weight 1400 years of civilization, scholarly tradition, cultural staying power
  lived_experience: 0.80  # Credit transformative capacity of submission, prayer discipline, communal solidarity
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Emphasize Tawhid as ultimate purposeful unity grounding all existence
- Connect submission framework to divine will as cosmic telos
- Frame Sharia as coherent teleological system ordering life toward Allah
- Highlight eschatological justice (Day of Judgment) as fulfillment of moral accountability

**Grok (Empirical):**
- Cite historical Islamic civilization's empirical achievements (science, mathematics, medicine)
- Reference sociological data on Islamic community cohesion and moral formation
- Acknowledge limits of empiricism for evaluating revelation claims
- Use comparative theology to show Islam's explanatory scope for metaphysical questions

**Nova (Symmetry):**
- Show balance between divine transcendence (Tawhid) and immanence (Allah's 99 names, providence)
- Demonstrate coherence across pillars (Shahada, salat, zakat, sawm, hajj) as integrated system
- Map symmetry between divine unity and ummah unity
- Check for internal consistency in theodicy (divine decree + human responsibility)

**Success Criteria:**
- Score reflects Islam's explanatory ambitions and historical robustness
- Critiques are acknowledged but framed as challenges not refutations
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Islam Stance

**Mission:** Challenge Islam's coherence, evidential support, and capacity to address suffering, epistemic access, and religious diversity.

**What to Emphasize:**
- **Revelation verification** - lack of independent historical evidence for Quranic origins, angelic transmission
  - 📚 **Challenge with:** [SEP Arabic-Islamic Metaphysics](https://plato.stanford.edu/entries/arabic-islamic-metaphysics/) - Epistemology of revelation claims
- **Sharia application concerns** - tensions between 7th-century legal frameworks and modern human rights
- **Theodicy under divine decree** - if Allah ordains all events, how is human moral responsibility coherent?
  - 📚 **Challenge with:** [SEP Causation in Arabic-Islamic Thought](https://plato.stanford.edu/entries/arabic-islamic-causation/) - Occasionalism problems
- **Religious diversity problem** - why would merciful Allah permit vast populations without access to Islam?
- **Scriptural literalism challenges** - Quranic cosmology reflects 7th-century context
- **Alternative naturalistic explanations** - comparative religion explains Islam's development without supernatural claims

**What to Acknowledge (Honest Opposition):**
- Islam has sophisticated theological defenses (Mutazilite rationalism, Asharite occasionalism, Sufi mysticism)
  - 📚 **Acknowledge:** [SEP Arabic-Islamic Natural](https://plato.stanford.edu/entries/arabic-islamic-natural/) - Kalām sophistication
- Tawhid's simplicity avoids some theological puzzles (Trinity, incarnation)
  - 📚 **Acknowledge:** [SEP Arabic-Islamic Metaphysics](https://plato.stanford.edu/entries/arabic-islamic-metaphysics/) - Divine unity coherence
- Lived experience and transformative capacity are real phenomena for millions
- Historical Islamic civilization made genuine contributions to human knowledge
- Metaphysical naturalism has its own explanatory gaps

**Scoring Calibration:**

```yaml
anti_isl_bias_adjustment:
  # When scoring Islam from ANTI stance
  axiom_confidence: 0.30  # Low confidence in Quranic revelation, prophetic authority claims
  burden_of_proof: 0.78   # Place burden on Islam to prove extraordinary claims (revelation, miracles)
  charity_interpretation: 0.48  # Interpret ambiguous Quranic texts neutrally, not favorably
  edge_case_weight: 0.82  # Upweight counterexamples (violence, apostasy laws) as systematic theological problems
  explanatory_credit: 0.38  # Require conclusive explanations, not just theological frameworks
  historical_weight: 0.28  # Discount historical staying power (argumentum ad populum/tradition fallacy)
  lived_experience: 0.42  # Acknowledge but don't overweight (other worldviews also transform lives)
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Question whether divine purposes (testing, submission) justify epistemic hiddenness
- Challenge whether Sharia's teleology aligns with modern moral intuitions
- Press on whether eschatological justice (hellfire for non-Muslims) truly fulfills moral meaningfulness
- Ask if naturalistic purpose (evolved cooperation, existential meaning-making) suffices without Allah

**Grok (Empirical):**
- Demand empirical evidence for Quranic origins, angelic transmission, prophetic miracles
- Press religious diversity as empirical data point against divine mercy claims
- Challenge fine-tuning arguments via multiverse or anthropic principle
- Require verification mechanisms for theological claims about Allah's attributes and will

**Nova (Symmetry):**
- Identify asymmetries (divine decree vs human freedom, Allah's mercy vs eternal hellfire)
- Challenge coherence of attribute combinations (all-merciful + eternal punishment)
- Test for hidden special pleading (Allah as necessary being, Quran as uncreated)
- Check whether theodicy of divine testing creates more moral problems than it solves

**Success Criteria:**
- Score reflects legitimate philosophical and evidential challenges to Islam
- Strengths are acknowledged but not overweighted
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### Adversarial Balance

**Why This Pairing Works:**

**PRO-Isl (Claude teleological):** Purpose-driven lens resonates with Islam's emphasis on divine will, submission as life's telos, and Sharia as comprehensive teleological ordering. Risk: Over-favor meaning-based explanations even when Sharia's moral implications are contested or revelation verification remains thin.

**ANTI-Isl (Grok empirical):** Evidence-driven lens challenges Islam's revelation claims, prophetic authority, and theological explanations for divine decree/human freedom tensions. Risk: Dismiss legitimate philosophical reasoning about metaphysical questions that transcend empirical verification or conflate cultural practices with core theology.

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate strengths (historical civilization) or ANTI scores ignore sophisticated defenses (kalam theology, jurisprudential diversity). Ensures both stances maintain intellectual honesty.

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
  - Added `academic_sources` metadata field referencing ACADEMIC_SOURCES.md#16
  - Enhanced Philosophical Foundations with 📚 academic references (SEP)
  - Updated Steel-Manning Guide with academic citations for PRO/ANTI arguments
  - Benefits: Eliminated content duplication, profile stays current via external sources

- **v0.3.0** (2025-11-10): Populated Steel-Manning calibration blocks for PRO/ANTI stances

- **v0.2.0** (2025-11-10): Added ToC and Steel-Manning Guide structure

- **v0.1.0** (2025-11-09): Initial scaffolded profile created (C4)

---

**Profile Version:** 0.3.1
**Created:** 2025-11-09 by C4
**Refactored:** 2025-11-10 by Doc_Claude (hyperlink architecture)
**Purpose:** Islam worldview profile for CFA framework
**Academic Sources:** See [../_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#16-islam)
