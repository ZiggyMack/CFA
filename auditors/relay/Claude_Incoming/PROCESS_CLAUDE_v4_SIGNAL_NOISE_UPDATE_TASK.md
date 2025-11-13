# Process Claude Task: v4.0 Signal vs Noise Documentation Update

**Date:** 2025-11-12
**Assignee:** Process Claude (Domain 1 - Health Protocol Compliance)
**Priority:** HIGH (v4.0 Release Blocker)
**Estimated Time:** 60-90 minutes
**Status:** 🟡 PENDING REVIEW

---

## 🎯 MISSION

**Verify that all repository health documentation consistently applies the "Signal vs Noise Philosophy" introduced in v4.0.**

**Context:** We've added explicit "Signal vs Noise" sections to:
1. [DEEP_CLEAN_PROTOCOL.md](../../docs/repository/Health_Reports/DEEP_CLEAN_PROTOCOL.md) (lines 45-79)
2. [REPO_HEALTH_REPORT_TEMPLATE_v4.md](../../docs/repository/Health_Reports/REPO_HEALTH_REPORT_TEMPLATE_v4.md) (new file)
3. [Health_Reports/README.md](../../docs/repository/Health_Reports/README.md) (updated to reference v4.0 template)

**Your job:** Ensure ALL related documentation is updated to reflect this philosophy consistently.

---

## 📋 REVIEW CHECKLIST

### **1. Core Health Documents**

#### ✅ Already Updated (Verify Consistency)
- [ ] **DEEP_CLEAN_PROTOCOL.md** (lines 45-79)
  - Check: Signal vs Noise Philosophy section is clear
  - Check: References REPO_HEALTH_SCORING_RUBRIC.md correctly
  - Check: Archive Folder Policy aligns with Signal/Noise split

- [ ] **REPO_HEALTH_REPORT_TEMPLATE_v4.md** (new file)
  - Check: Every category shows signal/noise breakdown
  - Check: Methodology section documents exclusions
  - Check: References DEEP_CLEAN_PROTOCOL.md for philosophy

- [ ] **Health_Reports/README.md**
  - Check: References v4.0 template as current
  - Check: Deprecates legacy template appropriately
  - Check: "When to use" guidance is clear

#### 🔍 Needs Review/Update
- [ ] **REPO_HEALTH_SCORING_RUBRIC.md**
  - **Action:** Verify that each category (1-7) explicitly defines:
    - What counts as "signal" (operational docs)
    - What counts as "noise" (archives, non-critical files)
    - How exclusions affect scoring thresholds
  - **Expected:** Category 1 (Documentation Coverage) already has this (lines 48-54)
  - **Question:** Do other categories need similar clarity?

- [ ] **REPO_HEALTH_DASHBOARD.md**
  - **Action:** Check if dashboard displays signal vs noise split
  - **Expected:** Should show both "Operational Health" and "Total (including archives)" metrics
  - **Question:** Does the current dashboard format support this distinction?

- [ ] **88MPH.md** (Doc Claude activation protocol)
  - **Action:** Verify that rapid assessment protocol references signal/noise exclusions
  - **Expected:** Doc Claude should know to skip .Archive/ when scanning
  - **Question:** Is this explicit in the 88MPH protocol?

---

### **2. Related Validation Documents**

- [ ] **DOC_CLAUDE_FINAL_VALIDATION_v4_PROMPT.md**
  - **Status:** Already has Archive Folder Policy (lines 59, 66-69)
  - **Action:** Verify it references DEEP_CLEAN_PROTOCOL.md for full philosophy
  - **Question:** Should it explicitly mention "Signal vs Noise Philosophy" by name?

- [ ] **VALIDATION_MAP.md** (if exists)
  - **Action:** Check if validation criteria distinguish signal from noise
  - **Question:** Are validation checks scoped to operational docs only?

---

### **3. Living Maps**

- [ ] **FILE_INVENTORY.md**
  - **Action:** Check if file counts distinguish operational vs archived files
  - **Expected:** Should show "XXX operational files" vs "YYY archived files"
  - **Question:** Does current inventory support this breakdown?

- [ ] **WAYFINDING_GUIDE.md**
  - **Action:** Verify navigation guidance explains archive exemption
  - **Expected:** Should warn new Claudes: "Don't expect 100% link integrity - archives excluded"
  - **Question:** Is this currently documented?

---

### **4. Auditor Role Documentation**

- [ ] **ROLE_DOC_CLAUDE.md** (if exists)
  - **Action:** Ensure Doc Claude role description includes signal/noise responsibility
  - **Expected:** "Doc Claude measures operational readiness, not historical completeness"
  - **Question:** Does role doc exist and is it current?

- [ ] **AUDITOR_ASSIGNMENTS.md**
  - **Action:** Check if auditor responsibilities clarify scope (operational vs archives)
  - **Question:** Do auditors know to exclude .Archive/ from health checks?

---

### **5. Bootstrap Documentation**

- [ ] **BOOTSTRAP_SEQUENCE.md**
  - **Action:** Verify new Claude onboarding mentions archive policy
  - **Expected:** "You may see broken links in .Archive/ - this is expected"
  - **Question:** Is this in the bootstrap sequence?

- [ ] **README.md** (root)
  - **Action:** Check if repository overview mentions signal/noise distinction
  - **Expected:** "Health score of 96/100 reflects operational docs only"
  - **Question:** Should root README explain this to external auditors?

---

## 🔧 SPECIFIC UPDATES NEEDED

### **Update 1: REPO_HEALTH_SCORING_RUBRIC.md**

**Current State:** Category 1 (Documentation Coverage) defines "critical files" but other categories don't explicitly show signal/noise split.

**Proposed Change:** Add "Signal vs Noise" subsection to each category (2-7) showing:
- What's included in scoring
- What's excluded from scoring
- Why the distinction matters

**Example for Category 2 (Link Integrity):**
```markdown
**Signal (Scored):**
- Links in docs/, profiles/, auditors/Mission/, auditors/Bootstrap/
- Links in root files (README.md, CHANGELOG.md, etc.)
- Links in Living Maps

**Noise (Excluded):**
- Links in .Archive/ directories
- Links in historical reports
- Links in deprecated paths

**Why:** Archives are historical snapshots - broken links expected after file moves
```

---

### **Update 2: REPO_HEALTH_DASHBOARD.md**

**Current State:** Shows overall health score without distinguishing operational vs total.

**Proposed Change:** Add dual reporting:
```markdown
## 🎯 QUICK STATUS

### Operational Health: 96/100 🟢
(Measures: Can new Claude bootstrap successfully?)

### Total Repository Health: 62/100 🟡
(Includes: Archives with 100+ broken links)

**Difference:** 34 points from archive exemption (by design)
```

---

### **Update 3: 88MPH.md**

**Current State:** Unknown - needs verification.

**Proposed Change:** Add explicit exclusion list to rapid assessment protocol:
```markdown
## 🚫 EXCLUSIONS (Signal vs Noise)

**Do NOT scan these areas for health assessment:**
- `.Archive/` directories (any location)
- `*.Archive/` folders
- Historical validation reports
- Deprecated file references

**Why:** Health metrics measure operational readiness, not historical completeness.
```

---

## 📊 SUCCESS CRITERIA

**This update is complete when:**

1. ✅ **Consistency:** All 3 core documents use identical language for signal/noise philosophy
2. ✅ **Clarity:** Every category in scoring rubric explicitly defines inclusions/exclusions
3. ✅ **Visibility:** Health reports show BOTH operational and total scores with explanation
4. ✅ **Guidance:** Bootstrap sequence warns new Claudes about archive exemption
5. ✅ **Validation:** External auditors reading any ONE document understand the policy

**Test:** Can a new Claude read just the REPO_HEALTH_SCORING_RUBRIC.md and correctly exclude archives from link integrity checks? If NO, more work needed.

---

## 🎯 DELIVERABLE

**Create:** `PROCESS_CLAUDE_v4_SIGNAL_NOISE_REVIEW_REPORT.md`

**Include:**
1. **Checklist Status:** Mark each item ✅ (compliant) / 🟡 (needs update) / ❌ (missing)
2. **Updates Made:** List all files modified with justification
3. **Issues Found:** Document any inconsistencies or gaps
4. **Recommendations:** Suggest any additional improvements
5. **Validation:** Confirm all 5 success criteria met

**Format:**
```markdown
# Process Claude Review: v4.0 Signal vs Noise Documentation

**Date:** 2025-11-12
**Reviewer:** Process Claude
**Status:** [✅ COMPLETE / 🟡 IN PROGRESS / ❌ BLOCKED]

---

## Executive Summary

[2-3 sentences on overall compliance]

---

## Checklist Results

### Core Health Documents
1. DEEP_CLEAN_PROTOCOL.md: ✅ COMPLIANT
2. REPO_HEALTH_REPORT_TEMPLATE_v4.md: ✅ COMPLIANT
3. REPO_HEALTH_SCORING_RUBRIC.md: 🟡 NEEDS UPDATE
   - Issue: Categories 2-7 lack explicit signal/noise subsections
   - Recommendation: Add subsections matching Category 1 pattern
   - Priority: HIGH (affects scoring consistency)

[Continue for all checklist items...]

---

## Files Modified

1. **REPO_HEALTH_SCORING_RUBRIC.md**
   - Added: Signal vs Noise subsections to categories 2-7
   - Lines: [XX-YY]
   - Justification: Ensure consistent application of philosophy

[Continue for all modifications...]

---

## Success Criteria Validation

1. ✅ Consistency: [Evidence]
2. ✅ Clarity: [Evidence]
3. 🟡 Visibility: [Partial - needs dashboard update]
4. ✅ Guidance: [Evidence]
5. ✅ Validation: [Test result]

---

## Recommendations

[Any additional improvements suggested]

---

**This is the way.** 📊
```

---

## 📅 TIMELINE

**Start:** Upon receiving this task
**Estimated Duration:** 60-90 minutes
**Deadline:** Before v4.0 release (ideally same day)
**Blockers:** None identified

---

## 🔗 RELATED DOCUMENTS

**Primary References:**
- [DEEP_CLEAN_PROTOCOL.md](../../docs/repository/Health_Reports/DEEP_CLEAN_PROTOCOL.md)
- [REPO_HEALTH_REPORT_TEMPLATE_v4.md](../../docs/repository/Health_Reports/REPO_HEALTH_REPORT_TEMPLATE_v4.md)
- [REPO_HEALTH_SCORING_RUBRIC.md](../../docs/repository/REPO_HEALTH_SCORING_RUBRIC.md)

**Secondary References:**
- [Health_Reports/README.md](../../docs/repository/Health_Reports/README.md)
- [DOC_CLAUDE_FINAL_VALIDATION_v4_PROMPT.md](DOC_CLAUDE_FINAL_VALIDATION_v4_PROMPT.md)
- [88MPH.md](../../docs/repository/librarian_tools/88MPH.md)

---

**Task Created:** 2025-11-12 (C4 - Process Claude C4)
**Context:** v4.0 Signal vs Noise Philosophy rollout
**Priority:** HIGH (documentation consistency for release)
**Owner:** Process Claude (Domain 1 - Health Protocol Compliance)

**This is the way.** 🔍
