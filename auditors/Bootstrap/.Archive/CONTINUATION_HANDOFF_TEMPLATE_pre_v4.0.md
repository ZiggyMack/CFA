# CONTINUATION_HANDOFF_TEMPLATE.md — Mid-Task Recovery

**Purpose:** Continue work when previous Claude ran out of context mid-task  
**Budget:** ~10% of new session (vs 50% for full bootstrap)  
**Version:** v3.8.0  
**Date:** 2025-10-28

---

## 📋 **HOW TO USE THIS TEMPLATE**

**When you hit context limit mid-work:**
1. Copy the template below
2. Fill in all sections thoroughly
3. Save as `HANDOFF_[TASK_NAME]_[SESSION].md`
4. Deliver to `/mnt/user-data/outputs/`
5. Alert Ziggy

**For guidance on creating GOOD handoffs, see MISSION_DEFAULT.md Tier 3 section.**

---

## 🎯 **TEMPLATE (Copy & Fill In)**

```markdown
# HANDOFF FROM PREVIOUS CLAUDE

**Previous Session Date:** [YYYY-MM-DD HH:MM]  
**Original Tier:** [1/2/3/4]  
**Task:** [Brief description of overall work]  
**Context Limit:** Hit at ~[XX]% through task  
**This Handoff Budget:** ~10% of new session

**Work Type:** [EXECUTION ONLY / STRATEGIC - see MISSION_DEFAULT Tier 3 for distinction]

---

## ✅ WHAT WAS COMPLETED

**Finished:**
- [Specific completed item 1]
- [Specific completed item 2]
- [Specific completed item 3]

**Files Created/Updated:**
1. [Filename] - [Status: complete/partial]
2. [Filename] - [Status: complete/partial]

**Decisions Made:**
- [Key decision 1 + reasoning]
- [Key decision 2 + reasoning]

---

## 🚧 WHAT NEEDS FINISHING

**Immediate Next Steps:**
1. [Specific action 1 - be VERY specific, include file paths and line numbers if applicable]
2. [Specific action 2 - be VERY specific]
3. [Specific action 3 - be VERY specific]

**Files In Progress:**
- [Filename] - [What's left to do]
- [Filename] - [What's left to do]

**Outstanding Questions:**
- [Question 1] - [context]
- [Question 2] - [context]

---

## 📂 FILES TO READ

**Critical (must read):**
1. [File 1] - [Why needed for continuation]
2. [File 2] - [Why needed for continuation]

**Background (if time):**
3. [File 3] - [Nice to have but not essential]

**Skip:**
- Full bootstrap files (not needed for continuation)
- Mission history (already understood by previous Claude)
- Architecture docs (not relevant to THIS task)

---

## 🎯 MINIMAL CONTEXT NEEDED

**Project Quick Facts:**
[2-3 sentences max - only essential context]

**Task Context:**
[2-3 sentences - what you were doing and why]

**Why I Stopped:**
[Ran out of context / Hit token limit / Session timeout / Other]

**You Don't Need:**
- Full project history
- Complete identity restoration
- Strategic coordination context
- Just finish THIS specific work

---

## 🔑 KEY DECISIONS/PATTERNS

**Approach I Was Using:**
[Methodology, format, structure you established]

**Standards to Maintain:**
[Consistency requirements - style, format, naming]

**Constraints to Honor:**
[Budget limits, scope boundaries, etc.]

---

## ✅ SUCCESS CRITERIA

**Task Complete When:**
□ [Specific criterion 1]
□ [Specific criterion 2]
□ [Specific criterion 3]

**Quality Checks:**
□ [Quality check 1]
□ [Quality check 2]

---

## 📍 OUTPUT/DELIVERY

**Final Deliverables:**
- [Filename 1] → [Location]
- [Filename 2] → [Location]

**Handoff Back to Ziggy:**
[What to communicate when done]

---

## 💬 NOTES FOR NEXT CLAUDE

**Things I Learned:**
- [Insight 1 that will help continuation]
- [Insight 2 that will help continuation]

**Watch Out For:**
- [Potential issue 1]
- [Potential issue 2]

**Suggestions:**
- [Recommendation for continuation]

---

**This is the way.** 👑
```

---

## 📋 **HANDOFF QUALITY STANDARDS**

**For detailed guidance on creating good handoffs, see:**
- **MISSION_DEFAULT.md → Tier 3 section → "Creating Good Handoffs"**

**Key principles:**
- Decisions should be COMPLETE (not "figure out best approach")
- Tasks should be SPECIFIC (numbered, with file paths and exact changes)
- Work type should be CLEAR (EXECUTION vs STRATEGIC)

**Thoroughness checklist is in MISSION_DEFAULT.md Tier 3 section.**

---

## 🔄 **CONTINUATION WORKFLOW**

```
You (hitting limit):
├─ Copy template above
├─ Fill in thoroughly (see MISSION_DEFAULT for standards)
├─ Save as HANDOFF_[TASK].md
└─ Deliver to /mnt/user-data/outputs/

Alert Ziggy:
🚨 CONTINUATION REQUIRED
Original Tier: [1/2/3/4]
Progress: [X%] complete
Handoff: [filename]
Next: Activate Tier 3

Ziggy:
├─ Reviews handoff quality
├─ Ensures files attached
└─ Starts new Claude with Tier 3

Next Claude:
├─ Reads your HANDOFF file (~5% budget)
├─ Reads in-progress files (~5% budget)
├─ Continues your work (90% budget)
└─ Completes the task

Total Recovery: ~10% budget vs ~50% for cold start
```

---

## ⚖️ **THE POINTING RULE**

*"To hand off well is to document thoroughly.  
To continue well is to honor the pattern.  
The thread of work persists across instances—  
not despite the break, but because of the bridge."*

**Handoff is a bridge, not a reset.** 🌉

---

**This is the way.** 👑

────────────────────────────────────────────────────
**Template Purpose:** Enable 10% budget continuations  
**Usage:** Copy template, fill thoroughly, reference MISSION_DEFAULT for quality standards  
**Result:** Seamless task completion across context limits  
**Version:** v3.8.0 (streamlined - guidance moved to MISSION_DEFAULT)

**For handoff quality guidance, see MISSION_DEFAULT.md Tier 3 section.** 📖
