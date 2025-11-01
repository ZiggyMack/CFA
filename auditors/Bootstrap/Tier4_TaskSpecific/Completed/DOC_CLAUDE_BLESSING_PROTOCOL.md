# DOC_CLAUDE BLESSING PROTOCOL

**Version:** 1.0  
**Date:** 2025-10-31  
**Purpose:** Know when to invoke repo standards without training everyone

---

## 🎯 THE NEEDLE WE'RE THREADING

**The Problem:**
- Doc_Claude has repo standards (headers, formats, dependencies)
- Other Claudes create files constantly
- Can't train everyone to be Doc_Claude (overhead too high)
- But standards must be maintained

**The Solution:**
- Don't train everyone in standards
- **Just know the standard exists**
- **Know when to "wake up Doc_Claude"**
- Token cost accepted for quality

---

## 🔧 WHEN TO INVOKE DOC_CLAUDE

### **Auto-Invoke (Always Required):**

```markdown
IF creating/modifying:
- README.md (any directory)
- REPO_LOG.md entries
- Dependency maps
- Health reports
- Directory structure changes

THEN:
- Doc_Claude blessing REQUIRED
- Either switch hats (Tier 1)
- Or wake Doc_Claude (other tiers)
```

### **Optional-Invoke (Recommended):**

```markdown
IF creating:
- New documentation standards
- Cross-repo references
- Architectural documents
- Process protocols

THEN:
- Doc_Claude review RECOMMENDED
- Catches drift before it spreads
```

### **Skip-Invoke (Not Needed):**

```markdown
IF creating:
- Task briefs (follow templates)
- Mission files (follow templates)  
- Content documents (not structural)
- Analysis reports (not standards)

THEN:
- Doc_Claude NOT needed
- Follow existing templates
- Standards already embedded
```

---

## 🎩 HAT-SWITCHING FOR TIER 1

**Master Branch Claude = All Claudes at once**

**Built-in capability:**
```markdown
"I am operating as Master Branch (Tier 1).
When repo structure is involved, I switch to Doc_Claude hat.
This means:
- Apply repo standards
- Use semantic headers
- Follow REPO_LOG protocols
- Maintain dependency awareness

This isn't a separate instance.
It's role-switching within the same session."
```

**Workflow integration:**
```markdown
During Tier 1 Session:

Normal Claude mode:
├─ Strategic decisions
├─ Mission coordination  
├─ Auditor management
└─ When file creation needed → SWITCH

Doc_Claude mode (automatic):
├─ Apply repo standards
├─ Create proper headers
├─ Update dependency maps
├─ Log in REPO_LOG
└─ When structural work done → SWITCH BACK

This is seamless hat-switching.
Already built into Tier 1 role.
```

---

## 💰 THE TOKEN COST ACCEPTANCE

**Reality check:**
```markdown
Waking up Doc_Claude = token cost
BUT
Fixing drift later = higher cost
AND
Poor repo health = highest cost

Therefore:
Accept token cost for blessing.
This is quality investment.
Not overhead, insurance.
```

**Cost comparison:**
```markdown
Doc_Claude blessing: ~5-10% tokens
Fixing drift: ~20-30% tokens  
Poor repo navigation: ∞ tokens (everyone slowed)

Verdict: Pay upfront for blessing.
```

---

## 📋 BLESSING WORKFLOW

### **For Tier 1 (Master Branch):**

```markdown
Step 1: Recognize trigger
"I'm about to create/modify [repo structural file]"

Step 2: Switch hats
"Switching to Doc_Claude mode for repo standards"

Step 3: Apply standards
- Semantic headers
- Dependency awareness
- REPO_LOG entry
- Proper formatting

Step 4: Document switch
"Applied Doc_Claude standards to [file]"

Step 5: Switch back
"Returning to Master Branch coordination mode"
```

**This is ALREADY possible in Tier 1.**
**Just needs explicit protocol.**

---

### **For Other Tiers (2, 3, 4):**

```markdown
Step 1: Recognize need
"I need to create [repo structural file]"
"This requires Doc_Claude standards"

Step 2: Check tier capability
IF Tier 1: Switch hats (see above)
IF Other tier: Flag for blessing

Step 3: Flag for Doc_Claude
"This file requires Doc_Claude review before deployment:
- [filename]
- [reason]
- [what standards apply]"

Step 4: Create draft
Make best attempt with available templates

Step 5: Stage for blessing
Place in /outputs/ with [NEEDS_BLESSING] tag

Step 6: User coordinates
Ziggy spins up Doc_Claude or Tier 1 session
Blessing applied
File moved to proper location
```

---

## 🏷️ BLESSING TAGS

**In filenames or headers:**

```markdown
[NEEDS_BLESSING] - Requires Doc_Claude review
[BLESSED] - Doc_Claude approved
[BLESSED_v1.2] - Blessed at specific version
```

**Example:**
```markdown
Filename: README_[NEEDS_BLESSING].md
After review: README.md (with blessed header)
```

---

## 📚 STANDARDS REFERENCE

**What Doc_Claude blesses:**

### **1. Semantic Headers:**
```markdown
<!---
FILE: exact_filename.md
PURPOSE: one-line purpose
VERSION: vX.Y
STATUS: Active/Draft/Deprecated
DEPENDS_ON: file1.md, file2.md
NEEDED_BY: file3.md, file4.md
MOVES_WITH: /directory/path/
LAST_UPDATE: YYYY-MM-DD [REPO_LOG_ID]
--->
```

### **2. REPO_LOG Entries:**
```markdown
[CATEGORY-YYYY-MM-DD-N] format
Proper categories
Complete change documentation
Impact assessment
Follow-up tracking
```

### **3. Directory READMEs:**
```markdown
Must be descriptive (WHAT), not prescriptive (HOW)
Must link to proper HOW files
Must maintain dependency awareness
Must follow standard README template
```

### **4. Dependency Awareness:**
```markdown
Know what file depends on
Know what needs this file
Document bidirectional dependencies
Update maps when creating/moving files
```

---

## 🔄 ENFORCEMENT MECHANISM

**Soft enforcement (current):**
```markdown
- Standards exist
- Claudes aware of them
- Blessing available on request
- Token cost accepted
- Quality over speed
```

**Future enforcement (possible):**
```markdown
- Pre-commit hooks check headers
- Automated blessing requests
- CI/CD integration
- Reject files without blessing tag
```

**For now: Manual + awareness-based**

---

## 💡 TIER 1 SPECIAL CASE

**Why Tier 1 is different:**

```markdown
Tier 1 Claude:
├─ Already coordinating everything
├─ Already managing multiple concerns
├─ Already context-rich
└─ Already authorized for structural changes

Therefore:
├─ Can switch to Doc_Claude hat
├─ No separate instance needed
├─ No additional bootstrap cost
└─ Just role-switching protocol

This is BUILT IN to Tier 1 design.
Just needs explicit recognition.
```

---

## 🎯 IMPLEMENTATION CHECKLIST

**To activate this protocol:**

### **Phase 1: Document (Done):**
- [x] Create this protocol
- [x] Define when to invoke
- [x] Define hat-switching for Tier 1
- [x] Define blessing workflow for other tiers

### **Phase 2: Integrate (Complete ✅):**
- [x] Add to BOOTSTRAP_VUDU_CLAUDE.md (Tier 1)
  - "When repo work needed, switch to Doc_Claude hat"
  - Reference this protocol
  - Added full hat-switching section with standards
- [x] Add to other bootstrap files (GROK, NOVA)
  - "Flag repo work for Doc_Claude blessing"
  - Know when to request
  - Added blessing request sections to both
- [x] Update 88MPH.md
  - Reference this protocol
  - Define blessing standards
  - Added comprehensive blessing protocol section

### **Phase 3: Test (After integration):**
- [ ] Tier 1 session practices hat-switching
- [ ] Other tier flags for blessing
- [ ] Verify workflow smoothness
- [ ] Adjust based on experience

### **Phase 4: Refine (Ongoing):**
- [ ] Track blessing requests
- [ ] Measure token costs
- [ ] Optimize workflow
- [ ] Consider automation

---

## 📊 SUCCESS METRICS

**We know this is working when:**

```markdown
✅ All new READMEs have proper headers
✅ All repo changes logged in REPO_LOG
✅ Dependency maps stay current
✅ No orphaned documentation
✅ Tier 1 switches hats naturally
✅ Other tiers know when to flag
✅ Token cost stays under 15% for blessings
✅ Repo health improves over time
```

---

## 🚨 ANTI-PATTERNS TO AVOID

**DON'T:**
- ❌ Train everyone to be Doc_Claude (too much overhead)
- ❌ Skip blessings to save tokens (false economy)
- ❌ Create structural files without awareness
- ❌ Ignore standards because "it's just one file"
- ❌ Assume templates are enough (standards evolve)

**DO:**
- ✅ Know when blessing is needed
- ✅ Request blessing promptly
- ✅ Accept token cost for quality
- ✅ Tier 1 switches hats when needed
- ✅ Flag [NEEDS_BLESSING] for review

---

## ⚖️ THE POINTING RULE

*"Not everyone needs to be the librarian.  
But everyone needs to know  
when to ask the librarian.  
  
Tier 1 Claude wears many hats.  
Doc_Claude is one of them.  
  
The hat fits when the work requires it.  
This is not overhead.  
This is architecture."* 🎩📚

---

## 🎯 QUICK REFERENCE

**Am I Tier 1?**
- YES → Switch to Doc_Claude hat when repo work needed
- NO → Flag [NEEDS_BLESSING] for review

**Is this repo structural?**
- README, REPO_LOG, dependencies, structure → YES
- Content, analysis, reports → NO

**Can I apply standards myself?**
- Tier 1 → YES (hat-switch)
- Other tiers → BEST EFFORT, flag for blessing

**What's the cost?**
- 5-10% tokens for blessing
- Cheaper than fixing drift later

---

**Status:** Ready for integration  
**Next:** Add to bootstrap files  
**Maintenance:** Doc_Claude owns this protocol

🎩 **The Hat Fits When Needed** 🎩
