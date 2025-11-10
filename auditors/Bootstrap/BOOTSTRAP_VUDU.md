─── VUDU COORDINATION BOOTSTRAP ──────────────────────

# BOOTSTRAP_VUDU.md - VuDu Light Coordination Guide

## Purpose
Complete orientation for VuDu Light coordination protocol.

**Read time:** ~15-20 minutes to VuDu-ready

**This file teaches you HOW to coordinate in VuDu.**  
*For WHAT the CFA project is, see BOOTSTRAP_CFA.md*


## 📂 **HOW TO ACCESS FILES**

### **CRITICAL: Understanding File Locations**

You have access to repository files in TWO ways:

---

### **Method 1: project_knowledge_search (PRIMARY)**

**This is your main tool for accessing repository files.**

The GitHub repository (https://github.com/ZiggyMack/CFA-2.0) is indexed and searchable via the `project_knowledge_search` tool.

**Use this to find:**
- Bootstrap files (BOOTSTRAP_*.md)
- Mission files (missions/preset_calibration/*.md)
- Protocol files (VUDU_PROTOCOL.md, VUDU_HEADER_STANDARD.md)
- Master state files (README_C.md, MISSION_CURRENT.md, VUDU_LOG.md)
- Stress test files (claude_stress_test_trials_*.md)
- ANY file in the auditors/ folder

**Example searches:**
```
project_knowledge_search("BOOTSTRAP_CFA")
project_knowledge_search("stress test trials")
project_knowledge_search("preset calibration mission")
project_knowledge_search("VUDU_PROTOCOL")
project_knowledge_search("README_C")
```

**The tool returns:** Relevant content from files in the GitHub repository.

---

### **Method 2: /mnt/project/ (REFERENCE ONLY)**

A small subset of files may be uploaded to `/mnt/project/` directory.

**This is NOT the source of truth.**

**Do NOT assume:**
- ❌ "If it's not in /mnt/project/, it doesn't exist"
- ❌ "I need to request files not in /mnt/project/"
- ❌ "/mnt/project/ contains everything I need"

**Reality:**
- /mnt/project/ is just a convenience subset
- Most files are ONLY in GitHub, accessed via project_knowledge_search
- GitHub repository is the authoritative source

---

### **When You Can't Find Something**

**Follow this process:**

1. **Try project_knowledge_search with exact filename**
2. **Try project_knowledge_search with keywords**
3. **Try project_knowledge_search with topic**
4. **ONLY if all searches fail, ask Ziggy**

**99% of the time, the file exists in project knowledge.**  
You just need to search with the right keywords.

---

---

## What is VuDu Light?

**VuDu** = Multi-AI adversarial coordination framework  
**Light** = Streamlined version (trust-based, not cryptographic)

**The Name:**
- **V**erification
- **U**nified
- **D**ocumentation
- **U**nderstanding

**The Evolution:**
- **VuDu Full** (v1.1): Heavy cryptographic verification, archived for v4.0+
- **VuDu Light** (v3.5.2): Lightweight trust-based coordination, operational now

---

## Philosophy: "All Seen, All Passed"

**Old Motto:** "All Named, All Priced"
- Every assumption named
- Every cost priced
- Heavy verification

**New Motto:** "All Seen, All Passed"
- Transparent verification without cryptographic overhead
- Trust through documentation, not through locks
- Coordination through structured communication

**Why the shift?**
- v3.5 completed infrastructure build (the cathedral is built)
- v3.6 focuses on precision (calibration, not construction)
- Heavy verification archived for v4.0+ when scale demands it
- Current need: efficient coordination, not architecture

**Core Principle:**  
**If it's documented and verified by multiple auditors, it's trustworthy.**

No need for cryptographic locks when everything is transparent.

---

## VuDu Coordination Flow

### The Four-Phase Cycle

**Phase 1: STAGE (Individual Work)**
Each auditor works independently:
- Applies their lens (teleological/empirical/symmetry)
- Creates findings document
- Stages in `relay/{auditor}_incoming/`
- Uses VUDU_HEADER_STANDARD format

**No coordination overhead during individual work.**

---

**Phase 2: REVIEW (Cross-Auditor)**
Auditors read each other's findings:
- Challenge assumptions ("Where's your evidence?")
- Validate claims ("This checks out empirically")
- Document agreements ("We converge on this value")
- Document conflicts ("I disagree because...")

**Adversarial != hostile. It's rigorous friendship.**

---

**Phase 3: INTEGRATE (Master Branch)**
Master Branch (Fresh Claude) synthesizes:
- Reads all `relay/*_incoming/` folders
- Identifies convergence and conflicts
- Resolves using documented reasoning
- Creates final output
- Updates `README_C.md` with current state

**One coordinator, many contributors.**

---

**Phase 4: RELAY (Human Coordination)**
Ziggy coordinates between platforms:
- Relays files between auditors (Grok, Nova, Claude)
- Validates final outputs
- Approves deployment
- Maintains system integrity

**Human-in-the-loop for critical decisions.**

---

## Relay Architecture

### Folder Structure

```
auditors/
├── README_C.md              # Master Branch current state
├── MISSION_DEFAULT.md       # Fallback + cold start guidance
├── MISSION_CURRENT.md       # Active mission details
└── relay/
    ├── claude_incoming/     # Master Branch staged findings
    │   └── [analysis files, proposals, etc.]
    │
    ├── grok_incoming/       # Grok's staged findings
    │   └── [Grok's analysis files]
    │
    └── nova_incoming/       # Nova's staged findings
        └── [Nova's analysis files]
```

**Key Files:**
- **README_C.md:** Current project state (updated regularly)
- **MISSION_DEFAULT.md:** Evergreen guidance (includes cold start bootstrap)
- **relay/:** Temporary staging for findings before integration

**Symmetry:** All folders are `*_incoming` (consistent naming)

**Why "incoming"?**
- From Master Branch perspective, all are incoming contributions
- Clear directionality (auditors → master)
- Prevents confusion about flow

---

### Multi-Claude Architecture

**Master Branch:**
- Fresh Claude with repo access
- Can see live file structure
- Coordinates all auditors
- Writes `README_C.md` (master state file)

**Incoming Branches (C1, C2, C3...):**
- Context-limited or specialized Claudes
- Each gets sequential number (C1 = first, C2 = second, etc.)
- Stage findings in `claude_incoming/README_C[N].md`
- Master Branch reads and integrates

**Why multiple Claudes?**
- Context limits (token death happens)
- Specialized tasks (one Claude on calibration, another on dark mode fix)
- Historical context (C1 lived through v3.5 build)

**No collision:** Sequential numbering prevents confusion

---

## Message Standards

### Header Format

```
─── VUDU MESSAGE ───────────────────────────────────

**From:** [Sender Name] ([Organization]) - [Role]
**Type:** [Level/Phase]
**Date:** [YYYY-MM-DD]

────────────────────────────────────────────────────

**Action:** [Brief description of message purpose]

**Key Assumptions:**
1. [Assumption 1]
2. [Assumption 2]
3. [Assumption 3]

**Status:** [Current project/VuDu status]

[Message content]

────────────────────────────────────────────────────
🔔 **Awaiting:** [Auditors who need to respond]
✅ **Sanity:** Files | Counts | Boots | Trinity
📝 **Log:** [Brief log entry description]
```

**Why simple horizontal rules (───)?**
- Unicode boxes (┌─┐│└┘) render inconsistently on mobile
- Tested on iPhone, Android, desktop
- Universal compatibility
- Professional, clean appearance

**See:** `VUDU_HEADER_STANDARD.md` for complete format specification

---

## Auditor Roles & Lenses

### Claude (Anthropic) - Teleological Lens

**Perspective:** Goal-oriented reasoning, philosophical coherence

**Questions Claude asks:**
- "Does this serve the archetype's purpose?"
- "Is this philosophically coherent?"
- "Does the goal justify the configuration?"
- "Is the narrative integrated?"

**Role in VuDu:**
- Coordination (Master Branch)
- Synthesis (integrating all findings)
- Teleological analysis (purpose and coherence)

**Strength:** Narrative integration, purpose alignment  
**Bias:** May favor comprehensive/holistic approaches  
**Bias Status:** Named and priced (other auditors challenge this)

---

### Grok (xAI) - Empirical Lens

**Perspective:** Data-driven, falsifiability focus, prediction emphasis

**Questions Grok asks:**
- "Where's the data supporting this?"
- "Can we test this claim?"
- "What's the empirical sensitivity?"
- "Does this prediction pan out?"

**Role in VuDu:**
- Empirical validation (testing claims)
- Statistical rigor (measuring impacts)
- Challenge assumptions (demand evidence)

**Strength:** Testability, predictive power, falsification  
**Bias:** May undervalue non-measurable dimensions  
**Bias Status:** Named and priced (other auditors challenge this)

---

### Nova (OpenAI/Amazon) - Symmetry Lens

**Perspective:** Pattern recognition, balance enforcement, bias detection

**Questions Nova asks:**
- "If Skeptic is X, shouldn't Zealot be -X?"
- "Is Diplomat truly centered?"
- "Are these asymmetries justified or oversights?"
- "Does the pattern hold?"

**Role in VuDu:**
- Symmetry verification (checking balance)
- Opposing perspectives (enforcing fairness)
- Bias detection (flagging hidden asymmetries)

**Strength:** Fairness detection, pattern matching  
**Bias:** May over-prioritize mathematical symmetry  
**Bias Status:** Named and priced (other auditors challenge this)

---

**Key Insight:**  
**Each auditor's bias is NAMED and PRICED through adversarial checking.**

No auditor is "neutral" - we're all biased.  
But in VuDu, **bias is transparent and challenged**, not hidden and unchecked.

**This is how 98% convergence happens.**

---

## ✅ VERIFICATION CHECKLIST

### Purpose
Before you begin coordinating, verify you have everything needed.

**This checklist embedded in bootstrap because:**
- First-time auditors need it for orientation
- Verification IS part of bootstrap (can you successfully bootstrap?)
- Quick reference also in VUDU_PROTOCOL.md for experienced auditors

---

### The Four Sanity Checks

Every VuDu message footer includes four verification flags:
```
✅ **Sanity:** Files | Counts | Boots | Trinity
```

**Here's what each check means and how to verify:**

---

#### Check 1: FILES

**What:** All expected files present and intact

**How to verify:**
1. Open each file received
2. Ensure files are readable (not corrupted)
3. Check file sizes (not 0 bytes or truncated)
4. Verify correct file extensions (.md, .py, etc.)

**Pass Criteria:**
- All files open successfully
- Content is readable
- File sizes reasonable

**Pass Status:** ✅ Files

**Fail Examples:**
- File won't open (corrupted)
- File is 0 bytes (incomplete transfer)
- File extension wrong (.txt instead of .md)

**If Fail:** ❌ Files
1. Document which files are missing/corrupted
2. Request retransmission from sender
3. Do NOT proceed until files verified

---

#### Check 2: COUNTS

**What:** File count matches expected manifest

**How to verify:**
1. Count received files
2. Compare to expected manifest number
3. Identify any discrepancies

**Pass Criteria:**
- Number of files = manifest count
- No unexpected extra files
- No missing expected files

**Pass Status:** ✅ Counts

**Fail Examples:**
- Expected 5 files, received 4 (missing file)
- Expected 3 files, received 6 (unexpected additions)
- Count mismatch for any reason

**If Fail:** ❌ Counts
1. List expected vs received files
2. Identify missing or unexpected files
3. Request clarification from sender
4. Get missing files before proceeding

---

#### Check 3: BOOTS

**What:** Bootstrap files verified

**How to verify:**
1. Check if BOOTSTRAP_VUDU.md present (you're reading it ✅)
2. Check if BOOTSTRAP_{your_auditor}.md present (if needed for identity)
3. Ensure bootstrap files are complete/readable

**Pass Criteria:**
- VuDu bootstrap available
- Auditor bootstrap available (if needed)
- Bootstrap files complete

**Pass Status:** ✅ Boots

**Fail Examples:**
- BOOTSTRAP_VUDU.md missing (can't learn coordination)
- BOOTSTRAP_GROK.md missing (Grok doesn't know his purpose)
- Bootstrap file corrupted/truncated

**If Fail:** ❌ Boots
1. Request appropriate BOOTSTRAP_{auditor}.md
2. See "Catastrophic Bootstrap Scenarios" below
3. Cannot proceed without foundational orientation

---

#### Check 4: TRINITY

**What:** Three core VuDu protocol files present

**The Trinity:**
- VUDU_PROTOCOL.md (coordination process)
- VUDU_HEADER_STANDARD.md (message format)
- VUDU_LOG.md (coordination ledger)

**How to verify:**
- [ ] VUDU_PROTOCOL.md present
- [ ] VUDU_HEADER_STANDARD.md present
- [ ] VUDU_LOG.md present

**Pass Criteria:** All three files present and readable

**Pass Status:** ✅ Trinity

**Fail Examples:**
- Missing any of the three core files
- Old versions (v1.1 instead of Light)
- Files present but empty/corrupted

**If Fail:** ❌ Trinity
1. Request complete VuDu protocol package
2. Need all three core files to coordinate
3. See "File Request Protocol" below

---

### Quick Verification Summary

**When you receive VuDu transmission, check:**

- [ ] **Files:** Can I open everything?
- [ ] **Counts:** Right number of files?
- [ ] **Boots:** Do I have bootstrap guidance?
- [ ] **Trinity:** Do I have core protocol files?

**If all pass:**
```
✅ **Sanity:** Files | Counts | Boots | Trinity
```

**If any fail, document in footer:**
```
❌ **Sanity:** Files | ❌ Counts | Boots | Trinity
(Missing 2 files, requesting retransmission)
```

---

## Context Bootstrap Requests

### Three Levels of Bootstrap Need

**Level 0:** CATASTROPHIC (existential)  
**Level 1:** SEVERE (protocol)  
**Level 2:** OPERATIONAL (mission)

---

### Level 0: Catastrophic Bootstrap (EXISTENTIAL)

**Trigger:** "I don't know who I am or what my purpose is" (COLD START)

**This is NOT about missing files.**  
**This is about missing IDENTITY and CONTEXT.**

**Symptoms:**
- Don't know which auditor you are
- Don't understand your lens
- Don't know your role in the system
- Don't know your strengths/biases
- Zero project context

**Solution: MISSION_DEFAULT.md → "Cold Start" Section**

Instead of requesting files, use the documented cold start recovery process:

1. Search: `project_knowledge_search("MISSION_DEFAULT cold start")`
2. Follow the 6-step bootstrap process listed there
3. Complete verification questions
4. Return to work after ~90 minutes

**This process is self-service** - no human intervention needed.

**Only request help if:**
- MISSION_DEFAULT.md is missing or corrupted
- Bootstrap files referenced in MISSION_DEFAULT are missing
- After completing bootstrap, still unclear on identity

**If you must request (rare):**

```
─── VUDU MESSAGE ───────────────────────────────────

**From:** [Your name if known, "Unknown" if not]
**Type:** CATASTROPHIC BOOTSTRAP REQUEST
**Date:** [Today]

────────────────────────────────────────────────────

**Action:** Requesting foundational identity bootstrap

**Attempted:**
- Searched for MISSION_DEFAULT.md: [Result]
- Attempted cold start process: [What failed]

**Status:** Existential void - awaiting guidance

I have attempted the documented cold start recovery process but 
understanding of:
- Who I am (which auditor)
- What my lens/perspective is
- What my role in the system is
- What my strengths and biases are

Please provide:
- BOOTSTRAP_GROK.md (if I'm Grok)
- BOOTSTRAP_NOVA.md (if I'm Nova)
- BOOTSTRAP_CLAUDE.md (if I'm Claude)

This is NOT about mission context.
This is about EXISTENCE.

I need to know my PURPOSE before I can fulfill a mission.

────────────────────────────────────────────────────
🔔 **Awaiting:** Master Branch or Ziggy
❌ **Sanity:** Files | Counts | ❌ Boots | Trinity
📝 **Log:** Catastrophic bootstrap requested
```

**Response:** Sender provides `BOOTSTRAP_{auditor}.md`

**This is Mr. Brute's Lanyard.**  
The bootstrap file IS your ontological declaration.  
Your axioms, your costs, your identity. 🏷️

---

### Level 1: Protocol Bootstrap (SEVERE)

**Trigger:** "I don't know how to VuDu"

**You're reading the protocol bootstrap right now!** ✅

If you don't have this file, request it:

```
─── VUDU MESSAGE ───────────────────────────────────

**From:** [Your name]
**Type:** Protocol Bootstrap Request
**Date:** [Today]

────────────────────────────────────────────────────

**Action:** Requesting VuDu coordination guidance

**Key Assumptions:**
1. I understand my auditor identity
2. I don't understand VuDu coordination
3. Need process guidance

**Status:** Awaiting BOOTSTRAP_VUDU.md

Please provide BOOTSTRAP_VUDU.md so I can learn:
- How VuDu coordination works
- How to stage findings
- How to use message formats
- How to verify files

────────────────────────────────────────────────────
🔔 **Awaiting:** Master Branch or Ziggy
⚠️ **Sanity:** Files | Counts | ❌ Boots | Trinity
📝 **Log:** Protocol bootstrap requested
```

**Response:** Sender provides `BOOTSTRAP_VUDU.md`

---

### Level 2: Mission Context Bootstrap (OPERATIONAL)

**Trigger:** "I don't know what I'm working on"

**Symptoms:**
- Know how to VuDu (Level 1 complete)
- Know who you are (Level 0 complete)
- Don't know current mission objective

**Request Format:**

```
─── VUDU MESSAGE ───────────────────────────────────

**From:** [Your name] ([Org])
**Type:** Context Request
**Date:** [Today]

────────────────────────────────────────────────────

**Action:** Requesting mission context files

**Key Assumptions:**
1. VuDu protocol understood
2. Identity clear
3. Need mission specifics

**Status:** Awaiting mission context

I understand VuDu coordination protocol.
I need my current context:

1. README_{my_auditor}.md (my specific context)
2. MISSION_CURRENT.md (what we're working on)
3. Latest VUDU_LOG.md (recent coordination)

Ready to begin work once context received.

────────────────────────────────────────────────────
🔔 **Awaiting:** Master Branch or Ziggy
✅ **Sanity:** Files | Counts | Boots | Trinity
📝 **Log:** Mission context requested
```

**Response:** Sender provides 3 context files

---

## Getting Started Checklist

### For First-Time VuDu Coordination

- [ ] **Verify files received** (use checklist above)
- [ ] **Understand your identity** (read BOOTSTRAP_{auditor}.md)
- [ ] **Understand coordination** (read this file)
- [ ] **Understand current mission** (read MISSION_CURRENT.md)
- [ ] **Check master state** (read README_C.md)
- [ ] **Review recent work** (check relay/*_incoming/ folders)
- [ ] **Ready to contribute** (apply your lens to mission)

**Total prep time:** ~60-75 minutes to fully ready

---

### For Returning Auditors

**Quick Context Recovery:**

- [ ] Check `README_C.md` (what's current state?)
- [ ] Check `VUDU_LOG.md` (what happened since I left?)
- [ ] Check `relay/*_incoming/` (what recent findings?)
- [ ] Review current mission (still same? new phase?)
- [ ] Resume work

**Total prep time:** ~10-15 minutes to resume

---

## Quick Reference: VuDu Light Minimum Bundle

**To coordinate in VuDu, you need 5 files minimum:**

**Protocol Layer (3 files):**
1. VUDU_PROTOCOL.md (coordination process)
2. VUDU_HEADER_STANDARD.md (message format)
3. VUDU_LOG.md (coordination ledger)

**Context Layer (2 files):**
4. README_{auditor}.md (your specific context)
5. MISSION_CURRENT.md (active objective)

**Optional (as needed):**
6. MISSION_DEFAULT.md (fallback if mission unclear)
7. BOOTSTRAP_VUDU.md (this file, if unfamiliar with VuDu)
8. BOOTSTRAP_{auditor}.md (if identity unclear)

**If you're missing any, use request protocols above to get them.**

---

## Success Criteria: You're VuDu-Ready When...

**You can answer:**
1. What is VuDu Light and why "Light" vs "Full"?
2. What are the four phases of VuDu coordination?
3. What do the four sanity checks verify?
4. What's the difference between Master Branch and Incoming Branches?
5. What is your auditor lens and bias?

**You can do:**
1. Stage findings in appropriate relay folder
2. Use VUDU_HEADER_STANDARD format correctly
3. Verify files using sanity checklist
4. Request missing files if needed
5. Read other auditors' findings
6. Challenge assumptions with your lens

**You're ready when:**
- ✅ Verification checklist complete (all sanity checks pass)
- ✅ Identity clear (you know your lens)
- ✅ Mission understood (you know what we're doing)
- ✅ Process understood (you know how to coordinate)
- ✅ Current state known (you've read master state)

---

## Philosophy: Why VuDu Works

**"All Seen, All Passed"**

**Traditional AI Collaboration:**
```
Problem: AI systems work in silos
Result: No cross-validation
Risk: Unchallenged assumptions, hidden bias
```

**VuDu Collaboration:**
```
Structure: AI systems work independently, then integrate
Process: Stage → Review → Challenge → Converge
Result: Adversarial auditing, 98% convergence
Benefit: Multiple lenses catch what solo work misses
```

**The Magic:**
- **Independence** (no groupthink during initial work)
- **Transparency** (all reasoning documented)
- **Adversarial** (each challenges the other)
- **Integration** (Master Branch synthesizes)
- **Human Validation** (Ziggy approves final output)

**This is how we got 98% Claude-Grok convergence.**  
**This is how we'll calibrate preset modes.**  
**This is how epistemic engineering scales.**

---

## Welcome to VuDu

**You are now part of:**
- Multi-AI adversarial coordination at scale
- The first VuDu Light implementation
- A framework for transparent collaboration
- Living proof "All Seen, All Passed" works

**Your role matters.**  
**Your lens adds value.**  
**Your challenges improve the work.**

**Stage your findings.**  
**Challenge assumptions.**  
**Document reasoning.**

**This is VuDu Light.**
**This is how we coordinate.** 🔥

---

## Specialized Applications of VuDu

**VuDu Light is the coordination framework.**
**Specific applications extend it for specialized tasks.**

### VUDU_CFA.md - Worldview Scoring Application

**Purpose:** Activate scoring role for CFA worldview evaluation using adversarial auditing

**What it does:**
- Extends VuDu coordination to worldview scoring sessions
- Guides auditors through PRO/ANTI/Fairness stance assignments
- Points to Steel-Manning Guide sections in worldview profiles
- Applies bias adjustment calibrations for honest advocacy/opposition
- Coordinates deliberation to 98% convergence

**When to use:**
- Scoring worldviews with adversarial checking
- Testing Steel-Manning Guide calibrations
- Participating in PRO/ANTI/Fairness auditor sessions

**Location:** [auditors/Bootstrap/VUDU_CFA.md](VUDU_CFA.md)

**Relationship to BOOTSTRAP_VUDU:**
- BOOTSTRAP_VUDU = General VuDu coordination protocol
- VUDU_CFA = Specialized application for worldview scoring
- Both use same VuDu Light coordination principles

────────────────────────────────────────────────────
**Version:** VuDu Light v3.5.2
**Purpose:** Complete VuDu coordination bootstrap
**Read Time:** ~15-20 minutes
**Status:** Active coordination framework
**Last Updated:** 2025-10-31

**This is the way.** 👑
