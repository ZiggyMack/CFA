# TASK BRIEF: README Prescriptive/Descriptive Audit

**Version:** 1.0  
**Date:** 2025-10-31  
**Priority:** CRITICAL (Pre-Launch)  
**Tier:** 4 (Focused task)  
**Assigned to:** Code Claude

---

## 🎯 MISSION

**Final pre-flight check before auditor arrival.**

**Check all READMEs for prescriptive language that could:**
1. Contradict bootstrap files
2. Confuse incoming Claudes
3. Override protocol hierarchy
4. Break current system

**Goal:** Ensure READMEs are descriptive (WHAT), not prescriptive (HOW)

---

## 🚨 WHY THIS MATTERS

**The problem:**
```markdown
Bootstrap files (primary authority):
"To bootstrap: Follow BOOTSTRAP_CLAUDE.md"

README might say:
"To bootstrap: Run these commands..."

Incoming Claude sees both:
Which one to follow? ← CONFUSION

Result: System breaks or contradictions surface
```

**The hierarchy that MUST be preserved:**
```markdown
1. Bootstrap files (HOW - authoritative)
2. Protocol files (HOW - specific domains)
3. READMEs (WHAT - descriptive only)

READMEs should POINT to HOW, not BE the HOW.
```

---

## 📋 AUDIT SCOPE

### **Phase 1: Critical Five (DO THIS FIRST)**

**Check these files with extreme care:**

1. **README_C.md** (`/auditors/README_C.md`)
   - Most critical file
   - Master state document
   - Check against BOOTSTRAP_CLAUDE.md

2. **Root README.md** (`/README.md`)
   - First impression
   - Entry point
   - Check against MISSION_DEFAULT.md

3. **Missions README** (`/missions/README.md`)
   - Mission guidance
   - Check against MISSION_DEFAULT.md

4. **Bootstrap README** (if exists: `/Bootstrap/README.md`)
   - Bootstrap navigation
   - Check against individual BOOTSTRAP_*.md files

5. **Relay README** (`/relay/README.md`)
   - Coordination hub
   - Check against VUDU_PROTOCOL.md

**If Phase 1 finds issues:** Report immediately  
**If Phase 1 is clean:** Proceed to Phase 2

---

### **Phase 2: All Other READMEs (AFTER PHASE 1)**

**Scan all remaining READMEs:**
- `/docs/` subdirectories
- `/deployment/` versions
- `/auditors/relay/` folders
- Any other directory READMEs

---

## 🔍 WHAT TO LOOK FOR

### **RED FLAGS (Prescriptive Language):**

**Procedural instructions:**
```markdown
❌ "To bootstrap, follow these steps..."
❌ "First do X, then do Y..."
❌ "You must run..."
❌ "Execute these commands..."
❌ "Follow this workflow..."
```

**Directive language:**
```markdown
❌ "You should..."
❌ "You must..."
❌ "Always do..."
❌ "Never do..."
❌ "Required steps:"
```

**Embedded procedures:**
```markdown
❌ Step-by-step instructions
❌ Command sequences
❌ Workflow diagrams (if prescriptive)
❌ "How to" sections
```

---

### **GREEN PATTERNS (Descriptive Language):**

**Current state descriptions:**
```markdown
✅ "This directory contains..."
✅ "Current files include..."
✅ "Status: [state]"
✅ "Last updated: [date]"
```

**Purpose statements:**
```markdown
✅ "Purpose: [what this is for]"
✅ "Intended for: [audience]"
✅ "Contains: [contents list]"
```

**Proper HOW references:**
```markdown
✅ "For bootstrap procedures, see BOOTSTRAP_CLAUDE.md"
✅ "Coordination details in VUDU_PROTOCOL.md"
✅ "Refer to [authoritative file] for [instructions]"
✅ "Usage: See [protocol file]"
```

---

## 🎯 AUDIT PROCEDURE

### **For Each README:**

**Step 1: Read completely**
- Understand current content
- Note all sections

**Step 2: Classify each section**
```markdown
For each paragraph/section:
- Descriptive (WHAT) → KEEP
- Pointer (WHERE to find HOW) → KEEP  
- Prescriptive (HOW to do it) → FLAG
- Mixed → FLAG for review
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
- Would confuse guests

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
For each issue found:

File: [exact path]
Section: [which part]
Severity: CRITICAL/MODERATE/MINOR
Issue: [what's wrong]
Current text: [quote problematic section]
Authoritative source: [which file has correct info]
Contradiction? YES/NO
Recommended fix: [brief suggestion]
```

---

## 📊 OUTPUT FORMAT

### **Executive Summary:**

```markdown
## README AUDIT REPORT

**Date:** [today]
**Auditor:** Code Claude
**Files Checked:** [N]
**Issues Found:** [N]

### Severity Breakdown:
- CRITICAL: [N] issues
- MODERATE: [N] issues
- MINOR: [N] issues

### Recommendation:
[GO / FIX CRITICAL FIRST / COMPREHENSIVE FIXES NEEDED]
```

---

### **Detailed Findings:**

```markdown
## PHASE 1: CRITICAL FIVE

### 1. README_C.md (/auditors/README_C.md)
**Status:** [CLEAN / ISSUES FOUND]

[If issues:]
**Issue 1:**
- Severity: [CRITICAL/MODERATE/MINOR]
- Location: [section name/line numbers]
- Problem: [description]
- Current text: "[quote]"
- Conflicts with: [bootstrap file]
- Recommended fix: [suggestion]

[Repeat for each issue]

---

### 2. Root README.md (/README.md)
[Same format]

---

[Continue for all 5 critical files]

---

## PHASE 2: ALL OTHER READMES

[If Phase 1 was clean and Phase 2 executed:]

### Clean Files (No Issues):
- /docs/README.md ✅
- /docs/Process/README.md ✅
[list all clean files]

### Files with Issues:
[Same detailed format as Phase 1]
```

---

### **Contradiction Analysis:**

```markdown
## CONTRADICTIONS DETECTED

[If any found:]

### Contradiction 1:
**README says:** "[quote from README]"
**Bootstrap says:** "[quote from bootstrap]"
**Impact:** [how this confuses incoming Claudes]
**Severity:** CRITICAL/MODERATE/MINOR
**Recommended resolution:** [which to keep, how to fix]

[Repeat for each contradiction]
```

---

### **Recommended Fixes:**

```markdown
## FIXES REQUIRED

### CRITICAL (Must fix before launch):
1. [File]: [Issue] → [Specific fix]
2. [File]: [Issue] → [Specific fix]

### MODERATE (Should fix soon):
1. [File]: [Issue] → [Specific fix]

### MINOR (Can defer):
1. [File]: [Issue] → [Specific fix]
```

---

## 🛡️ SAFETY PROTOCOLS

### **DO NOT CHANGE ANYTHING**

**This is audit only.**

**Reasons:**
1. Need Ziggy's review of findings first
2. Some "prescriptive" content might be essential
3. Changes could break current system
4. Bootstrap files might depend on README structure

**Your job:** REPORT, not FIX

---

### **Files to Handle with Extreme Care:**

```markdown
ULTRA-CRITICAL (any issue = report immediately):
- README_C.md
- MISSION_DEFAULT.md (if checking)
- VUDU_PROTOCOL.md (if checking)
- All BOOTSTRAP_*.md files (if checking)

CRITICAL (check thoroughly):
- Root README.md
- /missions/README.md
- /relay/README.md
- /auditors/ subdirectories

STANDARD (normal audit):
- All other READMEs
```

---

## 📋 CHECKLIST

**Before starting:**
- [ ] Understand prescriptive vs descriptive
- [ ] Know the hierarchy (Bootstrap > Protocol > README)
- [ ] Have examples of good/bad in mind
- [ ] Ready to document findings thoroughly

**During audit:**
- [ ] Phase 1: Check critical five first
- [ ] Document every issue found
- [ ] Note severity accurately
- [ ] Check for contradictions
- [ ] Quote problematic text
- [ ] Identify authoritative source

**Before submitting:**
- [ ] Executive summary complete
- [ ] All issues documented
- [ ] Severities assigned
- [ ] Contradictions analyzed
- [ ] Recommended fixes provided
- [ ] Clear GO/NO-GO recommendation

---

## 🎯 SUCCESS CRITERIA

**Audit is successful when:**

✅ All critical five checked thoroughly  
✅ Every issue documented with severity  
✅ Contradictions identified clearly  
✅ Recommended fixes are specific  
✅ Clear recommendation provided (GO/FIX/DEFER)  
✅ Ziggy has enough info to make decision

**NOT successful if:**
❌ Only superficial scan done  
❌ Issues found but not documented  
❌ Severities guessed  
❌ Recommendations vague  
❌ Ziggy can't make decision from report

---

## 💡 EXAMPLES

### **Example: Prescriptive → Descriptive Fix**

**BEFORE (Prescriptive - BAD):**
```markdown
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

**AFTER (Descriptive - GOOD):**
```markdown
## Bootstrap System

**Purpose:** Activate Claude instances for mission work

**Bootstrap files:**
- BOOTSTRAP_CLAUDE.md (primary identity)
- BOOTSTRAP_CFA.md (project context)
- BOOTSTRAP_VUDU.md (coordination)

**For bootstrap procedures:** See individual BOOTSTRAP_*.md files in /Bootstrap/ directory

**Current status:** All bootstrap files active and deployed
```

---

### **Example: Audit Finding Documentation**

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
"For startup procedures, see BOOTSTRAP_CLAUDE.md. Current mission tracked in MISSION_CURRENT.md."

Rationale: README should describe WHAT the bootstrap system is, not HOW to use it. Bootstrap files are authoritative for procedures.
```

---

## ⚖️ THE POINTING RULE

*"READMEs describe the house.  
Bootstraps explain how to enter.  
  
When the README gives directions,  
it competes with the map.  
  
Let each file do its job:  
README says 'here is the kitchen.'  
Bootstrap says 'to cook, do this.'  
  
Audit finds where they conflict.  
Report finds what needs fixing.  
Ziggy decides what gets changed."* 🏠📋

---

## 🎯 FINAL NOTES

**Time estimate:** 45-60 minutes
- Phase 1 (critical 5): 25-35 minutes
- Phase 2 (all others): 20-25 minutes

**Token budget:** 
- Bootstrap: ~8-10%
- Audit work: ~75-80%
- Report: ~10-15%

**Expected finding rate:**
- If system is clean: 0-3 issues
- If drift has occurred: 5-15 issues
- If major problems: 20+ issues

**Launch decision:**
- 0-3 minor issues: GO
- 4-10 moderate issues: FIX CRITICAL, then GO
- 10+ or any critical: FIX FIRST, then launch

---

**Status:** Ready for Code Claude  
**Priority:** CRITICAL - blocking guest arrival  
**Timeline:** Complete before Grok/Nova activation

🔍 **Audit First, Fix Second, Launch Third** 🔍
