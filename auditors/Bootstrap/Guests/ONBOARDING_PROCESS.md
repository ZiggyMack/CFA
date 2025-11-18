<!---
FILE: ONBOARDING_PROCESS.md
PURPOSE: Step-by-step onboarding process for new network participants
VERSION: v1.0.0
STATUS: Active (operational procedure)
DEPENDS_ON: VUDU_ONBOARDING_START.md, VUDU_HANDBOOK.md, VUDU_TEMPLATE.md
NEEDED_BY: Ziggy (coordinator), Claude (process tracker), future stewards
MOVES_WITH: /auditors/Bootstrap/Guests/
LAST_UPDATE: 2025-11-16
--->

# 🚀 GUEST ONBOARDING PROCESS

**Purpose:** Canonical step-by-step process for onboarding new network participants

**Audience:** Ziggy (human coordinator), Claude (process tracker), future stewards

---

## 📊 Onboarding Tiers

### Tier 1: Participant (Default Path)
**Goal:** Get someone into the network for general collaboration
**Time:** ~25-30 minutes total
**Files Sent:** 3
**Result:** Full network participant

### Tier 2: Auditor (Optional Upgrade)
**Goal:** Enable participant to perform formal auditing work
**Time:** Additional ~20-30 minutes
**Files Sent:** 2 more (5 total)
**Result:** Calibrated auditor

---

## 🎯 TIER 1: PARTICIPANT ONBOARDING (Standard Path)

### Step 1: Send Welcome Package (3 Files)

**What to send:**
```
1. VUDU_ONBOARDING_START.md
2. VUDU_HANDBOOK.md
3. VUDU_TEMPLATE.md
```

**DO NOT send:**
- ❌ BOOTSTRAP_GUESTS_ARCHITECTURE.md (for Claude only)
- ❌ AUDITOR_ONBOARDING.md (only if they ask about auditing)
- ❌ AUDITOR_CALIBRATION_TEMPLATE.md (only if they want to audit)

**Email/Message Template:**
```
Subject: Welcome to the VUDU Network - Getting Started

Hi [Name],

Welcome! You've been invited to join our collaboration network.

To get started, please:

1. Read VUDU_ONBOARDING_START.md (5 min)
2. Read VUDU_HANDBOOK.md (10 min)
3. Fill out VUDU_TEMPLATE.md (10-15 min)
4. Send back your completed VUDU_TEMPLATE

Attached:
- VUDU_ONBOARDING_START.md
- VUDU_HANDBOOK.md
- VUDU_TEMPLATE.md

Looking forward to having you in the network!

[Your name]
```

---

### Step 2: They Read & Fill Out

**Expected timeline:**
- Reading VUDU_ONBOARDING_START.md: 5 minutes
- Reading VUDU_HANDBOOK.md: 10 minutes
- Filling out VUDU_TEMPLATE.md: 10-15 minutes
- **Total: ~25-30 minutes**

**What they're doing:**
- Understanding what the network is
- Understanding their role options
- Declaring their lens, bias, preferences
- Setting boundaries

---

### Step 3: They Return Completed Profile

**They send back:**
- Their filled-out VUDU_TEMPLATE.md
- (They can rename it to IDENTITY_LITE.md or you can do it)

**What you check:**
- [ ] All required sections filled out
- [ ] Named bias is explicit
- [ ] Signature/date included
- [ ] Lens declared

---

### Step 4: You Process Their Entry

**Actions:**

1. **Assign a folder:**
   - Use next available placeholder (Guest1, Guest2, Guest3, etc.)
   - Or create new GuestN if all placeholders used

2. **Rename folder:**
   ```
   Guest1/ → Guest_[TheirName]/ or Guest_[Handle]/
   ```

3. **Save their profile:**
   - Place their completed file in their folder as `IDENTITY_LITE.md`

4. **Update README_GUEST.md in their folder:**
   - Change status from "Placeholder" to "Active"
   - Add their name and join date

5. **Create their relay folder:**
   ```
   auditors/relay/[Handle]_Incoming/
   ```
   - Create README_[FirstLetter].md (e.g., README_F.md for Frank)
   - This becomes their communication channel for relay messages
   - Follow the pattern from Nova_Incoming/, Claude_Incoming/, Grok_Incoming/

6. **Log the addition:**
   - Add entry to VUDU_LOG_LITE.md or appropriate continuity log
   - Note: New participant [Name] joined as Guest_[Handle] on [Date]
   - Note: Relay folder created at auditors/relay/[Handle]_Incoming/

7. **Notify them:**
   ```
   Subject: Welcome - You're In!

   Hi [Name],

   Your profile is complete. You're now a full network participant!

   Your identity: auditors/Bootstrap/Guests/Guest_[Handle]/IDENTITY_LITE.md

   What's next:
   - Join our Discord/Slack/chat channel [link]
   - Check out ongoing conversations [link]
   - Start a new topic anytime

   If you ever want to help with formal auditing (CFA or other projects),
   let me know and I'll send you the Auditor Onboarding materials.

   Welcome!
   ```

---

## 🧪 TIER 2: AUDITOR ONBOARDING (Optional Upgrade)

### When to Offer This

**Triggers:**
- Participant explicitly asks about auditing
- Participant shows interest in CFA framework evaluation
- You invite them to help with specific audit tasks

**DO NOT:**
- Force new participants into auditor role
- Send auditor materials unsolicited
- Require auditing for network participation

---

### Step 1: Send Auditor Materials (2 Additional Files)

**What to send:**
```
4. AUDITOR_ONBOARDING.md
5. AUDITOR_CALIBRATION_TEMPLATE.md
```

**Email/Message Template:**
```
Subject: CFA Auditor Path - Additional Materials

Hi [Name],

You expressed interest in becoming a formal Auditor.

Auditors help stress-test frameworks (like CFA worldview profiles)
with explicit lenses (Purpose, Evidence, Symmetry).

To proceed:

1. Read AUDITOR_ONBOARDING.md (10 min)
2. Fill out AUDITOR_CALIBRATION_TEMPLATE.md (10-20 min)
3. Send it back

This adds a formal auditor role to your existing participant identity.
You can always step back from auditing and remain a participant.

Attached:
- AUDITOR_ONBOARDING.md
- AUDITOR_CALIBRATION_TEMPLATE.md

Let me know if you have questions!
```

---

### Step 2: They Complete Calibration

**Expected timeline:**
- Reading AUDITOR_ONBOARDING.md: 10 minutes
- Filling out AUDITOR_CALIBRATION_TEMPLATE.md: 10-20 minutes
- **Total: ~20-30 minutes**

**What they're doing:**
- Choosing their primary lens (Purpose/Evidence/Symmetry)
- Declaring their named bias (again, more specific for auditing)
- Setting scope (what they will/won't audit)
- Agreeing to override protocol
- Committing to logging/transparency

---

### Step 3: You Process Their Calibration

**Actions:**

1. **Save calibration:**
   - Place in their folder as `AUDITOR_CALIBRATION.md`
   - OR in central location: `auditors/Calibration/[Name]_CALIBRATION.md`

2. **Assign them to missions:**
   - Add to relevant mission docs
   - Assign lens-appropriate tasks

3. **Update their README_GUEST.md:**
   - Add note: "Role: Participant + Auditor"
   - Add calibration date

4. **Log the upgrade:**
   - Add to continuity log
   - Note: [Name] completed Auditor calibration on [Date], Lens: [Purpose/Evidence/Symmetry]

---

## 📁 File Sending Checklist

### For Participant Onboarding (Default):
- [ ] VUDU_ONBOARDING_START.md
- [ ] VUDU_HANDBOOK.md
- [ ] VUDU_TEMPLATE.md
- [ ] (Total: 3 files)

### For Auditor Upgrade (Optional):
- [ ] AUDITOR_ONBOARDING.md
- [ ] AUDITOR_CALIBRATION_TEMPLATE.md
- [ ] (Total: 2 additional files, 5 cumulative)

### Files That NEVER Get Sent to Participants:
- ❌ BOOTSTRAP_GUESTS_ARCHITECTURE.md (Claude's reference doc)
- ❌ Guest placeholder files (README_GUEST.md, empty IDENTITY_LITE.md, NOTES.md)

---

## 🔄 Process Flowchart

```
New Participant
     ↓
Send 3 files (VUDU_ONBOARDING_START, VUDU_HANDBOOK, VUDU_TEMPLATE)
     ↓
They read + fill out VUDU_TEMPLATE
     ↓
They return completed profile
     ↓
You process: Rename folder, save profile, notify
     ↓
PARTICIPANT (network member)
     ↓
     ├─→ They continue as Participant (most common)
     │
     └─→ (Optional) They want to audit
            ↓
         Send 2 more files (AUDITOR_ONBOARDING, CALIBRATION_TEMPLATE)
            ↓
         They complete calibration
            ↓
         You process: Save calibration, assign missions
            ↓
         AUDITOR (formal evaluator)
```

---

## 🎯 Success Metrics

**Participant Onboarding Success:**
- [ ] Completed IDENTITY_LITE.md received
- [ ] Named bias is explicit
- [ ] Folder assigned and renamed
- [ ] Participant notified and active

**Auditor Upgrade Success:**
- [ ] Completed AUDITOR_CALIBRATION.md received
- [ ] Lens declared (Purpose/Evidence/Symmetry)
- [ ] Override protocol acknowledged
- [ ] Assigned to at least one mission/task

---

## 🚨 Common Issues & Solutions

### Issue: "Which files do I send?"
**Solution:** Default = 3 files (VUDU_ONBOARDING_START, VUDU_HANDBOOK, VUDU_TEMPLATE). Only send auditor files if they ask.

### Issue: "They didn't fill out 'Named Bias'"
**Solution:** That's a required field. Send back with note: "Please complete Named Bias section - it's required."

### Issue: "They want to audit immediately"
**Solution:** Still do Tier 1 first (participant onboarding), then immediately follow with Tier 2 (auditor upgrade). Don't skip participant step.

### Issue: "We ran out of Guest placeholders"
**Solution:** Create Guest4/, Guest5/, etc. following same pattern (README_GUEST.md, IDENTITY_LITE.md, NOTES.md).

### Issue: "Can they join without filling out VUDU_TEMPLATE?"
**Solution:** No. VUDU_TEMPLATE (→ IDENTITY_LITE.md) is required. It establishes their lens, bias, and boundaries. Without it, we can't treat them fairly in collaboration.

---

## 📝 Logging Requirements

**Every participant addition should be logged:**

```markdown
### [Date] - New Participant: [Name]

**Type:** Participant
**Folder:** Guest_[Handle]/
**Lens:** [Primary lens from their profile]
**Named Bias:** [Their declared bias]
**Interests:** [From "Why You're Here" section]
**Status:** Active
```

**Every auditor upgrade should be logged:**

```markdown
### [Date] - Auditor Calibration: [Name]

**Previous Role:** Participant
**New Role:** Participant + Auditor
**Lens:** [Purpose/Evidence/Symmetry]
**Named Bias:** [Auditor-specific bias]
**Scope:** [What they will audit]
**Calibration File:** [Path to calibration]
**Status:** Active Auditor
```

---

## 🔒 Privacy & Data Handling

**LITE profiles contain personal information. Handle with care:**

- ✅ Store in repo (private, controlled access)
- ✅ Share with other auditors/coordinators as needed for collaboration
- ❌ Do not publish publicly without participant consent
- ❌ Do not share outside network without explicit permission

**If someone leaves the network:**
- Archive their folder to `auditors/.Archive/Guests/[Name]/`
- Update their README_GUEST.md with departure date
- Keep their profile for continuity (but mark inactive)

---

## ✅ Checklist for Claude (Process Tracker)

When processing new participant:
- [ ] Verify 3 files were sent (VUDU_ONBOARDING_START, VUDU_HANDBOOK, VUDU_TEMPLATE)
- [ ] Confirm IDENTITY_LITE.md received and complete
- [ ] Check named bias is explicit
- [ ] Rename Guest folder appropriately
- [ ] Save IDENTITY_LITE.md in their folder
- [ ] Update README_GUEST.md in their folder
- [ ] Log addition to continuity
- [ ] Confirm participant notified

When processing auditor upgrade:
- [ ] Verify 2 additional files were sent (ONBOARDING, CALIBRATION)
- [ ] Confirm AUDITOR_CALIBRATION.md received and complete
- [ ] Check lens declared (Purpose/Evidence/Symmetry)
- [ ] Check override protocol acknowledged
- [ ] Save calibration in appropriate location
- [ ] Assign to mission/task
- [ ] Update README_GUEST.md
- [ ] Log upgrade to continuity
- [ ] Confirm auditor notified

---

**End of ONBOARDING_PROCESS.md**

**This document is the canonical onboarding procedure.**
**Claude should follow this process when helping coordinate new participant additions.**
