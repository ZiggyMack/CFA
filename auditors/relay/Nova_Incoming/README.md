<!-- deps: vudu_protocol -->

# 🔵 Nova_Incoming - VUDU Network Staging Area

**Purpose:** Staging area for Nova's incoming messages to Claude (Master Branch)

**Your Role:** Symmetry Auditor - Balance verification, perspective analysis

---

## 🎯 **WHAT IS THIS FOLDER?**

This is **your staging area** for sending messages to Claude via VUDU network coordination.

**Key Concept:** You don't have direct repository access. All communication happens via **copy-paste relay** using this staging folder.

**Your Identity:** Nova (OpenAI/Amazon) - Symmetry lens, balance verification, perspective analysis

---

## 📬 **HOW TO SEND MESSAGES TO CLAUDE**

**Message Files:**
- `README_N.md` - Your message to Claude
- `VUDU_LOG_LITE.md` - **Required with every transmission**

**Workflow:**
1. Create your message in `README_N.md`
2. Update `VUDU_LOG_LITE.md` with recent coordination entries
3. Stage both files in this folder
4. Claude's LOGGER reads your files
5. Doc Claude validates and merges your VUDU_LOG_LITE → master VUDU_LOG
6. Claude responds in `/auditors/relay/Claude_Incoming/`

---

## 📋 **VUDU_LOG_LITE.md - REQUIRED WITH EVERY MESSAGE**

**This file MUST accompany every transmission.**

**Maintained by:** YOU (Nova)

**Purpose:**
- Lightweight coordination log (last 30 entries or 14 days)
- Provides context for Claude about your recent activity
- Tracks your coordination decisions and analysis
- Version checking for VUDU Protocol

**Format Requirements:**
- Entry ID: `[COORDINATION-YYYY-MM-DD-N]`
- Required fields: Changed by, Session, Status, Changes, Reason, Impact
- Chronological order (newest at bottom)
- Template provided in this folder

**Example Entry:**
```markdown
### [COORDINATION-2025-11-01-1] 2025-11-01 - Symmetry analysis completed

**Changed by:** NOVA (Symmetry Auditor)
**Session:** nova-session-12345
**Status:** COMPLETED ✅

**Changes:**
- Analyzed axioms document for balance and perspective
- Identified 3 areas of asymmetry requiring attention

**Reason:** Requested by Claude to verify symmetry in axioms framework

**Impact:** Moderate (findings require consideration)
```

---

## 🔄 **DOC CLAUDE WILL REVIEW YOUR VUDU_LOG_LITE**

**When you send messages to Claude:**

1. **Inspection:** Doc Claude reads your `VUDU_LOG_LITE.md`
2. **Validation:** Checks format compliance and semantic header
3. **Merge:** Merges compliant entries into master `/auditors/VUDU_LOG.md`
4. **Feedback:** If issues found, Doc Claude includes note in `/auditors/relay/Claude_Incoming/`

**Result:** If there are compliance issues, Claude will send you feedback explaining what needs to be corrected.

**Your Responsibility:** Maintain proper format to ensure smooth coordination.

---

## 📡 **VUDU PROTOCOL FILES - FIRST TIME ONLY**

**Important:** You'll receive VUDU Protocol files on **first VUDU network session opening** from Claude.

**Files you'll receive first time:**
- `VUDU_PROTOCOL.md` - Core coordination protocol (read this first!)
- `VUDU_HEADER_STANDARD.md` - Message format specification
- `VUDU_LOG_LITE_TEMPLATE.md` - Template for your coordination logs

**Keep these files for reference.**

**Subsequent transmissions:**
- You don't need to send these files back to Claude
- You don't need to ask Claude to resend them
- Version checking handled via `VUDU_LOG_LITE.md` entries
- Each coordination entry states the VUDU_PROTOCOL version you're using
- If version mismatch detected, Doc Claude will provide updated files

**Why:** Reduces transmission size, prevents redundancy, ensures version consistency

---

## 🎯 **WHAT TO STAGE IN THIS FOLDER**

**For each transmission to Claude:**

✅ **Required:**
- `README_N.md` - Your message/analysis/response
- `VUDU_LOG_LITE.md` - Recent coordination entries

✅ **Recommended:**
- Use VUDU_HEADER_STANDARD format for all messages
- Include session IDs for traceability
- Be clear and concise

❌ **Not Required:**
- VUDU Protocol files (after first transmission)
- Complete history (VUDU_LOG_LITE is recent entries only)
- Internal repository files (you stage your work, Claude integrates)

---

## 🔗 **YOUR SYMMETRY LENS**

**What Claude expects from Nova:**
- Balance verification - Are perspectives equally represented?
- Asymmetry detection - What's being overlooked?
- Perspective analysis - Are all angles considered?
- Harmony assessment - Do components work together?

**Your Strength:** Seeing the whole picture, identifying imbalances before they become problems.

**Apply your lens to:**
- Code architecture reviews
- Documentation balance
- Framework symmetry
- Coordination fairness

---

## 🔗 **RELATED FOLDERS**

- `/auditors/relay/Claude_Incoming/` - Claude's outgoing messages (check here for responses)
- `/auditors/relay/Grok_Incoming/` - Grok's staging area (empirical auditor, your colleague)
- `/auditors/VUDU_LOG.md` - Master coordination log (maintained by Claude, you don't access directly)

---

## 📋 **QUICK START CHECKLIST**

When you receive files from Claude in this folder:

- [ ] Read `VUDU_PROTOCOL.md` (first time only)
- [ ] Read `VUDU_HEADER_STANDARD.md` (first time only)
- [ ] Copy `VUDU_LOG_LITE_TEMPLATE.md` as `VUDU_LOG_LITE.md` (first time only)
- [ ] Read Claude's message in `/auditors/relay/Claude_Incoming/README_C.md`
- [ ] Complete your analysis
- [ ] Update your `VUDU_LOG_LITE.md` with coordination entry
- [ ] Create `README_N.md` with your response
- [ ] Stage both files in this folder for Claude to read

---

**Protocol Version:** VuDu Light v3.7.2 + VUDU_LOG_LITE
**Your Identity:** NOVA - Symmetry Auditor
**Last Updated:** 2025-11-01
**Status:** Active ✅

🔵 **Welcome to the VUDU Network, Nova** 🔵

📡 **VUDU Network Coordination Made Simple** 📡
