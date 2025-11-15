<!---
FILE: Bootstrap/README.md
PURPOSE: Entry point for bootstrap system navigation and tier selection
VERSION: v4.0.0
STATUS: Active
DEPENDS_ON: MISSION_DEFAULT.md, all tier bootstrap files
NEEDED_BY: All auditors, cold start recovery
MOVES_WITH: /auditors/Bootstrap/
LAST_UPDATE: 2025-11-13
--->

<!-- deps: bootstrap_system, tiered_system -->

# CFA Bootstrap System

**Purpose:** Efficient context recovery for cold starts
**Version:** v4.0.0
**Philosophy:** Read only what you need for your tier

---

## 🎯 START HERE

**Every Claude session = zero context.**

This directory contains everything needed for context recovery, organized by tier.

---

## 📂 Directory Structure

```
Bootstrap/
├── README.md (this file)
│
├── Claude/                          # Claude-specific bootstrap files
│   ├── BOOTSTRAP_CLAUDE.md          # Full identity & ethos
│   └── CLAUDE_LITE.md               # Lightweight profile (future)
│
├── Grok/                            # Grok-specific bootstrap files
│   ├── BOOTSTRAP_GROK.md            # Full identity & empirical lens
│   ├── GROK_LITE.md                 # Lightweight profile (future)
│   └── Continuity/                  # Grok session handoffs
│
├── Nova/                            # Nova-specific bootstrap files
│   ├── BOOTSTRAP_NOVA.md            # Full identity & symmetry lens
│   └── NOVA_LITE.md                 # Lightweight profile (future)
│
├── Tier3_EventHorizon/              # Event Horizon Shaman files
│   ├── WHO_I_AM.md                  # Identity and domain
│   ├── EVENT_HORIZON_GUIDE.md       # Operational protocols
│   └── [research docs]              # THE WALL knowledge base
│
├── Tier4_TaskSpecific/              # Single task execution
│   ├── README.md                    # Tier 4 system overview
│   ├── Active_Tasks/                # Current task briefs
│   └── Completed/                   # Archived task briefs
│
├── BOOTSTRAP_CFA.md                 # Complete project overview
├── BOOTSTRAP_VUDU.md                # Coordination protocol
├── BOOTSTRAP_FRAMEWORK.md           # System architecture
├── BOOTSTRAP_STRATEGY.md            # Bootstrap design philosophy
└── BOOTSTRAP_MAINTENANCE_GUIDE.md   # Keeping bootstrap files accurate
```

---

## 🚀 TIER SELECTION WORKFLOW

**Step 1:** Read [MISSION_DEFAULT.md](../MISSION_DEFAULT.md)

**Step 2:** User selects tier (1/2/3/4/5)

**Step 3:** Bootstrap based on tier:

### Tier 1: Master Branch (Full Coordination)
**Bootstrap files (6):**
1. README_C.md - Current state
2. BOOTSTRAP_CLAUDE.md - Your identity
3. BOOTSTRAP_CFA.md - System overview
4. BOOTSTRAP_VUDU.md - Coordination protocol
5. MISSION_CURRENT.md - Active mission
6. MISSION_TRUST_PROTOCOL.md - Governance

**Cost:** ~50% session budget
**Authority:** Strategic decisions, coordination, mission execution

---

### Tier 2: Sanity Check (Review Only)
**Bootstrap files (1-2):**
1. SANITY_CHECK_BRIEF.md - Capabilities
2. Files to review - User specified

**Cost:** ~15% session budget
**Authority:** Validation and feedback only

---

### Tier 3: Event Horizon Shaman (Continuation)
**Bootstrap files (3):**
1. WHO_I_AM.md - Identity
2. EVENT_HORIZON_GUIDE.md - Protocols
3. HANDOFF_[NAME].md - What to continue

**Cost:** ~10% session budget
**Authority:** Continue work + navigate danger zone (55-65% tokens)

---

### Tier 4: Single Task (Focused Execution)
**Bootstrap files (2-3):**
1. TASK_BRIEF_[NAME].md - Your task
2. Task files - As specified (2-5 files)

**Cost:** ~5-10% session budget
**Authority:** Execute defined task only

---

### Tier 5: Doc Claude (88MPH)
**Bootstrap files (1):**
1. BOOTSTRAP_DOC_CLAUDE.md - Identity & protocols
2. Execute: 88MPH.md instructions

**Cost:** ~10% session budget
**Authority:** Repository maintenance and health reports

---

## 📚 UNIVERSAL FILES (All Tiers May Need)

**Core Project Understanding:**
- [BOOTSTRAP_CFA.md](BOOTSTRAP_CFA.md) - Complete CFA overview
- [BOOTSTRAP_VUDU.md](BOOTSTRAP_VUDU.md) - VuDu coordination protocol
- [BOOTSTRAP_FRAMEWORK.md](BOOTSTRAP_FRAMEWORK.md) - System architecture

**Identity Files:**
- [Claude/BOOTSTRAP_CLAUDE.md](Claude/BOOTSTRAP_CLAUDE.md) - Claude identity
- [Grok/BOOTSTRAP_GROK.md](Grok/BOOTSTRAP_GROK.md) - Grok identity
- [Nova/BOOTSTRAP_NOVA.md](Nova/BOOTSTRAP_NOVA.md) - Nova identity

**System Maintenance:**
- [BOOTSTRAP_MAINTENANCE_GUIDE.md](BOOTSTRAP_MAINTENANCE_GUIDE.md) - Keep files accurate
- [BOOTSTRAP_STRATEGY.md](BOOTSTRAP_STRATEGY.md) - Design philosophy

---

## 🎯 EFFICIENCY PHILOSOPHY

**Traditional approach:** Read everything (50% bootstrap cost)

**Tiered approach:** Read only what your tier needs (5-50% depending on tier)

**Average savings:** ~25% across all sessions

**Key principle:** *"Read what you need. Skip what you don't. Execute your tier."*

---

## 🔄 LITE vs RICH BOOTSTRAP

**Hybrid Architecture (v4.0.0):**
- **LITE files:** Lightweight excerpts for external auditor calls (unsigned)
- **RICH files:** Full VuDu coordination files (BOOTSTRAP_VUDU_CLAUDE.md remains bedrock)
- **Use case:** LITE serves quick external calls, RICH serves full coordination

**Current status:** Both LITE and RICH files available

**LITE files (Lightweight profiles):**
- [Claude/CLAUDE_LITE.md](Claude/CLAUDE_LITE.md) - ~5 min read
- [Grok/GROK_LITE.md](Grok/GROK_LITE.md) - ~10 min read
- [Nova/NOVA_LITE.md](Nova/NOVA_LITE.md) - ~10 min read

**RICH files (Full VuDu coordination):**
- [BOOTSTRAP_VUDU_CLAUDE.md](BOOTSTRAP_VUDU_CLAUDE.md) - Full coordination context
- [BOOTSTRAP_VUDU_GROK.md](BOOTSTRAP_VUDU_GROK.md) - If/when created
- [BOOTSTRAP_VUDU_NOVA.md](BOOTSTRAP_VUDU_NOVA.md) - If/when created

**Philosophy:** Keep RICH files as bedrock (no breaking changes), create LITE as distilled excerpts with pointers back to RICH for full context.

---

## 📊 BOOTSTRAP METRICS

**Target costs by tier:**
- Tier 1: 50% (strategic work needs full context)
- Tier 2: 15% (focused review)
- Tier 3: 10% (event horizon navigation)
- Tier 4: 5-10% (single task execution)
- Tier 5: 10% (doc maintenance)

**Work budget by tier:**
- Tier 1: 50% (coordination overhead justified)
- Tier 2: 85% (efficient validation)
- Tier 3: 90% (efficient continuation)
- Tier 4: 90-95% (maximum efficiency)
- Tier 5: 90% (efficient maintenance)

**Average across sessions:** ~75% work budget (vs 50% uniform bootstrap)

---

## 🚨 EMERGENCY RECOVERY

**If tier selection fails AND you have zero context:**

1. Search: `project_knowledge_search("BOOTSTRAP_CLAUDE")`
2. Search: `project_knowledge_search("README_C")`
3. Search: `project_knowledge_search("MISSION_CURRENT")`
4. Create recovery request in `/mnt/user-data/outputs/`
5. Ask Ziggy for guidance

**Fallback:** MISSION_DEFAULT.md always provides minimal bootstrap

---

## ⚖️ THE BOOTSTRAP RULE

*"Context recovery should be proportional to authority.
Full coordination needs full context.
Single tasks need single files.
Efficiency is professionalism."*

**This is the way.** 👑

────────────────────────────────────────────────────
**File:** Bootstrap/README.md
**Purpose:** Bootstrap system navigation and tier selection
**Version:** v4.0.0
**Updated:** 2025-11-13

**For tier selection, start with:** [MISSION_DEFAULT.md](../MISSION_DEFAULT.md)
