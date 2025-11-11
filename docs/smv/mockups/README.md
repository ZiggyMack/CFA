<!---
FILE: README.md
PURPOSE: Documentation for SMV SVG mockups (visual prototypes for Phase 1 UI implementation)
VERSION: 1.0.0
STATUS: Planned (awaiting Phase 0 mockup creation)
DEPENDS_ON: docs/smv/SMV_DESIGN_SPEC.md
NEEDED_BY: SMV Phase 1 prototype implementation
MOVES_WITH: /docs/smv/mockups/
CREATED: 2025-11-11 (B-STORM_6 Entry 3)
LAST_UPDATE: 2025-11-11 [Placeholder structure created]
--->

# SMV SVG Mockups

**Purpose:** Visual prototypes (SVG format) demonstrating SMV visualization goals for Phase 1 prototype implementation

**Status:** Planned (awaiting mockup creation in Phase 0)

---

## 📋 Mockup Overview

| Mockup | File | Status | Purpose |
|--------|------|--------|---------|
| **Scenario A: High Alignment** | scenario_A_high_alignment.svg | ⏳ Planned | Green triangle, flat sparkline, all ethics examined |
| **Scenario B: Constructive Tension** | scenario_B_constructive_tension.svg | ⏳ Planned | Amber edges, oscillating sparkline, ethics in progress |
| **Scenario C: Invariant Breach** | scenario_C_invariant_breach.svg | ⏳ Planned | Red alert, tension spike, Crux marker, ethics missing |

---

## 🎨 Mockup Specifications

### **Scenario A: High Alignment**

**Visual Elements:**
- **Auditor Triangle:**
  - 3 nodes (Claude/Grok/Nova) in equilateral triangle
  - All edges thin & green (low tension)
  - Nodes at full opacity (high confidence)
  - No halos (no violations)

- **Timeline:**
  - Horizontal slider at bottom
  - 3 tick markers evenly spaced
  - Current tick highlighted

- **Sparkline Chart:**
  - Flat lines (low variance)
  - Green color throughout
  - Y-axis: 0.0-1.0 tension scale

- **Ethics Overlay:**
  - 3 green checkmarks (examined: transparency, epistemic_access, stakeholder_impact)
  - 0 yellow pause icons (deferred: none)
  - 0 red X icons (missing: none)

- **Convergence Meter:**
  - Progress bar at 98% (green fill)
  - Label: "98% convergence - Target achieved"

---

### **Scenario B: Constructive Tension**

**Visual Elements:**
- **Auditor Triangle:**
  - Claude↔Grok edge: Thicker & amber (moderate tension)
  - Other edges: Thin & green (low tension)
  - Nodes: Varying opacity (confidence 0.78-0.85)
  - No halos (productive tension, no violations)

- **Timeline:**
  - 3 tick markers
  - Middle tick highlighted (peak tension)

- **Sparkline Chart:**
  - Oscillating lines (up at tick 2, down at tick 3)
  - Amber color for Claude-Grok line
  - Green for other pairs

- **Ethics Overlay:**
  - 1 green checkmark (examined: transparency)
  - 1 yellow pause icon (deferred: epistemic_access)
  - 0 red X (missing: none yet)

- **Convergence Meter:**
  - Progress bar at 90% (amber fill)
  - Label: "90% convergence - In progress"

---

### **Scenario C: Invariant Breach**

**Visual Elements:**
- **Auditor Triangle:**
  - Claude↔Grok edge: Thick & red (high tension)
  - Nova node: Red pulsing halo (violation flagged)
  - Other edges: Amber (elevated tension)

- **Timeline:**
  - 3 tick markers
  - Tick 3 has red Crux marker
  - Annotation bubble: "CRUX_BFI_001 declared"

- **Sparkline Chart:**
  - Sharp upward spike at tick 3
  - Red color for Claude-Grok line at peak
  - Vertical red line at Crux declaration

- **Ethics Overlay:**
  - 1 green checkmark (examined: transparency)
  - 0 yellow pause icons
  - 2 red X icons (missing: epistemic_access, stakeholder_impact)

- **Convergence Meter:**
  - Progress bar at 75% (red fill)
  - Label: "75% convergence - Crux blocking progress"
  - Blinking indicator (stalled state)

---

## 🎨 Design Specifications

**Color Palette:**
- **Green (Harmony):** #4CAF50
- **Amber (Tension):** #FFC107
- **Red (High Tension):** #F44336
- **Blue (Claude):** #2196F3
- **Purple (Nova):** #9C27B0
- **Green (Grok):** #4CAF50
- **Gray (UI Elements):** #757575

**Typography:**
- **Labels:** 12pt sans-serif
- **Node Names:** 14pt bold
- **Metrics:** 10pt monospace

**Layout:**
- **Canvas Size:** 1200px × 800px
- **Triangle Center:** 600px × 300px
- **Node Radius:** 60px
- **Edge Min Width:** 2px
- **Edge Max Width:** 10px
- **Timeline Height:** 100px (at bottom)
- **Sparkline Height:** 80px (bottom-right)
- **Ethics Overlay:** Top-right corner (200px × 150px)
- **Convergence Meter:** Top-left corner (200px × 40px)

---

## 📐 SVG Template Structure

```xml
<svg width="1200" height="800" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="1200" height="800" fill="#f5f5f5"/>

  <!-- Convergence Meter (top-left) -->
  <g id="convergence-meter" transform="translate(20, 20)">
    <!-- Progress bar, label -->
  </g>

  <!-- Ethics Overlay (top-right) -->
  <g id="ethics-overlay" transform="translate(980, 20)">
    <!-- Badge icons, counts -->
  </g>

  <!-- Auditor Triangle (center) -->
  <g id="auditor-triangle" transform="translate(600, 300)">
    <!-- Edges -->
    <line id="claude-grok-edge" ... />
    <line id="claude-nova-edge" ... />
    <line id="grok-nova-edge" ... />

    <!-- Nodes -->
    <circle id="claude-node" cx="0" cy="-150" r="60" fill="#2196F3" opacity="0.85"/>
    <text x="0" y="-145" text-anchor="middle">Claude</text>
    <text x="0" y="-125" text-anchor="middle" font-size="10">~0.5 overhead</text>

    <circle id="grok-node" cx="-130" cy="75" r="60" fill="#4CAF50" opacity="0.78"/>
    <text x="-130" y="80" text-anchor="middle">Grok</text>
    <text x="-130" y="100" text-anchor="middle" font-size="10">~0.4 overhead</text>

    <circle id="nova-node" cx="130" cy="75" r="60" fill="#9C27B0" opacity="0.92"/>
    <text x="130" y="80" text-anchor="middle">Nova</text>
    <text x="130" y="100" text-anchor="middle" font-size="10">~0.3 overhead</text>
  </g>

  <!-- Timeline (bottom) -->
  <g id="timeline" transform="translate(100, 700)">
    <!-- Slider, tick markers -->
  </g>

  <!-- Sparkline (bottom-right) -->
  <g id="sparkline" transform="translate(900, 620)">
    <!-- Line chart, axes -->
  </g>
</svg>
```

---

## 🚀 Next Steps

**Mockup Creation:**
1. Nova provides specifications or rough sketches
2. C4 creates SVG files per specifications
3. Nova reviews and approves visual accuracy
4. Mockups finalized for Phase 1 prototype reference

**Alternative:** Phase 1 developer creates mockups during UI implementation (wireframe → mockup → production)

**Phase 1 Usage:**
- Prototype developer references mockups for layout/colors/interactions
- Mockups serve as visual acceptance criteria
- Actual UI may deviate slightly (responsive design, accessibility)

---

**Created by:** C4 (B-STORM_6 Entry 3 - placeholder structure)
**Date:** 2025-11-11
**Status:** Planned (awaiting mockup creation)
**Next Steps:** Nova provides mockup specifications or C4 drafts from design spec descriptions

**Mockups: Where vision becomes pixels, and pixels guide implementation.** 🎨📐
