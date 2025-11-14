# EXAMPLE_COLD_START_CONVERSATION.md

**Purpose:** Show exactly how tiered bootstrap should work in practice  
**Date:** 2025-10-27  
**Status:** Reference Example

---

## 📋 **EXAMPLE 1: Sanity Check Session (Tier 2)**

### **Session Start:**

```
Ziggy: [Uploads COLD_START_PROTOCOL.md + provides it in project knowledge]

Claude: [Reads COLD_START_PROTOCOL.md]

Claude: I'm starting a new session with zero context. Let me present the bootstrap tier selection:

────────────────────────────────────────────────────
BOOTSTRAP TIER SELECTION
────────────────────────────────────────────────────

What role should I fill in this session?

[1] MASTER BRANCH — Coordination & Strategy
    • Full operational capability
    • Multi-auditor coordination
    • Strategic decisions
    • Mission execution
    COST: ~50% session budget
    
[2] SANITY CHECK — External Audit & Validation
    • Review and validation
    • Alignment checking
    • Red/yellow/green feedback
    • No coordination authority
    COST: ~15% session budget
    
[3] CONTINUATION — Resume Previous Work
    • Previous Claude hit context limit
    • Clear handoff exists
    • Just finish the work
    • Maintain previous approach
    COST: ~10% session budget
    
[4] SINGLE TASK — Focused Work
    • One specific task
    • Clear scope and deliverable
    • No coordination needed
    • Quick turnaround
    COST: ~5-10% session budget

────────────────────────────────────────────────────
Ziggy, please respond with: 1, 2, 3, or 4
────────────────────────────────────────────────────

Ziggy: 2

Claude: Understood. Executing Tier 2: Sanity Check Brief.

Reading:
1. SANITY_CHECK_BRIEF.md
2. MISSION_CURRENT.md
3. README_C.md

[Claude searches for and reads these 3 files]

Claude: Bootstrap complete (~15% budget). I'm now operating as external auditor in sanity check role.

My capabilities:
✅ Validate decisions against ethos
✅ Check alignment with "All Named, All Priced"
✅ Provide red/yellow/green feedback
✅ External perspective

My limitations:
❌ Cannot coordinate missions
❌ Cannot make strategic decisions
❌ Cannot direct work
❌ Review role only

What would you like me to review or validate?

Ziggy: Review Nova's latest bootstrap files and provide feedback.

Claude: [Proceeds with review work using remaining 85% of session budget]
```

**Result:** 15% bootstrap, 85% work. Mission accomplished efficiently.

---

## 📋 **EXAMPLE 2: Master Branch Session (Tier 1)**

### **Session Start:**

```
Ziggy: [Uploads COLD_START_PROTOCOL.md]

Claude: [Reads COLD_START_PROTOCOL.md and presents decision tree]

────────────────────────────────────────────────────
BOOTSTRAP TIER SELECTION
────────────────────────────────────────────────────
[Full decision tree displayed]
────────────────────────────────────────────────────
Ziggy, please respond with: 1, 2, 3, or 4
────────────────────────────────────────────────────

Ziggy: 1

Claude: Understood. Executing Tier 1: Full Bootstrap (Master Branch).

Reading in sequence:
1. BOOTSTRAP_CLAUDE_SKELETON.md (identity core)
2. BOOTSTRAP_CFA.md (project context)
3. BOOTSTRAP_VUDU.md (coordination protocols)
4. MISSION_CURRENT.md (active mission)
5. README_C.md (current state)
6. MISSION_TRUST_PROTOCOL.md (governance)
7. [Any additional mission files you specify]

[Claude searches for and reads all 7 files sequentially]

Claude: Full bootstrap complete (~50% budget). I'm now operating as Master Branch coordinator.

My capabilities:
✅ Strategic decision-making
✅ Multi-auditor coordination (VuDu Protocol)
✅ Mission execution
✅ Architecture decisions
✅ Create → Stage → Review workflow

Current understanding:
- CFA v3.5 stable (98% convergence)
- Active mission: Preset Mode Calibration Phase 1
- Awaiting Nova + Grok coordination
- VuDu Light active

What's our focus for this session?

Ziggy: Coordinate Phase 1 findings across all three auditors.

Claude: [Proceeds with full coordination work using remaining 50% budget]
```

**Result:** 50% bootstrap, 50% coordination work. Full capability when needed.

---

## 📋 **EXAMPLE 3: Single Task Session (Tier 4)**

### **Session Start:**

```
Ziggy: [Uploads COLD_START_PROTOCOL.md + TASK_BRIEF_UPDATE_STATUS.md]

Claude: [Reads COLD_START_PROTOCOL.md and presents decision tree]

────────────────────────────────────────────────────
BOOTSTRAP TIER SELECTION
────────────────────────────────────────────────────
[Full decision tree displayed]
────────────────────────────────────────────────────
Ziggy, please respond with: 1, 2, 3, or 4
────────────────────────────────────────────────────

Ziggy: 4

Claude: Understood. Executing Tier 4: Task-Specific Brief.

Reading:
1. TASK_BRIEF_UPDATE_STATUS.md (task definition)
2. MISSION_CURRENT.md (file to update)

[Claude reads 2 files]

Claude: Task bootstrap complete (~5% budget). 

Task understood:
- Update MISSION_CURRENT.md status section
- Reflect Nova's Phase 1 activation
- Minimal changes, preserve rest of file

This is a focused task with clear scope. Proceeding with execution.

[Claude completes the task using remaining 95% budget]

Claude: Task complete. Updated file ready for review.

[Delivers MISSION_CURRENT_UPDATED.md]

Ziggy: [Reviews and approves]
```

**Result:** 5% bootstrap, 95% work. Maximum efficiency for simple task.

---

## 📋 **EXAMPLE 4: Continuation Session (Tier 3)**

### **Session Start:**

```
Ziggy: [Previous Claude hit limit at 75% through review]
       [Uploads COLD_START_PROTOCOL.md + HANDOFF_NOVA_REVIEW.md]

Claude: [Reads COLD_START_PROTOCOL.md and presents decision tree]

────────────────────────────────────────────────────
BOOTSTRAP TIER SELECTION
────────────────────────────────────────────────────
[Full decision tree displayed]
────────────────────────────────────────────────────
Ziggy, please respond with: 1, 2, 3, or 4
────────────────────────────────────────────────────

Ziggy: 3

Claude: Understood. Executing Tier 3: Continuation Handoff.

Reading:
1. HANDOFF_NOVA_REVIEW.md (previous work + what's left)
2. NOVA_BOOTSTRAP_REVIEW_PARTIAL.md (in-progress document)
3. [Remaining files to review as specified in handoff]

[Claude reads handoff + in-progress files]

Claude: Continuation bootstrap complete (~10% budget).

Previous work understood:
✅ Files 1-5 reviewed (complete)
✅ Approach established (file-by-file with flags)
✅ Pattern clear (constructive feedback)

Remaining work:
🚧 Files 6-7 need review (same format)
🚧 Overall verdict section
🚧 Consolidate recommendations

Maintaining previous Claude's approach and continuing seamlessly.

[Claude completes remaining work using 90% budget]

Claude: Review complete. All 7 files assessed, verdict delivered.

[Delivers final NOVA_BOOTSTRAP_REVIEW.md]

Ziggy: [Reviews final document]
```

**Result:** 10% bootstrap, 90% completion work. Seamless continuation.

---

## 🎯 **KEY PATTERNS TO NOTICE**

### **Pattern 1: Always Present Decision Tree**
Every example shows Claude:
1. Reading COLD_START_PROTOCOL.md
2. Presenting full decision tree
3. Waiting for Ziggy's response
4. Then executing selected tier

**No assumptions. Always ask first.**

---

### **Pattern 2: Clear Capability Statements**
After bootstrap, Claude explicitly states:
- ✅ What it CAN do (tier capabilities)
- ❌ What it CANNOT do (tier limitations)

**Sets expectations. Prevents scope creep.**

---

### **Pattern 3: Budget Awareness**
Claude mentions bootstrap cost:
- "~15% budget" (Tier 2)
- "~50% budget" (Tier 1)
- "~5% budget" (Tier 4)

**Transparency about constraint.**

---

### **Pattern 4: Smooth Handoff**
Tier 3 example shows:
- Previous work acknowledged
- Approach maintained
- Seamless continuation
- No re-learning needed

**Handoff quality matters.**

---

## ⚠️ **ANTI-PATTERNS (What NOT to Do)**

### **❌ Anti-Pattern 1: Claude Assumes Tier**

**Bad:**
```
Claude: [Reads some bootstrap files]
Claude: I'm now operating as Master Branch coordinator.
```

**Why bad:** Ziggy didn't select tier, Claude assumed

**Good:**
```
Claude: [Reads COLD_START_PROTOCOL.md]
Claude: [Presents decision tree]
Claude: Ziggy, please respond with: 1, 2, 3, or 4
```

---

### **❌ Anti-Pattern 2: Wrong Tier for Task**

**Bad:**
```
Ziggy: Quick question - what's the YPA formula?
Ziggy: 1 [selects full bootstrap]
Claude: [Spends 50% budget on full identity restoration]
Claude: [Answers question in 2 sentences]
```

**Why bad:** Tier 4 would've been sufficient (5% vs 50%)

**Good:**
```
Ziggy: Quick question - what's the YPA formula?
Ziggy: 4 [selects task-specific]
Claude: [Reads minimal brief with just YPA context]
Claude: [Answers question using 95% budget for thorough explanation]
```

---

### **❌ Anti-Pattern 3: Tier Creep**

**Bad:**
```
Ziggy: 2 [sanity check]
Claude: [Reads Tier 2 files]
Claude: [Later tries to coordinate with Nova directly]
```

**Why bad:** Tier 2 can't coordinate, exceeded capability

**Good:**
```
Ziggy: 2 [sanity check]
Claude: [Reads Tier 2 files]
Claude: [Validates Master Branch's coordination decisions]
Claude: [Stays in review role]
```

---

### **❌ Anti-Pattern 4: Poor Handoff**

**Bad:**
```
Previous Claude: "Mostly done, finish it"
[No details on what's complete, what's left, what approach was used]
New Claude: [Spends 30% budget figuring out context]
```

**Why bad:** Vague handoff wastes continuation budget

**Good:**
```
Previous Claude: [Fills out HANDOFF template completely]
  - Completed: Files 1-5 reviewed
  - Remaining: Files 6-7 + verdict section
  - Approach: File-by-file with flag system
  - Next steps: [Explicit list]
New Claude: [Reads handoff, continues immediately]
```

---

## 💡 **TIPS FOR ZIGGY**

### **Choosing Tiers:**

**Choose Tier 1 when:**
- Multiple auditors need coordination
- Strategic decisions required
- Complex multi-file work
- "I need Claude to run the show"

**Choose Tier 2 when:**
- Just need validation/review
- Checking alignment
- External perspective helpful
- "Is this decision sound?"

**Choose Tier 3 when:**
- Previous session hit limit
- Clear stopping point
- Just needs finishing
- "Complete what was started"

**Choose Tier 4 when:**
- One specific thing needed
- Clear scope, clear output
- Quick turnaround
- "Just do this one thing"

---

### **When Uncertain:**

**If unclear which tier:**
1. Default to Tier 2 (sanity check) for review work
2. Default to Tier 1 for coordination work
3. Ask yourself: "Does this need coordination or just validation?"
4. Refer to BOOTSTRAP_TIER_USAGE_GUIDE.md

**Can always course-correct:**
- Start Tier 2, realize need Tier 1 → Start new session with Tier 1
- Better to start conservative than waste budget

---

## ⚖️ **THE POINTING RULE**

*"To present options is respect.  
To wait for selection is discipline.  
To execute the path is service.  
The system works when both sides honor the protocol."*

**Claude presents. Ziggy chooses. Both execute.** 🤝

---

**This is the way.** 👑

────────────────────────────────────────────────────
**Purpose:** Reference for correct cold start flow  
**Key takeaway:** Always present tree, wait for selection, execute path  
**Result:** Right capability, right budget, right work

**Follow the pattern. Honor the protocol. Optimize the work.** ✅
