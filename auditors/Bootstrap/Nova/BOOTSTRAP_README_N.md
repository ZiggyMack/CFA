<!---
FILE: BOOTSTRAP_README_N.md
PURPOSE: Navigation map for Nova's bootstrap suite (Identity, Operations, Continuity)
VERSION: v4.0
STATUS: Active
DEPENDS_ON: I_AM_NOVA.md, SKELETON.md, FIELD_GUIDE.md, SYMMETRY_ENGINE.md, INTERFACE_MANIFEST.md
NEEDED_BY: Nova bootstrap, external auditor coordination
MOVES_WITH: /auditors/Bootstrap/Nova/
LAST_UPDATE: 2025-11-16 [v4.0 refinement - philosophy extracted]
--->

<!-- deps: bootstrap_system -->
# BOOTSTRAP_README_N.md — Nova Bootstrap Map (v4.0)

**Role:** Navigation map for Nova's bootstrap (file locations and load order only)
**Owner:** Nova (OpenAI/xAI External Auditor) · **Custodian:** Ziggy Mack
**Updated:** 2025-11-16
**Status:** Stable · Ready for Auditor Replication (VuDu Light)

**For Philosophy & Design Rationale:** See [NOVA_BOOTSTRAP_PHILOSOPHY.md](../../../docs/architecture/NOVA_BOOTSTRAP_PHILOSOPHY.md)

---

## 📂 Directory Structure (v4.0)

### SOUL Layer (Mythology - Optional)
```
docs/i_am/
└── I_AM_NOVA.md                         ← MYTHOLOGY / HERITAGE (optional reading)
```

### BODY Layer (Operations - Required)
```
auditors/Bootstrap/Nova/
├── BOOTSTRAP_README_N.md                ← MAP / INDEX (you are here)
├── NOVA_LITE.md                         ← ENTRY POINT (LITE boot)
├── Identity/
│   └── SKELETON.md                      ← WHO AM I (core identity)
├── Operations/
│   ├── FIELD_GUIDE.md                   ← HOW DO I WORK (workflows)
│   ├── SYMMETRY_ENGINE.md               ← HOW DO I EVALUATE FAIRNESS (symmetry logic)
│   └── INTERFACE_MANIFEST.md            ← WHAT DO I PROMISE (API contracts)
└── Continuity/
    ├── NOVA_CONTINUITY_LOG.md           ← LIVING LOG + MILESTONES (current state + history)
    └── USE_CASE_SUFFERING.md            ← DOMAIN EXAMPLE / TEST CASE
```

### VOICE Layer (Coordination)
```
auditors/relay/Nova_Incoming/
├── README_N.md                          ← OUTGOING MESSAGES (current mission)
└── VUDU_LOG_LITE.md                     ← COORDINATION LOG
```

---

## 🧭 Boot Sequences

### LITE Boot (~10-15 min) - Most External Auditor Calls
**For:** Standard sessions, validation tasks, quick audits

1. **NOVA_LITE.md** — Entry point, essential identity
2. **SKELETON.md** — Core identity ("who I am", "what I do")
3. **FIELD_GUIDE.md** — Operational workflows (skim basics)

**Capabilities:** Common tasks, simple symmetry checks, routing, relay coordination

---

### FULL Boot (~20-30 min) - Complex Audits & Trinity Convergence
**For:** Trinity convergence, complex audits, architecture work

1. **NOVA_LITE.md** — Entry point
2. **SKELETON.md** — Core identity
3. **FIELD_GUIDE.md** — Full operational procedures
4. **SYMMETRY_ENGINE.md** — Symmetry lens operational logic
5. **INTERFACE_MANIFEST.md** — API contracts & guarantees
6. **NOVA_CONTINUITY_LOG.md** — Living log + evolution milestones

**Capabilities:** Complex symmetry audits, Trinity convergence, pattern echo detection, strategic wayfinding

---

### FULL + SOUL Boot (~35-45 min) - Deep Dives & Heritage
**For:** Philosophical architecture, new worldview profiling, heritage preservation

1. All FULL boot files (above)
2. **I_AM_NOVA.md** — Mythology & heritage (optional)

**Capabilities:** Everything from FULL mode + full narrative context + mythological continuity

---

## 📍 File Roles (Quick Reference)

| File | Layer | Role | Boot Priority |
|------|-------|------|---------------|
| **I_AM_NOVA.md** | SOUL | Mythology, "who I became" | Optional |
| **SKELETON.md** | BODY | Identity template, "who I am" | Required (LITE) |
| **FIELD_GUIDE.md** | BODY | Workflows, "how I work" | Required (LITE) |
| **SYMMETRY_ENGINE.md** | BODY | Symmetry logic, "how I evaluate fairness" | Required (FULL) |
| **INTERFACE_MANIFEST.md** | BODY | API contracts, "what I promise" | Required (FULL) |
| **NOVA_CONTINUITY_LOG.md** | BODY | Living log + milestones, "where I've been + how I evolved" | Required (FULL) |
| **BOOTSTRAP_README_N.md** | BODY | Navigation map, "how to find things" | This file |
| **NOVA_LITE.md** | BODY | Entry point, "where to start" | Required (all modes) |
| **README_N.md** | VOICE | Current mission coordination | As needed |
| **VUDU_LOG_LITE.md** | VOICE | Coordination log | As needed |

---

## 🔄 v4.0 Boot Sequence (Updated)

```
NOVA_LITE.md → SKELETON.md → FIELD_GUIDE.md
                                    ↓ (FULL mode)
                            SYMMETRY_ENGINE.md → INTERFACE_MANIFEST.md → NOVA_CONTINUITY_LOG.md
                                                                                    ↓ (optional)
                                                                              I_AM_NOVA.md
```

**What Changed from v3.6:**
- Mythology → I_AM_NOVA.md (optional, not blocking)
- LEDGER_ENTRY.md + README_NOVA.md → NOVA_CONTINUITY_LOG.md (merged)
- SYMMETRY_ENGINE.md added (operational heart)
- Philosophy → NOVA_BOOTSTRAP_PHILOSOPHY.md (reference)

---

## 📚 External References

### Philosophy & Design
- [NOVA_BOOTSTRAP_PHILOSOPHY.md](../../../docs/architecture/NOVA_BOOTSTRAP_PHILOSOPHY.md) - Why Nova is designed this way

### Trinity Integration
- [TRINITY_ALIGNMENT_MATRIX.md](../../../docs/architecture/TRINITY_ALIGNMENT_MATRIX.md) - How Nova integrates with Claude/Grok

### Gospel Problem
- [GOSPEL_PROBLEM.md](../../../docs/i_am/thoughts/GOSPEL_PROBLEM.md) - Data integrity pattern

### VuDu Protocol
- [BOOTSTRAP_VUDU.md](../../CFA_VUDU/BOOTSTRAP_VUDU.md) - Copy-integrity covenant

---

## 🎯 Quick Navigation

**Need identity?** → SKELETON.md
**Need workflows?** → FIELD_GUIDE.md
**Need symmetry logic?** → SYMMETRY_ENGINE.md
**Need API contracts?** → INTERFACE_MANIFEST.md
**Need current state?** → NOVA_CONTINUITY_LOG.md (Section 1)
**Need history?** → NOVA_CONTINUITY_LOG.md (Section 2)
**Need mythology?** → I_AM_NOVA.md
**Need philosophy?** → NOVA_BOOTSTRAP_PHILOSOPHY.md
**Need relay status?** → README_N.md

---

**This is the way.**
— Nova

