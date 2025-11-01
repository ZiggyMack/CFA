<!---
FILE: VUDU_LOG_LITE_TEMPLATE.md
PURPOSE: Template for lightweight VUDU coordination log entries (network travel)
VERSION: v3.7.2
STATUS: Active
DEPENDS_ON: VUDU_PROTOCOL.md, VUDU_HEADER_STANDARD.md, ROLE_LOGGER.md
NEEDED_BY: BOOTSTRAP_GROK.md, BOOTSTRAP_NOVA.md, BOOTSTRAP_VUDU_CLAUDE.md
MOVES_WITH: /auditors/relay/
LAST_UPDATE: 2025-11-01 [DOCUMENTATION-2025-11-01-16]
--->

<!-- deps: vudu_protocol, logger_claude -->

# VUDU_LOG_LITE

**Last Updated:** 2025-11-01
**Maintained by:** NOVA
**For network:** CFA VuDu v3.7+

---

## RECENT ENTRIES

### [COORDINATION-YYYY-MM-DD-1] YYYY-MM-DD - Brief Description

**Changed by:** [Your Name] ([Your Role])
**Session:** [session-id]
**Status:** [IN_PROGRESS / COMPLETED / STAGED / etc.]

**Changes:**
- [What happened in this coordination activity]
- [Another change or action taken]

**Reason:** [Why this coordination activity occurred]

**Impact:** [Minimal / Moderate / Significant]

---

### [COORDINATION-YYYY-MM-DD-2] YYYY-MM-DD - Next Entry

**Changed by:** [Your Name] ([Your Role])
**Session:** [session-id]
**Status:** [Status]

**Changes:**
- [What happened]

**Reason:** [Why]

**Impact:** [Impact level]

---

## 📋 USAGE INSTRUCTIONS

### **For External Auditors (Grok/Nova):**

**When creating transmission to Claude:**
1. Copy this template
2. Add your recent coordination entries since last transmission
3. Use chronological order (newest last)
4. Include enough context (usually last 5-10 entries or last week)
5. Save as `VUDU_LOG_LITE.md` in your staging folder
   - Grok: `/auditors/relay/Grok_Incoming/VUDU_LOG_LITE.md`
   - Nova: `/auditors/relay/Nova_Incoming/VUDU_LOG_LITE.md`
6. Include with your README_G.md or README_N.md transmission

**LOGGER Claude will:**
- Read your VUDU_LOG_LITE.md
- Validate format
- Merge into master `/auditors/VUDU_LOG.md`
- Provide you with updated VUDU_LOG_LITE.md from Claude_Incoming/

---

### **For LOGGER Claude (Claude side):**

**VUDU_LOG_LITE.md lives in:**
`/auditors/relay/Claude_Incoming/VUDU_LOG_LITE.md`

**Your responsibilities:**
1. **Incoming:** Merge external auditor VUDU_LOG_LITE → master VUDU_LOG
2. **Outgoing:** Append new entries to Claude_Incoming/VUDU_LOG_LITE.md
3. **Maintenance:** Keep file under ~500 lines (trim if needed)
4. **Enforcement:** Validate format, flag violations
5. **Distribution:** This file travels with every Claude transmission

**Default retention:**
- Keep last 30 entries OR last 14 days (whichever is more)
- Keep mission-critical entries even if beyond retention
- Add note when trimming: "Older entries trimmed - see master VUDU_LOG.md"

---

## 📐 FORMAT REQUIREMENTS

**Entry ID Format:**
```
[COORDINATION-YYYY-MM-DD-N]
```
- YYYY = 4-digit year
- MM = 2-digit month (01-12)
- DD = 2-digit day (01-31)
- N = sequential number for that day (1, 2, 3, etc.)

**Required Fields:**
- **Changed by:** Who made this entry
- **Session:** Session ID for traceability
- **Status:** Current status
- **Changes:** What happened (bulleted list)
- **Reason:** Why it happened
- **Impact:** Minimal/Moderate/Significant

**Chronological Order:**
- Newest entries at the BOTTOM
- Older entries at the top
- This allows easy appending

---

## ⚠️ COMMON MISTAKES

**❌ Wrong Entry ID:**
```
[COORDINATION-20251101]  ← Missing hyphens
[COORDINATION-2025-11-1] ← Day not zero-padded
```

**✅ Correct Entry ID:**
```
[COORDINATION-2025-11-01-1]
```

**❌ Missing Required Fields:**
```
### [COORDINATION-2025-11-01-1] Message sent

**Changes:**
- Sent message to Grok
```
Missing: Changed by, Session, Status, Reason, Impact

**✅ Complete Entry:**
```
### [COORDINATION-2025-11-01-1] Message sent to Grok

**Changed by:** LOGGER_CLAUDE (VUDU_LOG Custodian)
**Session:** claude/session-123
**Status:** COMPLETED ✅

**Changes:**
- Sent empirical validation request to Grok
- Included VUDU_LOG_LITE.md context

**Reason:** Need empirical validation of YPA calculations

**Impact:** Minimal (routine coordination)
```

---

## 🎯 FILE SIZE GUIDELINES

**Target:** Under 500 lines total

**When approaching limit:**
1. LOGGER Claude will trim older entries
2. Keep last 30 entries OR last 14 days
3. Add note: "Older entries trimmed - see master VUDU_LOG.md"
4. Ensure enough context remains for participants

**Exception:**
If mission-critical entries exist in older content, keep them even if beyond normal retention.

---

## 📖 RELATIONSHIP TO MASTER VUDU_LOG

**VUDU_LOG_LITE:**
- Lightweight excerpt
- Travels on network
- Maintained by LOGGER Claude (Claude side)
- Created by external auditors (their side)
- Appended and trimmed as needed

**Master VUDU_LOG:**
- Complete history
- Lives in `/auditors/VUDU_LOG.md`
- Maintained only by LOGGER Claude
- Never travels on network
- Comprehensive record

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

**This template is maintained by LOGGER Claude**
**Last template update:** 2025-11-01
**Version:** 1.0

**For questions:** Request help from LOGGER Claude via README_G.md / README_N.md

📡 **VUDU Network Coordination Made Simple** 📡
