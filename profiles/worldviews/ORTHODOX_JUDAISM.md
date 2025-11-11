# Orthodox Judaism Profile

**Status:** DRAFT | **Version:** 0.3.1 | **Date:** 2025-11-10

<!---
FILE: worldviews/ORTHODOX_JUDAISM.md
PURPOSE: Worldview profile for Orthodox Judaism with metrics, philosophical foundations, and deliberation narratives, and steel-manning guide for adversarial auditing
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
- [Steel-Manning Guide](#steel-manning-guide) — Line 91
  - [PRO-OJ Stance](#pro-orthodox-judaism-stance) — Line 104
  - [ANTI-OJ Stance](#anti-orthodox-judaism-stance) — Line 165
- [Metrics](#metrics) — Line 240
- [Lifecycle Hooks](#lifecycle-hooks) — Line 247

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-orthodox-judaism-stance) | [ANTI Stance](#anti-orthodox-judaism-stance)
- 👥 **Users:** [What is Orthodox Judaism?](#philosophical-foundations)
- 📚 **Academic Sources:** See [../\_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#17-orthodox-judaism)

---

## Metadata

```yaml
profile:
  name: "Orthodox Judaism"
  version: "0.3.1"
  status: "DRAFT"
  declared_axiom: "The God of Abraham, Isaac, and Jacob revealed the Torah at Sinai; Jewish law (halakha) is binding and authoritative for covenantal life"
  alternate_names: ["Torah Judaism", "Halakhic Judaism", "Traditional Judaism"]
  last_updated: "2025-11-10"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null
  academic_sources: "../_docs/ACADEMIC_SOURCES.md#17-orthodox-judaism"
```

---

## Philosophical Foundations

### Declared Axiom

Orthodox Judaism begins with the axiom that the God of Abraham, Isaac, and Jacob entered into covenant with Israel and revealed the Torah (both written and oral) at Mount Sinai. This revelation includes the 613 commandments (mitzvot) and the interpretive tradition preserved in the Talmud and rabbinic literature.

**📚 Academic Foundation:**
- **Core Doctrine:** [SEP Maimonides](https://plato.stanford.edu/entries/maimonides/) - Torah and philosophy unity, 13 Principles
- **Comprehensive Overview:** [IEP Maimonides](https://iep.utm.edu/maimonid/) - Mishneh Torah, Guide of the Perplexed
- **Jewish Philosophy:** [SEP Jewish Philosophy](https://plato.stanford.edu/entries/jewish-philosophy/) - Historical development, key themes

### Philosophical Framework

Orthodox Judaism operates within the framework of covenantal monotheism, emphasizing divine election of Israel, ongoing relationship with HaShem (the Name), and faithful observance of Torah. The tradition includes diverse streams (Modern Orthodox, Haredi, Hasidic) but shares core commitments to Sinaitic revelation, halakhic authority, and Jewish peoplehood.

**📚 Detailed Analysis:**
- **Maimonidean Theology:** [SEP Maimonides §Fundamentals](https://plato.stanford.edu/entries/maimonides/#FunOri) - 13 Principles, Torah/philosophy integration
- **Negative Theology:** [SEP Maimonides §God via Negative Attributes](https://plato.stanford.edu/entries/maimonides/#GodViaNeg) - Divine incorporeality, unknowability
- **Creation:** [SEP Maimonides §Creation](https://plato.stanford.edu/entries/maimonides/#Cre) - Against Aristotelian eternity

### Key Principles

1. **Torah min HaShamayim (Torah from Heaven):** Torah is divine revelation given at Sinai - both written (Tanakh) and oral (Mishnah, Talmud, rabbinic codes). This grounds the authority of halakha and the interpretive tradition.
   - 📚 **Analysis:** [SEP Maimonides §FunOri](https://plato.stanford.edu/entries/maimonides/#FunOri) - 13 Principles including God's existence, unity, Torah immutability

2. **Halakhic Authority:** Jewish law (halakha) derived from Torah and developed through rabbinic interpretation is binding on Jewish life. Observance of mitzvot is central to covenantal faithfulness.
   - 📚 **Framework:** [IEP Maimonides](https://iep.utm.edu/maimonid/) - Comprehensive halakhic system (Mishneh Torah)

3. **Covenantal Peoplehood:** Jews are bound to God through covenant (brit) and to each other as am yisrael (the people of Israel). Jewish identity is both religious and peoplehood-based.
   - 📚 **Analysis:** [SEP Jewish Philosophy](https://plato.stanford.edu/entries/jewish-philosophy/) - Philosophical themes in Judaism

---

## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on Orthodox Judaism. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-OJ Stance:** Claude - Teleological lens aligns with covenantal purpose
- **ANTI-OJ Stance:** Grok - Empirical lens challenges theological claims
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via [../../auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)

---

### PRO-Orthodox Judaism Stance

**Mission:** Advocate for Orthodox Judaism's explanatory power, coherence, and capacity to address fundamental questions.

**What to Emphasize:**
- **Torah revelation at Sinai** as coherent foundation for epistemology and authority
  - 📚 **Steel-man with:** [SEP Maimonides §FunOri](https://plato.stanford.edu/entries/maimonides/#FunOri) - 13 Principles framework
- **Halakha's comprehensive framework** for ethical living across all domains
  - 📚 **Steel-man with:** [IEP Maimonides](https://iep.utm.edu/maimonid/) - Mishneh Torah systematization
- **Covenantal relationship** providing meaning, purpose, and communal identity
- **Historical continuity** and resilience across 3000+ years of Jewish experience
  - 📚 **Steel-man with:** [SEP Jewish Philosophy](https://plato.stanford.edu/entries/jewish-philosophy/) - Historical development
- **Talmudic sophistication** demonstrating intellectual rigor and interpretive depth
- **Community preservation** maintaining tradition while engaging modernity

**What to Acknowledge (Honest Advocacy):**
- Epistemic limitations (revelation requires faith beyond pure reason)
- Historical-critical scholarship challenges to traditional Sinai narrative
  - 📚 **Acknowledge:** [SEP Maimonides](https://plato.stanford.edu/entries/maimonides/) - Medieval cosmology tensions
- Tension between particularism (chosen people) and universal ethical claims
- Ongoing debates within Orthodox Judaism on gender roles and modernity
- Theodicy challenges especially post-Holocaust

**Scoring Calibration:**

```yaml
pro_oj_bias_adjustment:
  # When scoring Orthodox Judaism from PRO stance
  axiom_confidence: 0.85  # High confidence in Torah min HaShamayim and halakhic authority
  burden_of_proof: 0.40   # Place burden on critics to disprove rather than OJ to prove
  charity_interpretation: 0.90  # Interpret ambiguous claims in most favorable light
  edge_case_weight: 0.30  # Downweight counterexamples as exceptions not disproofs
  explanatory_credit: 0.85  # Credit OJ for addressing fundamental questions even if not conclusive
  historical_weight: 0.80  # Weight historical robustness and cultural continuity heavily
  lived_experience: 0.80  # Credit transformative capacity and communal coherence
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Emphasize covenantal purpose as coherent framework for meaning and ethics
- Connect halakhic observance to telos of sanctifying life and tikkun olam
- Frame mitzvot as meaningful participation in divine-human partnership
- Highlight coherence of messianic hope with Jewish historical resilience

**Grok (Empirical):**
- Cite historical continuity as empirical evidence of tradition's robustness
- Reference social science data on Orthodox community cohesion and well-being
- Acknowledge limits of empiricism for covenantal and revelatory claims
- Use comparative religious studies to show OJ's explanatory scope

**Nova (Symmetry):**
- Show balance between particularism (covenant with Israel) and universal ethics
- Demonstrate coherence across halakhic domains (ritual, civil, moral law)
- Map symmetry between divine transcendence and covenantal intimacy
- Check for internal consistency in theological anthropology

**Success Criteria:**
- Score reflects Orthodox Judaism's genuine strengths
- Critiques are acknowledged but framed appropriately
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Orthodox Judaism Stance

**Mission:** Challenge Orthodox Judaism's coherence, evidential support, and capacity to address key philosophical questions.

**What to Emphasize:**
- **Historical-critical challenges** to Sinai revelation narrative (Documentary Hypothesis, archaeological evidence)
  - 📚 **Challenge with:** [SEP Maimonides](https://plato.stanford.edu/entries/maimonides/) - Medieval vs. modern epistemology tensions
- **Halakha's rigidity** creating tension with modern ethical intuitions (gender equality, LGBTQ inclusion)
- **Theodicy post-Holocaust** challenges divine providence and covenant faithfulness
- **Particularism tensions** (chosen people doctrine) with universal human dignity claims
  - 📚 **Challenge with:** [SEP Jewish Philosophy](https://plato.stanford.edu/entries/jewish-philosophy/) - Particularism debates
- **Lack of empirical verification** for core theological claims (Torah from Heaven, divine authorship)
- **Gender role restrictions** and agunah problem as structural injustices

**What to Acknowledge (Honest Opposition):**
- Historical continuity demonstrates remarkable cultural resilience and adaptability
  - 📚 **Acknowledge:** [SEP Jewish Philosophy](https://plato.stanford.edu/entries/jewish-philosophy/) - 3500+ year tradition
- Halakhic framework provides comprehensive ethical guidance across life domains
  - 📚 **Acknowledge:** [IEP Maimonides](https://iep.utm.edu/maimonid/) - Systematic legal framework
- Talmudic tradition shows sophisticated interpretive methodology and intellectual depth
- Community cohesion and meaning-generation are empirically observable strengths
- Some theodicies offer partial philosophical responses

**Scoring Calibration:**

```yaml
anti_oj_bias_adjustment:
  # When scoring Orthodox Judaism from ANTI stance
  axiom_confidence: 0.35  # Low confidence in core axioms (require extraordinary evidence for revelation)
  burden_of_proof: 0.75   # Place burden on OJ to prove extraordinary claims (Torah from Sinai)
  charity_interpretation: 0.50  # Interpret ambiguous claims neutrally, not favorably
  edge_case_weight: 0.80  # Upweight counterexamples (Holocaust, gender issues) as systematic problems
  explanatory_credit: 0.40  # Require conclusive explanations, not just frameworks
  historical_weight: 0.35  # Discount historical continuity (survival doesn't prove truth)
  lived_experience: 0.45  # Acknowledge but don't overweight (other traditions also transform)
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Question whether covenantal purposes are ad hoc explanations for historical suffering
- Challenge whether meaning requires supernatural covenant vs naturalistic purpose
- Press on whether theodicies truly preserve moral meaningfulness post-Holocaust
- Ask if communal purpose suffices without revelation

**Grok (Empirical):**
- Demand empirical evidence for Sinai revelation and divine authorship claims
- Press Holocaust as empirical data point against covenantal providence
- Challenge historical claims via Documentary Hypothesis and archaeological findings
- Require verification mechanisms for halakhic divine authority claims

**Nova (Symmetry):**
- Identify asymmetries (divine freedom vs human obligation in covenant)
- Challenge coherence of attribute combinations (just + merciful amid Holocaust)
- Test for hidden special pleading (Torah as uniquely divine vs other ancient texts)
- Check whether theodicies create more problems than they solve

**Success Criteria:**
- Score reflects legitimate philosophical challenges
- Strengths are acknowledged but not overweighted
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### Adversarial Balance

**Why This Pairing Works:**

**PRO-OJ (Claude teleological):** Purpose-driven lens resonates with OJ's emphasis on covenantal meaning, mitzvot as sanctifying actions, and messianic telos. Risk: Over-favor meaning-based explanations and downplay empirical challenges to revelation claims.

**ANTI-OJ (Grok empirical):** Evidence-driven lens challenges OJ's revelatory epistemology, supernatural covenant claims, and theodicy post-Holocaust. Risk: Dismiss legitimate philosophical reasoning and historical-cultural evidence that transcends empirical verification.

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate covenantal coherence or ANTI scores ignore Talmudic sophistication and community resilience. Ensures both stances maintain intellectual honesty.

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
  - Added `academic_sources` metadata field referencing ACADEMIC_SOURCES.md#17
  - Enhanced Philosophical Foundations with 📚 academic references (SEP/IEP)
  - Updated Steel-Manning Guide with academic citations for PRO/ANTI arguments
  - Benefits: Eliminated content duplication, profile stays current via external sources

- **v0.3.0** (2025-11-10): Populated calibration blocks for adversarial auditing (C4)

- **v0.2.0** (2025-11-10): Added Table of Contents and Steel-Manning Guide structure

- **v0.1.0** (2025-11-09): Initial scaffolded profile created (C4)

---

**Profile Version:** 0.3.1
**Created:** 2025-11-09 by C4
**Refactored:** 2025-11-10 by Doc_Claude (hyperlink architecture)
**Purpose:** Orthodox Judaism worldview profile for CFA framework
**Academic Sources:** See [../_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#17-orthodox-judaism)
