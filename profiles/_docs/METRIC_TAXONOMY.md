# Metric Taxonomy for CFA Profiles

**Purpose:** Define all metric categories, specific metrics, and standards for CFA worldview profiles

**Version:** 0.2.0 | **Status:** DRAFT | **Date:** 2025-11-09

<!---
FILE: METRIC_TAXONOMY.md
PURPOSE: Complete taxonomy of metrics used across all worldview profiles
VERSION: 0.2.0
STATUS: DRAFT
DEPENDS_ON: PROFILE_TEMPLATE.md
NEEDED_BY: All worldview profiles
MOVES_WITH: /auditors/relay/workshop/
LAST_UPDATE: 2025-11-09 [Profile Architecture Foundation - Nova Entry 4 approved]
--->

---

## Overview

This document defines the complete taxonomy of metrics used across all CFA (Comprehensive Framework Analysis) worldview profiles. Each worldview profile (Classical Theism, Methodological Naturalism, Buddhism, etc.) uses these same metric categories and definitions to enable meaningful comparison.

**Key Principles:**
1. **Consistency:** Same metric name = same meaning across all profiles
2. **Comparability:** Metrics designed to highlight where worldviews diverge
3. **Philosophical Rigor:** Each metric traces back to declared axioms
4. **Extensibility:** New metrics can be added following established patterns

---

## Metric Categories

### 1. Suffering Analysis

**Purpose:** Capture how different worldviews understand, weight, and respond to suffering

**Why This Matters:**
Suffering is a universal human experience, but worldviews differ dramatically in how they interpret it:
- Does suffering have meaning or purpose?
- Is it a problem to be solved or a mystery to be accepted?
- What causes suffering (natural, moral, metaphysical)?
- How should we respond to it?

These differences reveal deep commitments about the nature of reality, morality, and human flourishing.

**Metrics in This Category:**

#### 1.1 suffering_weight

```yaml
name: "suffering_weight"
type: "numeric"
unit: "normalized_scale"
range: [0, 100]
description: |
  Weight assigned to suffering as a factor in moral/philosophical evaluation.
  Higher values indicate suffering is given greater significance in the worldview's
  framework. Lower values suggest suffering is de-emphasized or reframed.

interpretation:
  0-25: "Suffering is minimized, reframed, or seen as illusory"
  26-50: "Suffering acknowledged but not primary concern"
  51-75: "Suffering is significant factor in moral evaluation"
  76-100: "Suffering is central/primary concern"

example_values:
  classical_theism: "[TBD - Grok deliberation]"
  methodological_naturalism: "[TBD - Grok deliberation]"
  buddhism: "[Expected higher - Four Noble Truths centered on suffering]"

justification_requirements:
  - axiom_connection: How does declared axiom inform this weight?
  - reasoning_process: What edge cases were considered?
  - assumptions: What assumptions about suffering's nature?
  - contestable_points: Where might reasonable people disagree?
```

#### 1.2 suffering_attribution

```yaml
name: "suffering_attribution"
type: "categorical"
unit: "category"
range: ["natural", "moral", "metaphysical", "meaningless", "mixed"]
description: |
  How this worldview attributes the source/cause of suffering.
  This reveals deep commitments about causation, agency, and cosmic order.

category_definitions:
  natural: "Suffering arises from natural processes (disease, disasters) without moral dimension"
  moral: "Suffering primarily results from moral evil (human choices, sin)"
  metaphysical: "Suffering is built into the structure of reality (karma, divine plan)"
  meaningless: "Suffering has no inherent meaning or purpose"
  mixed: "Multiple sources with no single dominant attribution"

example_values:
  classical_theism: "[Expected: mixed or moral - free will + natural evil framework]"
  methodological_naturalism: "[Expected: natural or meaningless - no teleology]"
  buddhism: "[Expected: metaphysical - karma and attachment]"

justification_requirements:
  - axiom_connection: How does declared axiom inform attribution?
  - reasoning_process: How are edge cases (innocent suffering) handled?
  - assumptions: What assumptions about causation and agency?
  - contestable_points: Where does attribution become ambiguous?
```

#### 1.3 suffering_response_priority

```yaml
name: "suffering_response_priority"
type: "ranked_categories"
unit: "priority_order"
range: ["eliminate", "alleviate", "accept", "transcend", "reframe"]
description: |
  Ranked priorities for how this worldview says we SHOULD respond to suffering.
  Reveals whether worldview is activist, contemplative, or mixed.

category_definitions:
  eliminate: "Primary goal is to eliminate suffering at its source"
  alleviate: "Primary goal is to reduce/mitigate suffering"
  accept: "Primary stance is acceptance of suffering as inevitable"
  transcend: "Primary goal is to transcend suffering through spiritual/philosophical means"
  reframe: "Primary approach is to reframe suffering's meaning rather than change it"

example_values:
  classical_theism: "[Expected: alleviate, accept, transcend - compassion + providence]"
  methodological_naturalism: "[Expected: eliminate, alleviate - medical/social solutions]"
  buddhism: "[Expected: transcend, accept - Eight fold Path to end dukkha]"

justification_requirements:
  - axiom_connection: How does axiom inform response priorities?
  - reasoning_process: Why this ordering?
  - assumptions: What practical or theological assumptions?
  - contestable_points: Where do priorities conflict?
```

---

### 2. Epistemological Foundations

**Purpose:** Capture how different worldviews approach knowledge, truth, and justification

**Why This Matters:**
Worldviews differ fundamentally in HOW we know things:
- What counts as a valid source of knowledge?
- How do we resolve conflicts between sources?
- What is the relationship between faith and reason?
- Can we have certainty, or only probability?

These differences affect every other aspect of the worldview, from morality to purpose.

**Metrics in This Category:**

#### 2.1 knowledge_source_priority

```yaml
name: "knowledge_source_priority"
type: "weighted_distribution"
unit: "percentage_weights"
range:
  revelation: [0, 100]
  reason: [0, 100]
  empiricism: [0, 100]
  intuition: [0, 100]
  tradition: [0, 100]
description: |
  Relative weights assigned to different sources of knowledge.
  Weights should sum to 100. Higher weight = greater epistemic authority.

source_definitions:
  revelation: "Divine disclosure, sacred texts, prophetic claims"
  reason: "Logical deduction, philosophical argument, rational inference"
  empiricism: "Sense experience, scientific observation, experimental data"
  intuition: "Direct apprehension, moral sense, phenomenological insight"
  tradition: "Historical wisdom, community practice, accumulated knowledge"

example_values:
  classical_theism: "{revelation: 40, reason: 30, empiricism: 15, intuition: 10, tradition: 5}"
  methodological_naturalism: "{revelation: 0, reason: 30, empiricism: 60, intuition: 5, tradition: 5}"
  buddhism: "{revelation: 0, reason: 20, empiricism: 20, intuition: 40, tradition: 20}"

justification_requirements:
  - axiom_connection: How does axiom privilege certain sources?
  - reasoning_process: How are conflicts between sources resolved?
  - assumptions: What assumptions about human cognitive capacity?
  - contestable_points: Where do sources overlap or conflict?
```

#### 2.2 truth_accessibility

```yaml
name: "truth_accessibility"
type: "categorical"
unit: "category"
range: ["fully_accessible", "partially_accessible", "asymptotically_accessible", "inaccessible"]
description: |
  To what extent can humans access ultimate truth/reality?
  This reveals epistemic humility or confidence.

category_definitions:
  fully_accessible: "All important truths are knowable with certainty (given time/effort)"
  partially_accessible: "Some truths knowable, others beyond human capacity"
  asymptotically_accessible: "Truth approachable but never fully reached (regulative ideal)"
  inaccessible: "Ultimate truth beyond human comprehension"

example_values:
  classical_theism: "[Expected: partially_accessible - revelation provides some, mystery remains]"
  methodological_naturalism: "[Expected: asymptotically_accessible - science progresses toward truth]"
  buddhism: "[Expected: partially_accessible - enlightenment possible, but not all are enlightened]"

justification_requirements:
  - axiom_connection: How does axiom inform accessibility?
  - reasoning_process: What limits human knowledge?
  - assumptions: What assumptions about truth's nature?
  - contestable_points: Where does accessibility become contested?
```

---

### 3. Moral Framework

**Purpose:** Capture how different worldviews ground morality and make ethical judgments

**Why This Matters:**
Worldviews differ on the very foundation of morality:
- Is morality objective or subjective?
- Where does moral obligation come from?
- How do we resolve moral dilemmas?
- What is the relationship between morality and flourishing?

These differences have profound practical implications for ethics, law, and social order.

**Metrics in This Category:**

#### 3.1 moral_foundation

```yaml
name: "moral_foundation"
type: "categorical"
unit: "category"
range: ["divine_command", "natural_law", "consequentialist", "deontological", "virtue_ethics", "relativist", "nihilist"]
description: |
  Primary basis for moral claims and obligations.
  This is the bedrock answer to "why is X wrong/right?"

category_definitions:
  divine_command: "Morality grounded in God's commands/nature"
  natural_law: "Morality grounded in objective natural order/teleology"
  consequentialist: "Morality grounded in outcomes/consequences"
  deontological: "Morality grounded in duties/rules/principles"
  virtue_ethics: "Morality grounded in character/virtues/flourishing"
  relativist: "Morality grounded in cultural/individual preferences"
  nihilist: "No objective moral foundation exists"

example_values:
  classical_theism: "[Expected: divine_command or natural_law]"
  methodological_naturalism: "[Expected: consequentialist, deontological, or virtue_ethics depending on thinker]"
  buddhism: "[Expected: virtue_ethics - cultivation of skillful qualities]"

justification_requirements:
  - axiom_connection: How does axiom ground moral claims?
  - reasoning_process: How are moral dilemmas resolved?
  - assumptions: What assumptions about human nature or agency?
  - contestable_points: Where does foundation become ambiguous?
```

#### 3.2 moral_objectivity

```yaml
name: "moral_objectivity"
type: "categorical"
unit: "category"
range: ["fully_objective", "partially_objective", "intersubjective", "subjective"]
description: |
  To what extent are moral truths mind-independent?
  This reveals commitments about moral realism.

category_definitions:
  fully_objective: "Moral truths exist independent of all minds (including God's if applicable)"
  partially_objective: "Some moral truths objective, others subjective or contextual"
  intersubjective: "Moral truths grounded in shared human nature/rationality but not fully independent"
  subjective: "Moral truths relative to individuals or cultures"

example_values:
  classical_theism: "[Expected: fully_objective or partially_objective - grounded in divine nature]"
  methodological_naturalism: "[Expected: varies - realists say intersubjective, anti-realists say subjective]"
  buddhism: "[Expected: partially_objective - karma laws objective, but contextual application]"

justification_requirements:
  - axiom_connection: How does axiom inform objectivity?
  - reasoning_process: What counts as objective vs subjective?
  - assumptions: What assumptions about mind-independence?
  - contestable_points: Where does objectivity become contested?
```

---

### 4. Teleological Commitments

**Purpose:** Capture how different worldviews understand purpose, meaning, and ultimate ends

**Why This Matters:**
Worldviews differ on whether reality has inherent purpose:
- Is there a cosmic telos (goal/purpose)?
- Do individual lives have objective meaning?
- Is purpose discovered or constructed?
- What is the ultimate end toward which we should strive?

These differences shape how we understand human flourishing, progress, and what makes life worth living.

**Metrics in This Category:**

#### 4.1 purpose_framework

```yaml
name: "purpose_framework"
type: "categorical"
unit: "category"
range: ["divine_purpose", "intrinsic_purpose", "constructed_purpose", "no_purpose"]
description: |
  Whether and how purpose/meaning exists in reality.
  This is the answer to "does life have meaning?"

category_definitions:
  divine_purpose: "Purpose externally given by divine being/plan"
  intrinsic_purpose: "Purpose built into nature/cosmos (but not necessarily divine)"
  constructed_purpose: "Purpose created by humans (existentialist)"
  no_purpose: "No objective purpose exists (nihilist)"

example_values:
  classical_theism: "[Expected: divine_purpose - God's plan for creation]"
  methodological_naturalism: "[Expected: constructed_purpose or no_purpose depending on thinker]"
  buddhism: "[Expected: intrinsic_purpose - escape samsara, achieve nirvana]"

justification_requirements:
  - axiom_connection: How does axiom inform purpose?
  - reasoning_process: How is purpose discovered/known?
  - assumptions: What assumptions about cosmic order?
  - contestable_points: Where does purpose become ambiguous?
```

#### 4.2 ultimate_end

```yaml
name: "ultimate_end"
type: "categorical"
unit: "category"
range: ["union_with_divine", "enlightenment_nirvana", "human_flourishing", "knowledge_truth", "pleasure_happiness", "survival_continuation", "none"]
description: |
  What is the ultimate goal/end toward which we should strive?
  This is the summum bonum (highest good).

category_definitions:
  union_with_divine: "Ultimate end is relationship with or union with God/divine"
  enlightenment_nirvana: "Ultimate end is spiritual enlightenment or escape from suffering"
  human_flourishing: "Ultimate end is eudaimonia, thriving, actualization"
  knowledge_truth: "Ultimate end is pursuit of knowledge/understanding"
  pleasure_happiness: "Ultimate end is maximizing pleasure or happiness"
  survival_continuation: "Ultimate end is survival of species/genes"
  none: "No ultimate end exists (nihilist)"

example_values:
  classical_theism: "[Expected: union_with_divine - beatific vision, glorification]"
  methodological_naturalism: "[Expected: varies - human_flourishing, knowledge_truth, or pleasure_happiness]"
  buddhism: "[Expected: enlightenment_nirvana - escape from dukkha]"

justification_requirements:
  - axiom_connection: How does axiom identify ultimate end?
  - reasoning_process: Why this end and not others?
  - assumptions: What assumptions about human nature or telos?
  - contestable_points: Where do ends conflict or overlap?
```

---

### 5. Anthropological Commitments

**Purpose:** Capture how different worldviews understand human nature, agency, and consciousness

**Why This Matters:**
Worldviews differ fundamentally in their understanding of what humans ARE:
- Is there an essential human nature, or is it constructed/emergent?
- What is the source and scope of human agency?
- Is consciousness purely physical, dualist, or something else?
- How does human nature relate to flourishing or purpose?

These differences shape views on ethics, freedom, identity, and what it means to be human.

**Metrics in This Category:**

#### 5.1 human_nature_baseline

```yaml
name: "human_nature_baseline"
type: "categorical"
unit: "category"
range: ["fallen", "neutral", "progressing", "illusory"]
description: |
  Baseline assessment of human nature in its default or starting state.
  This reveals whether worldview sees humans as fundamentally flawed,
  neutral, evolving, or perhaps not having a fixed nature at all.

category_definitions:
  fallen: "Human nature is corrupted, broken, or fallen from an ideal state (theological or philosophical)"
  neutral: "Human nature is neither good nor bad by default - morally blank slate"
  progressing: "Human nature is evolving/improving toward higher state (evolutionary, transhumanist)"
  illusory: "Fixed human nature is illusory - no essential self (Buddhist, some postmodern views)"

example_values:
  classical_theism: "[Expected: fallen - imago Dei corrupted by sin, requiring redemption]"
  methodological_naturalism: "[Expected: neutral or progressing - evolved nature without moral valence]"
  buddhism: "[Expected: illusory - anatta (no-self) doctrine]"

justification_requirements:
  - axiom_connection: How does declared axiom inform view of human nature?
  - reasoning_process: What anthropological framework supports this baseline?
  - assumptions: What assumptions about human origins or telos?
  - contestable_points: Where does anthropology become contested?
```

#### 5.2 agency_alignment

```yaml
name: "agency_alignment"
type: "ranked_categories"
unit: "priority_order"
range: ["divine_will", "natural_order", "personal_autonomy", "collective_design"]
description: |
  Ranked priorities for the source and direction of human agency.
  Reveals whether worldview sees human choices as primarily aligned with
  divine will, natural law, individual autonomy, or collective/social design.

category_definitions:
  divine_will: "Human agency properly aligned with God's will or divine purposes"
  natural_order: "Human agency aligned with natural law, telos, or cosmic order"
  personal_autonomy: "Human agency grounded in individual freedom and self-determination"
  collective_design: "Human agency shaped by and accountable to collective/social structures"

example_values:
  classical_theism: "[Expected: divine_will, natural_order, personal_autonomy - ordered loves]"
  methodological_naturalism: "[Expected: personal_autonomy, collective_design - social contract]"
  buddhism: "[Expected: natural_order, personal_autonomy - dharma and karma]"

justification_requirements:
  - axiom_connection: How does axiom inform agency priorities?
  - reasoning_process: Why this ordering of agency sources?
  - assumptions: What assumptions about freedom and moral responsibility?
  - contestable_points: Where do agency priorities conflict?
```

#### 5.3 consciousness_ontology

```yaml
name: "consciousness_ontology"
type: "categorical"
unit: "category"
range: ["dualist", "property_dualist", "physicalist", "panpsychist", "non_dual"]
description: |
  Ontological status of consciousness - what IS consciousness in this worldview?
  This reveals deep metaphysical commitments about mind, matter, and their relationship.

category_definitions:
  dualist: "Consciousness is non-physical substance distinct from matter (Cartesian dualism)"
  property_dualist: "Consciousness is emergent property of physical systems but not reducible"
  physicalist: "Consciousness is entirely physical - brain states, nothing more"
  panpsychist: "Consciousness is fundamental feature of all matter (degrees of consciousness)"
  non_dual: "Consciousness/matter distinction is ultimately illusory (Advaita, some Buddhism)"

example_values:
  classical_theism: "[Expected: dualist or property_dualist - soul as distinct from body]"
  methodological_naturalism: "[Expected: physicalist or property_dualist - no immaterial soul]"
  buddhism: "[Expected: non_dual - consciousness without inherent existence]"

justification_requirements:
  - axiom_connection: How does axiom inform consciousness ontology?
  - reasoning_process: What metaphysical framework supports this view?
  - assumptions: What assumptions about mind/body problem?
  - contestable_points: Where does consciousness account become contested?
```

---

### 6. Cosmological Commitments

**Purpose:** Capture how different worldviews understand the origin, structure, and fine-tuning of the cosmos

**Why This Matters:**
Worldviews differ on fundamental questions about physical reality:
- Did the universe have an origin, or is it eternal?
- Is causation deterministic, probabilistic, or open to libertarian agency?
- How do we explain cosmic fine-tuning for life?
- What does the universe's structure reveal about ultimate reality?

These differences affect views on divine action, scientific method, and cosmic meaning.

**Metrics in This Category:**

#### 6.1 origin_claim

```yaml
name: "origin_claim"
type: "categorical"
unit: "category"
range: ["creation", "eternal", "emergent", "brute_fact", "simulation"]
description: |
  How this worldview accounts for the universe's existence.
  This is the answer to "why is there something rather than nothing?"

category_definitions:
  creation: "Universe was created by divine being or intelligent designer"
  eternal: "Universe has always existed - no beginning"
  emergent: "Universe emerged from prior quantum/physical state (quantum fluctuation)"
  brute_fact: "Universe exists without explanation - brute contingent fact"
  simulation: "Universe is computational simulation by higher beings"

example_values:
  classical_theism: "[Expected: creation - creatio ex nihilo by God]"
  methodological_naturalism: "[Expected: emergent or brute_fact - no teleology required]"
  buddhism: "[Expected: eternal or emergent - cyclical cosmology without creator]"

justification_requirements:
  - axiom_connection: How does axiom inform origin account?
  - reasoning_process: What cosmological arguments support this claim?
  - assumptions: What assumptions about causation and contingency?
  - contestable_points: Where does origin account face objections?
```

#### 6.2 causal_structure

```yaml
name: "causal_structure"
type: "categorical"
unit: "category"
range: ["deterministic", "probabilistic", "libertarian_mix"]
description: |
  How causation operates in the universe according to this worldview.
  This reveals commitments about natural law, divine action, and freedom.

category_definitions:
  deterministic: "All events causally determined by prior states - no genuine openness"
  probabilistic: "Causation includes irreducible randomness (quantum indeterminacy)"
  libertarian_mix: "Some events causally determined, others open to libertarian agency (divine or human)"

example_values:
  classical_theism: "[Expected: libertarian_mix - natural law + divine providence + human free will]"
  methodological_naturalism: "[Expected: probabilistic or deterministic - closed causal system]"
  buddhism: "[Expected: deterministic or probabilistic - karma as causal law]"

justification_requirements:
  - axiom_connection: How does axiom inform causal structure?
  - reasoning_process: What physics/metaphysics supports this view?
  - assumptions: What assumptions about natural law and agency?
  - contestable_points: Where does causal account become contested?
```

#### 6.3 fine_tuning_account

```yaml
name: "fine_tuning_account"
type: "categorical"
unit: "category"
range: ["design", "multiverse", "brute_fact", "unknown"]
description: |
  How this worldview explains the apparent fine-tuning of physical constants for life.
  This is a key divergence point between theistic and naturalistic worldviews.

category_definitions:
  design: "Fine-tuning explained by intelligent designer setting parameters"
  multiverse: "Fine-tuning explained by many universes with varying constants (anthropic principle)"
  brute_fact: "Fine-tuning is just how things are - no explanation needed"
  unknown: "Fine-tuning requires explanation but current accounts are inadequate"

example_values:
  classical_theism: "[Expected: design - fine-tuning as evidence for divine designer]"
  methodological_naturalism: "[Expected: multiverse or brute_fact - naturalistic explanation]"
  buddhism: "[Expected: brute_fact or unknown - not central concern]"

justification_requirements:
  - axiom_connection: How does axiom inform fine-tuning account?
  - reasoning_process: What explanatory framework is used?
  - assumptions: What assumptions about design detection or probability?
  - contestable_points: Where do fine-tuning arguments face objections?
```

---

### 7. Eschatological Commitments

**Purpose:** Capture how different worldviews understand judgment, destiny, and ultimate ends

**Why This Matters:**
Worldviews differ on where everything is heading:
- Is there divine judgment or karmic consequence?
- What is the ultimate destiny of individuals and cosmos?
- How confident is this worldview about eschatological claims?
- Do eschatological beliefs affect present ethics and meaning?

These differences shape how people live in light of perceived ultimate outcomes.

**Metrics in This Category:**

#### 7.1 judgment_framework

```yaml
name: "judgment_framework"
type: "categorical"
unit: "category"
range: ["divine_judgment", "karma_cycle", "annihilation", "none"]
description: |
  How this worldview accounts for moral consequence in the cosmic order.
  This is the answer to "will there be justice/accountability?"

category_definitions:
  divine_judgment: "Moral accountability enforced by divine judgment (heaven/hell, reward/punishment)"
  karma_cycle: "Moral accountability through karmic causation and rebirth"
  annihilation: "Death is end of existence - no posthumous judgment"
  none: "No cosmic moral accountability - ethics are purely human/social"

example_values:
  classical_theism: "[Expected: divine_judgment - final judgment by God]"
  methodological_naturalism: "[Expected: none or annihilation - no cosmic justice]"
  buddhism: "[Expected: karma_cycle - rebirth determined by karma]"

justification_requirements:
  - axiom_connection: How does axiom inform judgment framework?
  - reasoning_process: What eschatological/soteriological framework supports this?
  - assumptions: What assumptions about moral order and agency?
  - contestable_points: Where does judgment account face objections?
```

#### 7.2 ultimate_destiny

```yaml
name: "ultimate_destiny"
type: "categorical"
unit: "category"
range: ["union_with_divine", "enlightenment", "heat_death", "cyclical_return", "uplift"]
description: |
  What is the ultimate end state for individuals/cosmos in this worldview?
  This reveals the telos or final purpose (if any) of existence.

category_definitions:
  union_with_divine: "Ultimate end is beatific vision, theosis, eternal communion with God"
  enlightenment: "Ultimate end is liberation from suffering/ignorance (nirvana, moksha)"
  heat_death: "Ultimate end is thermodynamic heat death of universe - no cosmic purpose"
  cyclical_return: "No ultimate end - eternal recurrence or cyclical rebirth"
  uplift: "Ultimate end is transhumanist/technological transcendence"

example_values:
  classical_theism: "[Expected: union_with_divine - eternal life with God]"
  methodological_naturalism: "[Expected: heat_death or uplift depending on thinker]"
  buddhism: "[Expected: enlightenment - nirvana as escape from samsara]"

justification_requirements:
  - axiom_connection: How does axiom inform ultimate destiny?
  - reasoning_process: What eschatological vision supports this end?
  - assumptions: What assumptions about cosmic telos?
  - contestable_points: Where do destiny claims face objections?
```

#### 7.3 eschatology_confidence

```yaml
name: "eschatology_confidence"
type: "numeric"
unit: "normalized_scale"
range: [0, 100]
description: |
  How confident is this worldview about its eschatological claims?
  Higher values indicate strong confidence in destiny/judgment framework.
  Lower values indicate agnosticism or epistemic humility about ultimate ends.

interpretation:
  0-25: "Highly agnostic about ultimate ends - eschatology not central or knowable"
  26-50: "Tentative eschatological claims - hope but not certainty"
  51-75: "Moderate confidence - eschatology important but some mystery remains"
  76-100: "High confidence - eschatological claims are certain/revealed"

example_values:
  classical_theism: "[Expected: 70-85 - revelation provides confidence but mystery remains]"
  methodological_naturalism: "[Expected: 40-60 - scientific predictions but cosmic purpose unclear]"
  buddhism: "[Expected: 65-80 - dharma provides path but ultimate reality beyond concepts]"

justification_requirements:
  - axiom_connection: How does axiom inform eschatological confidence?
  - reasoning_process: What epistemological factors affect confidence level?
  - assumptions: What assumptions about revelation or cosmic knowledge?
  - contestable_points: Where might confidence be challenged?
```

---

## Metric Standards

### Naming Conventions

**Format:** `{category}_{specific_descriptor}`

**Examples:**
- `suffering_weight` (category: suffering, descriptor: weight)
- `knowledge_source_priority` (category: knowledge, descriptor: source_priority)
- `moral_foundation` (category: moral, descriptor: foundation)

**Rules:**
- Use lowercase with underscores (snake_case)
- Keep names concise but descriptive
- Avoid acronyms unless universally understood
- Use consistent terminology across profiles

### Value Types

**Numeric (normalized_scale):**
- Range: 0-100
- Interpretation guide must be provided
- Example: suffering_weight

**Categorical:**
- Finite set of mutually exclusive categories
- Categories must be clearly defined
- Example: moral_foundation

**Weighted Distribution:**
- Multiple dimensions with percentage weights
- Must sum to 100
- Example: knowledge_source_priority

**Ranked Categories:**
- Ordered list of categories by priority
- Example: suffering_response_priority

### Justification Requirements

**Every metric must include:**
1. **axiom_connection:** 2-3 sentences linking metric to declared axiom
2. **reasoning_process:** Paragraph describing reasoning steps, edge cases
3. **assumptions:** Bulleted list of assumptions baked into metric
4. **contestable_points:** Bulleted list of where reasonable disagreement exists
5. **comparison_notes:** Cross-references to other profiles (CT and MdN minimum)
6. **methodological_notes:** Document deliberation modality, analytical tools, or scripts used
7. **evidence_threads:** REPO_LOG IDs, experiment links, or transcript references that support metric
8. **open_questions:** Bulleted list of unresolved tensions to revisit at next audit hook

### Deliberation Narrative Requirements

**Every metric must eventually include (Phase 3):**
1. **Prompt Stack:** Exact questions/prompts used in the deliberation
2. **Counterweight Table:** Claim vs counterclaim with resolution stamps
3. **Edge Case Ledger:** Numbered edge cases with keeper outcomes and next steps
4. **Mythology Capsule:** Shaman paragraph connecting axiom to outcome
5. **Decision Stamp:** Timestamp, participants, confidence band, Grok session ID, REPO_LOG reference

---

## Adding New Metrics

### Process

1. **Identify Gap:** Determine which philosophical dimension is not captured
2. **Define Metric:** Use standards above for naming, type, range
3. **Justify Addition:** Explain why this metric reveals worldview differences
4. **Add to Template:** Update PROFILE_TEMPLATE.md with new metric
5. **Backfill Profiles:** Add to all existing profiles with placeholder values
6. **Document Here:** Add to appropriate category in this taxonomy

### Quality Gates

**Before adding a new metric, ask:**
- Does this reveal a meaningful difference between worldviews?
- Is this distinct from existing metrics (not redundant)?
- Can this be applied across all worldviews (universal applicability)?
- Is the metric defined clearly enough for consistent use?

**Approval Required:**
- Nova validation against CFA context
- Ziggy approval for philosophical soundness
- C4 implementation in template and profiles

---

## Changelog

- **v0.2.0** (2025-11-09): Major expansion per Nova Entry 2 (C4 implementation)
  - 3 new categories added (Anthropological, Cosmological, Eschatological)
  - 9 new metrics added (3 per new category) with full specifications
  - Justification requirements expanded: +3 fields (methodological_notes, evidence_threads, open_questions)
  - Deliberation narrative scaffold specified: 5-part structure (Prompt Stack, Counterweight Table, Edge Case Ledger, Mythology Capsule, Decision Stamp)
  - Total: 7 categories, 18 metrics, 8 justification fields, 5-part deliberation framework
  - Awaiting Nova validation of implementation (KD-O2)

- **v0.1.0** (2025-11-09): Initial taxonomy created (C4)
  - 4 categories defined (Suffering, Epistemology, Morality, Teleology)
  - 9 metrics specified with full definitions
  - Standards for naming, justification, and deliberation narratives
  - Process for adding new metrics

---

**Next Steps:**
1. Nova validates C4 implementation of Entry 2 specifications (KD-O2)
2. Close KD-O1 and KD-O2 if validation passes
3. Close KD-O3 and proceed with production profiles (CT, MdN)
4. Apply this taxonomy structure to all worldview profiles

