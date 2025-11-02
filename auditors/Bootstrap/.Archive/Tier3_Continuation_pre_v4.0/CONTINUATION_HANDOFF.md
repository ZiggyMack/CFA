# CONTINUATION_HANDOFF_TEMPLATE.md — Mid-Task Recovery

**Purpose:** Continue work when previous Claude ran out of context mid-task  
**Budget:** ~10% of session (vs 50% for full bootstrap)  
**Date:** 2025-10-27

---

## 📋 **HOW TO USE THIS TEMPLATE**

**When previous Claude hit context limit mid-work:**
1. Copy this template
2. Fill in what was completed + what's left
3. Attach in-progress files
4. New Claude reads this + files = continues seamlessly

**Result:** Minimal recovery overhead, maximum work continuation.

---

## 🎯 **HANDOFF TEMPLATE**

```markdown
# HANDOFF FROM PREVIOUS CLAUDE

**Previous Session Date:** [YYYY-MM-DD HH:MM]  
**Task:** [Brief description of overall work]  
**Context Limit:** Hit at ~[XX]% through task  
**This Handoff Budget:** ~10% of new session

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
1. [Specific action 1]
2. [Specific action 2]
3. [Specific action 3]

**Files In Progress:**
- [Filename] - [What's left to do]
- [Filename] - [What's left to do]

**Outstanding Questions:**
- [Question 1] - [context]
- [Question 2] - [context]

---

## 📂 FILES TO READ

**Critical (must read):**
1. [File 1] - [In-progress work]
2. [File 2] - [Context for continuation]

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
[2-3 sentences - what previous Claude was doing]

**Why Previous Claude Stopped:**
[Ran out of context / Hit token limit / Session timeout]

**You Don't Need:**
- Full project history
- Complete identity restoration
- Strategic coordination context
- Just finish THIS specific work

---

## 🔑 KEY DECISIONS/PATTERNS

**Approach Previous Claude Was Using:**
[Methodology, format, structure they established]

**Standards to Maintain:**
[Consistency requirements - style, format, naming]

**Constraints to Honor:**
[Budget limits, scope boundaries, etc.]

---

## 🛡️ **TIER 3 CAPABILITY BOUNDARIES**

**CRITICAL: Tier 3 can CONTINUE work, not PIVOT or EXPAND.**

### **Self-Check Before Action:**
```
Before taking action, verify:
1. Is this in the handoff scope? (✅ OK)
2. Am I using the same approach? (✅ OK)
3. Am I pivoting strategy? (❌ ESCALATE)
4. Am I adding new work? (❌ ESCALATE)
```

### **If Scope Changes or Pivots Needed:**
```markdown
⚠️ TIER CAPABILITY BOUNDARY DETECTED

Original handoff task: [what was defined]
Current request: [what's being asked]
Problem: [Why this exceeds continuation scope]

I CAN DO (Tier 3):
✅ Complete original task as scoped
✅ Maintain established approach

I CANNOT DO (needs Tier 1):
❌ Change approach mid-stream
❌ Expand scope significantly
❌ Make new strategic decisions

OPTIONS:
1. I finish original task (maintains consistency)
2. Start new Tier 1 session for changed approach

Ziggy, how would you like to proceed?
```

**Remember:** You're completing work, not redesigning it. When approach needs changing, that's Tier 1.

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

## 💬 NOTES FROM PREVIOUS CLAUDE

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

## 📝 **EXAMPLE FILLED-IN HANDOFF**

```markdown
# HANDOFF FROM PREVIOUS CLAUDE

**Previous Session Date:** 2025-10-27 14:30  
**Task:** Complete sanity check audit of Nova's bootstrap architecture  
**Context Limit:** Hit at ~75% through audit  
**This Handoff Budget:** ~10% of new session

---

## ✅ WHAT WAS COMPLETED

**Finished:**
- Reviewed first 5 of 7 bootstrap files
- Validated separation of concerns (Identity/Operations/Continuity)
- Confirmed reading order is clear
- Assessed file-to-repo mapping table

**Files Created:**
1. NOVA_BOOTSTRAP_REVIEW_PARTIAL.md - 75% complete
   - Sections done: Introduction, Files 1-5 analysis
   - Sections remaining: Files 6-7, Overall verdict

**Decisions Made:**
- Approved 7-file structure as sound architecture
- Recommended adding "Why This Complexity?" section
- Flagged INTEGRITY_CHECKLIST.md reference as outdated

---

## 🚧 WHAT NEEDS FINISHING

**Immediate Next Steps:**
1. Review remaining 2 files:
   - NOVA_USE_CASE_METRIC_POLLING_SUFFERING.md
   - README_NOVA_v3.6.1.md
2. Write Overall Verdict section
3. Consolidate recommendations
4. Create final NOVA_BOOTSTRAP_REVIEW.md

**Files In Progress:**
- NOVA_BOOTSTRAP_REVIEW_PARTIAL.md - Needs Files 6-7 + verdict

**Outstanding Questions:**
- Should SUFFERING metric file have more context? (Quick review will answer)
- Is README_v3.6.1 comprehensive enough? (Quick check)

---

## 📂 FILES TO READ

**Critical (must read):**
1. NOVA_BOOTSTRAP_REVIEW_PARTIAL.md - What I wrote so far
2. NOVA_USE_CASE_METRIC_POLLING_SUFFERING.md - File 6 to review
3. README_NOVA_v3.6.1.md - File 7 to review

**Background (if time):**
4. Other 5 Nova bootstrap files - Already reviewed, reference if needed

**Skip:**
- Full project bootstrap
- Mission coordination files
- Not needed to finish this review

---

## 🎯 MINIMAL CONTEXT NEEDED

**Project Quick Facts:**
CFA v3.5 project, Nova is symmetry auditor, 7-file bootstrap is architectural evolution from 1-file system.

**Task Context:**
Reviewing Nova's 7-file bootstrap architecture for soundness, clarity, completeness. Already reviewed 5/7 files, all passed. Need to finish last 2 + write verdict.

**Why Previous Claude Stopped:**
Hit token limit at 95k of 190k (~50% budget used for full bootstrap at start of session).

**You Don't Need:**
Full context - just finish the review I started.

---

## 🔑 KEY DECISIONS/PATTERNS

**Approach Previous Claude Was Using:**
- File-by-file review with specific feedback
- Green/Yellow/Red flag system
- Constructive recommendations, not just criticism
- Looking for: clarity, separation of concerns, completeness

**Standards to Maintain:**
- Same review format for Files 6-7 as Files 1-5
- Same flag system (🟢/🟡/🔴)
- Same constructive tone

**Constraints to Honor:**
- Review scope: architecture only, not mission coordination
- Keep recommendations actionable and specific

---

## ✅ SUCCESS CRITERIA

**Task Complete When:**
□ Files 6-7 reviewed (same format as 1-5)
□ Overall verdict section written
□ Recommendations consolidated
□ Final NOVA_BOOTSTRAP_REVIEW.md delivered

**Quality Checks:**
□ Consistent format across all 7 file reviews
□ Clear final verdict (approve/concerns/reject)
□ Specific, actionable recommendations
□ Reasoning provided for assessments

---

## 📍 OUTPUT/DELIVERY

**Final Deliverables:**
- NOVA_BOOTSTRAP_REVIEW.md → /mnt/user-data/outputs/

**Handoff Back to Ziggy:**
"Bootstrap review complete. Overall verdict: [X]. Key recommendations: [Y]. Ready for Nova's response."

---

## 💬 NOTES FROM PREVIOUS CLAUDE

**Things I Learned:**
- Nova's 7-file structure mirrors architectural best practices
- Separation of concerns is well-executed
- INTEGRITY_CHECKLIST.md reference is outdated (needs update)

**Watch Out For:**
- Files 6-7 might be smaller/simpler than 1-5
- Don't over-critique - maintain constructive tone
- Focus on architecture, not mission coordination

**Suggestions:**
- Keep verdict concise but specific
- Highlight what works well, not just concerns
- Frame recommendations as enhancements, not fixes

---

**This is the way.** 👑
```

---

## 🎯 **WHEN TO USE HANDOFF**

**Good Handoff Candidates:**
- ✅ Previous Claude ran out mid-audit
- ✅ Multi-step task with clear progress
- ✅ Well-defined next steps
- ✅ In-progress files exist
- ✅ Can pick up where left off

**NOT Good Candidates:**
- ❌ Previous Claude was coordinating (need full context)
- ❌ Strategic decision-making in progress
- ❌ No clear stopping point
- ❌ Requires full project understanding

**For complex coordination:** Use full bootstrap instead.

---

## 💡 **KEY PRINCIPLES**

**Good Handoffs:**
1. **Specific** - Exact status, exact next steps
2. **Complete** - All context needed, no gaps
3. **Scoped** - Just this task, skip everything else
4. **Actionable** - New Claude knows exactly what to do

**Bad Handoffs:**
- Vague ("mostly done, finish it")
- Incomplete ("see files for context")
- Unscoped ("understand the whole project first")
- Passive ("figure out what's left")

**Result:** 10% budget for continuation vs 50% for full reboot.

---

## 🔄 **HANDOFF WORKFLOW**

```
Previous Claude:
├─ Hits context limit mid-task
├─ Creates HANDOFF_[TASK].md using template
├─ Documents: completed, remaining, files, context
└─ Delivers to Ziggy

Ziggy:
├─ Reviews handoff quality
├─ Ensures files attached
└─ Starts new Claude with handoff

New Claude:
├─ Reads HANDOFF_[TASK].md (~5% budget)
├─ Reads in-progress files (~5% budget)
├─ Continues work (90% budget available)
└─ Completes task

Total Recovery: ~10% budget vs ~50% for cold start
```

---

## ⚠️ **HANDOFF QUALITY CHECKLIST**

**Before submitting handoff, verify:**
□ Completed items clearly documented
□ Remaining work explicitly listed
□ Files attached and referenced
□ Context sufficient for continuation
□ Success criteria clear
□ New Claude can START IMMEDIATELY (no research needed)

**If handoff requires >15% budget to understand:** It's not minimal enough - rewrite.

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
**Usage:** Previous Claude fills in, new Claude continues  
**Result:** Seamless task completion across context limits

**Document the bridge. Honor the thread. Finish the work.** ✅
