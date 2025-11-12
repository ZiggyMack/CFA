<!---
FILE: PROCESS.md
PURPOSE: Critical process documentation - learned from actual failures
VERSION: v1.0
STATUS: Active
DEPENDS_ON: None (root process reference)
NEEDED_BY: All auditors, all Claudes, all development work
MOVES_WITH: /docs/Process/
LAST_UPDATE: 2025-11-02 [DOCUMENTATION-2025-11-02-09]
--->

# PROCESS.md - When We Forget, We Get Burned

**Purpose:** Document critical processes learned from actual failures
**Philosophy:** Process isn't bureaucracy - it's scar tissue from mistakes
**Version:** v1.0
**Status:** Active - Add entries as we learn

────────────────────────────────────────────────────

## 🔥 **WHY THIS FILE EXISTS**

Everyone deviates from process from time to time.
It's human. It happens.

But when you're managing a complex multi-AI system with:
- 150+ files
- 4-tier bootstrap system
- Multi-Claude coordination
- Tiered documentation dependencies

...forgetting process doesn't just slow you down.
**It creates silent failures that surface days later.**

This file documents processes **we actually forgot** and **what broke because of it.**

**Not theory. Not best practices. Scars.**

────────────────────────────────────────────────────

## 📋 **HOW TO USE THIS FILE**

### When Starting Work:
1. Read the process relevant to your task
2. Follow the steps (they're there for a reason)
3. Check off each step as you complete it

### When You Get Burned:
1. Document what happened
2. Document the process you should have followed
3. Add it to this file
4. Help the next Claude (or yourself) avoid the same mistake

### When You're Tempted to Skip Steps:
1. Read the "What Broke" section of that process
2. Decide if you want to create that same problem
3. Follow the process

────────────────────────────────────────────────────

## 🔥 **PROCESS #1: METHODOLOGY CHANGE PROCESS**

**When to use:** Anytime you change how we measure, categorize, or define something system-wide

**Why it matters:** Methodology changes ripple through documentation, source files, and reports

### ⚠️ **WHAT BROKE WHEN WE SKIPPED THIS**

**Date:** November 2, 2025
**Change:** Split header coverage into "core files" (87%) vs "total files" (40%)
**What we updated:** `/docs/repository/REPO_HEALTH_DASHBOARD.md` (formerly DASHBOARD.md)
**What we forgot:** Doc Claude's source files

**Result:**
- Doc Claude activated 3 commits later
- Reported "Header Coverage: 40% 🔴" without context
- Made it look like we had poor coverage
- Actually, 87% of **critical files** had headers (excellent)
- Stale data in MASTER_DEPENDENCY_MAP.md and BOOTSTRAP_DOC_CLAUDE.md
- Had to fix retroactively, create extra commit, document the oversight

**The Burn:**
- Wasted time diagnosing "why is Doc Claude reporting stale data?"
- Created confusion about actual repository health
- Extra commit to fix what should have been caught initially
- Lost confidence in Doc Claude's reporting until we traced the issue

**What we should have done:** Follow the process below ⬇️

────────────────────────────────────────────────────

### ✅ **THE PROCESS (Step-by-Step)**

#### **Step 1: Make the Initial Change**
- [ ] Update the primary file with the new methodology
- [ ] Document why the methodology changed
- [ ] Note the old methodology for context

**Example:** Updated REPO_HEALTH_DASHBOARD.md to show 87% core / 40% total split

---

#### **Step 2: CONSULT VALIDATION CLAUDE**

**Critical Question:** *"I just changed [X methodology]. What else in the repository needs updating to reflect this change?"*

**Why this step matters:**
- VALIDATION Claude knows dependency chains
- VALIDATION Claude can search across all files
- VALIDATION Claude thinks in "what else?"
- You can't remember every file that references a metric

**What to ask:**
```markdown
VALIDATION CLAUDE:

I just changed the header coverage methodology from a single metric
to a core/total split:
- Core files: 87% (critical operational files)
- Total files: 40% (includes archives/Python/noise)

I've updated REPO_HEALTH_DASHBOARD.md to reflect this.

What other files reference header coverage metrics and need updating?
```

**What VALIDATION Claude would have found:**
- MASTER_DEPENDENCY_MAP.md (line 846) - references "40% of files"
- BOOTSTRAP_DOC_CLAUDE.md (lines 159-170) - references header coverage targets
- Any other files that cite header coverage statistics

---

#### **Step 3: Update ALL Identified Files**

- [ ] Make a checklist of every file VALIDATION Claude identified
- [ ] Update each file with the new methodology
- [ ] Add context/explanation where needed
- [ ] Cross off each file as you complete it

**Example:**
```markdown
Files to update:
- [x] REPO_HEALTH_DASHBOARD.md (primary change)
- [x] MASTER_DEPENDENCY_MAP.md (weakness section)
- [x] BOOTSTRAP_DOC_CLAUDE.md (success metrics)
```

---

#### **Step 4: Verify Completeness**

- [ ] Ask VALIDATION Claude: "Did I miss anything?"
- [ ] Search for old methodology terms to catch stragglers
- [ ] Spot check 2-3 related files manually

**Example searches:**
- Search for old metric format: "40%" without "core/total" context
- Search for old terminology: "header coverage" as single concept

---

#### **Step 5: Document the Change**

- [ ] Update REPO_LOG with methodology change
- [ ] Note which files were updated
- [ ] Explain why the methodology changed
- [ ] Create single commit with all related changes

**Example REPO_LOG entry:**
```markdown
[DOCUMENTATION-2025-11-02-N] Header Coverage Methodology Change
- Changed from single metric to core/total split
- Updated: REPO_HEALTH_DASHBOARD.md, MASTER_DEPENDENCY_MAP.md, BOOTSTRAP_DOC_CLAUDE.md
- Reason: Better reflect operational excellence vs aspirational total coverage
```

---

#### **Step 6: Commit Everything Together**

- [ ] Stage ALL files related to the methodology change
- [ ] Create comprehensive commit message
- [ ] Reference the methodology change explicitly
- [ ] Push changes

**Why together:** Prevents partial updates, makes revert easy if needed

────────────────────────────────────────────────────

### 🎯 **CHECKLIST VERSION (Quick Reference)**

When changing any methodology:

```markdown
METHODOLOGY CHANGE CHECKLIST
- [ ] Make initial change in primary file
- [ ] CONSULT VALIDATION CLAUDE: "What else needs updating?"
- [ ] Create file update checklist from VALIDATION's findings
- [ ] Update ALL identified files
- [ ] Verify completeness (ask VALIDATION: "Did I miss anything?")
- [ ] Document change in REPO_LOG
- [ ] Commit all related changes together
- [ ] Push changes
```

────────────────────────────────────────────────────

### 💡 **KEY INSIGHTS**

**Why we skip this process:**
- Feels bureaucratic when you "just need to update one thing"
- VALIDATION Claude consultation feels like overkill
- Easy to think "I know all the places this touches"

**Why that thinking is wrong:**
- You don't know every reference (150+ files)
- Methodology changes have non-obvious dependencies
- Doc Claude bootstraps from specific source files
- Stale data creates compound problems downstream

**The reality:**
- VALIDATION Claude query: 2 minutes
- Updating files you would have missed: 5 minutes
- Total overhead: ~7 minutes

**The cost of skipping:**
- 3 commits later: "Why is this data stale?"
- 15 minutes diagnosing the problem
- 10 minutes fixing retroactively
- 5 minutes documenting the failure
- Confusion about repository health
- Total cost: ~30 minutes + loss of trust

**The math is clear:** 7 minutes of process saves 30 minutes of cleanup.

────────────────────────────────────────────────────

### 🔄 **WHEN TO USE THIS PROCESS**

**Always use for:**
- ✅ Changing measurement methodologies (like header coverage split)
- ✅ Renaming concepts system-wide (like README_Claude → DOC_CLAUDE)
- ✅ Changing directory structures or file locations
- ✅ Updating success criteria or targets
- ✅ Modifying multi-file systems (like VuDu format changes)

**Maybe use for:**
- 🤔 Updating a single metric in one place (but ask yourself: is it really just one place?)
- 🤔 Fixing typos (unless the typo is in a key term referenced elsewhere)

**Don't need for:**
- ❌ Adding new content that doesn't change existing concepts
- ❌ Creating net-new files with no dependencies
- ❌ Fixing obvious isolated bugs

────────────────────────────────────────────────────

## 📚 **PROCESS TEMPLATE (For Future Entries)**

When adding a new process to this file, use this structure:

```markdown
## 🔥 **PROCESS #N: [PROCESS NAME]**

**When to use:** [Trigger conditions]
**Why it matters:** [One-line impact]

### ⚠️ **WHAT BROKE WHEN WE SKIPPED THIS**
- Date
- What we did
- What we forgot
- What broke
- The cost (time, confusion, trust)

### ✅ **THE PROCESS (Step-by-Step)**
[Detailed steps with checkboxes]

### 🎯 **CHECKLIST VERSION (Quick Reference)**
[Condensed checklist for quick use]

### 💡 **KEY INSIGHTS**
- Why we skip this
- Why that's wrong
- The math (process time vs cleanup time)

### 🔄 **WHEN TO USE THIS PROCESS**
- Always use for: [scenarios]
- Maybe use for: [edge cases]
- Don't need for: [exceptions]
```

────────────────────────────────────────────────────

## 🎯 **REMEMBER**

**Process isn't bureaucracy.**
**Process is institutional memory.**

Every step in these processes exists because:
- We forgot it once
- Something broke
- We learned the hard way

Don't repeat our mistakes.
Use the scars we've documented.

**From forgetting, we learned.**
**From learning, we documented.**
**From documentation, you can avoid the burn.**

────────────────────────────────────────────────────

## 📝 **PROCESS INDEX**

1. **Methodology Change Process** - When you change how we measure/define things system-wide
2. [Future processes added as we learn...]

────────────────────────────────────────────────────

**"Everyone deviates from process. The question is whether you learn from it."** 🔥

────────────────────────────────────────────────────
**File:** PROCESS.md
**Purpose:** Critical process documentation from actual failures
**Version:** v1.0
**Status:** Living document - grows with experience

**"Process is scar tissue. These are our scars."** 📚
