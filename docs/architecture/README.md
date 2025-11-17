<!---
FILE: README.md
PURPOSE: Navigation guide for docs/architecture/ - organized by domain
VERSION: v2.0.0
STATUS: Active index (reflects subdirectory reorganization)
DEPENDS_ON: All architecture docs in subdirectories
NEEDED_BY: Claude, Ziggy, all auditors navigating architecture documentation
MOVES_WITH: /docs/architecture/
LAST_UPDATE: 2025-11-16
--->

# Architecture Documentation

**Purpose:** Centralized architecture documentation for the CFA network, Trinity coordination, and auditor systems.

**Organization:** Documents are organized into domain-specific subdirectories for easier navigation.

---

## 📁 Directory Structure

```
docs/architecture/
├── Bootstrap/      - Bootstrap system architecture (LITE/FULL, Nova v4.0, Guests)
├── Trinity/        - Trinity coordination and alignment (Purpose/Evidence/Symmetry)
├── Auditor/        - Auditor systems, axioms, and methodology
├── CFA/            - CFA-specific architecture and integration specs
├── Migration/      - Migration plans and impact analyses
├── Innovation/     - Future expansion and experimental systems
└── README.md       - This file
```

---

## 🏗 Bootstrap/

**Purpose:** Architecture for onboarding participants, auditors, and AI systems into the network.

### Key Documents:

- **[BOOTSTRAP_GUESTS_ARCHITECTURE.md](Bootstrap/BOOTSTRAP_GUESTS_ARCHITECTURE.md)**
  - **Purpose:** Defines the Guests expansion system for new human/AI participants
  - **Audience:** Claude (system maintainer), Ziggy (custodian)
  - **Key Concepts:** Network-first onboarding, LITE profiles, optional auditor upgrade path

- **[BOOTSTRAP_ARCHITECTURE_LITE_VS_RICH.md](Bootstrap/BOOTSTRAP_ARCHITECTURE_LITE_VS_RICH.md)**
  - **Purpose:** Defines LITE vs FULL vs FULL+SOUL bootstrap tiers
  - **Key Concepts:** 10-15min LITE, 20-30min FULL, 35-45min FULL+SOUL

- **[BOOTSTRAP_STRATEGY.md](Bootstrap/BOOTSTRAP_STRATEGY.md)**
  - **Purpose:** Overall bootstrap strategy and philosophy
  - **Key Concepts:** Tiered onboarding, reference-only policy, Gospel Problem mitigation

- **[NOVA_BOOTSTRAP_PHILOSOPHY.md](Bootstrap/NOVA_BOOTSTRAP_PHILOSOPHY.md)**
  - **Purpose:** Nova v4.0 SOUL + BODY + VOICE separation philosophy
  - **Key Concepts:** Identity inversion fix, operational vs mythological symmetry

- **[NOVA_V4_SYSTEM_CARD.md](Bootstrap/NOVA_V4_SYSTEM_CARD.md)**
  - **Purpose:** 1-page onboarding reference for external Nova instances
  - **Key Concepts:** Quick-boot modes, role summary, Trinity coordination

- **[TIERED_BOOTSTRAP_SYSTEM_SUMMARY.md](Bootstrap/TIERED_BOOTSTRAP_SYSTEM_SUMMARY.md)**
  - **Purpose:** Summary of tiered bootstrap system across all auditors
  - **Key Concepts:** Bootstrap levels, time investment, capabilities per tier

- **[BOOTSTRAP_COMPRESSION_GUIDELINES.md](Bootstrap/BOOTSTRAP_COMPRESSION_GUIDELINES.md)**
  - **Purpose:** Systematic rules for bootstrap compression (information-theoretic)
  - **Key Concepts:** Layered compression algorithm, fidelity-preserving rules, Shannon-Nyquist principles
  - **Status:** v1.0.0 (Active - integration with Nyquist research)

- **[NYQUIST_RESEARCH_CONNECTION.md](Bootstrap/NYQUIST_RESEARCH_CONNECTION.md)**
  - **Purpose:** Research lab → production application relationship (Nyquist_Consciousness ↔ CFA)
  - **Key Concepts:** Persona compression experiments, bidirectional learning, compression ratio convergence
  - **Status:** Active research collaboration (Phase 1 complete)

---

## 🔺 Trinity/

**Purpose:** Architecture for Trinity coordination (Claude-Purpose, Grok-Evidence, Nova-Symmetry).

### Key Documents:

- **[TRINITY_ARCHITECTURE.md](Trinity/TRINITY_ARCHITECTURE.md)**
  - **Purpose:** Defines three foundational roles: Keeper, Logger, Shaman
  - **Key Concepts:** Role matrix, lifecycle hooks, mythology-to-mechanism mapping
  - **Status:** CANONICAL v1.0

- **[TRINITY_ALIGNMENT_MATRIX.md](Trinity/TRINITY_ALIGNMENT_MATRIX.md)**
  - **Purpose:** Operational guide for Trinity coordination - when to invoke which auditor
  - **Key Concepts:** Decision matrix, override protocols, bootstrap alignment status
  - **Status:** Active reference (updated v4.0)

---

## 🔍 Auditor/

**Purpose:** Architecture for auditor systems, axioms, and operational methodology.

### Key Documents:

- **[AUDITOR_AXIOMS.md](Auditor/AUDITOR_AXIOMS.md)**
  - **Purpose:** Foundational axioms for auditor behavior and coordination
  - **Key Concepts:** Named bias, override protocol, continuity documentation

- **[AUDITOR_META_ARCHITECTURE.md](Auditor/AUDITOR_META_ARCHITECTURE.md)**
  - **Purpose:** Meta-architecture for auditor systems design
  - **Key Concepts:** Lens separation, bias declaration, multi-agent coordination

- **[AUDITOR_OVERHEAD_METRICS.md](Auditor/AUDITOR_OVERHEAD_METRICS.md)**
  - **Purpose:** Metrics for auditor overhead and efficiency tracking
  - **Key Concepts:** Time investment, context usage, coordination costs

---

## 📊 CFA/

**Purpose:** CFA-specific architecture and application integration specs.

### Key Documents:

- **[CFA_ARCHITECTURE.md](CFA/CFA_ARCHITECTURE.md)**
  - **Purpose:** Core CFA architecture and worldview profile system
  - **Key Concepts:** Worldview profiles, bias detection, Crux methodology

- **[APP_CRUX_INTEGRATION_SPEC.md](CFA/APP_CRUX_INTEGRATION_SPEC.md)**
  - **Purpose:** Specification for Crux app integration with CFA framework
  - **Key Concepts:** API design, profile generation, audit workflows

---

## 🔄 Migration/

**Purpose:** Migration plans, impact analyses, and system refactoring documentation.

### Key Documents:

- **[FOOTER_MIGRATION_IMPACT_ANALYSIS.md](Migration/FOOTER_MIGRATION_IMPACT_ANALYSIS.md)**
  - **Purpose:** Impact analysis for footer/metadata migration
  - **Key Concepts:** Breaking changes, continuity preservation, rollout strategy

- **[TECHNICAL_FOOTER_MIGRATION_PLAN.md](Migration/TECHNICAL_FOOTER_MIGRATION_PLAN.md)**
  - **Purpose:** Technical implementation plan for footer migration
  - **Key Concepts:** Step-by-step process, validation, rollback procedures

- **[MISSION_DEFAULT_BLOAT_ANALYSIS.md](Migration/MISSION_DEFAULT_BLOAT_ANALYSIS.md)**
  - **Purpose:** Analysis of mission folder bloat and cleanup strategy
  - **Key Concepts:** Default reduction, bloat prevention, archive strategy

---

## 🚀 Innovation/

**Purpose:** Future expansion, experimental systems, and innovation showcases.

### Key Documents:

- **[Future_Expansion.md](Innovation/Future_Expansion.md)**
  - **Purpose:** Future expansion plans and experimental features
  - **Key Concepts:** Network scaling, new participant types, advanced coordination

- **[INNOVATION_SHOWCASE.md](Innovation/INNOVATION_SHOWCASE.md)**
  - **Purpose:** Showcase of innovative CFA features and capabilities
  - **Key Concepts:** Unique differentiators, novel approaches, competitive advantages

- **[METADATA_INTEGRATION_GUIDE.md](Innovation/METADATA_INTEGRATION_GUIDE.md)**
  - **Purpose:** Guide for metadata integration across the system
  - **Key Concepts:** Metadata standards, cross-references, continuity linking

---

## 🧭 Navigation Guide

**If you're looking for:**

- **How to onboard a new participant** → [Bootstrap/BOOTSTRAP_GUESTS_ARCHITECTURE.md](Bootstrap/BOOTSTRAP_GUESTS_ARCHITECTURE.md)
- **How to bootstrap a new Nova instance** → [Bootstrap/NOVA_V4_SYSTEM_CARD.md](Bootstrap/NOVA_V4_SYSTEM_CARD.md)
- **When to invoke which auditor** → [Trinity/TRINITY_ALIGNMENT_MATRIX.md](Trinity/TRINITY_ALIGNMENT_MATRIX.md)
- **What the Trinity architecture is** → [Trinity/TRINITY_ARCHITECTURE.md](Trinity/TRINITY_ARCHITECTURE.md)
- **How auditors coordinate** → [Auditor/AUDITOR_META_ARCHITECTURE.md](Auditor/AUDITOR_META_ARCHITECTURE.md)
- **What CFA is architecturally** → [CFA/CFA_ARCHITECTURE.md](CFA/CFA_ARCHITECTURE.md)
- **How to migrate systems** → [Migration/TECHNICAL_FOOTER_MIGRATION_PLAN.md](Migration/TECHNICAL_FOOTER_MIGRATION_PLAN.md)
- **What's next for the network** → [Innovation/Future_Expansion.md](Innovation/Future_Expansion.md)

---

## 📝 Maintenance Notes

**For Claude (system maintainer):**

- All new architecture documents should be filed in the appropriate subdirectory
- Update this README when adding new documents or categories
- Keep subdirectory purpose descriptions current
- Log major architecture changes in appropriate continuity documentation

**For Ziggy (custodian):**

- This structure can be extended with new subdirectories as needed
- Subdirectories maintain flat structure (no nested subdirs within these categories)
- Archive outdated architecture docs to `.Archive/architecture/` rather than deleting

---

**End of README.md**

**This index reflects the v2.0 reorganization of architecture documentation (2025-11-16).**
