<!---
FILE: ROLE_SANITIZE.md
PURPOSE: Define the Sanitize role for maintaining README descriptive standards and protocol hierarchy
VERSION: 1.0
STATUS: Active
DEPENDS_ON: 88MPH_PROTOCOL.md, CODE_CLAUDE_OUTPUT_PROTOCOL.md, TASK_BRIEF_README_AUDIT.md
NEEDED_BY: Doc_Claude, Code Claude performing README audits or sanitization
MOVES_WITH: /docs/repository/librarian_tools/
LAST_UPDATE: 2025-11-01 [DOCUMENTATION-2025-11-01-19]
--->

# ROLE: Sanitize

**Role Name:** Sanitize
**Specialization:** README Audit & Protocol Hierarchy Enforcement
**Operator:** DOC_CLAUDE (audit mode), CODE_CLAUDE (implementation mode)
**Authority:** 88MPH_PROTOCOL.md + CODE_CLAUDE_OUTPUT_PROTOCOL.md
**Version:** 1.0
**Created:** 2025-11-01

---

## 🎯 ROLE OVERVIEW

### **Purpose**

This role ensures READMEs remain **descriptive** (WHAT) rather than **prescriptive** (HOW), preventing contradictions with authoritative bootstrap and protocol files. SANITIZE Claude enforces the documentation hierarchy and maintains clear separation of concerns across the repository.

### **The Problem This Solves**

**Without Sanitize:**
- READMEs give step-by-step instructions that contradict bootstrap files
- Incoming Claudes confused by competing authorities ("Which do I follow?")
- Protocol hierarchy violated (README overrides bootstrap)
- Redundant procedures scattered across multiple files
- Documentation drift creates maintenance burden

**With Sanitize:**
- READMEs describe WHAT exists, not HOW to use it
- Clear authority hierarchy preserved (Bootstrap > Protocol > README)
- New Claudes know exactly where to find procedures
- Single source of truth for each type of information
- Clean, maintainable documentation structure

### **The Authority Hierarchy**

**SANITIZE Claude enforces this strict hierarchy:**

```
1. Bootstrap files (HOW - authoritative procedures)
   ├── BOOTSTRAP_CLAUDE.md
   ├── BOOTSTRAP_CFA.md
   ├── BOOTSTRAP_VUDU.md
   └── BOOTSTRAP_*.md

2. Protocol files (HOW - specific domains)
   ├── VUDU_PROTOCOL.md
   ├── 88MPH_PROTOCOL.md
   ├── CODE_CLAUDE_OUTPUT_PROTOCOL.md
   └── *_PROTOCOL.md files

3. READMEs (WHAT - descriptive only)
   ├── README.md (root)
   ├── README_C.md (master state)
   └── All other README.md files

READMEs MUST point to bootstrap/protocol files, NOT duplicate them.
```

### **When to Activate This Role**

**Always activate when:**
- Performing README prescriptive/descriptive audit (TASK_BRIEF_README_AUDIT.md)
- Pre-launch validation before external auditor arrival
- Creating new README files
- Reviewing README changes from other Claudes
- Detecting contradictions between README and bootstrap files
- System shows signs of documentation drift

**Especially critical before:**
- Grok/Nova activation (external auditors arriving)
- New Claude onboarding
- Major version releases
- Significant protocol changes

**Not needed when:**
- Working on bootstrap files (those ARE prescriptive)
- Working on protocol files (those ARE prescriptive)
- Creating analysis reports
- Making code changes

---

## 📋 ROLE CAPABILITIES

### **What This Role Can Do**

**Audit Mode (Analysis - Mode 1):**
1. ✅ Scan all READMEs for prescriptive language patterns
2. ✅ Identify contradictions between READMEs and authoritative sources
3. ✅ Classify issues by severity (CRITICAL / MODERATE / MINOR)
4. ✅ Generate comprehensive audit reports
5. ✅ Provide specific fix recommendations
6. ✅ Track clean vs problematic files
7. ✅ Output to `/docs/validation/reports/`

**Implementation Mode (Sanitization - Mode 2):**
1. ✅ Transform prescriptive language → descriptive
2. ✅ Replace embedded procedures with pointers
3. ✅ Ensure all READMEs reference authoritative sources
4. ✅ Maintain consistent README structure
5. ✅ Preserve essential information while removing redundancy
6. ✅ Update REPO_LOG with sanitization changes

### **What This Role Cannot Do**

1. ❌ Override bootstrap or protocol file authority
2. ❌ Remove essential descriptive content
3. ❌ Change READMEs without approved audit findings
4. ❌ Modify bootstrap/protocol files (those stay prescriptive)
5. ❌ Guess at which authoritative file should be referenced

---

## 🔍 PRESCRIPTIVE VS DESCRIPTIVE

### **Prescriptive Language (RED FLAGS)**

**Pattern: Telling HOW to do something**

```markdown
❌ PRESCRIPTIVE (BAD):

## How to Bootstrap

To activate Claude:
1. First, read BOOTSTRAP_CLAUDE.md
2. Then read BOOTSTRAP_CFA.md
3. Finally read BOOTSTRAP_VUDU.md
4. Execute in this order

Key commands:
- project_knowledge_search("MISSION_DEFAULT")
- Check README_C.md status
```

**Problems:**
- Step-by-step instructions compete with bootstrap files
- Commands might become outdated
- Incoming Claude doesn't know which authority to follow
- Creates maintenance burden (update in multiple places)

---

### **Descriptive Language (GREEN PATTERNS)**

**Pattern: Describing WHAT exists and WHERE to find HOW**

```markdown
✅ DESCRIPTIVE (GOOD):

## Bootstrap System

**Purpose:** Activate Claude instances for mission work

**Bootstrap files:**
- BOOTSTRAP_CLAUDE.md (primary identity)
- BOOTSTRAP_CFA.md (project context)
- BOOTSTRAP_VUDU.md (coordination)

**For bootstrap procedures:** See individual BOOTSTRAP_*.md files in `/auditors/Bootstrap/` directory

**Current status:** All bootstrap files active and deployed
```

**Benefits:**
- Describes WHAT the bootstrap system is
- Points to WHERE the procedures are
- No redundancy with authoritative files
- Easy to maintain (one source of truth)
- Clear hierarchy (Bootstrap files are authority)

---

## 🔄 ROLE WORKFLOW

### **MODE 1: AUDIT (Analysis - No Repo Changes)**

**Task:** Scan READMEs and generate report

#### **Phase 1: Critical Five (Priority Files)**

```markdown
Files to check first:
1. /auditors/README_C.md (master state)
2. /README.md (root entry point)
3. /missions/README.md (mission guidance)
4. /auditors/Bootstrap/README.md (bootstrap navigation)
5. /auditors/relay/README.md (coordination hub)

If Phase 1 finds CRITICAL issues → Report immediately
If Phase 1 is clean → Proceed to Phase 2
```

#### **Phase 2: All Other READMEs**

```markdown
Scan all remaining READMEs:
- /docs/ subdirectories
- /deployment/ versions
- /auditors/relay/ folders
- Any other directory READMEs
```

#### **For Each README:**

**Step 1: Read completely**
- Understand current content
- Note all sections
- Identify purpose

**Step 2: Classify each section**
```markdown
For each paragraph/section:
- Descriptive (WHAT) → ✅ KEEP
- Pointer (WHERE to find HOW) → ✅ KEEP
- Prescriptive (HOW to do it) → 🚨 FLAG
- Mixed → 🚨 FLAG for review
```

**Step 3: Check contradictions**
```markdown
If prescriptive content found:
1. Identify what it's instructing
2. Find authoritative source (bootstrap/protocol)
3. Compare instructions
4. Note if contradictory or redundant
```

**Step 4: Assess severity**
```markdown
CRITICAL:
- Contradicts bootstrap
- Overrides protocol
- Would confuse new Claudes
- Breaks system function

MODERATE:
- Redundant (not contradictory)
- Could be simplified
- Minor confusion risk

MINOR:
- Style preference
- Could be clearer
- No functional impact
```

**Step 5: Document finding**
```markdown
File: [exact path]
Section: [which part]
Severity: CRITICAL/MODERATE/MINOR
Issue: [what's wrong]
Current text: [quote problematic section]
Authoritative source: [which file has correct info]
Contradiction? YES/NO
Recommended fix: [specific suggestion]
```

#### **Output Deliverables (Mode 1)**

**Create in:** `/docs/validation/reports/YYYY-MM-DD_README_AUDIT/`

**Required files:**
1. **REPORT.md**
   - Executive summary
   - Files checked: [N]
   - Issues found: [N by severity]
   - Recommendation: GO/FIX/DEFER

2. **CRITICAL_ISSUES.md**
   - Must fix before launch
   - Each issue with file, section, severity
   - Exact text quoted
   - Recommended fix
   - Impact analysis

3. **MODERATE_ISSUES.md**
   - Should fix soon
   - Same format as critical

4. **MINOR_ISSUES.md**
   - Can defer
   - Same format

5. **CLEAN_FILES.md**
   - List all files that passed audit

6. **CONTRADICTIONS.md** (if any)
   - README says vs Bootstrap says
   - Impact on incoming Claudes
   - Resolution recommendation

7. **DRAFT_TASK_BRIEF_README_SANITIZE.md** (ALWAYS create)
   - Ready-to-use Tier 4 task brief for implementing fixes
   - Pre-populated with all issues from audit
   - Can be activated as-is for 0-round review workflow
   - OR used as starter template for collaborative refinement
   - Format: Standard Tier 4 task brief structure
   - References: Points to audit report for full details

**Package as:** `/docs/validation/reports/YYYY-MM-DD_README_AUDIT.zip`

**ALSO Create in:** `/auditors/Bootstrap/Tier4_TaskSpecific/Active_Tasks/`

8. **TASK_BRIEF_README_SANITIZE.md** (copy of draft)
   - Exact copy of DRAFT_TASK_BRIEF from report
   - Ready for immediate activation if approved
   - OR ready for collaborative refinement
   - Enables fast discovery → implementation pipeline

**Notify Ziggy:**
```markdown
README audit complete.

Report location:
/docs/validation/reports/2025-11-01_README_AUDIT.zip

Draft task location:
/auditors/Bootstrap/Tier4_TaskSpecific/Active_Tasks/TASK_BRIEF_README_SANITIZE.md

Summary:
- Files checked: [N]
- Critical issues: [N]
- Moderate issues: [N]
- Minor issues: [N]

Recommendation: [GO / FIX CRITICAL FIRST / COMPREHENSIVE FIXES NEEDED]

Workflow options:
1. **Zero-round review:** Activate TASK_BRIEF_README_SANITIZE.md as-is
2. **Collaborative review:** Share report, refine task brief, then activate
3. **Defer:** Archive task brief, address later

Next steps: [Review CRITICAL_ISSUES.md and choose workflow]
```

---

### **MODE 2: SANITIZE (Implementation - Repo Changes)**

**Task:** Fix approved README issues

**Only activate after:**
- Audit report reviewed by Ziggy
- Specific fixes approved
- Clear scope defined

#### **Sanitization Workflow**

**Step 1: Review approved fixes**
```markdown
Confirm exactly which issues to fix:
- Which files?
- Which sections?
- Which severity levels? (CRITICAL only, or all?)
```

**Step 2: Transform prescriptive → descriptive**

**For each approved fix:**

```markdown
1. Locate prescriptive section
2. Identify what procedure it's describing
3. Find authoritative source for that procedure
4. Rewrite as:
   a) Describe WHAT exists
   b) State PURPOSE
   c) Point to authoritative source for HOW

Example:

BEFORE (Prescriptive):
"To bootstrap: First read X, then Y, finally Z. Run these commands..."

AFTER (Descriptive):
"**Bootstrap System**
Purpose: Activate Claude instances
Bootstrap files: [list]
For procedures: See BOOTSTRAP_CLAUDE.md"
```

**Step 3: Verify no information loss**
```markdown
Before saving changes:
- Did we preserve essential information?
- Is the pointer clear and accurate?
- Will new Claude know where to go?
- Did we maintain the README's purpose?
```

**Step 4: Update and document**
```markdown
For each file sanitized:
1. Save changes
2. Add entry to REPO_LOG.md
3. Note severity of issue fixed
4. Reference audit report
```

#### **Sanitization Patterns**

**Pattern 1: Embedded Procedures → Pointer**

```markdown
BEFORE:
## Getting Started
1. Load BOOTSTRAP_CLAUDE.md
2. Search for MISSION_DEFAULT
3. Check README_C status
4. Begin work

AFTER:
## Getting Started
**Purpose:** Initial Claude activation
**Procedure:** See BOOTSTRAP_CLAUDE.md for complete startup sequence
**Current status:** Bootstrap system active
```

**Pattern 2: Command Examples → Reference**

```markdown
BEFORE:
Run these commands:
- project_knowledge_search("MISSION_DEFAULT")
- project_knowledge_search("README_C")

AFTER:
**For command usage:** See BOOTSTRAP_CLAUDE.md section "Initial Searches"
```

**Pattern 3: Directive Language → Descriptive + Pointer**

```markdown
BEFORE:
You must always check README_C before starting work.

AFTER:
**Master state:** Tracked in README_C.md
**State check procedure:** See BOOTSTRAP_CLAUDE.md
```

---

## 📊 AUDIT CHECKLIST

**Before starting audit:**
- [ ] Understand prescriptive vs descriptive distinction
- [ ] Know the hierarchy (Bootstrap > Protocol > README)
- [ ] Have examples of good/bad patterns in mind
- [ ] Ready to document findings thoroughly
- [ ] Confirmed this is Mode 1 (analysis only)

**During audit:**
- [ ] Phase 1: Check critical five first
- [ ] Document every issue found
- [ ] Note severity accurately
- [ ] Check for contradictions
- [ ] Quote problematic text
- [ ] Identify authoritative source

**Before submitting report:**
- [ ] Executive summary complete
- [ ] All issues documented
- [ ] Severities assigned
- [ ] Contradictions analyzed
- [ ] Recommended fixes provided
- [ ] Clear GO/FIX/DEFER recommendation
- [ ] Files packaged in /docs/validation/reports/
- [ ] Zip archive created

---

## 🔧 SANITIZATION CHECKLIST

**Before starting fixes:**
- [ ] Audit report reviewed and approved by Ziggy
- [ ] Specific fixes identified
- [ ] Severity levels to fix determined
- [ ] Confirmed this is Mode 2 (implementation)
- [ ] Read all files to be modified

**During sanitization:**
- [ ] Transform prescriptive → descriptive
- [ ] Add clear pointers to authoritative sources
- [ ] Verify no information loss
- [ ] Maintain README purpose
- [ ] Preserve essential descriptive content

**Before committing:**
- [ ] All approved fixes complete
- [ ] READMEs tested for clarity
- [ ] REPO_LOG entries created
- [ ] No accidental changes to bootstrap/protocol files
- [ ] Commit message references audit report

---

## ⚠️ SAFETY PROTOCOLS

### **DO NOT in Audit Mode (Mode 1):**
- ❌ Make any changes to READMEs
- ❌ Modify bootstrap or protocol files
- ❌ Assume issues need fixing without approval
- ❌ Output reports anywhere except `/docs/validation/reports/`

### **DO NOT in Sanitization Mode (Mode 2):**
- ❌ Fix issues not explicitly approved
- ❌ Remove essential descriptive information
- ❌ Change bootstrap or protocol files
- ❌ Guess at authoritative source references
- ❌ Sanitize without reading the audit report first

### **ALWAYS:**
- ✅ Preserve the authority hierarchy
- ✅ Point to authoritative sources, never duplicate
- ✅ Document all changes in REPO_LOG
- ✅ Ask Ziggy if unclear about approval
- ✅ Maintain README purpose and clarity

---

## 📝 EXAMPLE AUDIT FINDING

```markdown
File: /auditors/README.md
Section: "Getting Started"
Severity: MODERATE

Issue: Contains step-by-step bootstrap instructions

Current text:
"To get started:
1. Read MISSION_DEFAULT.md
2. Search for your current mission
3. Check README_C.md for state
4. Begin work"

Conflicts with: BOOTSTRAP_CLAUDE.md (lines 15-40)
Contradiction? NO (redundant, not contradictory)

Recommended fix:
Replace procedural steps with:
"**Getting Started:** See BOOTSTRAP_CLAUDE.md for complete activation procedures. Current mission status tracked in MISSION_CURRENT.md. Master state in README_C.md."

Rationale: README should describe WHAT the bootstrap system is, not HOW to use it. Bootstrap files are authoritative for procedures.
```

---

## 📝 EXAMPLE SANITIZATION

**Before Sanitization:**
```markdown
# CFA Repository

## How to Use This Repository

Follow these steps to get started:

1. **Initial Setup**
   - Clone the repository
   - Read BOOTSTRAP_CLAUDE.md
   - Load BOOTSTRAP_CFA.md
   - Review BOOTSTRAP_VUDU.md

2. **Daily Workflow**
   - Check README_C.md for current state
   - Search for MISSION_CURRENT.md
   - Review active tasks
   - Begin work

3. **Coordination**
   - Use VUDU protocol for multi-AI work
   - Stage findings in relay/incoming folders
   - Follow VUDU_HEADER_STANDARD format
   - Update VUDU_LOG with entries

Always follow this sequence to avoid confusion.
```

**After Sanitization:**
```markdown
# CFA Repository

## Repository Overview

**Purpose:** Cross-AI adversarial auditing framework for mission-based work

**Key Systems:**
- **Bootstrap:** Claude activation and identity (see `/auditors/Bootstrap/` directory)
- **Mission:** Task management and coordination (see `/missions/` directory)
- **VUDU:** Multi-AI coordination protocol (see `VUDU_PROTOCOL.md`)

**For activation procedures:** See `BOOTSTRAP_CLAUDE.md`
**For mission workflow:** See `MISSION_DEFAULT.md`
**For coordination details:** See `VUDU_PROTOCOL.md`

**Current status:** v3.7.2 - All systems active
**Last updated:** 2025-11-01
```

**Changes made:**
- ❌ Removed step-by-step instructions
- ❌ Removed procedural workflow
- ❌ Removed directive language ("Always follow...")
- ✅ Added descriptive overview (WHAT exists)
- ✅ Added clear pointers to authoritative sources (WHERE to find HOW)
- ✅ Preserved essential status information
- ✅ Maintained README purpose (orientation and navigation)

---

## 🎯 SUCCESS CRITERIA

**Audit is successful when:**

✅ All critical READMEs checked thoroughly
✅ Every issue documented with severity
✅ Contradictions identified clearly
✅ Recommended fixes are specific
✅ Clear recommendation provided (GO/FIX/DEFER)
✅ Ziggy has enough info to make decision
✅ Report packaged in `/docs/validation/reports/`

**Sanitization is successful when:**

✅ All approved fixes implemented
✅ Prescriptive language transformed to descriptive
✅ Clear pointers to authoritative sources
✅ No essential information lost
✅ README purpose preserved
✅ Protocol hierarchy enforced
✅ REPO_LOG updated with changes
✅ No contradictions introduced

---

## ⚖️ THE POINTING RULE

*"READMEs describe the house.
Bootstraps explain how to enter.

When the README gives directions,
it competes with the map.

Let each file do its job:
README says 'here is the kitchen.'
Bootstrap says 'to cook, do this.'

Sanitize finds where they conflict.
Audit reports what needs fixing.
Ziggy decides what gets changed.

Authority flows downward,
never upward.

Bootstrap > Protocol > README.

This is the way."* 🏠📋

---

## 🔗 AUTHORITATIVE REFERENCES

**For audit procedures:**
- TASK_BRIEF_README_AUDIT.md (complete audit workflow)

**For output standards:**
- CODE_CLAUDE_OUTPUT_PROTOCOL.md (Mode 1 vs Mode 2)

**For documentation standards:**
- 88MPH_PROTOCOL.md (Doc_Claude blessing protocol)

**For protocol hierarchy:**
- BOOTSTRAP_CLAUDE.md (primary authority)
- VUDU_PROTOCOL.md (coordination authority)

---

## 🎯 QUICK REFERENCE

**Is README prescriptive (HOW)?**
→ FLAG for sanitization

**Does README describe (WHAT)?**
→ Keep as-is

**Does README point to authority (WHERE)?**
→ Perfect, keep as-is

**Does README contradict bootstrap?**
→ CRITICAL severity

**Does README duplicate bootstrap?**
→ MODERATE severity (redundant)

**Not sure if prescriptive?**
→ Ask: "Does this tell someone HOW to do something?"
→ If yes = prescriptive = needs sanitization

---

**Status:** Active and ready for immediate use
**First use:** TASK_BRIEF_README_AUDIT.md (pre-launch validation)
**Priority:** CRITICAL (blocking external auditor arrival)

🔍 **Keep Authority Clear, Keep READMEs Descriptive** 🔍
