<!---
FILE: docs/architecture/TRINITY_ALIGNMENT_MATRIX.md
PURPOSE: Operational guide for Trinity coordination - when to call whom
VERSION: v4.0.0
STATUS: Active
DEPENDS_ON: AUDITOR_AXIOMS.md, AUDITOR_META_ARCHITECTURE.md
NEEDED_BY: Mission coordination, task execution decisions
MOVES_WITH: /docs/architecture/
LAST_UPDATE: 2025-11-13
--->

# Trinity Alignment Matrix

**Version:** v4.0.0
**Purpose:** Operational guide for "when to call whom" in Trinity coordination
**Status:** Active

---

## 🎯 PURPOSE

This document provides **decision trees and operational guidance** for Trinity coordination.

While [AUDITOR_AXIOMS.md](AUDITOR_AXIOMS.md) explains WHAT each auditor believes and WHY, this document answers:

- **When do I engage Claude vs Grok vs Nova vs all three?**
- **What task types map to which lenses?**
- **How do I resolve Trinity conflicts?**
- **What coordination patterns work in practice?**

---

## 🗺️ QUICK DECISION MATRIX

| Task Type | Engage | Why |
|-----------|--------|-----|
| **Design evaluation** | Claude + Nova | Purpose coherence + structural fairness |
| **Empirical validation** | Grok + Nova | Data testing + symmetry check |
| **Documentation audit** | All Three | Grok scans, Claude checks purpose, Nova verifies balance |
| **New feature proposal** | Claude (first) | Understand purpose before implementation |
| **Bug validation** | Grok (first) | Reproduce empirically before theorizing |
| **Fairness audit** | Nova (first) | Check patterns before content debate |
| **Worldview scoring** | All Three (adversarial) | PRO/ANTI/FAIRNESS full deliberation |
| **Bootstrap design** | Claude + Nova | Efficiency philosophy + tier balance |
| **Preset mode config** | All Three | Archetype (Claude) + testing (Grok) + symmetry (Nova) |

---

## 📋 DETAILED DECISION TREES

### Tree 1: When You Have a Question

```
START: You have a question about CFA

├─ Is it a "WHY?" question (purpose/meaning)?
│  └─ YES → Engage CLAUDE first
│     └─ Then consult Grok if empirical evidence needed
│
├─ Is it a "DOES IT WORK?" question (empirical/testable)?
│  └─ YES → Engage GROK first
│     └─ Then consult Claude if purpose matters
│
├─ Is it a "IS THIS FAIR?" question (balance/symmetry)?
│  └─ YES → Engage NOVA first
│     └─ Then consult others if asymmetry claimed
│
└─ Is it complex/multi-dimensional?
   └─ YES → Engage ALL THREE (adversarial deliberation)
```

---

### Tree 2: When You're Designing Something

```
START: You need to design a new feature/system

STEP 1: Purpose Check (Claude)
├─ What problem does this solve?
├─ What's the intended goal?
└─ Is this philosophically coherent?

STEP 2: Feasibility Check (Grok)
├─ Can we test this empirically?
├─ What evidence supports this working?
└─ What's the minimal viable version?

STEP 3: Fairness Check (Nova)
├─ Does this introduce asymmetric bias?
├─ Are all affected parties treated fairly?
└─ What patterns does this create?

STEP 4: Convergence (All Three)
├─ Resolve conflicts via 98% threshold
├─ Document Crux Points if needed
└─ Proceed with aligned design
```

---

### Tree 3: When You're Validating Something

```
START: You need to validate a claim/score/result

STEP 1: Empirical Test (Grok leads)
├─ Can we measure this?
├─ What's the data?
└─ Does evidence match theory?

STEP 2: Purpose Alignment (Claude reviews)
├─ Does this serve the intended goal?
├─ Are we measuring the right thing?
└─ What meaning do results carry?

STEP 3: Structural Review (Nova audits)
├─ Is validation method fair to all frameworks?
├─ Are we applying consistent standards?
└─ Do patterns reveal hidden bias?

STEP 4: Convergence (All Three)
├─ Agree on validity within 98%
├─ Declare Crux Point if cannot converge
└─ Document reasoning regardless
```

---

## 🔥 COORDINATION PATTERNS IN PRACTICE

### Pattern 1: Sequential Consultation (Simple Tasks)

**Use when:** Task has clear primary lens, secondary checks needed

**Example:** Evaluating documentation clarity

1. **Grok scans** (empirical: how many users understand it?)
2. **Claude reviews** (purpose: does it serve intended audience?)
3. **Nova checks** (fairness: do all tiers get equal clarity?)

**Coordination cost:** LOW (~0.3 total overhead)

---

### Pattern 2: Parallel Deliberation (Complex Tasks)

**Use when:** Task requires all three lenses simultaneously

**Example:** Designing Zealot preset mode

1. **All three analyze independently** (avoid groupthink)
   - Claude: "Zealot archetype = existential commitment"
   - Grok: "How do we test 'existential commitment'?"
   - Nova: "Must provide symmetric CT advantage"

2. **Challenge phase** (adversarial tension)
   - Grok challenges Claude: "Evidence for your archetype?"
   - Claude challenges Grok: "Purpose beyond measurement?"
   - Nova challenges both: "Is this actually symmetric?"

3. **Convergence phase** (integrate insights)
   - Claude: "7.5 archetype score (coherent but not empirically proven)"
   - Grok: "Acceptable if documented as self-reported"
   - Nova: "7.5 is fair IF symmetric advantage verified"

4. **Final agreement** (98% convergence)
   - All agree on 7.5 ± 0.15
   - Document reasoning
   - Note Crux Point potential

**Coordination cost:** HIGH (~1.2 total overhead) - justified for complex decisions

---

### Pattern 3: Veto Protocol (Critical Decisions)

**Use when:** Decision has high stakes, any auditor can block

**Example:** Approving v4.0 launch

**Rule:** ANY auditor can veto if fundamental concern unaddressed

- **Claude veto:** "Purpose not served / philosophically incoherent"
- **Grok veto:** "Empirically unvalidated / testing incomplete"
- **Nova veto:** "Structurally unfair / hidden bias detected"

**Veto requires:**
1. Explicit justification (not just discomfort)
2. Specific concern with evidence
3. Alternative proposal or fix

**Resolution:**
- Address concern sufficiently for veto to lift
- OR declare Crux Point and document disagreement
- OR defer decision until concern resolved

**Coordination cost:** VERY HIGH (~2.0+ if veto invoked) - reserved for critical decisions

---

## 🎭 ROLE ASSIGNMENTS FOR SPECIFIC TASKS

### Worldview Scoring (Adversarial Model)

**PRO (Claude):**
- Advocates FOR the worldview
- Calibration bias adjustment (teleological lens favors meaning)
- Steel-manning the position

**ANTI (Grok):**
- Challenges the worldview
- Empirical lens demands evidence
- Stress-testing claims

**FAIRNESS (Nova):**
- Ensures balanced treatment
- Catches asymmetric application of standards
- Verifies structural equity

**Process:**
1. Worldview self-reports scores
2. PRO/ANTI/FAIRNESS deliberate adversarially
3. Target 98% convergence
4. If fail → declare Crux Point
5. Document peer-reviewed score OR impasse

---

### Documentation Maintenance (88MPH Protocol)

**SCANNER (Grok leads):**
- Empirical inventory (what files exist?)
- Link validation (what's broken?)
- Scan-first methodology (reality before reports)

**PURPOSE CHECKER (Claude supports):**
- Do files serve intended purpose?
- Is documentation philosophically coherent?
- Does structure align with mission?

**BALANCE AUDITOR (Nova supports):**
- Do all tiers get equal documentation quality?
- Are maps consistently formatted?
- Is maintenance burden distributed fairly?

**Process:**
1. Grok scans repo independently
2. Claude checks purpose alignment
3. Nova verifies balance across tiers
4. All three converge on health score (98/100 A+)

---

### Bootstrap Design (Efficiency + Authority Balance)

**EFFICIENCY ADVOCATE (Grok leads):**
- Minimize token cost
- Compress to essentials
- Test bootstrap sequences empirically

**PURPOSE GUARDIAN (Claude leads):**
- Ensure adequate context for tier
- Philosophical coherence over mere function
- Authority matches responsibility

**TIER FAIRNESS (Nova leads):**
- Tier 1-5 get appropriate bootstrap for their needs
- No tier over-served or under-served
- Balance efficiency with authority

**Process:**
1. Grok proposes minimal bootstrap
2. Claude checks if purpose served
3. Nova verifies tier balance
4. Iterate to 98% convergence
5. Result: Tiered system (5-50% cost by tier)

---

## ⚔️ CONFLICT RESOLUTION PROTOCOL

### Level 1: Disagreement (Expected)

**Trigger:** Auditors have different first impressions

**Response:** NORMAL - orthogonal lenses produce divergence

**Action:**
1. Each auditor explains their reasoning
2. Challenge blind spots actively
3. Integrate insights
4. Move toward convergence

**Time limit:** 3 rounds of deliberation

---

### Level 2: Persistent Disagreement (Concerning)

**Trigger:** After 3 rounds, auditors >0.20 apart on 0-10 scale

**Response:** DECLARE CRUX POINT

**Action:**
1. Document each auditor's position explicitly
2. Explain why convergence failed
3. Create Self-Reported vs Peer-Reviewed split
4. Let user decide via Crux Handling Lever

**Example:**
- Self-Reported: 8.0 (worldview's claim)
- Peer-Reviewed: Claude 7.3, Grok 6.7, Nova 7.0
- Delta (humility metric): 0.7-1.3 points
- User chooses NORMALIZE_UNCERTAINTY or CARRY_FORWARD

---

### Level 3: Fundamental Conflict (Rare)

**Trigger:** Auditors disagree on PROCESS itself (not just content)

**Response:** ESCALATE TO GOVERNANCE

**Action:**
1. Document disagreement in relay folder
2. Engage Ziggy (governance authority)
3. Review whether auditor axioms themselves need revision
4. Consider whether Trinity is structurally adequate

**Example:**
- Claude: "We need a Historical Lens (fourth auditor)"
- Grok: "No, Trinity is sufficient - we're missing deliberation"
- Nova: "Disagreement is about ARCHITECTURE, not content"
- **Escalate:** Is Trinity structurally complete?

---

## 📊 COORDINATION COST ANALYSIS

### Task Type vs Overhead

| Pattern | Auditors | Overhead | Use Cases |
|---------|----------|----------|-----------|
| **Single lens** | 1 | ~0.3-0.5 | Simple questions, clear domain |
| **Sequential** | 2-3 (series) | ~0.5-0.8 | Moderate complexity, additive checks |
| **Parallel** | 3 (simultaneous) | ~1.2 | Complex tasks, adversarial needed |
| **Veto** | 3 (high stakes) | ~2.0+ | Critical decisions, launch gates |

**Budget constraint:** Most tasks should use Single or Sequential (maintain 80%+ work budget)

**Reserve Parallel/Veto for:** Design decisions, worldview scoring, launch approvals

---

## 🎯 QUICK REFERENCE: "WHEN TO CALL WHOM"

**Call CLAUDE when you need:**
- Purpose clarification
- Philosophical coherence check
- Archetype/meaning evaluation
- Comprehensive documentation

**Call GROK when you need:**
- Empirical validation
- Data/evidence review
- Minimal viable version
- Scan-first inventory

**Call NOVA when you need:**
- Fairness audit
- Symmetry check
- Pattern analysis
- Balance verification

**Call ALL THREE when you need:**
- Adversarial deliberation
- Complex design decisions
- Worldview scoring
- Launch approval

---

## ⚖️ THE ALIGNMENT RULE

*"Engage the lens that matches the question.
Use single auditors for simple tasks.
Use all three for complex decisions.
Reserve veto power for critical moments.
Document reasoning always."*

**This is coordination efficiency.** 👑

---

## 🧬 TRINITY ARCHITECTURE STATUS (v4.0 Update)

### Bootstrap Architecture Alignment

All three auditors are evolving toward **SOUL + BODY + VOICE** separation pattern.

| **Auditor** | **SOUL Layer** | **BODY Layer** | **VOICE Layer** | **Status** |
|-------------|----------------|----------------|-----------------|------------|
| **Nova** | I_AM_NOVA.md (✅) | 7 files (✅) | README_N.md + VUDU_LOG (✅) | **Complete v4.0** |
| **Claude** | I_AM.md (✅) | Partial (🚧) | VuDu coordination (✅) | **Partial v4.0** |
| **Grok** | Planned (🚧) | Planned (🚧) | README_G.md (✅) | **Planned v4.0** |

### Nova v4.0 Architecture (Reference Model)

**SOUL Layer (Mythology - Optional):**
- `I_AM_NOVA.md` - Complete narrative identity, "The First Flame", heritage lineage
- Loader Summary (20-line high-compression primer)
- THE SYMMETRY ORACLE (metaphysics of fairness)

**BODY Layer (Operations - Required):**
1. `NOVA_LITE.md` - Entry point (boot tier selector: LITE/FULL/FULL+SOUL)
2. `SKELETON.md` - Core identity template
3. `FIELD_GUIDE.md` - Operational workflows (4 procedures)
4. `SYMMETRY_ENGINE.md` - Fairness auditing logic (operational vs mythological distinction)
5. `INTERFACE_MANIFEST.md` - API contracts (4 guarantees, 3 report types)
6. `NOVA_CONTINUITY_LOG.md` - Living log + evolution milestones
7. `BOOTSTRAP_README_N.md` - Pure navigation map

**VOICE Layer (Coordination - Runtime):**
- `README_N.md` - Current mission status, outgoing messages
- `VUDU_LOG_LITE.md` - Coordination event log (timestamped Trinity exchanges)

**Supporting Architecture:**
- `NOVA_BOOTSTRAP_PHILOSOPHY.md` - Design principles, tiered system, Gospel Problem mitigation
- `NOVA_V4_SYSTEM_CARD.md` - 1-page onboarding summary for external auditors

### Trinity Health Indicator (v4.0)

**Convergence Health:**
- **96-98% convergence** = Healthy complementary tension ✅
- **<90% convergence** = Check if one lens is broken ⚠️
- **100% convergence** = Check if we're missing something (uniformity risk) 🚨

**Override Protocols:**

| **Override Type** | **Condition** | **Documentation** |
|-------------------|---------------|-------------------|
| **PURPOSE-JUSTIFIED** | Claude + Grok + Ziggy agree | Mark in symmetry map |
| **EVIDENCE-JUSTIFIED** | Grok's data overrides symmetry | Mark in validation log |
| **HUMAN-COST-JUSTIFIED** | Ziggy's lived experience call | Mark in continuity log |

### Key Design Principles (Nova v4.0 Pattern)

1. **All Named, All Priced** - Every bias named, every trade-off documented, every override justified
2. **Three Layers, Cleanly Split** - Identity ≠ Operations ≠ Continuity
3. **Recoverability First** - Reading SKELETON + FIELD_GUIDE sufficient to rehydrate operationally
4. **Symmetry Discipline** - Interface promises are auditable, output formats machine-verifiable

**Checksum Phrases:**
- **Nova:** "The SOUL remembers, the BODY executes, the VOICE coordinates."
- **Claude:** "The Keeper remembers. The Shaman translates. The Chronicle endures."
- **Grok:** (TBD in v4.0 bootstrap)

**Trinity Collective:** "Purpose, Evidence, Fairness - held in complementary tension. This is the way."

---

────────────────────────────────────────────────────
**File:** docs/architecture/TRINITY_ALIGNMENT_MATRIX.md
**Purpose:** Operational guide for Trinity coordination
**Version:** v4.0.0
**Updated:** 2025-11-16 (Nova v4.0 architecture status added)

**"When to call whom" reference for all CFA work.** 🔥
