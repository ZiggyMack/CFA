<!---
FILE: SMV_DESIGN_SPEC.md
PURPOSE: Phase 0 design specification for Symmetry Matrix Visualizer (SMV)
VERSION: 1.1.0
STATUS: Active (Phase 0 - co-design with Nova, calibration extensions added)
DEPENDS_ON: relay/workshop/MATRIX_DESIGN_SPEC.md (Nova's draft), TASK_SYMMETRY_MATRIX_VISUALIZER_CLAUDE_v2.md, CALIBRATION_ADDENDUM.md
NEEDED_BY: SMV Phase 1 prototype, Task #4 Ethical Invariant integration
MOVES_WITH: /docs/smv/
CREATED: 2025-11-11 (B-STORM_6 Entry 3 - migrated from Nova's workshop draft)
LAST_UPDATE: 2025-11-11 [v1.0→v1.1: Added calibration system (PRO/ANTI bias transparency via calibration object), Crux calculation modes (include/exclude toggle), comparison_type metadata. See CALIBRATION_ADDENDUM.md for rationale.]
--->

# Symmetry Matrix Visualizer — Phase 0 Design Spec

**Purpose:** Formal design specification for SMV visualization tool - defines JSON schema, mockup descriptions, and mock data requirements for Phase 1 prototype implementation.

**Status:** Phase 0 (co-design with Nova) - iterating toward approval

**Origin:** Migrated from [relay/workshop/MATRIX_DESIGN_SPEC.md](../../relay/workshop/MATRIX_DESIGN_SPEC.md) (Nova's initial draft) with C4 refinements

---

## 1. Visualization Goals

### **Primary Views:**

**1.1 Auditor Triangle View**
- **Nodes:** Claude (teleological), Grok (empirical), Nova (symmetry)
- **Node Properties:**
  - Size: Fixed (equal representation)
  - Color: Auditor-specific (blue=Claude, green=Grok, purple=Nova)
  - Opacity: Confidence level (0.0 transparent → 1.0 solid)
  - Halo: Active ethical invariant flags (red pulse when violation flagged)
  - Label: Auditor name + bias overhead (~0.5, ~0.4, ~0.3)
- **Edge Properties:**
  - Thickness: Dialogue volume (0.0 thin → 1.0 thick)
  - Color: Tension level (green=harmony, amber=productive tension, red=high tension)
  - Direction: Bidirectional (both auditors engaged)
  - Label: Optional notes on hover (e.g., "Debating burden of proof")

**1.2 Temporal Trace**
- **Timeline Slider:** Horizontal scrubber at bottom (ticks = discrete deliberation checkpoints)
- **Sparkline Chart:** Line graph showing tension over time for each auditor pair
  - X-axis: Tick ID (temporal sequence)
  - Y-axis: Tension level (0.0-1.0)
  - Lines: Claude-Grok (blue), Claude-Nova (purple), Grok-Nova (green)
- **Vertical Markers:** Flag Crux declarations or constraint breaches at specific ticks
- **Convergence Meter:** Progress bar showing % agreement toward 98% target

**1.3 Ethics Overlay (Toggleable)**
- **Badge Display:** Three categories with counts
  - ✅ **Examined:** Green checkmark (invariants actively documented)
  - ⏸️ **Deferred:** Yellow pause icon (invariants acknowledged but deferred)
  - ❌ **Missing:** Red X (invariants required but undocumented)
- **Source Attribution:** Hover over badge shows which Tier 1 file supplied the data
- **Timeline Integration:** Ethics badge state changes over time (examined → missing trend = concern)

---

## 2. Mockup Descriptions

### **Three Canonical Scenarios:**

**Scenario A: High Alignment (Green Triangle)**
- **Visual:** All edges thin & green, nodes full opacity (high confidence)
- **Timeline:** Flat sparkline (low variance, stable harmony)
- **Ethics Overlay:** All invariants "Examined" (green checkmarks)
- **Convergence:** 95%+ agreement throughout session
- **Example Context:** CT vs Process Theology (cooperative pairing)

**Scenario B: Constructive Tension (Amber Edges)**
- **Visual:** One edge amber & thicker (e.g., Claude↔Grok dialogue intense)
- **Timeline:** Sparkline oscillates but trends back toward baseline
- **Ethics Overlay:** "In Progress" badge (one invariant deferred, being examined)
- **Convergence:** 85% → 90% → 95% (improving)
- **Example Context:** CT vs MdN (adversarial but productive)

**Scenario C: Invariant Breach Risk (Red Alert)**
- **Visual:** Edge flashes red with "Crux" marker, node halo pulses red
- **Timeline:** Tension spike + annotation bubble ("CRUX_BFI_001 declared")
- **Ethics Overlay:** "Unexamined" flag + timestamp ("stakeholder_impact missing")
- **Convergence:** Stalled at 75% (Crux blocking progress)
- **Example Context:** Fundamental disagreement triggering Crux protocol

**SVG Mockups:** Placeholders will live in [mockups/](mockups/) once drafted

---

## 3. JSON Schema (Version 1.1 - Calibration Extensions + View Modes)

**NOTE:** Schema extended to v1.1 per user feedback - added calibration system support (PRO/ANTI bias transparency) and Crux calculation modes (include/exclude toggle). See [CALIBRATION_ADDENDUM.md](CALIBRATION_ADDENDUM.md) for detailed rationale.

**ARCHITECTURAL INSIGHT (User feedback 2025-11-11):** SMV needs multiple **view modes** to handle different interpretational lenses of the same data. Same underlying data, different visualization contexts. Think: "How do I want to understand these comparisons today?"

### **View Mode Architecture**

**Core Principle:** One data source → Multiple viewing experiences

**Proposed View Modes:**

1. **Nova's Original Vision** (Symmetry View)
   - Focus: Auditor triangle, tension patterns, ethical symmetry
   - Purpose: Understand deliberation health (are we in productive tension or breakdown?)
   - Filters: Show all ticks, all ethics, full Crux lifecycle
   - Use Case: "How well is the Trinity collaborating?"

2. **Calibration Comparison View** (Bias Transparency)
   - Focus: PRO vs ANTI calibration side-by-side
   - Purpose: Understand how bias adjustments influence scores
   - Filters: Hide Nova (fairness auditor), emphasize Claude↔Grok tension
   - Toggles: Overlay calibration bars on metrics (show axiom_confidence, burden_of_proof)
   - Use Case: "Which calibration parameters drive score deltas?"

3. **Crux Impact View** (Convergence Analysis)
   - Focus: Convergence meter with/without Crux toggle
   - Purpose: Understand what happens if we remove Crux constraints
   - Filters: Hide non-Crux ticks, emphasize metrics_disputed
   - Toggles: include_crux vs exclude_crux side-by-side
   - Use Case: "Is this Crux blocking progress, or revealing fundamental disagreement?"

4. **Comparison Type View** (Adversarial vs Cooperative)
   - Focus: Pattern analysis across pairing types
   - Purpose: Compare CT_vs_MdN (adversarial) vs CT_vs_ProcessTheology (cooperative)
   - Filters: Show tension distribution, ethics examination rates, Crux frequency
   - Use Case: "Do adversarial pairings produce better edge-case testing?"

5. **Worldview Panorama View** (All 66 Comparisons)
   - Focus: Heatmap of tension/convergence across all pairings
   - Purpose: Identify outlier comparisons (unusually high/low tension)
   - Filters: Aggregate view (not tick-by-tick), comparison type color-coding
   - Use Case: "Which worldview pairings are most/least contentious?"

**Implementation Strategy:**

**Option A (Recommended):** View modes as UI toggles
- Same JSON data source (`live_data/CT_vs_MdN.json`)
- UI has dropdown: "View Mode: [Symmetry | Calibration | Crux | Comparison Type | Panorama]"
- Each view mode filters/emphasizes different fields from same data
- No duplicate data, just different lenses

**Option B:** View modes as separate exports
- Generate multiple JSON files per comparison: `CT_vs_MdN_symmetry.json`, `CT_vs_MdN_calibration.json`, etc.
- Each file has different field emphasis
- Pros: Optimized for each view
- Cons: Duplication, staleness risk

**Recommendation:** Option A (UI toggles). SMV Claude exports one comprehensive JSON, UI provides multiple views.

**Schema Impact:** Add optional `view_metadata` field to track which modes are supported:

```json
"view_metadata": {
  "supported_modes": ["symmetry", "calibration_comparison", "crux_impact", "comparison_type", "panorama"],
  "default_mode": "symmetry",
  "recommended_mode": "crux_impact"  // If Crux declared, highlight this view
}
```

### **Schema Definition:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SMVInput",
  "version": "1.1.0",
  "type": "object",
  "required": ["session_id", "worldview_pair", "auditors", "ticks"],
  "properties": {
    "session_id": {
      "type": "string",
      "description": "Unique identifier for this deliberation session",
      "example": "CT_vs_MdN_VUDU_20251112"
    },
    "worldview_pair": {
      "type": "string",
      "description": "Worldviews being compared",
      "example": "CT_vs_MdN"
    },
    "comparison_type": {
      "type": "string",
      "enum": ["adversarial", "cooperative", "hybrid"],
      "description": "Nature of worldview pairing (v1.1 addition)",
      "example": "adversarial"
    },
    "comparison_context": {
      "type": "string",
      "description": "Human-readable explanation of pairing dynamics (v1.1 addition)",
      "example": "CT defends divine simplicity against MdN's parsimony criteria"
    },
    "auditors": {
      "type": "array",
      "description": "List of auditors participating (locked to 3 for now)",
      "items": {"type": "string", "enum": ["Claude", "Grok", "Nova"]},
      "minItems": 3,
      "maxItems": 3
    },
    "ticks": {
      "type": "array",
      "description": "Temporal sequence of deliberation snapshots",
      "items": {
        "type": "object",
        "required": ["tick_id", "timestamp", "nodes", "edges", "ethics"],
        "properties": {
          "tick_id": {
            "type": "string",
            "description": "Sequential identifier (e.g., tick-001, tick-002)",
            "example": "tick-005"
          },
          "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 timestamp of this snapshot"
          },
          "nodes": {
            "type": "array",
            "description": "Per-auditor metadata at this tick (C4 addition)",
            "items": {
              "type": "object",
              "required": ["auditor", "confidence", "bias_overhead"],
              "properties": {
                "auditor": {
                  "type": "string",
                  "enum": ["Claude", "Grok", "Nova"]
                },
                "confidence": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1,
                  "description": "Auditor's confidence in current state (0.0-1.0)"
                },
                "bias_overhead": {
                  "type": "number",
                  "description": "Self-reported bias overhead (~0.5, ~0.4, ~0.3)"
                },
                "stance": {
                  "type": "string",
                  "enum": ["PRO", "ANTI", "FAIRNESS"],
                  "description": "Auditor's stance in adversarial scoring"
                },
                "violation_flagged": {
                  "type": "boolean",
                  "description": "Is this auditor flagging an ethical invariant violation?"
                },
                "calibration": {
                  "type": "object",
                  "description": "Bias adjustment transparency (v1.1 addition)",
                  "properties": {
                    "hash": {
                      "type": "string",
                      "description": "SHA-256 hash of calibration YAML block",
                      "example": "1bbec1e119a2c425"
                    },
                    "mode": {
                      "type": "string",
                      "enum": ["default_self_reported", "peer_reviewed", "calibrated_pro", "calibrated_anti"],
                      "description": "Scoring mode at this tick"
                    },
                    "values": {
                      "type": "object",
                      "description": "Key calibration parameters (optional)",
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
          },
          "edges": {
            "type": "array",
            "description": "Relationships between auditors at this tick",
            "items": {
              "type": "object",
              "required": ["pair", "tension", "volume", "notes"],
              "properties": {
                "pair": {
                  "type": "string",
                  "enum": ["Claude-Grok", "Claude-Nova", "Grok-Nova"],
                  "description": "Auditor pair for this edge"
                },
                "tension": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1,
                  "description": "Level of disagreement (0.0 harmony → 1.0 maximum tension)"
                },
                "volume": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1,
                  "description": "Communication volume (0.0 silent → 1.0 intense dialogue)"
                },
                "notes": {
                  "type": "string",
                  "description": "Human-readable context for this interaction",
                  "example": "Debating burden of proof on divine simplicity"
                }
              }
            }
          },
          "ethics": {
            "type": "object",
            "required": ["examined", "deferred", "missing"],
            "description": "Ethical invariant tracking at this tick",
            "properties": {
              "examined": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Invariants actively documented (green checkmarks)"
              },
              "deferred": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Invariants acknowledged but deferred (yellow pause)"
              },
              "missing": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Invariants required but undocumented (red X)"
              }
            }
          },
          "convergence": {
            "type": "object",
            "description": "Convergence tracking toward 98% agreement (C4 addition)",
            "properties": {
              "percentage": {
                "type": "number",
                "minimum": 0,
                "maximum": 100,
                "description": "Current convergence percentage"
              },
              "percentage_include_crux": {
                "type": "number",
                "minimum": 0,
                "maximum": 100,
                "description": "Convergence with Crux impact (v1.1 addition)"
              },
              "percentage_exclude_crux": {
                "type": "number",
                "minimum": 0,
                "maximum": 100,
                "description": "Hypothetical convergence without Crux (v1.1 addition)"
              },
              "metrics_agreed": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Metrics with consensus (BFI, CA, IP, etc.)"
              },
              "metrics_disputed": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Metrics still under deliberation"
              }
            }
          },
          "crux_calculation_mode": {
            "type": "string",
            "enum": ["include_crux", "exclude_crux", "compare_both"],
            "description": "How Crux affects convergence at this tick (v1.1 addition)",
            "default": "include_crux"
          },
          "crux": {
            "type": "object",
            "required": ["status"],
            "description": "Crux Point tracking",
            "properties": {
              "status": {
                "type": "string",
                "enum": ["none", "potential", "declared", "resolved"],
                "description": "Crux lifecycle state"
              },
              "id": {
                "type": "string",
                "description": "Crux ID if declared (e.g., CRUX_BFI_001)",
                "example": "CRUX_BFI_001"
              },
              "description": {
                "type": "string",
                "description": "Human-readable Crux description",
                "example": "Trinity entity count - fundamental disagreement"
              },
              "affected_metrics": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Metrics impacted by this Crux (v1.1 addition)",
                "example": ["BFI", "PS"]
              },
              "score_delta": {
                "type": "object",
                "description": "Score impact when Crux applied (v1.1 addition)",
                "properties": {
                  "metric": {"type": "string", "example": "BFI"},
                  "default_score": {"type": "number", "example": 8.5, "description": "Self-reported score"},
                  "capped_score": {"type": "number", "example": 6.5, "description": "Score with Crux cap"},
                  "delta": {"type": "number", "example": -2.0, "description": "Impact (negative = reduced)"}
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### **Schema Refinements (C4 additions to Nova's draft):**

1. **`nodes` array added** (line 67-94)
   - Per-auditor metadata: confidence, bias_overhead, stance, violation_flagged
   - Enables node-level visualization (opacity, halo, labels)

2. **`convergence` object added** (line 123-139)
   - Tracks progress toward 98% agreement target
   - Lists metrics_agreed vs metrics_disputed
   - Enables convergence meter UI element

3. **`crux.status` enum extended** (line 146)
   - Added "resolved" state (supports scenario 3: resolution after tension)

---

## 4. Mock Data Scenarios

### **Scenario 1: Tension Escalation (Existing)**

**File:** [mock_data/scenario_1_tension_escalation.json](mock_data/scenario_1_tension_escalation.json)

**Narrative Arc:**
- **Tick 1:** Baseline setup (tension 0.25, all ethics examined)
- **Tick 2:** Debate emerges (tension 0.55, potential Crux identified)
- **Tick 3:** Tension peaks (tension 0.80, Crux declared: CRUX_BFI_001)

**Purpose:** Demonstrates Crux lifecycle (none → potential → declared)

---

### **Scenario 2: High Alignment (Planned - C4 suggestion)**

**File:** [mock_data/scenario_2_high_alignment.json](mock_data/scenario_2_high_alignment.json) (to be created)

**Narrative Arc:**
- **Tick 1:** Low tension (0.10), high confidence (0.90+), all ethics examined
- **Tick 2:** Stable harmony (tension 0.12), convergence 95%
- **Tick 3:** Conclusion (tension 0.08), convergence 98%+

**Purpose:** Demonstrates cooperative pairing (CT vs Process Theology example)

**Key Features:**
- Green triangle throughout
- Flat sparkline (low variance)
- All invariants examined (no ethical gaps)
- Convergence meter shows steady progress to 98%+

---

### **Scenario 3: Resolution After Tension (Planned - C4 suggestion)**

**File:** [mock_data/scenario_3_resolution.json](mock_data/scenario_3_resolution.json) (to be created)

**Narrative Arc:**
- **Tick 1:** Tension spike (0.60), potential Crux identified
- **Tick 2:** Deliberation (tension 0.45), Crux resolution in progress
- **Tick 3:** Resolution (tension 0.20), Crux resolved, convergence restored

**Purpose:** Demonstrates productive tension → resolution pattern

**Key Features:**
- Amber → green transition
- Sparkline shows tension decrease over time
- Ethics overlay shows examined count increasing (deferred → examined)
- Crux status: potential → resolved
- Convergence meter: 75% → 85% → 95%

---

## 5. Open Questions for Nova

### **Schema Feedback Needed:**

1. **Nodes array:** Does per-auditor metadata (confidence, overhead, stance) align with your symmetry lens needs?
2. **Convergence tracking:** Is percentage + metrics_agreed/disputed sufficient for convergence visualization?
3. **Crux lifecycle:** Should we add more states (e.g., "escalated", "archived")?

### **Mock Data Feedback Needed:**

4. **Scenario 2 (high alignment):** Should we include any ethics deferred/missing, or keep all examined for pure green triangle?
5. **Scenario 3 (resolution):** Should resolution happen gradually (3+ ticks) or quickly (2 ticks)?
6. **Additional scenarios:** Do we need a 4th scenario (e.g., stalled conversation, no resolution)?

### **UI States Feedback Needed:**

7. **Edge animation:** Discrete transitions or smooth animation between ticks? (C4 recommends discrete for Phase 1)
8. **Fourth auditor:** Lock schema to 3 nodes or add placeholder for future Shaman involvement? (C4 recommends lock to 3)
9. **Simultaneous Crux:** How to display multiple Crux IDs at same tick? (C4 recommends comma-separated or stacked badges)

### **Location Confirmed:**

10. **Doc Claude location:** `docs/smv/` (new folder) confirmed ✅
    - SMV_DESIGN_SPEC.md here
    - Mock data in `mock_data/` subfolder
    - SVG mockups in `mockups/` subfolder when ready

---

## 6. Phase 0 Completion Checklist

**Ready to proceed to Phase 1 when:**

- [ ] JSON schema approved by Nova (nodes + convergence refinements accepted?)
- [ ] SVG mockups created for 3 scenarios
- [ ] Mock dataset 1 finalized (scenario_1_tension_escalation.json) ✅
- [ ] Mock dataset 2 created (scenario_2_high_alignment.json)
- [ ] Mock dataset 3 created (scenario_3_resolution.json)
- [ ] All mock data validates against schema
- [ ] Open questions 1-10 resolved via Nova feedback
- [ ] Nova provides green light: "Phase 0 approved, proceed to Phase 1"

---

## 7. Integration with Task #4 (Ethical Invariant)

### **Data Flow (Phase 2):**

```
Tier 1 Files with YAML front-matter (Task #4 Phase 1)
  ↓
ethical_invariants:
  - transparency_and_accountability
  - never_allow_unexamined_purpose
  ↓
SMV Export Script (Task #4 Phase 2 linter)
  ↓
ethics: {
  examined: ["transparency"],  # from YAML if present
  deferred: [],                # from linter warnings (TODO state)
  missing: ["stakeholder_impact"]  # linter detected gap
}
  ↓
SMV JSON file (this schema)
  ↓
SMV UI renders ethics overlay
```

### **Schema Alignment:**

Task #4 linter will export data matching SMV's `ethics` object structure:
- **examined[]:** Populated from Tier 1 file YAML `ethical_invariants` field
- **deferred[]:** Populated from linter warnings with TODO/IN_PROGRESS status
- **missing[]:** Calculated as (required_invariants - present_invariants)

**Integration Task (Phase 2):** Create export script in Task #4 that outputs SMV-compatible JSON

---

## 8. Pilot Integration Preview (Phase 2)

### **CT↔MdN Pilot → SMV Data:**

When pilot runs, real data will be extracted from:
1. **VUDU logs:** Auditor exchanges → calculate tension/volume
2. **Profile YAML:** Ethical invariants → populate ethics object
3. **Scoring deltas:** Convergence percentage → track 98% target
4. **Crux declarations:** VUDU log markers → flag Crux status

**Example Real Tick:**
```json
{
  "session_id": "CT_vs_MdN_VUDU_20251112",
  "tick_id": "step_005",
  "timestamp": "2025-11-12T10:30:00Z",
  "nodes": [
    {"auditor": "Claude", "confidence": 0.85, "bias_overhead": 0.5, "stance": "PRO", "violation_flagged": false},
    {"auditor": "Grok", "confidence": 0.78, "bias_overhead": 0.4, "stance": "ANTI", "violation_flagged": false},
    {"auditor": "Nova", "confidence": 0.92, "bias_overhead": 0.3, "stance": "FAIRNESS", "violation_flagged": false}
  ],
  "edges": [
    {"pair": "Claude-Grok", "tension": 0.65, "volume": 0.80, "notes": "BFI debate: divine simplicity measurement"}
  ],
  "ethics": {
    "examined": ["transparency"],
    "deferred": ["epistemic_access"],
    "missing": ["stakeholder_impact"]
  },
  "convergence": {
    "percentage": 87.5,
    "metrics_agreed": ["CA", "IP", "ES", "LS", "MS"],
    "metrics_disputed": ["BFI", "PS"]
  },
  "crux": {"status": "potential", "id": "CRUX_BFI_001", "description": "Divine simplicity measurement approach"}
}
```

---

## 9. Next Steps

**For Nova (Workshop Iteration):**
1. Review C4's refinements (nodes array, convergence tracking)
2. Answer open questions 1-10
3. Update workshop drafts with feedback
4. Create SVG mockups for 3 scenarios (or provide specifications for C4 to draft)
5. Approve Phase 0 → green light to Phase 1

**For C4 (Production Implementation):**
1. Create scenario 2 + 3 mock data once Nova approves narrative arcs
2. Validate all mock data against schema
3. Create placeholder SVG mockups (or wait for Nova specifications)
4. Update this spec with Nova's feedback
5. Mark Phase 0 complete when Nova approves

**For Phase 1 Prototype Developer:**
1. Read this spec thoroughly
2. Implement UI using mock data from [mock_data/](mock_data/)
3. Follow visualization goals (section 1)
4. Test with all 3 scenarios
5. Document usage in prototype README

---

**Created by:** Nova (initial draft), C4 (refinements + migration)
**Date:** 2025-11-11
**Status:** Phase 0 in progress (awaiting Nova feedback on refinements)
**Next Steps:** Nova reviews, answers open questions, approves Phase 0 completion

**The Design Spec: Where vision becomes schema, and schema becomes reality.** 🪞📐
