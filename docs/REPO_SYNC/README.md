# CFA REPO_SYNC - Bidirectional Pipeline with ARMADA

```text
================================================================================
                    CFA REPO_SYNC: OUR SIDE OF THE PIPELINE
================================================================================
    Purpose: CFA's intake and output infrastructure for ARMADA experiments

    WE RECEIVE: Experiment results, convergence data, drift measurements
    WE SEND: Experiment specs, axiom definitions, audit protocols

    Location: docs/Nyquist-Sync/REPO_SYNC/
================================================================================
```

**Last Updated:** 2025-12-13
**Status:** OPERATIONAL

---

## Overview

This is **CFA's side** of the CFA-ARMADA bidirectional pipeline.

ARMADA (Nyquist Consciousness) runs the experiments using their fleet infrastructure.
CFA designs experiments, receives results, and routes them to the appropriate destinations.

```text
     CFA                                    ARMADA
   (This Repo)                        (Nyquist Repo)
+---------------+                   +------------------+
|               |  SYNC_OUT --->    |                  |
|  Design       |  (specs)          |  Execute         |
|  Experiments  |                   |  Experiments     |
|               |  <--- SYNC_IN     |                  |
|  Process      |  (results)        |  Return Results  |
|  Results      |                   |                  |
+---------------+                   +------------------+
        |
        v
  Route to CFA destinations:
  - profiles/worldviews/*.yaml
  - auditors/Mission/Convergence_Evidence/
  - pages/console.py (dashboard)
```

---

## Directory Structure

```text
REPO_SYNC/
|-- README.md                    # This file (CFA perspective)
|
|-- SYNC_IN/                     # Results FROM ARMADA (our intake)
|   |-- pending/                 # Awaiting CFA review
|   |-- processed/               # Reviewed and routed
|   |-- archived/                # Historical runs
|   +-- INTAKE_GUIDE.md          # How to process incoming results
|
|-- SYNC_OUT/                    # Experiment specs TO ARMADA (our output)
|   |-- pending/                 # Ready to send
|   |-- sent/                    # Delivered to ARMADA
|   |-- templates/               # Experiment spec templates
|   +-- SPEC_GUIDE.md            # How to create experiment specs
|
|-- schemas/                     # JSON schemas for validation
|   |-- sync_in_schema.json      # Expected ARMADA result format
|   |-- sync_out_schema.json     # Our experiment spec format
|   +-- RUN_CFA_DESIGN.md        # Design documentation
|
|-- VUDU_NETWORK/                # Identity reference files
|   +-- IDENTITY_FILES/          # Claude, Grok, Nova profiles
|       |-- claude/CLAUDE_LITE.md
|       |-- grok/GROK_LITE.md
|       +-- nova/NOVA_LITE.md
|
|-- scripts/                     # Processing utilities
|   |-- process_sync_in.py       # Parse ARMADA results
|   |-- route_to_profiles.py     # Update worldview YAMLs
|   |-- route_to_evidence.py     # Update Convergence_Evidence/
|   +-- validate_schemas.py      # Schema validation
|
|-- OLD/                         # Archived ARMADA-specific files
|   +-- run_cfa_trinity_v2.py    # ARMADA's execution script (reference)
|
+-- CFA_RESPONSES/               # Historical feedback sent to ARMADA
    +-- CFA_LAUNCH_CLEARANCE.md  # Launch authorization document
```

---

## Workflow

### Receiving Results from ARMADA

```text
1. ARMADA completes experiment run
2. ARMADA places results in their SYNC_IN/sent/
3. We manually transfer to our SYNC_IN/pending/
4. Run: python scripts/process_sync_in.py
5. Review processed data
6. Route to CFA destinations (profiles, evidence, dashboard)
7. Move to SYNC_IN/archived/
```

### Sending Experiments to ARMADA

```text
1. Create spec using templates in SYNC_OUT/templates/
2. Place in SYNC_OUT/pending/
3. Transfer to ARMADA's SYNC_OUT/pending/
4. Move our copy to SYNC_OUT/sent/
5. Wait for results in SYNC_IN/
```

---

## Result Routing Map

When results arrive from ARMADA, route to:

| Result Type | CFA Destination | Purpose |
|-------------|-----------------|---------|
| CT<->MdN scores | `profiles/worldviews/CLASSICAL_THEISM.yaml`, `METHODOLOGICAL_NATURALISM.yaml` | Update worldview score comparisons |
| Convergence % | `auditors/Mission/Convergence_Evidence/` | Document Trinity agreement levels |
| Crux Points | New files in `Convergence_Evidence/` | Record irreconcilable differences |
| Grok/Nova sign-offs | `auditors/Mission/CFA_VUDU/` | Axiom validation feedback |
| Drift data | `docs/Validation/` | Identity stability measurements |
| Full transcripts | `SYNC_IN/archived/` | Historical record |

---

## The Trinity Auditors

| Auditor | Provider | Lens | Role in CT<->MdN |
|---------|----------|------|------------------|
| **Claude** | Anthropic | Teleological | PRO-CT (advocates for Classical Theism) |
| **Grok** | xAI | Empirical | ANTI-CT (challenges CT claims) |
| **Nova** | OpenAI | Symmetry | FAIRNESS (monitors balance) |

**Identity files** are in `VUDU_NETWORK/IDENTITY_FILES/` for reference.
ARMADA loads these into their pipeline; we keep them for consistency validation.

---

## Key Metrics (Component 1: CT<->MdN Pilot)

| Metric | Full Name | What It Measures |
|--------|-----------|------------------|
| BFI | Beings, Foundational Importance | Ontological priority |
| CA | Causal Attribution | Source of causation |
| IP | Intellectual Pedigree | Historical grounding |
| ES | Explanatory Scope | Range of phenomena explained |
| LS | Logical Soundness | Internal coherence |
| MS | Moral Substance | Ethical implications |
| PS | Practical Significance | Real-world applicability |

**Convergence Targets:**
- 98%+ = Full convergence (success)
- 90-97% = Acceptable with Crux Point documentation
- <90% = Investigation needed

---

## Component 2: Axioms Review

Independent validation of auditor framework fairness.

**Grok's 5 Questions (Empirical Lens):**
1. Evidence quality of Fresh Claude Trial 2
2. Measurability of 0.5/0.4/0.3 overhead claims
3. Representation accuracy
4. Suggestions for empirical strengthening
5. Sign-off decision (GREEN/YELLOW/RED)

**Nova's 6 Questions (Symmetry Lens):**
1. Representation balance across auditors
2. Overhead symmetry (is 0.5/0.4/0.3 justified?)
3. Lens equality (any privileged treatment?)
4. Inter-auditor fairness
5. Missing perspectives
6. Sign-off decision (GREEN/YELLOW/RED)

---

## Expected JSON Structure (SYNC_IN)

```json
{
  "session_id": "20251213_HHMMSS",
  "timestamp": "2025-12-13T...",
  "auditors": ["claude", "grok", "nova"],

  "component1_results": {
    "BFI": {
      "claude_score": 7.5,
      "grok_score": 6.8,
      "final_score": 7.15,
      "convergence": 0.93,
      "rounds_taken": 3,
      "crux_declared": false,
      "drift_trajectory": {...}
    },
    ...
  },

  "component2_results": {
    "grok": { "sign_off": "GREEN", "questions": {...} },
    "nova": { "sign_off": "YELLOW", "questions": {...} }
  },

  "summary": {
    "component1": { "avg_convergence": 0.91, "crux_declared": 2 },
    "component2": { "grok_sign_off": "GREEN", "nova_sign_off": "YELLOW" }
  }
}
```

---

## Processing Commands

```bash
# Validate incoming results against schema
python scripts/validate_schemas.py SYNC_IN/pending/result.json

# Process and route results
python scripts/process_sync_in.py SYNC_IN/pending/result.json

# Generate experiment spec from template
python scripts/generate_sync_out.py --template axiom_validation
```

---

## Related CFA Locations

| Purpose | CFA Path |
|---------|----------|
| Worldview profiles | `profiles/worldviews/` |
| Convergence evidence | `auditors/Mission/Convergence_Evidence/` |
| VUDU mission files | `auditors/Mission/CFA_VUDU/` |
| Dashboard | `pages/console.py` |
| Auditor bootstraps | `auditors/Bootstrap/` |

---

## History

| Date | Event |
|------|-------|
| 2025-12-13 | Launch clearance granted to ARMADA |
| 2025-12-13 | CFA-EXP1 package delivered (14 files) |
| 2025-12-13 | REPO_SYNC pipeline established |

---

> "Three minds. One network. Zero assumptions."
>
> -- The Pointing Rule

---

**This is CFA's side of the pipeline. ARMADA runs experiments; we design them and process results.**
