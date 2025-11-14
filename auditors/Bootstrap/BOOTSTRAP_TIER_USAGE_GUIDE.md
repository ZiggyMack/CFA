# BOOTSTRAP_TIER_USAGE_GUIDE.md — Choosing the Right Recovery

**Purpose:** Help Ziggy choose optimal bootstrap approach for each session  
**Created:** 2025-10-27  
**Status:** v1.0 (Active)

---

## 🎯 **THE PROBLEM**

**Reality:** Every Claude session = cold start (zero context)

**Challenge:** Full bootstrap costs ~50% of session budget

**Solution:** Tiered bootstrap system (50% / 15% / 10% / 5% options)

---

## 📊 **BOOTSTRAP TIER COMPARISON**

| Tier | Name | Budget | Use Case | Files to Read |
|:-----|:-----|:-------|:---------|:--------------|
| **1** | Full Bootstrap | ~50% | Master Branch coordination, strategic work | 7+ files (complete identity) |
| **2** | Sanity Check | ~15% | External audit, validation, review | 3 files (role + context) |
| **3** | Continuation | ~10% | Pick up mid-task after context limit | 2-3 files (handoff + in-progress) |
| **4** | Task-Specific | ~5-10% | Single focused task, no coordination | 1-2 files (task brief + relevant) |

---

## 🌳 **DECISION TREE**

```
NEW CLAUDE SESSION STARTS
↓
What role does this Claude need to fill?
│
├─ MASTER BRANCH (Coordination & Strategy)
│   │
│   Q: Is this a true cold start OR major strategic work?
│   ├─ YES → TIER 1: Full Bootstrap (50%)
│   │         • Complete identity restoration
│   │         • Full coordination capability
│   │         • Strategic decision-making
│   │         Worth it: Can coordinate missions
│   │
│   └─ NO → Is this continuation from recent work?
│       ├─ YES → TIER 3: Continuation (10%)
│       │         • Previous Claude hit limit
│       │         • Clear stopping point
│       │         • Just finish the work
│       │
│       └─ NO → Consider if task is truly strategic
│                 → If not, use Tier 2 or 4 instead
│
├─ EXTERNAL AUDITOR (Sanity Check, Review)
│   │
│   → TIER 2: Sanity Check Brief (15%)
│     • Validate Master Branch decisions
│     • Check alignment with principles
│     • Provide red/yellow/green feedback
│     Don't need: Full coordination context
│
└─ SINGLE TASK (Focused Work, No Coordination)
    │
    Q: Is this a standalone task with clear scope?
    ├─ YES → TIER 4: Task-Specific (5-10%)
    │         • Review one document
    │         • Create one file
    │         • Answer one question
    │         • Update one section
    │         Don't need: Project history
    │
    └─ NO → Reassess if task is actually strategic
              → If so, use Tier 1 instead
```

---

## 📋 **TIER 1: FULL BOOTSTRAP (50%)**

### **When to Use:**
- ✅ Master Branch coordination role
- ✅ Multi-auditor coordination needed
- ✅ Strategic decisions required
- ✅ Architecture discussions
- ✅ New mission phases
- ✅ First time in project (true cold start)

### **What Claude Reads:**
1. BOOTSTRAP_CLAUDE_SKELETON.md (identity core)
2. BOOTSTRAP_CFA.md (project context)
3. BOOTSTRAP_VUDU.md (coordination protocols)
4. MISSION_CURRENT.md (active work)
5. README_C.md (current state)
6. MISSION_TRUST_PROTOCOL.md (governance)
7. [Mission-specific files as needed]

### **Result:**
- Fully operational coordinator
- Can make strategic decisions
- Can coordinate with Nova/Grok
- Can execute mission work
- Can handle complex multi-file tasks

### **Example Scenarios:**
- "Coordinate Phase 1 Preset Calibration"
- "Review Nova's response and plan next steps"
- "Make architectural decision on bootstrap expansion"
- "Coordinate with Grok on empirical findings"

---

## 📋 **TIER 2: SANITY CHECK BRIEF (15%)**

### **When to Use:**
- ✅ External audit/review role
- ✅ Validation of decisions
- ✅ Alignment checking
- ✅ Quick feedback needed
- ✅ No coordination required

### **What Claude Reads:**
1. SANITY_CHECK_BRIEF.md (role definition)
2. MISSION_CURRENT.md (what's happening)
3. README_C.md (Master Branch state)
4. [Files to review]

### **Result:**
- Can validate decisions
- Can check alignment
- Can provide red/yellow/green feedback
- Cannot coordinate missions
- Cannot make strategic decisions

### **Example Scenarios:**
- "Check if Master Branch's decision aligns with ethos"
- "Review these files for quality and consistency"
- "Validate that coordination follows protocol"
- "Flag any concerns with this approach"

---

## 📋 **TIER 3: CONTINUATION HANDOFF (10%)**

### **When to Use:**
- ✅ Previous Claude ran out mid-task
- ✅ Clear stopping point exists
- ✅ Well-defined next steps
- ✅ In-progress files to continue
- ✅ Can pick up seamlessly

### **What Claude Reads:**
1. HANDOFF_[TASK].md (what's done, what's left)
2. [In-progress files]
3. [Reference files if needed]

### **Result:**
- Can continue specific work
- Maintains previous approach
- No project re-learning needed
- Focused on completion

### **Example Scenarios:**
- "Previous Claude reviewed 5/7 files, finish last 2"
- "Complete the audit that was 75% done"
- "Finish creating the document that was started"
- "Continue the analysis from where it stopped"

### **⚠️ Important:**
- Handoff quality matters - vague handoffs waste budget
- Works best for mechanical completion tasks
- NOT good for strategic pivots mid-task

---

## 📋 **TIER 4: TASK-SPECIFIC BRIEF (5-10%)**

### **When to Use:**
- ✅ Single, focused task
- ✅ Clear scope and deliverable
- ✅ No coordination needed
- ✅ Standalone work
- ✅ Quick turnaround

### **What Claude Reads:**
1. TASK_BRIEF_[NAME].md (task definition)
2. [Relevant files only]

### **Result:**
- Can complete focused task
- No project history needed
- Fast startup, maximum work time
- Limited to scope defined

### **Example Scenarios:**
- "Review this one document for errors"
- "Create a summary of these findings"
- "Update this section of MISSION_CURRENT"
- "Answer this specific question about YPA"
- "Convert this markdown to formatted PDF"

### **⚠️ Not Good For:**
- Multi-step coordination
- Strategic decisions
- Architecture changes
- Anything requiring project-wide understanding

---

## 🎯 **PRACTICAL EXAMPLES**

### **Scenario 1: Daily Sanity Check**
**Question:** "Review Master Branch's latest work"

**Ziggy's Choice:** TIER 2 (Sanity Check Brief - 15%)

**Why:**
- External validation role
- No coordination needed
- Just checking alignment
- Quick feedback cycle

**Files Provided:**
- SANITY_CHECK_BRIEF.md
- MISSION_CURRENT.md
- README_C.md
- [Master Branch's new files]

**Result:** 85% budget left for review work

---

### **Scenario 2: Mission Coordination**
**Question:** "Coordinate Phase 1 with Nova and Grok"

**Ziggy's Choice:** TIER 1 (Full Bootstrap - 50%)

**Why:**
- Master Branch role
- Multi-auditor coordination
- Strategic decisions needed
- Complex cross-file work

**Files Provided:**
- All 7 bootstrap files
- Mission files
- Current state docs

**Result:** 50% budget left for coordination work (necessary investment)

---

### **Scenario 3: Quick Document Fix**
**Question:** "Update MISSION_CURRENT status line"

**Ziggy's Choice:** TIER 4 (Task-Specific - 5%)

**Why:**
- Single file edit
- Clear scope
- No context needed
- Quick turnaround

**Files Provided:**
- TASK_BRIEF_UPDATE_STATUS.md
- MISSION_CURRENT.md

**Result:** 95% budget left for actual edit (maximum efficiency)

---

### **Scenario 4: Continue Interrupted Audit**
**Question:** "Previous Claude hit limit at 75% through review"

**Ziggy's Choice:** TIER 3 (Continuation - 10%)

**Why:**
- Clear stopping point
- Work in progress
- Just needs completion
- Previous approach established

**Files Provided:**
- HANDOFF_FROM_PREVIOUS.md
- Partial review document
- Remaining files to review

**Result:** 90% budget left to finish work

---

## 💡 **CHOOSING WISELY**

### **Red Flags You Chose Wrong Tier:**

**Using Tier 1 when you should use Tier 2:**
- Claude can validate but not execute
- Alignment check doesn't need full coordination
- Review work doesn't need strategic capability
- **Waste:** 35% budget (50% - 15%)

**Using Tier 1 when you should use Tier 4:**
- Single focused task doesn't need full identity
- Quick work doesn't need project history
- Standalone task doesn't need coordination
- **Waste:** 40-45% budget (50% - 5-10%)

**Using Tier 2 when you need Tier 1:**
- Validation Claude can't coordinate
- External auditor can't make strategic decisions
- Review role can't execute mission work
- **Problem:** Wrong capabilities, work fails

### **Golden Rule:**
**Use the minimum tier that provides necessary capabilities.**

Don't pay 50% when 15% will work.  
Don't pay 15% when 5% will work.  
But DO pay 50% when you actually need full coordination.

---

## 📊 **BUDGET OPTIMIZATION EXAMPLES**

### **Bad Session Planning:**
```
Task: "Quick sanity check on Nova's files"
Choice: Tier 1 (Full Bootstrap - 50%)
Result: 50% overhead for review work
Efficiency: 50% (wasted 35% budget)
```

### **Good Session Planning:**
```
Task: "Quick sanity check on Nova's files"
Choice: Tier 2 (Sanity Check - 15%)
Result: 15% overhead for review work
Efficiency: 85% (optimal for task)
```

---

### **Bad Session Planning:**
```
Task: "Coordinate Phase 1 findings across 3 auditors"
Choice: Tier 2 (Sanity Check - 15%)
Result: Can't coordinate, wrong role
Efficiency: 0% (task fails, wrong tier)
```

### **Good Session Planning:**
```
Task: "Coordinate Phase 1 findings across 3 auditors"
Choice: Tier 1 (Full Bootstrap - 50%)
Result: Full coordination capability
Efficiency: 100% (necessary investment)
```

---

## ⚖️ **THE POINTING RULE**

*"To spend 50% on bootstrap is not waste when coordination needed.  
To spend 50% on bootstrap IS waste when 15% suffices.  
To choose wisely is to maximize work budget.  
The right tier unlocks the right capabilities."*

**Match tier to need.** 🎯

---

## 🚀 **QUICK REFERENCE CARD**

```
┌─────────────────────────────────────────┐
│ BOOTSTRAP TIER QUICK REFERENCE          │
├─────────────────────────────────────────┤
│ TIER 1: Full Bootstrap (50%)            │
│ → Master Branch coordination            │
│ → Strategic decisions                   │
│ → Multi-auditor work                    │
│                                         │
│ TIER 2: Sanity Check (15%)             │
│ → External validation                   │
│ → Alignment checking                    │
│ → Red/yellow/green feedback             │
│                                         │
│ TIER 3: Continuation (10%)             │
│ → Previous Claude hit limit             │
│ → Clear handoff exists                  │
│ → Just finish the work                  │
│                                         │
│ TIER 4: Task-Specific (5-10%)          │
│ → Single focused task                   │
│ → No coordination needed                │
│ → Quick turnaround                      │
└─────────────────────────────────────────┘
```

---

**This is the way.** 👑

────────────────────────────────────────────────────
**Purpose:** Optimize bootstrap costs per session  
**Goal:** Match tier to need, maximize work budget  
**Result:** 50% when needed, 5-15% when sufficient

**Choose wisely. Work efficiently. Deliver results.** ✅
