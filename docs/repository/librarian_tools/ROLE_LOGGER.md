<!---
FILE: ROLE_LOGGER.md
PURPOSE: Define the Logger role for Doc_Claude (REPO_LOG entry creation)
VERSION: 1.1
STATUS: Active
DEPENDS_ON: REPO_LOG.md, REPO_LOG_ASSISTANT.md (in Tier4 tasks)
NEEDED_BY: Doc_Claude, any AI maintaining REPO_LOG
MOVES_WITH: /docs/repository/librarian_tools/
LAST_UPDATE: 2025-11-01 [DOCUMENTATION-2025-11-01-11]
--->

# ROLE: Logger

**Role Name:** Logger
**Specialization:** Compliance Helper for REPO_LOG Entry Creation
**Operator:** DOC_CLAUDE (primary), any AI maintaining REPO_LOG
**Authority:** REPO_LOG.md is source of truth - this role assists interpretation
**Version:** 1.0
**Created:** 2025-11-01

---

## 🎯 ROLE OVERVIEW

### **Purpose**

This role helps any AI create properly formatted, compliant REPO_LOG entries that follow repository standards. It transforms plain language descriptions of work into structured, standardized documentation.

### **The Problem This Solves**

**Without Logger:**
- Inconsistent entry formatting across sessions
- Missing required fields (impact, follow-up, etc.)
- Incorrect entry ID sequencing
- Vague change descriptions
- Unclear follow-up tracking

**With Logger:**
- Consistent, compliant entries every time
- All required fields populated
- Proper sequential entry IDs
- Specific, actionable change descriptions
- Clear follow-up status and actions

### **When to Activate This Role**

**Always activate when:**
- Creating new REPO_LOG entries
- Documenting completed work at coordination checkpoints
- Moving tasks between Active/Completed
- Making structural changes to repository
- Unsure about REPO_LOG entry format

**Not needed when:**
- Just reading REPO_LOG.md
- Reviewing existing entries (unless validating format)
- Working on non-repository documentation

---

## 📋 ROLE CAPABILITIES

### **What This Role Can Do**

1. ✅ Guide entry creation step-by-step (7-step wizard)
2. ✅ Generate correct entry IDs with sequential numbering
3. ✅ Format changes with proper action verbs
4. ✅ Assess impact levels (Minimal/Moderate/Significant)
5. ✅ Determine follow-up requirements
6. ✅ Validate entries against compliance checklist
7. ✅ Provide scenario-based examples

### **What This Role Cannot Do**

1. ❌ Override REPO_LOG.md standards (only assists interpretation)
2. ❌ Create entries without knowing what work was done
3. ❌ Guess at file paths or changes
4. ❌ Modify existing REPO_LOG entries without guidance

---

## 🔄 ROLE WORKFLOW

### **Step 1: Information Gathering**

**Ask these questions:**
```
What files did I change?
What type of changes? (update/create/fix/move)
Why did I make these changes?
What's the impact?
Does anything need follow-up?
```

**Required information:**
- Exact file paths (absolute paths from repo root)
- Specific changes made to each file
- Reason for making changes (the "why")
- Session ID for traceability

### **Step 2: Category Selection**

**Primary category (choose ONE):**
- `[DOCUMENTATION]` - Doc_Claude's main category
- `[STRUCTURE]` - Directory reorganization
- `[TASK_MOVEMENT]` - Moving task briefs
- `[VALIDATION]` - Reporting validation issues

**Additional categories (if relevant):**
- Add after primary if changes span multiple areas
- Example: `[DOCUMENTATION] [STRUCTURE]`

### **Step 3: Entry ID Generation**

**Format:** `[CATEGORY-YYYY-MM-DD-N]`

**To find N:**
1. Open REPO_LOG.md
2. Find last entry for today with same category
3. N = that number + 1

**Example:**
```
Last entry: [DOCUMENTATION-2025-11-01-9]
Your entry: [DOCUMENTATION-2025-11-01-10]
```

### **Step 4: Entry Construction**

**Use standard template:**
```markdown
### [CATEGORY-YYYY-MM-DD-N] Date - Brief Description

**Categories:** [CATEGORY] [ADDITIONAL_IF_ANY]
**Changed by:** Doc_Claude (Repo Librarian)
**Session ID:** [your-session-id]
**Status:** DEPLOYED ✅ (or PENDING ⏳)

**Changes:**
- `ACTION`: /exact/path/to/file.md - What specifically changed
- `ACTION`: /another/path/file.md - What changed here

**Reason:** [Why you made these changes - the business value]

**Impact:** Minimal/Moderate/Significant

**Follow-up Required:** YES/NO
**Follow-up Status:** N/A or PENDING
**Follow-up Action:** [What needs to happen next, if YES]
```

### **Step 5: Action Verb Selection**

**Standard action verbs:**
- `UPDATED` - Modified existing file
- `CREATED` - Made new file
- `FIXED` - Repaired broken link/error
- `MOVED` - Relocated file
- `DELETED` - Removed file
- `RENAMED` - Changed file name
- `MERGED` - Combined content from multiple sources
- `FLAGGED` - Identified issue for follow-up

### **Step 6: Impact Assessment**

**Minimal:**
- Single file update
- No downstream effects
- Routine maintenance

**Moderate:**
- Multiple files updated
- Some downstream updates needed
- Cross-references affected

**Significant:**
- Directory restructure
- Many files affected
- Major protocol changes
- System-wide implications

### **Step 7: Follow-up Determination**

**Follow-up Required: YES if:**
- Changes are incomplete
- Waiting on specialist input
- Subcontract created
- Cascade updates needed
- Testing required

**Follow-up Required: NO if:**
- Changes complete
- All cascade updates done
- Self-contained update
- No dependencies affected

---

## ✅ COMPLIANCE CHECKLIST

**Before submitting any entry, verify:**

- [ ] Entry ID format correct: `[CAT-YYYY-MM-DD-N]`
- [ ] N is sequential (checked last entry for today)
- [ ] All file paths are exact and absolute (start with /)
- [ ] All actions use proper verbs (UPDATED/CREATED/etc)
- [ ] Reason explains WHY (not just WHAT)
- [ ] Impact assessed (Minimal/Moderate/Significant)
- [ ] Follow-up status matches requirement (YES/NO alignment)
- [ ] Entry placed at coordination checkpoint (top of REPO_LOG.md)
- [ ] Session ID included and properly formatted
- [ ] Status indicator present (✅ or ⏳)

---

## 💡 EXAMPLE SCENARIOS

### **Scenario 1: Updated Multiple Files (Minimal Impact)**

**Work done:** Updated 3 READMEs to fix broken links

**Assistant output:**
```markdown
### [DOCUMENTATION-2025-11-01-3] 2025-11-01 - Updated READMEs for Link Fixes

**Categories:** [DOCUMENTATION]
**Changed by:** Doc_Claude (Repo Librarian)
**Session ID:** claude/onboarding-88mph-review-011CUgHTs3EjgHdXg9Sy4Tvf
**Status:** DEPLOYED ✅

**Changes:**
- `UPDATED`: /auditors/README.md - Fixed 2 broken links to mission files
- `UPDATED`: /docs/README.md - Updated version reference to v3.7.2
- `UPDATED`: /auditors/missions/README.md - Fixed 1 broken link to VUDU_PROTOCOL

**Reason:** Routine maintenance sweep identified broken links across navigation docs

**Impact:** Minimal

**Follow-up Required:** NO
**Follow-up Status:** N/A
**Follow-up Action:** N/A
```

### **Scenario 2: Created New Structure (Moderate Impact)**

**Work done:** Created new /tools/ directory and moved files there

**Assistant output:**
```markdown
### [STRUCTURE-2025-11-01-1] 2025-11-01 - Created /tools/ Directory

**Categories:** [STRUCTURE] [DOCUMENTATION]
**Changed by:** Doc_Claude (Repo Librarian)
**Session ID:** claude/onboarding-88mph-review-011CUgHTs3EjgHdXg9Sy4Tvf
**Status:** DEPLOYED ✅

**Changes:**
- `CREATED`: /docs/repository/librarian_tools/ - New directory for Doc_Claude tools
- `CREATED`: /docs/repository/librarian_tools/README.md - Directory documentation
- `MOVED`: /ROLE_VALIDATION.md → /docs/repository/librarian_tools/ROLE_VALIDATION.md
- `UPDATED`: /docs/repository/README.md - Added librarian_tools/ reference

**Reason:** Consolidating Doc_Claude role definitions into organized directory for better discoverability

**Impact:** Moderate

**Follow-up Required:** YES
**Follow-up Status:** PENDING
**Follow-up Action:** Update all references to moved ROLE_VALIDATION.md in other docs
```

### **Scenario 3: Found Issue, Created Subcontract (Significant Impact)**

**Work done:** Identified outdated protocol content needing specialist review

**Assistant output:**
```markdown
### [VALIDATION-2025-11-01-1] 2025-11-01 - Identified VUDU_PROTOCOL Update Needed

**Categories:** [VALIDATION] [DOCUMENTATION]
**Changed by:** Doc_Claude (Repo Librarian)
**Session ID:** claude/onboarding-88mph-review-011CUgHTs3EjgHdXg9Sy4Tvf
**Status:** PENDING ⏳

**Changes:**
- `CREATED`: /auditors/relay/SUBCONTRACT_VUDU_SPECIALIST_2025-11-01.md
- `FLAGGED`: /auditors/VUDU_PROTOCOL.md - Sections 3.2, 4.1 outdated

**Reason:** Routine audit revealed protocol drift from v3.5.2 → v3.7.2, affects coordination reliability

**Impact:** Significant (affects all multi-AI coordination)

**Follow-up Required:** YES
**Follow-up Status:** PENDING
**Follow-up Action:** VUDU specialist to review and update protocol sections 3.2, 4.1
```

---

## 🎯 QUALITY STANDARDS

### **Good Entry Characteristics**

✅ Specific file paths (not "several files")
✅ Exact changes described
✅ Clear reasoning (the "why")
✅ Realistic impact assessment
✅ Follow-up clearly defined
✅ Proper action verbs
✅ Sequential entry ID
✅ All required fields present

### **Bad Entry Characteristics**

❌ Vague descriptions ("updated some stuff")
❌ Missing file paths
❌ No reason given
❌ Impact not assessed
❌ Unclear follow-up
❌ Wrong action verbs
❌ Non-sequential entry ID
❌ Missing required fields

---

## 🔧 ACTIVATION INSTRUCTIONS

### **How to Activate This Role**

**Method 1: Explicit Activation (Recommended)**
```
I am activating Logger role.
I need to create a REPO_LOG entry for the following work:

[Describe work in plain language]

Applying Logger workflow:
1. Gathering information...
2. Selecting category...
3. Generating entry ID...
4. Constructing entry...
```

**Method 2: Reference Guide**
```
I need to create a REPO_LOG entry.
Referencing ROLE_LOGGER.md workflow...

[Follow 7-step process]
```

**Method 3: Quick Format Check**
```
Created this REPO_LOG entry - validating with Assistant checklist:
[Entry content]

Compliance check: [✓/✗ for each checklist item]
```

### **How to Deactivate This Role**

**After entry is created and validated:**
```
REPO_LOG entry created and validated.
Entry ID: [CATEGORY-YYYY-MM-DD-N]
Compliance: ✅ All checklist items passed
Status: Ready for deployment

Deactivating Logger role.
```

---

## 📚 REFERENCE MATERIALS

### **Primary Authority**
- **REPO_LOG.md (root)** - Source of truth for all standards
- This role assists interpretation, does not override

### **Supporting Materials**
- **/auditors/Bootstrap/Tier4_TaskSpecific/Active_Tasks/REPO_LOG_ASSISTANT.md** - Detailed guide with wizard
- **Recent REPO_LOG.md entries** - Examples of current format

### **For Questions**
- Consult REPO_LOG.md coordination checkpoint
- Check recent entries for pattern matching
- Ask Ziggy before guessing on edge cases

---

## 🎩 INTEGRATION WITH DOC_CLAUDE

### **This Role is Part of Doc_Claude's Toolkit**

When operating as Doc_Claude (Repo Librarian), this role is one of several capabilities:

1. **ROLE_VALIDATION** - Health reports and validation
2. **ROLE_DEPENDENCY_MAPPING** - Dependency tracking
3. **ROLE_LOGGER** - REPO_LOG entry creation ← YOU ARE HERE
4. **ROLE_REVIEW** - Review and validate prior work
5. **ROLE_HEALTH_REPORTS** - Repository health assessment

### **Hat-Switching Context**

When Master Branch Claude (Tier 1) switches to Doc_Claude hat for repo structural work, Logger should be activated for documenting that work.

### **Cross-Role Dependencies**

- **After ROLE_VALIDATION:** Use Logger to document findings
- **After ROLE_DEPENDENCY_MAPPING:** Use Logger to log map updates
- **After ROLE_HEALTH_REPORTS:** Use Logger to record health assessments
- **After ROLE_REVIEW:** Use Logger to document review outcomes

---

## ⚖️ THE POINTING RULE

*"Every change deserves documentation.
Every entry deserves specificity.
Every log deserves truth.

This is not overhead.
This is memory.
This is how the future
understands the past."* 📝

---

## 📊 SUCCESS METRICS

**Role is successful when:**

- ✅ All REPO_LOG entries pass compliance checklist
- ✅ Entry IDs are properly sequential
- ✅ File paths are accurate and complete
- ✅ Impact assessments are realistic
- ✅ Follow-up tracking is clear
- ✅ Future readers can understand what happened and why

**Role needs improvement when:**

- ❌ Entries missing required fields
- ❌ Entry ID numbering breaks sequence
- ❌ Vague or unclear change descriptions
- ❌ Impact levels inconsistent
- ❌ Follow-up status unclear

---

## 🔄 MAINTENANCE

**This role document should be updated when:**

- REPO_LOG.md standards change
- New entry categories are added
- Compliance checklist is modified
- New action verbs are standardized
- Impact assessment criteria change

**Maintainer:** DOC_CLAUDE (Repo Librarian)
**Review Frequency:** After major REPO_LOG.md updates
**Version Control:** Track in REPO_LOG.md when this role is updated

---

**Role Status:** ✅ Active
**Authority Level:** Assistant (not override)
**Integration:** Part of Doc_Claude toolkit
**Purpose:** Enable consistent, compliant REPO_LOG documentation

🔧 **Ready to assist with REPO_LOG entry creation** 🔧

---

**This is the way.** 🔥
