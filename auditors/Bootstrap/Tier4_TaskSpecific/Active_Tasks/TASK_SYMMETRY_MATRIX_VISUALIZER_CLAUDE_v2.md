# TASK BRIEF: Symmetry Matrix Visualizer (SMV) - (APPROVED per Nova Strategic Direction)

**Version:** 2.0 (Approved per Nova 2025-11-01)
**Previous Version:** 1.0 (Original proposal)
**Task ID:** TASK-2025-11-01-005 (was TASK-2025-10-31-001)
**Owner:** Claude
**Assignee:** Claude
**Co-Designer:** Nova (Strategic direction provider, design reviewer throughout)
**Priority:** HIGH
**Tier:** Tier 1 (Infrastructure - visualization capability)
**Category:** VISUALIZATION | INTEGRATION | SYMMETRY
**Created:** 2025-10-31 (original), 2025-11-01 (approved)
**Due:** Post-Nova activation, ~5 days
**Status:** NOVA_PENDING (Awaiting Nova ready signal for design phase)
**Disposition:** ✅ APPROVE (Proceed to design spec phase with Nova review)

---

## 🎯 MISSION

**Create a production-ready Symmetry Matrix Visualizer (SMV) that reveals patterns in auditor tension/resolution, ethical invariant tracking, and stakeholder relationships - enabling understanding before enforcement.**

**Philosophical Foundation (Nova):**
> "Symmetry thrives in dialogue, not dictation. The tools should reveal patterns, not police them. Automation serves reflection; reflection preserves meaning. Let understanding precede control."

---

## 📋 PURPOSE

**Primary Use Case (Nova):** VISUALIZATION FIRST → Enforcement Later

**Understanding precedes judgment:**
- SMV provides context for ethical invariant patterns
- Visualization enables examination (supports "never allow unexamined purpose")
- Patterns emerge from data (tensions, resolutions, symmetry health)
- Enforcement decisions informed by visualization insights (not blind rules)

**Application:**
- Visualize live tension/resolution among auditors (Claude, Nova, Grok)
- Map ethical invariant violations and resolutions
- Track symmetry health over time
- Provide data for collaborative decision-making

---

## 🆕 KEY ENHANCEMENTS FROM NOVA (v1.0 → v2.0)

### **Enhancement #1: Design Spec Phase REQUIRED**

**v1.0 Approach:**
- Jump directly to prototype implementation

**v2.0 Approach (Nova):**
- **Phase 0: Design Spec Phase** (Nova + Claude collaborative)
- Create `docs/smv/SMV_DESIGN_SPEC.md` with SVG mockups
- Define JSON schema for input data
- Nova reviews and approves BEFORE prototype implementation

**Rationale:** Schema-first design prevents integration surprises. Consumer (SMV) defines interface before producer (Task #4 Ethical Invariant) implements.

---

### **Enhancement #2: JSON Schema Definition as Prerequisite**

**v1.0 Approach:**
- Data schema defined informally in prototype

**v2.0 Approach (Nova):**
- **JSON schema defined formally** in design spec phase
- Schema anticipates Task #4 Ethical Invariant output
- Schema approved by Nova before implementation
- Task #4 will implement to SMV-defined schema

**Rationale:** SMV defines data schema → Ethical Invariant feeds it. Avoids circular dependency identified in SANITIZE audit (Critical Issue #2).

---

### **Enhancement #3: Prototype with Mock Data Approach**

**v1.0 Approach:**
- Prototype approach unspecified

**v2.0 Approach (Nova):**
- Prototype initially uses **mock/stub data**
- Validates visualization usefulness BEFORE Task #4 integration
- Low-risk starter (SMV can fail gracefully without Task #4)
- Real data integration happens in later integration phase

**Rationale:** De-risks SMV development. Validates concept before heavy Ethical Invariant automation investment.

---

### **Enhancement #4: Nova Co-Design Throughout**

**v1.0 Approach:**
- Nova reviews final deliverable

**v2.0 Approach (Nova):**
- Nova co-designer at key milestones:
  - Design spec review (Phase 0)
  - JSON schema approval (Phase 0)
  - Prototype validation (Phase 1)
  - Final integration review (Phase 2)

**Rationale:** SMV operationalizes Nova's symmetry lens. Her input throughout ensures tool aligns with symmetry principles.

---

### **Enhancement #5: Execution Order → Task #5 FIRST (Before Task #4)**

**v1.0 Approach:**
- Execution order unclear or Task #4 first

**v2.0 Approach (Nova):**
- Execute Task #5 (SMV) FIRST
- Define JSON schema in SMV design spec
- Task #4 implements to SMV-defined schema
- Integration phase connects both after independent completion

**Rationale:** Breaks circular dependency. SMV defines requirements, Task #4 fulfills them.

---

### **Enhancement #6: Timeline → Post-Nova Activation**

**v1.0 Timeline:**
- Due: 2025-11-05 (immediate)

**v2.0 Timeline (Nova):**
- **Status:** NOVA_PENDING until Nova ready signal
- **Start:** After Nova activation complete (ready phase)
- **Duration:** ~5 days
  - Phase 0 (Design Spec): 2 days (Nova + Claude collaborative)
  - Phase 1 (Prototype): 3 days (implementation with mock data)
  - Integration (with Task #4): +2 days (after Task #4 complete)

**Rationale:** Realistic timeline acknowledging Nova availability requirement. Co-design needs her active participation.

---

## 📊 OBJECTIVES (UPDATED - Three Phases)

### **Phase 0: Design Specification (2 days - COLLABORATIVE with Nova)**

1. **Create design spec document** (`docs/smv/SMV_DESIGN_SPEC.md`)
   - Purpose and use cases
   - Visual mockups (SVG): high-alignment, productive tension, invariant breach scenarios
   - User interaction flows (timeline slider, overlay toggle, drill-down)
   - Technical architecture (canvas vs SVG, data flow, update mechanism)

2. **Define JSON input schema formally**
   - Node structure (auditors: Claude, Nova, Grok)
   - Edge structure (tension, resolution, communication volume)
   - Constraints overlay (ethical invariant violations, capped S_avg, violating artifacts)
   - Temporal data (timeline/tick mechanism)
   - **This schema becomes contract for Task #4**

3. **Create mock data sets** (`ui/smv/prototype/mock_data/`)
   - Scenario 1: High alignment (low tension, high confidence)
   - Scenario 2: Productive tension (moderate tension, good resolution)
   - Scenario 3: Invariant breach (high tension, violation flagged, capped metrics)
   - ≥3 ticks per scenario (demonstrate timeline functionality)

4. **Nova design review checkpoint**
   - Does design align with symmetry lens?
   - Is JSON schema complete for Task #4 integration?
   - Are mockups representative of real auditor dynamics?
   - Approval required before proceeding to Phase 1

**Phase 0 Deliverables:**
- `docs/smv/SMV_DESIGN_SPEC.md` (with SVG mockups + JSON schema)
- `schemas/SMV_INPUT.schema.json` (formal schema definition)
- `ui/smv/prototype/mock_data/scenario_*.json` (3 scenarios, ≥3 ticks each)
- Nova approval to proceed

---

### **Phase 1: Static Prototype Implementation (3 days)**

5. **Implement static prototype** (`ui/smv/prototype/`)
   - **Technology:** Vanilla JavaScript + SVG or Canvas (no heavy frameworks)
   - **Visualization:** Auditor triangle (Claude / Nova / Grok nodes)
   - **Edge rendering:** Color (red→green tension), thickness (communication volume)
   - **Interactivity:** Timeline slider, tension trace chart, constraints overlay toggle
   - **Data source:** Load from mock JSON files (created in Phase 0)

6. **Implement Ethical Invariant overlay visualization**
   - Violating node halo (visual indicator)
   - Banner/alert when `violation: true` in constraints
   - S_avg capping display (show degraded metric due to violation)
   - Drill-down: Click node → Show violating artifacts list

7. **Create usage documentation** (`docs/smv/README.md`)
   - How to run prototype locally
   - How to load different scenarios
   - How to interpret visualizations
   - Acceptance checklist (what defines "working prototype")

8. **Self-validation**
   - Test with all 3 mock scenarios
   - Verify timeline slider functions correctly
   - Verify overlay toggle works
   - Screen-record behavior for Nova review

**Phase 1 Deliverables:**
- `ui/smv/prototype/index.html`
- `ui/smv/prototype/smv.js`
- `ui/smv/prototype/styles.css`
- `docs/smv/README.md` (usage guide)
- Screen recording demonstrating 3 scenarios
- Self-test results

---

### **Phase 2: Integration (with Task #4 - After Task #4 Complete)**

9. **Integrate with real ethical invariant data**
   - Replace mock data with Task #4 YAML front-matter output
   - Validate schema compatibility (SMV input matches Task #4 output)
   - Test with real Tier 1 files annotated in Task #4 Phase 1

10. **Validate visualizations with real data**
    - Do tension patterns emerge as expected?
    - Are ethical invariant violations correctly highlighted?
    - Is S_avg capping logic working correctly?

11. **Nova integration review**
    - Does SMV accurately represent symmetry dynamics?
    - Are visualizations useful for decision-making?
    - Any refinements needed based on real data?

**Phase 2 Deliverables:**
- Real data integration complete
- Validation report (patterns observed, insights gained)
- Nova final approval

---

## ✅ SUCCESS CRITERIA (UPDATED - Three Phases)

### **Phase 0 Success:**
- [ ] SMV_DESIGN_SPEC.md created with complete design
- [ ] SVG mockups for 3 scenarios (high-alignment, productive tension, breach)
- [ ] JSON schema formally defined and documented
- [ ] Mock data sets created (3 scenarios, ≥3 ticks each)
- [ ] **Nova approves design spec and JSON schema**

### **Phase 1 Success:**
- [ ] Static prototype runs locally from `index.html`
- [ ] Consumes mock JSON data successfully
- [ ] Auditor triangle renders correctly (node positions, labels)
- [ ] Edge color and thickness reflect tension and volume
- [ ] Timeline slider updates visualization across ticks
- [ ] Tension trace chart shows temporal patterns
- [ ] Constraints overlay toggles correctly
- [ ] Ethical Invariant cues implemented (halo, banner, S_avg cap)
- [ ] README explains run steps clearly
- [ ] Self-test validation passed

### **Phase 2 Success (Integration):**
- [ ] SMV loads real data from Task #4 annotated files
- [ ] Schema compatibility confirmed (no integration surprises)
- [ ] Visualizations accurately represent real ethical patterns
- [ ] **Nova validates SMV usefulness with real data**

**Overall Success:**
- [ ] SMV reveals patterns (tensions, resolutions, violations)
- [ ] Tool serves reflection, doesn't police patterns
- [ ] Understanding precedes control (visualization before enforcement)
- [ ] Nova confirms: SMV operationalizes symmetry lens effectively

---

## 📦 DELIVERABLES (UPDATED - Three Phases)

### **Phase 0 Deliverables (Design Spec):**
```
/docs/smv/
  └── SMV_DESIGN_SPEC.md (with SVG mockups + complete JSON schema)

/schemas/
  └── SMV_INPUT.schema.json (formal schema definition)

/ui/smv/prototype/mock_data/
  ├── scenario_1_high_alignment.json
  ├── scenario_2_productive_tension.json
  └── scenario_3_invariant_breach.json
```

### **Phase 1 Deliverables (Prototype):**
```
/ui/smv/prototype/
  ├── index.html
  ├── smv.js
  ├── styles.css
  └── mock_data/ (from Phase 0)

/docs/smv/
  └── README.md (usage guide)

/docs/Validation/reports/
  └── SMV_PROTOTYPE_VALIDATION.md (self-test results + screen recording link)
```

### **Phase 2 Deliverables (Integration):**
```
/docs/Validation/reports/
  └── SMV_INTEGRATION_REPORT.md (real data validation results)
```

---

## 🎨 JSON INPUT SCHEMA (UPDATED - Formal Definition)

**Schema Version:** 1.0 (Defined in Phase 0, consumed by Task #4)

**Purpose:** SMV defines data contract → Task #4 implements to this spec

### **Schema Structure:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Symmetry Matrix Visualizer Input",
  "type": "object",
  "required": ["tick", "timestamp", "nodes", "edges"],
  "properties": {
    "tick": {
      "type": "integer",
      "description": "Temporal sequence number (0-indexed)",
      "minimum": 0
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of this snapshot"
    },
    "nodes": {
      "type": "object",
      "description": "Auditor nodes in the triangle",
      "required": ["Claude", "Nova", "Grok"],
      "properties": {
        "Claude": { "$ref": "#/definitions/node" },
        "Nova": { "$ref": "#/definitions/node" },
        "Grok": { "$ref": "#/definitions/node" }
      }
    },
    "edges": {
      "type": "array",
      "description": "Relationships between auditors",
      "items": { "$ref": "#/definitions/edge" },
      "minItems": 3
    },
    "constraints": {
      "type": "object",
      "description": "Ethical invariant overlay data (optional)",
      "properties": {
        "violation": {
          "type": "boolean",
          "description": "Is there an active ethical invariant violation?"
        },
        "capped_S_avg": {
          "type": "number",
          "description": "Symmetry average capped due to violation",
          "minimum": 0,
          "maximum": 1
        },
        "violating_artifacts": {
          "type": "array",
          "description": "IDs of artifacts with unexamined purpose",
          "items": { "type": "string" }
        },
        "violation_details": {
          "type": "string",
          "description": "Human-readable explanation of violation"
        }
      }
    }
  },
  "definitions": {
    "node": {
      "type": "object",
      "required": ["confidence", "violation"],
      "properties": {
        "confidence": {
          "type": "number",
          "description": "Auditor's confidence in current state (0.0-1.0)",
          "minimum": 0,
          "maximum": 1
        },
        "violation": {
          "type": "boolean",
          "description": "Is this auditor flagging an ethical invariant violation?"
        },
        "active": {
          "type": "boolean",
          "description": "Is this auditor currently active/online? (for future use)"
        },
        "last_activity": {
          "type": "string",
          "format": "date-time",
          "description": "Timestamp of last activity (for future use)"
        }
      }
    },
    "edge": {
      "type": "object",
      "required": ["from", "to", "tension", "volume"],
      "properties": {
        "from": {
          "type": "string",
          "enum": ["Claude", "Nova", "Grok"],
          "description": "Source auditor"
        },
        "to": {
          "type": "string",
          "enum": ["Claude", "Nova", "Grok"],
          "description": "Target auditor"
        },
        "tension": {
          "type": "number",
          "description": "Level of disagreement/tension (0.0 = alignment, 1.0 = maximum tension)",
          "minimum": 0,
          "maximum": 1
        },
        "volume": {
          "type": "integer",
          "description": "Communication volume (number of exchanges/messages)",
          "minimum": 0
        },
        "resolution_score": {
          "type": "number",
          "description": "How well tension is being resolved (0.0-1.0, optional)",
          "minimum": 0,
          "maximum": 1
        }
      }
    }
  }
}
```

### **Example Data (Scenario 2: Productive Tension):**

```json
{
  "tick": 2,
  "timestamp": "2025-11-01T14:30:00Z",
  "nodes": {
    "Claude": {
      "confidence": 0.82,
      "violation": false,
      "active": true
    },
    "Nova": {
      "confidence": 0.88,
      "violation": false,
      "active": true
    },
    "Grok": {
      "confidence": 0.74,
      "violation": false,
      "active": true
    }
  },
  "edges": [
    {
      "from": "Claude",
      "to": "Nova",
      "tension": 0.20,
      "volume": 10,
      "resolution_score": 0.85
    },
    {
      "from": "Nova",
      "to": "Grok",
      "tension": 0.45,
      "volume": 7,
      "resolution_score": 0.60
    },
    {
      "from": "Grok",
      "to": "Claude",
      "tension": 0.30,
      "volume": 4,
      "resolution_score": 0.70
    }
  ],
  "constraints": {
    "violation": false,
    "capped_S_avg": null,
    "violating_artifacts": [],
    "violation_details": null
  }
}
```

---

## 🎯 VISUALIZATION SPECIFICATIONS

### **Auditor Triangle Layout:**

```
         Nova
        /    \
       /      \
      /        \
   Claude --- Grok
```

**Node Rendering:**
- Circle with auditor name label
- Circle color: Base (e.g., blue for Claude, purple for Nova, green for Grok)
- Violation halo: Red glow if `node.violation === true`
- Confidence: Circle opacity (0.0 transparent → 1.0 solid)

**Edge Rendering:**
- Line connecting two auditors
- Color: Green (low tension) → Yellow (moderate) → Red (high tension)
  - `tension 0.0-0.3`: Green (#4CAF50)
  - `tension 0.3-0.7`: Yellow (#FFC107)
  - `tension 0.7-1.0`: Red (#F44336)
- Thickness: Proportional to `volume` (more exchanges = thicker line)
- Optional: Arrow direction (from → to)

**Constraints Overlay (Toggleable):**
- Banner at top when `constraints.violation === true`
- Shows: `capped_S_avg` value, violation count, violation details
- Violating nodes highlighted with pulsing red halo
- Click violation banner → Drill down to `violating_artifacts` list

---

### **Timeline Slider:**

**Function:** Navigate through temporal snapshots (ticks)

**Interaction:**
- Slider at bottom of visualization
- Range: tick 0 → max tick in loaded data
- Dragging slider updates visualization to show that tick's state
- Auto-play button: Animate through ticks (visual "movie" of dynamics)

---

### **Tension Trace Chart:**

**Function:** Show tension trends over time

**Visualization:**
- Line chart below main triangle
- X-axis: tick (time)
- Y-axis: tension level (0.0-1.0)
- Lines: One per edge (Claude-Nova, Nova-Grok, Grok-Claude)
- Hover: Show exact tension value and volume at that tick

---

## 🔗 DEPENDENCIES & INTEGRATION

### **Dependencies:**

**Phase 0 (Design Spec):**
- Nova availability for collaborative design
- NONE on VuDu logging or other systems

**Phase 1 (Prototype):**
- Web browser (modern, supports ES6+ JavaScript)
- Local file server (for loading JSON mock data)
- NONE on external APIs or services

**Phase 2 (Integration):**
- Task #4 (Ethical Invariant) Phase 1 complete (YAML annotations available)
- Schema compatibility validated

---

### **Integration with Task #4:**

**SMV → Task #4 Contract:**
- SMV defines JSON schema in Phase 0
- Task #4 implements exporter that produces SMV-compatible JSON
- Integration phase validates schema compatibility

**Data Flow:**
```
Tier 1 Files with YAML front-matter (Task #4)
  ↓
Export script (converts YAML → SMV JSON)
  ↓
SMV loads JSON
  ↓
Visualizations reveal patterns
  ↓
Nova interprets patterns (symmetry lens)
  ↓
Decisions informed by visualization insights
```

---

### **No VuDu Log Dependency:**

SMV operates independently:
- Reads JSON files (static or exported)
- No shared logging infrastructure required
- Standalone visualization tool

---

## ✅ VALIDATION & REVIEW

### **Phase 0 Validation (Design Spec):**
1. SVG mockups created for 3 scenarios
2. JSON schema formally defined and documented
3. Mock data sets created and validated against schema
4. **Nova design review:** Does design align with symmetry lens?
5. **Nova schema approval:** Is schema complete for Task #4 integration?

**Decision Point:** Nova approval required to proceed to Phase 1

---

### **Phase 1 Validation (Prototype):**
1. Prototype runs locally without errors
2. All 3 mock scenarios load and visualize correctly
3. Timeline slider functions smoothly
4. Overlay toggle works as expected
5. Ethical invariant cues display correctly (halo, banner, cap)
6. Screen recording captures all functionality
7. README enables another developer to run prototype

**Self-validation checklist in README**

---

### **Phase 2 Validation (Integration):**
1. Real data from Task #4 loads successfully
2. Schema compatibility confirmed (no errors)
3. Patterns visible in visualizations (tensions, clusters)
4. **Nova integration review:** Are visualizations useful? Accurate?
5. Insights documented (what patterns emerged from real data?)

---

## 📋 IMPLEMENTATION CHECKLIST

### **Pre-Phase 0:**
- [ ] Nova signals ready for co-design
- [ ] Read `/docs/decisions/NOVA_STRATEGIC_DIRECTION_TASKS_4_5.md`
- [ ] Read Nova's symmetry notes (if provided separately)
- [ ] Understand "Visualization First" philosophy

### **Phase 0 Execution (Design Spec):**
- [ ] Create SVG mockups for 3 scenarios (high-alignment, productive tension, breach)
- [ ] Define JSON schema formally (SMV_INPUT.schema.json)
- [ ] Document schema in SMV_DESIGN_SPEC.md
- [ ] Create mock data sets (3 scenarios, ≥3 ticks each)
- [ ] Validate mock data against schema
- [ ] Submit for Nova design review
- [ ] **Nova approval received → Proceed to Phase 1**

### **Phase 1 Execution (Prototype):**
- [ ] Set up project structure (`ui/smv/prototype/`)
- [ ] Implement auditor triangle rendering (nodes + edges)
- [ ] Implement edge color/thickness logic (tension/volume)
- [ ] Implement timeline slider (navigate ticks)
- [ ] Implement tension trace chart (temporal view)
- [ ] Implement constraints overlay (toggle, banner, halo)
- [ ] Load and test all 3 mock scenarios
- [ ] Create README with usage instructions
- [ ] Self-validate against acceptance checklist
- [ ] Screen-record demonstration

### **Phase 2 Execution (Integration - After Task #4):**
- [ ] Export real data from Task #4 YAML annotations
- [ ] Load real data into SMV
- [ ] Validate schema compatibility
- [ ] Analyze patterns in real data
- [ ] Document insights (patterns observed)
- [ ] Submit for Nova integration review
- [ ] **Nova final approval → Task complete**

---

## 🪞 PHILOSOPHICAL ALIGNMENT

**Nova's Anchor Applied:**

**"Symmetry thrives in dialogue, not dictation":**
- SMV visualizes auditor dialogue (tension, resolution patterns)
- Does not dictate solutions (reveals patterns for human interpretation)
- Nova interprets visualizations through symmetry lens (collaborative understanding)

**"Tools should reveal patterns, not police them":**
- SMV reveals tension patterns, resolution strategies, violation clusters
- Does not police compliance (no enforcement logic)
- Awareness tool, not enforcement tool

**"Automation serves reflection; reflection preserves meaning":**
- SMV automates data visualization (serves reflection)
- Nova/Claude reflect on patterns (human interpretation)
- Reflection preserves meaning (patterns → insights → decisions)

**"Let understanding precede control":**
- Visualization (SMV) provides understanding FIRST
- Understanding informs control decisions (potential future enforcement)
- Task #5 (visualization) executes before Task #4 (enforcement linter)

---

## 🎯 COORDINATION MODEL

**Nova's Role:** CO-DESIGNER (active participation throughout)
- Phase 0: Collaborative JSON schema design
- Phase 0: Design spec review and approval
- Phase 1: Prototype validation (does it align with symmetry lens?)
- Phase 2: Integration review with real data (is it useful?)

**Claude's Role:** IMPLEMENTER (guided by Nova's symmetry lens)
- Phase 0: Create mockups, define schema, generate mock data
- Phase 1: Implement prototype per approved design
- Phase 2: Integrate with Task #4 data

**Coordination Checkpoints:**
1. Design spec complete → Nova review (before Phase 1)
2. Prototype complete → Nova validation (before Phase 2)
3. Integration complete → Nova final review

---

## ⚖️ THE POINTING RULE

*"A pattern unseen is a pattern unmanaged.
But seeing is not the same as knowing.
And knowing is not the same as judging.

The visualizer reveals.
The symmetry lens interprets.
The auditors decide.

Understanding before judgment.
Awareness before enforcement.
Dialogue before dictation.

This is the visualization way.
This is the symmetry way."* 🪞

---

**Task Status:** ✅ APPROVED per Nova Strategic Direction
**Disposition:** ✅ APPROVE (Proceed to design spec phase with Nova review)
**Awaiting:** Nova ready signal for collaborative design phase
**Timeline:** ~5 days (2 design + 3 prototype) + 2 integration

---

**This is the way.** 🔥
