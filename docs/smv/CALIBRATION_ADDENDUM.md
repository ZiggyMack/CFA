<!---
FILE: CALIBRATION_ADDENDUM.md
PURPOSE: SMV schema extensions to handle CFA calibration system and Crux calculation modes
VERSION: 1.0.0
STATUS: Draft (critical additions identified by user feedback)
DEPENDS_ON: SMV_DESIGN_SPEC.md, profiles/worldviews/CLASSICAL_THEISM.md (calibration YAML)
NEEDED_BY: SMV Phase 1 prototype, Task #4 Ethical Invariant integration
MOVES_WITH: /docs/smv/
CREATED: 2025-11-11 (B-STORM_6 Entry 3 addendum - user feedback on calibration system)
LAST_UPDATE: 2025-11-11 [Initial draft addressing calibration levers and Crux calculation modes]
--->

# SMV Calibration & Crux System Addendum

**Purpose:** Extend SMV JSON schema to support CFA's calibration system (PRO/ANTI bias adjustments) and Crux calculation flexibility (include/exclude modes).

**Context:** Original SMV design spec (v1.0) predates CFA profile architecture refinements (calibration YAML blocks, Crux calculation modes). This addendum ensures SMV can visualize:
1. **Default scores vs peer-reviewed scores** (self-reported with bias vs adversarial deliberation)
2. **Calibration transparency** (which bias adjustments influenced each auditor's scores)
3. **Crux impact visualization** (how scores change when Crux included vs excluded)

---

## Gap Analysis

### **Gap 1: Calibration System Not Captured** ❌

**What CFA Has:**
- PRO stance calibration YAML (lines 277-287 in CLASSICAL_THEISM.md)
  - `axiom_confidence: 0.85` (how strongly auditor trusts core axioms)
  - `burden_of_proof: 0.40` (where auditor places epistemic burden)
  - `charity_interpretation: 0.90` (how generously auditor interprets ambiguities)
  - `edge_case_weight: 0.30` (how much counterexamples reduce score)
  - `explanatory_credit: 0.85`, `historical_weight: 0.75`, `lived_experience: 0.80`
  - **Calibration hash:** `1bbec1e119a2c425` (SHA-256 of this YAML block)

- ANTI stance calibration YAML (similar structure, different values)
  - Calibration hash: `00cd73274759e218`

**What SMV v1.0 Schema Has:**
- `nodes[].stance`: "PRO", "ANTI", "FAIRNESS" ✅
- `nodes[].bias_overhead`: ~0.5, ~0.4, ~0.3 ✅
- ❌ No way to show **which calibration values** influenced scores
- ❌ No way to compare **default (self-reported) vs peer-reviewed** scores

**Why This Matters:**
- Transparency: Users need to see which bias adjustments led to score differences
- Validation: Nova checks if PRO-CT's high BFI score (8.5) is justified by calibration or exaggerated
- Gold Standard: CT↔MdN pilot aims to model "how to score with disclosed bias"

---

### **Gap 2: Crux Calculation Modes Not Captured** ❌

**What CFA Has:**
- **Crux Points** can be declared on specific metrics (e.g., CRUX_BFI_001: "Divine simplicity measurement")
- **Calculation flexibility:**
  - **Mode 1 (Include Crux):** BFI score capped at convergence threshold (e.g., 6.5 instead of 8.5)
  - **Mode 2 (Exclude Crux):** Calculate "what if no Crux" (BFI 8.5 used, show hypothetical)
  - **Visualization need:** Toggle between modes, show delta

**What SMV v1.0 Schema Has:**
- `crux.status`: "none", "potential", "declared", "resolved" ✅
- `crux.id`: "CRUX_BFI_001" ✅
- ❌ No way to toggle **Crux calculation mode** (include vs exclude)
- ❌ No way to show **score delta** (8.5 default → 6.5 capped)

**Why This Matters:**
- Decision-making: User needs to see "what if we resolve this Crux? How much does CT's score improve?"
- Transparency: Show when Crux is blocking progress vs when metrics converge naturally
- Comparison: CT vs MdN (adversarial, Crux likely) ≠ CT vs Process Theology (cooperative, Crux unlikely)

---

### **Gap 3: Scoring Context Partially Captured** ⚠️

**What CFA Has:**
- **Comparison context matters:**
  - CT vs MdN = adversarial (empirical/parsimony pressures)
  - CT vs Process Theology = cooperative (shared theism, different metaphysics)
- **Auditor assignments vary:**
  - CT vs MdN: Claude PRO-CT, Grok ANTI-CT, Nova Fairness
  - CT vs Pantheism: Claude PRO-CT, Nova PRO-Pantheism, Grok Fairness

**What SMV v1.0 Schema Has:**
- `worldview_pair`: "CT_vs_MdN" ✅ (identifies which comparison)
- `nodes[].stance`: "PRO", "ANTI", "FAIRNESS" ✅ (identifies auditor role)
- ❌ No **comparison_type** field ("adversarial" vs "cooperative")
- ❌ No **calibration_hash** tracking (which YAML block influenced this tick?)

**Why This Matters:**
- Pattern recognition: Nova can identify "adversarial pairings have higher tension but better edge-case testing"
- Reproducibility: Future auditors can verify "Claude used calibration hash X when scoring tick 5"

---

## Proposed Schema Extensions

### **Extension 1: Add `calibration` Object to `nodes` Array**

```json
"nodes": {
  "type": "array",
  "items": {
    "required": ["auditor", "confidence", "bias_overhead", "stance"],
    "properties": {
      "auditor": {"enum": ["Claude", "Grok", "Nova"]},
      "confidence": {"type": "number", "minimum": 0, "maximum": 1},
      "bias_overhead": {"type": "number"},
      "stance": {"enum": ["PRO", "ANTI", "FAIRNESS"]},
      "violation_flagged": {"type": "boolean"},

      // NEW: Calibration transparency
      "calibration": {
        "type": "object",
        "description": "Bias adjustment parameters influencing this auditor's scores at this tick",
        "properties": {
          "hash": {
            "type": "string",
            "description": "SHA-256 hash of calibration YAML block (e.g., 1bbec1e119a2c425)",
            "example": "1bbec1e119a2c425"
          },
          "mode": {
            "type": "string",
            "enum": ["default_self_reported", "peer_reviewed", "calibrated_pro", "calibrated_anti"],
            "description": "Scoring mode: default (self-reported from profile), peer-reviewed (post-deliberation), calibrated (with bias adjustments)"
          },
          "values": {
            "type": "object",
            "description": "Key calibration parameters (optional, for transparency UI)",
            "properties": {
              "axiom_confidence": {"type": "number", "minimum": 0, "maximum": 1},
              "burden_of_proof": {"type": "number", "minimum": 0, "maximum": 1},
              "charity_interpretation": {"type": "number", "minimum": 0, "maximum": 1},
              "edge_case_weight": {"type": "number", "minimum": 0, "maximum": 1}
            }
          }
        }
      }
    }
  }
}
```

**Example Tick with Calibration:**
```json
{
  "tick_id": "tick-005",
  "nodes": [
    {
      "auditor": "Claude",
      "confidence": 0.85,
      "bias_overhead": 0.5,
      "stance": "PRO",
      "calibration": {
        "hash": "1bbec1e119a2c425",
        "mode": "calibrated_pro",
        "values": {
          "axiom_confidence": 0.85,
          "burden_of_proof": 0.40,
          "charity_interpretation": 0.90,
          "edge_case_weight": 0.30
        }
      }
    },
    {
      "auditor": "Grok",
      "confidence": 0.78,
      "bias_overhead": 0.4,
      "stance": "ANTI",
      "calibration": {
        "hash": "00cd73274759e218",
        "mode": "calibrated_anti",
        "values": {
          "axiom_confidence": 0.40,
          "burden_of_proof": 0.75,
          "charity_interpretation": 0.50,
          "edge_case_weight": 0.80
        }
      }
    },
    {
      "auditor": "Nova",
      "confidence": 0.92,
      "bias_overhead": 0.3,
      "stance": "FAIRNESS",
      "calibration": {
        "mode": "peer_reviewed",
        "hash": null
      }
    }
  ]
}
```

**Visualization Impact:**
- **Calibration Badge:** Show hash on hover (click → full YAML view)
- **Calibration Comparison:** Side-by-side PRO vs ANTI calibration values
- **Mode Indicator:** Color-code nodes (blue = default, purple = calibrated_pro, amber = calibrated_anti, green = peer_reviewed)

---

### **Extension 2: Add `crux_calculation_mode` to Tick Level**

```json
"ticks": {
  "type": "array",
  "items": {
    "required": ["tick_id", "timestamp", "nodes", "edges", "ethics", "convergence", "crux"],
    "properties": {
      // ... existing fields ...

      // NEW: Crux calculation flexibility
      "crux_calculation_mode": {
        "type": "string",
        "enum": ["include_crux", "exclude_crux", "compare_both"],
        "description": "How Crux affects convergence calculation at this tick",
        "default": "include_crux"
      },

      "crux": {
        "type": "object",
        "required": ["status"],
        "properties": {
          "status": {"enum": ["none", "potential", "declared", "resolved"]},
          "id": {"type": "string"},
          "description": {"type": "string"},

          // NEW: Crux impact on scores
          "affected_metrics": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Which metrics are impacted by this Crux (e.g., ['BFI', 'PS'])",
            "example": ["BFI"]
          },
          "score_delta": {
            "type": "object",
            "description": "Score difference when Crux included vs excluded",
            "properties": {
              "metric": {"type": "string", "example": "BFI"},
              "default_score": {"type": "number", "example": 8.5, "description": "Self-reported score (no Crux)"},
              "capped_score": {"type": "number", "example": 6.5, "description": "Score with Crux cap applied"},
              "delta": {"type": "number", "example": -2.0, "description": "Impact of Crux (negative = score reduced)"}
            }
          }
        }
      }
    }
  }
}
```

**Example Tick with Crux Calculation Modes:**
```json
{
  "tick_id": "tick-008",
  "crux_calculation_mode": "compare_both",
  "convergence": {
    "percentage_include_crux": 75.0,
    "percentage_exclude_crux": 88.0,
    "delta": -13.0
  },
  "crux": {
    "status": "declared",
    "id": "CRUX_BFI_001",
    "description": "Divine simplicity measurement approach",
    "affected_metrics": ["BFI"],
    "score_delta": {
      "metric": "BFI",
      "default_score": 8.5,
      "capped_score": 6.5,
      "delta": -2.0
    }
  }
}
```

**Visualization Impact:**
- **Toggle Switch:** "Include Crux" / "Exclude Crux" / "Compare Both"
- **Convergence Meter:** Show two bars (75% with Crux, 88% without)
- **Crux Impact Badge:** "Crux reduces convergence by 13%" (red alert)
- **Score Delta Overlay:** Show BFI 8.5 → 6.5 with arrow (visualize impact)

---

### **Extension 3: Add `comparison_type` to Session Level**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SMVInput",
  "version": "1.1.0",  // Bump version for calibration extensions
  "type": "object",
  "required": ["session_id", "worldview_pair", "auditors", "ticks"],
  "properties": {
    "session_id": {"type": "string"},
    "worldview_pair": {"type": "string"},
    "auditors": {"type": "array", "items": {"enum": ["Claude", "Grok", "Nova"]}},

    // NEW: Comparison context
    "comparison_type": {
      "type": "string",
      "enum": ["adversarial", "cooperative", "hybrid"],
      "description": "Nature of worldview pairing: adversarial (tension expected), cooperative (shared ground), hybrid (mixed)",
      "example": "adversarial"
    },

    "comparison_context": {
      "type": "string",
      "description": "Human-readable explanation of why this pairing matters",
      "example": "CT vs MdN tests theism under empirical/parsimony pressures (adversarial)"
    },

    "ticks": { /* ... */ }
  }
}
```

**Example Session Metadata:**
```json
{
  "session_id": "CT_vs_MdN_VUDU_20251112",
  "worldview_pair": "CT_vs_MdN",
  "comparison_type": "adversarial",
  "comparison_context": "CT defends divine simplicity against MdN's parsimony criteria. Empirical lens (Grok) challenges supernatural claims. Crux likely on BFI (existence claims) and PS (problem of suffering).",
  "auditors": ["Claude", "Grok", "Nova"]
}
```

**Visualization Impact:**
- **Session Badge:** "Adversarial" (red border) vs "Cooperative" (green border)
- **Context Tooltip:** Hover over session_id → see comparison_context explanation
- **Pattern Analysis:** Nova can filter "show all adversarial pairings" to identify tension patterns

---

## Visualization Mockup Updates

### **New UI Elements Needed:**

**1. Calibration Transparency Panel** (top-left, expandable)
```
┌─────────────────────────────────────┐
│ Calibration Mode: Include Crux     │ [Toggle: Include | Exclude | Compare]
├─────────────────────────────────────┤
│ Claude (PRO-CT):                    │
│   Hash: 1bbec1e1... [View YAML]    │
│   Axiom Confidence: 0.85 ████████   │
│   Burden of Proof: 0.40 ████        │
│   Charity: 0.90 █████████           │
├─────────────────────────────────────┤
│ Grok (ANTI-CT):                     │
│   Hash: 00cd7327... [View YAML]    │
│   Axiom Confidence: 0.40 ████       │
│   Burden of Proof: 0.75 ███████     │
│   Charity: 0.50 █████               │
└─────────────────────────────────────┘
```

**2. Crux Impact Overlay** (when crux_calculation_mode = "compare_both")
```
Triangle View:
  Claude ──[tension 0.65]── Grok
    └── CRUX_BFI_001 marker (red badge)

Convergence Meter:
  With Crux:    ████████████████░░░░░░ 75%
  Without Crux: ████████████████████░░ 88%
  Impact: -13% (Crux blocking progress)

Score Delta Badge:
  BFI: 8.5 → 6.5 (-2.0 from Crux cap)
```

**3. Comparison Type Badge** (session header)
```
Session: CT_vs_MdN | Type: ADVERSARIAL | [i] Context
  Hover tooltip: "CT defends divine simplicity against MdN's parsimony criteria..."
```

---

## Mock Data Updates Needed

### **Scenario 1 (Tension Escalation) - Add Calibration:**

```json
{
  "session_id": "CT_vs_MdN_mock",
  "worldview_pair": "CT_vs_MdN",
  "comparison_type": "adversarial",
  "comparison_context": "Testing CT under empirical pressure",
  "auditors": ["Claude", "Grok", "Nova"],
  "ticks": [
    {
      "tick_id": "tick-001",
      "nodes": [
        {
          "auditor": "Claude",
          "confidence": 0.85,
          "bias_overhead": 0.5,
          "stance": "PRO",
          "calibration": {
            "hash": "1bbec1e119a2c425",
            "mode": "calibrated_pro",
            "values": {"axiom_confidence": 0.85, "burden_of_proof": 0.40}
          }
        },
        {
          "auditor": "Grok",
          "confidence": 0.78,
          "bias_overhead": 0.4,
          "stance": "ANTI",
          "calibration": {
            "hash": "00cd73274759e218",
            "mode": "calibrated_anti",
            "values": {"axiom_confidence": 0.40, "burden_of_proof": 0.75}
          }
        }
      ],
      "crux_calculation_mode": "include_crux",
      "crux": {
        "status": "declared",
        "id": "CRUX_BFI_001",
        "affected_metrics": ["BFI"],
        "score_delta": {"metric": "BFI", "default_score": 8.5, "capped_score": 6.5, "delta": -2.0}
      },
      "convergence": {
        "percentage_include_crux": 75.0,
        "percentage_exclude_crux": 88.0
      }
    }
  ]
}
```

---

## Integration with CFA Pilot

### **CT↔MdN Pilot → SMV Data Flow:**

**Step 1: Extract Calibration Hashes**
```python
# From CLASSICAL_THEISM.md lines 277-287
pro_ct_hash = calculate_yaml_hash(pro_ct_bias_adjustment)  # "1bbec1e119a2c425"

# From METHODOLOGICAL_NATURALISM.md
anti_mdn_hash = calculate_yaml_hash(anti_mdn_bias_adjustment)  # "00cd73274759e218"
```

**Step 2: Populate SMV Nodes with Calibration**
```python
smv_tick["nodes"] = [
    {
        "auditor": "Claude",
        "stance": "PRO",
        "calibration": {
            "hash": pro_ct_hash,
            "mode": "calibrated_pro",
            "values": extract_calibration_values(CLASSICAL_THEISM.pro_ct_bias_adjustment)
        }
    },
    # ... Grok, Nova
]
```

**Step 3: Calculate Crux Impact**
```python
if crux_declared_on_BFI:
    smv_tick["crux"] = {
        "status": "declared",
        "id": "CRUX_BFI_001",
        "affected_metrics": ["BFI"],
        "score_delta": {
            "metric": "BFI",
            "default_score": CT_profile.metrics.BFI.self_reported,  # 8.5
            "capped_score": apply_crux_cap(8.5, convergence_threshold),  # 6.5
            "delta": -2.0
        }
    }

    smv_tick["convergence"] = {
        "percentage_include_crux": calculate_convergence(include_crux=True),  # 75%
        "percentage_exclude_crux": calculate_convergence(include_crux=False),  # 88%
        "delta": -13.0
    }
```

---

## Phase 0 Completion Checklist (Updated)

**Original checklist items:** ✅ (from SMV_DESIGN_SPEC.md)

**NEW checklist items:**

- [ ] **Calibration extension approved:** Add `calibration` object to `nodes` array?
- [ ] **Crux calculation modes approved:** Add `crux_calculation_mode` + `score_delta` fields?
- [ ] **Comparison type approved:** Add `comparison_type` + `comparison_context` session metadata?
- [ ] **Mock data updated:** Scenario 1 includes calibration hashes + Crux toggle example?
- [ ] **Visualization mockups updated:** Show calibration transparency panel + Crux impact overlay?
- [ ] **Nova approval:** Extensions align with symmetry lens and visualization-first philosophy?

---

## Next Steps

1. **Nova reviews this addendum** (calibration + Crux extensions)
2. **User confirms:** Do these extensions capture the calibration system and Crux flexibility?
3. **C4 updates SMV_DESIGN_SPEC.md** with approved extensions (bump to v1.1)
4. **C4 updates mock data** (scenario_1 with calibration fields)
5. **Phase 0 complete** → Phase 1 prototype implements extensions

---

**Created by:** C4 (B-STORM_6 Entry 3 addendum - user feedback integration)
**Date:** 2025-11-11
**Status:** Draft (awaiting Nova + user approval)
**Purpose:** Ensure SMV can visualize CFA's calibration system and Crux calculation flexibility

**"Where bias becomes transparency, and Crux becomes insight."** 🎚️⚖️
