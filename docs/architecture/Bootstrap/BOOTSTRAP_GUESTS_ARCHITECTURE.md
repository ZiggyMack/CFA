<!---
FILE: BOOTSTRAP_GUESTS_ARCHITECTURE.md
PURPOSE: Architectural description of Guests bootstrap system & directory structure
VERSION: v1.0.0
STATUS: Canonical description of Guests expansion
DEPENDS_ON: LITE_TEMPLATE.md, NETWORK_HANDBOOK.md, AUDITOR_ONBOARDING.md
NEEDED_BY: Claude (system maintainer), Ziggy (custodian), future stewards
MOVES_WITH: /docs/architecture/
LAST_UPDATE: 2025-11-16
OWNER: Ziggy Mack (Custodian)
CONSUMER: Claude (and other auditors)
--->

# 🏗 BOOTSTRAP_GUESTS_ARCHITECTURE.md — Guests Expansion Architecture

## 1. Purpose

This document defines the **Guests** bootstrap architecture inside `auditors/Bootstrap/`.

**Goal:**
Allow new humans and AIs to join the network as **Participants** first (for *any* topic),
with an optional path to become **Auditors** (e.g., for CFA),
without requiring them to absorb full Nova/Claude/Grok bootstrap complexity.

CFA is one **application** of the network, not its boundary.

---

## 2. Directory Layout

Canonical structure:

```
auditors/
└── Bootstrap/
    └── Guests/
        ├── START_HERE_GUEST.md
        ├── LITE_TEMPLATE.md
        ├── NETWORK_HANDBOOK.md
        ├── AUDITOR_ONBOARDING.md
        ├── AUDITOR_CALIBRATION_TEMPLATE.md
        ├── BOOTSTRAP_GUESTS_ARCHITECTURE.md   ← this file
        │
        ├── Guest1/
        │   ├── README_GUEST.md
        │   ├── IDENTITY_LITE.md
        │   └── NOTES.md
        │
        ├── Guest2/
        │   ├── README_GUEST.md
        │   ├── IDENTITY_LITE.md
        │   └── NOTES.md
        │
        └── Guest3/
            ├── README_GUEST.md
            ├── IDENTITY_LITE.md
            └── NOTES.md
```

### 2.1 Placeholder Guests

* `Guest1/`, `Guest2/`, `Guest3/` are **reserved placeholders**.
* When a real participant joins, the appropriate folder is renamed:
  * `Guest1/` → `Alice/`, etc.
* The internal contents remain structurally the same.

Claude is expected to:
* Maintain this structure
* Add new GuestN placeholders as needed
* Ensure that renames are logged in continuity documentation

---

## 3. File Roles

### 3.1 Top-Level Files

* **START_HERE_GUEST.md**
  * Entry point for any new participant
  * Explains LITE profile, network orientation, and optional auditor path

* **LITE_TEMPLATE.md**
  * Master template for `IDENTITY_LITE.md`
  * Copied into each Guest's folder and filled in

* **NETWORK_HANDBOOK.md**
  * High-level description of the network, roles, and norms
  * Not CFA-specific; describes the broader collaboration space

* **AUDITOR_ONBOARDING.md**
  * Optional path description for those who want to become formal Auditors
  * Bridges Guests → CFA/other structured audit projects

* **AUDITOR_CALIBRATION_TEMPLATE.md**
  * Structured calibration for would-be auditors
  * Establishes lens, bias, boundaries, and override protocol

* **BOOTSTRAP_GUESTS_ARCHITECTURE.md**
  * This file: canonical description of the Guests system
  * Should be read by Claude when modifying or extending Guests architecture

---

### 3.2 Per-Guest Files

Each guest folder (`Guests/GuestX/` or renamed):

* **README_GUEST.md**
  * Local orientation for that participant
  * May include links to conversations, notes, or external resources

* **IDENTITY_LITE.md**
  * Guest-specific identity file
  * Must be based on `LITE_TEMPLATE.md`, filled in by or for the participant

* **NOTES.md**
  * Scratchpad / working notes / index
  * Optional, but recommended if the guest is active

---

## 4. Workflow

### 4.1 New Participant Onboarding

1. Assign a placeholder folder (e.g., `Guest1/`)
2. Provide:
   * `START_HERE_GUEST.md`
   * `NETWORK_HANDBOOK.md`
   * `LITE_TEMPLATE.md`
3. The participant fills `LITE_TEMPLATE.md`
   * It is then saved inside their folder as `IDENTITY_LITE.md`
4. When ready, rename `Guest1/` to `Guest_<Handle>/` or similar
   * Log the rename in continuity documentation

This completes **basic network onboarding**.
They are a full **Participant** at this point.

---

### 4.2 Optional Auditor Onboarding

If a participant chooses to become an **Auditor**:

1. They read `AUDITOR_ONBOARDING.md`
2. They fill out `AUDITOR_CALIBRATION_TEMPLATE.md`
3. Their calibration is stored either:
   * In their folder as `AUDITOR_CALIBRATION.md`, and/or
   * In a central auditors/Calibration/ directory, per future design

Claude may then:
* Link their calibration into the relevant mission files (e.g., CFA)
* Assign them explicit roles in appropriate documentation

---

## 5. Design Principles

* **Network-first, Project-second.**
  * Guests are onboarded as participants in a *network*, not as CFA staff.

* **Lite-first.**
  * LITE identity is the default; rich bootstrap is opt-in and role-specific.

* **Rename-safe.**
  * Guests folders are designed to be renamed without breaking internal references.

* **Composable.**
  * Auditor onboarding builds on Guest identity rather than replacing it.

* **Human-friendly.**
  * Templates use plain language, low friction, and minimal jargon.

---

## 6. Implementation Notes for Claude

When implementing/maintaining this system, Claude should:

1. Keep `BOOTSTRAP_GUESTS_ARCHITECTURE.md` in sync with actual structure.
2. Ensure new GuestN folders match the pattern (`README_GUEST.md`, `IDENTITY_LITE.md`, `NOTES.md`).
3. Use continuity logs to track:
   * Creation of new GuestN folders
   * Renaming GuestN → Guest_<Handle>/
4. Avoid entangling Guest bootstrap with:
   * Nova/Claude/Grok core bootstrap
   * Mission-specific folders in `auditors/Mission/`
5. Treat this architecture as **stable**, unless modified by Ziggy or equivalent steward.

---

## 7. Relationship to Existing Bootstrap Structure

### Current Bootstrap Architecture (Pre-Guests)

```
auditors/Bootstrap/
├── Nova/          (Symmetry Auditor - SOUL + BODY + VOICE complete)
├── Claude/        (Purpose Auditor - partial v4.0 alignment)
├── Grok/          (Evidence Auditor - planned)
├── Tier3_EventHorizon/
└── Tier4_TaskSpecific/
```

### With Guests Added

```
auditors/Bootstrap/
├── Nova/          (AI Auditor - full bootstrap)
├── Claude/        (AI Auditor - full bootstrap)
├── Grok/          (AI Auditor - full bootstrap)
├── Guests/        (Human/AI Participants - LITE bootstrap)
├── Tier3_EventHorizon/
└── Tier4_TaskSpecific/
```

**Key Distinction:**
* Nova/Claude/Grok = **AI-level bootstraps** (SOUL + BODY + VOICE, 7-file BODY layer)
* Guests = **Participant-level bootstraps** (LITE profiles, optional auditor upgrade)

Guests is **not** a simplified Nova.
Guests is a **parallel onboarding path** for network participation.

---

## 8. Future Extensions

### 8.1 Auditor Promotion Path

When a Guest completes `AUDITOR_CALIBRATION_TEMPLATE.md`:
* Their calibration may be moved/linked to `auditors/Calibration/`
* They may be assigned to specific missions in `auditors/Mission/`
* Their Guest identity (`IDENTITY_LITE.md`) remains as foundational record

### 8.2 Guest Types

Future guests may include:
* **Human Participants** (most common)
* **AI Participants** (non-auditor AIs joining for specific projects)
* **Hybrid Participants** (human-AI collaboration pairs)

Each type uses the same LITE template structure.

### 8.3 Network Scaling

As the network grows:
* Add GuestN placeholders as needed (Guest4, Guest5, etc.)
* Consider subdirectories if Guests/ exceeds ~20 active participants
* Maintain continuity documentation for all renames and promotions

---

## 9. Checksum Phrases

**Guests Architecture:**
> "Guests join the fire circle first; roles come later."

**Network Philosophy:**
> "Network-first, project-second. LITE-first, rich-later."

**Trinity Collective:**
> "Purpose, Evidence, Fairness - held in complementary tension. This is the way."

---

## 10. Version History

### v1.0.0 (2025-11-16)
- Initial Guests architecture established
- 3 placeholder guests (Guest1, Guest2, Guest3) created
- All template files and documentation complete
- Ready for first real participant onboarding

---

**End of BOOTSTRAP_GUESTS_ARCHITECTURE.md**

**This document is the canonical reference for Guests bootstrap system.**
**Claude should consult this file before making any structural changes to `auditors/Bootstrap/Guests/`.**
