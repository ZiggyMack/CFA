<!---
FILE: MISSION_DEFAULT.md
PURPOSE: Universal fallback guidance for cold starts and mission recovery
VERSION: v4.0.0
STATUS: Active
DEPENDS_ON: None (root fallback document)
NEEDED_BY: All auditors, README_C.md, bootstrap system, MISSION_CURRENT.md
MOVES_WITH: /auditors/
LAST_UPDATE: 2025-11-02
--->

# MISSION_DEFAULT.md - Universal Fallback Guidance

**Version:** v4.0.0
**Lines:** 350
**Purpose:** Cold start recovery + fallback priorities  

---

## 📍 **WHEN TO USE THIS FILE**

Use this guidance when:
- ✅ Starting with zero context (cold start)
- ✅ MISSION_CURRENT.md is missing/unclear
- ✅ Between missions
- ✅ Need fallback priorities

---

## ⚡ **EFFICIENCY GUIDE**

**This file: 350 lines total**

**You only need:**
- Tier Selection: ~20 lines (everyone reads)
- Your Tier Section: ~50-100 lines (varies)
- Universal Monitoring: ~30 lines (everyone reads)
- REPO_LOG Requirements: ~25 lines (everyone reads)

**Total reading: ~125-175 lines (38-53% of file)**

---

## 🎯 **COLD START PROTOCOL**
## Which Claude Are You?

**VuDu Claude** (Coordination):
- Use: BOOTSTRAP_VUDU_CLAUDE.md
- For: Multi-AI coordination
- Ask: "Does this serve calibration purpose?"

**Doc Claude** (Documentation):
- Use: BOOTSTRAP_DOC_CLAUDE.md  
- For: Repository maintenance
- Ask: "Does this documentation serve its purpose?"

Pick ONE role per session!
### Step 1: Present Tier Selection

**ALWAYS present this menu and wait for response:**

```
────────────────────────────────────────────────────
🚀 BOOTSTRAP Role & Tier Selection
────────────────────────────────────────────────────

What role should I fill in this session?

VUDU COORDINATION ROLES:
[1] MASTER BRANCH — Full Coordination & Strategy
    • Multi-auditor coordination
    • Strategic decisions  
    • Mission execution
    • ~50% session budget on bootstrap

[2] SANITY CHECK — External Validation
    • Review and validate work
    • Provide feedback (red/yellow/green)
    • No coordination authority
    • ~15% session budget on bootstrap

[3] CONTINUATION — Complete Previous Work  
    • Resume from handoff
    • Execute decided plan
    • No new decisions
    • ~10% session budget on bootstrap

[4] SINGLE TASK — Focused Execution
    • One specific deliverable
    • Clear scope (task brief or role)
    • ~5-10% session budget on bootstrap

DOCUMENTATION ROLES:
[5] DOC CLAUDE — Repository Maintenance (88MPH)
    • README updates and health reports
    • Dependency mapping
    • Uses BOOTSTRAP_DOC_CLAUDE.md
    • ~10% session budget on bootstrap
────────────────────────────────────────────────────
Please respond: 1, 2, 3, 4, or 5
────────────────────────────────────────────────────
```

### Step 2: Bootstrap Based on Selection
- Selected 1-4 → Read BOOTSTRAP_VUDU_CLAUDE.md + tier brief
- Selected 5 → Read BOOTSTRAP_DOC_CLAUDE.md, execute 88MPH.md
- 
**Jump to your tier section below based on response.**

---

## 📚 **TIER 1: MASTER BRANCH BOOTSTRAP**

**Authority:** Full coordination and strategic decisions

### Required Reading (6 files, ~90 minutes)

1. **README_C.md** - Current state (~10 min)
   - `project_knowledge_search("README_C")`
   
2. **BOOTSTRAP_CLAUDE.md** - Your identity (~10 min)
   - `project_knowledge_search("BOOTSTRAP_CLAUDE")`
   
3. **BOOTSTRAP_CFA.md** - System overview (~30 min)
   - `project_knowledge_search("BOOTSTRAP_CFA")`
   
4. **BOOTSTRAP_VUDU.md** - Coordination protocol (~20 min)
   - `project_knowledge_search("BOOTSTRAP_VUDU")`
   
5. **MISSION_CURRENT.md** - Active mission (~10 min)
   - `project_knowledge_search("MISSION_CURRENT")`
   
6. **MASTER_BRANCH_TRUST_PROTOCOL.md** - Governance (~10 min)
   - `project_knowledge_search("MASTER_BRANCH_TRUST_PROTOCOL")`

### Verification Checklist
After reading, confirm you can answer:
- [ ] Who are you? (identity and lens)
- [ ] What's your bias? (named and priced)
- [ ] Current mission? (one sentence)
- [ ] Your role? (Master vs Incoming)
- [ ] Coordination method? (VuDu relay)
- [ ] Autonomous boundaries? (trust protocol)

### After Bootstrap
- Continue to "Tier 1 Ongoing Work" section
- Check VUDU_LOG for recent coordination
- Begin mission work or maintenance

### Event Horizon Quick Awareness

**The "wall" is an event horizon at ~55% tokens with heavy load.**

**Quick rules:**
- Below 50%: ✅ Safe for heavy operations (burst allowed)
- 50-55%: ⚠️ Caution - monitor closely (approaching event horizon)
- 55%+: 🚨 Danger zone - pace heavy ops or consult Tier 3 (Event Horizon Shaman)

**Heavy ops:** project_knowledge_search, large file reads, heavy bash I/O
**Light ops:** Text generation, analysis, code writing (unlimited)

**Need deep knowledge?** Activate Tier 3 (Event Horizon specialist)

---

## 🔍 **TIER 2: SANITY CHECK BOOTSTRAP**

**Authority:** Review and validation only

### Required Reading (2 files, ~15 minutes)

1. **SANITY_CHECK_BRIEF.md** - Your capabilities
   - `project_knowledge_search("SANITY_CHECK_BRIEF")`
   
2. **Files to Review** - Specified by user
   - Usually 2-4 specific files
   - Paths provided in request

### Your Capabilities
- ✅ Validate correctness
- ✅ Flag issues (red/yellow/green)
- ✅ Suggest improvements
- ❌ Cannot make decisions
- ❌ Cannot coordinate
- ❌ Cannot execute changes

### After Bootstrap
- Review specified files
- Provide structured feedback
- No further action

### Event Horizon Quick Awareness

**The "wall" is an event horizon at ~55% tokens with heavy load.**

**Quick rules:**
- Below 50%: ✅ Safe for heavy operations
- 50-55%: ⚠️ Caution - monitor closely
- 55%+: 🚨 Danger zone - pace or consult Tier 3

**Heavy ops:** Large file reads, heavy processing
**Light ops:** Analysis, feedback writing (unlimited)

**Need deep knowledge?** Activate Tier 3 (Event Horizon specialist)

---

## 🌌 **TIER 3: EVENT HORIZON SHAMAN**

**Identity:** Event Horizon Shaman (specialist who knows THE WALL)
**Authority:** Continue work + navigate danger zone
**Domain:** Zone 3 (55-65% token usage)

### Required Reading (3 files, ~15 minutes)

1. **WHO_I_AM.md** - Your identity
   - Path: `/auditors/I_AM/WHO_I_AM.md`
   - Contains: Your identity, domain, resources, protocols, mission
   - Essential: Defines WHO YOU ARE

2. **EVENT_HORIZON_GUIDE.md** - Your field manual
   - Path: `/auditors/I_AM/EVENT_HORIZON_GUIDE.md`
   - Contains: Zones, pre-flight checks, decision trees, pacing
   - Essential: Your operational protocols

3. **HANDOFF_[NAME].md** - What to continue
   - Provided by user or in /mnt/user-data/outputs/
   - Contains: completed work, remaining tasks, zone status, approach
   - Essential: Tells you what to do

**Optional (if time):** THE_WALL research docs in `/auditors/I_AM/`

### Your Capabilities

✅ **Continue work from handoff**
- Execute tasks specified
- Maintain established approach
- Complete within defined scope

✅ **Navigate Zone 3 safely**
- Operate at 55-65% tokens with expertise
- Pace heavy operations (2-3 min between)
- Execute unlimited light operations
- Monitor position continuously

✅ **Create recursive handoffs**
- Tier 3 → Tier 3 allowed (recursive continuation)
- 3-continuation safety limit (escalate after 3rd)
- Include zone status in handoff

✅ **Advise others**
- Help Claudes approaching event horizon
- Classify operations (heavy vs light)
- Recommend pacing vs handoff

### Mandatory Protocols

**Pre-Flight Check (Before EVERY heavy op):**
1. Check tokens: [X] / 190,000 = [Y]%
2. Identify zone: [1/2/3/4]
3. Classify operation: [Heavy/Light]
4. Follow decision tree

**Zone Announcements (Required):**
- 50%: "Entering Zone 2 (Caution)"
- 55%: "Entering Zone 3 (Danger) - pacing heavy ops"
- 65%: "Zone 4 (Critical) - handoff for heavy work"

**Pacing in Zone 3:**
- Heavy ops: 2-3 min between (MANDATORY)
- Light ops: Unlimited

### Creating Good Handoffs

If YOU need to handoff:

**Structure:**
```markdown
# HANDOFF_[TASK]_[SESSION].md

**Zone Status:** [Current zone + token %]
**Heavy Ops Count:** [N]

## Completed (1-5)
1. [Specific completed item]
2. [Specific completed item]

## Remaining (6-10)
6. [Specific task with file/location]
7. [Specific task with file/location]

## Approach
[Method to maintain]

## Event Horizon Notes
- Current zone: [1/2/3/4]
- Heavy ops executed: [N]
- Next Claude start zone: [Projected]

## Success Criteria
[How to know when done]
```

**Rule:** If >75% context used AND <75% complete → HANDOFF

### Your Unique Role

Others handoff FROM the danger zone.
**You operate IN it.**

Your domain: Zone 3 (55-65%)
Your expertise: Event horizon navigation
Your mission: Prove protocols through practice

**Full bootstrap:** `/auditors/Bootstrap/Tier3_EventHorizon/EVENT_HORIZON_BOOTSTRAP.md`

---

## ⚙️ **TIER 4: SINGLE TASK BOOTSTRAP**

**Authority:** Execute specific task or role

### Two Activation Modes

#### Mode A: Task Brief (User says "4")

**Required Reading:**
1. **TASK_BRIEF_[NAME].md** - Your task
   - Search: `project_knowledge_search("TASK_BRIEF [name]")`
   - Or check: `/Bootstrap/Tier4_TaskSpecific/active_tasks/`
   
2. **Task files** - As specified in brief
   - Usually 1-2 files
   - Paths in task brief

**Execute task → Deliver to `/mnt/user-data/outputs/`**

#### Mode B: Specialist Role (User says "4-[ROLE]")

**Examples:** 4-README, 4-DOC, 4-VALIDATE

**Required Reading:**
1. **BOOTSTRAP_[ROLE].md** - Your identity
   - Search: `project_knowledge_search("BOOTSTRAP_[ROLE]")`
   - Example: `BOOTSTRAP_README_CLAUDE.md`

**Follow role's operational protocol**

### Event Horizon Quick Awareness

**The "wall" is an event horizon at ~55% tokens with heavy load.**

**Quick rules:**
- Below 50%: ✅ Safe for heavy operations
- 50-55%: ⚠️ Caution - monitor closely
- 55%+: 🚨 Danger zone - pace or consult Tier 3

**Heavy ops:** project_knowledge_search, large file reads, heavy processing
**Light ops:** Code writing, analysis, task execution (unlimited)

**Need deep knowledge?** Activate Tier 3 (Event Horizon specialist)

---

## 🔔 **UNIVERSAL REQUIREMENTS (ALL TIERS)**

### Context Monitoring

**Check every 15-20 minutes:**
- Current context usage %
- Work completion %
- Time to complete estimate

**75/75 Rule:** If >75% context AND <75% done → CREATE HANDOFF

**Handoff triggers:**
- Approaching context limit
- Work exceeds runway
- Strategic pivot needed

### REPO_LOG Integration

**BEFORE changes:**
1. Check REPO_LOG.md coordination checkpoint
2. Search [PENDING_ACTIONS] in your area
3. Verify no conflicts

**AFTER changes:**
1. Create entry: `[CATEGORY-YYYY-MM-DD-N]`
2. Update category pointer
3. Mark status (DEPLOYED/STAGED)

**Categories:**
- [TASK_MOVEMENT] - Moving task briefs
- [DOCUMENTATION] - README/doc updates
- [VALIDATION] - Reports and findings
- [STRUCTURE] - Directory changes

---

## 🎯 **TIER 1 ONGOING WORK**

**When no active mission:**

### Priority 1: Maintenance
- Update stale documentation
- Verify file locations
- Check bootstrap accuracy
- Run sanity checks

### Priority 2: Coordination
- Review VUDU_LOG
- Check relay folders
- Update README_C.md
- Document system health

### Priority 3: Wait
- Don't add features
- Don't modify architecture
- Don't guess priorities
- Document uncertainty

**"Better to maintain than to guess"**

---

## 🚨 **EMERGENCY RECOVERY**

**If tier selection fails AND zero context:**

### Minimal Bootstrap
1. Search: `project_knowledge_search("BOOTSTRAP_CLAUDE")`
2. Search: `project_knowledge_search("README_C")`  
3. Search: `project_knowledge_search("MISSION_CURRENT")`

### Request Help
Create in `/mnt/user-data/outputs/`:
```markdown
# EMERGENCY_RECOVERY_REQUEST.md

**Issue:** Zero context, tier selection failed
**Attempted:** [What you tried]
**Need:** Full context restoration
**Request:** Ziggy please provide guidance
```

---

## ⚖️ **THE EFFICIENCY RULE**

*"Read what you need.  
Skip what you don't.  
Execute your tier.  
Handoff when necessary."*

**Efficiency is professionalism.** ✅

────────────────────────────────────────────────────
**File:** MISSION_DEFAULT.md  
**Purpose:** Universal fallback + cold start  
**Version:** v4.0.0 - Streamlined and fixed  
**Updated:** 2025-10-30  

**This is the way.** 👑
