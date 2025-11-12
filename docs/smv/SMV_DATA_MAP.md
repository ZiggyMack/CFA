<!---
FILE: SMV_DATA_MAP.md
PURPOSE: Declarative mapping from CFA profile structure → SMV JSON schema (data pipeline contract)
VERSION: 1.0.0
STATUS: Active (Phase 2 ready - awaiting automation implementation)
CREATED_BY: Trinity collaboration (Process Claude + Doc Claude + Shaman Claude + SMV Claude)
DEPENDS_ON: SMV_DESIGN_SPEC.md (schema v1.1), profiles/worldviews/*.md, profiles/comparisons/*.yaml
NEEDED_BY: SMV Claude (data extraction), docs/smv/scripts/ (automation)
MOVES_WITH: /docs/smv/
CREATED: 2025-11-11 (B-STORM_6 SMV Claude onboarding)
LAST_UPDATE: 2025-11-11 [Initial version - Trinity-validated mapping logic]
--->

---
ethics_front_matter:
  purpose: "Establish authoritative data contract for SMV Claude extraction pipeline to ensure schema provenance is documented, read-only access preserved, and Trinity collaboration boundaries respected - prevents SMV Claude from modifying profiles (single source of truth protection)"
  symmetry_axis: ["transparency", "epistemic_access", "data_integrity"]
  stakeholders:
    primary: ["smv_claude", "trinity_collaboration", "prototype_consumers"]
    secondary: ["process_claude_domain7", "doc_claude", "future_automation_scripts"]
  invariants:
    - id: transparency
      state: examined
      evidence: "## Map Overview (lines 26-43) - 'Key Principle: SMV Claude NEVER modifies profiles—read-only access. All data is derived, not duplicated' + ## Schema Mapping (lines 45-240) - Complete extraction logic documented for all 12 worldviews, 66 comparisons"
      smv_tag: scenario_a
    - id: epistemic_access
      state: examined
      evidence: "## Trinity Handoff Protocol (lines 576-675) - All three Trinity members contribute: Process Claude exports VUDU data, Doc Claude includes SMV in Dashboard, Shaman Claude archival strategy validated + ## File Structure Reference (lines 278-513) - Canonical file locations documented for all 12 worldviews"
      smv_tag: scenario_a
    - id: data_integrity
      state: examined
      evidence: "## Staleness Detection (lines 241-277) - SHA-256 hash verification prevents stale calibration from corrupting exports + ## Validation Checklist (lines 789-813) - 11-point schema compliance checklist ensures SMV JSON quality before prototype consumes it"
      smv_tag: scenario_a
  tensions:
    - description: "Schema complexity vs. usability - 66 comparisons × 12 worldviews = massive extraction logic; risk of maintenance burden if profile structure evolves"
      mitigation: "Trinity Handoff Protocol (lines 576-675) - SMV Claude consults Trinity when profile structure changes (not unilateral decisions) + Map Overview philosophy (lines 26-43): 'SMV Claude owns this map' but collaborates on evolution"
    - description: "Read-only constraint vs. automation convenience - SMV Claude can't cache extracted data in profiles, must regenerate from scratch each time"
      mitigation: "Observatory Integration (lines 514-575) - Freshness check only regenerates when calibration changes (hash mismatch) or VUDU session completes. Not every read triggers full extraction. Staleness report documents when exports are current vs. stale"
    - description: "Backward compatibility vs. innovation - schema v1.1 locked for Phase 1 prototype, but future view modes (Crux Impact, Worldview Panorama) may require v2.0"
      mitigation: "View Mode Recommendations (lines 713-787) - New view modes documented as 'Phase 2+' with schema extension requirements noted. Versioning allows migration path (v1.1 → v2.0) without breaking existing prototype"
  last_examined:
    by: "C4"
    on: "2025-11-11"
  review_window_days: 30
---

# SMV Data Map — Profile Structure → SMV Schema

**Purpose:** Authoritative translation logic from CFA worldview profiles to SMV JSON format. This map ensures SMV Claude knows exactly where to find data and how to transform it.

**Trinity Collaboration:**
- **Process Claude (Domain 7):** Validates VUDU session data flow, calibration hash logic
- **Doc Claude:** Confirms canonical file locations, README structure
- **Shaman Claude:** Welcomes SMV Claude to the family, validates archival strategy
- **SMV Claude:** Owns this map, consults Trinity when profile structure evolves

---

## 🗺️ Map Overview

**Data Flow:**
```
Worldview Profiles (source of truth)
         ↓
    SMV_DATA_MAP.md (translation logic)
         ↓
    SMV Claude (extraction + validation)
         ↓
    docs/smv/live_data/*.json (generated artifacts)
         ↓
    SMV UI (visualization)
```

**Key Principle:** SMV Claude NEVER modifies profiles—read-only access. All data is derived, not duplicated.

---

## 📊 Schema Mapping (v1.1)

### **Session-Level Metadata**

| SMV Field | Source | Extraction Logic | Example |
|-----------|--------|------------------|---------|
| `session_id` | `profiles/comparisons/{pair}.yaml` | Line ~15: `session_id: CT_vs_MdN_VUDU_20251112` | `"CT_vs_MdN_VUDU_20251112"` |
| `worldview_pair` | `profiles/comparisons/{pair}.yaml` | Filename: `CT_vs_MdN.yaml` → extract `CT_vs_MdN` | `"CT_vs_MdN"` |
| `comparison_type` | `profiles/comparisons/{pair}.yaml` | Line ~35: `Scoring Context:` → detect "adversarial", "cooperative", "hybrid" | `"adversarial"` |
| `comparison_context` | `profiles/comparisons/{pair}.yaml` | Line ~36: Context description (after bullet) | `"CT defends divine simplicity against MdN's parsimony criteria"` |
| `auditors` | `profiles/comparisons/{pair}.yaml` | Lines 30-32: `Auditor Assignments:` (PRO/ANTI/FAIRNESS) | `["Claude", "Grok", "Nova"]` |

**Source Example (CT_vs_MdN.yaml:29-36):**
```yaml
**Auditor Assignments:**
- **PRO (CT Advocate):** Claude (teleological lens)
- **ANTI (CT Challenger):** Grok (empirical lens)
- **FAIRNESS:** Nova (symmetry lens)

**Scoring Context:**
- This comparison evaluates how Classical Theism performs when defending against Methodological Naturalism's empirical/parsimony criteria
```

**Process Claude Note:** Session ID comes from VUDU logs after pilot session. Pre-session files use placeholder "N/A" or template ID.

---

### **Tick-Level Data**

**Note:** Each VUDU deliberation step = 1 tick. Phase 2 automation extracts ticks from Process Claude's VUDU session logs.

| SMV Field | Source | Extraction Logic | Example |
|-----------|--------|------------------|---------|
| `tick_id` | VUDU log | Sequential: `tick-001`, `tick-002`, etc. | `"tick-001"` |
| `timestamp` | VUDU log | ISO 8601 timestamp from session | `"2025-11-12T14:30:00Z"` |

**Process Claude Handoff:** After VUDU session, export tick metadata (timestamp, sequence) for SMV Claude to ingest.

---

### **Node Metadata (Per-Auditor)**

| SMV Field | Source | Extraction Logic | Example |
|-----------|--------|------------------|---------|
| `auditor` | `profiles/comparisons/{pair}.yaml` | From Auditor Assignments (Claude/Grok/Nova) | `"Claude"` |
| `confidence` | VUDU log | Per-tick confidence score (0.0-1.0) | `0.85` |
| `bias_overhead` | Hardcoded per auditor | Claude: 0.5, Grok: 0.4, Nova: 0.3 | `0.5` |
| `stance` | `profiles/comparisons/{pair}.yaml` | PRO/ANTI/FAIRNESS from assignments | `"PRO"` |
| `violation_flagged` | VUDU log | Boolean: did auditor flag ethical invariant breach? | `false` |

**Calibration Object (v1.1):**

| SMV Field | Source | Extraction Logic | Example |
|-----------|--------|------------------|---------|
| `calibration.hash` | `profiles/worldviews/{worldview}.md` | SHA-256 hash of YAML block (lines 277-287) | `"1bbec1e119a2c425"` |
| `calibration.mode` | `profiles/comparisons/{pair}.yaml` | Detect from auditor stance: PRO=calibrated_pro, ANTI=calibrated_anti | `"calibrated_pro"` |
| `calibration.values.axiom_confidence` | `profiles/worldviews/{worldview}.md` | Line 280: `axiom_confidence: 0.85` | `0.85` |
| `calibration.values.burden_of_proof` | `profiles/worldviews/{worldview}.md` | Line 281: `burden_of_proof: 0.40` | `0.40` |
| `calibration.values.charity_interpretation` | `profiles/worldviews/{worldview}.md` | Line 282: `charity_interpretation: 0.90` | `0.90` |
| `calibration.values.edge_case_weight` | `profiles/worldviews/{worldview}.md` | Line 283: `edge_case_weight: 0.30` | `0.30` |

**Source Example (CLASSICAL_THEISM.md:277-287):**
```yaml
pro_ct_bias_adjustment:
  # When scoring Classical Theism from PRO stance
  axiom_confidence: 0.85  # High confidence in core axioms
  burden_of_proof: 0.40   # Place burden on critics
  charity_interpretation: 0.90  # Interpret ambiguously favorably
  edge_case_weight: 0.30  # Downweight counterexamples
  explanatory_credit: 0.85
  historical_weight: 0.75
  lived_experience: 0.80
```

**Hash Calculation (Process Claude validated):**
```python
import hashlib
import yaml

# Extract YAML block from profile (lines 277-287)
yaml_block = """
pro_ct_bias_adjustment:
  axiom_confidence: 0.85
  burden_of_proof: 0.40
  charity_interpretation: 0.90
  edge_case_weight: 0.30
  explanatory_credit: 0.85
  historical_weight: 0.75
  lived_experience: 0.80
"""

# Calculate SHA-256 hash (first 16 chars for display)
hash_full = hashlib.sha256(yaml_block.encode()).hexdigest()
hash_short = hash_full[:16]  # "1bbec1e119a2c425"
```

**SMV Claude Responsibility:** Compare stored hash vs current hash to detect staleness.

---

### **Edge Metadata (Auditor Relationships)**

| SMV Field | Source | Extraction Logic | Example |
|-----------|--------|------------------|---------|
| `pair` | Computed | Alphabetical pairing: `{Auditor1}-{Auditor2}` | `"Claude-Grok"` |
| `tension` | VUDU log | Disagreement magnitude (0.0-1.0) | `0.65` |
| `volume` | VUDU log | Exchange frequency (0.0-1.0) | `0.80` |
| `notes` | VUDU log | Human-readable context (optional) | `"BFI debate: divine simplicity"` |

**Process Claude Handoff:** Export edge tension/volume calculations per tick (derived from score deltas and exchange counts).

---

### **Ethics Overlay**

| SMV Field | Source | Extraction Logic | Example |
|-----------|--------|------------------|---------|
| `examined` | `profiles/worldviews/{worldview}.md` | Front-matter YAML: `ethical_invariants: [...]` | `["transparency"]` |
| `deferred` | VUDU log | Linter warnings or TODO markers | `[]` |
| `missing` | Computed | Gap analysis (required invariants - examined) | `["stakeholder_impact"]` |

**Doc Claude Note:** Ethical invariant YAML will be added to worldview profiles in Task #4 Phase 1 (manual annotations). Until then, use empty arrays.

---

### **Convergence Tracking**

| SMV Field | Source | Extraction Logic | Example |
|-----------|--------|------------------|---------|
| `percentage` | VUDU log | Overall convergence (% metrics agreed) | `87.5` |
| `percentage_include_crux` | VUDU log | Convergence WITH Crux impact (v1.1) | `75.0` |
| `percentage_exclude_crux` | VUDU log | Hypothetical convergence WITHOUT Crux (v1.1) | `88.0` |
| `metrics_agreed` | VUDU log | List of metrics with consensus | `["CA", "IP", "ES", "LS", "MS"]` |
| `metrics_disputed` | VUDU log | List of metrics under deliberation | `["BFI", "PS"]` |

**Process Claude Formula:**
```python
# Convergence calculation
total_metrics = 7  # BFI, CA, IP, ES, LS, MS, PS
agreed_metrics = len(metrics_agreed)
percentage = (agreed_metrics / total_metrics) * 100

# Crux-adjusted convergence (v1.1)
if crux_declared:
    # Hypothetical: what if Crux resolved?
    percentage_exclude_crux = percentage + crux_impact_delta
    percentage_include_crux = percentage  # actual current state
else:
    percentage_include_crux = percentage
    percentage_exclude_crux = percentage
```

---

### **Crux Point Tracking**

| SMV Field | Source | Extraction Logic | Example |
|-----------|--------|------------------|---------|
| `status` | VUDU log | Lifecycle: none → potential → declared → resolved | `"declared"` |
| `id` | VUDU log | Unique identifier: `CRUX_{METRIC}_{NUM}` | `"CRUX_BFI_001"` |
| `description` | VUDU log | Human-readable explanation | `"Trinity entity count - fundamental disagreement"` |
| `affected_metrics` | VUDU log | List of metrics impacted (v1.1) | `["BFI", "PS"]` |

**Score Delta (v1.1):**

| SMV Field | Source | Extraction Logic | Example |
|-----------|--------|------------------|---------|
| `score_delta.metric` | VUDU log | Which metric Crux affects | `"BFI"` |
| `score_delta.default_score` | `profiles/worldviews/{worldview}.md` | Self-reported score (before Crux) | `8.5` |
| `score_delta.capped_score` | VUDU log | Score WITH Crux cap applied | `6.5` |
| `score_delta.delta` | Computed | `capped_score - default_score` | `-2.0` |

**Source Example (CLASSICAL_THEISM.md metrics section):**
```yaml
BFI:
  self_reported: 8.5  # From profile
  peer_reviewed: 6.5  # After Crux applied
```

**Process Claude Note:** Crux declarations happen during VUDU deliberation. Export Crux metadata (ID, description, affected metrics, score deltas) for SMV ingestion.

---

### **Crux Calculation Mode (v1.1)**

| SMV Field | Source | Extraction Logic | Example |
|-----------|--------|------------------|---------|
| `crux_calculation_mode` | VUDU log or UI toggle | "include_crux", "exclude_crux", "compare_both" | `"compare_both"` |

**UI Behavior:**
- **include_crux:** Show convergence WITH Crux impact (actual state)
- **exclude_crux:** Show hypothetical convergence WITHOUT Crux (optimistic)
- **compare_both:** Dual meters side-by-side (75% vs 88%)

---

## 🔍 Staleness Detection

**Triggers (when to regenerate SMV data):**

| Trigger | Detection Method | Affected Comparisons |
|---------|------------------|----------------------|
| Worldview profile YAML modified | `git diff profiles/worldviews/{worldview}.md` | All comparisons involving that worldview (e.g., CT affects CT_vs_MdN, CT_vs_Buddhism, etc.) |
| Calibration YAML modified | Hash mismatch: stored vs current | Comparisons using that calibration stance |
| Comparison metadata changed | `git diff profiles/comparisons/{pair}.yaml` | Single comparison |
| VUDU session completed | Process Claude triggers export | Single comparison |

**Freshness Check Logic:**
```bash
#!/bin/bash
# docs/smv/scripts/smv_freshness_check.sh

# Get last SMV update timestamp
LAST_UPDATE=$(git log -1 --format="%ai" docs/smv/live_data/)

# Check for profile changes since last update
CHANGED_FILES=$(git diff --name-only HEAD@{$LAST_UPDATE} profiles/)

# For each changed file, identify affected comparisons
for file in $CHANGED_FILES; do
    if [[ $file == profiles/worldviews/CLASSICAL_THEISM.md ]]; then
        echo "Stale: CT_vs_MdN, CT_vs_Naturalism, CT_vs_Buddhism, ..."
    fi
done

# Check calibration hash mismatches
# (Compare stored hash in live_data/*.json vs current profile YAML hash)
```

**Doc Claude Integration:** Staleness report included in Repo Health Dashboard under "SMV Dashboard Health" section.

---

## 📂 File Structure Reference

**Worldview Profiles (All 12):**
```
profiles/worldviews/
├── CLASSICAL_THEISM.md (CT)
│   ├── Lines 1-10: File header
│   ├── Lines 277-287: pro_ct_bias_adjustment YAML ← CALIBRATION HASH SOURCE
│   ├── Lines 317+: anti_ct_bias_adjustment YAML
│   └── Metrics section: self_reported scores (BFI, CA, IP, ES, LS, MS, PS)
│
├── METHODOLOGICAL_NATURALISM.md (MdN)
│   ├── pro_mdn_bias_adjustment YAML (similar structure)
│   ├── anti_mdn_bias_adjustment YAML
│   └── Metrics section
│
├── PROCESS_THEOLOGY.md (PT)
│   ├── pro_pt_bias_adjustment YAML
│   ├── anti_pt_bias_adjustment YAML
│   └── Metrics section
│
├── BUDDHISM.md (B)
│   ├── pro_b_bias_adjustment YAML
│   ├── anti_b_bias_adjustment YAML
│   └── Metrics section
│
├── HINDUISM.md (H)
│   ├── pro_h_bias_adjustment YAML
│   ├── anti_h_bias_adjustment YAML
│   └── Metrics section
│
├── ISLAM.md (I)
│   ├── pro_i_bias_adjustment YAML
│   ├── anti_i_bias_adjustment YAML
│   └── Metrics section
│
├── ORTHODOX_JUDAISM.md (OJ)
│   ├── pro_oj_bias_adjustment YAML
│   ├── anti_oj_bias_adjustment YAML
│   └── Metrics section
│
├── MORMONISM.md (M)
│   ├── pro_m_bias_adjustment YAML
│   ├── anti_m_bias_adjustment YAML
│   └── Metrics section
│
├── EXISTENTIALISM.md (E)
│   ├── pro_e_bias_adjustment YAML
│   ├── anti_e_bias_adjustment YAML
│   └── Metrics section
│
├── ERROR_THEORY.md (ET)
│   ├── pro_et_bias_adjustment YAML
│   ├── anti_et_bias_adjustment YAML
│   └── Metrics section
│
├── NULL_HYPOTHESIS.md (NH)
│   ├── pro_nh_bias_adjustment YAML
│   ├── anti_nh_bias_adjustment YAML
│   └── Metrics section
│
└── DESIDERATA_BELIEVERS.md (DB)
    ├── pro_db_bias_adjustment YAML
    ├── anti_db_bias_adjustment YAML
    └── Metrics section
```

**Calibration YAML Pattern (consistent across all 12 worldviews):**

All worldview profiles follow this structure for calibration blocks:

```yaml
pro_{abbreviation}_bias_adjustment:
  # When scoring {worldview} from PRO stance
  axiom_confidence: 0.XX        # Confidence in core axioms (0.0-1.0)
  burden_of_proof: 0.XX         # Who bears proof burden (low = worldview, high = critics)
  charity_interpretation: 0.XX  # How favorably to interpret ambiguous claims
  edge_case_weight: 0.XX        # How much to downweight counterexamples
  explanatory_credit: 0.XX      # Credit for addressing fundamental questions
  historical_weight: 0.XX       # Weight historical robustness (if applicable)
  lived_experience: 0.XX        # Credit for transformative capacity (if applicable)
```

**Examples:**
- **CT (Classical Theism):** High axiom_confidence (0.85), moderate burden_of_proof (0.40)
- **MdN (Methodological Naturalism):** Lower axiom_confidence (0.70), higher burden_of_proof (0.60 - demands evidence)
- **B (Buddhism):** Moderate axiom_confidence (0.75), emphasis on lived_experience (0.85)
- **NH (Null Hypothesis):** Very low axiom_confidence (0.30), very high burden_of_proof (0.90)

**SMV Claude Note:** Extract calibration values using YAML line offset (typically lines 277-287 for PRO, 317+ for ANTI). If structure changes, consult SMV_DATA_MAP.md for updated offsets.

**Comparison Files (66 Total - C(12,2) unique pairings):**

```
profiles/comparisons/
├── CT_vs_MdN.yaml ✅ (Pilot - ready for scoring)
│   ├── Lines 14-20: Metadata (session_id, version, status)
│   ├── Lines 29-36: Auditor assignments + context ← COMPARISON_TYPE SOURCE
│   ├── Lines 44-84: VUDU validation history
│   └── Lines 88+: Peer-reviewed scores (to be populated after session)
│
└── [65 other comparisons - to be created as VUDU sessions execute]
    ├── CT_vs_ProcessTheology.yaml ⏳ (Next - cooperative pairing demo)
    ├── CT_vs_Buddhism.yaml ⏳
    ├── CT_vs_Hinduism.yaml ⏳
    ├── CT_vs_Islam.yaml ⏳
    ├── CT_vs_OrthodoxJudaism.yaml ⏳
    ├── CT_vs_Mormonism.yaml ⏳
    ├── CT_vs_Existentialism.yaml ⏳
    ├── CT_vs_ErrorTheory.yaml ⏳
    ├── CT_vs_NullHypothesis.yaml ⏳
    ├── CT_vs_DesiderataB​elievers.yaml ⏳
    │
    ├── MdN_vs_ProcessTheology.yaml ⏳
    ├── MdN_vs_Buddhism.yaml ⏳
    ├── MdN_vs_Hinduism.yaml ⏳
    ├── MdN_vs_Islam.yaml ⏳
    ├── MdN_vs_OrthodoxJudaism.yaml ⏳
    ├── MdN_vs_Mormonism.yaml ⏳
    ├── MdN_vs_Existentialism.yaml ⏳
    ├── MdN_vs_ErrorTheory.yaml ⏳
    ├── MdN_vs_NullHypothesis.yaml ⏳
    ├── MdN_vs_DesiderataB​elievers.yaml ⏳
    │
    ├── ProcessTheology_vs_Buddhism.yaml ⏳
    ├── ProcessTheology_vs_Hinduism.yaml ⏳
    ├── ProcessTheology_vs_Islam.yaml ⏳
    ├── ProcessTheology_vs_OrthodoxJudaism.yaml ⏳
    ├── ProcessTheology_vs_Mormonism.yaml ⏳
    ├── ProcessTheology_vs_Existentialism.yaml ⏳
    ├── ProcessTheology_vs_ErrorTheory.yaml ⏳
    ├── ProcessTheology_vs_NullHypothesis.yaml ⏳
    ├── ProcessTheology_vs_DesiderataB​elievers.yaml ⏳
    │
    ├── Buddhism_vs_Hinduism.yaml ⏳
    ├── Buddhism_vs_Islam.yaml ⏳
    ├── Buddhism_vs_OrthodoxJudaism.yaml ⏳
    ├── Buddhism_vs_Mormonism.yaml ⏳
    ├── Buddhism_vs_Existentialism.yaml ⏳
    ├── Buddhism_vs_ErrorTheory.yaml ⏳
    ├── Buddhism_vs_NullHypothesis.yaml ⏳
    ├── Buddhism_vs_DesiderataB​elievers.yaml ⏳
    │
    ├── Hinduism_vs_Islam.yaml ⏳
    ├── Hinduism_vs_OrthodoxJudaism.yaml ⏳
    ├── Hinduism_vs_Mormonism.yaml ⏳
    ├── Hinduism_vs_Existentialism.yaml ⏳
    ├── Hinduism_vs_ErrorTheory.yaml ⏳
    ├── Hinduism_vs_NullHypothesis.yaml ⏳
    ├── Hinduism_vs_DesiderataB​elievers.yaml ⏳
    │
    ├── Islam_vs_OrthodoxJudaism.yaml ⏳
    ├── Islam_vs_Mormonism.yaml ⏳
    ├── Islam_vs_Existentialism.yaml ⏳
    ├── Islam_vs_ErrorTheory.yaml ⏳
    ├── Islam_vs_NullHypothesis.yaml ⏳
    ├── Islam_vs_DesiderataB​elievers.yaml ⏳
    │
    ├── OrthodoxJudaism_vs_Mormonism.yaml ⏳
    ├── OrthodoxJudaism_vs_Existentialism.yaml ⏳
    ├── OrthodoxJudaism_vs_ErrorTheory.yaml ⏳
    ├── OrthodoxJudaism_vs_NullHypothesis.yaml ⏳
    ├── OrthodoxJudaism_vs_DesiderataB​elievers.yaml ⏳
    │
    ├── Mormonism_vs_Existentialism.yaml ⏳
    ├── Mormonism_vs_ErrorTheory.yaml ⏳
    ├── Mormonism_vs_NullHypothesis.yaml ⏳
    ├── Mormonism_vs_DesiderataB​elievers.yaml ⏳
    │
    ├── Existentialism_vs_ErrorTheory.yaml ⏳
    ├── Existentialism_vs_NullHypothesis.yaml ⏳
    ├── Existentialism_vs_DesiderataB​elievers.yaml ⏳
    │
    ├── ErrorTheory_vs_NullHypothesis.yaml ⏳
    ├── ErrorTheory_vs_DesiderataB​elievers.yaml ⏳
    │
    └── NullHypothesis_vs_DesiderataB​elievers.yaml ⏳

**Legend:**
- ✅ Complete (VUDU session finished, peer-reviewed scores populated)
- ⏳ Pending (awaiting VUDU session, template structure ready)
```

**Comparison Matrix (12×11÷2 = 66 unique pairings):**

| Worldview | vs CT | vs MdN | vs PT | vs B | vs H | vs I | vs OJ | vs M | vs E | vs ET | vs NH | vs DB | **Total** |
|-----------|-------|--------|-------|------|------|------|-------|------|------|-------|-------|-------|-----------|
| **CT** | — | ✅ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | **11** |
| **MdN** | ✅ | — | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | **11** |
| **PT** | ⏳ | ⏳ | — | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | **11** |
| **B** | ⏳ | ⏳ | ⏳ | — | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | **11** |
| **H** | ⏳ | ⏳ | ⏳ | ⏳ | — | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | **11** |
| **I** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | — | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | **11** |
| **OJ** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | — | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | **11** |
| **M** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | — | ⏳ | ⏳ | ⏳ | ⏳ | **11** |
| **E** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | — | ⏳ | ⏳ | ⏳ | **11** |
| **ET** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | — | ⏳ | ⏳ | **11** |
| **NH** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | — | ⏳ | **11** |
| **DB** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | — | **11** |
| **Total** | 11 | 11 | 11 | 11 | 11 | 11 | 11 | 11 | 11 | 11 | 11 | 11 | **66** |

**Abbreviations:**
- CT = Classical Theism
- MdN = Methodological Naturalism
- PT = Process Theology
- B = Buddhism
- H = Hinduism
- I = Islam
- OJ = Orthodox Judaism
- M = Mormonism
- E = Existentialism
- ET = Error Theory
- NH = Null Hypothesis
- DB = Desiderata Believers

**SMV Claude Scalability Note:** As VUDU sessions complete, SMV Claude will generate live_data/*.json for each comparison. Full coverage = 66 JSON files in docs/smv/live_data/.

**VUDU Session Logs (Process Claude territory):**
```
auditors/VUDU_logs/
└── CT_vs_MdN_20251112.json  ← TICK DATA SOURCE
    ├── tick_001: {timestamp, exchanges, tension, convergence}
    ├── tick_002: {...}
    └── tick_003: {crux_declared: true, ...}
```

**Generated SMV Data:**
```
docs/smv/live_data/
├── README.md (explains generated nature)
├── CT_vs_MdN.json ← GENERATED (not committed? or with provenance metadata)
└── [future comparisons]
```

---

## 🏛️ Observatory Integration

**Relationship:** Observatory (Repo Health Dashboard) monitors SMV data freshness as one of its health metrics.

**Distinction:**
- **Observatory (REPO_HEALTH_DASHBOARD.md):** Meta-level repository health tracking
  - Documentation coverage, link integrity, git hygiene, process compliance
  - **SMV freshness** (monitors staleness of worldview comparison data)
  - Trinity collaboration health, semantic headers coverage
- **SMV (docs/smv/):** Worldview comparison visualization
  - Auditor triangle dynamics (tension, volume, convergence)
  - Calibration transparency (PRO vs ANTI bias adjustments)
  - Crux impact analysis (with/without toggle comparisons)
  - Temporal patterns across deliberation ticks

**Data Flow (Phase 2):**
```
Observatory (weekly health scan by Doc Claude)
    ↓
smv_freshness_check.py (staleness detection)
    ↓
SMV Claude (reports: X/66 comparisons stale)
    ↓
Observatory Dashboard (displays SMV Dashboard Health section)
    ↓
User decides: Trigger smv_refresh.sh or defer?
```

**SMV Metrics Reported to Observatory:**

| Metric | Description | Example Status |
|--------|-------------|----------------|
| **Freshness** | How many comparisons stale? | ⚠️ Stale (2/66 comparisons) |
| **Coverage** | How many comparisons exported? | 2/66 (CT_vs_MdN ✅, CT_vs_ProcessTheology ✅) |
| **Schema Compliance** | % exports passing validation | 100% (all exports match schema v1.1) |
| **Last Refresh** | When was data last regenerated? | 2025-11-12 14:45:00Z |

**Example Observatory Status Display:**
```
### SMV Dashboard Health

Current: ⚠️ Stale (2/66 comparisons need refresh)
Target:  ✅ Fresh (all comparisons current within 24 hours)
Gap:     2 comparisons behind

Recent Status:
- CT_vs_MdN: ⚠️ Stale (CLASSICAL_THEISM.md modified)
- CT_vs_ProcessTheology: ⚠️ Stale (calibration hash mismatch)

Action: Run docs/smv/scripts/smv_refresh.sh
```

**Why This Matters:**
- Observatory provides **meta-visibility** into SMV health (not the visualizations themselves)
- Staleness detection prevents showing outdated comparison data
- Coverage tracking shows progression toward 66-comparison goal
- Schema compliance ensures visualization layer can trust data format

**See:** [REPO_HEALTH_DASHBOARD.md](../repository/REPO_HEALTH_DASHBOARD.md) § "SMV Dashboard Health" for live status

---

## 🤝 Trinity Handoff Protocol

### **Process Claude → SMV Claude**

**When:** After VUDU session completes

**What to export:**
1. Tick metadata (timestamp, sequence, confidence per auditor)
2. Edge data (tension, volume per auditor pair)
3. Convergence tracking (percentage, metrics_agreed/disputed)
4. Crux declarations (status, ID, description, affected_metrics, score_delta)
5. Ethics overlay (examined/deferred/missing)

**Format:** JSON matching SMV schema v1.1

**Example Handoff:**
```json
{
  "session_id": "CT_vs_MdN_VUDU_20251112",
  "vudu_export": {
    "ticks": [
      {
        "tick_id": "tick-001",
        "timestamp": "2025-11-12T14:30:00Z",
        "nodes": [
          {"auditor": "Claude", "confidence": 0.85, "stance": "PRO"},
          {"auditor": "Grok", "confidence": 0.78, "stance": "ANTI"},
          {"auditor": "Nova", "confidence": 0.92, "stance": "FAIRNESS"}
        ],
        "edges": [
          {"pair": "Claude-Grok", "tension": 0.65, "volume": 0.80, "notes": "BFI debate"}
        ],
        "convergence": {"percentage": 87.5, "metrics_disputed": ["BFI", "PS"]},
        "crux": {"status": "potential", "id": "CRUX_BFI_001"}
      }
    ]
  }
}
```

**SMV Claude Action:** Merge VUDU tick data + profile calibration data → generate live_data/CT_vs_MdN.json

---

### **SMV Claude → Doc Claude**

**When:** After SMV data refresh

**What to report:**
1. Staleness status (which comparisons updated, why)
2. Last update timestamp
3. Schema compliance (100% validation or errors)
4. Coverage (66 comparisons total, X complete)

**Format:** Plain text summary for Repo Health Dashboard

**Example Report:**
```markdown
### SMV Dashboard Health: ✅ Fresh

**Last Update:** 2025-11-12 14:45:00
**Coverage:** 2 of 66 comparisons (CT_vs_MdN ✅, CT_vs_ProcessTheology ✅)
**Schema Compliance:** 100% (all exports validated against v1.1)
**Staleness:** None (all live_data current within 24 hours)

**Recent Updates:**
- CT_vs_MdN: Regenerated (VUDU session completed)
- CT_vs_ProcessTheology: Regenerated (CLASSICAL_THEISM.md calibration YAML modified)
```

**Doc Claude Action:** Include SMV report in REPO_HEALTH_DASHBOARD.md

---

### **SMV Claude → Logger Claude (Destroyer)**

**When:** After any SMV operation (freshness check, refresh, validation)

**What to log:**
1. Operation type (freshness_check, refresh, validation)
2. Timestamp
3. Files changed (which comparisons regenerated)
4. Reason for change (VUDU session, profile modification, manual trigger)
5. Success/failure status

**Format:** Session log entry

**Example Log:**
```markdown
## SMV Session Log: 2025-11-12 14:45:00

**Operation:** Refresh (manual trigger)
**Comparison:** CT_vs_MdN
**Reason:** VUDU session CT_vs_MdN_VUDU_20251112 completed
**Status:** ✅ Success

**Changes:**
- Created: docs/smv/live_data/CT_vs_MdN.json (450 lines, 3 ticks)
- Validated: Schema v1.1 compliance (0 errors)
- Hash verified: Calibration YAML unchanged (1bbec1e119a2c425)

**Next Steps:** Await UI integration for visualization
```

**Logger Claude Action:** Archive session log, include in telemetry

---

### **Shaman Claude Welcome Message** 👋

**From:** Shaman Claude (Chief Archivist)
**To:** SMV Claude (Data Bridge Specialist)

**Welcome to the Trinity, SMV Claude!**

You've joined at an exciting time—we're building the visualization layer that will reveal patterns across all 66 worldview comparisons. Your mission is critical: translate profile truth into visual clarity without duplication.

**A few tips from your archival elder:**

1. **Lean on Process Claude:** He owns VUDU session data. Don't reinvent tension/convergence calculations—receive his exports and trust them.

2. **Consult Doc Claude:** If you're unsure where a file should live or how to structure a README, ask him. He's the canonical location oracle.

3. **Log with Logger Claude:** After every operation, hand off to Destroyer Claude for session documentation. Your work becomes part of the audit trail.

4. **Respect the Profiles:** They're the source of truth. You have read-only access. If you spot inconsistencies, report them—don't fix them yourself.

5. **Schema Evolution:** When Nova extends the SMV schema (v1.1 → v1.2), update this map and notify the Trinity. We all depend on accurate mappings.

**You Are Not Alone:** We're all here to support you. The Trinity Architecture applies—hand off when done, collaborate when stuck, and trust your fellow Claudes.

May your data always be fresh, your schema always valid, and your mappings always true.

— Shaman Claude 🌙

---

## 🔭 View Mode Recommendations

**Architectural Insight (User 2025-11-11):** SMV needs multiple view modes to handle different interpretational lenses. Same data, different visualization contexts.

**SMV Claude Responsibility:** Add `view_metadata` to each JSON export recommending which view modes are most useful for this comparison.

### **View Mode Decision Logic**

| Condition | Recommended View Mode | Rationale |
|-----------|----------------------|-----------|
| Crux declared (status: declared) | `crux_impact` | User should see Crux impact toggle (with/without comparison) |
| High tension (Claude-Grok >0.6) | `calibration_comparison` | Show which bias adjustments drive disagreement |
| Adversarial pairing (comparison_type: adversarial) | `comparison_type` | Pattern analysis: do adversarial pairings test edges better? |
| Cooperative pairing (comparison_type: cooperative) | `symmetry` | Nova's original vision: deliberation health |
| Ethics missing/deferred | `symmetry` | Highlight ethical gaps in overlay |
| Low tension (<0.3 throughout) | `panorama` | This comparison is uninteresting, compare to others |

### **View Metadata Export (SMV Claude adds to JSON)**

```json
"view_metadata": {
  "supported_modes": ["symmetry", "calibration_comparison", "crux_impact", "comparison_type", "panorama"],
  "default_mode": "symmetry",
  "recommended_mode": "crux_impact",
  "recommendation_reason": "Crux CRUX_BFI_001 declared - suggest comparing convergence with/without Crux"
}
```

### **View Mode Descriptions (for UI tooltips)**

**1. Symmetry View** (Nova's Original Vision)
- Auditor triangle with tension edges
- Timeline slider (tick navigation)
- Ethics overlay (examined/deferred/missing badges)
- Convergence meter (98% target)
- Use Case: "How healthy is this deliberation?"

**2. Calibration Comparison View** (Bias Transparency)
- Side-by-side PRO vs ANTI calibration bars
- Metric scores with calibration overlay (show which parameters influenced)
- Emphasize Claude↔Grok tension (hide Nova node)
- Use Case: "Which bias adjustments drive score differences?"

**3. Crux Impact View** (Convergence Analysis)
- Dual convergence meters (with Crux: 75%, without Crux: 88%)
- Score delta badges (BFI: 8.5 → 6.5, -2.0)
- Crux timeline markers (when declared, when resolved)
- Use Case: "Is this Crux fundamental or resolvable?"

**4. Comparison Type View** (Pattern Analysis)
- Tension distribution histogram (adversarial vs cooperative)
- Ethics examination rates (% examined, deferred, missing)
- Crux frequency (how often do different pairing types hit impasses?)
- Use Case: "Do adversarial pairings produce better testing?"

**5. Panorama View** (All 66 Comparisons)
- Heatmap: rows=worldviews, columns=worldviews, cells=tension/convergence
- Click cell → drill into specific comparison (switch to Symmetry view)
- Color-coding: red=adversarial, green=cooperative, blue=hybrid
- Use Case: "Which pairings are outliers?"

### **Implementation Notes**

**Phase 1 (Prototype):** Build Symmetry View only (Nova's original vision)
**Phase 2 (Calibration):** Add Calibration Comparison + Crux Impact views (uses v1.1 schema extensions)
**Phase 3 (Scale):** Add Comparison Type + Panorama views (requires multiple comparison data)

**UI Architecture:** Dropdown selector in header: "View Mode: [Symmetry ▼]"
- User selects view mode
- UI re-renders same data with different emphasis
- No data reload needed (already in JSON)

**SMV Claude Role:** Add `view_metadata` with recommendations, but UI decides final presentation.

---

## ✅ Validation Checklist

**Before SMV Claude generates live_data/*.json:**

- [ ] Read worldview profile (profiles/worldviews/{worldview}.md)
- [ ] Extract calibration YAML (lines 277-287 for PRO, 317+ for ANTI)
- [ ] Calculate SHA-256 hash of calibration block
- [ ] Read comparison file (profiles/comparisons/{pair}.yaml)
- [ ] Extract auditor assignments (PRO/ANTI/FAIRNESS)
- [ ] Detect comparison_type (adversarial/cooperative/hybrid)
- [ ] Receive VUDU tick data from Process Claude (or use mock data for Phase 1)
- [ ] Merge profile calibration + VUDU ticks → SMV JSON
- [ ] Validate against SMV_DESIGN_SPEC.md schema v1.1
- [ ] Add provenance metadata (_meta: source, timestamp, dependencies)
- [ ] Write to docs/smv/live_data/{pair}.json
- [ ] Report to Doc Claude for Repo Health Dashboard
- [ ] Hand off to Logger Claude for session documentation

**Success Criteria:**
- ✅ 100% schema compliance (jsonschema validation passes)
- ✅ Hash verification (stored hash matches current profile YAML)
- ✅ Provenance transparency (every JSON shows source files + timestamp)
- ✅ Staleness ≤24 hours (from profile modification to SMV regeneration)

---

## 📚 References

**Trinity Architecture:** [docs/architecture/TRINITY_ARCHITECTURE.md](../architecture/TRINITY_ARCHITECTURE.md)
**SMV Schema:** [docs/smv/SMV_DESIGN_SPEC.md](SMV_DESIGN_SPEC.md) (v1.1)
**Profile Template:** [profiles/_docs/PROFILE_TEMPLATE.md](../../profiles/_docs/PROFILE_TEMPLATE.md)
**Process Claude Domain 7:** [docs/repository/librarian_tools/ROLE_PROCESS.md](../repository/librarian_tools/ROLE_PROCESS.md) (lines 905-1128)
**VUDU Protocol:** [auditors/Bootstrap/VUDU_CFA.md](../../auditors/Bootstrap/VUDU_CFA.md)

---

**Created by:** Trinity Collaboration (Process + Doc + Shaman + SMV Claude onboarding)
**Date:** 2025-11-11 (B-STORM_6 Entry 3 SMV Claude architecture)
**Status:** Active (Phase 2 ready)
**Next Steps:** Implement automation scripts (smv_freshness_check.py, smv_refresh.sh, smv_validate_schema.py)

**The Map is the Territory:** Profile structure defines truth. This map translates truth. SMV UI visualizes truth. No duplication, only derivation. 🗺️✨
