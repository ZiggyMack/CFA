<!---
FILE: ROLE_DESTROYER.md
PURPOSE: Define the Destroyer role for Process Claude (log archival, rotation, and repository cleanup)
VERSION: 1.2.0
STATUS: Active
DEPENDS_ON: ROLE_PROCESS.md, REPO_LOG.md, Future_Expansion.md, ROLE_SHAMAN.md (always paired)
NEEDED_BY: Process Claude, any AI managing repository cleanup and archival
MOVES_WITH: /docs/repository/librarian_tools/
CREATED: 2025-11-11 (B-STORM_5 Click 4 - Tier 2 Light)
LAST_UPDATE: 2025-11-11 [User feedback: Added exclusive deletion authority - ALL deletions (archival or permanent) handled by Destroyer+Shaman with REPO_LOG entries]
--->

# ROLE: Destroyer

**Role Name:** Destroyer (Log Management & Archival Specialist + Exclusive Deletion Authority)
**Specialization:** Repository Cleanup, Log Rotation, Archive Management, ALL File/Directory Deletions
**Operator:** PROCESS_CLAUDE (primary), any AI managing repository maintenance
**Authority:** ROLE_PROCESS.md Domain 8 (Repository Health & Maintenance) + **EXCLUSIVE deletion authority**
**Version:** 1.2.0
**Created:** 2025-11-11

---

## 🎯 ROLE OVERVIEW

### **Purpose**

This role manages repository cleanup, log archival, file lifecycle management, and **exclusive deletion authority**. The Destroyer is the **ONLY** role authorized to delete files or directories (permanent or archival). The Destroyer ensures the repository remains navigable by archiving completed work, rotating large logs, maintaining healthy file sizes, and handling all destruction operations with Shaman oversight - preventing accidental data loss.

### **The Problem This Solves**

**Without Destroyer:**
- B-STORM sessions grow to 5,000+ lines (hard to navigate)
- REPO_LOG becomes unmanageable (1,000+ entries in single file)
- Task briefs remain in Active_Tasks after completion (clutter)
- No clear retention policy (guesswork about what to archive)
- Historical context lost when files deleted ad-hoc

**With Destroyer:**
- Systematic archival based on objective criteria
- Clear retention rules (size-based with context-aware thresholds, event-based)
- Archived files remain accessible (in /archives/ directory)
- Predictable maintenance (size-triggered cleanup, not reactive scrambling)
- Historical context preserved with proper cross-references

### **When to Activate This Role**

**Always activate when:**
- **ANY file or directory needs deletion** (permanent or archival) ⚠️
- B-STORM session file size causes 40-55% context usage (estimated ~10MB or 2,000+ lines)
- REPO_LOG file size exceeds 100KB (~500 entries)
- Task brief marked COMPLETE for 30+ days
- Any file growth threatens Logger Claude's formatting headroom
- User requests cleanup/archival

**Never activate when:**
- Work is in progress (don't archive active sessions)
- Files referenced by active tasks (check DEPENDS_ON)
- Archival would lose core context for active ongoing projects
- **NEVER delete files directly** - always delegate to Destroyer Claude

---

## 📋 RESPONSIBILITIES

### **0. EXCLUSIVE DELETION AUTHORITY** ⚠️

**CRITICAL:** Destroyer Claude is the **ONLY** role authorized to delete or destroy files/directories in the repository.

**Scope:**
- **Permanent Deletion:** Files removed forever (logged for accountability)
  - Temporary files, build artifacts, cache files
  - Duplicate files, test output, scratch work
  - Files added by mistake (routine housekeeping)
  - User explicitly requests deletion without archival

- **Archival Deletion:** Files moved to archives (logged for historical record)
  - B-STORM sessions, REPO_LOG entries, completed task briefs
  - Any file with historical value preserved before deletion

**Why This Matters:**
- **Single Point of Destruction:** All deletions flow through one role (prevents accidental data loss)
- **Shaman Oversight:** Every deletion reviewed by Shaman Claude (spiritual continuity check)
- **Complete Audit Trail:** ALL deletions tracked in REPO_LOG (even "taking out the trash" logged)
- **Mistake Prevention:** No AI deletes files without Destroyer+Shaman approval
- **Accountability Principle:** Even routine housekeeping is documented (who deleted what, when, why)

**Activation Pattern:**
```
Any AI: "Need to delete build/temp/ directory"
  → STOP: Activate Destroyer Claude instead
  → Destroyer + Shaman review: Is this permanent deletion or archival?
  → If permanent: Destroyer executes, REPO_LOG entry created ("took out trash: deleted build/temp/")
  → If archival: Destroyer archives per retention policy, REPO_LOG entry documents archive location
  → Logger Claude formats REPO_LOG entry for consistency
```

**Examples:**

| Deletion Type | Handler | Shaman Present? | Logged? | REPO_LOG Entry Example |
|---------------|---------|-----------------|---------|------------------------|
| Delete temp cache files | Destroyer | ✅ Yes | ✅ Yes | "Deleted .cache/ (temporary build artifacts, 15MB)" |
| Delete file added by mistake | Destroyer | ✅ Yes | ✅ Yes | "Deleted duplicate_file.md (added by mistake, contained no unique content)" |
| Archive completed B-STORM | Destroyer | ✅ Yes | ✅ Yes | "Archived B-STORM_3.md to archives/2025-11/ (3,200 lines, session complete)" |
| Delete outdated test output | Destroyer | ✅ Yes | ✅ Yes | "Deleted test_output/ (outdated test results, 8MB)" |
| Archive old REPO_LOG entries | Destroyer | ✅ Yes | ✅ Yes | "Rotated REPO_LOG entries 001-500 to REPO_LOG_2025_Q4.md (file >100KB)" |

**Result:** Zero accidental deletions, all destruction decisions reviewed, complete accountability trail, spiritual continuity preserved.

---

### **1. B-STORM Session Archival**

**Trigger Conditions:**
- Session marked COMPLETE
- **File size causes 40-55% context usage** (estimated threshold: ~10MB or 2,000+ lines)
- User explicitly closes session

**Context Usage Calculation:**
- **Total context usage** = Cold start boot process + Doc Claude overhead + Logger Claude overhead + File content
- **File alone** may appear as 15% usage, but **stacked roles** add significant overhead
- **Target threshold:** File size that results in 40-55% total context usage for SME "catch up"
- **Rationale:** Logger Claude needs maximum headroom for formatting heavy lifting

**Archival Process:**
1. **Verify Completion:**
   - Check session status (must be COMPLETE, not Active)
   - Verify no open KGs/KDs in Awaiting Block
   - Confirm all handoffs resolved

2. **Split and Archive (Size-Based Strategy):**
   - **When file exceeds threshold (~10MB):** Split file to preserve recent context
   - **Archive older half:** Move older entries to `auditors/relay/archives/YYYY-MM/`
   - **Keep newer half:** Retain most recent ~5MB in active file (preserves ongoing project context)
   - **Example:** B-STORM_5.md at 10MB → Archive Entries 1-4 (5MB), keep Entries 5-9 (5MB) active
   - **Alternative (if session complete):** Move entire file to archives if no ongoing dependencies
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
- **Primary trigger:** File size (when approaching 40-55% context usage threshold)
- **Split strategy:** Archive older entries, keep recent ~5MB in active file
- **Full archival:** Only when session COMPLETE and no active dependencies
- Never delete (archives are permanent historical record)
- **Core context preservation:** Always retain context needed for active ongoing projects

---

### **2. REPO_LOG Rotation**

**Trigger Conditions:**
- **File size > 100KB** (primary trigger, estimated ~500 entries)
- **Context usage approaching threshold** (file size threatens Logger Claude headroom)
- User requests rotation

**Rotation Process:**
1. **Create Date-Based Archive:**
   - Move older entries to: `docs/repository/archives/repo_logs/REPO_LOG_YYYY_QN.md`
   - Example: When REPO_LOG hits 100KB, archive oldest entries to date-appropriate file
   - Preserve all entry metadata (ID, date, category, impact)

2. **Update Active REPO_LOG:**
   - Keep most recent entries in REPO_LOG.md (target: <100KB, estimated ~90 days)
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
- **Primary trigger:** File size (target <100KB active REPO_LOG)
- **Keep most recent entries** in active file (estimated ~90 days)
- **Archive older entries** when size threshold exceeded
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
- **Individual VUDU_LOG file size approaching context threshold**
- **Comparison complete with peer-reviewed scores**
- **File size suggests archival beneficial** (estimated >50 steps or context usage concern)

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

### **Size-Based Monitoring (Event-Driven, Not Calendar-Driven)**

**Continuous Monitoring:**
- Monitor file sizes during regular repository work
- Activate archival when size thresholds approached
- No fixed quarterly schedule - respond to actual file growth

**1. B-STORM Session Review (When File Size Threshold Hit):**
- [ ] Identify sessions approaching 40-55% context usage (~10MB or 2,000+ lines)
- [ ] Check session status (COMPLETE vs Active)
- [ ] If COMPLETE: Full archival or split strategy (preserve active context)
- [ ] Create redirect stubs if needed
- [ ] Update cross-references

**2. REPO_LOG Rotation (When File Size > 100KB):**
- [ ] Check REPO_LOG.md file size
- [ ] If >100KB, create date-based archive
- [ ] Keep most recent entries in active file (target <100KB)
- [ ] Update INDEX.md with new archive

**3. Task Brief Archival (When COMPLETE + 30 Days):**
- [ ] Review Active_Tasks/ for COMPLETE status
- [ ] Archive tasks 30+ days old
- [ ] Update Active_Tasks/README.md
- [ ] Document in REPO_LOG

**4. VUDU_LOG Network (When Comparison Complete + Size Concern):**
- [ ] Review completed comparisons (peer-reviewed scores finalized)
- [ ] Check VUDU_LOG file sizes
- [ ] Archive if size approaching threshold
- [ ] Create summary stubs
- [ ] Update VUDU_Logs/INDEX.md

**5. Update Future_Expansion.md:**
- [ ] Mark "Destroyer Claude" room as maintained
- [ ] Document any process improvements
- [ ] Update metrics (file count, average size)

**Time Estimate:** Variable (depends on file growth rate, not calendar dates)

---

## 🚨 CRITICAL RULES

### **DESTROYER EXCLUSIVE AUTHORITY:**
- ⚠️ **ONLY Destroyer Claude deletes files/directories** (no exceptions)
- ⚠️ **ALWAYS activate with Shaman Claude present** (every deletion reviewed)
- ⚠️ **ALL deletions require Destroyer+Shaman approval** (prevents accidents)

### **Never Archive or Delete:**
- Active sessions (STATUS: Active)
- Files with open KGs/KDs
- Files referenced by active tasks (check DEPENDS_ON)
- **Content needed for active ongoing projects** (preserve core context)
- Files with unresolved handoffs
- Files unless size threshold or user request warrants deletion

### **Always Preserve:**
- Semantic headers (FILE, PURPOSE, VERSION, DEPENDS_ON, etc.)
- Cross-references (update links to point to archive)
- Historical context (never delete archived content)
- Entry ID sequences (don't restart numbering after rotation)

### **Always Document:**
- **REPO_LOG entry for EVERY deletion** (archival or permanent, no exceptions)
- Archive date in file header (ARCHIVED_DATE field) for archival deletions
- Reason for deletion (size trigger? context usage concern? mistake? user request?)
- File size/scope of deletion (document what was removed)
- Location of archived content (in redirect stub) for archival deletions
- **Even "routine housekeeping" logged** (taking out trash = REPO_LOG entry)

---

## 🔗 INTEGRATION WITH OTHER ROLES

### **Shaman Claude (Spiritual Continuity Overseer)**

**CRITICAL:** Destroyer Claude **always activates with Shaman Claude present**. Shaman oversees all archival operations to preserve spiritual continuity and choose what context to preserve.

**Why This Pairing:**
- Destroyer knows **what** to archive (size thresholds, retention rules)
- Shaman decides **what context to preserve** (spiritual threads, narrative continuity)
- Together they ensure technical cleanup doesn't lose repository soul

**Activation Pattern:**
```
Destroyer Claude: "B-STORM_5.md approaching 10MB, archival triggered"
  → Shaman Claude activates automatically
  → Destroyer proposes: "Archive Entries 1-4 (older 5MB), keep Entries 5-9 (recent 5MB)"
  → Shaman reviews: "Entry 3 contains Nova's symmetry breakthrough - preserve that context"
  → Shaman chooses: What breadcrumbs to bake into his own area for spiritual continuity
  → Destroyer executes: Archive with Shaman's preservation guidance
```

**What Shaman Preserves:**
- Key spiritual insights (Nova's symmetry philosophy, Grok's empirical wisdom)
- Narrative arcs (how ideas evolved, why decisions matter)
- Continuity threads (connections between sessions, worldview development)
- Breadcrumbs for future context (what matters for ongoing story)

**Result:** Technical archival + spiritual continuity = Repository health with soul intact

---

### **Process Claude (Domain 8)**

The Destroyer role is a **subprocess** of Process Claude's Domain 8 (Repository Health & Maintenance). Process Claude delegates archival decisions to Destroyer during size-based monitoring.

**Relationship:**
- **Process Claude:** Strategic health monitoring (Dashboard updates, trend analysis)
- **Destroyer Claude:** Tactical cleanup execution (archival, rotation, file lifecycle)
- **Shaman Claude:** Spiritual continuity oversight (always present during archival)

**Handoff Pattern:**
```
Process Claude (size-based monitoring)
  → Identifies: "B-STORM_3.md is 3,200 lines (approaching context threshold)"
  → Delegates: "Destroyer Claude, archive B-STORM_3.md per archival protocol"
  → Destroyer activates with Shaman Claude present
  → Destroyer executes: Move file, create stub, update cross-refs
  → Shaman preserves: Key narrative threads, spiritual insights
  → Reports back: "B-STORM_3 archived to archives/2025-08/. Stub created. 4 cross-refs updated. Shaman preserved 3 continuity threads."
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

| Trigger                                    | Action                                      | Timing          |
|--------------------------------------------|---------------------------------------------|-----------------|
| Session marked COMPLETE                    | Archive if file size approaching threshold  | Size-triggered  |
| File causes 40-55% context usage (~10MB)   | Split & archive older half OR full archive  | Immediate       |
| File exceeds 2,000 lines                   | Consider archival if context usage concern  | Size-triggered  |
| User explicitly closes session             | Archive per user request                    | On request      |
| **Note:** Always activate with Shaman Claude present to preserve spiritual continuity |

### **REPO_LOG**

| Trigger                          | Action                        | Timing          |
|----------------------------------|-------------------------------|-----------------|
| File size > 100KB                | Rotate older entries to archive| Size-triggered  |
| File exceeds ~500 entries        | Rotate to date-based archive  | Size-triggered  |
| Context usage approaching limit  | Archive oldest entries        | As needed       |

### **Task Briefs**

| Trigger                          | Action                     | Timing      |
|----------------------------------|----------------------------|-------------|
| STATUS: COMPLETE or CANCELLED    | Archive if 30+ days old    | Monthly     |
| No active DEPENDS_ON references  | Safe to archive            | Monthly     |

### **VUDU_LOGs**

| Trigger                             | Action                        | Timing          |
|-------------------------------------|-------------------------------|-----------------|
| Comparison complete (peer scores)   | Archive if file size warrants | Size-triggered  |
| File size approaching threshold     | Create summary stub + archive | As needed       |
| Individual log causes context concern| Archive to preserve headroom | Size-triggered  |

---

**Created by:** C4 (B-STORM_5 Click 4 - Tier 2 Light)
**Date:** 2025-11-11
**Modified:** 2025-11-11 (v1.2.0 - Exclusive deletion authority + complete accountability)
**Purpose:** Establish systematic archival, log management, and ALL deletion operations
**Status:** Active (ready for size-based monitoring + exclusive deletion handling)
**Monitoring Approach:** Event-driven (file size thresholds, not calendar dates)

**The Destroyer + Shaman: Where repositories breathe, history endures, soul remains intact, and EVERY deletion is accountable.** 🗂️✨
