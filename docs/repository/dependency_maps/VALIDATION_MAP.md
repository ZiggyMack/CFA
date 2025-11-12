<!---
FILE: VALIDATION_MAP.md
PURPOSE: Systematic validation checklist for Validation Claude operations
VERSION: 1.0
STATUS: Active
DEPENDS_ON: DASHBOARD.md, MASTER_DEPENDENCY_MAP.md, REPO_LOG.md
NEEDED_BY: Validation Claude, auditors, quality assurance
MOVES_WITH: /docs/repository/dependency_maps/
LAST_UPDATE: 2025-11-02 [DOCUMENTATION-2025-11-02-05]
--->

# VALIDATION_MAP.md - Validation Claude's Systematic Checklist

**Purpose:** Comprehensive validation map ensuring no loops, stale references, or quality issues remain undetected
**Owner:** Validation Claude (Quality Assurance Role)
**Created:** 2025-11-02
**Status:** Active Validation Tool

---

## 🎯 **WHAT THIS MAP DOES**

**Problem this solves:**
- Doc Claude instances reporting already-completed items as pending
- Validation checks missing critical issues
- No systematic way to ensure all validation bases are covered
- Quality loops slipping through ad-hoc validation

**How this map helps:**
- **Structured checklist** - Never miss a validation category
- **Traceable validation** - Document what was checked and when
- **Loop detection** - Systematic identification of circular issues
- **Quality gates** - Clear pass/fail criteria for each check

---

## 📋 **VALIDATION CATEGORIES**

### **Category 1: Documentation Health**
**Purpose:** Detect stale documentation, outdated references, false positives

### **Category 2: Loop Detection**
**Purpose:** Identify circular dependencies, infinite redirects, contradictions

### **Category 3: Structural Integrity**
**Purpose:** Verify file organization, naming conventions, orphaned files

### **Category 4: Standards Compliance**
**Purpose:** Check adherence to semantic headers, deps tags, REPO_LOG protocol

### **Category 5: State Consistency**
**Purpose:** Validate version numbers, status fields, cross-document consistency

### **Category 6: Process Adherence**
**Purpose:** Verify git commit messages, branch naming, workflow compliance

---

## 🔍 **CATEGORY 1: DOCUMENTATION HEALTH**

### **Check 1.1: Stale Checklists**
**Risk:** Doc Claude instances report already-completed items as pending

**Validation Process:**
1. **Read DASHBOARD.md** - Check status updates section
2. **Read MASTER_DEPENDENCY_MAP.md** - Check issues section
3. **Read health reports** in `/docs/repository/health_reports/`
4. **Cross-reference with REPO_LOG.md** - Verify completion dates

**What to look for:**
- [ ] TODO items marked incomplete that are actually complete
- [ ] Issues listed without ✅ resolved markers
- [ ] Stale version numbers in status sections
- [ ] Completion dates that don't match REPO_LOG
- [ ] "Pending" status on archived/completed work

**Pass Criteria:**
- All completed items marked with ✅
- All stale checklists updated with STATUS UPDATE sections
- Health reports reflect current state (not past state)
- Cross-references between documents are consistent

**Fix Pattern:**
```markdown
Add STATUS UPDATE section at top of affected files:

## ⚠️ **STATUS UPDATE (v[X.X] - [DATE])**

**IMPORTANT: Issues documented below have been RESOLVED:**

✅ **RESOLVED:** [Issue] - [Status]
- Status: [Current state]
- Resolved: [Date]
- Location: [Path]
```

**Files to Check:**
- `/docs/repository/DASHBOARD.md`
- `/docs/repository/dependency_maps/MASTER_DEPENDENCY_MAP.md`
- `/docs/repository/health_reports/*.md`
- `/auditors/Bootstrap/Tier4_TaskSpecific/Active_Tasks/*.md`

**Last Validated:** 2025-11-02
**Status:** ✅ PASSING (stale checklists fixed)

---

### **Check 1.2: Broken Internal Links**
**Risk:** Documentation references that lead to 404s or wrong locations

**Validation Process:**
1. **Extract all markdown links** from documentation files
2. **Verify each link target exists** at specified path
3. **Check for case sensitivity issues** (validation/ vs Validation/)
4. **Verify anchor links** point to existing headings

**What to look for:**
- [ ] `[Link text](/path/to/file.md)` where path doesn't exist
- [ ] Case mismatches (docs/validation/ vs docs/Validation/)
- [ ] Anchor links `#heading` pointing to non-existent sections
- [ ] Relative paths that resolve incorrectly
- [ ] Links to moved/archived files without redirects

**Pass Criteria:**
- 100% of internal links resolve to existing files
- All anchor links point to existing headings
- Case sensitivity matches actual filesystem

**Fix Pattern:**
- Update links to correct paths
- Add redirects for moved files
- Fix case sensitivity issues
- Remove links to deleted files

**Files to Check:**
- All `/docs/**/*.md` files
- All `/auditors/**/*.md` files
- `README.md`, `README_C.md`, `MISSION_CURRENT.md`

**Last Validated:** [Not yet validated]
**Status:** ⏳ PENDING

---

### **Check 1.3: Outdated Version References**
**Risk:** Documentation claiming repository is at v3.7.0 when it's v3.8.0

**Validation Process:**
1. **Read VuDu_PROTOCOL.md** for current version
2. **Search all docs** for version references
3. **Verify consistency** across all files
4. **Check changelog** matches version claims

**What to look for:**
- [ ] Version numbers that don't match current version
- [ ] "Latest version is vX.X" claims that are outdated
- [ ] Changelog entries missing for version bumps
- [ ] README version badge showing wrong version

**Pass Criteria:**
- All version references consistent with VuDu_PROTOCOL.md
- Changelog entries exist for all version bumps
- No "current version" claims that are outdated

**Files to Check:**
- `/auditors/protocols/VuDu_PROTOCOL.md`
- `/docs/CHANGELOG.md`
- `README.md`
- `README_C.md`

**Last Validated:** [Not yet validated]
**Status:** ⏳ PENDING

---

## 🔄 **CATEGORY 2: LOOP DETECTION**

### **Check 2.1: Circular Dependency Loops**
**Risk:** File A depends on File B which depends on File A (infinite loop)

**Validation Process:**
1. **Extract all DEPENDS_ON fields** from semantic headers
2. **Build dependency graph** (File → Dependencies)
3. **Run cycle detection algorithm** (depth-first search)
4. **Report any circular dependencies** found

**What to look for:**
- [ ] A → B → A (simple 2-node cycle)
- [ ] A → B → C → A (3-node cycle)
- [ ] Longer chains that eventually loop back
- [ ] Self-dependencies (File depends on itself)

**Pass Criteria:**
- Zero circular dependencies detected
- All dependency chains terminate at leaf nodes
- Dependency graph is acyclic (DAG structure)

**Fix Pattern:**
- Break circular dependencies by introducing abstraction layer
- Refactor to one-way dependency flow
- Document justification if circular dependency is intentional

**Algorithm:**
```python
def detect_cycles(dependencies):
    visited = set()
    rec_stack = set()

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in dependencies.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True  # Cycle detected

        rec_stack.remove(node)
        return False

    for node in dependencies:
        if node not in visited:
            if dfs(node):
                return True
    return False
```

**Files to Check:**
- All files with semantic headers containing DEPENDS_ON
- `/docs/repository/dependency_maps/MASTER_DEPENDENCY_MAP.md`

**Last Validated:** [Not yet validated]
**Status:** ⏳ PENDING

---

### **Check 2.2: Infinite Redirect Chains**
**Risk:** Doc A says "See Doc B" → Doc B says "See Doc C" → Doc C says "See Doc A"

**Validation Process:**
1. **Search for "See [file]" patterns** in all docs
2. **Extract redirect chains** (A → B → C)
3. **Detect loops** where chain circles back
4. **Verify redirects terminate** at actual content

**What to look for:**
- [ ] "See X.md" → X.md says "See Y.md" → Y.md says "See X.md"
- [ ] More than 2 hops in a redirect chain
- [ ] Redirects to non-existent files
- [ ] Redirects to archived/deprecated files

**Pass Criteria:**
- No redirect chains longer than 2 hops
- No circular redirect loops
- All redirects terminate at active content
- Archived files don't redirect to each other

**Fix Pattern:**
- Replace redirect chains with direct links to final destination
- Remove circular redirects by consolidating content
- Update redirects from archived files to point to active content

**Files to Check:**
- All markdown files with "See", "Refer to", "Check" language
- `/auditors/relay/.Archive/*`
- `/auditors/.Archive/*`

**Last Validated:** [Not yet validated]
**Status:** ⏳ PENDING

---

### **Check 2.3: Contradictory State Claims**
**Risk:** File A says "Task complete" but File B says "Task pending"

**Validation Process:**
1. **Identify state-bearing fields** (STATUS, state:, progress:)
2. **Build state claim map** (Task → Claims about task)
3. **Detect contradictions** where same entity has conflicting states
4. **Verify against REPO_LOG** as source of truth

**What to look for:**
- [ ] DASHBOARD.md says "Complete" but task brief says "Pending"
- [ ] README_C.md says "Phase 3" but MISSION_CURRENT.md says "Phase 4"
- [ ] REPO_LOG shows completion but dependent docs don't reflect it
- [ ] Multiple files claiming different current states

**Pass Criteria:**
- All state claims consistent across documents
- REPO_LOG is the authoritative source for state
- Dependent documents updated when REPO_LOG changes
- No contradictory status fields for same entity

**Fix Pattern:**
- Use REPO_LOG as source of truth
- Update all dependent documents to match REPO_LOG
- Add cross-references to REPO_LOG entries for verification

**Files to Check:**
- `/REPO_LOG.md` (source of truth)
- `/docs/repository/DASHBOARD.md`
- `/README_C.md`
- `/auditors/Bootstrap/MISSION_CURRENT.md`
- Task briefs in Active_Tasks/

**Last Validated:** [Not yet validated]
**Status:** ⏳ PENDING

---

## 🏗️ **CATEGORY 3: STRUCTURAL INTEGRITY**

### **Check 3.1: Archive Naming Consistency**
**Risk:** Some archives use `_Archive`, others use `.Archive`, creates confusion

**Validation Process:**
1. **Find all directories with "archive" in name** (case-insensitive)
2. **Check naming convention** (_Archive vs .Archive vs archive/)
3. **Verify standardization** to approved pattern (.Archive)
4. **Check for orphaned archive folders**

**What to look for:**
- [ ] `_Archive/` directories (old convention)
- [ ] `archive/` directories (non-standard)
- [ ] Mixed naming within same directory level
- [ ] Empty archive directories
- [ ] Archives not documented in DASHBOARD.md

**Pass Criteria:**
- All archives use `.Archive` naming convention (dot prefix)
- Zero instances of `_Archive` or `archive/` naming
- All archives documented in structure docs
- No empty archive directories

**Fix Pattern:**
```bash
# Standardize to .Archive naming
mv Folder/_Archive Folder/.Archive
git add Folder/.Archive
git commit -m "Standardize: Rename _Archive to .Archive"
```

**Files to Check:**
- `/auditors/relay/.Archive/`
- `/auditors/.Archive/`
- `/auditors/Mission/.Archive/`
- All subdirectories

**Last Validated:** 2025-11-01
**Status:** ✅ PASSING (all archives standardized)

---

### **Check 3.2: Orphaned Files**
**Risk:** Files exist but are not referenced anywhere, dead weight in repo

**Validation Process:**
1. **Build reference map** - What files reference what files
2. **Identify unreferenced files** - Files with zero incoming references
3. **Check if intentionally standalone** (READMEs, entry points)
4. **Flag as orphaned** if not intentionally isolated

**What to look for:**
- [ ] Markdown files not linked from any other file
- [ ] Code files not imported anywhere
- [ ] Documents not listed in any index/navigation
- [ ] Files with zero NEEDED_BY entries in semantic headers

**Pass Criteria:**
- All files are reachable from entry points (README.md, etc.)
- Orphaned files are either intentional or archived
- No surprise orphaned files discovered

**Exceptions (Intentional Standalone):**
- `/README.md` (repo entry point)
- `/REPO_LOG.md` (primary log)
- `/auditors/Bootstrap/BOOTSTRAP_*.md` (entry points)

**Fix Pattern:**
- Archive orphaned files to `.Archive/` if no longer needed
- Add links/references if file should be discoverable
- Add to navigation docs (README, DASHBOARD, etc.)

**Files to Check:**
- All markdown files
- All Python files
- All directories

**Last Validated:** [Not yet validated]
**Status:** ⏳ PENDING

---

### **Check 3.3: Naming Convention Violations**
**Risk:** Files not following established conventions, hard to discover

**Validation Process:**
1. **Load naming conventions** from standards docs
2. **Check each file** against expected pattern
3. **Flag violations** (wrong case, wrong prefix, wrong suffix)
4. **Verify semantic header FILE field** matches actual filename

**What to look for:**
- [ ] `readme.md` instead of `README.md` (case violation)
- [ ] `task-brief.md` instead of `TASK_BRIEF_*.md` (prefix violation)
- [ ] `.MD` instead of `.md` (extension case violation)
- [ ] Semantic header FILE field doesn't match actual filename

**Pass Criteria:**
- All files follow naming conventions per standards
- FILE field in semantic headers matches actual filename
- No case sensitivity issues

**Conventions:**
- READMEs: `README.md` (all caps)
- Task briefs: `TASK_BRIEF_[NAME].md` (all caps prefix)
- Protocols: `[NAME]_PROTOCOL.md` (all caps)
- Reports: `[DATE]_[NAME].md` or `[NAME]_REPORT.md`

**Fix Pattern:**
```bash
# Rename to follow convention
git mv wrong_name.md CORRECT_NAME.md
# Update semantic header FILE field
# Update all references to use new name
```

**Files to Check:**
- All files in repository

**Last Validated:** [Not yet validated]
**Status:** ⏳ PENDING

---

## 📜 **CATEGORY 4: STANDARDS COMPLIANCE**

### **Check 4.1: Semantic Header Coverage**
**Risk:** Files missing semantic headers, dependency tracking fails

**Validation Process:**
1. **Scan all markdown files** for semantic header block
2. **Check header completeness** (FILE, PURPOSE, VERSION, STATUS, etc.)
3. **Calculate coverage percentage** (files with headers / total files)
4. **Target: 80% coverage** per DASHBOARD.md goals

**What to look for:**
- [ ] Markdown files with no semantic header block
- [ ] Headers missing required fields (FILE, PURPOSE, STATUS)
- [ ] Headers with empty field values
- [ ] Headers using wrong format (not HTML comment block)

**Pass Criteria:**
- ≥80% of tracked markdown files have semantic headers
- All required fields present (FILE, PURPOSE, VERSION, STATUS)
- No empty field values
- Correct format (HTML comment block at top of file)

**Required Fields:**
```markdown
<!---
FILE: example.md
PURPOSE: Brief description
VERSION: 1.0
STATUS: Active
DEPENDS_ON: dependency1, dependency2
NEEDED_BY: consumer1, consumer2
MOVES_WITH: /path/to/location/
LAST_UPDATE: YYYY-MM-DD
--->
```

**Fix Pattern:**
- Add semantic header to files without one
- Fill in missing fields based on file context
- Update MASTER_DEPENDENCY_MAP.md header coverage metric

**Files to Check:**
- All markdown files in `/docs/`
- All markdown files in `/auditors/`
- Exclude: Archives, Completed/, temporary files

**Last Validated:** 2025-10-31
**Status:** 🟡 AT RISK (40% coverage, target 80%)

---

### **Check 4.2: `<!-- deps: -->` Tag Consistency**
**Risk:** Deps tags present but incorrect, misleading dependency tracking

**Validation Process:**
1. **Extract all `<!-- deps: -->` tags** from files
2. **Verify dependencies actually exist** in referenced locations
3. **Check for stale dependencies** (deps on deleted/moved files)
4. **Cross-reference with semantic header DEPENDS_ON**

**What to look for:**
- [ ] `<!-- deps: foo -->` but foo doesn't exist
- [ ] Deps tags referencing deleted files
- [ ] Mismatch between `<!-- deps: -->` and DEPENDS_ON field
- [ ] Deps tags with typos or wrong names

**Pass Criteria:**
- All deps tags reference existing files/components
- No stale dependencies to deleted/moved files
- Consistency between deps tags and semantic headers
- Deps are bidirectional (if A deps B, B knows about A)

**Fix Pattern:**
- Remove deps tags for deleted dependencies
- Update deps tags when files are moved
- Sync deps tags with semantic header DEPENDS_ON
- Add NEEDED_BY entries to dependency targets

**Files to Check:**
- All files with `<!-- deps: -->` tags (currently ~40% of repo)

**Last Validated:** [Not yet validated]
**Status:** ⏳ PENDING

---

### **Check 4.3: REPO_LOG Entry Format**
**Risk:** REPO_LOG entries don't follow protocol, hard to parse/track

**Validation Process:**
1. **Read REPO_LOG.md** from top to bottom
2. **Verify each entry** follows standard format
3. **Check for required fields** (ID, Date, Type, Description)
4. **Validate chronological order** (newest first)

**What to look for:**
- [ ] Entries missing [ID] tag (e.g., [DOCUMENTATION-2025-11-02-01])
- [ ] Entries with wrong date format
- [ ] Entries out of chronological order
- [ ] Entries missing description or context
- [ ] ID tags that skip numbers or duplicate

**Pass Criteria:**
- All entries have proper [ID] tag format
- Chronological order maintained (newest first)
- No missing required fields
- ID sequence is monotonic (no gaps, no duplicates)

**Standard Format:**
```markdown
### [ID] - Date: Description

**Details:**
- Change 1
- Change 2

**Impact:** Impact description

**Related:** Links to related files/commits
```

**Fix Pattern:**
- Add missing [ID] tags using next available sequence number
- Reorder entries if chronological order broken
- Fill in missing fields from git commit history
- Update ID sequence to fix gaps/duplicates

**Files to Check:**
- `/REPO_LOG.md`

**Last Validated:** 2025-11-02
**Status:** ✅ PASSING (entries following protocol)

---

## ⚖️ **CATEGORY 5: STATE CONSISTENCY**

### **Check 5.1: Version Number Consistency**
**Risk:** Different files claim different current versions, confusion ensues

**Validation Process:**
1. **Identify authoritative version source** (VuDu_PROTOCOL.md)
2. **Extract version claims** from all documentation
3. **Compare all versions** to authoritative source
4. **Flag mismatches** as inconsistencies

**What to look for:**
- [ ] README.md says v3.7.0 but VuDu_PROTOCOL.md says v3.8.0
- [ ] DASHBOARD.md references wrong version
- [ ] Semantic headers VERSION field doesn't increment
- [ ] Changelog missing entries for version bumps

**Pass Criteria:**
- All version references match VuDu_PROTOCOL.md
- Semantic header VERSION fields are consistent
- Changelog has entries for all version bumps
- No "current version" claims that contradict source

**Authoritative Sources:**
- `/auditors/protocols/VuDu_PROTOCOL.md` - Repository version
- Individual file semantic headers - File version

**Fix Pattern:**
- Update all version references to match VuDu_PROTOCOL.md
- Increment semantic header VERSION when file changes
- Add changelog entries when version bumps occur
- Document version bump rationale in REPO_LOG

**Files to Check:**
- `/auditors/protocols/VuDu_PROTOCOL.md` (source of truth)
- `/README.md`
- `/docs/repository/DASHBOARD.md`
- `/docs/CHANGELOG.md`

**Last Validated:** [Not yet validated]
**Status:** ⏳ PENDING

---

### **Check 5.2: Status Field Accuracy**
**Risk:** Files marked "Active" that are actually deprecated/archived

**Validation Process:**
1. **Extract STATUS field** from all semantic headers
2. **Verify status matches location** (Active files not in archives)
3. **Check for stale "Active" status** on unused files
4. **Validate status transitions** documented in REPO_LOG

**What to look for:**
- [ ] STATUS: Active but file is in .Archive/ directory
- [ ] STATUS: Deprecated but file is still referenced everywhere
- [ ] STATUS: Draft but file is being used in production
- [ ] No STATUS field (default to Active assumed)

**Pass Criteria:**
- All archived files have STATUS: Archived or Deprecated
- All active files have STATUS: Active
- Status transitions documented in REPO_LOG
- No STATUS field contradicting file location

**Valid Status Values:**
- `Active` - Currently in use
- `Draft` - Work in progress
- `Deprecated` - Replaced, kept for reference
- `Archived` - No longer active, historical record

**Fix Pattern:**
- Update STATUS field to match actual file state
- Move misplaced files (Active files to active location, etc.)
- Document status transitions in REPO_LOG
- Add DEPRECATED note to deprecated files

**Files to Check:**
- All files with semantic headers
- All files in `.Archive/` directories
- All files in `Completed/` directories

**Last Validated:** [Not yet validated]
**Status:** ⏳ PENDING

---

### **Check 5.3: Cross-Document State Alignment**
**Risk:** One doc updated but dependent docs not updated, state divergence

**Validation Process:**
1. **Identify state-bearing documents** (DASHBOARD, README_C, MISSION_CURRENT)
2. **Extract state claims** from each (phase, status, progress)
3. **Cross-reference state claims** for consistency
4. **Use REPO_LOG as tiebreaker** when conflicts found

**What to look for:**
- [ ] DASHBOARD says "Phase 3" but MISSION_CURRENT says "Phase 4"
- [ ] README_C.md shows different progress than DASHBOARD.md
- [ ] Task briefs not updated when DASHBOARD milestones change
- [ ] Health score in DASHBOARD doesn't match health reports

**Pass Criteria:**
- All state-bearing documents agree on current state
- When state changes in one doc, all dependents updated
- REPO_LOG entries exist for state transitions
- No contradictory progress/phase/status claims

**State-Bearing Documents:**
- `/REPO_LOG.md` - Source of truth for all changes
- `/docs/repository/DASHBOARD.md` - Health status, metrics
- `/README_C.md` - Master state document
- `/auditors/Bootstrap/MISSION_CURRENT.md` - Current mission phase
- Task briefs - Task status, progress

**Fix Pattern:**
- Use REPO_LOG as authoritative state source
- Update all dependent documents when REPO_LOG changes
- Add cross-references between state-bearing documents
- Document state transitions in REPO_LOG with references

**Files to Check:**
- `/REPO_LOG.md`
- `/docs/repository/DASHBOARD.md`
- `/README_C.md`
- `/auditors/Bootstrap/MISSION_CURRENT.md`

**Last Validated:** [Not yet validated]
**Status:** ⏳ PENDING

---

## 🔧 **CATEGORY 6: PROCESS ADHERENCE**

### **Check 6.1: Git Commit Message Format**
**Risk:** Commit messages don't follow convention, hard to parse history

**Validation Process:**
1. **Read recent commit history** (last 20-50 commits)
2. **Check format compliance** (Type: Description [ID])
3. **Verify [ID] tag presence** and format
4. **Check for empty or vague commit messages**

**What to look for:**
- [ ] Commit messages without type prefix (Documentation:, Fix:, etc.)
- [ ] Commit messages without [ID] tag
- [ ] Vague messages ("updated files", "fixed stuff")
- [ ] Multi-line commit messages not following HEREDOC format

**Pass Criteria:**
- All commits have type prefix (Documentation:, Fix:, Feature:, etc.)
- All commits have [ID] tag matching REPO_LOG entry
- Commit messages are descriptive (what/why)
- Recent commits (last 20) score 90%+ compliance

**Standard Format:**
```
Type: Brief description [ID]

Detailed explanation of what changed and why.

IMPACT: What this affects
```

**Fix Pattern:**
- Cannot retroactively fix past commits (unless amending/rebasing)
- Document commit message standards for future
- Use HEREDOC format for multi-line messages
- Always include [ID] tag and REPO_LOG entry

**Files to Check:**
- Git commit history (via `git log`)

**Last Validated:** 2025-11-02
**Status:** ✅ PASSING (recent commits following protocol)

---

### **Check 6.2: Branch Naming Convention**
**Risk:** Branches not following convention, hard to track purpose

**Validation Process:**
1. **List all branches** (local and remote)
2. **Check naming convention** (claude/*, feature/*, fix/*)
3. **Verify session ID suffix** for claude/* branches
4. **Check for stale branches** (no commits in >30 days)

**What to look for:**
- [ ] Branches without prefix (main, master exempt)
- [ ] claude/* branches without session ID suffix
- [ ] Branches with vague names ("test", "temp", "new")
- [ ] Many stale branches not cleaned up

**Pass Criteria:**
- All feature branches follow naming convention
- claude/* branches have session ID suffix
- No branches with vague names
- Stale branches archived or deleted

**Naming Conventions:**
- `claude/[description]-[sessionID]` - Claude-created branches
- `feature/[description]` - Feature branches
- `fix/[description]` - Bug fix branches
- `docs/[description]` - Documentation branches

**Fix Pattern:**
- Cannot rename remote branches easily (create new, delete old)
- Document branch naming standards
- Clean up stale branches periodically
- Add session ID suffix to claude/* branches before push

**Files to Check:**
- Git branches (via `git branch -a`)

**Last Validated:** 2025-11-02
**Status:** ✅ PASSING (current branch follows convention)

---

### **Check 6.3: Active_Tasks vs Completed/ Organization**
**Risk:** Completed tasks mixed with active tasks, confusing task status

**Validation Process:**
1. **List files in Active_Tasks/** directory
2. **Check REPO_LOG for completion entries** for each task
3. **Verify completed tasks moved to Completed/**
4. **Check for orphaned tasks** (no REPO_LOG entry)

**What to look for:**
- [ ] Tasks in Active_Tasks/ that are complete per REPO_LOG
- [ ] Tasks in Completed/ that are still referenced as active
- [ ] Tasks with no REPO_LOG entry (orphaned)
- [ ] Redundant archives (zip files already extracted)

**Pass Criteria:**
- All completed tasks per REPO_LOG are in Completed/
- All active tasks per REPO_LOG are in Active_Tasks/
- No orphaned tasks without REPO_LOG entry
- No redundant archives

**Fix Pattern:**
```bash
# Move completed task
git mv Active_Tasks/TASK_FOO.md Completed/TASK_FOO.md
git commit -m "Task Housekeeping: Move TASK_FOO to Completed/ [ID]"

# Delete redundant archive
git rm "Redundant Archive.zip"
git commit -m "Cleanup: Remove Completed Archive (Redundant Archive.zip) [ID]"
```

**Files to Check:**
- `/auditors/Bootstrap/Tier4_TaskSpecific/Active_Tasks/`
- `/auditors/Bootstrap/Tier4_TaskSpecific/Completed/`
- `/REPO_LOG.md` (task completion entries)

**Last Validated:** 2025-11-02
**Status:** ✅ PASSING (all completed tasks moved)

---

## 📊 **VALIDATION SCORECARD**

### **How to Use This Scorecard:**

After completing validation, calculate scores for each category:

```
Score = (Passing Checks / Total Checks) × 100%

Category 1: Documentation Health     [__/3] = ___%
Category 2: Loop Detection           [__/3] = ___%
Category 3: Structural Integrity     [__/3] = ___%
Category 4: Standards Compliance     [__/3] = ___%
Category 5: State Consistency        [__/3] = ___%
Category 6: Process Adherence        [__/3] = ___%

OVERALL VALIDATION SCORE: [__/18] = ___%
```

### **Score Interpretation:**

| Score | Grade | Action Required |
|-------|-------|-----------------|
| 95-100% | 🟢 Excellent | Continue current practices |
| 85-94% | 🟡 Good | Address minor issues |
| 70-84% | 🟠 Needs Improvement | Create improvement plan |
| <70% | 🔴 Critical | Stop and fix immediately |

### **Latest Validation Results:**

**Date:** 2025-11-02
**Validated By:** [Claude instance ID]
**Overall Score:** [___%]

**Category Breakdown:**
- Category 1 (Documentation Health): [___%] - [Status emoji]
- Category 2 (Loop Detection): [___%] - [Status emoji]
- Category 3 (Structural Integrity): [___%] - [Status emoji]
- Category 4 (Standards Compliance): [___%] - [Status emoji]
- Category 5 (State Consistency): [___%] - [Status emoji]
- Category 6 (Process Adherence): [___%] - [Status emoji]

**Critical Findings:** [List any critical issues found]

**Recommendations:** [List top 3 recommended actions]

**Next Validation Due:** [Date + 7 days for active development]

---

## 🔄 **VALIDATION WORKFLOW**

### **Standard Validation Process:**

**1. Pre-Validation Setup (5 minutes)**
```markdown
- [ ] Read VALIDATION_MAP.md (this file)
- [ ] Read latest DASHBOARD.md for current state
- [ ] Read REPO_LOG.md last 10 entries
- [ ] Note any recent major changes
- [ ] Prepare validation checklist
```

**2. Execute Validation (30-45 minutes)**
```markdown
- [ ] Category 1: Documentation Health (3 checks)
- [ ] Category 2: Loop Detection (3 checks)
- [ ] Category 3: Structural Integrity (3 checks)
- [ ] Category 4: Standards Compliance (3 checks)
- [ ] Category 5: State Consistency (3 checks)
- [ ] Category 6: Process Adherence (3 checks)
```

**3. Document Findings (10 minutes)**
```markdown
- [ ] Fill in validation scorecard above
- [ ] List critical findings with line numbers/paths
- [ ] Prioritize findings (Critical/Important/Nice-to-have)
- [ ] Create fix plan for critical items
```

**4. Execute Fixes (Variable)**
```markdown
- [ ] Fix all critical findings immediately
- [ ] Document fixes in REPO_LOG
- [ ] Re-validate affected areas
- [ ] Update validation scorecard
```

**5. Post-Validation (5 minutes)**
```markdown
- [ ] Update DASHBOARD.md with validation status
- [ ] Update this file with latest validation date
- [ ] Commit validation results
- [ ] Schedule next validation date
```

---

## 🚨 **CRITICAL VALIDATION TRIGGERS**

**Run full validation immediately when:**

1. **Before Major Version Bump** (v3.7 → v3.8)
   - Ensures clean state before version increment
   - Validates all documentation reflects new version
   - Checks for breaking changes documented

2. **After Large Merge** (>50 files changed)
   - Detects conflicts introduced by merge
   - Validates cross-document consistency
   - Checks for broken links/references

3. **Before Deployment Decision** (production release)
   - Confirms repository health score
   - Validates no critical issues outstanding
   - Checks all process gates passed

4. **When Doc Claude Reports False Positives** (stale data)
   - Identifies source of stale checklists
   - Updates all affected documentation
   - Prevents future false positives

5. **Weekly During Active Development** (ongoing work)
   - Maintains quality standards
   - Catches issues early
   - Prevents technical debt accumulation

6. **After Bootstrap System Changes** (structural changes)
   - Validates bootstrap still functional
   - Checks for broken entry points
   - Confirms recovery systems operational

---

## 📋 **VALIDATION REPORT TEMPLATE**

**Use this template when creating validation reports:**

```markdown
# Validation Report - [Date]

**Validated By:** [Claude instance ID or name]
**Validation Scope:** [Full | Partial | Targeted]
**Duration:** [Time taken]
**Status:** [PASS | FAIL | CONDITIONAL PASS]

---

## Executive Summary

[2-3 sentence summary of overall validation state]

**Overall Score:** [X/18] = [___%]
**Grade:** [🟢/🟡/🟠/🔴] [Excellent/Good/Needs Improvement/Critical]

**Critical Findings:** [Count]
**Important Findings:** [Count]
**Minor Findings:** [Count]

---

## Category Results

### Category 1: Documentation Health
**Score:** [X/3] = [___%]
**Status:** [Emoji + Text]
**Findings:**
- Check 1.1: [Pass/Fail] - [Details]
- Check 1.2: [Pass/Fail] - [Details]
- Check 1.3: [Pass/Fail] - [Details]

[Repeat for all 6 categories]

---

## Critical Findings

### Finding #1: [Title]
**Severity:** Critical
**Category:** [Category name]
**Check:** [Check number]
**Location:** [File path and line number]
**Description:** [What's wrong]
**Impact:** [What this breaks]
**Fix:** [How to fix]
**Status:** [Open/In Progress/Fixed]

[Repeat for all critical findings]

---

## Recommendations

1. **[Priority 1 Action]** - [Why] - [When]
2. **[Priority 2 Action]** - [Why] - [When]
3. **[Priority 3 Action]** - [Why] - [When]

---

## Next Validation

**Scheduled:** [Date]
**Scope:** [Full/Partial]
**Focus Areas:** [Areas needing attention]
**Prerequisites:** [Actions to complete before next validation]

---

**Report Generated:** [Timestamp]
**Signed:** [Validation Claude ID]
**Stored:** /docs/Validation/reports/[DATE]_VALIDATION_REPORT.md
```

---

## 🎯 **SUCCESS CRITERIA**

**This VALIDATION_MAP is effective when:**

✅ **Zero False Positives**
- Doc Claude instances never report already-completed items
- Stale checklists caught and updated immediately
- STATUS UPDATE sections keep documentation current

✅ **Zero Missed Loops**
- Circular dependencies detected before they cause issues
- Redirect chains caught and fixed
- Contradictory state claims identified

✅ **High Quality Score**
- Validation score consistently ≥90%
- Critical findings addressed within 24 hours
- Validation becomes routine, not heroic

✅ **Systematic Coverage**
- All 6 categories checked in every validation
- No validation areas skipped or forgotten
- Consistent validation process across all validators

✅ **Process Improvement**
- Validation findings drive process improvements
- Common issues addressed at root cause
- Validation time decreases as quality increases

---

## 🔧 **MAINTENANCE**

### **This VALIDATION_MAP should be updated when:**

1. **New validation category identified** - Add as Category 7, 8, etc.
2. **New check needed in existing category** - Add as Check X.4, X.5, etc.
3. **Check becomes obsolete** - Mark as deprecated, move to archive section
4. **Validation process improves** - Update workflow section
5. **New tools available** - Add to automation section

### **Update Process:**

1. Identify needed change
2. Update VALIDATION_MAP.md
3. Increment VERSION in semantic header
4. Update LAST_UPDATE date and [ID] tag
5. Document change in REPO_LOG
6. Test validation with updated map
7. Commit changes

---

## 📖 **RELATED DOCUMENTATION**

**Validation Process:**
- `/docs/repository/librarian_tools/ROLE_VALIDATION.md` - Validation role definition
- `/docs/Validation/` - Validation reports and history
- `/docs/Validation/Criteria/` - Validation criteria

**Quality Standards:**
- `/docs/repository/librarian_tools/HEADER_STANDARD.md` - Semantic header standard
- `/docs/repository/librarian_tools/88MPH.md` - Repository assessment
- `/auditors/protocols/VuDu_PROTOCOL.md` - Version and update protocol

**State Tracking:**
- `/REPO_LOG.md` - Authoritative change log
- `/docs/repository/DASHBOARD.md` - Current repository health
- `/README_C.md` - Master state document

**Dependency Tracking:**
- `/docs/repository/dependency_maps/MASTER_DEPENDENCY_MAP.md` - Full dependency map
- `/docs/repository/dependency_maps/DOCUMENTATION_DEPENDENCY_ANALYSIS.md` - Doc dependencies

---

## 🎯 **QUICK START**

**First time using this map? Follow these steps:**

1. **Read this entire file** (15 minutes) - Understand all 6 categories
2. **Read ROLE_VALIDATION.md** (10 minutes) - Understand your role
3. **Run your first validation** (45 minutes) - Use checklist below
4. **Document findings** (10 minutes) - Use scorecard template
5. **Fix critical issues** (variable) - Address findings
6. **Schedule next validation** (1 minute) - Add to calendar

**Validation Checklist:**
```markdown
- [ ] Pre-validation setup (5 min)
- [ ] Category 1: Documentation Health (8 min)
- [ ] Category 2: Loop Detection (8 min)
- [ ] Category 3: Structural Integrity (8 min)
- [ ] Category 4: Standards Compliance (8 min)
- [ ] Category 5: State Consistency (8 min)
- [ ] Category 6: Process Adherence (8 min)
- [ ] Calculate scorecard (3 min)
- [ ] Document findings (10 min)
- [ ] Create fix plan (5 min)
```

**Total Time:** ~70 minutes for first full validation

---

**"The map that prevents loops, closes gaps, and ensures quality."** 🗺️

**Validation Map maintained by Validation Claude** 🔍
**Systematic quality assurance, not heroic firefighting**

────────────────────────────────────────────────────

**Created:** 2025-11-02
**Version:** 1.0
**Status:** Active Validation Tool
**Next Review:** After first 5 validations (gather feedback for improvements)

**This is the way.** ✅
