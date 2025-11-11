<!---
FILE: README.md
PURPOSE: Documentation for SMV mock data scenarios used in Phase 1 prototype
VERSION: 1.0.0
STATUS: Active (Scenario 1 complete, Scenarios 2-3 planned)
DEPENDS_ON: docs/smv/SMV_DESIGN_SPEC.md, relay/workshop/MATRIX_MOCK_DATA.json
NEEDED_BY: SMV Phase 1 prototype implementation
MOVES_WITH: /docs/smv/mock_data/
CREATED: 2025-11-11 (B-STORM_6 Entry 3)
LAST_UPDATE: 2025-11-11 [Initial structure, Scenario 1 migrated from workshop]
--->

# SMV Mock Data Scenarios

**Purpose:** Mock JSON datasets for SMV Phase 1 prototype development - validates visualization behavior before live data integration

---

## 📋 Scenario Overview

| Scenario | File | Status | Purpose |
|----------|------|--------|---------|
| **1: Tension Escalation** | [scenario_1_tension_escalation.json](scenario_1_tension_escalation.json) | ✅ Complete | Demonstrates Crux lifecycle (none → potential → declared) |
| **2: High Alignment** | scenario_2_high_alignment.json | ⏳ Planned | Demonstrates cooperative pairing (green triangle, 98%+ convergence) |
| **3: Resolution After Tension** | scenario_3_resolution.json | ⏳ Planned | Demonstrates productive tension → resolution pattern |

---

## 🎯 Scenario 1: Tension Escalation

**File:** [scenario_1_tension_escalation.json](scenario_1_tension_escalation.json)

**Narrative Arc:**
- **Tick 1 (baseline):** Low tension (0.25), ethics examined, no Crux
- **Tick 2 (debate):** Moderate tension (0.55), ethics gaps emerge, potential Crux
- **Tick 3 (escalation):** High tension (0.80), Crux declared (CRUX_BFI_001)

**Key Features:**
- Claude-Grok edge: 0.25 → 0.55 → 0.80 tension
- Volume increase: 0.40 → 0.65 → 0.75 (dialogue intensifies)
- Ethics degradation: all examined → deferred → missing (stakeholder_impact)
- Crux lifecycle: none → potential → declared

**Use Cases:**
- Test tension color gradient (green → amber → red)
- Test Crux marker rendering
- Test ethics badge transitions
- Test timeline sparkline (upward tension trend)

---

## 🎯 Scenario 2: High Alignment (Planned)

**File:** scenario_2_high_alignment.json (to be created)

**Narrative Arc:**
- **Tick 1:** Low tension (0.10), high confidence (0.90+), all ethics examined
- **Tick 2:** Stable harmony (0.12), convergence 95%
- **Tick 3:** Conclusion (0.08), convergence 98%+

**Key Features:**
- All edges green (low tension throughout)
- Flat sparkline (low variance)
- All invariants examined (no ethical gaps)
- Convergence meter: 92% → 95% → 98%
- No Crux (status: none throughout)

**Use Cases:**
- Test green triangle visualization (harmony state)
- Test convergence meter (success case)
- Test ethics overlay (all examined state)
- Demonstrate cooperative pairing (CT vs Process Theology example)

---

## 🎯 Scenario 3: Resolution After Tension (Planned)

**File:** scenario_3_resolution.json (to be created)

**Narrative Arc:**
- **Tick 1:** Tension spike (0.60), potential Crux identified, convergence 75%
- **Tick 2:** Deliberation (0.45), Crux resolution in progress, convergence 85%
- **Tick 3:** Resolution (0.20), Crux resolved, convergence 95%

**Key Features:**
- Tension decrease: 0.60 → 0.45 → 0.20 (amber → green transition)
- Ethics improvement: deferred → examined (gaps closed)
- Crux resolution: potential → resolved
- Convergence improvement: 75% → 85% → 95%

**Use Cases:**
- Test tension de-escalation visualization
- Test Crux resolution marker
- Test ethics overlay transitions (deferred → examined)
- Test convergence meter (recovery case)
- Demonstrate productive deliberation pattern

---

## 📊 Schema Validation

All mock scenarios validate against SMV JSON schema v1.0:
- Required fields: `session_id`, `worldview_pair`, `auditors`, `ticks`
- Each tick includes: `tick_id`, `timestamp`, `nodes`, `edges`, `ethics`, `convergence`, `crux`
- Auditors locked to 3: Claude, Grok, Nova
- Tension/volume/confidence: 0.0-1.0 range
- Ethics arrays: examined, deferred, missing
- Crux status: none, potential, declared, resolved

**Validation Tool:** (to be created in Phase 1)
```bash
# Validate mock data against schema
python scripts/validate_smv_json.py docs/smv/mock_data/scenario_1_tension_escalation.json
```

---

## 🔗 Integration with Phase 1 Prototype

**How Prototype Uses Mock Data:**

1. **Load JSON:** Parse mock scenario file
2. **Initialize UI:** Render auditor triangle with tick 1 data
3. **Timeline Slider:** Enable tick navigation (1 → 2 → 3)
4. **Tension Trace:** Plot sparkline using all ticks' tension values
5. **Ethics Overlay:** Toggle display of examined/deferred/missing badges
6. **Convergence Meter:** Update progress bar per tick
7. **Crux Markers:** Flag timeline at ticks with Crux status changes

**Example Code (pseudocode):**
```javascript
const scenario = loadJSON('docs/smv/mock_data/scenario_1_tension_escalation.json');
const ticks = scenario.ticks;

// Initialize with first tick
renderTriangle(ticks[0].nodes, ticks[0].edges);
renderEthicsBadges(ticks[0].ethics);
updateConvergenceMeter(ticks[0].convergence.percentage);

// Timeline slider handler
onSliderChange(tickIndex => {
  const tick = ticks[tickIndex];
  updateTriangle(tick.nodes, tick.edges);
  updateEthicsBadges(tick.ethics);
  updateConvergenceMeter(tick.convergence.percentage);
  highlightCrux(tick.crux);
});
```

---

## 🚀 Creating New Mock Scenarios

**Template Structure:**
```json
{
  "session_id": "unique_session_id",
  "worldview_pair": "WV1_vs_WV2",
  "auditors": ["Claude", "Grok", "Nova"],
  "ticks": [
    {
      "tick_id": "tick-001",
      "timestamp": "2025-11-11T14:00:00Z",
      "nodes": [
        {"auditor": "Claude", "confidence": 0.85, "bias_overhead": 0.5, "stance": "PRO", "violation_flagged": false},
        {"auditor": "Grok", "confidence": 0.78, "bias_overhead": 0.4, "stance": "ANTI", "violation_flagged": false},
        {"auditor": "Nova", "confidence": 0.92, "bias_overhead": 0.3, "stance": "FAIRNESS", "violation_flagged": false}
      ],
      "edges": [
        {"pair": "Claude-Grok", "tension": 0.25, "volume": 0.40, "notes": "Context here"},
        {"pair": "Claude-Nova", "tension": 0.10, "volume": 0.20, "notes": "Context here"},
        {"pair": "Grok-Nova", "tension": 0.15, "volume": 0.25, "notes": "Context here"}
      ],
      "ethics": {
        "examined": ["transparency"],
        "deferred": [],
        "missing": []
      },
      "convergence": {
        "percentage": 85.0,
        "metrics_agreed": ["CA", "IP"],
        "metrics_disputed": ["BFI"]
      },
      "crux": {"status": "none"}
    }
    // Add ticks 2, 3, etc.
  ]
}
```

**Guidelines:**
- **≥3 ticks per scenario** (minimum for timeline demonstration)
- **Tension range 0.0-1.0:** 0.0-0.3 green, 0.3-0.6 amber, 0.6-1.0 red
- **Volume range 0.0-1.0:** 0.0-0.3 thin edge, 0.3-0.7 medium, 0.7-1.0 thick
- **Confidence range 0.0-1.0:** Maps to node opacity
- **Ethics arrays:** Use invariant names from AXIOMS.md (transparency, epistemic_access, stakeholder_impact)
- **Convergence:** 0-100% (target 98%+)
- **Crux lifecycle:** none → potential → declared → resolved

---

## 📝 Next Steps

**Scenario 2 + 3 Creation:**
1. Nova approves narrative arcs (see SMV_DESIGN_SPEC.md Open Questions)
2. C4 creates JSON files per approved narratives
3. Validate against schema
4. Test with Phase 1 prototype
5. Iterate based on visualization feedback

**Phase 2 Real Data:**
- Mock scenarios remain for testing/demo
- Real data files follow same schema
- Export script (Task #4 Phase 2) generates production JSON
- SMV UI seamlessly switches from mock → real data

---

**Created by:** C4 (B-STORM_6 Entry 3 - migrated from Nova's workshop draft)
**Date:** 2025-11-11
**Status:** Scenario 1 complete, Scenarios 2-3 awaiting Nova approval
**Next Steps:** Create scenarios 2-3 per Nova's guidance, validate all against schema

**Mock Data: Where synthetic narratives validate real insights.** 🧪📊
