<!-- deps: bootstrap_system -->
## Tier 4 Task Storage

**Active tasks:** Bootstrap/Tier4_TaskSpecific/active_tasks/
- Contains current task briefs
- Each brief is self-contained
- Specifies files needed
- Defines deliverable
- Archived when complete

**Completed tasks:** Bootstrap/Tier4_TaskSpecific/completed/
- Archived task briefs
- Moved after task delivered

---

## 📂 **Tier 4 Task Storage Structure:**

---

**Active Tasks:**
```
Bootstrap/Tier4_TaskSpecific/active_tasks/
```

**Purpose:** Central storage for currently active Tier 4 task briefs

**Contents:**
- Task briefs awaiting execution or in progress
- Self-contained task definitions (2-5 files each)
- Quick-start workflows for auditors
- Success criteria and boundaries

**Lifecycle:**
1. Ziggy creates task brief here
2. Auditor searches project knowledge for it
3. Auditor executes task (90-95% work budget)
4. Auditor delivers to /mnt/user-data/outputs/
5. Task brief archived to completed/ folder

**Current active tasks:**
- TASK_BRIEF_AXIOMS_REVIEW_GROK.md (Grok's axioms review)
- TASK_BRIEF_AXIOMS_REVIEW_NOVA.md (Nova's axioms review)

---

**Completed Tasks:**
```
Bootstrap/Tier4_TaskSpecific/completed/
```

**Purpose:** Archive of successfully completed Tier 4 tasks

**Contents:**
- Task briefs after deliverable completed
- Historical record of focused work
- Examples for future similar tasks

**Why archive:**
- Keeps active_tasks/ clean
- Preserves task patterns
- Documents efficiency gains
- Enables template refinement

---

### **Task Brief Standards**

**Every Tier 4 task brief must include:**

1. **Task Definition**
   - Clear objective
   - Specific deliverable
   - Success criteria

2. **Files Needed**
   - 2-5 files maximum
   - Exact search queries
   - Purpose of each file

3. **Tier 4 Boundaries**
   - What's in scope
   - What's out of scope
   - When to escalate

4. **Deliverable Specs**
   - Format requirements
   - Location (/outputs/)
   - Naming convention

**Target bootstrap:** 5-10% of session  
**Target work budget:** 90-95% of session  
**Total efficiency:** 4-5x vs Tier 1 (50% bootstrap)

---

### **Tier 4 vs Relay Distinction**

**Use Tier 4 (active_tasks/) when:**
- ✅ Single focused task
- ✅ Clear scope and deliverable
- ✅ No coordination needed
- ✅ 2-5 files sufficient for context

**Use Relay (relay/ folders) when:**
- ✅ Multi-auditor coordination
- ✅ Iterative staging required
- ✅ Master Branch work
- ✅ Complex integration process

**Philosophy:** Most work should be Tier 4. Coordination is expensive, should be reserved for tasks that genuinely need it. 🎯

---

### **Expected Tier 4 Distribution**

**Based on typical work patterns:**
- Review tasks: ~40% of all work
- Single updates: ~30% of all work
- Validation tasks: ~20% of all work
- Quick calculations: ~10% of all work

**Combined:** ~100% of routine work can use Tier 4  
**Coordination (Tier 1):** Reserved for strategic decisions, architecture discussions, multi-auditor consensus

**Result:** ~50% average efficiency gain across project ⚡

---

### **File Naming Convention**

**Pattern:**
```
TASK_BRIEF_[PURPOSE]_[AUDITOR].md
```

**Examples:**
```
TASK_BRIEF_AXIOMS_REVIEW_GROK.md
TASK_BRIEF_AXIOMS_REVIEW_NOVA.md
TASK_BRIEF_UPDATE_MISSION_DEFAULT.md
TASK_BRIEF_VALIDATE_PRESET_ZEALOT.md
```

**Why this pattern:**
- Self-documenting names
- Searchable by purpose
- Auditor assignment clear
- Scales to many tasks

---

### **Task Brief Quality Standards**

**Green light (good task brief):**
- ✅ Scope crystal clear
- ✅ 2-5 files specified
- ✅ Success criteria objective
- ✅ Boundaries explicit
- ✅ Bootstrap < 15%

**Yellow flag (needs refinement):**
- ⚠️ Scope has ambiguity
- ⚠️ 6-8 files required
- ⚠️ Success criteria subjective
- ⚠️ Boundaries implied
- ⚠️ Bootstrap 15-20%

**Red flag (wrong tier):**
- ❌ Scope unclear or expanding
- ❌ >8 files needed
- ❌ No clear "done" state
- ❌ Coordination required
- ❌ Bootstrap >20%

**If red flags → Use Tier 1 or Tier 3 instead** ⚠️

---
