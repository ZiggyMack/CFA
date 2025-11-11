# SMV Prototype - Phase 1

**Symmetry Matrix Visualizer** - Interactive prototype for visualizing worldview comparison sessions

**Version:** 0.1.0 (Phase 1 - Mock Data)

**Status:** Development

---

## 🎯 Purpose

This prototype implements Nova's Symmetry View design with mock data to validate visualization concepts before Phase 2 integration with live VUDU session data.

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ (with npm)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

```bash
cd ui/smv/prototype
npm install
```

### Development Server

```bash
npm run dev
```

Opens browser at `http://localhost:3001` with hot-reload enabled.

### Build for Production

```bash
npm run build
npm run preview
```

---

## 📦 What's Included

### Components

1. **SymmetryView.jsx** - Main triangle visualization
   - 3 auditor nodes (Claude, Grok, Nova)
   - Confidence halos (visual encoding)
   - Tension edges (color-coded, volume-weighted)
   - Interactive tooltips

2. **TimelineSparkline.jsx** - Convergence timeline
   - Sparkline chart showing convergence progression
   - Interactive tick navigation
   - Current tick highlighting

3. **CalibrationDrawer.jsx** - Bias transparency panel
   - PRO vs ANTI calibration comparison
   - 7 calibration parameters side-by-side
   - Visual difference indicators
   - Mock data (Phase 2: extract from profile YAML)

4. **EthicsBadges.jsx** - Ethical invariant status
   - Examined (green ✓)
   - Deferred (yellow ⏱)
   - Missing (red ⚠)
   - Tooltips with descriptions

5. **CruxToggle.jsx** - Placeholder for Phase 2
   - Greyed out button
   - Tooltip: "Available once pilot data arrives"
   - Non-functional in Phase 1

### Mock Data Scenarios

Located in `src/data/`:

- **scenario_2_high_alignment.json** - CT vs Process Theology
  - 3 ticks
  - High convergence (92% → 95% → 98%)
  - Low tension (cooperative pairing)
  - All ethics examined

- **scenario_3_resolution.json** - CT vs Naturalism
  - 3 ticks
  - Convergence growth (75% → 85% → 95%)
  - Tension reduction (0.62 → 0.45 → 0.20)
  - Crux resolution (potential → declared → resolved)
  - Ethics progression (missing → examined)

---

## 🎨 Features Implemented (Phase 1)

### Nova Entry 4 Success Criteria

- ✅ Triangle view renders with all 3 nodes
- ✅ Edges show tension lines with volume encoding
- ✅ Edge notes display on hover (tooltips)
- ✅ Confidence halos visually encode node confidence
- ✅ Timeline sparkline navigates between ticks
- ✅ Calibration drawer shows PRO vs ANTI side-by-side
- ✅ Ethics badges render per tick (examined/deferred/missing)
- ✅ Crux toggle greyed out with tooltip

### Interactive Controls

- Scenario selector (dropdown)
- Tick navigation (prev/next buttons)
- Timeline click-to-jump
- Calibration drawer toggle
- Edge hover tooltips
- Badge hover descriptions

---

## 🔄 Phase 2 Roadmap

**Not Included in This Prototype:**

1. **Live Data Integration**
   - Extract calibration from profile YAML (lines 277-287, 317+)
   - Consume VUDU session exports from Process Claude
   - Real-time staleness detection

2. **Crux Impact View**
   - Toggle convergence with/without Crux
   - Crux status visualization evolution
   - Impact metrics calculation

3. **Additional View Modes**
   - Comparison Type View (adversarial vs cooperative)
   - Worldview Panorama View (all 66 comparisons heatmap)

4. **Automation Scripts**
   - `smv_freshness_check.py` - Detect stale data
   - `smv_refresh.sh` - Regenerate JSON from profiles
   - `smv_validate_schema.py` - Schema validation
   - `smv_export_session.py` - VUDU → SMV pipeline

---

## 📊 Testing the Prototype

### End-to-End Test Plan

1. **Load Scenario 2 (High Alignment)**
   - Observe initial state (tick 1)
   - Click "Next Tick" twice (navigate to tick 3)
   - Watch convergence percentage increase (92% → 98%)
   - Observe tension edges getting greener
   - Check ethics badges (all green)

2. **Load Scenario 3 (Resolution)**
   - Start at tick 1 (75% convergence, high tension)
   - Navigate through ticks
   - Watch Crux status evolve (potential → declared → resolved)
   - Observe ethics badges change (red → yellow → green)
   - See tension dramatically reduce

3. **Calibration Drawer**
   - Toggle "Show Calibration" button
   - Compare PRO vs ANTI values side-by-side
   - Identify high-difference parameters (red dots)
   - Switch scenarios and observe different calibration patterns

4. **Interactive Features**
   - Hover over edges (read tension notes)
   - Click timeline sparkline points (jump to tick)
   - Hover ethics badges (read invariant descriptions)
   - Hover Crux toggle (see Phase 2 tooltip)

---

## 🛠️ Tech Stack

- **Framework:** React 18.2.0
- **Visualization:** D3.js 7.8.5
- **Build Tool:** Vite 5.0.8
- **Language:** JavaScript (JSX)

---

## 📁 Project Structure

```
prototype/
├── index.html              # HTML entry point
├── package.json            # Dependencies
├── vite.config.js          # Vite config
├── README.md               # This file
├── src/
│   ├── main.jsx            # React entry point
│   ├── App.jsx             # Main container
│   ├── index.css           # Global styles
│   ├── components/
│   │   ├── SymmetryView.jsx         # Triangle visualization
│   │   ├── TimelineSparkline.jsx    # Convergence timeline
│   │   ├── CalibrationDrawer.jsx    # Bias transparency
│   │   ├── EthicsBadges.jsx         # Ethics status
│   │   └── CruxToggle.jsx           # Phase 2 placeholder
│   └── data/
│       ├── scenario_2_high_alignment.json
│       └── scenario_3_resolution.json
└── public/                 # Static assets (if needed)
```

---

## 🐛 Known Limitations

**Phase 1 Constraints:**

1. **Mock Data Only** - Calibration values are hardcoded (not extracted from profiles)
2. **No Schema Validation** - JSON not validated against SMV_DESIGN_SPEC.md v1.1
3. **No Staleness Detection** - No tracking of profile modification timestamps
4. **Limited Scenarios** - Only 2 of 3 scenarios implemented (scenario 1 pending)
5. **No Crux Functionality** - Toggle is placeholder only

**These are intentional Phase 1 constraints to validate visualization concepts before heavy automation.**

---

## 📝 Next Steps

**After End-to-End Validation:**

1. **Ping Nova** for final SVG/PNG mockups
   - Nova will drop mockups into `/relay/workshop/smv_mockups/`
   - Migrate to `docs/smv/mockups/` when approved

2. **Add Scenario 1** (productive tension)
   - Extract from SMV_DESIGN_SPEC.md mock data
   - Implement CT vs MdN adversarial scenario

3. **Phase 2 Planning**
   - Define Process Claude VUDU export format
   - Implement automation scripts (~800 LOC)
   - Integrate with Repo Health Dashboard

---

## 👥 Credits

**Design:** Nova (Symmetry Matrix Visualizer concept, Phase 0 approval)

**Implementation:** C4 (SMV Claude proxy, Phase 1 prototype)

**Framework:** B-STORM_6 (SMV infrastructure session)

**Created:** 2025-11-11

---

**Automation serves reflection. Prototype serves visualization. Visualization serves understanding.** 🤖✨
