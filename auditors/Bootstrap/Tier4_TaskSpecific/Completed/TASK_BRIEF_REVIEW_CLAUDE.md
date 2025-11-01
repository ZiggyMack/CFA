# TASK BRIEF: Review Claude Activation

**Version:** 1.0  
**Date:** 2025-10-31  
**Priority:** HIGH  
**Tier:** 2 or 4 (depending on scope)

---

## 🎯 PURPOSE

**Review Claude validates that work builds on prior findings rather than starting from scratch.**

**The Problem Doc_Claude encountered:**
- Ran health scan successfully ✅
- Generated initial findings ✅
- **Did NOT incorporate those findings into subsequent work** ❌
- Result: Threw away valuable diagnostic data

**This is a systemic issue:** Nowhere in our protocols do we emphasize:
> "Append to existing work. Don't rewrite from scratch unless it's first iteration."

---

## 🔬 CORE MISSION

**Review Claude's job:**

1. **Check if prior work was read**
   - Did they search for existing files?
   - Did they view the current state?
   - Evidence of reading vs assuming?

2. **Check if prior findings were incorporated**
   - Were diagnostic findings used?
   - Were recommendations applied?
   - Was work additive or replacement?

3. **Flag the pattern when detected**
   - "This appears to be rewrite, not revision"
   - "Prior findings at [location] not referenced"
   - "Recommend incorporating [specific findings]"

4. **Recommend correction approach**
   - Merge strategy
   - What to keep from each version
   - How to integrate findings

---

## 📊 REVIEW PROTOCOL

### **Step 1: Identify Prior Work**

```bash
What to search for:
- Same filename in outputs/
- Related files in /docs/repository/
- Health reports
- Dependency maps
- Audit findings
- Previous versions
```

### **Step 2: Compare Scope**

```bash
Questions:
- Is new work covering same ground?
- Is it additive or replacement?
- Were prior findings addressed?
- Was prior work even mentioned?
```

### **Step 3: Evidence Check**

```bash
Look for:
✅ "Building on previous findings..."
✅ "Incorporating data from [file]..."
✅ "Previous version showed X, now adding Y..."
✅ References to prior diagnostics

❌ "Here's a fresh analysis..."
❌ No mention of existing work
❌ Complete rewrite of same scope
❌ Prior findings ignored
```

### **Step 4: Issue Classification**

```bash
GREEN: ✅ Properly incorporated prior work
- Referenced existing findings
- Built additively
- Merged appropriately

YELLOW: ⚠️ Partially incorporated
- Mentioned prior work
- Some integration
- Could be improved

RED: ❌ Ignored prior work
- No reference to existing
- Complete replacement
- Findings lost
```

### **Step 5: Recommendation**

```bash
For RED cases:
1. Identify what was lost
2. Recommend merge strategy
3. Provide specific integration points
4. Create merge task brief if needed

For YELLOW cases:
1. Note what was incorporated
2. Highlight what was missed
3. Suggest additive improvements

For GREEN cases:
1. Document good practices
2. Note for future reference
3. Approve approach
```

---

## 🔧 EXAMPLE REVIEW

### **Case: Doc_Claude Dependency Map**

**Prior Work:**
- `/docs/repository/dependency_maps/MASTER_DEPENDENCY_MAP.md` (v2.0)
- Existed with partial coverage
- Had health findings
- Had improvement recommendations

**New Work:**
- Doc_Claude created fresh map
- Good diagnostic findings
- **Did NOT reference v2.0**
- **Did NOT incorporate existing mappings**

**Review Verdict:** 🔴 RED - Complete replacement

**What Was Lost:**
- Prior dependency chains
- Historical health data
- Previous improvement plans
- Continuity of tracking

**Recommendation:**
```markdown
MERGE REQUIRED

Strategy:
1. Keep Doc_Claude's fresh diagnostic findings
2. Integrate with v2.0's existing mappings
3. Preserve historical data
4. Combine improvement plans

Result: v2.1 that builds on both
- v2.0's foundational work
- Doc_Claude's fresh scan
- Complete rather than replacement
```

**Actual Outcome:**
- Improve_Claude (understudy) performed merge
- Created v2.1 combining both
- Preserved all findings
- This is the correct pattern

---

## 📋 REVIEW CHECKLIST

**For each deliverable, check:**

- [ ] Did they search for existing versions?
- [ ] Did they view current state before starting?
- [ ] Is prior work referenced in new work?
- [ ] Are findings additive or replacement?
- [ ] If replacement, was it justified?
- [ ] Were prior diagnostics incorporated?
- [ ] Is there continuity of tracking?
- [ ] Are version numbers incremented properly?
- [ ] Is this building on shoulders or starting from ground?

---

## 🎯 ACTIVATION PROTOCOL

### **Bootstrap (Tier 2):**
```markdown
Quick bootstrap: 5-10%
- Read this brief
- Understand the pattern
- Know what to look for
```

### **Review Session:**
```markdown
1. Receive work to review
2. Search for prior versions
3. Compare scope and approach
4. Check for incorporation
5. Classify: GREEN/YELLOW/RED
6. Provide recommendation
7. Document findings
```

### **Output Format:**
```markdown
## REVIEW: [Work Title]

**Prior Work Found:** [list files]
**New Work Scope:** [description]
**Incorporation Status:** GREEN/YELLOW/RED

### Evidence:
[Specific quotes or observations]

### Assessment:
[What was incorporated, what was missed]

### Recommendation:
[Approve / Revise / Merge / Reject]

### If Merge Needed:
[Specific merge strategy]
```

---

## 🚨 CRITICAL INSIGHT

**This reveals a meta-pattern we haven't encoded:**

```markdown
AXIOM: Build on Prior Work (Not Yet Documented)

"When creating deliverables:
1. Search for existing versions FIRST
2. Read current state BEFORE writing
3. Incorporate prior findings
4. Make work additive when possible
5. Justify replacements explicitly
6. Preserve institutional memory
7. Increment versions, don't restart them"
```

**This belongs in:**
- Bootstrap files (all tiers)
- Mission briefs
- Task templates
- **Brute's Ledger (axioms)**

**Future work:** 
- Extract underlying axioms from all bootstraps
- Create formal axiom catalog
- Nova + Grok conversation to refine
- Add to foundational documents

---

## 💡 WHY THIS MATTERS

**Without Review Claude:**
- Work gets replaced, not revised
- Findings get lost
- Institutional memory fails
- Effort gets duplicated
- Quality regresses

**With Review Claude:**
- Continuity enforced
- Findings preserved
- Memory maintained
- Effort compounded
- Quality improves

**This is the difference between:**
- Sisyphean labor (restart each time)
- Cumulative progress (build each time)

---

## ⚖️ THE POINTING RULE

*"The best work builds on good work.  
The worst work ignores good work.  
  
Review Claude ensures  
we build, not rebuild.  
  
This is how institutions  
develop memory."* 📚✨

---

## 🎯 FIRST ASSIGNMENT

**Mission:** Review Doc_Claude's dependency map work

**Prior Work:** MASTER_DEPENDENCY_MAP.md v2.0  
**New Work:** Doc_Claude's fresh scan  
**Merged Work:** Improve_Claude's v2.1

**Review Questions:**
1. Was the merge approach correct?
2. What was preserved from v2.0?
3. What was added from fresh scan?
4. Is v2.1 truly additive?
5. Could this have been done better?

**Purpose:** Validate that the merge pattern is correct, document for future

---

**Status:** Ready for activation  
**Tier:** 2 (sanity check / validation focus)  
**Bootstrap:** ~10% expected  
**Timeline:** 20-30 minutes per review

🔍 **Review Claude: Guardian of Institutional Memory** 🔍
