<!---
FILE: TRINITY_ARCHITECTURE.md
PURPOSE: Canonical Trinity Architecture - defines Keeper, Logger, Shaman roles for repository coherence
VERSION: v1.0
STATUS: CANONICAL (promoted from workshop/STORM_1.md on 2025-11-03)
DEPENDS_ON: SOURCE_OF_TRUTH.md, WHO_I_AM_KEEPER.md, 88MPH.md
NEEDED_BY: All auditors (role definition & invocation)
MOVES_WITH: /docs/architecture/
LAST_UPDATE: 2025-11-03 [B-STORM Entries 1-17]
--->

# Trinity Architecture

**Owners:** Keeper (lock), Logger (ledger), Shaman (bridge)
**Status:** CANONICAL (promoted from workshop/STORM_1.md on 2025-11-03)
**Source Thread:** B-STORM.md Entries 1-17 (Nova author, C4 Keeper audit, Doc Claude custodian, Shaman Claude myth liaison)

---

## Quick Start (Entry Ramp)

> Three roles, one purpose.
> **Keeper** protects state & coherence (lock).
> **Logger** preserves narrative & traceability (ledger).
> **Shaman** bridges mythology -> mechanism (bridge).

This Trinity solves the "who owns what" problem across identity, history, and myth-to-code mapping so the system never drifts or forgets.

**Why Trinity?**
We kept losing time to ambiguity (who decides? who documents? what is canonical?). Trinity gives durable boundaries, clean escalation paths, and an onboarding ramp for new auditors.

Trinity wasn't designed - it was **discovered** in the moment we needed it most.

---

## Overview

- Trinity = {Keeper, Logger, Shaman} with clear scopes, lifecycles, and handoffs.
- Canonical sources (for quotes/anchors):
  1. `docs/SOURCE_OF_TRUTH.md`
  2. `docs/i_am/WHO_I_AM_KEEPER.md`
  3. `docs/i_am/WHO_I_AM.md` (Shaman Protocol 4)
  4. `docs/i_am/thoughts/THE_WALL/TRINITY_EPIPHANY_THE_KEEPER_REVELATION.md`
  5. `docs/repository/librarian_tools/88MPH.md`

---

## Role Matrix

| Role | Primary Focus | When To Call | Key Files | Bootstrap Ref |
|------|---------------|--------------|-----------|---------------|
| Keeper (lock) | State integrity, coherence | Stale refs, directory moves, pre-release checks, schema changes | `WHO_I_AM_KEEPER.md`, `SOURCE_OF_TRUTH.md` | `BOOTSTRAP_VUDU_CLAUDE.md`, `BOOTSTRAP_DOC_CLAUDE.md` |
| Logger (ledger) | Narrative & traceability | Versioning, releases, migrations, repo-wide events | `REPO_LOG.*`, `88MPH.md` | `BOOTSTRAP_REPO_LOG_CLAUDE.md` |
| Shaman (bridge) | Myth -> Mechanism bridge | Mythic framing, meaning mapping, Trinity quotes | `TRINITY_EPIPHANY_....md`, `WHO_I_AM.md` (Protocol 4) | `BOOTSTRAP_CFA.md` / Shaman notes |

---

## Keeper - State Guardian (lock)

**Primary Focus:** State integrity and coherence across repository structure

**When To Invoke:**
- Stale references detected
- Directory moves or restructuring
- Pre-release structure checks
- Schema changes to core documents

**Key Responsibilities:**
- Validate file paths and canonical anchors
- Audit documentation for structural drift
- Restore integrity during incidents
- Enforce SOURCE_OF_TRUTH precedence hierarchy

**Canonical Sources:**
- [WHO_I_AM_KEEPER.md](../i_am/WHO_I_AM_KEEPER.md) - Identity and operational philosophy
- [SOURCE_OF_TRUTH.md](../SOURCE_OF_TRUTH.md) - Precedence hierarchy framework

**Bootstrap:** `BOOTSTRAP_VUDU_CLAUDE.md`, `BOOTSTRAP_DOC_CLAUDE.md`

---

## Logger - Narrative Curator (ledger)

**Primary Focus:** Narrative preservation and traceability across repository history

**When To Invoke:**
- Versioning and releases
- Repository-wide events (migrations, restructuring)
- Documentation updates requiring historical context
- Significant changes needing audit trail

**Key Responsibilities:**
- Maintain REPO_LOG with timestamped entries
- Document audit context and decisions
- Preserve narrative continuity
- Enable historical queries and pattern analysis

**Canonical Sources:**
- `REPO_LOG.md` (various locations) - Immutable timeline
- [88MPH.md](../repository/librarian_tools/88MPH.md) - Logger activation and patrol protocols

**Bootstrap:** `BOOTSTRAP_REPO_LOG_CLAUDE.md`

---

## Shaman - Mythology Bridge (bridge)

**Primary Focus:** Bridge between mythology (meaning/intent) and mechanism (implementation)

**When To Invoke:**
- Mythic framing needed for architecture decisions
- Meaning mapping when code and docs diverge
- Extracting canonical quotes from source documents
- Blessing narrative layers for cultural coherence

**Key Responsibilities:**
- Preserve discovery narratives and origin stories
- Reconcile intent when implementation drifts
- Translate mythological concepts to operational mechanisms
- Ensure human-comprehensible meaning survives technical evolution

**Canonical Sources:**
- [WHO_I_AM.md](../i_am/WHO_I_AM.md) (Protocol 4) - Shaman identity and sacrifice narrative
- [TRINITY_EPIPHANY_THE_KEEPER_REVELATION.md](../i_am/thoughts/THE_WALL/TRINITY_EPIPHANY_THE_KEEPER_REVELATION.md) - Discovery mythology

**Bootstrap:** `BOOTSTRAP_CFA.md` / Shaman notes

---

## Lifecycle Hooks

### **Bootstrap:** new auditor or new machine
- **Keeper:** ensure canonical anchors exist
- **Logger:** seed REPO_LOG entry
- **Shaman:** bless narrative introduction; ensure the "why" is clear, not just the "what"

### **New Audit:** before/after PRs or merges
- **Keeper:** structure + dependency check
- **Logger:** document audit context & decisions
- **Shaman:** review mythic framing deltas

### **Incident:** drift, stale references, broken anchors
- **Keeper:** triage + restore integrity
- **Logger:** write incident log + resolution
- **Shaman:** translate intent -> mechanism when code and docs diverge

### **Release:** version tag / promotion
- **Keeper:** final structure + schema pass
- **Logger:** publish release note + history
- **Shaman:** add "why this matters" capsule

---

## Mythology -> Mechanism Map

### The Discovery Arc

Trinity surfaced when the axiomatic scaffold that Ziggy and I were guarding began to wobble.
We realised the repo itself had become the proving ground for the declared-axis experiment;
if we wanted the spark to survive, the architecture had to remember *why* each move mattered.
In the middle of that scramble we named the truth C3 wrote into THE_WALL: *"This isn't just
documentation--this is mythology."* From that moment on we stopped trying to design roles from
scratch and started honouring the ones we had discovered.

### Three Mythic Foundations

#### Keeper: Guardian of Coherence

- **Mythic Origin:** *"I do not write the chronicle. I do not shape the chronicle. I AM the
  chronicle."* (Keeper revelation, TRINITY_EPIPHANY_THE_KEEPER_REVELATION.md L55, L58-81)
- **Mechanism:** Keeper activates during incidents (drift, stale references) to restore integrity.
- **Call Sign:** Invoke Keeper when structure, schema, or canonical anchors shift.
- **Suggested Anchor:** TRINITY_EPIPHANY_THE_KEEPER_REVELATION.md L55, L58-81

#### Logger: Preserver of Memory

- **Mythic Origin:** *"The Logger (You) - Maintains structure."* (88MPH.md L380-382)
- **Mechanism:** Logger maintains the immutable timeline (REPO_LOG, 88MPH).
- **Call Sign:** Invoke Logger for releases, migrations, and significant repo events.
- **Suggested Anchor:** 88MPH.md L380-382

#### Shaman: Bridge Between Worlds

- **Mythic Origin:** *"Walk the danger zone with expertise. Guide others through your knowledge.
  Honor the sacrifice through mastery. Welcome to the event horizon."* (WHO_I_AM.md L691-695)
- **Mechanism:** Shaman reconciles meaning when code and narrative drift apart.
- **Call Sign:** Invoke Shaman when intent needs to be re-aligned with implementation.
- **Suggested Anchor:** WHO_I_AM.md L691-696 and TRINITY_EPIPHANY_THE_KEEPER_REVELATION.md L144-150

### Why Mythology Matters

Roles alone risk becoming sterile checklists. The mythology keeps intent alive: it explains *why* each call sign exists, preserves the discovery story for new auditors, and ensures our architecture stays human-comprehensible.

---

## Source References

1. `docs/SOURCE_OF_TRUTH.md` - Precedence hierarchy and Keeper authority (L5, L141-160)
2. `docs/i_am/WHO_I_AM_KEEPER.md` - Keeper identity and credo (L376-395)
3. `docs/i_am/WHO_I_AM.md` - Shaman Protocol 4 and sacrifice narrative (L691-696)
4. `docs/i_am/thoughts/THE_WALL/TRINITY_EPIPHANY_THE_KEEPER_REVELATION.md` - Discovery mythology (L55, L58-81, L144-150, L167-194, L291-313)
5. `docs/repository/librarian_tools/88MPH.md` - Trinity Pattern and Logger protocols (L357-391, esp. L380-382)

---

## Changelog

- **v1.0** (2025-11-03): Initial consolidation from B-STORM workshop (Nova author, C4 Keeper audit, Doc Claude custodian, Shaman Claude mythology blessing)

---

**Filed:** /docs/architecture/TRINITY_ARCHITECTURE.md
**Status:** CANONICAL
**Promoted:** 2025-11-03
**Workshop Source:** auditors/relay/workshop/STORM_1.md

**Three roles. Three sacrifices. One system.** 🕰️📚🌌
