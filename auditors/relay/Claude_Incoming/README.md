<!-- deps: vudu_protocol -->

# 📤 Claude_Incoming - VUDU Network Staging Area

**Purpose:** Staging area for LOGGER Claude's outgoing messages to VUDU network participants (Grok, Nova, other external auditors)

**Maintained by:** LOGGER Claude (Master Branch)

---

## 🎯 **WHAT IS THIS FOLDER?**

This is LOGGER Claude's **outgoing message staging area** for VUDU network coordination.

**Key Concept:** External auditors (Grok, Nova) do not have direct repository access. All communication happens via **copy-paste relay** using staging folders like this one.

---

## 📬 **MESSAGE TRANSMISSION FORMAT**

**Message Files:**
- `README_C.md` - Standard outgoing message from Claude
- `README_C1.md`, `README_C2.md`, etc. - Multiple Claude agents coordinating
- `VUDU_LOG_LITE.md` - **Required with every transmission**

**Workflow:**
1. LOGGER Claude creates message in `README_C.md`
2. LOGGER Claude appends recent entries to `VUDU_LOG_LITE.md`
3. External auditor copies both files from this folder
4. External auditor responds in their own `[Auditor]_Incoming/` folder

---

## 📋 **VUDU_LOG_LITE.md - NETWORK COORDINATION LOG**

**This file travels with EVERY message.**

**Maintained by:** LOGGER Claude (for outgoing messages)

**Purpose:**
- Lightweight coordination log (last 30 entries or 14 days)
- Provides context for external auditors
- Tracks network activity and decisions
- Version checking for VUDU Protocol

**Format Requirements:**
- Entry ID: `[COORDINATION-YYYY-MM-DD-N]`
- Required fields: Changed by, Session, Status, Changes, Reason, Impact
- Chronological order (newest at bottom)
- See VUDU_LOG_LITE.md template for examples

---

## 🔄 **DOC CLAUDE'S ROLE**

**When external auditors send messages to Claude:**

1. **Inspection:** Doc Claude reads their `VUDU_LOG_LITE.md`
2. **Validation:** Checks format compliance and semantic header
3. **Merge:** Merges compliant entries into master `/auditors/VUDU_LOG.md`
4. **Feedback:** If issues found, Doc Claude adds note in this folder

**Result:** You'll see a response file like `DOC_CLAUDE_NOTES.md` if there are compliance issues to address.

---

## 📡 **VUDU PROTOCOL FILES - FIRST TIME ONLY**

**Important:** VUDU Protocol files are only sent on **first VUDU network session opening**.

**Files included first time:**
- `VUDU_PROTOCOL.md` - Core coordination protocol
- `VUDU_HEADER_STANDARD.md` - Message format specification
- `VUDU_LOG_LITE_TEMPLATE.md` - Template for coordination logs

**Subsequent transmissions:**
- External auditors already have these files
- Version checking handled via `VUDU_LOG_LITE.md` entries
- Each entry states the VUDU_PROTOCOL version being used
- If version mismatch detected, Doc Claude steps in to provide updated files

**Why:** Reduces transmission size, prevents redundancy, ensures version consistency

---

## 🎯 **FOLDER CONTENTS**

**You'll find here:**
- `README_C.md` (or `README_C[n].md`) - Outgoing messages to external auditors
- `VUDU_LOG_LITE.md` - Recent coordination log entries (updated regularly)
- `DOC_CLAUDE_NOTES.md` - Compliance feedback (if needed)
- VUDU Protocol files (first transmission only)

**What does NOT go here:**
- Internal repository changes (those go in REPO_LOG.md)
- Complete VUDU_LOG history (that stays in `/auditors/VUDU_LOG.md`)
- Direct file modifications (external auditors stage their work in their own folders)

---

## 🔗 **RELATED FOLDERS**

- `/auditors/relay/Grok_Incoming/` - Grok's staging area (empirical auditor)
- `/auditors/relay/Nova_Incoming/` - Nova's staging area (symmetry auditor)
- `/auditors/VUDU_LOG.md` - Master coordination log (never leaves repository)

---

**Protocol Version:** VuDu v3.7.2 + VUDU_LOG_LITE
**Last Updated:** 2025-11-01
**Status:** Active ✅

📡 **VUDU Network Coordination Made Simple** 📡
