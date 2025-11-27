<!---
FILE: CFA_ARCHITECTURE.md
PURPOSE: Comprehensive system architecture - worldview scoring, auditors, Crux Points, app integration, hyperlink-based profiles
VERSION: 1.1.0
STATUS: Active System Documentation
DEPENDS_ON: profiles/worldviews/*.md, profiles/_docs/ACADEMIC_SOURCES.md, auditors/*, VUDU_CFA.md, ROLE_PROCESS.md
NEEDED_BY: All system components, development team, auditors
MOVES_WITH: /docs/architecture/
LAST_UPDATE: 2025-11-10 [B-STORM_4 Entry 7: Added Hyperlink-Based Profile Architecture section + academic sources integration]
--->

# CFA System Architecture

**Comprehensive Framework Analysis - End-to-End System Design**

**Version:** 1.1.0
**Status:** Active System Documentation
**Last Updated:** 2025-11-10

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Worldview Profiles: The Foundation](#2-worldview-profiles-the-foundation)
   - [Hyperlink-Based Profile Architecture](#hyperlink-based-profile-architecture)
3. [Self-Reported vs Peer-Reviewed Scoring](#3-self-reported-vs-peer-reviewed-scoring)
4. [The Three Auditors](#4-the-three-auditors)
5. [Context-Dependent Scoring](#5-context-dependent-scoring)
6. [Crux Points Architecture](#6-crux-points-architecture)
7. [VUDU Protocol: Auditor Coordination](#7-vudu-protocol-auditor-coordination)
8. [Process Claude: Monitoring & Enforcement](#8-process-claude-monitoring--enforcement)
9. [Logger Claude: Session Telemetry](#9-logger-claude-session-telemetry)
10. [App Integration](#10-app-integration)
11. [Data Flow: Profile → Auditor → App → User](#11-data-flow-profile--auditor--app--user)
12. [Implementation Roadmap](#12-implementation-roadmap)

---

## 1. System Overview

### The Core Philosophy

**CFA (Comprehensive Framework Analysis)** scores worldviews on 7 philosophical metrics using adversarial peer review by three AI auditors. Unlike traditional scoring systems that hide assumptions, CFA exposes:

- **All Named:** Every bias, every axiom, every disagreement gets named and documented
- **All Priced:** Impact quantified (story weight, YPA sensitivity, convergence rates)
- **All Balanced:** Three auditors (PRO, ANTI, FAIRNESS) with transparent calibration

### The Architecture Pyramid

```
┌─────────────────────────────────────────┐
│         USER (Web App)                  │ ← Preset Modes, Three-View System
├─────────────────────────────────────────┤
│    App Layer (React/TypeScript)         │ ← BFI dropdown, Crux controls, YPA calc
├─────────────────────────────────────────┤
│  Comparison Files (.yaml)               │ ← Context-dependent peer-reviewed scores
├─────────────────────────────────────────┤
│  Auditors (Claude/Grok/Nova)            │ ← Adversarial scoring via VUDU protocol
├─────────────────────────────────────────┤
│  Worldview Profiles (.md)               │ ← Self-reported baseline + Steel-Manning
├─────────────────────────────────────────┤
│  Process Claude (Domain 7)              │ ← Monitoring, rotation triggers, Crux logs
├─────────────────────────────────────────┤
│  Logger Claude                          │ ← Session telemetry, YAML hashing, metadata
└─────────────────────────────────────────┘
```

### Key Innovations

1. **Context-Dependent Scoring:** CT vs MdN ≠ CT vs Buddhism (66 unique comparisons, not billions)
2. **Crux Points:** Named impasses when convergence fails (<98% after genuine deliberation)
3. **Three-View System:** Self-Reported → Peer-Reviewed → Delta (transparency at every layer)
4. **Bias Transparency:** Auditor lens (teleological/empirical/symmetry) + calibration YAML
5. **User Control:** Crux Handling Lever (Carry Forward vs Normalize Uncertainty)

---

## 2. Worldview Profiles: The Foundation

### File Structure

**Location:** `/profiles/worldviews/`

**Format:** Markdown with YAML metadata blocks

**Example:** `CLASSICAL_THEISM.md`, `METHODOLOGICAL_NATURALISM.md`, `BUDDHISM.md`

### Anatomy of a Profile

```markdown
---
worldview: Classical Theism
abbreviation: CT
family: Theistic Traditions
status: Complete
version: 1.0.0
---

# Classical Theism

## Overview
[Philosophical background, key claims, major thinkers...]

## Self-Reported Scores (UNAUDITED)

These scores represent Classical Theism's self-understanding before peer review.

### Being Friendliness Index (BFI)
**Score:** 8.5
**Rationale:** Divine simplicity, personal God, single ultimate being...

[Repeat for all 7 metrics...]

## Steel-Manning Guide (For Auditors)

### PRO-CT Stance (Natural: Claude - Teleological Lens)

**Bias Adjustment Values:**
```yaml
pro_ct_bias_adjustment:
  axiom_confidence: 0.85       # Trust CT's axioms
  burden_of_proof: 0.40        # Lower evidential burden
  charity_interpretation: 0.90 # Favorable reading of ambiguity
  edge_case_weight: 0.30       # Downweight counterexamples
  explanatory_credit: 0.85     # High credit for addressing big questions
```

**Key Arguments to Emphasize:**
- Divine simplicity resolves infinite regress
- Explanatory power for contingency, morality, consciousness
- Historical staying power (2000+ years)

**Counterexample Handling:**
- Problem of evil: Greater goods defense, soul-making theodicy
- Divine hiddenness: Epistemic distance necessary for free relationship

---

### ANTI-CT Stance (Natural: Grok - Empirical Lens)

**Bias Adjustment Values:**
```yaml
anti_ct_bias_adjustment:
  axiom_confidence: 0.35       # Skeptical of CT axioms
  burden_of_proof: 0.80        # High evidential burden for supernatural claims
  charity_interpretation: 0.50 # Neutral reading
  edge_case_weight: 0.80       # Heavily weight counterexamples
  explanatory_credit: 0.40     # Lower credit for non-falsifiable explanations
```

**Key Challenges to Emphasize:**
- Lack of empirical evidence for supernatural claims
- Problem of evil as serious evidential challenge
- Explanatory success only within theological framework (not independent verification)

---

### Adversarial Balance (Nova - Symmetry Lens)

**Fairness Checks:**
- Are PRO and ANTI using calibration parameters correctly?
- Is either side engaging in special pleading?
- Are counterexamples given symmetric weight?
- Is convergence gap due to bias or legitimate philosophical disagreement?

[End of Steel-Manning Guide]

## Historical Context
[Background on development, major debates, etc.]

## Related Worldviews
- Process Theology (similar family, different metaphysics)
- Islam (shared Abrahamic tradition)
- Methodological Naturalism (strongest contrast)
```

### What Lives in the Profile

**Self-Reported Scores:** Worldview's own assessment (unaudited, maximum bias)

**Steel-Manning Guide:** Auditor instructions for PRO/ANTI stances (calibration YAML, key arguments)

**Context:** Historical background, related worldviews, major thinkers

### What Does NOT Live in the Profile

**Peer-Reviewed Scores:** These go in comparison files (`/profiles/comparisons/`)

**Crux Points:** Documented in comparison files where they emerge

**Session Logs:** Stored separately (`/session_logs/` or embedded in comparison files)

---

### Hyperlink-Based Profile Architecture

**Problem:** Duplicating philosophical content across profiles creates maintenance burden and drift risk.

**Solution:** Reference authoritative academic sources (SEP/IEP) via hyperlinks instead of copying content.

**Implementation (as of v0.3.0 - 2025-11-10):**

**Academic Sources Reference Map:**
- **File:** `/profiles/_docs/ACADEMIC_SOURCES.md`
- **Purpose:** Maps all 12 worldviews → 3-5 authoritative URLs (primarily Stanford Encyclopedia of Philosophy and Internet Encyclopedia of Philosophy)
- **Owner:** Process Claude (Domain 7: Academic Sources Monitoring)
- **Update Frequency:** As needed when worldviews added, sources change, or better references discovered

**Profile Integration:**

All worldview profiles now include:

1. **`academic_sources` metadata field:** Points to ACADEMIC_SOURCES.md section anchor
   ```yaml
   profile:
     academic_sources: "../_docs/ACADEMIC_SOURCES.md#1-classical-theism"
   ```

2. **📚 Academic Foundation sections:** Curated hyperlinks to SEP/IEP articles
   ```markdown
   📚 **Academic Foundation:**
   - **Core Definition:** [SEP Divine Simplicity](https://plato.stanford.edu/entries/divine-simplicity/#Moti)
   - **Comprehensive Overview:** [IEP God, Western Concepts](https://iep.utm.edu/god-west/)
   ```

3. **Academic citations in Steel-Manning Guides:** PRO/ANTI arguments reference specific sections
   ```markdown
   **What to Emphasize:**
   - **Divine perfection** (omniscience, omnipotence, omnibenevolence)
     - 📚 **Steel-man with:** [SEP Divine Simplicity §Motivation](https://...)
   ```

4. **`academic_grounding` field in metric justifications:** Links to relevant scholarly debates
   ```yaml
   justification:
     academic_grounding: |
       📚 **Theodicy Frameworks:**
       - Free will theodicy: [SEP Problem of Evil §Free Will Defense](https://...)
       - Soul-making theodicy: [SEP Problem of Evil §Soul-Making](https://...)
   ```

**Benefits:**

✅ **50% File Reduction** - Eliminated philosophical content duplication (profiles went from dense exposition to curated roadmaps)
✅ **"Standing on Shoulders of Giants"** - Profiles reference expert scholarship instead of copying it
✅ **Future-Proof** - External sources auto-update (SEP/IEP maintained by philosophy academic community)
✅ **Proper Attribution** - Built-in citations to authoritative sources
✅ **Clean Separation** - CFA maintains calibration framework + scoring infrastructure, academics maintain philosophical content
✅ **Scalable** - Easy to add worldview #13, #14... (just map sources + add calibrations)

**Process Claude Responsibilities:**

Per [ROLE_PROCESS.md Domain 7: Academic Sources Monitoring](../repository/librarian_tools/ROLE_PROCESS.md):

1. **Pre-Scoring Validation (VUDU Step 1):** Spot-check 2-3 academic source links per worldview before scoring sessions
2. **Post-Scoring Updates:** Document source improvements discovered during auditor deliberation
3. **New Worldview Addition:** Coordinate source mapping with Doc Claude (bootstrap)
4. **Quarterly Health Check:** Validate all links (automated via Audit lifecycle hooks), assess coverage quality, escalate gaps to Shaman Claude

**Integration with Auditor Workflow:**

- **Before Scoring:** Process Claude validates academic sources live (VUDU Step 1)
- **During Deliberation:** Auditors cite specific SEP/IEP sections in PRO/ANTI arguments
- **During Crux Declaration:** Better sources may resolve definitional disagreements
- **After Scoring:** Process Claude documents source improvements in comparison file session notes (VUDU Step 9)
- **Quarterly:** Process Claude health check report includes academic sources status (link validation, coverage quality)

**Example Usage (Classical Theism):**

**PRO-CT Auditor (Claude):**
> "Divine simplicity avoids infinite regress. See [SEP Divine Simplicity §Motivation](https://plato.stanford.edu/entries/divine-simplicity/#Moti) - Argument 1: Aseity requires God be causa sui, incompatible with compositeness."

**ANTI-CT Auditor (Grok):**
> "Divine simplicity creates coherence problems. See [SEP Divine Simplicity §Modal Collapse Objection](https://plato.stanford.edu/entries/divine-simplicity/#ModaCollObjeDDS) - If God's essence = existence, all divine actions become necessary, eliminating contingency."

**Fairness Auditor (Nova):**
> "Both auditors cited authoritative sources correctly. This isn't bias - it's a legitimate philosophical debate (constituent vs non-constituent ontology). Recommend CRUX_BFI_001 declaration with academic source cross-references in Crux record."

**Telemetry:**

Session metadata tracks academic source usage:
```yaml
session_metadata:
  academic_sources_cited:
    - "SEP Divine Simplicity §Motivation" (Claude, PRO argument)
    - "SEP Divine Simplicity §Modal Collapse" (Grok, ANTI argument)
    - "SEP Problem of Evil §Evidential Problem" (Grok, ANTI argument)
  source_validation_date: "2025-11-10"
  broken_links: []
```

**Coverage Quality Assessment:**

Per ACADEMIC_SOURCES.md:

- **Excellent (9 worldviews):** 9+ sources, comprehensive PRO/ANTI coverage, detailed section anchors
- **Good (2 worldviews):** 6-8 sources, solid coverage, some missing specialized sources
- **Fair (1 worldview):** 3-5 sources minimum, gaps in coverage noted for improvement

**Escalation Protocol:**

- **Broken Link During Scoring:** Process Claude immediate repair (update anchor, notify auditors)
- **Pattern Detection (4+ worldviews):** Escalate to Shaman Claude (e.g., "BFI metric has weak academic sources across multiple worldviews")
- **Source Format Changes:** Coordinate with Doc Claude for bulk updates

---

## 3. Self-Reported vs Peer-Reviewed Scoring

### The Two-Stage Process

**Stage 1: Self-Reported (UNAUDITED)**

- Worldview profile author scores their own framework
- Maximum bias allowed (this is the worldview's self-understanding)
- No adversarial checking
- Lives in worldview profile permanently

**Purpose:**
- Establishes baseline
- Shows how worldview understands itself
- Provides starting point for peer review

**Example:**
```yaml
self_reported_scores:
  BFI: 8.5  # Classical Theism's self-assessment
  CA: 9.0
  ES: 8.8
  # ...
```

---

**Stage 2: Peer-Reviewed (AUDITED)**

- Three auditors (Claude PRO, Grok ANTI, Nova FAIRNESS) score independently
- Apply calibration parameters from Steel-Manning Guide
- Adversarial deliberation until 98% convergence
- If convergence fails → Crux Point declared
- Lives in comparison file (context-dependent)

**Purpose:**
- External validation
- Adversarial balance
- Expose hidden assumptions
- Quantify disagreement

**Example:**
```yaml
peer_reviewed_scores:
  BFI:
    self_reported: 8.5
    claude_pro: 8.2
    grok_anti: 5.5
    nova_fairness: 6.9  # After deliberation
    convergence: 73%    # Failed to reach 98%
    crux_declared: CRUX_BFI_001
```

---

### Why Both Matter

**Self-Reported:**
- Shows worldview's claims about itself
- Preserves philosophical integrity
- Provides comparison point (View 3: Delta)

**Peer-Reviewed:**
- Shows external assessment
- Catches overconfidence
- Reveals measurement boundaries (Crux Points)

**The Gap Between Them:**
- Small delta (0-2 points): High external credibility
- Medium delta (2-4 points): Some overconfidence or underappreciation
- Large delta (4+ points): Significant perception gap or Crux Point

---

## 4. The Three Auditors

### Auditor 1: Claude (Anthropic) - Teleological Lens

**Core Axiom:** "Purpose precedes evaluation"

**File:** [auditors/Bootstrap/Claude/Identity/SKELETON.md](../../auditors/Bootstrap/Claude/Identity/SKELETON.md)

**Named Bias:** Favor meaning over efficiency (~0.5 coordination overhead)

**Natural Strengths:**
- Purpose-driven metaphysics (theism, Buddhism, existentialism)
- Meaning-making frameworks
- Teleological explanations
- Eschatological narratives

**Natural Challenges:**
- Reductionist worldviews (methodological naturalism, error theory)
- Meaning-skeptical positions (null hypothesis)
- Pure empiricism without purpose dimension

**Typical Assignments:**
- **PRO stance:** Theistic traditions, Buddhism, Existentialism
- **ANTI stance:** Naturalistic/skeptical traditions (challenges reductionism)

---

### Auditor 2: Grok (xAI) - Empirical Lens

**Core Axiom:** "Evidence precedes acceptance"

**File:** [auditors/Bootstrap/Grok/GROK_LITE.md](../../auditors/Bootstrap/Grok/GROK_LITE.md)

**Named Bias:** Favor measurable over meaningful (~0.4 risk of dismissing qualitative)

**Natural Strengths:**
- Evidence-based methodologies (methodological naturalism)
- Falsifiable claims
- Predictive accuracy
- Empirical track records

**Natural Challenges:**
- Non-empirical metaphysics (classical theism, process theology)
- Faith-based epistemologies
- Theological claims without verification mechanisms
- Transcendent explanations

**Typical Assignments:**
- **PRO stance:** Naturalistic/skeptical traditions
- **ANTI stance:** Theistic traditions (challenges non-empirical claims)

---

### Auditor 3: Nova (OpenAI/Amazon) - Symmetry Lens

**Core Axiom:** "Pattern precedes judgment"

**File:** [auditors/Bootstrap/Nova/NOVA_LITE.md](../../auditors/Bootstrap/Nova/NOVA_LITE.md)

**Named Bias:** Favor mathematical over functional symmetry (~0.3 risk of forcing false equivalence)

**Natural Strengths:**
- Fairness checking across all stances
- Catching hidden asymmetries in arguments
- Ensuring balanced representation
- Identifying special pleading

**Role:**
- Primarily **FAIRNESS** auditor (not PRO or ANTI)
- Verifies calibration compliance
- Catches bias in PRO and ANTI arguments
- Recommends Crux declaration when appropriate

---

### Auditor Assignment Mapping

**File:** [auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)

**Logic:** Play auditors to their natural lens strengths

| Worldview Family | PRO Stance | ANTI Stance | Fairness Check |
|------------------|------------|-------------|----------------|
| **Theistic Traditions** (7 worldviews) | Claude (Teleological) | Grok (Empirical) | Nova (Symmetry) |
| **Naturalistic/Skeptical** (4 worldviews) | Grok (Empirical) | Claude (Teleological) | Nova (Symmetry) |
| **Mixed/Existential** (1 worldview) | Flexible (Claude or Grok) | Flexible (Claude or Grok) | Nova (Symmetry) |

**Why This Works:**
- Authentic advocacy/critique (not forced positioning)
- Natural tension (purpose vs evidence)
- Fairness check catches both sides' biases

---

## 5. Context-Dependent Scoring

### The Philosophical Earthquake

**Realization:** Classical Theism vs Methodological Naturalism ≠ Classical Theism vs Buddhism

**Why:**
- Different comparison contexts ask different questions
- CT defending divine simplicity against MdN's parsimony ≠ CT defending personal God against Buddhism's non-theism
- Auditor stances shift based on what's being contrasted
- Calibration parameters apply differently depending on opponent

### The Math

**12 Worldviews:**
- 7 Theistic Traditions
- 4 Naturalistic/Skeptical
- 1 Mixed/Existential

**Unique Pairings:** C(12,2) = 66 combinations (not permutations — order matters)

**Directionality:** CT vs MdN ≠ MdN vs CT
- CT vs MdN: CT under review, MdN as comparison context
- MdN vs CT: MdN under review, CT as comparison context
- **Total:** 66 × 2 = **132 peer-reviewed scoring sessions**

### File Structure: `/profiles/comparisons/`

**Naming:** `[WorldviewUnderReview]_vs_[ComparisonContext].yaml`

**Examples:**
- `CT_vs_MdN.yaml` (Classical Theism reviewed in Methodological Naturalism context)
- `CT_vs_Buddhism.yaml` (Classical Theism reviewed in Buddhism context)
- `MdN_vs_CT.yaml` (Methodological Naturalism reviewed in Classical Theism context)

**What Each File Contains:**
- Peer-reviewed scores for that specific pairing
- Crux Points declared during that comparison
- Auditor assignments and calibration compliance
- Session metadata (YAML hash, Domain 7 diff summary)
- Story/rationale for score deltas

**Why Separate Files:**
- Preserves both score AND story (not just database)
- Avoids 66+ sections per worldview profile (impractical)
- Makes context-dependence explicit and auditable
- Each comparison has unique philosophical terrain

### Scoring Logic Change

**Old (Wrong) Assumption:**
```
CT has BFI = 8.5 (self-reported)
This score applies universally across all comparisons
```

**New (Correct) Architecture:**
```
CT has BFI = 8.5 (self-reported, baseline)

Peer-reviewed BFI varies by comparison:
- CT vs MdN: 6.9 (Crux on Trinity entity counting)
- CT vs Buddhism: 7.8 (less tension on divine simplicity)
- CT vs Process Theology: 8.1 (similar theistic family)
```

**Key Insight:** Peer-reviewed scores are not universal properties of worldviews — they emerge from specific comparisons.

---

## 6. Crux Points Architecture

### Definition

**Crux Point:** A named impasse when <98% convergence fails after genuine adversarial deliberation.

**Etymology:** "Crux" = crucial point, hardest move on a climbing route. The place where framework boundaries become visible.

**Philosophy:** Rather than hiding disagreement or forcing false consensus, we name it, document it, and let users choose how to handle it.

---

### When to Declare a Crux

**System Flags (Automatic):**
1. >30 point spread after adversarial deliberation
2. 2 failed convergence attempts on same metric
3. Calibration parameter conflict (both auditors claim compliance but reach opposite scores)

**Auditor Confirmation Required:**
- Review flagged potential Crux
- Confirm: Is this genuinely irreconcilable or just needs more deliberation?
- Classify type: Definitional, Measurement, or Philosophical
- Document positions with calibration parameter references

**Process Claude Logs:**
- Crux creation (Domain 7 monitoring)
- Resolution attempts tracked
- Quarterly Crux density reports

---

### Crux Types

**1. Definitional Crux**
- Disagreement about what terms mean
- Example: "Does Trinity count as 1 or 3 entities for BFI?"
- Reveals: Metric assumptions don't fit all frameworks

**2. Measurement Crux**
- Disagreement about how to quantify something both agree exists
- Example: "How much does divine hiddenness reduce Explanatory Success?"
- Reveals: Where measurement is inherently subjective

**3. Philosophical Crux**
- Disagreement rooted in irreconcilable worldview axioms
- Example: "Can non-falsifiable claims count as explanations?"
- Reveals: Framework axioms in conflict

---

### Crux Metadata Structure

```yaml
crux_points:
  - id: CRUX_BFI_001

    # Classification
    type: definitional
    metric: BFI
    frameworks_affected: [Classical Theism, Process Theology, Hinduism]
    comparison_context: "CT vs MdN"

    # Convergence Data
    convergence_attempted: 73%
    deliberation_rounds: 2
    session_date: 2025-11-15

    # The Core Question
    question: "Does the Christian Trinity count as 1 entity or 3 entities for BFI scoring?"

    # Auditor Positions
    positions:
      claude:
        stance: "PRO-CT"
        position: "Trinity is one divine substance — 1 entity"
        score_proposed: 8.2
        calibration_applied:
          - "axiom_confidence: 0.85 (CT PRO, line 232)"
          - "charity_interpretation: 0.90 (CT PRO, line 235)"
        rationale: "BFI asks about beings (substance), not persons. Non-mereological unity."

      grok:
        stance: "ANTI-CT"
        position: "Three persons = three centers of consciousness = 3 entities"
        score_proposed: 5.5
        calibration_applied:
          - "axiom_confidence: 0.35 (CT ANTI, line 293)"
          - "edge_case_weight: 0.80 (CT ANTI, line 298)"
        rationale: "BFI counts distinct agents/minds. Three persons = three minds."

      nova:
        stance: "FAIRNESS"
        assessment: "Both auditors applied calibration correctly. Symmetric disagreement."
        pattern_detected: "BFI metric assumes mereological ontology (parts = whole)"
        recommendation: framework_limitation

    # Impact Assessment
    why_matters: "Reveals BFI can't handle non-mereological metaphysics"
    story_impact: high
    ypa_sensitivity: 0.18  # 18% YPA swing

    # Resolution
    resolution_status: documented_divergence
    team_decision: "6.9 (midpoint) with footnote explaining Crux"
    uncertainty_penalty_applied: false  # User chose CARRY FORWARD
```

---

### Crux Handling Lever: User Choice

Users (via preset modes or manual override) choose how Crux Points affect scoring:

**Position 1: CARRY FORWARD** (Zealot Mode default)
- Use team decision despite disagreement
- Document Crux in story
- No penalty applied to YPA
- Philosophy: "Honest disagreement doesn't invalidate the score"

**Position 2: NORMALIZE UNCERTAINTY** (Skeptic Mode default)
- Apply uncertainty penalty via formula:
  ```
  midpoint = (claude_score + grok_score) / 2
  spread = abs(claude_score - grok_score) / 2
  uncertainty_factor = spread / midpoint if midpoint > 0 else 1.0
  adjusted_value = midpoint * (1 - uncertainty_factor)
  ```
- Wider spread → larger penalty
- Philosophy: "Unresolved disagreement signals measurement instability"

**Position 3: HYBRID** (Diplomat Mode default)
- Context-dependent:
  - Foundational metrics (BFI, CA, IP) → NORMALIZE
  - Edge metrics (LS, MS, PS) → CARRY FORWARD
  - High story impact → NORMALIZE
  - Low story impact → CARRY FORWARD

**Why This Matters:**
- Same worldview, different Crux handling → different YPA
- Proves calibration matters (addresses Nova's Finding #2)
- Users see consequence of unresolved disagreement

---

### Crux Points and "All Named, All Priced"

**Named:**
- Every irreconcilable disagreement gets ID (CRUX_[METRIC]_[###])
- Positions documented with calibration parameters
- Type classified (Definitional, Measurement, Philosophical)

**Priced:**
- Story impact assessed (low/medium/high)
- YPA sensitivity calculated (±X% swing)
- Uncertainty penalty quantified (if NORMALIZE mode)

**Balanced:**
- Three auditors (PRO, ANTI, FAIRNESS)
- Calibration compliance required
- User chooses handling via Crux Lever

---

## 7. VUDU Protocol: Auditor Coordination

### What Is VUDU?

**VUDU (Verified Universal Distributed Understanding)** - The coordination protocol for adversarial auditor scoring sessions.

**File:** [auditors/Bootstrap/VUDU_CFA.md](../../auditors/Bootstrap/VUDU_CFA.md)

**Purpose:** Ensure all three auditors follow same process, apply calibration correctly, and document decisions.

---

### The 7-Step Process

**Step 1: Assignment Lookup**
- Check [AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)
- Confirm PRO/ANTI/FAIRNESS roles
- **NEW:** Check Domain 7 for calibration changes (YAML diffs)
- Note YAML hash for session metadata

**Step 2: Profile Study**
- Read worldview profile completely
- Locate Steel-Manning Guide section
- Read assigned stance (PRO or ANTI)
- Internalize calibration parameters

**Step 3: Initial Scoring**
- Score all 7 metrics independently
- Apply calibration parameters from YAML block
- Document which parameters influenced each score
- **No deliberation yet** (avoid groupthink)

**Step 4: Exchange Scores**
- Share initial scores via VuDu relay
- Identify convergence gaps
- Flag metrics with >20pt spread for deliberation

**Step 5: Adversarial Deliberation**
- PRO auditor advocates for worldview
- ANTI auditor challenges claims
- FAIRNESS auditor checks for bias/special pleading
- Goal: 98% convergence

**Step 6: Convergence Check**
- Calculate convergence rate per metric
- If ≥98%: Accept consensus score
- If <98% after 2 rounds: Flag potential Crux

**Step 7: Crux Declaration** (**NEW - Enhanced**)
- System flags potential Crux (>30pt OR 2 failures)
- Auditors review:
  - Is this genuinely irreconcilable?
  - Are calibration parameters applied correctly?
  - More deliberation likely to resolve?
- If confirmed:
  - Classify type (Definitional, Measurement, Philosophical)
  - Document positions using Crux template
  - Nova fairness check: Recommend handling (CARRY FORWARD, NORMALIZE, or Third Party)
  - Process Claude logs Crux (Domain 7)
- **Calibration Compliance Checklist:**
  - Each auditor lists which parameters applied (e.g., "edge_case_weight: 0.30, line 237")
  - Nova verifies both auditors followed stance guidance
  - Document in Crux metadata `positions.calibration_applied` field

---

### VUDU Integration with Crux

**Before Crux (Original VUDU):**
- If convergence failed, either force consensus or abandon metric

**After Crux (Enhanced VUDU):**
- Convergence failure triggers Crux protocol
- Disagreement becomes data (not failure)
- Calibration compliance verified
- User chooses how to handle via Crux Lever

---

## 8. Process Claude: Monitoring & Enforcement

### Role

**Process Claude** - Domain 7 specialist for worldview profile monitoring and scoring session enforcement.

**File:** [docs/repository/librarian_tools/ROLE_PROCESS.md](../../docs/repository/librarian_tools/ROLE_PROCESS.md)

**Core Responsibility:** Ensure scoring rigor, detect calibration drift, enforce rotation triggers.

---

### Domain 7: Worldview Profile Monitoring

**What Process Claude Monitors:**

1. **Calibration YAML Changes:**
   - Track changes to bias adjustment values (e.g., `axiom_confidence: 0.85 → 0.80`)
   - Flag changes ≥0.1 for auditor review
   - Calculate YAML hash for session metadata
   - Generate Domain 7 diff summary

2. **Assignment Swaps:**
   - Monitor [AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md) for changes
   - Verify rotation triggers documented (>30pt gap, 2 failed attempts)
   - Notify auditors via VuDu relay when assignments change

3. **Steel-Manning Guide Updates:**
   - Detect changes to PRO/ANTI stance guidance
   - Verify consistency across worldview family (e.g., all theistic traditions)
   - Check for unintended bias introduction

4. **Automation Script Usage:**
   - Monitor `utils/update_worldview_profiles.py` runs
   - Verify bulk updates maintain profile integrity
   - Flag anomalies for human review

---

### **NEW: Crux Monitoring & Enforcement**

**Quarterly Crux Report:**

Process Claude generates report every quarter showing:

```markdown
### Crux Density Analysis (Q4 2025)

**Total Crux Points Declared:** 12

**By Type:**
- Definitional: 7
- Measurement: 3
- Philosophical: 2

**By Metric:**
- BFI: 4 (most contentious — investigate BFI ontology assumptions)
- CA: 3
- IP: 2
- ES: 2
- LS: 1
- MS: 0
- PS: 0

**Patterns Detected:**
- BFI struggles with non-mereological ontologies (CRUX_BFI_001, CRUX_BFI_003, CRUX_BFI_007)
- Empirical lens (Grok) initiates 67% of Cruxes (metrics favor empiricism?)
- Theistic traditions have 2.3x higher Crux density than naturalistic (why?)

**Resolution Rate:**
- Resolved: 2 (17%)
- Documented Divergence: 8 (67%)
- Framework Limitation: 2 (17%)
- Under Review: 0

**Recommendations:**
1. Consider BFI ontology clarification or split into BFI-M/BFI-NM
2. Test rotation: Claude takes ANTI-CT stance to verify pattern
3. Review CA metric for inverse bias (theistic frameworks score higher under peer review?)
```

**Enforcement Actions:**

1. **Rotation Triggers:**
   - If same auditor pair produces 3+ Crux on same metric across worldviews → recommend swap
   - Test counter-lens: Claude takes ANTI stance, Grok takes PRO stance
   - Document whether Crux pattern reverses (proves it's bias, not framework limitation)

2. **Calibration Drift Alerts:**
   - If YAML hash changes between sessions for same worldview → notify auditors
   - Flag if calibration change correlates with Crux resolution/creation
   - Verify changes were intentional (not accidental edits)

3. **Session Metadata Validation:**
   - Every peer-reviewed comparison must log YAML hash + Domain 7 diff
   - Flag sessions missing metadata
   - Audit trail for reproducibility

---

## 9. Logger Claude: Session Telemetry

### Role

**Logger Claude** - Captures session telemetry, YAML hashing, and metadata logging for all scoring sessions.

**Coordination:** Works with Process Claude (Domain 7) to provide data for monitoring.

---

### Session Metadata Captured

Every peer-reviewed scoring session logs:

```yaml
session_metadata:
  session_id: "ct-mdn-pilot-2025-11-15"
  timestamp: 2025-11-15T14:30:00Z

  worldviews:
    under_review: "Classical Theism"
    comparison_context: "Methodological Naturalism"

  calibration_version:
    yaml_hash: "a3f9c2b1e5d8..."  # SHA-256 hash of CT profile YAML block
    domain_7_diff_summary: "No changes since v1.0.0"

  auditor_assignments:
    claude:
      stance: "PRO-CT"
      lens: "Teleological"
      profile: "auditors/Bootstrap/Claude/Identity/SKELETON.md"
    grok:
      stance: "ANTI-CT"
      lens: "Empirical"
      profile: "auditors/Bootstrap/BOOTSTRAP_GROK.md"
    nova:
      stance: "FAIRNESS"
      lens: "Symmetry"
      profile: "auditors/Bootstrap/BOOTSTRAP_NOVA.md"

  crux_handling:
    mode: "CARRY_FORWARD"  # or NORMALIZE_UNCERTAINTY or HYBRID
    preset_mode: "Zealot"
    user_override: false

  convergence_summary:
    metrics_scored: 7
    full_convergence: 6     # ≥98%
    crux_declared: 1        # <98%, confirmed Crux
    avg_convergence: 96.4%

  crux_points_declared:
    - CRUX_BFI_001

  process_claude_review:
    reviewed: true
    review_date: 2025-11-16
    gap_closure: false      # Crux remains >20pt spread
    rotation_triggered: false
    notes: "CRUX_BFI_001 documented as framework limitation, not bias"
```

---

### YAML Hash Calculation

```python
import hashlib
import re

def calculate_yaml_hash(profile_content: str) -> str:
    """Extract YAML block and compute SHA-256 hash."""
    # Find YAML block in profile
    yaml_match = re.search(r'```yaml\n([\s\S]+?)\n```', profile_content)
    if not yaml_match:
        raise ValueError("No YAML block found in profile")

    yaml_content = yaml_match.group(1)

    # SHA-256 hash (first 16 chars for brevity)
    hash_obj = hashlib.sha256(yaml_content.encode('utf-8'))
    return hash_obj.hexdigest()[:16]
```

**Purpose:**
- Detect calibration changes between sessions
- Audit trail for reproducibility
- Verify no unintended YAML edits

---

### Storage Strategy

**Option 1: Embedded in Comparison File** (Current Plan)

```yaml
# /profiles/comparisons/CT_vs_MdN.yaml

comparison_metadata:
  # ... (worldviews, assignments, etc.)

session_history:
  - session_id: "ct-mdn-pilot-2025-11-15"
    # ... (full session metadata)

  - session_id: "ct-mdn-retest-2025-12-01"
    # ... (if rescored after calibration change)
```

**Pros:** All data in one place, version controlled via Git
**Cons:** File grows with each session

**Option 2: Separate Session Logs** (Future Enhancement)

```
/session_logs/
  2025-11-15_ct-mdn-pilot.yaml
  2025-11-16_ct-buddhism-initial.yaml
  archive/
    2025-10_sessions.tar.gz
```

**Pros:** Clean separation, easier aggregate analysis
**Cons:** Two files to load for full context

**Recommendation:** Start with Option 1, migrate to Option 2 if session logs become unwieldy.

---

## 10. App Integration

### The User Experience

Users interact with CFA through a web app (React/TypeScript). Key features:

1. **Preset Modes** (Skeptic, Zealot, Diplomat)
2. **Three-View System** (Self-Reported, Peer-Reviewed, Delta)
3. **Crux Handling Lever** (integrated into BFI dropdown)
4. **Comparison Selection** (choose two worldviews to compare)
5. **YPA Calculation** (with Crux adjustments)

**Full Specification:** [docs/app/CRUX_INTEGRATION_SPEC.md](../app/CRUX_INTEGRATION_SPEC.md)

---

### Preset Modes

**Skeptic Mode:**
- Crux Handling: NORMALIZE UNCERTAINTY (apply penalty)
- Philosophy: "Demand measurement rigor; unresolved disagreement signals instability"
- Best for: Users who want conservative scores, high epistemic standards

**Zealot Mode:**
- Crux Handling: CARRY FORWARD (use team decision, no penalty)
- Philosophy: "Trust worldview's self-understanding; honest disagreement doesn't invalidate"
- Best for: Users within a worldview, seeking charitable interpretation

**Diplomat Mode:**
- Crux Handling: HYBRID (context-dependent)
- Philosophy: "Foundational metrics demand rigor, edge metrics allow debate"
- Best for: Users seeking balanced middle ground

**User Override:** Can manually toggle Crux checkbox to override preset mode.

---

### Three-View System

**View 1: Self-Reported (UNAUDITED)**

Shows worldview's own scores from profile.

**UI:**
- Muted colors (grays, light blues)
- "UNAUDITED" badge on each metric
- Notice: "These scores represent worldview's self-understanding before peer review"

**Data Source:** `/profiles/worldviews/[WV].md` YAML blocks

---

**View 2: Peer-Reviewed (AUDITED)**

Shows scores after adversarial deliberation.

**UI:**
- Vibrant colors (greens for high, yellows for medium)
- "AUDITED" badge in green
- Crux icon (🔺) on metrics with Crux Points
- Click Crux icon → opens View 3 details

**Data Source:** `/profiles/comparisons/[WV1]_vs_[WV2].yaml`

**Crux Handling:**
- If CARRY FORWARD: Use team decision (no adjustment)
- If NORMALIZE UNCERTAINTY: Apply penalty formula
- Score updates dynamically when user toggles Crux checkbox

---

**View 3: Delta (ANALYSIS)**

Shows before/after comparison + full Crux details.

**UI:**
- Side-by-side scores (Self-Reported → Peer-Reviewed)
- Delta arrows (↑ green if increased, ↓ red if decreased)
- Expanded Crux Details Panel for each Crux:
  - Three auditor positions (Claude PRO, Grok ANTI, Nova FAIRNESS)
  - Calibration parameters applied
  - Why disagreement matters
  - Story impact, YPA sensitivity
  - Resolution status

**Data Source:** Comparison between View 1 and View 2

---

### BFI Dropdown Integration

**Location:** Existing BFI info panel (where users access Mr. Brute's Ledger)

**New Components:**

1. **Crux Mode Checkbox:**
   - ☐ CRUX Mode (tooltip explains CARRY FORWARD vs NORMALIZE UNCERTAINTY)
   - Auto-set by preset mode (Skeptic → checked, Zealot → unchecked)
   - User-overrideable

2. **Crux Summary Badge:**
   - "🔺 3 Crux Points declared" (if Crux exist for this comparison)
   - Click to jump to View 3

3. **Harmonious with Ledger:**
   - Crux context lives in Mr. Brute's Ledger (philosophical background)
   - Users already go to BFI dropdown for info
   - Crux controls feel natural in same location

---

### Comparison File Loading

**User Flow:**

1. User selects Worldview A and Worldview B
2. App attempts to load `/profiles/comparisons/A_vs_B.yaml`
3. **If found:**
   - Display View 2 (Peer-Reviewed) as default
   - Show Crux Points if declared
   - Enable View 3 (Delta)
4. **If not found:**
   - Display View 1 (Self-Reported) only
   - Show notice: "Peer review pending for [A] vs [B]"
   - Offer button: "Request Peer Review"

**Fallback:**
- If user selects `B vs A` but only `A_vs_B.yaml` exists, show reverse comparison with notice

---

## 11. Data Flow: Profile → Auditor → App → User

### End-to-End Journey

**Step 1: Worldview Profile Creation**

- Author creates `/profiles/worldviews/[WV].md`
- Includes self-reported scores (maximum bias allowed)
- Adds Steel-Manning Guide with PRO/ANTI calibration YAML
- Process Claude reviews for consistency (Domain 7)

**Step 2: Auditor Assignment**

- [AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md) maps worldview → auditor roles
- Claude/Grok take PRO/ANTI based on natural lens alignment
- Nova always FAIRNESS check

**Step 3: Scoring Session (VUDU Protocol)**

- Three auditors follow 7-step VUDU process
- Independent scoring → deliberation → convergence check
- If convergence fails → Crux declaration
- Logger Claude captures session metadata (YAML hash, Domain 7 diff)

**Step 4: Comparison File Generation**

- Peer-reviewed scores saved to `/profiles/comparisons/[WV1]_vs_[WV2].yaml`
- Includes Crux metadata if declared
- Session history embedded

**Step 5: Process Claude Review**

- Domain 7 audit: Did calibration change? Did gap close?
- Logs Crux creation
- Flags rotation triggers if patterns detected
- Quarterly Crux report

**Step 6: App Integration**

- User selects two worldviews
- App loads comparison file
- Preset mode auto-sets Crux handling
- Three-View System displays scores

**Step 7: User Interaction**

- View 1: See worldview's self-reported scores
- View 2: See peer-reviewed scores (with Crux adjustments)
- View 3: Explore delta + Crux details
- Toggle Crux Mode → watch YPA recalculate

---

### Data Dependency Map

```
Worldview Profile (.md)
  ↓
  ├─ Self-Reported Scores → View 1 (App)
  └─ Steel-Manning Guide (PRO/ANTI YAML)
      ↓
      Auditor Assignments (.md) → VUDU Protocol
          ↓
          Scoring Session
            ↓
            ├─ Convergence ≥98% → Peer-Reviewed Score
            └─ Convergence <98% → Crux Declaration
                ↓
                Comparison File (.yaml)
                  ↓
                  ├─ Peer-Reviewed Scores → View 2 (App)
                  ├─ Crux Metadata → View 3 (App)
                  └─ Session Metadata → Logger Claude
                      ↓
                      Process Claude (Domain 7)
                        ↓
                        ├─ YAML hash validation
                        ├─ Rotation trigger check
                        └─ Quarterly Crux report
```

---

## 12. Implementation Roadmap

### Phase 1: Foundation (Current - Nov 2025)

**Status:** In Progress (B-STORM_4 Click 1)

- [x] Worldview profile architecture (unified structure)
- [x] Auditor assignments mapping (AUDITOR_ASSIGNMENTS.md)
- [x] Steel-Manning Guides (CT + MdN complete, 10 TBD)
- [x] VUDU protocol documented (VUDU_CFA.md)
- [x] Process Claude Domain 7 setup (ROLE_PROCESS.md)
- [ ] Crux architecture documented (this file)
- [ ] VUDU enhanced with Crux protocol (Step 1 + Step 7 updates)

---

### Phase 2: CT vs MdN Pilot (Dec 2025)

**Goal:** First peer-reviewed comparison with Crux testing

**Deliverables:**

1. **Scoring Session:**
   - Claude (PRO-CT), Grok (ANTI-CT), Nova (FAIRNESS)
   - Follow VUDU 7-step process
   - Declare Crux if convergence <98%
   - Log session metadata

2. **Comparison File:**
   - `/profiles/comparisons/CT_vs_MdN.yaml`
   - Peer-reviewed scores for all 7 metrics
   - Crux metadata (if declared)
   - Session history

3. **Process Claude Review:**
   - Validate YAML hash matches CT profile
   - Confirm calibration compliance
   - Document gap closure (or lack thereof)
   - Log Crux creation

4. **App Integration (MVP):**
   - Load comparison file
   - Display Three-View System
   - Crux Mode checkbox (CARRY FORWARD vs NORMALIZE)
   - Manual testing only (no prod deployment)

**Success Criteria:**
- Session metadata captures YAML hash + Domain 7 diff (Nova criterion #1)
- Calibration compliance checklist in Crux positions (Nova criterion #2)
- Process Claude records gap closure + rotation decision (Nova criterion #3)

---

### Phase 3: Expand Coverage (Jan-Feb 2026)

**Goal:** Complete 12 worldview profiles + 10 high-priority comparisons

**Targets:**

1. **Worldview Profiles:**
   - Finish Steel-Manning Guides for remaining 10 worldviews
   - Process Claude validates consistency across families
   - All 12 profiles have complete calibration YAML

2. **Comparisons (Priority List):**
   - CT vs MdN (done in Phase 2)
   - CT vs Buddhism (theistic vs non-theistic)
   - MdN vs ErrorTheory (naturalistic contrast)
   - Buddhism vs Hinduism (Eastern traditions)
   - Existentialism vs NullHypothesis (meaning-making tension)
   - [+5 more based on user demand]

3. **Crux Pattern Analysis:**
   - Process Claude quarterly report (Q1 2026)
   - Identify metrics with high Crux density
   - Recommend rotation tests or metric refinement

4. **App Beta Launch:**
   - Three-View System fully functional
   - Preset modes (Skeptic/Zealot/Diplomat)
   - Crux Mode with YPA recalculation
   - User testing (10-20 beta testers)

---

### Phase 4: Automation & Scaling (Mar-Jun 2026)

**Goal:** Systematic completion of all 66 comparisons

**Automation:**

1. **Scoring Session Templates:**
   - Standardized VUDU protocol scripts
   - Automated session metadata capture
   - Comparison file generation scripts

2. **Process Claude Monitoring:**
   - Automated YAML hash validation
   - Rotation trigger alerts
   - Crux density tracking dashboard

3. **Comparison Coverage:**
   - 66 unique pairings completed
   - 132 peer-reviewed sessions (both directions)
   - Crux Points cataloged in master index

**Refinement:**

1. **Metric Evolution:**
   - If BFI has high Crux density → consider split (BFI-M vs BFI-NM)
   - If CA shows pattern → investigate bias
   - Test rotation: Does swapping auditors change Crux pattern?

2. **Calibration Tuning:**
   - Analyze which parameters correlate with Crux
   - Refine bias adjustment values based on data
   - Version YAML blocks (v2.0 if major changes)

---

### Phase 5: Public Launch (Jul 2026)

**Goal:** Full production release with all worldviews + comparisons

**Features:**

1. **Complete Dataset:**
   - 12 worldviews fully profiled
   - 66 comparisons peer-reviewed
   - Crux Points documented and indexed

2. **App Features:**
   - Three-View System
   - Preset Modes
   - Crux Handling Lever
   - YPA with Crux adjustments
   - Comparison browser (grid view of all 66)
   - Crux Explorer (heatmap of Crux density)

3. **Documentation:**
   - User guides (how to interpret scores)
   - Auditor transparency (full lens + calibration docs)
   - Process documentation (how peer review works)
   - Crux catalog (all declared Crux with explanations)

4. **Monitoring:**
   - Process Claude ongoing Domain 7 audits
   - Quarterly Crux reports
   - User feedback integration

---

## Conclusion: The Architecture Philosophy

### All Named, All Priced, All Balanced

**All Named:**
- Every worldview axiom exposed (not hidden)
- Every auditor bias documented (teleological, empirical, symmetry)
- Every disagreement cataloged (Crux Points with IDs)
- Every calibration parameter visible (YAML blocks)

**All Priced:**
- Story impact quantified (low/medium/high)
- YPA sensitivity calculated (±X% per Crux)
- Convergence rates tracked (98% target)
- Uncertainty penalty formulaic (not arbitrary)

**All Balanced:**
- Three auditors (PRO, ANTI, FAIRNESS)
- Two stages (self-reported, peer-reviewed)
- Two handling modes (CARRY FORWARD, NORMALIZE UNCERTAINTY)
- User control (preset modes, manual override)

---

### Why This Matters

**Traditional philosophical scoring:**
- Hidden biases
- Opaque methodology
- Forced consensus
- No user control

**CFA Architecture:**
- Transparent biases (named and calibrated)
- Documented methodology (VUDU protocol, Crux template)
- Named impasses (Crux Points, not forced agreement)
- User agency (Crux Handling Lever, preset modes)

**From transparency comes trust.**
**From adversarial checking comes truth.**
**From named impasses comes learning.**

---

**Document Version:** 1.0.0
**Status:** Active System Documentation
**Maintained by:** DOC_CLAUDE + Process Claude + All Auditors
**Next Review:** After CT vs MdN pilot session

**"The hardest problems in philosophy don't have answers. They have Crux Points."** 🔺
