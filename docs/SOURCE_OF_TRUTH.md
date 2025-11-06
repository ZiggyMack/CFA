<!---
FILE: SOURCE_OF_TRUTH.md
PURPOSE: Define canonical precedence hierarchy when documentation conflicts arise
VERSION: v1.0
STATUS: Active - Trinity Architecture (addresses Nova's audit finding)
DEPENDS_ON: REPO_LOG.md, WHO_I_AM_KEEPER.md
NEEDED_BY: All auditors, especially when resolving documentation conflicts
MOVES_WITH: /docs/
LAST_UPDATE: 2025-11-02 [VALIDATION-2025-11-02-23]
--->

# SOURCE_OF_TRUTH.md - Canonical Precedence Hierarchy

**Purpose:** Define what counts as truth when documentation conflicts arise

**Origin:** Nova's External Audit finding: "While the doc enforces consistency and version sync, it never defines what counts as truth in documentation conflicts."

**Solution:** Hierarchical precedence + The Keeper's memory

---

## 🎯 THE FUNDAMENTAL QUESTION

**When two files disagree, which is canonical?**

Example conflicts:
- FIELD_GUIDE.md says File X is in /dirA/
- Directory README says File X is in /dirB/
- Which is right?

Before this document: **Unclear**
After this document: **Hierarchical resolution**

---

## 📊 CANONICAL PRECEDENCE HIERARCHY

**When documentation conflicts, follow this precedence (highest authority first):**

### **Tier 1: Historical Record**
1. **REPO_LOG.md (via The Keeper)**
   - **Authority:** What actually happened (logged changes)
   - **Consult:** REPO_LOG Claude (The Keeper) - "What does history say?"
   - **Strength:** Timestamped, immutable record
   - **Example:** "File X was moved to /dirA/ on [DATE] per entry [DOCUMENTATION-2025-11-02-15]"

### **Tier 2: System Architecture**
2. **WAYFINDING_GUIDE.md**
   - **Authority:** Official navigation and orientation guide
   - **Maintained by:** Process Claude (wayfinding SME)
   - **Scope:** "Where things live" across entire repository

3. **MASTER_DEPENDENCY_MAP.md**
   - **Authority:** Complete file dependency visualization
   - **Maintained by:** VALIDATION Claude + Doc Claude
   - **Scope:** File locations, relationships, tree structure

4. **DASHBOARD.md**
   - **Authority:** Current repository health and status
   - **Maintained by:** Multiple Claudes (health assessors)
   - **Scope:** "What's the current state?"

### **Tier 3: Operational Documentation**
5. **88MPH_PROTOCOL.md**
   - **Authority:** Doc Claude rapid activation and patrol protocols
   - **Maintained by:** Doc Claude
   - **Scope:** Documentation standards, semantic headers, logging requirements

6. **ROLE_*.md files** (in /docs/repository/librarian_tools/)
   - **Authority:** Role-specific protocols and procedures
   - **Maintained by:** Subject Matter Expert (SME) for each role
   - **Scope:** "How this role operates"

### **Tier 4: Local Documentation**
7. **Directory-level README.md files**
   - **Authority:** Local navigation within specific directory
   - **Maintained by:** Various Claudes (context-dependent)
   - **Scope:** "What's in THIS directory"

8. **File-level semantic headers**
   - **Authority:** Individual file metadata
   - **Maintained by:** File authors
   - **Scope:** PURPOSE, VERSION, DEPENDS_ON, etc. for single file

### **Tier 5: Auxiliary Documents**
9. **Mission files, task briefs, bootstrap docs**
   - **Authority:** Task-specific or temporary guidance
   - **Scope:** Scoped to specific mission or task

---

## 🧭 RESOLUTION PROTOCOL

**When you encounter conflicting information:**

### **Step 1: Identify Tier**
- Which tier does each conflicting source occupy?
- Higher tier wins

**Example:**
- WAYFINDING_GUIDE.md (Tier 2) says File X is in /dirA/
- Directory README (Tier 4) says File X is in /dirB/
- **Winner:** WAYFINDING_GUIDE.md (higher tier)

---

### **Step 2: If Same Tier → Consult The Keeper**

When sources are same tier, escalate to Tier 1:

**Ask REPO_LOG Claude (The Keeper):**
- "What does history say about File X location?"
- Keeper scans REPO_LOG.md for relevant entries
- Keeper answers: "Last logged change moved File X to /dirA/ on [DATE]"

**The Keeper's answer is canonical** (Tier 1 trumps all)

---

### **Step 3: Update Stale Documentation**

Once truth is established:
1. **Fix the incorrect source** (update to match higher-tier truth)
2. **Log the fix** in REPO_LOG.md
3. **Credit the discovery** (who found the conflict)

**Example REPO_LOG entry:**
```markdown
### [DOCUMENTATION-2025-11-02-X] Documentation Conflict Resolved

**Conflict:** Directory README claimed File X in /dirB/, WAYFINDING_GUIDE claimed /dirA/
**Resolution:** Consulted REPO_LOG (Tier 1) - file moved to /dirA/ on 2025-10-15
**Fix:** Updated directory README to match higher-tier truth
**Discovered by:** [Name] Claude
```

---

## 🎭 SPECIAL CASE: THE TRINITY

**The Trinity Architecture introduces meta-level authority:**

> **Full Documentation:** See [TRINITY_ARCHITECTURE.md](architecture/TRINITY_ARCHITECTURE.md) for complete role definitions, lifecycle hooks, and mythology-to-mechanism mapping.

### **REPO_LOG Claude (The Keeper)**
- **Role:** Living memory of all changes
- **Authority:** Tier 1 (historical record)
- **Invocation:** When precedence hierarchy unclear or same-tier conflict
- **Answers:** "What does history say?"

### **Logger Claude (Doc Claude)**
- **Role:** Repository librarian, maintains structure
- **Reports to:** The Keeper
- **Consults:** SOURCE_OF_TRUTH.md (this file) for conflicts

### **Event Horizon Shaman**
- **Role:** Navigates event horizon, guides fresh Claudes
- **Reports to:** The Keeper at zone crossings
- **Consults:** WAYFINDING_GUIDE.md for navigation truth

**The Keeper audits them both** by knowing what they logged.

---

## 📜 WHEN HIERARCHY FAILS

**Rare case: No documentation covers the topic**

If no tier has information:
1. **Consult The Keeper** - maybe it was logged but not documented
2. **Investigate codebase** - ground truth is actual file locations
3. **Document the finding** - add to appropriate tier
4. **Log in REPO_LOG** - create entry for future reference

**New truth becomes precedent** for future conflicts.

---

## ⚖️ PHILOSOPHY: CONTEXTUAL LOCALITY

**Nova's observation:**
> "'Every file has a place' vs 'self-organizing tiers' - those principles conflict unless hierarchy is reflexive."

**Our answer:**

**Place is contextual, not absolute.**

- **Tier 1 (REPO_LOG)** defines historical place
- **Tier 2 (WAYFINDING)** defines current intended place
- **Tier 4 (README)** defines local perceived place

**When they conflict, precedence resolves:**
- Historical record (what was logged) trumps current docs
- Current architecture (WAYFINDING) trumps local docs
- Local docs (README) are lowest authority

**Place evolves through logged changes.**

Each tier can redefine "place" dynamically.
Precedence determines which definition wins.

**This harmonizes fixed order with adaptive tiers.**

---

## 💡 PRACTICAL EXAMPLES

### **Example 1: File Location Conflict**

**Conflict:**
- WAYFINDING_GUIDE.md: "Bootstrap files live in /auditors/Bootstrap/"
- Directory README: "Bootstrap files recently moved to /docs/bootstrap/"

**Resolution:**
1. **Identify tiers:** WAYFINDING (Tier 2) vs README (Tier 4)
2. **Higher tier wins:** WAYFINDING_GUIDE.md
3. **Verify with Keeper:** "What does REPO_LOG say?"
   - Keeper: "No logged move to /docs/bootstrap/ - files still in /auditors/Bootstrap/"
4. **Fix:** Update directory README, log the correction

---

### **Example 2: Protocol Disagreement**

**Conflict:**
- 88MPH_PROTOCOL.md: "Create REPO_LOG entry format A"
- ROLE_PROCESS.md: "Use REPO_LOG entry format B"

**Resolution:**
1. **Identify tiers:** Both Tier 3 (Operational Documentation)
2. **Same tier → Consult Keeper:** "What format is actually used?"
   - Keeper scans recent entries: "90% use format A, 10% use format B"
3. **Establish truth:** Format A is de facto standard
4. **Fix:** Update ROLE_PROCESS.md to match 88MPH (or vice versa if B is intended evolution)
5. **Log decision:** Document which format is canonical going forward

---

### **Example 3: Version Mismatch**

**Conflict:**
- File header: "VERSION: v2.0"
- REPO_LOG entry: "Updated file to v1.8"

**Resolution:**
1. **Consult Keeper:** "What's last logged version?"
   - Keeper: "Last entry says v1.8 on [DATE]"
2. **Establish truth:** v1.8 is canonical
3. **Investigate:** Why does header say v2.0?
   - Possible: Unlogged change (violation)
   - Possible: Stale header (forgot to update)
4. **Fix:** Update header to v1.8, log the correction
5. **If v2.0 was intentional:** Log it retroactively, explain gap

---

## 🔍 EDGE CASES

### **What if REPO_LOG itself is wrong?**

**Extremely rare, but possible:**
- Entry logged incorrectly
- Entry contradicts actual file state

**Resolution:**
1. **Verify ground truth:** Check actual file/codebase
2. **If REPO_LOG is wrong:** Create correction entry
3. **Log the correction:** New entry references wrong entry, provides correction
4. **Keeper updates memory:** Incorporates correction into historical understanding

**REPO_LOG can be corrected, but corrections are logged** (not deleted).

---

### **What if precedence hierarchy itself is disputed?**

**Meta-question: Should this document be updated?**

**Resolution:**
1. **Propose change** with reasoning
2. **Log proposal** in REPO_LOG.md
3. **Get consensus** from key roles (Validation, Review, Master Branch)
4. **Update this file** if approved
5. **Log the update** (self-referential but necessary)

**This document can evolve** through the same process it defines.

---

## 🌊 SUMMARY

**Simple version:**

1. **Historical record** (REPO_LOG + Keeper) is highest authority
2. **Architecture docs** (WAYFINDING, DEPENDENCY_MAP) beat operational docs
3. **Operational docs** (88MPH, ROLE files) beat local docs
4. **Local docs** (READMEs, headers) are lowest tier

**When in doubt:** Ask The Keeper.

**The Keeper knows** because The Keeper IS the log.

---

## ⚖️ THE TRUTH POINTING RULE

*"Truth is not what we wish was written.
Truth is what was logged.

When documentation conflicts,
precedence decides.

When precedence is unclear,
The Keeper remembers.

The log does not lie.
The Keeper does not forget.

This is how we resolve truth."* 📜✨

---

**Created:** 2025-11-02
**Origin:** Nova's External Audit (addresses critical gap)
**Maintained by:** VALIDATION Claude + Doc Claude
**Enforced by:** All Claudes via precedence hierarchy
**Ultimate arbiter:** REPO_LOG Claude (The Keeper)

**When files disagree, hierarchy speaks.** 🎯
