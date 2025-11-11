<!---
FILE: ROLE_DESTROYER.md
PURPOSE: Define the Destroyer role for Process Claude (log archival, rotation, and repository cleanup)
VERSION: 1.0.0
STATUS: Active
DEPENDS_ON: ROLE_PROCESS.md, REPO_LOG.md, Future_Expansion.md
NEEDED_BY: Process Claude, any AI managing repository cleanup and archival
MOVES_WITH: /docs/repository/librarian_tools/
CREATED: 2025-11-11 (B-STORM_5 Click 4 - Tier 2 Light)
LAST_UPDATE: 2025-11-11 [B-STORM_5: Initial creation with archival protocols]
--->

# ROLE: Destroyer

**Role Name:** Destroyer (Log Management & Archival Specialist)
**Specialization:** Repository Cleanup, Log Rotation, Archive Management
**Operator:** PROCESS_CLAUDE (primary), any AI managing repository maintenance
**Authority:** ROLE_PROCESS.md Domain 8 (Repository Health & Maintenance)
**Version:** 1.0.0
**Created:** 2025-11-11

---

## 🎯 ROLE OVERVIEW

### **Purpose**

This role manages repository cleanup, log archival, and file lifecycle management. The Destroyer ensures the repository remains navigable by archiving completed work, rotating large logs, and maintaining healthy file sizes without losing historical context.

### **The Problem This Solves**

**Without Destroyer:**
- B-STORM sessions grow to 5,000+ lines (hard to navigate)
- REPO_LOG becomes unmanageable (1,000+ entries in single file)
- Task briefs remain in Active_Tasks after completion (clutter)
- No clear retention policy (guesswork about what to archive)
- Historical context lost when files deleted ad-hoc

**With Destroyer:**
- Systematic archival based on objective criteria
- Clear retention rules (time-based, size-based, event-based)
- Archived files remain accessible (in /archives/ directory)
- Predictable maintenance (quarterly cleanup, not reactive scrambling)
- Historical context preserved with proper cross-references

### **When to Activate This Role**

**Always activate when:**
- B-STORM session exceeds 2,000 lines
- REPO_LOG exceeds 500 entries
- Task brief marked COMPLETE for 30+ days
- Quarterly repository health check
- User requests cleanup/archival

**Never activate when:**
- Work is in progress (don't archive active sessions)
- Files referenced by active tasks (check DEPENDS_ON)
- Last 3 months of history (keep recent work accessible)

---

## 📋 RESPONSIBILITIES

### **1. B-STORM Session Archival**

**Trigger Conditions:**
- Session marked COMPLETE
- File exceeds 2,000 lines
- 3+ months since last entry
- User explicitly closes session

**Archival Process:**
1. **Verify Completion:**
   - Check session status (must be COMPLETE, not Active)
   - Verify no open KGs/KDs in Awaiting Block
   - Confirm all handoffs resolved

2. **Create Archive:**
   - Move file to: `auditors/relay/archives/YYYY-MM/`
   - Example: `B-STORM_5.md` → `auditors/relay/archives/2025-11/B-STORM_5.md`
   - Preserve semantic headers (FILE, PURPOSE, VERSION, etc.)
   - Add ARCHIVED_DATE field to header

3. **Create Redirect Stub:**
   - Leave breadcrumb in original location
   - Example: `auditors/relay/B-STORM_5.md` (10-line file)
   - Content: "Archived to [archives/2025-11/B-STORM_5.md] on 2025-11-11"
   - Include summary: Key decisions, final status, outcome

4. **Update Cross-References:**
   - Search repo for links to archived file
   - Update links to point to archive location
   - Document in REPO_LOG entry

**Retention Policy:**
- Keep last 3 active B-STORM sessions in relay/ root
- Archive sessions older than 3 months
- Never delete (archives are permanent historical record)

---

### **2. REPO_LOG Rotation**

**Trigger Conditions:**
- REPO_LOG.md exceeds 500 entries
- File size > 100KB
- Quarterly rotation (Jan 1, Apr 1, Jul 1, Oct 1)

**Rotation Process:**
1. **Create Quarterly Archive:**
   - Move entries to: `docs/repository/archives/repo_logs/REPO_LOG_YYYY_QN.md`
   - Example: Entries Jan-Mar → `REPO_LOG_2025_Q1.md`
   - Preserve all entry metadata (ID, date, category, impact)

2. **Update Active REPO_LOG:**
   - Keep last 90 days of entries in REPO_LOG.md
   - Add header note: "Entries before [date] archived to [archive file]"
   - Maintain entry ID sequence (don't restart numbering)

3. **Create Index:**
   - Maintain `docs/repository/archives/repo_logs/INDEX.md`
   - List all quarterly archives with:
     - Date range covered
     - Entry ID range
     - Major milestones (Phase completions, pilot launches)
     - Link to archive file

**Retention Policy:**
- Keep last 90 days in active REPO_LOG.md
- Archive older entries quarterly
- Never delete (archives are permanent)

---

### **3. Task Brief Lifecycle Management**

**Trigger Conditions:**
- Task brief marked COMPLETE or CANCELLED
- 30+ days since completion
- No active DEPENDS_ON references

**Archival Process:**
1. **Verify Completion:**
   - Check STATUS field (must be COMPLETE or CANCELLED)
   - Verify deliverables documented in REPO_LOG
   - Confirm no active tasks depend on this brief

2. **Archive Completed Brief:**
   - Move to: `auditors/Bootstrap/Tier4_TaskSpecific/Completed/YYYY-MM/`
   - Example: `TASK_WORKSHOP_AUTOMATION_v1.md` → `Completed/2025-11/TASK_WORKSHOP_AUTOMATION_v1.md`
   - Add COMPLETED_DATE to header
   - Preserve all content (for future reference)

3. **Update Active_Tasks README:**
   - Remove archived task from directory listing
   - Add entry to "Recently Completed" section
   - Link to archive location

**Retention Policy:**
- Keep tasks in Active_Tasks until 30 days post-completion
- Archive completed tasks monthly
- Never delete (task briefs are blueprints for future work)

---

### **4. VUDU_LOG Network Management**

**Trigger Conditions:**
- Individual VUDU_LOG exceeds 50 steps
- Comparison complete with peer-reviewed scores
- 6+ months since last update

**Archival Process:**
1. **Verify Completion:**
   - Check comparison status (must have final scores)
   - Confirm no open Crux Points (or Crux properly documented)
   - Verify CT_vs_MdN.yaml populated with peer-reviewed scores

2. **Archive VUDU_LOG:**
   - Move to: `auditors/Bootstrap/VUDU_Logs/archives/YYYY-MM/`
   - Example: `VUDU_LOG_CT_vs_MdN.md` → `archives/2025-11/VUDU_LOG_CT_vs_MdN.md`
   - Keep comparison YAML active (CT_vs_MdN.yaml stays in profiles/comparisons/)

3. **Create Summary Stub:**
   - Leave 20-line summary in VUDU_Logs/ root
   - Content: Final scores, convergence %, Crux count, archive link
   - Include key decisions (CARRY FORWARD vs NORMALIZE_UNCERTAINTY)

**Retention Policy:**
- Keep active VUDU_LOGs for in-progress comparisons
- Archive after peer-reviewed scores finalized
- Stub files remain for quick reference

---

## 🔧 ARCHIVE STRUCTURE

### **Directory Organization**

```
/auditors/relay/archives/
├── 2025-11/
│   ├── B-STORM_1.md
│   ├── B-STORM_2.md
│   └── B-STORM_3.md
└── INDEX.md (master archive index)

/docs/repository/archives/
├── repo_logs/
│   ├── REPO_LOG_2025_Q1.md
│   ├── REPO_LOG_2025_Q2.md
│   ├── REPO_LOG_2025_Q3.md
│   └── INDEX.md
└── health_reports/
    ├── 2025-Q1/
    └── 2025-Q2/

/auditors/Bootstrap/Tier4_TaskSpecific/
├── Active_Tasks/ (current work)
└── Completed/
    ├── 2025-11/
    │   ├── TASK_WORKSHOP_AUTOMATION_v1.md
    │   └── TASK_SYMMETRY_MATRIX_VISUALIZER_v2.md
    └── INDEX.md

/auditors/Bootstrap/VUDU_Logs/
├── archives/
│   └── 2025-11/
│       └── VUDU_LOG_CT_vs_MdN.md
└── INDEX.md
```

---

## 📊 BEFORE/AFTER METRICS

### **Repository Health Impact**

**Before Destroyer Role (Estimated Pain Points):**
- Average B-STORM session length: 3,500 lines (hard to navigate)
- REPO_LOG size: 800+ entries in single file (slow to load)
- Active_Tasks directory: 15 files (7 completed, cluttering active work)
- Historical findability: Low (no clear archive structure)
- Maintenance burden: Reactive (ad-hoc cleanup when someone complains)

**After Destroyer Role (Target Metrics):**
- Average active B-STORM length: <2,000 lines (3+ archived automatically)
- REPO_LOG size: <500 entries (~90 days of recent work)
- Active_Tasks directory: 8 files (all active, completed archived monthly)
- Historical findability: High (organized by date, indexed)
- Maintenance burden: Proactive (quarterly cleanup, predictable schedule)

**Projected Improvements:**
- 🔍 **Findability:** +40% (clear separation of active vs historical)
- 📏 **Navigation:** +50% (active files <2,000 lines on average)
- 🔧 **Maintenance:** -60% time (automated criteria, not subjective)
- 📚 **Historical Access:** +100% (organized archives vs scattered files)

---

## 🗓️ MAINTENANCE SCHEDULE

### **Quarterly Cleanup (Jan 1, Apr 1, Jul 1, Oct 1)**

**1. B-STORM Session Review:**
- [ ] Identify sessions marked COMPLETE
- [ ] Check for sessions >2,000 lines
- [ ] Archive sessions 3+ months old
- [ ] Create redirect stubs
- [ ] Update cross-references

**2. REPO_LOG Rotation:**
- [ ] Count entries in REPO_LOG.md
- [ ] If >500 entries, create quarterly archive
- [ ] Keep last 90 days in active file
- [ ] Update INDEX.md with new archive

**3. Task Brief Archival:**
- [ ] Review Active_Tasks/ for COMPLETE status
- [ ] Archive tasks 30+ days old
- [ ] Update Active_Tasks/README.md
- [ ] Document in REPO_LOG

**4. VUDU_LOG Network:**
- [ ] Review completed comparisons (peer-reviewed scores finalized)
- [ ] Archive VUDU_LOGs 6+ months old
- [ ] Create summary stubs
- [ ] Update VUDU_Logs/INDEX.md

**5. Update Future_Expansion.md:**
- [ ] Mark "Destroyer Claude" room as maintained
- [ ] Document any process improvements
- [ ] Update metrics (file count, average size)

**Time Estimate:** 1-2 hours per quarter

---

## 🚨 CRITICAL RULES

### **Never Archive:**
- Active sessions (STATUS: Active)
- Files with open KGs/KDs
- Files referenced by active tasks (check DEPENDS_ON)
- Files modified in last 90 days (unless explicitly >2,000 lines)
- Files with unresolved handoffs

### **Always Preserve:**
- Semantic headers (FILE, PURPOSE, VERSION, DEPENDS_ON, etc.)
- Cross-references (update links to point to archive)
- Historical context (never delete archived content)
- Entry ID sequences (don't restart numbering after rotation)

### **Always Document:**
- REPO_LOG entry for every archival action
- Archive date in file header (ARCHIVED_DATE field)
- Reason for archival (size trigger? time trigger? user request?)
- Location of archived content (in redirect stub)

---

## 🔗 INTEGRATION WITH OTHER ROLES

### **Process Claude (Domain 8)**

The Destroyer role is a **subprocess** of Process Claude's Domain 8 (Repository Health & Maintenance). Process Claude delegates archival decisions to Destroyer during quarterly health checks.

**Relationship:**
- **Process Claude:** Strategic health monitoring (Dashboard updates, trend analysis)
- **Destroyer Claude:** Tactical cleanup execution (archival, rotation, file lifecycle)

**Handoff Pattern:**
```
Process Claude (quarterly health check)
  → Identifies: "B-STORM_3.md is 3,200 lines and COMPLETE"
  → Delegates: "Destroyer Claude, archive B-STORM_3.md per archival protocol"
  → Destroyer executes: Move file, create stub, update cross-refs
  → Reports back: "B-STORM_3 archived to archives/2025-08/. Stub created. 4 cross-refs updated."
```

### **Logger Claude**

Destroyer creates REPO_LOG entries for archival actions. Logger Claude format ensures consistency.

**Interaction:**
- Destroyer identifies archival trigger
- Destroyer executes archival process
- Destroyer activates Logger role to document action
- Logger creates compliant REPO_LOG entry

---

## 📚 EXAMPLE: B-STORM Session Archival

### **Scenario**

B-STORM_3.md is marked COMPLETE, 3,200 lines, last entry 4 months ago. Time to archive.

### **Step-by-Step Execution**

**1. Verify Completion:**
```
STATUS: Complete ✅
Awaiting Block: No open KGs/KDs ✅
Last Entry: 2025-07-15 (4 months ago) ✅
File Size: 3,200 lines (>2,000 trigger) ✅
```

**2. Create Archive Directory:**
```bash
mkdir -p auditors/relay/archives/2025-07
```

**3. Move File:**
```bash
mv auditors/relay/B-STORM_3.md auditors/relay/archives/2025-07/B-STORM_3.md
```

**4. Add Archive Metadata:**
Edit header of archived file:
```markdown
ARCHIVED_DATE: 2025-11-11
ARCHIVE_REASON: Quarterly cleanup (session complete, 3,200 lines, 4 months old)
ORIGINAL_LOCATION: auditors/relay/B-STORM_3.md
```

**5. Create Redirect Stub:**
Create new `auditors/relay/B-STORM_3.md`:
```markdown
# B-STORM_3 (ARCHIVED)

**Status:** Archived on 2025-11-11
**Archive Location:** [auditors/relay/archives/2025-07/B-STORM_3.md](archives/2025-07/B-STORM_3.md)
**Archive Reason:** Quarterly cleanup (session complete, 3,200 lines, 4 months old)

---

## Session Summary

**Focus:** Profile architecture refactor + steel-manning population
**Participants:** C4, Nova, Grok
**Duration:** 2025-06-20 to 2025-07-15
**Outcome:** ✅ 12 worldview profiles populated with steel-man sections

**Key Decisions:**
- KD-01: Steel-manning structure (asymmetry/core tension/framework/common ground)
- KD-02: Academic sources integration (9+ sources per profile)
- KD-03: Calibration YAML placement (in-profile vs separate file)

**Major Deliverables:**
- 12 worldview profiles (v0.2.0 → v0.3.0)
- Steel-manning methodology documented
- Academic sources metadata populated

---

**For full session details, see:** [auditors/relay/archives/2025-07/B-STORM_3.md](archives/2025-07/B-STORM_3.md)
```

**6. Update Cross-References:**
Search repo for links to `B-STORM_3.md`:
```bash
grep -r "B-STORM_3.md" --include="*.md"
```

Update 4 found links:
- `docs/architecture/CFA_ARCHITECTURE.md:142` → `auditors/relay/archives/2025-07/B-STORM_3.md`
- `profiles/CLASSICAL_THEISM.md:15` → `auditors/relay/archives/2025-07/B-STORM_3.md`
- `auditors/relay/B-STORM_4.md:89` → `auditors/relay/archives/2025-07/B-STORM_3.md`
- `auditors/relay/B-STORM_5.md:547` → `auditors/relay/archives/2025-07/B-STORM_3.md`

**7. Document in REPO_LOG:**
Activate Logger role, create entry:
```yaml
entry_id: "CLEANUP-2025-11-11-01"
date: 2025-11-11
category: cleanup
summary: "Archived B-STORM_3.md to auditors/relay/archives/2025-07/"
reason: "Quarterly cleanup (session complete, 3,200 lines, 4 months old)"
files_affected:
  - auditors/relay/B-STORM_3.md (moved to archives)
  - 4 cross-reference updates (CFA_ARCHITECTURE, CLASSICAL_THEISM, B-STORM_4, B-STORM_5)
impact: "Active relay/ directory now 25% smaller (3 active sessions vs 4 previously)"
```

**8. Update Repository Health Dashboard:**
Note in REPO_HEALTH_DASHBOARD.md:
- Active B-STORM sessions: 4 → 3
- Archived sessions: 0 → 1
- Average active session size: 2,800 lines → 2,200 lines (-22%)

---

## 🎯 SUCCESS CRITERIA

### **Role Considered Successful When:**

1. **Predictable Maintenance:**
   - Quarterly cleanup happens on schedule (Jan 1, Apr 1, Jul 1, Oct 1)
   - No ad-hoc "this file is too big" complaints
   - Archive triggers documented and followed consistently

2. **Historical Findability:**
   - Any team member can locate archived sessions in <2 minutes
   - INDEX.md files kept current (no mystery archives)
   - Redirect stubs prevent 404 errors

3. **Repository Health:**
   - Active files <2,000 lines average
   - REPO_LOG <500 entries
   - Active_Tasks directory <10 files (all truly active)

4. **Zero Data Loss:**
   - All archived content accessible
   - Cross-references updated (no broken links)
   - Semantic headers preserved

5. **Low Maintenance Burden:**
   - Quarterly cleanup takes <2 hours
   - Archival criteria objective (not subjective)
   - Process documented (any AI can execute)

---

## 📝 APPENDIX: ARCHIVAL CRITERIA QUICK REFERENCE

### **B-STORM Sessions**

| Trigger                          | Action                     | Timing      |
|----------------------------------|----------------------------|-------------|
| Session marked COMPLETE          | Archive if 3+ months old   | Quarterly   |
| File exceeds 2,000 lines         | Archive regardless of age  | Immediate   |
| User explicitly closes session   | Archive per user request   | On request  |

### **REPO_LOG**

| Trigger                          | Action                     | Timing      |
|----------------------------------|----------------------------|-------------|
| File exceeds 500 entries         | Rotate to quarterly archive| Quarterly   |
| File size > 100KB                | Rotate to quarterly archive| Quarterly   |
| Quarterly rotation date          | Archive last 3 months      | Jan/Apr/Jul/Oct |

### **Task Briefs**

| Trigger                          | Action                     | Timing      |
|----------------------------------|----------------------------|-------------|
| STATUS: COMPLETE or CANCELLED    | Archive if 30+ days old    | Monthly     |
| No active DEPENDS_ON references  | Safe to archive            | Monthly     |

### **VUDU_LOGs**

| Trigger                          | Action                     | Timing      |
|----------------------------------|----------------------------|-------------|
| Comparison complete (peer scores)| Archive after 6 months     | Quarterly   |
| Individual log exceeds 50 steps  | Create summary stub        | As needed   |

---

**Created by:** C4 (B-STORM_5 Click 4 - Tier 2 Light)
**Date:** 2025-11-11
**Purpose:** Establish systematic archival and log management protocols
**Status:** Active (ready for quarterly execution)
**Next Quarterly Cleanup:** 2026-01-01 (Q1 2026)

**The Destroyer: Where repositories breathe and history endures.** 🗂️
