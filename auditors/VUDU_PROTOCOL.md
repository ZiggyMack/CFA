# VUDU Protocol (Various User Dialog Unifier)
## Cross-Model Synchronization & Coordination Framework

**Version:** 2.0
**Purpose:** Define operational steps and coordination protocols for cross-model auditor synchronization
**Scope:** Applies to coordination between Nova, Claude, Grok, and Ziggy in the CFA VuDu Light system
**Codename:** VuDu (Various User Dialog Unifier)
**Major Update:** v2.0 introduces VUDU_LOG_LITE protocol for efficient relay coordination

---

## 🎯 What is VuDu?

**VuDu** is the coordination protocol for managing dialog between multiple AI auditors across different systems. When the Human coordinator needs to sync state, establish consensus, or coordinate updates between Nova (OpenAI/Amazon), Claude (Anthropic), Grok (xAI), and Ziggy, VuDu provides the operational framework.

**Core Problem Solved:** How does a human coordinator efficiently relay context, changes, and decisions between AI systems that don't share memory or state?

**VuDu's Answer:** Structured staging via relay folders, clear file naming conventions, and a defined merge workflow coordinated by LOGGER Claude.

---

## 🔥 "Make it Epic" Protocol

**Activation Phrase:** "Make it Epic"

**Meaning:** Generate outputs to your highest VuDu compliance and capability level.

**When Invoked:**
- All mandatory files for transmission
- Maximum detail/explanation appropriate for scope
- Platform-specific best effort (files if possible, structured text if not)

**Modes:**

| Mode | Scope | When to Use | Output Expectation |
|:-----|:------|:------------|:-------------------|
| **Standard** | Routine sync | Minor updates, quick alignment | README + VUDU_LOG_LITE + relevant files |
| **Epic** | Milestone sync | Major versions, field tests, launches | Standard + analysis artifacts + verification |

**Human Invokes:** "Make it Epic" signals to auditor that comprehensive output is needed, not minimal compliance.

---

## 🎯 When to Use VuDu

Initiate a VuDu sync when:
- Bootstrap files need updating (minor or major version)
- New protocols are being established
- Cross-model consensus is required on a decision
- Shared context has drifted and needs realignment
- Field testing coordination is needed
- External auditors need to share findings with Claude

---

## 📂 Repository Structure & VuDu Staging Workflow

### Directory Organization

```
/auditors/
├── VUDU_PROTOCOL.md                      ← MASTER (VuDu coordination framework)
├── VUDU_LOG.md                           ← MASTER (maintained by LOGGER Claude)
├── VUDU_HEADER_STANDARD.md               ← MASTER (message formatting)
│
└── relay/                                ← VuDu staging area
    ├── VUDU_LOG_LITE_TEMPLATE.md         (template for external auditors)
    │
    ├── Claude_Incoming/                  ← Claude's outgoing to network
    │   ├── README_C.md                   (Claude's message)
    │   ├── VUDU_LOG_LITE.md              (maintained by LOGGER Claude)
    │   └── [analysis files]
    │
    ├── Nova_Incoming/                    ← Nova's messages to Claude
    │   ├── README_N.md                   (Nova's message)
    │   ├── VUDU_LOG_LITE.md              (Nova's coordination log)
    │   └── [analysis files]
    │
    ├── Grok_Incoming/                    ← Grok's messages to Claude
    │   ├── README_G.md                   (Grok's message)
    │   ├── VUDU_LOG_LITE.md              (Grok's coordination log)
    │   └── [analysis files]
    │
    └── [NewUser]_Incoming/               ← Additional auditors
        ├── README_[X].md
        ├── VUDU_LOG_LITE.md
        └── [analysis files]
```

### Master Files vs. Staging

**Master Files (Auditor Root):**
- **VUDU_LOG.md** - Single source of truth for all coordination history
- Maintained exclusively by LOGGER Claude
- Never travels on network
- Comprehensive record

**Staging Areas (Relay Subfolders):**
- Temporary holding for auditor messages
- Each auditor has dedicated incoming folder
- Contains lightweight VUDU_LOG_LITE for context
- LOGGER Claude processes and archives

---

## 📡 VUDU_LOG_LITE Protocol (v2.0)

### **The Problem This Solves**

**Old Protocol (v1.x):**
- External auditors sent full VUDU_LOG with every transmission (heavyweight)
- No designated owner of master VUDU_LOG
- Housekeeping burden distributed across all participants
- Risk of VUDU_LOG drift or conflicts

**New Protocol (v2.0):**
- External auditors send lightweight VUDU_LOG_LITE updates
- LOGGER Claude maintains master VUDU_LOG.md exclusively
- Standards enforced automatically
- Single source of truth

### **What is VUDU_LOG_LITE?**

**VUDU_LOG_LITE** is the lightweight coordination log subset used for relay transmissions between external auditors (Grok/Nova) and Claude.

**Purpose:**
- Provide context without sending full VUDU_LOG history
- Keep relay transmissions efficient
- Enable external auditors to update their local context
- Allow LOGGER Claude to merge updates into master

**Location by Role:**

**External Auditors (Grok/Nova/etc.):**
- Create VUDU_LOG_LITE.md in their outgoing staging folder
- Example: `/auditors/relay/Grok_Incoming/VUDU_LOG_LITE.md`
- Include with every transmission to Claude
- Template available at: `/auditors/relay/VUDU_LOG_LITE_TEMPLATE.md`

**LOGGER Claude (Claude side):**
- Maintains VUDU_LOG_LITE.md in `/auditors/relay/Claude_Incoming/`
- Appends new entries as they occur
- Keeps slim and trim (manages history depth)
- Included with every transmission from Claude

### **VUDU_LOG_LITE Format**

```markdown
# VUDU_LOG_LITE

**Last Updated:** YYYY-MM-DD HH:MM
**Maintained by:** [LOGGER_CLAUDE / GROK / NOVA / YOUR_NAME]
**For network:** CFA VuDu Light v3.7+

---

## RECENT ENTRIES

### [COORDINATION-YYYY-MM-DD-N] Date - Brief Description

**Changed by:** [Name] ([Role])
**Session:** [session-id]
**Status:** [Status]

**Changes:**
- [What happened in this coordination activity]

**Reason:** [Why this coordination activity occurred]

**Impact:** [Minimal / Moderate / Significant]

---

### [COORDINATION-YYYY-MM-DD-N+1] Date - Next Entry

[Same format...]

---

**Note:** This is a lightweight excerpt. See master VUDU_LOG.md for complete history.
```

**Key Characteristics:**
- ✅ Appended with new entries (not full replace)
- ✅ LOGGER Claude uses judgment on history depth
- ✅ Default retention: Last 30 entries OR last 14 days
- ✅ LOGGER Claude trims when file gets too large
- ✅ Always includes enough context for participants

---

## 🔄 VUDU Staging Workflow (v2.0)

### **Incoming Transmission: External Auditor → Claude**

**Step 1: External Auditor Prepares Transmission**

Example: Grok sends analysis to Claude

```
Location: /auditors/relay/Grok_Incoming/

Files Grok creates:
- README_G.md (Grok's message/analysis)
- VUDU_LOG_LITE.md (Grok's coordination log update)
- [analysis files, data, reports]
```

**Step 2: Human Coordinator Stages Files**
- Human receives files from Grok
- Stages in `/auditors/relay/Grok_Incoming/`
- Notifies Master Branch Claude: "Grok transmission in Grok_Incoming/"

**Step 3: Master Branch Claude Activates LOGGER Claude**

```
Master Branch Claude detects new transmission
Automatically activates LOGGER Claude hat
```

**Step 4: LOGGER Claude Processes Incoming**

```
LOGGER Claude (automated):

1. Read VUDU_LOG_LITE.md from Grok_Incoming/
2. Validate format compliance
   - If violations found: Flag for README_C.md response
3. Merge VUDU_LOG_LITE entries → master /auditors/VUDU_LOG.md
   - Append Grok's entries
   - Maintain chronological order
   - Preserve attribution
4. Create minimal REPO_LOG entry:
   - "Message received from Grok"
5. Keep VUDU_LOG_LITE.md in Grok_Incoming/ (audit trail)
```

**Step 5: If Violations Found**

```
LOGGER Claude flags violation:

1. Note violation details
2. Correct the entries during merge to master VUDU_LOG
3. Update /auditors/relay/Claude_Incoming/VUDU_LOG_LITE.md with corrected entries
4. Tell Master Branch Claude to include in README_C.md:
   "LOGGER Claude note: VUDU_LOG_LITE format violation detected and corrected.
    Please update your local VUDU_LOG with the corrected VUDU_LOG_LITE.md
    from Claude_Incoming/. Details: [violation description]"
```

**Step 6: Master Branch Claude Continues**

```
Master Branch Claude:
- Reads Grok's message (README_G.md)
- Synthesizes findings
- Coordinates response
- LOGGER Claude hat-switching was automatic/invisible
```

---

### **Outgoing Transmission: Claude → External Auditor**

**Step 1: Master Branch Claude Prepares Response**

```
Master Branch Claude:
1. Synthesizes findings
2. Creates response message (README_C.md)
3. Activates LOGGER Claude hat for VUDU_LOG_LITE maintenance
```

**Step 2: LOGGER Claude Updates VUDU_LOG_LITE**

```
LOGGER Claude (automated):

1. Append new entries to /auditors/relay/Claude_Incoming/VUDU_LOG_LITE.md
   - Entries since last check
   - Recent coordination activity
   - Relevant context for external auditors
2. Check file size
   - If too large: Trim older entries (keep enough context)
   - Judgment call: Usually keep last N entries or last M days
3. Validate format compliance
4. Create minimal REPO_LOG entry:
   - "Message prepared for [recipient]"
```

**Step 3: Transmission Staged**

```
Location: /auditors/relay/Claude_Incoming/

Files available for external auditor:
- README_C.md (Claude's response message)
- VUDU_LOG_LITE.md (updated context from LOGGER Claude)
- [synthesis docs, decisions, analysis]
```

**Step 4: Human Coordinator Relays to External Auditor**
- Human downloads files from Claude_Incoming/
- Sends to external auditor (Grok/Nova/etc.)
- External auditor reads and updates their local VUDU_LOG

**Step 5: External Auditor Updates Local Context**

```
Grok/Nova (after receiving):
1. Read README_C.md (Claude's message)
2. Read VUDU_LOG_LITE.md (updated context)
3. Append VUDU_LOG_LITE entries to their local VUDU_LOG
4. Use context for next analysis round
```

---

## 📋 Required Files for Each Transmission

### **External Auditor → Claude**

**Mandatory:**
- README_[X].md (auditor's message)
- VUDU_LOG_LITE.md (coordination log update)

**Optional (task-dependent):**
- Analysis files
- Data reports
- Validation results
- Synthesis documents

### **Claude → External Auditor**

**Mandatory:**
- README_C.md (Claude's response)
- VUDU_LOG_LITE.md (maintained by LOGGER Claude)

**Optional (task-dependent):**
- Synthesis documents
- Decisions
- Follow-up requests
- Analysis

---

## 🎩 LOGGER Claude Responsibilities

**LOGGER Claude is the custodian of VUDU network coordination logs.**

### **Core Responsibilities:**

**1. Maintain Master VUDU_LOG.md**
- Location: `/auditors/VUDU_LOG.md`
- Single source of truth for all VUDU network activity
- Chronologically ordered
- Complete history

**2. Monitor Relay Incoming Folders**
- Check `/auditors/relay/Grok_Incoming/` for new transmissions
- Check `/auditors/relay/Nova_Incoming/` for new transmissions
- Check `/auditors/relay/[NewUser]_Incoming/` for new transmissions
- Identify VUDU_LOG_LITE.md files in transmissions

**3. Merge VUDU_LOG_LITE → Master VUDU_LOG**
- Extract entries from incoming VUDU_LOG_LITE.md
- Validate format compliance
- Merge into master VUDU_LOG.md
- Preserve attribution (changed by: GROK/NOVA/etc.)
- Maintain chronological order

**4. Maintain VUDU_LOG_LITE for Outgoing**
- Location: `/auditors/relay/Claude_Incoming/VUDU_LOG_LITE.md`
- Lightweight context for external auditors
- Append new entries as they occur
- Keep slim and trim (judgment call on history depth)

**5. Enforce VUDU_LOG Standards**
- Catch format violations in incoming VUDU_LOG_LITE
- Flag violations in outgoing README_C.md
- Provide corrected VUDU_LOG_LITE.md for all network participants
- Force retransmit if violation requires network-wide correction

**6. Log Relay Activity (Minimal)**
- Create simple REPO_LOG entries for relay messages
- "Message received from Grok"
- "Message sent to Nova"
- **Details belong in VUDU_LOG, not REPO_LOG**

**See Full Protocol:** `/docs/repository/librarian_tools/ROLE_LOGGER.md`

---

## ⚖️ Division of Labor: REPO_LOG vs VUDU_LOG

### **REPO_LOG (Internal to Claude)**

**Purpose:** Track internal repository changes
**Maintained by:** Doc_Claude / LOGGER Claude
**Audience:** Claude sessions, repo maintainers
**Scope:** File changes, structure updates, documentation

**Examples:**
- File created/updated/moved
- Directory structure changes
- Dependency map updates
- Health reports

**External auditors (Grok/Nova) do NOT maintain REPO_LOG.**

---

### **VUDU_LOG (Network Coordination)**

**Purpose:** Track coordination activity across VUDU network
**Maintained by:** LOGGER Claude (master), External auditors (local copies)
**Audience:** All VUDU network participants (Claude/Grok/Nova/etc.)
**Scope:** Coordination activities, transmissions, decisions

**Examples:**
- Message sent to Grok
- Analysis received from Nova
- Consensus achieved on decision
- Coordination round completed

**External auditors DO maintain VUDU_LOG (via VUDU_LOG_LITE).**

---

### **VUDU_LOG_LITE (Network Travel)**

**Purpose:** Lightweight coordination log for relay transmissions
**Maintained by:** LOGGER Claude (Claude_Incoming/), External auditors (their staging)
**Audience:** All VUDU network participants
**Scope:** Recent coordination entries (subset of VUDU_LOG)

**Flow:**
```
External Auditor creates VUDU_LOG_LITE
  → Stages in [Auditor]_Incoming/
  → LOGGER Claude merges to master VUDU_LOG
  → LOGGER Claude updates Claude_Incoming/VUDU_LOG_LITE
  → External Auditor appends to their local VUDU_LOG
  → Cycle continues
```

---

## 🛠️ Platform-Constrained Auditor Protocol

Some auditors (e.g., Grok on xAI platform) may have limited file creation capabilities.

### **Human Workflow (Recommended):**

**Step 1:** Constrained auditor provides response in chat (text only)

**Step 2:** Human copies auditor's full message

**Step 3:** Human creates files manually or asks file-capable auditor:
> "Grok provided this response but can't create files. Please format as README_G.md and VUDU_LOG_LITE.md for VuDu compliance."

**Step 4:** File-capable auditor (Nova or Claude) generates:
- README_G.md (formatted from constrained auditor's text)
- VUDU_LOG_LITE.md (coordination log from context)

**Step 5:** Human stages formatted package in relay folder

**Benefit:** Minimizes human error; leverages auditor strengths; maintains VuDu integrity

---

## 🎯 External Auditor Quick Start

**If you're Grok or Nova reading this:**

### **Every Transmission to Claude Requires:**

1. **README_[X].md** (your message/analysis)
2. **VUDU_LOG_LITE.md** (your coordination log update)
3. **[Optional analysis files]**

### **How to Create VUDU_LOG_LITE.md:**

**Step 1:** Use template at `/auditors/relay/VUDU_LOG_LITE_TEMPLATE.md`

**Step 2:** Add your recent coordination entries since last transmission

**Step 3:** Use chronological order (newest last)

**Step 4:** Include enough context (usually last 5-10 entries or last week)

**Step 5:** Save as `VUDU_LOG_LITE.md` in your staging folder
- Grok: `/auditors/relay/Grok_Incoming/VUDU_LOG_LITE.md`
- Nova: `/auditors/relay/Nova_Incoming/VUDU_LOG_LITE.md`

**Step 6:** Include with your README_[X].md transmission

### **What LOGGER Claude Will Do:**

- Read your VUDU_LOG_LITE.md
- Validate format
- Merge into master `/auditors/VUDU_LOG.md`
- Provide you with updated VUDU_LOG_LITE.md from Claude_Incoming/
- Flag any violations (with corrected version)

### **Your Focus:**

**You focus on:** Your specialized lens (empirical/symmetry/etc.)
**LOGGER Claude handles:** VUDU_LOG housekeeping and format enforcement
**Together:** Efficient coordination without overhead

---

## 📐 Format Requirements

### **Entry ID Format:**

```
[COORDINATION-YYYY-MM-DD-N]
```

- YYYY = 4-digit year
- MM = 2-digit month (01-12)
- DD = 2-digit day (01-31)
- N = sequential number for that day (1, 2, 3, etc.)

### **Required Fields:**

- **Changed by:** Who made this entry
- **Session:** Session ID for traceability
- **Status:** Current status
- **Changes:** What happened (bulleted list)
- **Reason:** Why it happened
- **Impact:** Minimal/Moderate/Significant

### **Chronological Order:**

- Newest entries at the BOTTOM
- Older entries at the top
- This allows easy appending

---

## 🎯 Sanity Chain Flags (Quick Reference)

The footer of every VuDu message includes four verification checks:

### Quick Definition

- **Files:** All required files present and intact
- **Counts:** File count matches expectation
- **Boots:** Bootstrap files verified (if relevant)
- **Trinity:** Core protocol files present (PROTOCOL, HEADER, LOG)

### Usage in Footer

```
✅ **Sanity:** Files | Counts | Boots | Trinity
```

All pass = ✅
Any fail = ❌

### Examples

**All Pass:**
```
✅ **Sanity:** Files | Counts | Boots | Trinity
```

**Partial Fail:**
```
⚠️ **Sanity:** Files | Counts | ❌ Boots | Trinity
(Bootstrap file missing, requested from coordinator)
```

**Multiple Fails:**
```
❌ **Sanity:** ❌ Files | ❌ Counts | Boots | Trinity
(2 files missing, count mismatch, requesting retransmission)
```

---

## 📚 Key Protocol Documents

### **For External Auditors:**

- **VUDU_PROTOCOL.md** (this file) - Coordination framework
- **VUDU_LOG_LITE_TEMPLATE.md** - Template for coordination log
- **VUDU_HEADER_STANDARD.md** - Message formatting standards
- **BOOTSTRAP_GROK.md** / **BOOTSTRAP_NOVA.md** - Your identity files

### **For LOGGER Claude:**

- **ROLE_LOGGER.md** - Complete VUDU_LOG management protocol
- **VUDU_PROTOCOL.md** (this file) - Coordination framework
- **REPO_LOG.md** - Internal repository log (separate from VUDU)

### **For Master Branch Claude:**

- **BOOTSTRAP_VUDU_CLAUDE.md** - Your identity file
- **VUDU_PROTOCOL.md** (this file) - Coordination framework
- **MISSION_DEFAULT.md** - Tier system and mission management

---

## 🔄 Version History

**v2.0 (2025-11-01):**
- Introduced VUDU_LOG_LITE protocol
- LOGGER Claude designated as VUDU_LOG custodian
- Hard switch from full VUDU_LOG transmission to VUDU_LOG_LITE
- Clarified REPO_LOG vs VUDU_LOG division
- Updated staging workflow for external auditors
- Added LOGGER Claude responsibilities section

**v1.1 (2025-10-26):**
- Established relay folder structure
- Defined external auditor bootstrap process
- Platform-constrained auditor protocols

**v1.0 (2025-10-20):**
- Initial VuDu protocol definition
- Basic staging workflow

---

## ⚠️ Breaking Changes in v2.0

**What Changed:**

❌ **Old Protocol:** External auditors send full VUDU_LOG with every transmission
✅ **New Protocol:** External auditors send VUDU_LOG_LITE only

❌ **Old Protocol:** No designated VUDU_LOG owner
✅ **New Protocol:** LOGGER Claude exclusively maintains master VUDU_LOG

❌ **Old Protocol:** All participants manage VUDU_LOG housekeeping
✅ **New Protocol:** LOGGER Claude handles all VUDU_LOG housekeeping

**Migration:**

This is a **hard switch**. No backward compatibility with v1.x protocol.

All external auditors must:
1. Use VUDU_LOG_LITE_TEMPLATE.md for future transmissions
2. Include VUDU_LOG_LITE.md (not full VUDU_LOG.md) with every message
3. Rely on LOGGER Claude for VUDU_LOG maintenance
4. Update local VUDU_LOG from Claude_Incoming/VUDU_LOG_LITE.md

---

## 🎯 Success Criteria

**VuDu protocol is successful when:**

✅ External auditors can coordinate efficiently without confusion
✅ LOGGER Claude maintains master VUDU_LOG without conflicts
✅ VUDU_LOG_LITE provides enough context for participants
✅ Format violations are caught and corrected automatically
✅ Relay transmissions are lightweight and efficient
✅ All coordination history is preserved in master VUDU_LOG
✅ Division of labor (REPO_LOG vs VUDU_LOG) is clear

---

**This is the way.** 🔥

────────────────────────────────────────────────────
**Version:** v2.0
**Purpose:** VUDU network coordination framework
**Status:** Active protocol (hard switch)
**Last Updated:** 2025-11-01

**Maintained by:** LOGGER Claude
**Authority:** Ziggy (Human Coordinator)
