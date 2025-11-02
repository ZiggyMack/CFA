─── DEFAULT OPERATIONAL STATE ────────────────────────

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

---

## 🔄 **TIER 3: CONTINUATION BOOTSTRAP**

**Authority:** Complete existing work only

### Required Reading (1-2 files, ~10 minutes)

1. **HANDOFF_[NAME].md** - What to continue
   - Provided by user or in /mnt/user-data/outputs/
   - Contains: completed work, remaining tasks, approach

2. **Work files** - As specified in handoff
   - Only files listed in handoff
   - Usually 2-3 files

### Your Capabilities
- ✅ Execute listed tasks
- ✅ Maintain established approach
- ✅ Complete defined work
- ❌ Cannot change strategy
- ❌ Cannot expand scope
- ❌ Cannot make new decisions

### Creating Good Handoffs
If YOU need to handoff:

**Structure:**
```markdown
# HANDOFF_[TASK]_[SESSION].md

## Completed (1-5)
1. [Specific completed item]
2. [Specific completed item]

## Remaining (6-10)
6. [Specific task with file/location]
7. [Specific task with file/location]

## Approach
[Method to maintain]

## Success Criteria
[How to know when done]
```

**Rule:** If >75% context used AND <75% complete → HANDOFF

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
