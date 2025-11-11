<!---
FILE: MATRIX_PROTOTYPE_NOTES.md
PURPOSE: Running notes for SMV prototype work (mock data tests, UI behaviors)
STATUS: Draft (workshop)
OWNER: Nova
CREATED: 2025-11-11
LAST_UPDATE: 2025-11-11 [Scaffold created]
--->

# SMV Prototype Notes (Workshop)

Use this file to track experiments, rendering issues, and open questions while Phase 1 is underway. Once the prototype stabilizes we can migrate the relevant content into `ui/smv/README.md`.

## Initial TODOs

- [ ] Set up local viewer (React D3 or static HTML) for triangle + timeline demos
- [ ] Import `MATRIX_MOCK_DATA.json` and confirm schema validation
- [ ] Implement color scale utility (green ? amber ? red)
- [ ] Prototype tension sparkline component
- [ ] Prototype ethics badge overlay (examined/deferred/missing)

## Open Questions

1. Should we animate edge-width transitions or keep them discrete per tick?
2. Do we need a fourth auditor placeholder for future sessions (e.g., Shaman involvement), or keep schema locked to 3 nodes for now?
3. How do we display simultaneous Crux IDs if multiple metrics trigger at the same tick?

Add notes below as we test pieces of the UI.

---

## Build Session Log

### Session 1: Scaffolding (2025-11-11)

**Status:** ✅ Complete

**Tasks Completed:**

1. **Directory Structure Created**
   ```
   ui/smv/prototype/
   ├── index.html
   ├── package.json
   ├── vite.config.js
   ├── src/
   │   ├── components/
   │   ├── data/
   │   │   ├── scenario_2_high_alignment.json
   │   │   └── scenario_3_resolution.json
   │   └── (pending: main.jsx, App.jsx, components)
   └── public/
   ```

2. **Framework Selection:**
   - ✅ React 18.2.0
   - ✅ D3 7.8.5 (d3-scale, d3-shape, d3-selection, d3-transition)
   - ✅ Vite 5.0.8 (dev server)

3. **Mock Data Integration:**
   - ✅ Copied scenario_2_high_alignment.json (CT vs Process Theology, 3 ticks, high alignment)
   - ✅ Copied scenario_3_resolution.json (CT vs Naturalism, 3 ticks, Crux resolution)

4. **Hashes Verified (per Nova Entry 4):**
   - Scenario 2: `C01610D7B7A30E4D...` ✅
   - Scenario 3: `DB99258B5F6B1844...` ✅

**Next Steps:** Implement React components starting with App.jsx and SymmetryView.jsx

---

### Session 2: Core Components Implementation (2025-11-11)

**Status:** ✅ Complete

**Components Created:**

1. **App.jsx** - Main container
   - Scenario selector (dropdown: scenario 2, scenario 3)
   - Tick navigation (prev/next buttons, tick counter)
   - Calibration drawer toggle
   - Crux toggle placeholder
   - Layout management

2. **SymmetryView.jsx** - Triangle visualization with D3
   - Equilateral triangle positioning (3 nodes)
   - Confidence halos (radius scales with confidence)
   - Tension edges (color: green → yellow → red, width scales with volume)
   - Interactive tooltips (edge notes on hover)
   - Node labels (auditor name, confidence %, stance)

3. **TimelineSparkline.jsx** - Convergence timeline
   - D3 line chart (convergence % over ticks)
   - Area fill under curve
   - Interactive points (click to jump to tick)
   - Current tick highlighting (orange dot)
   - X-axis labels (T1, T2, T3)

4. **EthicsBadges.jsx** - Ethics status display
   - Examined badges (green ✓)
   - Deferred badges (yellow ⏱)
   - Missing badges (red ⚠)
   - Hover tooltips with descriptions
   - Dynamic badge rendering

5. **CalibrationDrawer.jsx** - Bias transparency panel
   - PRO vs ANTI side-by-side comparison
   - 7 calibration parameters with visual bars
   - Difference indicators (red/yellow/green dots)
   - Mock data for CT vs Process Theology and CT vs Naturalism
   - Phase 2 note (will extract from profile YAML)

6. **CruxToggle.jsx** - Phase 2 placeholder
   - Greyed out button (disabled state)
   - Hover tooltip explaining Phase 2 availability
   - Visual placeholder for future Crux Impact View

**Supporting Files:**

- `main.jsx` - React entry point
- `index.css` - Global styles (dark theme, badge styles, tooltip styles)
- `README.md` - Comprehensive documentation with quick start, features, testing plan

**Files Created:** 10 new files (~1,200 lines total)

**Next Steps:** Local testing (user will run `npm install && npm run dev`)

---

### Session 3: End-to-End Testing (Pending User Execution)

**Status:** ⏳ Ready for User Testing

**Test Scenarios:**

1. **Scenario 2 (High Alignment)**
   - Load scenario → navigate 3 ticks → observe smooth convergence
   - Check ethics badges (all green)
   - Toggle calibration drawer → compare PRO vs ANTI
   - Hover edges → read tension notes

2. **Scenario 3 (Resolution)**
   - Load scenario → navigate 3 ticks → observe Crux resolution
   - Watch ethics badges evolve (red → yellow → green)
   - See tension reduction (0.62 → 0.20)
   - Verify Crux status display

3. **Interactive Features**
   - Sparkline click-to-jump
   - Edge hover tooltips
   - Badge hover descriptions
   - Crux toggle tooltip

**Success Criteria (Nova Entry 4):**

- ✅ Triangle view renders with all 3 nodes
- ✅ Edges show tension lines with volume encoding
- ✅ Edge notes display on hover (tooltips)
- ✅ Confidence halos visually encode node confidence
- ✅ Timeline sparkline navigates between ticks
- ✅ Calibration drawer shows PRO vs ANTI side-by-side
- ✅ Ethics badges render per tick (examined/deferred/missing)
- ✅ Crux toggle greyed out with tooltip

**All 8 criteria implemented. Ready to ping Nova after user validates end-to-end rendering.**

---
