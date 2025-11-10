# CFA Worldview Profiles

**Purpose:** This directory contains worldview profiles for the Comparative Foundational Analysis (CFA) framework. Each profile represents a distinct philosophical/religious worldview with metrics, foundational commitments, and deliberation narratives that enable systematic comparison.

**Status:** Phase 3 - Production profiles deployed, awaiting Grok integration for metric determination

---

## Directory Structure

```
profiles/
├── _docs/                          # Supporting documentation
│   ├── METRIC_TAXONOMY.md         # Canonical metric definitions
│   └── PROFILE_TEMPLATE.md        # Template for new profiles
├── worldviews/                     # All worldview profiles
│   ├── [12 profiles listed below]
├── use_cases/                      # Example use cases
│   └── NOVA_USE_CASE_METRIC_POLLING_SUFFERING.md
└── README.md                       # This file
```

---

## Profile Index

### Production Profiles (Phase 3 - Complete Scaffolding)

**[Classical Theism](worldviews/CLASSICAL_THEISM.md)** - v0.2.0 (DRAFT)
- **Axiom:** God exists as necessary perfect being who created and sustains the universe
- **Tradition:** Medieval scholasticism (Anselm, Aquinas, Maimonides)
- **Key Commitments:** Divine perfection, creatio ex nihilo, imago Dei anthropology
- **Status:** Full structure with ToC, Steel-Manning Guide, 1 detailed metric (suffering_weight), all hooks implemented

**[Methodological Naturalism](worldviews/METHODOLOGICAL_NATURALISM.md)** - v0.2.0 (DRAFT)
- **Axiom:** Natural world operates by discoverable laws; knowledge requires empirical evidence
- **Tradition:** Scientific empiricism, logical positivism, naturalized epistemology
- **Key Commitments:** Empirical evidentialism, causal closure, methodological parsimony
- **Status:** Full structure with ToC, Steel-Manning Guide, 1 detailed metric (suffering_weight), all hooks implemented

### Priority Queue Profiles (Phase 3 - Scaffolded)

Per Ziggy Entry 2.5 (B-STORM_3.md), next priority for Phase 4 Grok deliberation:

**1. [Orthodox Judaism](worldviews/ORTHODOX_JUDAISM.md)** - v0.2.0 (DRAFT)
- **Axiom:** God revealed Torah at Sinai; halakha is binding and authoritative
- **Status:** Scaffolded with ToC and Steel-Manning Guide - foundations complete, metrics ready for Grok

**2. [Mormonism (LDS)](worldviews/MORMONISM.md)** - v0.2.0 (DRAFT)
- **Axiom:** Continuing revelation through prophets; humans have potential for divine progression
- **Status:** Scaffolded with ToC and Steel-Manning Guide - foundations complete, metrics ready for Grok

**3. [Error Theory](worldviews/ERROR_THEORY.md)** - v0.2.0 (DRAFT)
- **Axiom:** All positive moral claims are false; moral properties do not exist
- **Status:** Scaffolded with ToC and Steel-Manning Guide - foundations complete, metrics ready for Grok

**4. [Null Hypothesis](worldviews/NULL_HYPOTHESIS.md)** - v0.2.0 (DRAFT)
- **Axiom:** Suspend judgment on claims lacking sufficient evidence; epistemic minimalism
- **Status:** Scaffolded with ToC and Steel-Manning Guide - foundations complete, metrics ready for Grok

**5. [Desiderata Believers](worldviews/DESIDERATA_BELIEVERS.md)** - v0.2.0 (DRAFT)
- **Axiom:** Adopt beliefs that promote flourishing; pragmatic value justifies belief
- **Status:** Scaffolded with ToC and Steel-Manning Guide - foundations complete, metrics ready for Grok

### Additional Worldview Profiles (Phase 3 - Scaffolded)

**[Buddhism](worldviews/BUDDHISM.md)** - v0.2.0 (DRAFT)
- **Axiom:** Suffering is universal; liberation achieved through Eightfold Path
- **Status:** Scaffolded with ToC and Steel-Manning Guide - foundations complete, metrics ready for Grok

**[Islam](worldviews/ISLAM.md)** - v0.2.0 (DRAFT)
- **Axiom:** There is no god but Allah; Muhammad is His messenger; Quran is final revelation
- **Status:** Scaffolded with ToC and Steel-Manning Guide - foundations complete, metrics ready for Grok

**[Hinduism](worldviews/HINDUISM.md)** - v0.2.0 (DRAFT)
- **Axiom:** Brahman is ultimate reality; atman-Brahman identity; moksha is liberation
- **Status:** Scaffolded with ToC and Steel-Manning Guide - foundations complete, metrics ready for Grok

**[Process Theology](worldviews/PROCESS_THEOLOGY.md)** - v0.2.0 (DRAFT)
- **Axiom:** God is dipolar; divine power is persuasive not coercive; panentheism
- **Status:** Scaffolded with ToC and Steel-Manning Guide - foundations complete, metrics ready for Grok

**[Existentialism](worldviews/EXISTENTIALISM.md)** - v0.2.0 (DRAFT)
- **Axiom:** Existence precedes essence; radical freedom creates meaning in absurd universe
- **Status:** Scaffolded with ToC and Steel-Manning Guide - foundations complete, metrics ready for Grok

### Future Profiles (Planned)

Additional worldviews for comprehensive coverage: Confucianism, Stoicism, Open Theism, Sikhism, Jainism, Taoism, Secular Humanism, Transhumanism, and others as needed for worldview comparison framework.

---

## Profile Structure

Each profile follows the validated template structure (see [_docs/PROFILE_TEMPLATE.md](_docs/PROFILE_TEMPLATE.md)):

### Components

1. **Metadata** - Version, status, declared axiom, maintainers
2. **Philosophical Foundations** - Axiom, framework, key principles
3. **Metrics** (14 total across 7 categories):
   - Suffering Analysis (suffering_weight)
   - Epistemological Commitments (revelation_weight, rational_confidence)
   - Moral Foundations (moral_source)
   - Teleological Commitments (purpose_framework)
   - Anthropological Commitments (human_nature_baseline, agency_alignment, consciousness_ontology)
   - Cosmological Commitments (origin_claim, causal_structure, fine_tuning_account)
   - Eschatological Commitments (judgment_framework, ultimate_destiny, eschatology_confidence)
4. **Lifecycle Hooks** (6 total) - Bootstrap, Audit, Incident, Release, Deliberation, Comparative Audit
5. **Changelog** - Version history

### Metric Justification Framework (8 fields per metric)

Each metric includes comprehensive justification:
- `axiom_connection` - How declared axiom informs this metric
- `reasoning_process` - Step-by-step reasoning
- `assumptions` - Baked-in assumptions
- `contestable_points` - Where reasonable disagreement exists
- `comparison_notes` - Cross-references to other profiles
- `methodological_notes` - Deliberation modality, tools used
- `evidence_threads` - REPO_LOG IDs, transcripts, references
- `open_questions` - Unresolved tensions

### Deliberation Narrative (5-part scaffold)

Each metric includes structured deliberation capture:
1. **Prompt Stack** - Exact questions/prompts used
2. **Counterweight Table** - Claim vs counterclaim with resolutions
3. **Edge Case Ledger** - Numbered edge cases with keeper outcomes
4. **Mythology Capsule** - Shaman paragraph connecting axiom to outcome
5. **Decision Stamp** - Timestamp, participants, confidence, session ID, references

---

## Steel-Manning Guide (B-STORM_4 Addition)

**Purpose:** Enable adversarial auditing where AI auditors can advocate for or challenge worldviews with full bias transparency.

**Location:** Embedded in each worldview profile between Philosophical Foundations and Metrics sections

**Structure:**
- **Overview** - Purpose, current auditor assignments, dynamic assignment note
- **PRO Stance Section** - Mission, what to emphasize, what to acknowledge, scoring calibration (YAML), auditor lens calibration, success criteria
- **ANTI Stance Section** - Mission, what to emphasize, what to acknowledge, scoring calibration (YAML), auditor lens calibration, success criteria
- **Adversarial Balance** - Why this auditor pairing works, risks of each stance, fairness check role, 98% convergence target

### Key Innovation: Unified Architecture

**Before B-STORM_4:**
- Worldview profiles = User-facing transparency only
- Auditor calibration = Separate axiom files per auditor per worldview (36+ files needed)

**After B-STORM_4:**
- Worldview profiles = BOTH user transparency AND auditor calibration
- Steel-Manning Guide = Worldview-agnostic PRO/ANTI stance guidance
- Auditor assignments = Dynamic mapping via [../auditors/AUDITOR_ASSIGNMENTS.md](../auditors/AUDITOR_ASSIGNMENTS.md)
- File count = 50% reduction (12 profiles + 1 assignments file vs 24+ separate files)

### Scoring Calibration (Bias Transparency)

Each stance includes YAML bias adjustment values:

```yaml
pro_worldview_bias_adjustment:
  axiom_confidence: 0.85      # Trust in core axioms (0.0-1.0)
  burden_of_proof: 0.40       # Where to place evidential burden (low=on critics, high=on worldview)
  charity_interpretation: 0.90 # How favorably to interpret ambiguity (0.0-1.0)
  edge_case_weight: 0.30      # Weight of counterexamples (low=exceptions, high=refutations)
  explanatory_credit: 0.85    # Credit for addressing questions (0.0-1.0)
  historical_weight: 0.75     # Weight of historical/cultural staying power (0.0-1.0)
  lived_experience: 0.80      # Weight of transformative capacity (0.0-1.0)
```

**PRO stance:** Values calibrated for honest advocacy (high confidence, charitable interpretation)
**ANTI stance:** Values calibrated for honest opposition (low confidence, skeptical interpretation)

### Auditor Assignment Principles

**Natural Lens Alignment:** Play auditors to their strengths
- **Claude (Teleological)** - PRO on theistic traditions (purpose-driven), ANTI on naturalistic (challenges reductionism)
- **Grok (Empirical)** - PRO on naturalistic (evidence-based), ANTI on theistic (challenges non-empirical claims)
- **Nova (Symmetry)** - Fairness check across all pairings (catches hidden asymmetries)

**Current Assignments:** See [../auditors/AUDITOR_ASSIGNMENTS.md](../auditors/AUDITOR_ASSIGNMENTS.md)

### Usage for Auditors

**Step 1:** Consult [AUDITOR_ASSIGNMENTS.md](../auditors/AUDITOR_ASSIGNMENTS.md) to identify your stance (PRO, ANTI, or Fairness)

**Step 2:** Navigate to your assigned stance section in worldview profile (use ToC quick links)

**Step 3:** Read mission, emphasis points, acknowledgment requirements

**Step 4:** Apply bias adjustment values from YAML block to your scoring lens

**Step 5:** Score independently, disclose bias, provide rationale

**Step 6:** Deliberate with other auditors until 98% convergence

### Table of Contents Enhancement

All profiles now include ToC with:
- **Core Sections** - Line number references for raw file navigation
- **Quick Links** - Markdown anchors for IDE clickability
- **Auditor Jumps** - Direct links to PRO/ANTI stance sections (e.g., L221, L295)

**Example from CLASSICAL_THEISM.md:**
```markdown
**Quick Links:**
- 🎯 **Auditors:** [PRO Stance](#pro-classical-theism-stance) (L221) | [ANTI Stance](#anti-classical-theism-stance) (L295)
- 👥 **Users:** [What is CT?](#philosophical-foundations) (L167) | [Axioms & Debts](#mr-brutes-ledger) (L95)
```

### Process Integration

**Process Claude (Domain 7) Monitors:**
- Changes to Steel-Manning Guide sections
- Bias adjustment value changes (±0.1 triggers review)
- Auditor assignment swaps
- Profile content changes that impact calibration

**See:** [../docs/repository/librarian_tools/ROLE_PROCESS.md](../docs/repository/librarian_tools/ROLE_PROCESS.md) (Domain 7: Worldview Profile Monitoring)

### Automation

**Script:** [../utils/update_worldview_profiles.py](../utils/update_worldview_profiles.py)

**Purpose:** Bulk updates to profile structure (ToC, Steel-Manning Guide)

**Usage:**
```bash
cd d:/Documents/CFA && python utils/update_worldview_profiles.py
```

**Pattern:**
1. Reads profile template structure
2. Generates ToC with line number placeholders
3. Generates Steel-Manning Guide with worldview-agnostic stance guidance
4. Inserts via regex (preserves unique content, standardizes structure)
5. Updates version metadata

**Why script exists:** 12 profiles × manual updates = 2-3 hours, error-prone. Script = 30 seconds, consistent.

---

## Development Workflow

### Phase 3: Foundation & Production Deployment (Current)

**Status:** Complete ✅
- Profile template validated (KD-C6, Nova Entry 8)
- Metric taxonomy approved (KD-C5, Nova Entry 4)
- Classical Theism & Methodological Naturalism profiles deployed
- All profiles scaffolded with placeholder metrics

**Next:** Phase 4 - Grok integration for metric determination

### Phase 4: Grok Integration & Metric Determination (Upcoming)

**Goal:** Populate all 14 metrics with Grok-determined values through philosophical deliberation

**Process:**
1. Launch Grok deliberation session for each metric
2. Use 5-part deliberation scaffold to capture reasoning
3. Document all prompts, debates, edge cases in deliberation narrative
4. Assign metric values based on philosophical consensus
5. Update profile versions as metrics complete

**Quality Gates:**
- All deliberation narratives complete
- All comparison_notes reference live profiles
- Keeper/Logger/Shaman audits pass
- Ziggy approval for philosophical rigor

### Phase 5: Expansion & Maintenance (Future)

**Goal:** Add priority worldviews, maintain existing profiles, respond to comparative audits

**Activities:**
- Deploy profiles for Orthodox Judaism, Mormonism, Error Theory, Null Hypothesis, Desiderata
- Comparative audit hook triggers when profiles evolve
- Regular audit hooks ensure no drift from canonical taxonomy
- Version updates track all changes

---

## Using Profiles

### For Developers

```python
# Example: Loading a profile for CFA analysis
from utils.profile_loader import load_profile

ct_profile = load_profile("CLASSICAL_THEISM")
mdn_profile = load_profile("METHODOLOGICAL_NATURALISM")

# Access metrics
suffering_weight_ct = ct_profile.metrics.suffering_weight.value
suffering_weight_mdn = mdn_profile.metrics.suffering_weight.value

# Compare worldviews
delta = suffering_weight_mdn - suffering_weight_ct
print(f"MdN weights suffering {delta} points higher than CT")
```

### For Philosophers/Theologians

Profiles are designed for human readability:
1. Read `Philosophical Foundations` to understand axiom/principles
2. Review `Metrics` to see how foundations translate to values
3. Examine `Deliberation Narratives` to see reasoning process
4. Check `comparison_notes` to understand cross-profile differences
5. Review `open_questions` to identify areas needing further deliberation

---

## Trinity Architecture Integration

All profiles integrate with Trinity Architecture hooks:

- **Keeper** - Guards structural integrity, prevents drift from taxonomy
- **Logger** - Preserves all changes, deliberations, incidents for traceability
- **Shaman** - Ensures mythology (axiom/principles) grounds all mechanisms (metrics)

See [../docs/architecture/README.md](../docs/architecture/README.md) for Trinity Architecture details.

---

## Contributing

### Adding New Profiles

1. Copy [_docs/PROFILE_TEMPLATE.md](_docs/PROFILE_TEMPLATE.md)
2. Create new file in `worldviews/[WORLDVIEW_NAME].md` (use SCREAMING_SNAKE_CASE)
3. Fill in Metadata, Philosophical Foundations, Key Principles
4. Scaffold all 14 metrics with justification framework (keep placeholder values)
5. Implement all 6 lifecycle hooks with worldview-specific guidance
6. Update DEPENDS_ON to point to `../_docs/METRIC_TAXONOMY.md`
7. Submit for Nova validation before Grok deliberation

### Updating Existing Profiles

1. Check that changes align with canonical [METRIC_TAXONOMY.md](_docs/METRIC_TAXONOMY.md)
2. Document all changes in profile's Changelog
3. Trigger Comparative Audit hook if changes affect cross-profile comparisons
4. Update version number (semantic versioning: major.minor.patch)
5. Log changes in REPO_LOG.md

---

## Dependencies

- **[METRIC_TAXONOMY.md](_docs/METRIC_TAXONOMY.md)** - Canonical definitions for all metrics
- **[PROFILE_TEMPLATE.md](_docs/PROFILE_TEMPLATE.md)** - Template structure for all profiles
- **Trinity Architecture** - Keeper/Logger/Shaman hook system
- **REPO_LOG.md** - Change history and deliberation references
- **B-STORM files** - Collaboration and validation workflow

---

## Status & Roadmap

**Current Phase:** Phase 3 Complete - Foundation validated, production profiles deployed

**Next Milestone:** Phase 4 - Grok integration for CT/MdN metric determination

**Long-term Vision:** Comprehensive worldview comparison framework with 10+ profiles covering major philosophical/religious traditions

---

**Documentation Version:** 1.0
**Last Updated:** 2025-11-09 by C4
**Contact:** See [../README.md](../README.md) for project information
