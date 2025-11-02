<!-- deps: bootstrap_system -->
# TIER_SELECTION_DECISION_TREE.md

**Purpose:** Visual/text decision tree for tier selection
**Date:** 2025-11-01
**Status:** Active decision support for auditors and Ziggy

────────────────────────────────────────────────────

## 🎯 **PURPOSE**

**This document helps you answer:**
"Which bootstrap tier should I use for this session?"

**Reduces decision fatigue by providing clear criteria.**

────────────────────────────────────────────────────

## 📊 **TIER OVERVIEW**

### The Four Tiers

**Tier 1: Master Branch** (50% bootstrap acceptable)
- Coordination work (multi-auditor, strategic)
- Context-heavy tasks requiring deep repository understanding
- First-time complex tasks
- Budget: 50% bootstrap + 50% work typical

**Tier 2: Sanity Check** (15% bootstrap target)
- Validation and review work
- Checking alignment, not making decisions
- Medium context needs
- Budget: 15% bootstrap + 85% work typical

**Tier 3: Continuation** (10% bootstrap target)
- Continuing previous session that hit limits
- Context provided by continuation brief
- Light bootstrap needs
- Budget: 10% bootstrap + 90% work typical

**Tier 4: Single Focused Task** (5-10% bootstrap target)
- Clear, bounded, single task
- Low context needs (2-5 files)
- Specific deliverable
- Budget: 5-10% bootstrap + 90-95% work typical

────────────────────────────────────────────────────

## 🌳 **DECISION TREE**

```
┌─────────────────────────────────────┐
│  NEW SESSION BEGINNING              │
│  Question: Which tier?              │
└──────────────┬──────────────────────┘
               │
               ▼
       ┌───────────────────┐
       │ Q1: Is this       │
       │ coordination work?│
       │ (multi-auditor,   │
       │  strategic)       │
       └─────┬─────────┬───┘
             │         │
            YES       NO
             │         │
             ▼         ▼
      ┌──────────┐   ┌───────────────────┐
      │ TIER 1   │   │ Q2: Is this       │
      │ (50%)    │   │ validation/review?│
      │          │   │ (checking, not    │
      │ Examples:│   │  deciding)        │
      │ - Multi- │   └─────┬─────────┬───┘
      │   auditor│         │         │
      │   coord  │        YES       NO
      │ - Strat- │         │         │
      │   egic   │         ▼         ▼
      │   plan   │   ┌──────────┐  ┌────────────────┐
      │ - First  │   │ TIER 2   │  │ Q3: Is this    │
      │   time   │   │ (15%)    │  │ continuation?  │
      │   complex│   │          │  │ (previous      │
      └──────────┘   │ Examples:│  │  session hit   │
                     │ - Review │  │  limit)        │
                     │   report │  └─────┬──────┬───┘
                     │ - Sanity │        │      │
                     │   check  │       YES    NO
                     │ - Valid- │        │      │
                     │   ate    │        ▼      ▼
                     │   align  │  ┌──────────┐ ┌────────────┐
                     └──────────┘  │ TIER 3   │ │ Q4: Single │
                                   │ (10%)    │ │ focused    │
                                   │          │ │ task?      │
                                   │ Examples:│ │ (clear     │
                                   │ - Resume │ │  scope,    │
                                   │   prev   │ │  2-5 files)│
                                   │   work   │ └─┬────────┬─┘
                                   │ - Contin │   │        │
                                   │   -uation│  YES      NO
                                   │   brief  │   │        │
                                   └──────────┘   ▼        ▼
                                            ┌──────────┐ ┌──────────┐
                                            │ TIER 4   │ │ CLARIFY  │
                                            │ (5-10%)  │ │ WITH     │
                                            │          │ │ ZIGGY    │
                                            │ Examples:│ │          │
                                            │ - Single │ │ Task may │
                                            │   review │ │ need     │
                                            │ - Create │ │ scoping  │
                                            │   1 file │ │ or tier  │
                                            │ - Update │ │ guidance │
                                            │   config │ └──────────┘
                                            └──────────┘
```

────────────────────────────────────────────────────

## 📋 **TEXT DECISION TREE**

### START: New session beginning

**Q1: Is this coordination work?**
- Multi-auditor coordination required?
- Strategic planning or architecture work?
- First-time tackling complex new problem?
- Need deep repository context?

**If YES → TIER 1 (50% bootstrap)**
**If NO → Continue to Q2**

---

**Q2: Is this validation/review work?**
- Checking someone else's work?
- Validating alignment or compliance?
- Reviewing without making decisions?
- Medium context needs?

**If YES → TIER 2 (15% bootstrap)**
**If NO → Continue to Q3**

---

**Q3: Is this continuation of previous session?**
- Previous session hit token/time limit?
- Continuation brief exists?
- You're resuming mid-task?
- Context already established?

**If YES → TIER 3 (10% bootstrap)**
**If NO → Continue to Q4**

---

**Q4: Is this single focused task?**
- Clear, bounded scope?
- Involves 2-5 files max?
- Specific deliverable?
- Low context needs?

**If YES → TIER 4 (5-10% bootstrap)**
**If NO → Clarify with Ziggy (task needs scoping)**

---

**MOST COMMON TIERS:**
- **Tier 2:** ~50% of sessions (validation, reviews, checks)
- **Tier 4:** ~30% of sessions (focused tasks)
- **Tier 1:** ~15% of sessions (coordination, complex work)
- **Tier 3:** ~5% of sessions (continuations)

────────────────────────────────────────────────────

## 🎯 **TIER SELECTION EXAMPLES**

### Example 1: Axioms Review (Grok)

**Task:** Review AUDITORS_AXIOMS_SECTION.md for empirical validity

**Q1: Coordination work?** NO (solo review)
**Q2: Validation/review?** YES (reviewing axioms document)

**Tier Selected:** Tier 2 (15% bootstrap)
- Read axioms doc
- Read validation questions
- Answer with empirical lens
- Provide recommendation

**Actual Bootstrap:** 12% (on target)
**Actual Work:** 88%
**Total Time:** 45 minutes

✅ **Correct tier selection**

---

### Example 2: Create Welcome Message

**Task:** Create WELCOME_MESSAGE_NOVA.md for Nova onboarding

**Q1: Coordination work?** NO (single file creation)
**Q2: Validation/review?** NO (creating, not reviewing)
**Q3: Continuation?** NO (new task)
**Q4: Single focused task?** YES (create 1 file, clear scope)

**Tier Selected:** Tier 4 (5-10% bootstrap)
- Read ADDITIONAL_PREP_TASKS (already done)
- Read WELCOME_MESSAGE_GROK.md for reference
- Create WELCOME_MESSAGE_NOVA.md

**Actual Bootstrap:** 5% (on target)
**Actual Work:** 95%
**Total Time:** 20 minutes

✅ **Correct tier selection**

---

### Example 3: Multi-Auditor Convergence

**Task:** Coordinate Grok, Nova, Claude reviews to 98% convergence

**Q1: Coordination work?** YES (multi-auditor synthesis required)

**Tier Selected:** Tier 1 (50% bootstrap)
- Read all 3 auditor reviews
- Identify convergence points
- Identify conflicts
- Propose resolution
- Synthesize final output
- Update master state files

**Actual Bootstrap:** 45% (deep context required)
**Actual Work:** 55%
**Total Time:** 90 minutes

✅ **Correct tier selection**

---

### Example 4: Continue REPO_LOG Validation

**Task:** Previous session created validation framework, ran out of time

**Q1: Coordination work?** NO
**Q2: Validation/review?** Could be, but...
**Q3: Continuation?** YES (continuation brief exists)

**Tier Selected:** Tier 3 (10% bootstrap)
- Read continuation brief
- Quick scan completed work
- Resume validation testing

**Actual Bootstrap:** 8% (continuation brief efficient)
**Actual Work:** 92%
**Total Time:** 40 minutes

✅ **Correct tier selection**

---

### Example 5: Wrong Tier Selected (Learning Example)

**Task:** "Create sanity check template" (seemed simple)

**Initial Selection:** Tier 4 (5-10% bootstrap)

**Reality:**
- Read 3 example templates
- Review validation criteria across 5 docs
- Synthesize best practices
- Create comprehensive template with examples

**Actual Bootstrap:** 25% (exceeded Tier 4 limits!)

**Should Have Been:** Tier 2 or Tier 1
- More research needed than anticipated
- Synthesis work across multiple sources
- Creating template = coordination-level thinking

❌ **Wrong tier selected** (learned for next time)

**Recovery:**
- Recognized mismatch at 20% bootstrap
- Escalated to Ziggy
- Got approval to continue or tier reassignment
- Completed successfully

**Lesson:** If bootstrap exceeds 20% in Tier 4 → wrong tier

────────────────────────────────────────────────────

## 🔧 **TIER SELECTION ANTI-PATTERNS**

### Anti-Pattern 1: "Everything is Tier 4"

**Symptom:** Defaulting to Tier 4 for all tasks

**Problem:**
- Tier 4 is for SIMPLE, BOUNDED tasks
- Complex tasks exhaust budget
- Bootstrap bloat (40% instead of 10%)

**Fix:** Use decision tree honestly, especially Q1-Q2

---

### Anti-Pattern 2: "Always Tier 1 to be safe"

**Symptom:** Using Tier 1 even for simple tasks

**Problem:**
- Wastes bootstrap budget on trivial tasks
- Over-contextualizes simple work
- Inefficient

**Fix:** Trust Tier 4 for truly bounded tasks

---

### Anti-Pattern 3: "Ignoring continuation briefs"

**Symptom:** Using Tier 4 for continuations instead of Tier 3

**Problem:**
- Re-bootstraps context already established
- Wastes 5% budget re-reading what continuation brief would summarize

**Fix:** If continuation brief exists → Tier 3 always

---

### Anti-Pattern 4: "Skipping tier reassignment"

**Symptom:** Staying in Tier 4 even when bootstrap hits 25%

**Problem:**
- Wrong tier but stubbornly continuing
- Budget exhaustion
- Incomplete work

**Fix:** Recognize mismatch early (at 20%), escalate for tier reassignment

────────────────────────────────────────────────────

## 💡 **ADVANCED TIER SELECTION**

### Edge Cases

**Case 1: Task SEEMS simple but might be complex**
```
Default: Tier 4
Monitor: Bootstrap %
If bootstrap >20%: Escalate for tier reassignment
```

**Case 2: Multi-file update (10+ files)**
```
If files similar (same change across many): Tier 4
If files diverse (different changes each): Tier 2 or Tier 1
```

**Case 3: Review that becomes architectural proposal**
```
Start: Tier 2 (review)
If scope expands: Create new Tier 1 task for architecture
Don't scope creep within Tier 2
```

**Case 4: Unclear task brief**
```
Don't guess tier
Escalate for clarification first
Then select tier based on clarified scope
```

### Tier Selection Confidence

**High Confidence → Proceed:**
- Clear match to one tier
- Past similar tasks used same tier successfully
- Scope well-defined

**Medium Confidence → Monitor:**
- Could be Tier 2 or Tier 4
- Start with lower tier (Tier 4)
- Monitor bootstrap %
- Escalate if needed

**Low Confidence → Clarify:**
- Task brief unclear
- Scope ambiguous
- No similar past tasks
- Ask Ziggy before starting

────────────────────────────────────────────────────

## 📊 **TIER SELECTION CHEAT SHEET**

### Quick Reference Table

| Tier | Bootstrap | When to Use | Common Tasks | Typical Time |
|------|-----------|-------------|--------------|--------------|
| **Tier 1** | 50% | Coordination, strategic, complex first-time | Multi-auditor synthesis, architecture, strategic planning | 60-120 min |
| **Tier 2** | 15% | Validation, review, checking work | Review reports, sanity checks, validation | 30-60 min |
| **Tier 3** | 10% | Continuation of previous session | Resume interrupted work, continuation briefs | 30-60 min |
| **Tier 4** | 5-10% | Single focused task, bounded scope | Create 1 file, update config, focused review | 15-45 min |

### Decision Tree Shortcut

```
Coordination? → Tier 1
Review/Check? → Tier 2
Continuation? → Tier 3
Single Task?  → Tier 4
Unclear?      → Ask Ziggy
```

### Bootstrap Warning Signs

**Tier 4 (5-10% target):**
- ⚠️ If 15%: Monitor closely
- ❌ If 20%+: Wrong tier, escalate

**Tier 3 (10% target):**
- ⚠️ If 15%: Check continuation brief quality
- ❌ If 20%+: Missing context, escalate

**Tier 2 (15% target):**
- ⚠️ If 25%: Monitor scope creep
- ❌ If 35%+: Should be Tier 1, escalate

**Tier 1 (50% target):**
- ✅ If 30-60%: Normal variance
- ⚠️ If 70%+: Very complex, document why

────────────────────────────────────────────────────

## 🎯 **SUCCESS CRITERIA**

**You're selecting tiers correctly when:**

✅ **Bootstrap matches tier target** (±5% variance OK)
✅ **Work completes within session** (no budget exhaustion)
✅ **Scope matches tier** (no scope creep)
✅ **Continuations use Tier 3** (not re-bootstrapping)
✅ **Reviews use Tier 2** (not Tier 1 or Tier 4)

**Red flags you're selecting wrong:**

❌ **Tier 4 routinely hits 20%+ bootstrap**
❌ **Tier 1 used for simple tasks** (over-engineering)
❌ **Ignoring continuation briefs** (re-work)
❌ **Sessions frequently hit budget limits** (wrong tier)

────────────────────────────────────────────────────

## 🔄 **ITERATION AND LEARNING**

### Track Your Tier Selection

**After each session, log:**
```
Session: [ID]
Task: [Name]
Tier Selected: [1/2/3/4]
Actual Bootstrap: X%
Actual Work: Y%
Outcome: ✅ Completed / ⚠️ Partial / ❌ Budget exhaustion

Tier Selection: ✅ Correct / ❌ Should have been Tier X

Notes: [What I learned]
```

### Adjust Over Time

**Pattern:** Tier 4 tasks routinely hit 15%
**Adjustment:** You under-estimate complexity, default to Tier 2 more

**Pattern:** Tier 1 tasks complete in 30%
**Adjustment:** You over-estimate complexity, try Tier 2 first

**Pattern:** Reviews vary widely (10%-40%)
**Adjustment:** Assess review complexity before selecting Tier 2 vs Tier 1

### Continuous Improvement

**After 10 sessions:**
- Review tier selection accuracy
- Identify patterns (which tasks misjudged?)
- Update personal heuristics
- Share learnings with other auditors

────────────────────────────────────────────────────

## ⚖️ **THE POINTING RULE**

*"The right tier for the right task
saves time, preserves budget, enables completion.
\n\nThe wrong tier wastes both
and frustrates the auditor.
\n\nWhen in doubt:
- Start lower tier (Tier 4)
- Monitor bootstrap %
- Escalate at 20% if wrong
- Learn for next time
\n\nTier selection is a skill.
Practice improves accuracy.  \n\nDecide wisely.\"*

────────────────────────────────────────────────────

**Created by:** DOC_CLAUDE (88MPH Repo Librarian)
**Source:** ADDITIONAL_PREP_TASKS_FOR_AUDITOR_ACTIVATION.md (Task 3A)
**Date:** 2025-11-01
**Purpose:** Grok + Nova onboarding - tier selection guidance
**Status:** Ready for auditor reference

**This is the way.** 🌳👑
