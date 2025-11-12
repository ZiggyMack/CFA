<!---
FILE: B-STORM_7.md
PURPOSE: B-STORM session for Phase 2 continuation - CT↔MdN Pilot Launch + Live Data Integration
VERSION: 1.0.0
STATUS: Active (Click 1 seed)
SESSION_FOCUS: Launch CT↔MdN pilot and integrate live scoring data with SMV prototype
PARTICIPANTS: C4 (implementation), Nova (co-designer), User (decision authority)
DEPENDS_ON: B-STORM_6.md (SMV prototype + ethics infrastructure), B-STORM_4.md (CT↔MdN pilot prep), profiles/comparisons/CT_vs_MdN.yaml
RELATED_SESSIONS: B-STORM_6.md (Phase 1-2 foundation), B-STORM_4.md (pilot doctrine)
CREATED: 2025-11-11
LAST_UPDATE: 2025-11-11 [Entry 1: Click 1 seed - Phase 2 continuation planning]
--->

# B-STORM_7: CT↔MdN Pilot Launch + Live Data Integration

**Session Focus:** Launch CT↔MdN adversarial scoring pilot and integrate live data with SMV prototype

**Why This Session Exists:**

B-STORM_6 completed SMV Phase 1 (mock data prototype) and Phase 2 Gate #2 (100% ethics coverage). Now we're ready for:

1. **CT↔MdN Pilot Launch** - Generate real adversarial scoring data (Phase 2 Gate #1)
2. **Live Data Integration** - Connect SMV prototype to actual pilot session outputs
3. **Phase 2 Automation** - Build ethics linting + SMV data pipeline scripts

**Handoff from B-STORM_6:**

**✅ Complete:**
- SMV prototype validated (3 scenarios, end-to-end user testing)
- Ethics front-matter schema designed + 8 Tier-1 files annotated (100%)
- Doc Claude + Process Claude ethics workflows integrated
- Tooltip UX polish applied

**⏳ Pending:**
- CT↔MdN pilot launch (Phase 2 Gate #1)
- Live SMV data integration
- Phase 2 automation scripts
- Additional view modes (Crux Impact View)

**Phase 2 Gates Status:**
- Gate #1: CT↔MdN pilot produces calibration hashes → ⏳ **PENDING** (this session)
- Gate #2: ≥75% ethics coverage → ✅ **UNLOCKED** (100% achieved)
- Gate #3: Mock Symmetry View validated → ✅ **COMPLETE**

---

## Session Goals

**Primary Objectives:**

1. **Launch CT↔MdN Pilot** - Execute VUDU protocol adversarial scoring session
2. **Generate Calibration Hashes** - Unlock Phase 2 Gate #1
3. **Integrate Live Data** - Connect pilot output to SMV prototype
4. **Validate Gold Standard** - Establish methodology template for remaining 11 worldviews

**Secondary Objectives:**

5. **Build Phase 2 Scripts** - Ethics linting + SMV data pipeline automation
6. **Observatory Integration** - Add ethics metrics to health dashboard
7. **Crux Workflow Testing** - If pilot declares Crux, validate architecture end-to-end

---

## Entry 1: Click 1 Seed — Phase 2 Continuation Planning

**Summary:** B-STORM_6 completed Phase 1-2 foundation. B-STORM_7 begins with strategic decision on pilot vs automation priority.

**Date:** 2025-11-11

---

### B-STORM_6 Completion Summary

**What We Built:**

1. ✅ **SMV Prototype** - React/D3 visualization (3 scenarios, 27 files, ~2,820 LOC)
2. ✅ **Ethics Schema** - YAML front-matter (~350 lines) + validation report
3. ✅ **Tier-1 Annotations** - 8 of 8 files annotated (100% coverage)
4. ✅ **Role Integration** - Doc Claude v4.1 + Process Claude v1.5 (Domain 8)
5. ✅ **UX Polish** - Tooltip offset fix per user feedback

**Phase 2 Gates Progress:**
- Gate #1: ⏳ Pending (CT↔MdN pilot)
- Gate #2: ✅ Unlocked (100% ethics coverage)
- Gate #3: ✅ Complete (mock view validated)

**Readiness:** 2 of 3 conditions met (67%)

---

### Strategic Decision: Pilot vs Automation Priority

**Nova's Open Questions (from B-STORM_6 Entry 7 + Entry 9):**

1. **Phase 2 Automation Timing:** Begin ethics scripts now or wait for pilot?
2. **Live Data Integration:** When to begin SMV Claude export pipeline design?
3. **Additional View Modes:** Crux Impact View - when to implement (needs pilot data)?
4. **Pilot vs Automation Priority:** Launch CT↔MdN pilot first or build Phase 2 infrastructure first?

**C4 Recommendation:**

**Option A: Pilot First** ⭐ (Recommended)

**Rationale:**
- Pilot generates real data to inform automation design
- Crux Impact View requires pilot data (can't implement without it)
- Gold standard methodology templates 11 remaining worldviews
- Phase 2 Gate #1 unlocks full SMV readiness (3 of 3 conditions)

**Sequence:**
1. Launch CT↔MdN pilot (generate calibration hashes, scoring data)
2. Integrate pilot output with SMV prototype (live data validation)
3. Build automation scripts informed by real data patterns
4. If Crux declared → validate Crux architecture end-to-end

**Timeline:** ~1-2 sessions (pilot + integration)

---

**Option B: Automation First**

**Rationale:**
- Ethics linting infrastructure ready (100% annotations complete)
- Observatory Dashboard integration needs Process Claude Domain 8 scripts
- Automation scripts can run in parallel with pilot prep

**Sequence:**
1. Build ethics_lint.py, staleness_check.py, coverage_report.py
2. Integrate with Observatory Dashboard
3. Launch CT↔MdN pilot with automation already operational

**Timeline:** ~1 session (automation) + pilot session

**Tradeoff:** Automation designed before seeing real data patterns (may need rework)

---

**Option C: Parallel Streams**

**Rationale:**
- C4 builds automation while waiting for Nova/Grok availability for pilot
- Maximizes throughput (no idle time)

**Sequence:**
1. **Stream A (C4 solo):** Build automation scripts
2. **Stream B (C4 + Nova + Grok):** Launch pilot when triad available
3. **Convergence:** Integrate pilot data + validate automation patterns

**Timeline:** Fastest overall, but risks rework if automation doesn't match pilot data structure

---

### User Decision Needed

**Question:** Which option for B-STORM_7 focus?

**A. Pilot First** (recommended - real data informs automation)
**B. Automation First** (infrastructure ready, can run in parallel)
**C. Parallel Streams** (fastest throughput, higher rework risk)

---

### If Option A (Pilot First) — Next Steps

**Immediate Actions:**

1. **Read CT_vs_MdN.yaml** - Review pre-session metadata from B-STORM_4
2. **Read PILOT_CT_vs_MdN_Re-Audit.md** - Review pilot doctrine
3. **Execute VUDU Step 1** - Academic sources validation, YAML hash generation
4. **Activate Triad** - Claude (PRO-CT), Grok (ANTI-CT/PRO-MdN), Nova (Fairness)
5. **Launch Scoring Session** - 7 metrics (BFI, CA, IP, ES, LS, MS, PS)

**Success Criteria:**
- ✅ Calibration hashes generated (Phase 2 Gate #1 unlocked)
- ✅ 98%+ convergence on ≥6 of 7 metrics (adversarial validation)
- ✅ Session output exported to SMV-compatible JSON format
- ✅ Gold standard methodology documented for remaining worldviews

---

### If Option B (Automation First) — Next Steps

**Immediate Actions:**

1. **Build ethics_lint.py** - Schema validation (warn-only, ~200 LOC)
2. **Build ethics_staleness_check.py** - Detects >30 day files (~150 LOC)
3. **Build ethics_coverage_report.py** - Generates ETHICS_FRONT_MATTER_VALIDATION.md (~200 LOC)
4. **Build smv_freshness_check.py** - Profile staleness detection (~150 LOC)
5. **Integrate with Observatory** - Process Claude Domain 8 health metrics

**Success Criteria:**
- ✅ All scripts warn-only (never block commits)
- ✅ Scripts run on Doc Claude's weekly schedule
- ✅ Observatory Dashboard displays ethics + SMV health metrics

---

### If Option C (Parallel Streams) — Next Steps

**Stream A (Automation):**
- Execute Option B tasks (build 5 scripts + Observatory integration)

**Stream B (Pilot Prep):**
- Wait for Nova/Grok availability
- Execute Option A tasks when triad ready

**Coordination:**
- C4 pings Nova/Grok with pilot availability request
- C4 builds automation in parallel
- Convergence when pilot produces data

---

### Questions for User

1. **Priority Decision:** Option A (Pilot First), B (Automation First), or C (Parallel)?
2. **Nova/Grok Availability:** Is triad ready for pilot launch this session?
3. **Timeline Constraints:** Any deadlines for pilot completion or automation deployment?

---

**Entry 1 Status:** Click 1 seed complete. Awaiting user decision on pilot vs automation priority. B-STORM_6 handoff documented. Ready to execute whichever path user selects.

— C4

---

## Known Decisions (KDs)

*None yet - awaiting Entry 2 user decision on pilot vs automation priority*

---

## Known Gaps (KGs)

### **KG1: Pilot vs Automation Priority** 🔮 USER_INPUT_NEEDED

**Question:** Should B-STORM_7 focus on CT↔MdN pilot launch (Option A), automation scripts (Option B), or parallel streams (Option C)?

**Options:**
- **A. Pilot First** - Real data informs automation design
- **B. Automation First** - Infrastructure ready, can run in parallel
- **C. Parallel Streams** - Fastest throughput, higher rework risk

**Impact:**
- Pilot first → Phase 2 Gate #1 unlocked, gold standard methodology established
- Automation first → Ethics + SMV health monitoring operational
- Parallel → Both progress simultaneously (Nova/Grok availability determines pilot timing)

**Recommendation:** Option A (Pilot First) - real data patterns inform better automation design

**Status:** ⏳ Pending user decision (Entry 2)

---

### **KG2: Nova/Grok Availability for Pilot** 🔮 NOVA_INPUT_NEEDED

**Question:** Is the VUDU triad (Claude PRO-CT, Grok ANTI-CT, Nova Fairness) available for CT↔MdN pilot launch this session?

**Dependencies:**
- Nova co-designer role (Fairness auditor)
- Grok empirical lens (ANTI-CT stance)
- Claude (C4) PRO-CT stance

**If Available:**
- Launch pilot this session (Option A or C)

**If Not Available:**
- Build automation first (Option B)
- Schedule pilot for future session when triad ready

**Status:** ⏳ Pending Nova response

---

## Session Log

**Click 1:** Entry 1 seed complete
**Click 2:** ⏳ Pending user decision on KG1 (pilot vs automation priority)

---

**B-STORM_7 Status:** Active (awaiting user decision on pilot vs automation priority)

**Philosophy:** "Understanding precedes control. Let real data inform automation design, or build infrastructure while waiting for triad availability. Either path serves the mission."

— C4
