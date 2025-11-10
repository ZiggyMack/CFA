# [Profile Name] Profile

**Status:** DRAFT | **Version:** 0.2.0 | **Date:** 2025-11-09

<!---
FILE: [PROFILE_NAME].md
PURPOSE: Worldview profile with metrics, philosophical foundations, and deliberation narratives
VERSION: 0.2.0
STATUS: DRAFT
DEPENDS_ON: METRIC_TAXONOMY.md, Trinity Architecture
NEEDED_BY: CFA analysis, worldview comparison tooling
MOVES_WITH: /profiles/
LAST_UPDATE: 2025-11-09 [Profile Architecture Foundation - Nova Entry 4 fixes]
--->

---

## Metadata

```yaml
profile:
  name: "[Profile Name]"
  version: "0.1.0"
  status: "DRAFT"
  declared_axiom: "[Core axiom or brute fact position - e.g., 'God exists and has revealed Himself through classical theistic claims']"
  alternate_names: ["[Alternative name 1]", "[Alternative name 2]"]
  last_updated: "2025-11-09"
  maintainers: ["Ziggy", "Grok", "C4", "Nova"]
  grok_deliberation_session: null  # Will be filled during Phase 3
```

---

## Philosophical Foundations

### Declared Axiom

[2-3 sentences explaining the core axiom or brute fact position this profile starts from]

### Philosophical Framework

[2-3 paragraphs describing:
- What philosophical tradition or school of thought does this profile operate within?
- What are the core commitments that flow from the declared axiom?
- How does this worldview approach questions of knowledge, morality, purpose, etc.?
- What distinguishes this profile from others in the CFA framework?]

### Key Principles

1. **[Principle Name]:** [1-2 sentence description]
2. **[Principle Name]:** [1-2 sentence description]
3. **[Principle Name]:** [1-2 sentence description]

---

## Metrics

### Suffering Analysis

Analysis of how this worldview understands, weights, and responds to suffering.

#### Metric: Suffering Weight

```yaml
metric:
  name: "suffering_weight"
  value: 0  # PLACEHOLDER - awaiting Grok deliberation
  unit: "normalized_scale"
  range: [0, 100]
  description: "Weight assigned to suffering as a factor in moral/philosophical evaluation"

justification:
  axiom_connection: |
    [2-3 sentences explaining how this worldview's declared axiom
    informs its understanding of suffering. E.g., "Classical Theism
    holds that suffering has potential meaning within divine providence..."]

  reasoning_process: |
    [Paragraph describing the reasoning steps from axiom to metric.
    Include edge cases considered, distinctions made, etc. E.g.,
    "Given the axiom, we reasoned through several edge cases:
    1. Suffering with known purpose vs unknown purpose
    2. Temporary suffering vs eternal consequences
    3. Individual suffering vs collective redemption"]

  assumptions:
    - "[Assumption 1 - e.g., 'Divine omniscience includes knowledge of suffering's ultimate purpose']"
    - "[Assumption 2 - e.g., 'Free will framework allows for morally significant choices']"
    - "[Assumption 3 - e.g., 'Suffering can serve redemptive or pedagogical functions']"

  contestable_points:
    - "[Point 1 - e.g., 'The weight assigned assumes a specific theodicy framework']"
    - "[Point 2 - e.g., 'Different traditions within this worldview might weight differently']"
    - "[Point 3 - e.g., 'The boundary between meaningful/meaningless suffering is debatable']"

  comparison_notes:
    classical_theism: "[How does this compare to CT's approach?]"
    methodological_naturalism: "[How does this compare to MdN's approach?]"

  methodological_notes: |
    [Document the deliberation modality, analytical tools, or scripts used.
    E.g., "Used Socratic questioning with Grok to explore edge cases;
    applied comparative theology framework from Plantinga's analysis"]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, or transcript references that support this metric.
    E.g., "REPO_LOG entry #47 (2025-11-15); Grok session transcript:
    grok_session_abc123; Bootstrap reference: B-STORM_2 Entry 8"]

  open_questions:
    - "[Unresolved tension 1 - e.g., 'How to weight infant suffering with no moral framework?']"
    - "[Unresolved tension 2 - e.g., 'Boundary between natural/moral evil remains contested']"
    - "[Unresolved tension 3 - e.g., 'Cross-tradition variance not yet fully explored']"
```

**Deliberation Narrative:**

[This section captures the STORY of how this metric was determined. To be filled during Grok integration (Phase 3).]

**1. Prompt Stack**

[Exact questions/prompts used in the deliberation]

Example:
- Initial framing: "Given [worldview]'s axiom that [X], how should suffering factor into moral evaluation?"
- Follow-up 1: "How does this worldview handle innocent suffering with no apparent purpose?"
- Follow-up 2: "Where does [worldview] diverge from [comparison worldview] on suffering's significance?"
- Closing: "On a 0-100 scale, what weight captures this worldview's stance?"

**2. Counterweight Table**

[Claim vs counterclaim with resolution stamps]

| Claim | Counterclaim | Resolution |
|-------|--------------|------------|
| [E.g., "Suffering has redemptive value, so weight should be moderate"] | [E.g., "Innocent suffering with no explanation challenges redemptive framing"] | [E.g., "Weight accounts for both - higher than pure naturalism, lower than pure consequentialism"] |
| [Claim 2] | [Counterclaim 2] | [Resolution 2] |

**3. Edge Case Ledger**

[Numbered edge cases with keeper outcomes and next steps]

1. **Edge Case:** [E.g., "Infant suffering with no moral agency"]
   - **Keeper Assessment:** [How this challenges the metric]
   - **Outcome:** [How it was resolved or noted as open question]
   - **Next Steps:** [Future deliberation needed? Noted in open_questions?]

2. **Edge Case:** [Example 2]
   - **Keeper Assessment:** [Assessment]
   - **Outcome:** [Outcome]
   - **Next Steps:** [Next steps]

**4. Mythology Capsule**

[Shaman paragraph connecting axiom to outcome]

[E.g., "Classical Theism's axiom that God exists and governs providentially creates a mythology where suffering is neither meaningless nor the primary reality. The axiom shapes the metric by requiring weight that acknowledges suffering's significance (against pure Stoicism) while maintaining hope in redemptive purpose (against pure consequentialism). The number 65 reflects this tension - high enough to show moral seriousness, low enough to leave room for divine purposes beyond human comprehension. This is the mythology informing the mechanism."]

**5. Decision Stamp**

- **Timestamp:** [YYYY-MM-DD HH:MM UTC]
- **Participants:** [E.g., "Grok, C4, Nova"]
- **Confidence Band:** [E.g., "High (80-95%)" or "Medium (60-80%)" or "Low (<60%)"]
- **Grok Session ID:** [E.g., "grok_session_abc123"]
- **REPO_LOG Reference:** [E.g., "Entry #47"]

**Why This Number:**

[Concise 1-paragraph summary connecting axiom → principle → value]

We settled on [value] because it reflects [worldview]'s commitment to [principle], while acknowledging [limitation or boundary condition]. Reasonable people might challenge this on the grounds of [contestable point], but given our declared axiom, this value maintains internal consistency with [philosophical framework or tradition].

---

#### Metric: Suffering Attribution

```yaml
metric:
  name: "suffering_attribution"
  value: 0  # PLACEHOLDER
  unit: "categorical"
  range: ["natural", "moral", "metaphysical", "meaningless", "mixed"]
  description: "How this worldview attributes the source/cause of suffering"

justification:
  axiom_connection: |
    [How does the declared axiom inform attribution of suffering's source?]

  reasoning_process: |
    [Reasoning steps and distinctions made]

  assumptions:
    - "[Assumption 1]"
    - "[Assumption 2]"

  contestable_points:
    - "[Point 1]"
    - "[Point 2]"

  comparison_notes:
    classical_theism: "[Comparison]"
    methodological_naturalism: "[Comparison]"

  methodological_notes: |
    [Document deliberation modality, analytical tools, or scripts used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, or transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[To be filled during Phase 3]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Value:**

[Summary]

---

### Epistemological Foundations

How this worldview approaches knowledge, truth, and justification.

#### Metric: Knowledge Source Priority

```yaml
metric:
  name: "knowledge_source_priority"
  value: 0  # PLACEHOLDER
  unit: "weighted_ranking"
  range: {revelation: 0, reason: 0, empiricism: 0, intuition: 0, tradition: 0}
  description: "Relative weights assigned to different sources of knowledge"

justification:
  axiom_connection: |
    [How does the axiom inform epistemology?]

  reasoning_process: |
    [Reasoning steps]

  assumptions:
    - "[Assumption 1]"
    - "[Assumption 2]"

  contestable_points:
    - "[Point 1]"
    - "[Point 2]"

  comparison_notes:
    classical_theism: "[Comparison]"
    methodological_naturalism: "[Comparison]"

  methodological_notes: |
    [Document deliberation modality, analytical tools, or scripts used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, or transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[To be filled during Phase 3]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why These Weights:**

[Summary]

---

### Moral Framework

How this worldview grounds morality and makes ethical judgments.

#### Metric: Moral Foundation

```yaml
metric:
  name: "moral_foundation"
  value: 0  # PLACEHOLDER
  unit: "categorical"
  range: ["divine_command", "natural_law", "consequentialist", "deontological", "virtue_ethics", "relativist", "nihilist"]
  description: "Primary basis for moral claims and obligations"

justification:
  axiom_connection: |
    [How does axiom ground morality?]

  reasoning_process: |
    [Reasoning steps]

  assumptions:
    - "[Assumption 1]"
    - "[Assumption 2]"

  contestable_points:
    - "[Point 1]"
    - "[Point 2]"

  comparison_notes:
    classical_theism: "[Comparison]"
    methodological_naturalism: "[Comparison]"

  methodological_notes: |
    [Document deliberation modality, analytical tools, or scripts used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, or transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[To be filled during Phase 3]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Foundation:**

[Summary]

---

### Teleological Commitments

How this worldview understands purpose, meaning, and ultimate ends.

#### Metric: Purpose Framework

```yaml
metric:
  name: "purpose_framework"
  value: 0  # PLACEHOLDER
  unit: "categorical"
  range: ["divine_purpose", "intrinsic_purpose", "constructed_purpose", "no_purpose"]
  description: "Whether and how purpose/meaning exists in reality"

justification:
  axiom_connection: |
    [How does axiom inform purpose/teleology?]

  reasoning_process: |
    [Reasoning steps]

  assumptions:
    - "[Assumption 1]"
    - "[Assumption 2]"

  contestable_points:
    - "[Point 1]"
    - "[Point 2]"

  comparison_notes:
    classical_theism: "[Comparison]"
    methodological_naturalism: "[Comparison]"

  methodological_notes: |
    [Document deliberation modality, analytical tools, or scripts used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, or transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[To be filled during Phase 3]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Framework:**

[Summary]

---

### Anthropological Commitments

How this worldview understands human nature, agency, and consciousness.

#### Metric: Human Nature Baseline

```yaml
metric:
  name: "human_nature_baseline"
  value: 0  # PLACEHOLDER
  unit: "categorical"
  range: ["essential_fixed", "essential_malleable", "constructed_stable", "constructed_fluid", "emergent_only"]
  description: "Whether human nature is essential, constructed, or purely emergent"

justification:
  axiom_connection: |
    [How does axiom inform view of human nature?]

  reasoning_process: |
    [Walk through reasoning: fixed essence vs constructed identity vs emergent properties]

  assumptions:
    - "[Assumption 1 about human nature]"
    - "[Assumption 2]"

  contestable_points:
    - "[Where reasonable disagreement exists]"

  comparison_notes:
    classical_theism: "[How CT differs on human nature]"
    methodological_naturalism: "[How MdN differs on human nature]"

  methodological_notes: |
    [Document deliberation modality, analytical tools used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[Story of how this metric was determined - to be filled during Grok integration]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Baseline:**

[Summary]

---

#### Metric: Agency Alignment

```yaml
metric:
  name: "agency_alignment"
  value: 0  # PLACEHOLDER
  unit: "scale"
  range: [0, 100]
  description: "Degree to which human agency is real vs illusory (0=fully determined, 100=libertarian free will)"

justification:
  axiom_connection: |
    [How does axiom inform view of human agency?]

  reasoning_process: |
    [Walk through reasoning: determinism vs compatibilism vs libertarian freedom]

  assumptions:
    - "[Assumption 1 about agency]"
    - "[Assumption 2]"

  contestable_points:
    - "[Where reasonable disagreement exists]"

  comparison_notes:
    classical_theism: "[How CT differs on agency]"
    methodological_naturalism: "[How MdN differs on agency]"

  methodological_notes: |
    [Document deliberation modality, analytical tools used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[Story of how this metric was determined - to be filled during Grok integration]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Alignment:**

[Summary]

---

#### Metric: Consciousness Ontology

```yaml
metric:
  name: "consciousness_ontology"
  value: 0  # PLACEHOLDER
  unit: "categorical"
  range: ["substance_dualism", "property_dualism", "emergent_materialism", "eliminative_materialism", "idealism"]
  description: "Ontological status of consciousness and mental states"

justification:
  axiom_connection: |
    [How does axiom inform view of consciousness?]

  reasoning_process: |
    [Walk through reasoning: mind-body relationship, mental causation]

  assumptions:
    - "[Assumption 1 about consciousness]"
    - "[Assumption 2]"

  contestable_points:
    - "[Where reasonable disagreement exists]"

  comparison_notes:
    classical_theism: "[How CT differs on consciousness]"
    methodological_naturalism: "[How MdN differs on consciousness]"

  methodological_notes: |
    [Document deliberation modality, analytical tools used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[Story of how this metric was determined - to be filled during Grok integration]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Ontology:**

[Summary]

---

### Cosmological Commitments

How this worldview understands the origin, structure, and fine-tuning of the cosmos.

#### Metric: Origin Claim

```yaml
metric:
  name: "origin_claim"
  value: 0  # PLACEHOLDER
  unit: "categorical"
  range: ["divine_creation", "necessary_existence", "brute_fact", "eternal_universe", "multiverse_framework"]
  description: "Account of cosmic origins and why universe exists"

justification:
  axiom_connection: |
    [How does axiom inform view of cosmic origins?]

  reasoning_process: |
    [Walk through reasoning: necessity vs contingency, explanation vs brute fact]

  assumptions:
    - "[Assumption 1 about origins]"
    - "[Assumption 2]"

  contestable_points:
    - "[Where reasonable disagreement exists]"

  comparison_notes:
    classical_theism: "[How CT differs on origins]"
    methodological_naturalism: "[How MdN differs on origins]"

  methodological_notes: |
    [Document deliberation modality, analytical tools used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[Story of how this metric was determined - to be filled during Grok integration]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Origin:**

[Summary]

---

#### Metric: Causal Structure

```yaml
metric:
  name: "causal_structure"
  value: 0  # PLACEHOLDER
  unit: "categorical"
  range: ["primary_secondary", "natural_only", "overdetermined", "occasionalism", "no_causation"]
  description: "Nature of causality in the universe"

justification:
  axiom_connection: |
    [How does axiom inform view of causation?]

  reasoning_process: |
    [Walk through reasoning: primary vs secondary causes, natural law]

  assumptions:
    - "[Assumption 1 about causation]"
    - "[Assumption 2]"

  contestable_points:
    - "[Where reasonable disagreement exists]"

  comparison_notes:
    classical_theism: "[How CT differs on causation]"
    methodological_naturalism: "[How MdN differs on causation]"

  methodological_notes: |
    [Document deliberation modality, analytical tools used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[Story of how this metric was determined - to be filled during Grok integration]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Structure:**

[Summary]

---

#### Metric: Fine-Tuning Account

```yaml
metric:
  name: "fine_tuning_account"
  value: 0  # PLACEHOLDER
  unit: "categorical"
  range: ["design", "necessity", "chance", "multiverse", "brute_fact", "selection_effect"]
  description: "Explanation for cosmic fine-tuning for life"

justification:
  axiom_connection: |
    [How does axiom inform view of fine-tuning?]

  reasoning_process: |
    [Walk through reasoning: design vs chance vs necessity]

  assumptions:
    - "[Assumption 1 about fine-tuning]"
    - "[Assumption 2]"

  contestable_points:
    - "[Where reasonable disagreement exists]"

  comparison_notes:
    classical_theism: "[How CT differs on fine-tuning]"
    methodological_naturalism: "[How MdN differs on fine-tuning]"

  methodological_notes: |
    [Document deliberation modality, analytical tools used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[Story of how this metric was determined - to be filled during Grok integration]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Account:**

[Summary]

---

### Eschatological Commitments

How this worldview understands judgment, destiny, and ultimate ends.

#### Metric: Judgment Framework

```yaml
metric:
  name: "judgment_framework"
  value: 0  # PLACEHOLDER
  unit: "categorical"
  range: ["divine_judgment", "karmic_rebirth", "natural_consequence", "none", "transformation"]
  description: "Nature and mechanism of ultimate judgment or accountability"

justification:
  axiom_connection: |
    [How does axiom inform view of judgment?]

  reasoning_process: |
    [Walk through reasoning: accountability, justice, consequences]

  assumptions:
    - "[Assumption 1 about judgment]"
    - "[Assumption 2]"

  contestable_points:
    - "[Where reasonable disagreement exists]"

  comparison_notes:
    classical_theism: "[How CT differs on judgment]"
    methodological_naturalism: "[How MdN differs on judgment]"

  methodological_notes: |
    [Document deliberation modality, analytical tools used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[Story of how this metric was determined - to be filled during Grok integration]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Framework:**

[Summary]

---

#### Metric: Ultimate Destiny

```yaml
metric:
  name: "ultimate_destiny"
  value: 0  # PLACEHOLDER
  unit: "categorical"
  range: ["eternal_communion", "annihilation", "reincarnation", "naturalistic_end", "universal_restoration"]
  description: "Final state or end of human existence"

justification:
  axiom_connection: |
    [How does axiom inform view of ultimate destiny?]

  reasoning_process: |
    [Walk through reasoning: afterlife, continuation, finality]

  assumptions:
    - "[Assumption 1 about destiny]"
    - "[Assumption 2]"

  contestable_points:
    - "[Where reasonable disagreement exists]"

  comparison_notes:
    classical_theism: "[How CT differs on destiny]"
    methodological_naturalism: "[How MdN differs on destiny]"

  methodological_notes: |
    [Document deliberation modality, analytical tools used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[Story of how this metric was determined - to be filled during Grok integration]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Destiny:**

[Summary]

---

#### Metric: Eschatology Confidence

```yaml
metric:
  name: "eschatology_confidence"
  value: 0  # PLACEHOLDER
  unit: "scale"
  range: [0, 100]
  description: "Epistemic confidence in eschatological claims (0=agnostic, 100=certainty)"

justification:
  axiom_connection: |
    [How does axiom inform confidence in ultimate ends?]

  reasoning_process: |
    [Walk through reasoning: epistemic access, revelation, speculation]

  assumptions:
    - "[Assumption 1 about eschatological knowledge]"
    - "[Assumption 2]"

  contestable_points:
    - "[Where reasonable disagreement exists]"

  comparison_notes:
    classical_theism: "[How CT differs on eschatological confidence]"
    methodological_naturalism: "[How MdN differs on eschatological confidence]"

  methodological_notes: |
    [Document deliberation modality, analytical tools used]

  evidence_threads: |
    [REPO_LOG IDs, experiment links, transcript references]

  open_questions:
    - "[Unresolved tension 1]"
    - "[Unresolved tension 2]"
```

**Deliberation Narrative:**

[Story of how this metric was determined - to be filled during Grok integration]

**1. Prompt Stack:** [Exact questions/prompts used]

**2. Counterweight Table:** [Claim vs counterclaim with resolution]

**3. Edge Case Ledger:** [Numbered edge cases with keeper outcomes]

**4. Mythology Capsule:** [Shaman paragraph connecting axiom to outcome]

**5. Decision Stamp:** [Timestamp, participants, confidence, session ID]

**Why This Confidence:**

[Summary]

---

## Lifecycle Hooks

Profile-specific guidance for Trinity Architecture hooks.

### Bootstrap Hook

```yaml
hook:
  name: "bootstrap"
  trigger: "New auditor or new machine initializing with this profile"
  actions:
    - "Ensure declared axiom is clearly stated"
    - "Verify all metric categories have structure (even if placeholder values)"
    - "Check justification fields are present for each metric"
    - "Validate philosophical foundations section is complete"
  keeper_role: "Verify profile structure integrity"
  logger_role: "Log profile initialization"
  shaman_role: "Ensure axiom-to-metric reasoning is clear"
```

**Narrative:**

When bootstrapping with [profile name], the auditor must first understand the declared axiom and how it shapes all downstream metrics. The Keeper ensures structural integrity, the Logger records the bootstrap event, and the Shaman verifies that the mythology layer (philosophical foundations) properly informs the mechanism (metrics).

---

### Audit Hook

```yaml
hook:
  name: "audit"
  trigger: "Profile review, metric update, or cross-profile comparison"
  actions:
    - "Validate metrics against declared axiom (no drift)"
    - "Check justification fields for internal consistency"
    - "Review deliberation narratives for completeness"
    - "Verify comparison_notes are accurate across profiles"
  keeper_role: "Audit structural and logical consistency"
  logger_role: "Document audit findings and changes"
  shaman_role: "Verify mythology (why) still aligns with mechanism (what)"
```

**Narrative:**

Audit hooks ensure the profile maintains internal consistency over time. As metrics are updated or refined, the justification fields and deliberation narratives must evolve to match. The Shaman watches for drift between the stated philosophical foundations and the actual metric values.

---

### Incident Hook

```yaml
hook:
  name: "incident"
  trigger: "Metric inconsistency, axiom drift, or contested value discovered"
  actions:
    - "Identify which metric or justification is problematic"
    - "Trace reasoning from axiom to metric to find break point"
    - "Document the incident in deliberation narrative"
    - "Propose correction or refinement"
  keeper_role: "Restore integrity by fixing inconsistency"
  logger_role: "Log incident details and resolution"
  shaman_role: "Re-establish axiom-to-metric connection"
```

**Narrative:**

When a metric value or justification is challenged, the incident hook provides a structured response. Rather than silently updating values, we document WHY the challenge arose and HOW it was resolved. This becomes part of the deliberation narrative, enriching institutional memory.

---

### Release Hook

```yaml
hook:
  name: "release"
  trigger: "Profile promoted from DRAFT to CANONICAL status"
  actions:
    - "Final Keeper pass: all structures valid"
    - "Final Shaman pass: all narratives complete"
    - "Logger creates release entry in REPO_LOG"
    - "Version number incremented"
    - "Status changed from DRAFT to CANONICAL"
  keeper_role: "Final integrity check before release"
  logger_role: "Document release in REPO_LOG with full context"
  shaman_role: "Bless the profile as mythology-complete"
```

**Narrative:**

Release is the moment a profile transitions from iterative development to canonical reference. All three Trinity roles perform final checks. The Keeper ensures structure, the Logger preserves the moment in history, and the Shaman blesses the mythology layer as complete and aligned.

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
  shaman_role: "Watch for mythology drift during value assignment"
```

**Narrative:**

The Deliberation Hook marks the critical moment when philosophical reasoning converts to metric values. When engaging Grok or conducting multi-model debates to determine "why this number," this hook ensures the reasoning process is captured completely. The Keeper freezes edits to prevent mid-deliberation changes, the Logger preserves the entire deliberation trail (prompts, debates, edge cases), and the Shaman monitors whether the mythology layer (declared axiom and principles) stays grounded throughout the process. This hook is what makes metrics defensible - it preserves the "laborious effort" that justifies trust in the values.

---

### Comparative Audit Hook

```yaml
hook:
  name: "comparative_audit"
  trigger: "Metric adjustment prompted by another worldview profile moving"
  actions:
    - "Run diff between this profile and the updated profile"
    - "Refresh comparison_notes fields to reflect new divergences"
    - "Log rationale for synchronized deltas (if any)"
    - "Check for ripple effects on other metrics in this profile"
    - "Update deliberation narratives with new cross-profile insights"
  keeper_role: "Ensure consistency across profile ecosystem"
  logger_role: "Document why and how profiles evolved together or apart"
  shaman_role: "Verify comparative mythology remains sound"
```

**Narrative:**

Worldview profiles don't exist in isolation - they're part of a comparative framework. When one profile's metrics change (e.g., Classical Theism refines its suffering_weight), other profiles may need to adjust their comparison_notes to maintain accurate cross-references. The Comparative Audit Hook ensures these ripple effects are intentional and documented. The Keeper checks for structural consistency across profiles, the Logger documents the rationale for synchronized or divergent changes, and the Shaman ensures the comparative mythology (why worldviews differ on this dimension) remains coherent. This hook prevents silent drift between profiles and preserves the integrity of the CFA comparison framework.

---

## Changelog

- **v0.2.0** (2025-11-09): Major expansion per Nova Entry 2 (C4 implementation) + Nova Entry 4 fixes
  - 2 new hooks added (Deliberation, Comparative Audit)
  - 3 new justification fields added to all metrics (methodological_notes, evidence_threads, open_questions)
  - 5-part deliberation narrative scaffold mandated (Prompt Stack, Counterweight Table, Edge Case Ledger, Mythology Capsule, Decision Stamp)
  - All existing metrics updated with new structure
  - **3 new category sections added** (Anthropological, Cosmological, Eschatological) with 9 placeholder metrics (Nova Entry 4 fix)
  - Header metadata bumped to v0.2.0 (Nova Entry 4 fix)
  - Template now includes all 7 metric categories with 14 total metrics

- **v0.1.0** (2025-11-09): Initial skeleton created during Profile Architecture Foundation (C4)
  - Structure defined with hybrid YAML + narrative approach
  - Placeholder metrics with justification framework
  - 4 Trinity lifecycle hooks specified (Bootstrap, Audit, Incident, Release)
  - 4 metric categories established (Suffering, Epistemology, Morality, Teleology)

---

## Notes for Future Development

**Phase 3 Backfill Checklist:**
- [ ] Conduct Grok deliberation session for each metric
- [ ] Fill deliberation narratives with actual debates and edge cases
- [ ] Replace placeholder values with agreed-upon numbers
- [ ] Complete "Why This Number/Value" summaries
- [ ] Add comparison_notes by reviewing other profiles
- [ ] Document Grok session ID in metadata

**Cross-Profile Consistency:**
- [ ] Ensure metric definitions match across all profiles (same name = same meaning)
- [ ] Verify comparison_notes are reciprocal (if CT mentions MdN, MdN should mention CT)
- [ ] Check that contestable_points identify genuine disagreement areas
- [ ] Validate that lifecycle hooks work consistently across profiles

**Quality Gates:**
- [ ] Keeper audit: Structure and logical consistency
- [ ] Shaman review: Mythology (foundations) aligns with mechanism (metrics)
- [ ] Logger verification: All changes documented with rationale
- [ ] Ziggy approval: Philosophical rigor is transparent and defensible

---

**Template Version:** 1.0
**Created:** 2025-11-09 by C4
**Purpose:** Base template for all CFA worldview profiles
**Usage:** Copy this template to create new profiles, customizing all bracketed sections

