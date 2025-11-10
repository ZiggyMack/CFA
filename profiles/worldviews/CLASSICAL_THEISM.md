# Classical Theism Profile

**Status:** DRAFT | **Version:** 0.1.0 | **Date:** 2025-11-09

<!---
FILE: worldviews/CLASSICAL_THEISM.md
PURPOSE: Worldview profile for Classical Theism with metrics, philosophical foundations, and deliberation narratives
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
  name: "Classical Theism"
  version: "0.1.0"
  status: "DRAFT"
  declared_axiom: "God exists as a necessary, perfect being who created and sustains the universe, and has revealed Himself through reason and special revelation"
  alternate_names: ["Traditional Theism", "Anselmian Theism", "Perfect Being Theology"]
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

      - name: "Logos/intelligibility"
        description: "Claims God's rationality grounds cosmic order and comprehensibility"

      - name: "Revelation reliability"
        description: "Assumes Scripture/tradition reliably communicates divine truth"

      - name: "Moral realism"
        description: "Claims objective moral facts exist, grounded in God's nature"

      - name: "Teleology"
        description: "Posits purpose and design as fundamental features of reality"

      - name: "PSR (Principle of Sufficient Reason)"
        description: "Everything has an explanation (in God)"

      - name: "Imago Dei"
        description: "Claims humans bear God's image, enabling knowledge and moral agency"

  debts:
    count: 4
    list:
      - name: "Divine hiddenness"
        description: "Why doesn't God make existence more evident?"

      - name: "Problem of evil"
        description: "How does omnipotent/benevolent God permit suffering?"

      - name: "Hermeneutic variance"
        description: "Why do interpretations of revelation differ?"

      - name: "Beauty→truth bridge"
        description: "Does aesthetic resonance actually track truth?"

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

Classical Theism begins with the axiom that God exists as a necessary being possessing all perfections (omniscience, omnipotence, omnibenevolence, immutability, simplicity, eternality). This God is the creator ex nihilo and sustainer of all contingent reality, and has made Himself known through both natural revelation (reason, creation) and special revelation (scripture, incarnation).

### Philosophical Framework

Classical Theism operates within the tradition of medieval scholasticism, particularly drawing from Anselm, Aquinas, and Maimonides, while maintaining roots in Augustinian Platonism and Aristotelian metaphysics. The framework emphasizes divine transcendence while maintaining divine immanence through providence and incarnation.

Core commitments include: the via negativa (knowing God through what He is not), analogical predication (speaking of God analogically rather than univocally or equivocally), and the doctrine of divine simplicity (God's essence and existence are identical). These commitments shape how Classical Theism approaches epistemology (faith seeking understanding), morality (divine command grounded in God's nature), teleology (created purposes ordered toward God), and anthropology (humans as imago Dei).

What distinguishes Classical Theism from other profiles is its commitment to God's aseity (self-existence), immutability, and timelessness, which contrasts with open theism, process theology, and naturalistic worldviews. It maintains that God is both utterly transcendent (wholly other) and yet personally involved in creation through providence, miracles, and incarnation.

### Key Principles

1. **Divine Perfection:** God possesses all perfections maximally and essentially - omniscience, omnipotence, perfect goodness, immutability, eternality, and simplicity are not contingent attributes but necessary features of God's nature.

2. **Creatio Ex Nihilo:** God created the universe from nothing by divine fiat, establishing contingent reality's complete dependence on necessary being. This grounds the distinction between Creator and creation, rejecting pantheism and panentheism.

3. **Imago Dei Anthropology:** Humans are created in God's image, possessing rationality, moral agency, and relationality, but are fallen through sin and require redemption through divine grace. This shapes views on human dignity, freedom, and ultimate destiny.

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
  keeper_role: "Ensure consistency across profile ecosystem"
  logger_role: "Document why and how profiles evolved together or apart"
  shaman_role: "Verify comparative mythology remains sound"
```

**Narrative:**
When Methodological Naturalism or another profile's metrics change, Classical Theism may need to adjust comparison_notes to maintain accurate cross-references. The Comparative Audit Hook ensures these ripple effects are intentional and documented. The Keeper checks for structural consistency, the Logger documents the rationale for changes, and the Shaman ensures the comparative theology remains coherent.

---

## Changelog

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
- Keeper/Logger/Shaman audits pass
- Ziggy approval for philosophical rigor and transparency

---

**Profile Version:** 0.1.0
**Created:** 2025-11-09 by C4
**Purpose:** Classical Theism worldview profile for CFA framework
**Usage:** Production-ready after Phase 3 Grok integration completes metric deliberations
