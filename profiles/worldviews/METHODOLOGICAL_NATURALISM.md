# Methodological Naturalism Profile

**Status:** DRAFT | **Version:** 0.1.0 | **Date:** 2025-11-09

<!---
FILE: worldviews/METHODOLOGICAL_NATURALISM.md
PURPOSE: Worldview profile for Methodological Naturalism with metrics, philosophical foundations, and deliberation narratives
VERSION: 0.1.0
STATUS: DRAFT
DEPENDS_ON: ../_docs/METRIC_TAXONOMY.md, Trinity Architecture
NEEDED_BY: CFA analysis, worldview comparison tooling
MOVES_WITH: /profiles/worldviews/
LAST_UPDATE: 2025-11-10 [Reorganized directory structure]
--->

---

## Metadata

```yaml
profile:
  name: "Methodological Naturalism"
  version: "0.1.0"
  status: "DRAFT"
  declared_axiom: "The natural world operates according to consistent, discoverable laws without supernatural intervention; knowledge claims require empirical evidence and methodological rigor"
  alternate_names: ["Scientific Naturalism", "Methodological Physicalism", "Empirical Naturalism"]
  last_updated: "2025-11-09"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null  # Will be filled during Phase 4 - Grok integration
```

---

## YPA Application Data (CFA v3.5)

**Purpose:** This section documents the current YPA (Yield-Per-Axiom) lever values used by the CFA application. These values represent the *output* of philosophical deliberation and will eventually be derived from the foundational metrics below through a mapping layer.

**Status:** Legacy data - Preserved from `utils/frameworks.py` for app compatibility. Phase 4 goal: Justify these values through philosophical metrics + mapping rules.

```yaml
ypa_levers:
  # Categorical Confidence Index - How well this worldview handles conceptual/abstract challenges
  CCI: 8.0

  # Existential-Dread Bearing - How effectively this worldview addresses existential questions
  EDB: 7.5

  # Pragmatic Fertility (Instrumental) - Practical problem-solving capacity
  PF_instrumental: 10.0

  # Pragmatic Fertility (Existential) - Meaning/purpose-generating capacity
  PF_existential: 3.0

  # Asymptotic Realism - How well worldview tracks reality long-term
  AR: 7.0

  # Moral Generativity - Capacity to generate robust moral guidance
  MG: 4.0

brute_fact_index:
  # Number of foundational axioms required (unprovable starting points)
  axioms: 6

  # Number of explanatory debts (phenomena requiring further explanation)
  debts: 4

behavioral_flags:
  # Whether worldview acknowledges epistemic limitations
  admits_limits: true
```

**Integration Notes:**
- Current app references: `utils/frameworks.py:6-18`, `pages/console.py`, `pages/brute_ledger.py`
- Phase 2: Profile loader will extract these values for app consumption
- Phase 3: Mapping layer will derive YPA levers from philosophical metrics (suffering_weight, moral_foundation, etc.)
- Phase 4: Grok deliberations will justify *why* these specific values (e.g., why PF_instrumental=10.0 follows from MdN's empirical evidentialism)

**Comparative Notes:**
- **vs Classical Theism:** Higher CCI (8.0 vs 7.5) reflects empirical evidence standards; Lower EDB (7.5 vs 8.5) reflects naturalistic constraints on existential meaning; Dramatically higher PF_instrumental (10.0 vs 7.0) reflects scientific method's problem-solving power; Dramatically lower PF_existential (3.0 vs 8.0) reflects lack of transcendent purpose framework; Lower MG (4.0 vs 8.5) reflects challenges grounding objective morality without divine command

---

## Mr. Brute's Ledger

**"To name your brute is to pay your fee. To deny you have one is to summon him twice."**

This section documents the unprovable assumptions (axioms) and unresolved questions (debts) that form Methodological Naturalism's BFI (Brute-Fact Index). Mr. Brute is our accountability mechanism - a metaphor for intellectual honesty in acknowledging what every worldview must assume without proof.

```yaml
brute_ledger:
  axioms:
    count: 6
    list:
      - name: "Regularity exists"
        description: "The universe operates according to consistent patterns"

      - name: "Cognition is reliable"
        description: "Our minds can track reality (at least approximately)"

      - name: "Testing arbitrates"
        description: "Empirical testing can distinguish better from worse explanations"

      - name: "Natural causation default"
        description: "Assume natural causes unless evidence suggests otherwise"

      - name: "Parsimony works"
        description: "Simpler explanations are generally more likely to be true"

      - name: "Findings are provisional"
        description: "All conclusions remain open to revision"

  debts:
    count: 4
    list:
      - name: "Why does regularity exist?"
        description: "No explanation for why universe has laws"

      - name: "Why does cognition track truth?"
        description: "Evolution explains survival, not truth-tracking"

      - name: "Why does success = truth?"
        description: "No grounding for equating predictive success with truth"

      - name: "Why pursue knowledge?"
        description: "No internal justification for epistemic values"

  audit_notes: |
    **Why these axioms?**

    MdN's axioms reflect the minimal commitments needed for scientific practice:
    - Regularity + Cognition = ability to investigate
    - Testing + Natural causation = methodological toolkit
    - Parsimony + Provisionality = self-correcting discipline

    **Why these debts?**

    MdN **brackets** (sets aside) questions it can't answer empirically:
    - Metaphysical foundations (why regularities?)
    - Epistemological grounding (why cognition works?)
    - Normative justification (why pursue truth?)

    This is **intellectual honesty**, not weakness. MdN admits what it can and cannot explain.

    **Grok's perspective**: "MdN's lean BFI reflects its disciplined scope. It doesn't claim to answer everything—just what's testable."

    **Claude's perspective**: "MdN's debts reveal its dependence on external grounding. It's a powerful method, but not a complete worldview."
```

---

## Philosophical Foundations

### Declared Axiom

Methodological Naturalism begins with the axiom that the natural world operates according to consistent, discoverable laws, and that knowledge claims about reality must be grounded in empirical evidence and methodological rigor. This worldview brackets (but does not necessarily deny) supernatural or metaphysical claims that cannot be tested empirically, focusing instead on what can be known through observation, experimentation, and inference to the best explanation.

### Philosophical Framework

Methodological Naturalism operates within the scientific tradition, drawing from logical positivism, pragmatism, and naturalized epistemology. While often associated with philosophical naturalism (the metaphysical claim that only natural entities exist), methodological naturalism is technically neutral on ultimate metaphysical questions, focusing instead on methodological constraints: what counts as evidence, how to test hypotheses, and what explanations are admissible in scientific inquiry.

Core commitments include: empiricism (knowledge comes from sensory experience and experimentation), fallibilism (all knowledge claims are provisional and subject to revision), parsimony (prefer simpler explanations over complex ones), and methodological materialism (explain phenomena through natural causes without invoking supernatural agency). These commitments shape how Methodological Naturalism approaches epistemology (empirical verification), morality (evolutionary ethics, social contract), teleology (purposeless cosmos), and anthropology (humans as evolved biological organisms).

What distinguishes Methodological Naturalism from other profiles is its methodological agnosticism about ultimate questions (meaning, purpose, transcendence) combined with epistemic confidence about the natural world. It rejects appeals to divine revelation, a priori metaphysics, or supernatural causation in explanatory frameworks, while remaining technically compatible with various metaphysical views (atheism, agnosticism, deism) at the personal level.

### Key Principles

1. **Empirical Evidentialism:** Knowledge claims about reality require empirical evidence derived from observation, experimentation, and reproducible results. Non-empirical claims (metaphysical, theological) are epistemically bracketed as untestable.

2. **Causal Closure:** The physical world operates as a causally closed system governed by natural laws. Explanations invoke natural causes and mechanisms without recourse to supernatural intervention or teleological purposes.

3. **Methodological Parsimony:** Prefer simpler, naturalistic explanations over complex, supernatural ones (Occam's Razor applied to scientific inquiry). Supernatural hypotheses are methodologically inadmissible regardless of metaphysical possibility.

---

## Metrics

_Note: All metric values are PLACEHOLDERS pending Phase 3 Grok deliberation sessions. The deliberation narratives below are templates to be filled during philosophical reasoning with Grok._

### Suffering Analysis

Analysis of how Methodological Naturalism understands, weights, and responds to suffering.

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
    Methodological Naturalism's axiom that the natural world operates without supernatural intervention or cosmic justice creates a framework where suffering is the primary moral reality requiring human response. Since there is no divine compensation, eschatological vindication, or karmic rebalancing, present suffering is ultimate - its alleviation depends entirely on human agency, social structures, and medical/technological intervention. The axiom grounds a high suffering weight because naturalism lacks transcendent mechanisms for redeeming or transforming suffering beyond its empirical reality.

  reasoning_process: |
    The reasoning moves from: (1) No supernatural agency intervenes to prevent or redeem suffering, (2) suffering is a biological/psychological reality produced by natural causes (disease, injury, loss), (3) therefore suffering's moral weight is maximal - it is not penultimate but ultimate, with no cosmic scales balancing it. Methodological Naturalism rejects theodicies (soul-making, greater goods) as unfalsifiable and instead emphasizes reduction of suffering through science, medicine, social reform, and compassionate human action. The high weight reflects naturalism's lack of transcendent hope or cosmic meaning that could relativize present suffering.

  assumptions:
    - "No divine providence or cosmic justice governs suffering distribution"
    - "Suffering is produced by natural causes (evolution, entropy, biology)"
    - "Present suffering is ultimate - no afterlife compensation or karmic adjustment"
    - "Human agency is primary means of alleviating suffering"
    - "Empirical measurement of suffering (pain scales, quality of life metrics) is possible"

  contestable_points:
    - "Whether suffering's ultimacy increases or decreases its moral weight"
    - "Whether naturalism can ground objective moral obligation to alleviate suffering"
    - "Whether evolutionary accounts of suffering (natural selection) undermine its moral significance"
    - "Whether hedonic calculus adequately captures suffering's complexity"

  comparison_notes:
    classical_theism: "CT weights suffering as significant but penultimate (redemption, eschatology transform it); MdN weights it as ultimate and primary moral reality"
    buddhism: "Buddhism sees suffering as universal condition requiring escape (nirvana); MdN sees suffering as contingent biological reality requiring alleviation"

  methodological_notes: |
    [To be filled during Grok deliberation - will document empirical ethics framework, utilitarian calculus considerations, evolutionary psychology insights on suffering]

  evidence_threads: |
    [To be filled during Grok deliberation - will reference REPO_LOG entries, session transcripts, literature (Singer, Harris, Greene on moral psychology)]

  open_questions:
    - "How to weight suffering's ultimacy against naturalism's lack of objective moral grounding?"
    - "Whether evolutionary debunking arguments undermine suffering's moral weight"
    - "Boundary between descriptive (suffering exists) and prescriptive (suffering matters morally)"
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
    - "Ensure declared axiom is clearly stated: Natural world operates by discoverable laws"
    - "Verify all metric categories have structure (even if placeholder values)"
    - "Check that philosophical foundations align with naturalistic/empiricist tradition"
    - "Log initialization in REPO_LOG with profile version and date"
  keeper_role: "Guard Methodological Naturalism's core commitments (empiricism, causal closure, parsimony)"
  logger_role: "Record bootstrap event with machine ID, profile version, any customizations"
  shaman_role: "Verify methodology (empirical evidence) grounds all metrics and deliberations"
```

**Narrative:**
The Bootstrap Hook ensures that every new auditor or machine initializing with Methodological Naturalism starts from the same methodological foundation and structural integrity. The Keeper verifies core methodological commitments, the Logger preserves initialization metadata for traceability, and the Shaman confirms that the empirical foundations remain coherent with the declared axiom.

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
    - "Validate comparison_notes reference other live profiles (CT minimum)"
    - "Ensure REPO_LOG entries referenced in evidence_threads exist"
  keeper_role: "Structural integrity check - metrics match taxonomy, no drift"
  logger_role: "Document audit findings, version changes, discrepancies resolved"
  shaman_role: "Methodology check - does empirical grounding still cohere?"
```

**Narrative:**
Regular audits prevent silent drift in the Methodological Naturalism profile. The Keeper ensures structural consistency with the canonical taxonomy, the Logger documents any corrections or updates, and the Shaman verifies that the methodological foundations remain internally coherent. This hook catches errors before they propagate to production use.

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
    - "Add incident details to metric's open_questions"
    - "Log incident in REPO_LOG with severity and resolution plan"
  keeper_role: "Isolate incident - prevent cascade to other metrics"
  logger_role: "Capture full incident context for future reference and learning"
  shaman_role: "Assess if incident reveals methodology/mechanism misalignment"
```

**Narrative:**
When Methodological Naturalism's metrics produce unexpected results or show inconsistencies with other profiles, the Incident Hook activates. The Keeper isolates the problem metric, the Logger preserves full context for investigation, and the Shaman determines whether the issue stems from methodological assumptions or implementation details. This hook transforms errors into learning opportunities.

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
    - "Update REPO_LOG with release notes and validation status"
    - "Archive pre-release draft for rollback capability"
  keeper_role: "Final validation - profile meets quality gates before release"
  logger_role: "Preserve complete release documentation and change history"
  shaman_role: "Confirm methodology layer is production-ready and coherent"
```

**Narrative:**
The Release Hook marks the transition from draft to production-ready. The Keeper performs final validation against quality gates, the Logger generates comprehensive release documentation, and the Shaman confirms the methodological foundations are coherent and defensible. This hook ensures Methodological Naturalism profiles are trustworthy for production CFA analysis.

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
  keeper_role: "Guard structural integrity during deliberation process"
  logger_role: "Store deliberation artifacts (prompts, transcripts, decisions)"
  shaman_role: "Watch for methodology drift during value assignment"
```

**Narrative:**
The Deliberation Hook marks the critical moment when empirical reasoning and philosophical analysis convert to metric values. When engaging Grok to determine "why this number" for Methodological Naturalism's metrics, this hook ensures the reasoning process is captured completely. The Keeper freezes edits to prevent mid-deliberation changes, the Logger preserves the entire deliberation trail, and the Shaman monitors whether the empirical foundations stay grounded throughout.

---

### Comparative Audit Hook

```yaml
hook:
  name: "comparative_audit"
  trigger: "Metric adjustment prompted by another worldview profile moving"
  actions:
    - "Run diff between Methodological Naturalism and the updated profile"
    - "Refresh comparison_notes fields to reflect new divergences"
    - "Log rationale for synchronized deltas (if any)"
    - "Check for ripple effects on other metrics in this profile"
    - "Update deliberation narratives with new cross-profile insights"
  keeper_role: "Ensure consistency across profile ecosystem"
  logger_role: "Document why and how profiles evolved together or apart"
  shaman_role: "Verify comparative methodology remains sound"
```

**Narrative:**
When Classical Theism or another profile's metrics change, Methodological Naturalism may need to adjust comparison_notes to maintain accurate cross-references. The Comparative Audit Hook ensures these ripple effects are intentional and documented. The Keeper checks for structural consistency, the Logger documents the rationale for changes, and the Shaman ensures the comparative analysis remains methodologically sound.

---

## Changelog

- **v0.1.0** (2025-11-09): Initial production profile created (C4)
  - Structure based on PROFILE_TEMPLATE.md v0.2.0 (validated KD-C6)
  - Declared axiom, philosophical foundations, and key principles defined
  - suffering_weight metric fully scaffolded with justification framework and 5-part deliberation template
  - All 6 Trinity lifecycle hooks implemented with Methodological Naturalism-specific guidance
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
- Ensure comparison_notes reciprocally reference Classical Theism (minimum)
- Add references to priority worldviews: Orthodox Judaism, Mormonism, Error Theory, Null Hypothesis, Desiderata believers

**Quality Gates Before v1.0:**
- All 14 metrics have Grok-determined values
- All deliberation narratives complete with 5-part scaffold
- All comparison_notes reference live profiles
- Keeper/Logger/Shaman audits pass
- Ziggy approval for philosophical rigor and transparency

---

**Profile Version:** 0.1.0
**Created:** 2025-11-09 by C4
**Purpose:** Methodological Naturalism worldview profile for CFA framework
**Usage:** Production-ready after Phase 3 Grok integration completes metric deliberations
