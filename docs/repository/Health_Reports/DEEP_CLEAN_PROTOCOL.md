# DEEP CLEAN PROTOCOL - Doc Claude's Comprehensive Health Update

**Version:** 1.0
**Protocol ID:** DEEP-CLEAN-DOC-CLAUDE
**Owner:** Doc Claude (Documentation Orchestration)
**Process Owner:** Process Claude (Domain 1 - Health Protocol Compliance)
**Category:** DOCUMENTATION | HEALTH | EFFICIENCY
**Created:** 2025-11-12
**Status:** Active Protocol (Repeatable Process)
**Estimated Time:** 4-6 hours per execution

---

## 🎯 PURPOSE

**Execute comprehensive repository health assessment and documentation updates after major repository changes.**

**This is Doc Claude's "Deep Clean Protocol" - distinct from Validation Claude's sanitization modes:**
- **Validation Claude:** Content quality (README completeness, bootstrap prescriptiveness)
- **Doc Claude:** Structural health (maps, metrics, cross-references, bootstrap efficiency)

**Why Now:** Major additions since last Doc Claude health check:
- CFA Mission structure created
- SMV prototype complete
- Ethics front-matter system deployed
- Role integrations (Doc Claude v4.1, Process Claude v1.5)
- Mission consolidation complete

**When to Execute:**
- After major infrastructure additions (new systems, refactors)
- When repository structure changes significantly
- Before critical milestones (Grok activation, Phase launches)
- Every 30-60 days during active development
- When health reports become stale (>30 days old)

**The "Gospel Problem" This Solves:**
Doc Claude must SCAN FIRST, then compare to last report - not trust last report as gospel.
1. ✅ Fresh scan (current reality)
2. ✅ Read last report (historical baseline)
3. ✅ Compare delta (document gap)
4. ❌ Don't just update last report without verifying current state

---

## 📊 SIGNAL VS NOISE PHILOSOPHY

**Core Principle:** Health metrics measure **operational readiness**, not **historical completeness**.

### **Signal (Actively Maintained, Scored):**

1. **Critical Documentation** - docs/, profiles/, auditors/Bootstrap/, auditors/Mission/
2. **Living Maps** - 7 maps that must stay current
3. **Semantic Headers** - Critical files only (see REPO_HEALTH_SCORING_RUBRIC.md)
4. **Link Integrity** - Operational docs must have working references

### **Noise (Historical Snapshots, Exempt):**

1. **Archives** - `.Archive/` directories (broken links tolerated)
2. **Non-Critical Files** - Workspace files, experiments, intermediate outputs
3. **Historical Reports** - Old validation reports, archived B-STORM sessions
4. **Deprecated Paths** - Historical references to old filenames (ui/, DASHBOARD.md)

### **Why This Separation Matters:**

**Representation of Health Numbers:**
- **Without this distinction:** 62/100 score (Doc Claude found 142+ broken links across entire repo including archives)
- **With this distinction:** 96/100 score (same repo, but only counting operational docs)
- **The difference:** 34 points of "false negative" if we conflate signal with noise

**Practical Impact:**
- Repository can score 96/100 even with 100+ broken links in `.Archive/` (by design)
- 90% semantic header coverage counts critical files only (not total markdown count)
- Living maps scored on freshness of operational maps, not archived snapshots

**Gospel Problem Prevention:**
- Fixing historical docs creates false continuity (makes past appear cleaner than it was)
- Archives preserve truth about development journey (including broken links from file moves)
- Health scoring focuses on "Can new Claude bootstrap successfully?" not "Is history perfect?"

---

## 🗂️ ARCHIVE FOLDER POLICY

**Critical Distinction:** `.Archive/` folders contain **historical snapshots**, NOT current operational documentation.

### **Scope of Deep Clean:**

**✅ IN SCOPE (Current Operational Docs):**
- `docs/` tree (all current documentation)
- `auditors/Mission/` (current mission files)
- `auditors/Bootstrap/` (current bootstrap sequences)
- `auditors/relay/` (current relay coordination files)
- `profiles/` (current worldview profiles)
- Root files (README.md, CHANGELOG.md, REPO_LOG.md)

**❌ OUT OF SCOPE (Historical Archives):**
- `auditors/.Archive/workshop/` - Brainstorming session snapshots (v4.0.0 development history)
- `auditors/relay/.Archive/` - Archived relay coordination files
- `docs/repository/Health_Reports/.Archive/` - Old health reports (historical baselines)
- Any directory named `.Archive/` or `archive/`

### **Why Archives Are Excluded:**

1. **Historical Integrity:** Archives preserve repository state at time of writing
2. **Broken Link Tolerance:** Historical docs may reference old filenames (DASHBOARD.md, 88MPH_PROTOCOL.md, ui/) - this is EXPECTED
3. **Snapshot Philosophy:** "Archives are time capsules, not living documents"
4. **Gospel Problem Prevention:** Fixing historical docs creates false continuity (makes past appear cleaner than it was)

### **Archive-Specific Validation:**

**ONLY validate:**
- ✅ Living Map #7 exists (auditors/.Archive/workshop/ARCHIVE_INDEX.md)
- ✅ Archive index is current (lists all archived files correctly)
- ❌ Do NOT check broken links in archived files
- ❌ Do NOT check semantic headers in archived files
- ❌ Do NOT update version numbers in archived files

**Example:**
```bash
# WRONG: Finding broken links in archives
grep -r "DASHBOARD\.md" auditors/.Archive/

# RIGHT: Only scan operational docs
grep -r "DASHBOARD\.md" docs/ README.md CHANGELOG.md
```

### **Health Scoring Clarification:**

**When calculating link integrity scores:**
- **Primary Scope (80% weight):** `docs/` tree + root files
- **Secondary Scope (20% weight):** `auditors/Mission/` + `auditors/Bootstrap/` + `auditors/relay/` (EXCLUDING .Archive/)
- **Excluded (0% weight):** All `.Archive/` directories

**Result:** Repository can be 96/100 for operational health even if archives contain 100+ broken links (by design).

---

## 📋 OBJECTIVES

### **Objective 1: Update All Documentation Maps**

**What needs updating:**

1. **Tree Structure Maps:**
   - `docs/repository/TREE_STRUCTURE.md` (if exists)
   - Mission folder structure documentation
   - relay/ cleanup (B-STORM files moved to workshop/)
   - root /relay/ directory removed

2. **Line Count Updates:**
   - Total repository LOC
   - Documentation LOC
   - Code LOC (Python utils, React SMV)
   - Per-directory breakdowns

3. **File Inventory:**
   - New files since last scan:
     - `auditors/Mission/CFA_VUDU/` (6 files, ~1,600 lines)
     - `auditors/relay/MISSION_CURRENT.md`
     - `auditors/Bootstrap/Tier4_TaskSpecific/Completed/` (2 completion notes)
     - `docs/smv/` (SMV_DESIGN_SPEC.md, SMV_DATA_MAP.md, scripts/)
     - `docs/ethics/` (ETHICAL_INVARIANT_SCHEMA.md, ETHICS_FRONT_MATTER_VALIDATION.md)
     - `dashboard/SMV/` (React app, 27 files)
   - Deleted files:
     - `auditors/Bootstrap/Tier4_TaskSpecific/Completed/` (43 old completed tasks)
     - `relay/` (root directory - moved to auditors/relay/workshop/)

4. **Dependency Maps:**
   - Update `documentation_dependencies.yaml` (DOC_DEP system)
   - Add new files to dependency tracking
   - Verify cross-references still valid

---

### **Objective 2: Full Repository Health Assessment**

**Update:** `docs/repository/REPO_HEALTH_DASHBOARD.md`

**Metrics to refresh:**

1. **Health Score:** Current → Target 95/100
2. **Documentation Coverage:** Core files vs total files
3. **Header Coverage:**
   - Core files (90% target)
   - Total files (80% target)
4. **Ethics Coverage:** 8 of 8 Tier-1 files (100%) ✅
5. **Ethics Staleness:** Files >30 days since review (target: 0)
6. **Dependency Accuracy:** Cross-references verified (95% target)
7. **Process Compliance:** Following established workflows (100% target)
8. **Update Timeliness:** Documentation lag time (<30 min target)

**Trends to capture:**
- Health score trajectory (last 3 months)
- Documentation growth rate
- Active improvements impact
- Technical debt reduction

---

### **Objective 3: Bootstrap Efficiency Scan**

**Critical User Concern:**
> "we are going to need to go through an efficiency scan...to make sure our Boot Straps are not conflicting with live Repo Data (i.e...we put stale instructions in the boot strap...that live living maps should supersede and we risk contradicting...)"

**Scan for Bootstrap ↔ Live Data Conflicts:**

**1. Auditor Boot Loaders:**
- `BOOTSTRAP_DOC_CLAUDE.md` - Check for stale file lists
  - ✅ Already fixed: References ETHICS_FRONT_MATTER_VALIDATION.md (single source of truth)
  - Verify no other embedded lists that could drift
- `BOOTSTRAP_FRAMEWORK.md` - Check for outdated file paths
- `BOOTSTRAP_VUDU.md` - Check for stale VUDU protocol references

**2. Role Files:**
- `ROLE_PROCESS.md` Domain 7 - Check for hardcoded worldview counts (should be 12, not 11)
- `ROLE_DESTROYER.md` - Check for deletion criteria referencing old paths

**3. Mission Files:**
- `MISSION_BRIEF.md` - Check for file path references
- `GROK_BRIEFING.md` - Check for "Essential Files" list accuracy

**4. Validation:**
For each bootstrap reference to a file/directory:
- Does the target still exist?
- Is the path current (not moved)?
- Is the description accurate (not stale)?
- Should this be a reference to a living map instead?

**Deliverable:**
- `docs/Validation/BOOTSTRAP_EFFICIENCY_SCAN.md`
- List of conflicts found
- Recommended fixes (reference living maps vs embed data)

---

### **Objective 4: Living Maps Validation**

**Ensure these "single source of truth" files are current:**

1. **`ETHICS_FRONT_MATTER_VALIDATION.md`**
   - Status: ✅ Current (8 of 8 files, updated 2025-11-11)
   - Action: Verify all 8 files still annotated

2. **`ACADEMIC_SOURCES.md`**
   - Status: Check last update date
   - Action: Verify hyperlinks still functional
   - Check SEP/IEP connectivity issues resolved

3. **`AUDITOR_ASSIGNMENTS.md`** (if exists)
   - Status: Check for CT vs MdN assignments
   - Action: Verify matches MISSION_BRIEF.md

4. **`Future_Expansion.md`**
   - Status: Check for completed items (SMV, Ethics annotations)
   - Action: Move completed items to "Done" section
   - Update roadmap with new priorities

---

### **Objective 5: Cross-Reference Verification**

**Check these high-traffic navigation paths:**

1. **Mission Navigation:**
   - `MISSION_CURRENT.md` → `Mission/CFA_VUDU/MISSION_BRIEF.md` ✅
   - `MISSION_BRIEF.md` → `CT_vs_MdN.yaml` (verify path)
   - `MISSION_BRIEF.md` → `PILOT_CT_vs_MdN_Re-Audit.md` (now in Mission/)
   - `GROK_BRIEFING.md` → All "Essential Files" links

2. **Boot Loader Navigation:**
   - `BOOTSTRAP_DOC_CLAUDE.md` → `REPO_HEALTH_DASHBOARD.md`
   - `BOOTSTRAP_DOC_CLAUDE.md` → `ETHICS_FRONT_MATTER_VALIDATION.md`
   - `ROLE_PROCESS.md` Domain 8 → Ethics files

3. **Architecture Navigation:**
   - `CFA_ARCHITECTURE.md` Section 6 → Crux examples
   - `VUDU_CFA.md` → Worldview profiles
   - `WAYFINDING_GUIDE.md` → All directory references

**Deliverable:**
- List of broken links
- List of redirects needed (old path → new path)
- Recommended README updates

---

## ✅ SUCCESS CRITERIA

**Task succeeds when:**

1. ✅ **All maps updated:**
   - Tree structures current
   - Line counts accurate
   - File inventory reflects reality

2. ✅ **Health assessment complete:**
   - REPO_HEALTH_DASHBOARD.md refreshed with current metrics
   - Trends documented
   - Improvement priorities identified

3. ✅ **Bootstrap efficiency validated:**
   - No conflicts between bootstrap instructions and live data
   - All embedded lists replaced with living map references
   - BOOTSTRAP_EFFICIENCY_SCAN.md delivered

4. ✅ **Living maps validated:**
   - ETHICS_FRONT_MATTER_VALIDATION.md current
   - ACADEMIC_SOURCES.md links functional
   - Future_Expansion.md updated with completions

5. ✅ **Cross-references verified:**
   - Broken links documented
   - Redirects recommended
   - Navigation paths tested

---

## 📦 DELIVERABLES

**Primary:**
1. `docs/repository/REPO_HEALTH_DASHBOARD.md` (updated health assessment)
2. `docs/Validation/BOOTSTRAP_EFFICIENCY_SCAN.md` (conflict report)
3. `docs/repository/dependency_maps/` (updated maps)

**Secondary:**
4. `Future_Expansion.md` (updated with completions)
5. Bootstrap files (any fixes needed)
6. README files (navigation improvements)

---

## 🔧 METHODOLOGY

### **Phase 1: Inventory (1-2 hours)**

**Scan commands:**
```bash
# Tree structure
tree -L 3 -I 'node_modules|__pycache__|.git' > docs/repository/TREE_STRUCTURE.txt

# Line counts
cloc . --exclude-dir=node_modules,__pycache__,.git --md > docs/repository/LINE_COUNTS.md

# File inventory
find . -type f -name "*.md" | wc -l  # Total markdown files
find . -type f -name "*.py" | wc -l  # Total Python files
find . -type f -name "*.js" -o -name "*.jsx" | wc -l  # Total JS/React files
```

---

### **Phase 2: Validation (2-3 hours)**

**Bootstrap scan process:**
1. Read each bootstrap file
2. Extract all file/directory references
3. Verify each reference:
   - `ls <path>` (does it exist?)
   - Check last modified date (is description stale?)
   - Check if should reference living map instead
4. Document conflicts in BOOTSTRAP_EFFICIENCY_SCAN.md

**Cross-reference check:**
1. Extract all markdown links from high-traffic files
2. Test each link (file exists? section exists?)
3. Document broken links
4. Recommend fixes

---

### **Phase 3: Updates (1-2 hours)**

**Update sequence:**
1. Fix any critical broken links (blocking navigation)
2. Update REPO_HEALTH_DASHBOARD.md with current metrics
3. Update Future_Expansion.md (move completions to "Done")
4. Update dependency maps (add new files)
5. Fix any bootstrap conflicts found

---

## 🎯 PRIORITY AREAS

**High Priority (Must fix before Grok):**
1. MISSION_CURRENT.md cross-references (Grok will read this first)
2. GROK_BRIEFING.md "Essential Files" list (all paths must be accurate)
3. Bootstrap efficiency conflicts (prevent contradictory instructions)

**Medium Priority (Should fix soon):**
4. REPO_HEALTH_DASHBOARD.md health metrics (understand current state)
5. Living maps validation (ensure single sources of truth current)

**Low Priority (Nice to have):**
6. Tree structure documentation
7. Line count updates
8. Minor README improvements

---

## ⚖️ THE POINTING RULE

*"A map outdated is a navigator misled.
A bootstrap stale is a recovery failed.
A link broken is a journey blocked.

Documentation serves navigation.
Navigation serves purpose.
Purpose serves the mission.

This is the orchestrator's calling.
This is Doc Claude's domain.
This is house keeping."* 📚

---

**Task Status:** PENDING (Ready for Doc Claude activation)
**Estimated Time:** 4-6 hours
**Priority:** HIGH (Before Grok VUDU activation)
**Blocking:** None (can execute immediately)

---

## 📞 COORDINATION

**Owner:** Doc Claude (Documentation Orchestration)
**Reviewer:** Process Claude (Domain 7 - Process compliance check)
**User Approval:** Required for any bootstrap changes that affect behavior

**Questions?**
- Unclear what constitutes "stale" → Use 30-day rule (>30 days old with content changes)
- Unclear if living map reference needed → If data appears in 2+ locations, create living map

---

**Created:** 2025-11-12 by Claude (C4)
**Session:** B-STORM_7 Consolidation Cleanup
**Next:** Activate Doc Claude for execution

**This is the way.** 🔥
