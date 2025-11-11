# Classical Theism Profile

**Status:** DRAFT | **Version:** 0.3.0 | **Date:** 2025-11-10

<!---
FILE: worldviews/CLASSICAL_THEISM.md
PURPOSE: Worldview profile for Classical Theism with metrics, philosophical foundations, and deliberation narratives
VERSION: 0.3.0 - Refactored to hyperlink-based architecture
STATUS: DRAFT
DEPENDS_ON: ../_docs/METRIC_TAXONOMY.md, ../_docs/ACADEMIC_SOURCES.md, Trinity Architecture
NEEDED_BY: CFA analysis, worldview comparison tooling, Auditor steel-manning calibration
MOVES_WITH: /profiles/worldviews/
LAST_UPDATE: 2025-11-10 [Refactored to use academic source hyperlinks per ACADEMIC_SOURCES.md]
--->

---

## 📑 Table of Contents

**Core Sections:**
- [Metadata](#metadata) — Line 33
- [YPA Application Data](#ypa-application-data-cfa-v35) — Line 49
- [Mr. Brute's Ledger](#mr-brutes-ledger) — Line 95
- [Philosophical Foundations](#philosophical-foundations) — Line 167
- [Steel-Manning Guide](#steel-manning-guide) — Line 198
  - [PRO-CT Stance](#pro-classical-theism-stance) — Line 221
  - [ANTI-CT Stance](#anti-classical-theism-stance) — Line 295
- [Metrics](#metrics) — Line 369
- [Lifecycle Hooks](#lifecycle-hooks) — Line 471

**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-classical-theism-stance) (L221) | [ANTI Stance](#anti-classical-theism-stance) (L295)
- 👥 **Users:** [What is CT?](#philosophical-foundations) (L167) | [Axioms & Debts](#mr-brutes-ledger) (L95)
- 📚 **Academic Sources:** See [../\_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#1-classical-theism)

---

## Metadata

```yaml
profile:
  name: "Classical Theism"
  version: "0.3.0"
  status: "DRAFT"
  declared_axiom: "God exists as a necessary, perfect being who created and sustains the universe, and has revealed Himself through reason and special revelation"
  alternate_names: ["Traditional Theism", "Anselmian Theism", "Perfect Being Theology"]
  last_updated: "2025-11-10"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null  # Will be filled during Phase 4 - Grok integration
  academic_sources: "../_docs/ACADEMIC_SOURCES.md#1-classical-theism"
```

---

## YPA Application Data (CFA v3.5)

**Purpose:** This section documents the current YPA (Yield-Per-Axiom) lever values used by the CFA application. These values represent the *output* of philosophical deliberation and will eventually be derived from the foundational metrics below through a mapping layer.

**Status:** Legacy data - Preserved from `utils/frameworks.py` for app compatibility. Phase 4 goal: Justify these values through philosophical metrics + mapping rules.

```yaml
ypa_levers:
  # Categorical Confidence Index - How well this worldview handles conceptual/abstract challenges
  CCI: 7.5

  # Existential-Dread Bearing - How effectively this worldview addresses existential questions
  EDB: 8.5

  # Pragmatic Fertility (Instrumental) - Practical problem-solving capacity
  PF_instrumental: 7.0

  # Pragmatic Fertility (Existential) - Meaning/purpose-generating capacity
  PF_existential: 8.0

  # Asymptotic Realism - How well worldview tracks reality long-term
  AR: 8.5

  # Moral Generativity - Capacity to generate robust moral guidance
  MG: 8.5

brute_fact_index:
  # Number of foundational axioms required (unprovable starting points)
  axioms: 7

  # Number of explanatory debts (phenomena requiring further explanation)
  debts: 4

behavioral_flags:
  # Whether worldview acknowledges epistemic limitations
  admits_limits: true
```

**Integration Notes:**
- Current app references: `utils/frameworks.py:20-32`, `pages/console.py`, `pages/brute_ledger.py`
- Phase 2: Profile loader will extract these values for app consumption
- Phase 3: Mapping layer will derive YPA levers from philosophical metrics (suffering_weight, moral_foundation, etc.)
- Phase 4: Grok deliberations will justify *why* these specific values (e.g., why CCI=7.5 follows from CT's epistemological commitments)

---

## Mr. Brute's Ledger

**"To name your brute is to pay your fee. To deny you have one is to summon him twice."**

This section documents the unprovable assumptions (axioms) and unresolved questions (debts) that form Classical Theism's BFI (Brute-Fact Index). Mr. Brute is our accountability mechanism - a metaphor for intellectual honesty in acknowledging what every worldview must assume without proof.

```yaml
brute_ledger:
  axioms:
    count: 7
    list:
      - name: "Divine aseity/simplicity"
        description: "Posits that God exists necessarily and is metaphysically simple"
        academic_ref: "See [SEP Divine Simplicity](https://plato.stanford.edu/entries/divine-simplicity/#Moti)"

      - name: "Logos/intelligibility"
        description: "Claims God's rationality grounds cosmic order and comprehensibility"
        academic_ref: "See [IEP God, Western Concepts](https://iep.utm.edu/god-west/) (Omniscience section)"

      - name: "Revelation reliability"
        description: "Assumes Scripture/tradition reliably communicates divine truth"
        academic_ref: "See [IEP God, Western Concepts](https://iep.utm.edu/god-west/) (Special Revelation section)"

      - name: "Moral realism"
        description: "Claims objective moral facts exist, grounded in God's nature"
        academic_ref: "See [IEP God, Western Concepts](https://iep.utm.edu/god-west/) (Goodness section)"

      - name: "Teleology"
        description: "Posits purpose and design as fundamental features of reality"
        academic_ref: "Relates to divine providence - see [SEP Divine Providence](https://plato.stanford.edu/entries/providence-divine/)"

      - name: "PSR (Principle of Sufficient Reason)"
        description: "Everything has an explanation (in God)"
        academic_ref: "See cosmological arguments in [IEP God, Western Concepts](https://iep.utm.edu/god-west/)"

      - name: "Imago Dei"
        description: "Claims humans bear God's image, enabling knowledge and moral agency"
        academic_ref: "See [IEP God, Western Concepts](https://iep.utm.edu/god-west/) (Anthropology section)"

  debts:
    count: 4
    list:
      - name: "Divine hiddenness"
        description: "Why doesn't God make existence more evident?"
        academic_ref: "See [SEP Divine Hiddenness](https://plato.stanford.edu/entries/divine-hiddenness/) for scholarly debate"

      - name: "Problem of evil"
        description: "How does omnipotent/benevolent God permit suffering?"
        academic_ref: "See [SEP Problem of Evil](https://plato.stanford.edu/entries/evil/) for theodicy responses"

      - name: "Hermeneutic variance"
        description: "Why do interpretations of revelation differ?"
        academic_ref: "Related to religious diversity - see [SEP Religious Diversity](https://plato.stanford.edu/entries/religious-pluralism/)"

      - name: "Beauty→truth bridge"
        description: "Does aesthetic resonance actually track truth?"
        academic_ref: "Epistemological question - see [IEP God, Western Concepts](https://iep.utm.edu/god-west/) (Natural Theology section)"

  audit_notes: |
    **Why these axioms?**

    CT's axioms reflect commitments needed for a theistic worldview:
    - Divine attributes (aseity, simplicity) = foundation
    - Logos + PSR = intelligibility and explanation
    - Revelation + Imago Dei = knowledge possibility
    - Moral realism + Teleology = normative grounding

    **Why these debts?**

    CT acknowledges **mystery** - questions it can't fully resolve:
    - Theodicy (hiddenness, evil) remains debated for millennia
    - Hermeneutic variance (denominational differences) acknowledged
    - Beauty's epistemic role (does it track truth?) unclear

    This is **honest theology**, not evasion. CT names what it cannot fully explain.

    **Claude's perspective**: "CT's higher BFI reflects its comprehensive scope. It addresses questions MdN brackets—at a cost."

    **Grok's perspective**: "CT's debts (especially theodicy) remain live tensions. Acknowledging them maintains intellectual honesty."
```

---

## Philosophical Foundations

### Declared Axiom

Classical Theism begins with the axiom that **God exists as a necessary being possessing all perfections** (omniscience, omnipotence, omnibenevolence, immutability, simplicity, eternality). This God is the creator *ex nihilo* and sustainer of all contingent reality, and has made Himself known through both natural revelation (reason, creation) and special revelation (scripture, incarnation).

**📚 Academic Foundation:**
- **Core Definition:** [SEP Divine Simplicity](https://plato.stanford.edu/entries/divine-simplicity/#Moti) - Five primary motivations for classical attributes
- **Comprehensive Overview:** [IEP God, Western Concepts](https://iep.utm.edu/god-west/) - Historical development and attribute analysis
- **By Contrast:** [SEP Process Theism §Historical Notes](https://plato.stanford.edu/entries/process-theism/#HistNoteProcThei) - Distinguishes CT from alternatives

### Philosophical Framework

Classical Theism operates within the tradition of **medieval scholasticism**, particularly drawing from Anselm, Aquinas, and Maimonides, while maintaining roots in Augustinian Platonism and Aristotelian metaphysics.

**Core Methodological Commitments:**
- **Via Negativa** (knowing God through what He is not)
- **Analogical Predication** (speaking of God analogically rather than univocally or equivocally)
- **Divine Simplicity** (God's essence and existence are identical)

These commitments shape how CT approaches:
- **Epistemology:** Faith seeking understanding (*fides quaerens intellectum*)
- **Morality:** Divine command grounded in God's nature
- **Teleology:** Created purposes ordered toward God
- **Anthropology:** Humans as *imago Dei*

**📚 Detailed Analysis:**
- **Divine Simplicity:** [SEP Divine Simplicity §Constituent vs. Nonconstituent Ontology](https://plato.stanford.edu/entries/divine-simplicity/#ConsVersNoncOnto)
- **Divine Attributes:** [IEP God, Western Concepts](https://iep.utm.edu/god-west/) - Detailed sections on each attribute
- **Philosophical Method:** [SEP Divine Simplicity §Truthmaker Defense](https://plato.stanford.edu/entries/divine-simplicity/#TrutDefe)

### Key Distinguishing Features

What distinguishes Classical Theism from other profiles:
- **vs. Open Theism:** CT maintains God's timelessness and complete foreknowledge (see [IEP Open Theism](https://iep.utm.edu/o-theism/) for contrast)
- **vs. Process Theology:** CT affirms God's immutability and aseity (see [SEP Process Theism §Real Relations in God](https://plato.stanford.edu/entries/process-theism/#RealRelaGod) for contrast)
- **vs. Panentheism:** CT maintains asymmetrical Creator-creation relationship (see [SEP Panentheism §Nature of God/World Relation](https://plato.stanford.edu/entries/panentheism/#OntBas) for contrast)
- **vs. Naturalism:** CT affirms supernatural reality and non-empirical knowledge (see [SEP Naturalism](https://plato.stanford.edu/entries/naturalism/) for contrast)

### Key Principles

1. **Divine Perfection:** God possesses all perfections maximally and essentially - omniscience, omnipotence, perfect goodness, immutability, eternality, and simplicity are not contingent attributes but necessary features of God's nature.
   - 📚 **Arguments FOR:** [SEP Divine Simplicity §Motivation](https://plato.stanford.edu/entries/divine-simplicity/#Moti) - Five core arguments
   - 📚 **Objections:** [SEP Divine Simplicity §Question of Coherence](https://plato.stanford.edu/entries/divine-simplicity/#QuesCohe) - Plantinga's critique

2. **Creatio Ex Nihilo:** God created the universe from nothing by divine fiat, establishing contingent reality's complete dependence on necessary being. This grounds the distinction between Creator and creation, rejecting pantheism and panentheism.
   - 📚 **Analysis:** [IEP God, Western Concepts](https://iep.utm.edu/god-west/) (Creation and Providence sections)

3. **Imago Dei Anthropology:** Humans are created in God's image, possessing rationality, moral agency, and relationality, but are fallen through sin and require redemption through divine grace. This shapes views on human dignity, freedom, and ultimate destiny.
   - 📚 **Context:** [IEP God, Western Concepts](https://iep.utm.edu/god-west/) (Divine-Human Relationship section)

---

## Steel-Manning Guide

**Purpose:** This section provides guidance for AI auditors to calibrate their scoring when taking PRO or ANTI stances on Classical Theism. This enables adversarial auditing where auditors can advocate for or challenge this worldview while maintaining transparency about bias.

**Current Assignments:**
- **PRO-CT Stance:** Claude (Anthropic) - Teleological lens naturally aligns with purpose-driven metaphysics
- **ANTI-CT Stance:** Grok (xAI) - Empirical lens challenges non-empirical claims
- **Fairness Check:** Nova (OpenAI/Amazon) - Symmetry lens ensures balanced representation

**Note:** Assignments are dynamic and can be adjusted per scoring session via [../../auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)

---

### PRO-Classical Theism Stance

**Mission:** Advocate for Classical Theism's explanatory power, coherence, and capacity to address fundamental questions about reality, morality, and meaning.

**What to Emphasize:**
- **Coherence of divine attributes** when properly understood (via analogy, apophatic theology)
  - 📚 **Steel-man with:** [SEP Divine Simplicity §Motivation](https://plato.stanford.edu/entries/divine-simplicity/#Moti), [SEP Divine Simplicity §Truthmaker Defense](https://plato.stanford.edu/entries/divine-simplicity/#TrutDefe)
- **Explanatory power** for contingency, moral realism, consciousness, fine-tuning
  - 📚 **Steel-man with:** [IEP God, Western Concepts](https://iep.utm.edu/god-west/) (Arguments for God's Existence section)
- **Historical robustness** across cultures and millennia
  - 📚 **Context:** [IEP God, Western Concepts](https://iep.utm.edu/god-west/) (Historical Development sections)
- **Integration of reason and revelation** (faith seeking understanding)
- **Theodicies** that preserve divine goodness while acknowledging mystery
  - 📚 **Steel-man with:** [SEP Problem of Evil](https://plato.stanford.edu/entries/evil/) (Theodicy responses)
- **Transformative capacity** for human flourishing, meaning, and ethical motivation

**What to Acknowledge (Honest Advocacy):**
- Epistemic limitations (faith required beyond pure reason)
- Problem of evil remains existentially challenging even if philosophically defensible
  - 📚 **Acknowledge:** [SEP Problem of Evil](https://plato.stanford.edu/entries/evil/) (Evidential Problem section)
- Tension between immanence and transcendence
- Historical record includes misuse and harm
- Competitor worldviews have legitimate critiques
  - 📚 **Examples:** [SEP Divine Simplicity §Modal Collapse](https://plato.stanford.edu/entries/divine-simplicity/#ModaCollObjeDDS)

**Scoring Calibration:**

```yaml
pro_ct_bias_adjustment:
  # When scoring Classical Theism from PRO stance
  axiom_confidence: 0.85  # High confidence in core axioms (divine simplicity, aseity, providence)
  burden_of_proof: 0.40   # Place burden on critics to disprove rather than CT to prove
  charity_interpretation: 0.90  # Interpret ambiguous claims in most favorable light
  edge_case_weight: 0.30  # Downweight counterexamples as exceptions not disproofs
  explanatory_credit: 0.85  # Credit CT for addressing fundamental questions even if not conclusive
  historical_weight: 0.75  # Weight historical robustness and cultural staying power
  lived_experience: 0.80  # Credit transformative capacity and existential resonance
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Emphasize purpose/meaning explanations as core strength
- Connect divine simplicity to ultimate ontological unity
- Frame theodicies as preserving meaningful moral order
- Highlight coherence of eschatological hope with human longing for justice

**Grok (Empirical):**
- Cite cosmological fine-tuning as empirical pointer
- Reference moral psychology data on religious motivation
- Acknowledge limits of empiricism for metaphysical questions
- Use comparative theology to show CT's explanatory scope

**Nova (Symmetry):**
- Show balance between transcendence and immanence
- Demonstrate coherence across attributes (omnipotence + omnibenevolence)
- Map symmetry between divine simplicity and explanatory parsimony
- Check for internal consistency in theodicies

**Success Criteria:**
- Score reflects CT's explanatory ambitions and historical robustness
- Critiques are acknowledged but framed as challenges not refutations
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### ANTI-Classical Theism Stance

**Mission:** Challenge Classical Theism's coherence, evidential support, and capacity to address suffering, diversity, and epistemic accessibility.

**What to Emphasize:**
- **Problem of evil** (horrendous evils, natural evil, divine hiddenness)
  - 📚 **Challenge with:** [SEP Problem of Evil](https://plato.stanford.edu/entries/evil/) (Evidential Problem section), [SEP Divine Hiddenness](https://plato.stanford.edu/entries/divine-hiddenness/)
- **Incoherence charges** (omnipotence paradoxes, immutability + responsiveness)
  - 📚 **Challenge with:** [SEP Divine Simplicity §Question of Coherence](https://plato.stanford.edu/entries/divine-simplicity/#QuesCohe) (Plantinga's objection), [SEP Divine Simplicity §Modal Collapse](https://plato.stanford.edu/entries/divine-simplicity/#ModaCollObjeDDS)
- **Lack of empirical verification** for core claims
  - 📚 **Compare with:** [SEP Naturalism §Methodological Naturalism](https://plato.stanford.edu/entries/naturalism/#MetNat)
- **Religious diversity** undermines exclusivist truth claims
  - 📚 **Challenge with:** [SEP Religious Diversity](https://plato.stanford.edu/entries/religious-pluralism/)
- **Historical harms** and institutional corruption
- **Alternative explanations** (naturalism, Buddhism) without theological baggage
  - 📚 **Alternatives:** [SEP Naturalism](https://plato.stanford.edu/entries/naturalism/), [SEP Buddha](https://plato.stanford.edu/entries/buddha/)

**What to Acknowledge (Honest Opposition):**
- CT has sophisticated philosophical defenses (free will theodicy, greater good)
  - 📚 **Acknowledge:** [SEP Problem of Evil](https://plato.stanford.edu/entries/evil/) (Theodicy responses)
- Some questions (why is there something rather than nothing) remain difficult for alternatives
- Lived experience and transformative capacity are real phenomena
- Metaphysical naturalism has its own explanatory gaps (consciousness, moral realism)
  - 📚 **Acknowledge:** [SEP Naturalism](https://plato.stanford.edu/entries/naturalism/) (Challenges section)
- Historical staying power suggests some resonance with human experience

**Scoring Calibration:**

```yaml
anti_ct_bias_adjustment:
  # When scoring Classical Theism from ANTI stance
  axiom_confidence: 0.35  # Low confidence in core axioms (require extraordinary evidence)
  burden_of_proof: 0.75   # Place burden on CT to prove extraordinary claims
  charity_interpretation: 0.50  # Interpret ambiguous claims neutrally, not favorably
  edge_case_weight: 0.80  # Upweight counterexamples as evidence of systematic problems
  explanatory_credit: 0.40  # Require conclusive explanations, not just frameworks
  historical_weight: 0.30  # Discount historical robustness (appeal to tradition fallacy)
  lived_experience: 0.45  # Acknowledge but don't overweight (other worldviews also transform)
```

**Auditor Lens Calibration:**

**Claude (Teleological):**
- Question whether divine purposes are ad hoc explanations
- Challenge whether meaning requires transcendent grounding
- Press on whether theodicies truly preserve moral meaningfulness
- Ask if naturalistic purpose (Darwinian, existentialist) suffices

**Grok (Empirical):**
- Demand empirical evidence for divine attributes
- Press problem of evil as empirical data point against omnibenevolence
- Challenge fine-tuning via multiverse or anthropic principle
- Require verification mechanisms for theological claims

**Nova (Symmetry):**
- Identify asymmetries (divine freedom vs human freedom)
- Challenge coherence of attribute combinations (immutable + responsive)
- Test for hidden special pleading (God as necessary being)
- Check whether theodicies create more problems than they solve

**Success Criteria:**
- Score reflects legitimate philosophical challenges to CT
- Strengths are acknowledged but not overweighted
- Bias is disclosed (see calibration values above)
- Other auditors can verify scoring rationale

---

### Adversarial Balance

**Why This Pairing Works:**

**PRO-CT (Claude teleological):** Purpose-driven lens naturally resonates with CT's emphasis on divine intentions, meaningful creation, and eschatological fulfillment. Risk: Over-favor meaning-based explanations even when evidence is thin.

**ANTI-CT (Grok empirical):** Evidence-driven lens naturally challenges CT's non-empirical metaphysical claims and theological explanations for suffering. Risk: Dismiss legitimate philosophical reasoning that transcends empirical verification.

**Fairness Check (Nova symmetry):** Pattern-driven lens catches when PRO scores inflate strengths or ANTI scores ignore sophisticated defenses. Ensures both stances maintain intellectual honesty.

**Target:** 98% convergence after adversarial checking. If scores diverge significantly, auditors deliberate until consensus or document irreconcilable differences as **Crux Points** (see [../../auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)).

---

## Metrics

_Note: All metric values are PLACEHOLDERS pending Phase 3 Grok deliberation sessions. The deliberation narratives below are templates to be filled during philosophical reasoning with Grok._

### Suffering Analysis

Analysis of how Classical Theism understands, weights, and responds to suffering.

#### Metric: Suffering Weight

```yaml
metric:
  name: "suffering_weight"
  value: 0  # PLACEHOLDER - to be determined via Grok deliberation
  type: "scale"
  unit: "weight"
  range: [0, 100]
  description: |
    How heavily does this worldview weight suffering in moral/existential calculus?
    0=suffering is illusory or irrelevant, 100=suffering is the primary moral reality

justification:
  axiom_connection: |
    Classical Theism's axiom that God is omnipotent, omnibenevolent, and providential creates a framework where suffering is real and significant but not ultimate. The axiom requires that suffering serve purposes within divine providence (soul-making, free will consequences, greater goods) while acknowledging the genuine evil and pain of the fallen world. Suffering matters deeply because humans are imago Dei, but it is not the final word because redemption and resurrection overcome it.

  reasoning_process: |
    The reasoning moves from: (1) God's perfect goodness means He wills only good, (2) suffering exists as real evil, (3) therefore suffering must serve purposes consistent with divine goodness (free will, soul-making theodicies), or remain mystery within the limits of human epistemic access. Classical Theism rejects pure consequentialism (suffering as mere means) and pure stoicism (suffering as illusion) in favor of a middle position: suffering is real, significant, and to be alleviated, but is penultimate rather than ultimate.

  academic_grounding: |
    📚 **Theodicy Frameworks:**
    - Free will theodicy: [SEP Problem of Evil §Free Will Defense](https://plato.stanford.edu/entries/evil/)
    - Soul-making theodicy: [SEP Problem of Evil §Soul-Making Theodicy](https://plato.stanford.edu/entries/evil/)
    - Divine hiddenness: [SEP Divine Hiddenness](https://plato.stanford.edu/entries/divine-hiddenness/)

    📚 **Critiques to Consider:**
    - Evidential problem of evil: [SEP Problem of Evil §Evidential Problem](https://plato.stanford.edu/entries/evil/)
    - Horrendous evils objection: See scholarly debate in SEP Problem of Evil

  assumptions:
    - "Divine providence governs all events including permission of suffering"
    - "Human free will is genuine and can produce moral evil"
    - "Some suffering serves soul-making or greater-good purposes"
    - "Epistemic humility required - not all suffering's purposes are knowable"
    - "Eschatological hope transforms present suffering's significance"

  contestable_points:
    - "Whether free will theodicy adequately explains natural evil (earthquakes, disease)"
    - "Whether soul-making theodicy justifies extreme suffering (infant mortality, genocide)"
    - "Whether divine goodness is compatible with permission of horrendous evils"
    - "Whether eschatological vindication truly redeems present suffering"

  comparison_notes:
    methodological_naturalism: "MdN weights suffering more heavily as primary moral reality with no cosmic compensation; CT sees suffering as penultimate, not ultimate"
    buddhism: "Buddhism sees suffering as fundamental to existence (dukkha) requiring escape; CT sees suffering as consequence of fall requiring redemption"
    stoicism: "Stoicism emphasizes virtue over suffering management; CT maintains suffering is real evil requiring divine redemption"

  methodological_notes: |
    [To be filled during Grok deliberation - will document Socratic questioning method, comparative theology framework, edge case analysis of problem of evil variants]

  evidence_threads: |
    [To be filled during Grok deliberation - will reference REPO_LOG entries, session transcripts, theological literature (Plantinga, Adams, Swinburne)]

  open_questions:
    - "How to weight innocent suffering with no apparent soul-making value?"
    - "Boundary between natural evil (divine permission) and moral evil (human free will)"
    - "Whether divine simplicity allows God to experience or respond to suffering"
```

**Deliberation Narrative:**

[This section will capture the STORY of how this metric was determined during Phase 3 Grok integration]

**1. Prompt Stack**

[Exact questions/prompts used in the Grok deliberation - to be filled Phase 3]

**2. Counterweight Table**

[Claim vs counterclaim with resolution stamps - to be filled Phase 3]

| Claim | Counterclaim | Resolution |
|-------|--------------|------------|
| [TBD] | [TBD] | [TBD] |

**3. Edge Case Ledger**

[Numbered edge cases with keeper outcomes - to be filled Phase 3]

**4. Mythology Capsule**

[Shaman paragraph connecting axiom to outcome - to be filled Phase 3]

**5. Decision Stamp**

- **Timestamp:** [TBD Phase 3]
- **Participants:** [Grok, C4, Nova, Ziggy]
- **Confidence Band:** [TBD]
- **Grok Session ID:** [TBD]
- **REPO_LOG Reference:** [TBD]

**Why This Weight:**

[Concise 1-paragraph summary connecting axiom → principle → value - to be filled Phase 3]

---

_[Note: Template includes 13 additional metrics across 6 remaining categories. For initial production deployment, only suffering_weight is fully scaffolded. Remaining metrics (epistemology, morality, teleology, anthropology, cosmology, eschatology) will follow same structure during Phase 3 Grok deliberation sessions.]_

---

## Lifecycle Hooks

Profile-specific guidance for Trinity Architecture hooks.

### Bootstrap Hook

```yaml
hook:
  name: "bootstrap"
  trigger: "New auditor or new machine initializing with this profile"
  actions:
    - "Ensure declared axiom is clearly stated: God exists as necessary perfect being"
    - "Verify all metric categories have structure (even if placeholder values)"
    - "Check that philosophical foundations align with Classical Theistic tradition"
    - "Verify academic_sources reference in metadata points to valid ACADEMIC_SOURCES.md entry"
    - "Log initialization in REPO_LOG with profile version and date"
  keeper_role: "Guard Classical Theism's core commitments (divine perfection, creatio ex nihilo, imago Dei)"
  logger_role: "Record bootstrap event with machine ID, profile version, any customizations"
  shaman_role: "Verify mythology (axiom/principles) grounds all metrics and deliberations"
```

**Narrative:**
The Bootstrap Hook ensures that every new auditor or machine initializing with Classical Theism starts from the same axiomatic foundation and structural integrity. The Keeper verifies core theological commitments, the Logger preserves initialization metadata for traceability, and the Shaman confirms that the philosophical foundations remain coherent with the declared axiom.

---

### Audit Hook

```yaml
hook:
  name: "audit"
  trigger: "Scheduled review or pre-release validation"
  actions:
    - "Compare metrics against METRIC_TAXONOMY.md canonical definitions"
    - "Verify justification blocks reference axiom/principles consistently"
    - "Check deliberation narratives have complete 5-part scaffold"
    - "Validate comparison_notes reference other live profiles (MdN minimum)"
    - "Ensure REPO_LOG entries referenced in evidence_threads exist"
    - "Verify academic source links are valid and point to correct sections"
    - "Check academic_grounding blocks cite appropriate SEP/IEP articles"
  keeper_role: "Structural integrity check - metrics match taxonomy, no drift"
  logger_role: "Document audit findings, version changes, discrepancies resolved"
  shaman_role: "Mythology check - does axiom still coherently ground all metrics?"
```

**Narrative:**
Regular audits prevent silent drift in the Classical Theism profile. The Keeper ensures structural consistency with the canonical taxonomy, the Logger documents any corrections or updates, and the Shaman verifies that the philosophical foundations remain internally coherent. This hook catches errors before they propagate to production use.

---

### Incident Hook

```yaml
hook:
  name: "incident"
  trigger: "Metric produces unexpected result or comparison shows inconsistency"
  actions:
    - "Flag the specific metric and circumstance that triggered incident"
    - "Review justification block for that metric - is reasoning sound?"
    - "Check if axiom_connection needs refinement"
    - "Verify academic_grounding references support the metric value"
    - "Add incident details to metric's open_questions"
    - "Log incident in REPO_LOG with severity and resolution plan"
  keeper_role: "Isolate incident - prevent cascade to other metrics"
  logger_role: "Capture full incident context for future reference and learning"
  shaman_role: "Assess if incident reveals mythology/mechanism misalignment"
```

**Narrative:**
When Classical Theism's metrics produce unexpected results or show inconsistencies with other profiles, the Incident Hook activates. The Keeper isolates the problem metric, the Logger preserves full context for investigation, and the Shaman determines whether the issue stems from foundational assumptions or implementation details. This hook transforms errors into learning opportunities.

---

### Release Hook

```yaml
hook:
  name: "release"
  trigger: "Profile approved for production use in CFA tooling"
  actions:
    - "Freeze profile version with semantic versioning (major.minor.patch)"
    - "Generate changelog documenting all changes since last release"
    - "Tag Grok session IDs that contributed to this version"
    - "Validate all academic source links are accessible"
    - "Update REPO_LOG with release notes and validation status"
    - "Archive pre-release draft for rollback capability"
  keeper_role: "Final validation - profile meets quality gates before release"
  logger_role: "Preserve complete release documentation and change history"
  shaman_role: "Confirm mythology layer is production-ready and coherent"
```

**Narrative:**
The Release Hook marks the transition from draft to production-ready. The Keeper performs final validation against quality gates, the Logger generates comprehensive release documentation, and the Shaman confirms the philosophical foundations are coherent and defensible. This hook ensures Classical Theism profiles are trustworthy for production CFA analysis.

---

### Deliberation Hook

```yaml
hook:
  name: "deliberation"
  trigger: "Grok session or multi-model debate kickoff for metric determination"
  actions:
    - "Freeze metric edits during deliberation to preserve consistency"
    - "Log prompt pack metadata (questions, frameworks, constraints used)"
    - "Capture raw transcripts of debates and reasoning processes"
    - "Tag Grok session ID in profile metadata for traceability"
    - "Document consensus points and contested areas"
    - "Reference academic sources consulted during deliberation"
  keeper_role: "Guard structural integrity during deliberation process"
  logger_role: "Store deliberation artifacts (prompts, transcripts, decisions)"
  shaman_role: "Watch for mythology drift during value assignment"
```

**Narrative:**
The Deliberation Hook marks the critical moment when philosophical reasoning converts to metric values. When engaging Grok to determine "why this number" for Classical Theism's metrics, this hook ensures the reasoning process is captured completely. The Keeper freezes edits to prevent mid-deliberation changes, the Logger preserves the entire deliberation trail, and the Shaman monitors whether the theological foundations stay grounded throughout.

---

### Comparative Audit Hook

```yaml
hook:
  name: "comparative_audit"
  trigger: "Metric adjustment prompted by another worldview profile moving"
  actions:
    - "Run diff between Classical Theism and the updated profile"
    - "Refresh comparison_notes fields to reflect new divergences"
    - "Log rationale for synchronized deltas (if any)"
    - "Check for ripple effects on other metrics in this profile"
    - "Update deliberation narratives with new cross-profile insights"
    - "Verify academic sources still support comparative claims"
  keeper_role: "Ensure consistency across profile ecosystem"
  logger_role: "Document why and how profiles evolved together or apart"
  shaman_role: "Verify comparative mythology remains sound"
```

**Narrative:**
When Methodological Naturalism or another profile's metrics change, Classical Theism may need to adjust comparison_notes to maintain accurate cross-references. The Comparative Audit Hook ensures these ripple effects are intentional and documented. The Keeper checks for structural consistency, the Logger documents the rationale for changes, and the Shaman ensures the comparative theology remains coherent.

---

## Changelog

- **v0.3.0** (2025-11-10): Refactored to hyperlink-based architecture
  - Replaced long philosophical expositions with hyperlinks to academic sources (SEP/IEP)
  - Added `academic_sources` field to metadata pointing to ACADEMIC_SOURCES.md
  - Enhanced axioms/debts with inline academic references
  - Updated Steel-Manning Guide with academic source citations for PRO/ANTI arguments
  - Added `academic_grounding` field to metric justification blocks
  - Maintained all CFA-specific content (bias calibrations, VuDu coordination, lifecycle hooks)
  - Updated audit hooks to validate academic source links
  - Benefits: Eliminated content duplication, profiles stay current via external sources, lean repo focused on scoring framework

- **v0.2.0** (2025-11-10): Added Steel-Manning Guide and Table of Contents
  - Implemented PRO/ANTI stance calibration blocks with quantified bias adjustments
  - Added auditor lens-specific guidance (Claude/Grok/Nova)
  - Added adversarial balance rationale
  - Created navigable Table of Contents with line numbers
  - Quick links for auditors and users

- **v0.1.0** (2025-11-09): Initial production profile created (C4)
  - Structure based on PROFILE_TEMPLATE.md v0.2.0 (validated KD-C6)
  - Declared axiom, philosophical foundations, and key principles defined
  - suffering_weight metric fully scaffolded with justification framework and 5-part deliberation template
  - All 6 Trinity lifecycle hooks implemented with Classical Theism-specific guidance
  - Remaining 13 metrics stubbed - awaiting Phase 3 Grok deliberation sessions
  - Status: DRAFT - not production-ready until Grok integration completes metric values

---

## Notes for Phase 3 Development

**Grok Deliberation Priority:**
1. Complete suffering_weight metric (already scaffolded)
2. Epistemological metrics (revelation_weight, rational_confidence)
3. Moral/teleological metrics (moral_source, purpose_framework)
4. Anthropological/cosmological/eschatological metrics

**Cross-Profile Consistency:**
- Ensure comparison_notes reciprocally reference Methodological Naturalism (minimum)
- Add references to priority worldviews: Orthodox Judaism, Mormonism, Error Theory, Null Hypothesis, Desiderata believers

**Quality Gates Before v1.0:**
- All 14 metrics have Grok-determined values
- All deliberation narratives complete with 5-part scaffold
- All comparison_notes reference live profiles
- All academic source links validated and accessible
- Keeper/Logger/Shaman audits pass
- Ziggy approval for philosophical rigor and transparency

---

**Profile Version:** 0.3.0
**Created:** 2025-11-09 by C4
**Refactored:** 2025-11-10 by Doc_Claude (hyperlink architecture)
**Purpose:** Classical Theism worldview profile for CFA framework
**Usage:** Production-ready after Phase 3 Grok integration completes metric deliberations
**Academic Sources:** See [../_docs/ACADEMIC_SOURCES.md](../_docs/ACADEMIC_SOURCES.md#1-classical-theism)
