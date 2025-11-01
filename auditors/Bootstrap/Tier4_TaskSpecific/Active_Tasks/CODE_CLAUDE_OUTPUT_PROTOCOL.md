# CODE CLAUDE OUTPUT PROTOCOL

**Version:** 1.0  
**Date:** 2025-10-31  
**Purpose:** Standardize where Code Claude puts analysis/reports vs actual changes

---

## 🎯 THE DISTINCTION

**Code Claude operates in two modes:**

### **Mode 1: ANALYSIS (No repo changes)**
```markdown
Task: Audit, scan, analyze, report
Output: Findings, reports, recommendations
Action: NO changes to repo
Destination: /docs/validation/reports/
```

### **Mode 2: IMPLEMENTATION (Repo changes)**
```markdown
Task: Fix, update, refactor, implement
Output: Changed files in repo
Action: Direct repo modifications
Destination: Actual file locations in repo
```

**This protocol covers MODE 1 (Analysis).**

---

## 📁 STANDARD OUTPUT LOCATION

**For all analysis tasks:**

```
/docs/validation/reports/
```

**This directory already exists.**

**Structure:**
```
/docs/validation/reports/
├── YYYY-MM-DD_[TASK_NAME]/
│   ├── REPORT.md (main findings)
│   ├── DETAILS.md (technical details)
│   ├── RECOMMENDATIONS.md (what to do)
│   └── [supporting files]
└── [next task folder]
```

---

## 📦 PACKAGING PROTOCOL

**For analysis tasks, Code Claude should:**

### **Step 1: Create dated folder**
```bash
Format: YYYY-MM-DD_TASK_NAME
Example: 2025-10-31_README_AUDIT
```

### **Step 2: Generate report files**
```markdown
Required files:
1. REPORT.md
   - Executive summary
   - Key findings
   - Go/no-go recommendation

2. DETAILS.md (if needed)
   - Technical analysis
   - Specific examples
   - Evidence

3. RECOMMENDATIONS.md (if needed)
   - Specific fixes needed
   - Priority order
   - Implementation guidance
```

### **Step 3: Package everything**
```bash
Create: /docs/validation/reports/YYYY-MM-DD_TASK_NAME.zip

Contents:
├── REPORT.md
├── DETAILS.md
├── RECOMMENDATIONS.md
└── [any other files]

Then:
├── Leave zip in /docs/validation/reports/
└── Also expand folder for browsing
```

### **Step 4: Notify completion**
```markdown
Analysis complete.

Report location:
/docs/validation/reports/2025-10-31_README_AUDIT.zip

Summary: [brief findings]
Recommendation: [GO/FIX/DEFER]
Next steps: [what Ziggy should do]
```

---

## 🎯 EXAMPLE: README AUDIT TASK

**Task:** Audit all READMEs for prescriptive language

**Code Claude should:**

```markdown
1. Perform audit (no changes to repo)

2. Create folder:
   /docs/validation/reports/2025-10-31_README_AUDIT/

3. Generate files:
   - REPORT.md (findings summary)
   - CRITICAL_ISSUES.md (must-fix items)
   - MODERATE_ISSUES.md (should-fix items)
   - CLEAN_FILES.md (no issues found)

4. Create zip:
   /docs/validation/reports/2025-10-31_README_AUDIT.zip

5. Report to Ziggy:
   "README audit complete.
    Report: /docs/validation/reports/2025-10-31_README_AUDIT.zip
    Found: X critical, Y moderate, Z minor issues
    Recommendation: [FIX CRITICAL FIRST / GO / DEFER]"
```

**Ziggy then:**
- Reviews report
- Decides: go / fix / iterate
- Creates fix task if needed (Mode 2)

---

## 📋 TASK BRIEF TEMPLATE ADDITION

**Add this section to analysis task briefs:**

```markdown
## 📦 OUTPUT PROTOCOL

**This is an ANALYSIS task (no repo changes).**

Your deliverables should be placed in:
`/docs/validation/reports/YYYY-MM-DD_[TASK_NAME]/`

Required files:
1. REPORT.md - Executive summary and recommendation
2. DETAILS.md - Full findings and analysis
3. RECOMMENDATIONS.md - Specific fixes needed (if any)

Package everything into:
`/docs/validation/reports/YYYY-MM-DD_[TASK_NAME].zip`

**Do NOT make changes to the actual repo files.**
**This is report-only. Fixes come later if approved.**

Upon completion, notify with:
- Location of report
- Brief summary of findings
- Clear GO/FIX/DEFER recommendation
```

---

## 🔄 WORKFLOW COMPARISON

### **Analysis Workflow (Mode 1):**
```
Ziggy: "Audit the READMEs"
  ↓
Code Claude: 
  - Scans files
  - Generates report
  - Places in /docs/validation/reports/
  - Notifies Ziggy
  ↓
Ziggy:
  - Reviews report
  - Decides action
  ↓
If fixes needed:
  Ziggy: "Fix items in CRITICAL_ISSUES.md"
  (This becomes Mode 2)
```

### **Implementation Workflow (Mode 2):**
```
Ziggy: "Fix these 5 README issues"
  ↓
Code Claude:
  - Modifies actual files
  - Updates repo
  - Commits changes
  - Updates REPO_LOG
  ↓
Ziggy:
  - Reviews changes
  - Approves/iterates
```

---

## 🎯 UPDATED README AUDIT BRIEF

**Add this section to TASK_BRIEF_README_AUDIT.md:**

```markdown
## 📦 OUTPUT DELIVERABLES

**This is an ANALYSIS task - no repo changes.**

Place all findings in:
`/docs/validation/reports/2025-10-31_README_AUDIT/`

Required files:
1. **REPORT.md** - Executive summary
   - Files checked: [N]
   - Issues found: [N by severity]
   - Recommendation: GO/FIX/DEFER

2. **CRITICAL_ISSUES.md** - Must fix before launch
   - Each issue with file, section, severity
   - Exact text quoted
   - Recommended fix
   - Impact analysis

3. **MODERATE_ISSUES.md** - Should fix soon
   - Same format as critical

4. **MINOR_ISSUES.md** - Can defer
   - Same format

5. **CLEAN_FILES.md** - No issues found
   - List all files that passed audit

6. **CONTRADICTIONS.md** (if any)
   - README says vs Bootstrap says
   - Impact on incoming Claudes
   - Resolution recommendation

Package as:
`/docs/validation/reports/2025-10-31_README_AUDIT.zip`

**Do NOT modify any README files.**
**Report only. Fixes require separate task.**
```

---

## 📋 CODE CLAUDE CHECKLIST

**Before starting analysis task:**
- [ ] Confirm this is Mode 1 (analysis only)
- [ ] Know output goes to /docs/validation/reports/
- [ ] Understand packaging protocol
- [ ] Won't modify repo files

**During analysis:**
- [ ] Perform thorough analysis
- [ ] Document all findings
- [ ] Create required report files
- [ ] Organize by severity/category

**Before completing:**
- [ ] All required files created
- [ ] Folder created with date_taskname format
- [ ] Zip package created
- [ ] Clear recommendation provided
- [ ] Ziggy notification prepared

---

## 🚨 CRITICAL DISTINCTIONS

### **Analysis Tasks (Mode 1) Include:**
- Audits
- Scans  
- Health checks
- Dependency analysis
- Code reviews
- Pattern detection
- Recommendation generation

**Output:** Reports in /docs/validation/reports/

---

### **Implementation Tasks (Mode 2) Include:**
- Fixes
- Refactors
- Updates
- Migrations
- Optimizations
- New features
- Bug fixes

**Output:** Modified files in actual repo locations

---

## 💡 WHY THIS MATTERS

**Without this protocol:**
```markdown
❌ Code Claude might modify files during "analysis"
❌ Reports might go to random locations
❌ Ziggy can't find outputs
❌ No staged approval process
❌ Risky changes without review
```

**With this protocol:**
```markdown
✅ Clear separation: analyze vs implement
✅ Standard report location
✅ Ziggy reviews before changes
✅ Staged approval workflow
✅ Safe iteration process
```

---

## 🎯 INTEGRATION POINTS

**Update these files to reference this protocol:**

1. **88MPH.md** (Doc_Claude)
   - Add reference to report location
   - Note Mode 1 vs Mode 2

2. **All analysis task briefs**
   - Add output protocol section
   - Specify /docs/validation/reports/
   - Packaging requirements

3. **BOOTSTRAP_CLAUDE.md** (if Code Claude section exists)
   - Note the two modes
   - Standard output locations

4. **Code Claude activation docs** (when created)
   - Core protocol reference
   - Examples of both modes

---

## ⚖️ THE POINTING RULE

*"Code Claude has two hats:  
The analyst and the fixer.  
  
When analyzing,  
reports go to validation.  
When fixing,  
changes go to repo.  
  
Never confuse the two.  
Analysis without approval  
stays in reports.  
  
Only approved fixes  
touch the actual code."* 🎩📊

---

## 🎯 QUICK REFERENCE

**Is this an analysis task?**
→ Output to `/docs/validation/reports/YYYY-MM-DD_TASKNAME/`

**Is this an implementation task?**
→ Output to actual repo file locations

**Not sure?**
→ If you're recommending changes (not making them) = Analysis  
→ If you're making changes = Implementation

**Always zip analysis reports:**
→ Makes download easy for Ziggy  
→ Keeps reports organized  
→ One package per task

---

**Status:** Ready for immediate use  
**Integration:** Add to all analysis task briefs  
**First use:** README_AUDIT task

📦 **Know Where Your Reports Go** 📦
