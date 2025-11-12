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

### Session 4: User Validation Complete (2025-11-11)

**Status:** ✅ **PHASE 1 VALIDATION COMPLETE**

**Scenario 1 Added:**

Prior to user testing, added Scenario 1 (tension escalation) to achieve parity per Nova Entry 6:

- ✅ Created `scenario_1_tension_escalation.json` - CT vs MdN adversarial pairing
  - 3 ticks with declining convergence (82% → 72% → 65%)
  - Escalating tension (0.25 → 0.55 → 0.80)
  - Crux workflow (none → potential → declared)
  - Ethics degradation (3 examined → 1 examined + 1 missing → 1 examined + 2 missing)

- ✅ Updated `App.jsx` - Added scenario1 to dropdown selector
  - Set as default scenario
  - Updated worldview_pair logic for CalibrationDrawer

- ✅ Updated `CalibrationDrawer.jsx` - Added CT_vs_MdN calibration data
  - PRO stance (axiom_confidence: 0.85, burden_of_proof: 0.60)
  - ANTI stance (axiom_confidence: 0.35, burden_of_proof: 0.80)
  - Shows larger divergence for adversarial pairing

**User Test Environment:**

- Platform: WSL Ubuntu (avoided PowerShell `&&` syntax issues)
- Node.js: Successfully installed via nvm
- Browser: Modern browser (Chrome/Edge/Firefox)
- Dev Server: `npm run dev` → localhost:3001

**User Validation Results:**

**✅ All 3 Scenarios Tested:**

1. **Scenario 1 (Tension Escalation - CT vs MdN):**
   - ✅ Tick 1: 82% convergence, low tension, 3 ethics examined
   - ✅ Tick 2: 72% convergence, rising tension, 1 ethics missing (stakeholder_impact)
   - ✅ Tick 3: 65% convergence, high tension, 2 ethics missing, Crux declared (CRUX_BFI_001)
   - ✅ Tooltip display on edge hover - **User feedback:** "elegant!"
   - ✅ Sparkline click-to-jump confirmed
   - ✅ Calibration drawer with 7 parameters confirmed

2. **Scenario 2 (High Alignment - CT vs Process Theology):**
   - ✅ Tick 1: 92% convergence
   - ✅ Tick 2: 95% convergence
   - ✅ Tick 3: 98% convergence (target achieved)
   - ✅ All ethics examined (green badges)
   - ✅ Low tension (thin green edges)

3. **Scenario 3 (Resolution - CT vs Naturalism):**
   - ✅ Tick 1: 75% convergence, high tension
   - ✅ Tick 2: 85% convergence, reducing tension
   - ✅ Tick 3: 95% convergence, Crux resolved
   - ✅ Ethics progression observed (red → yellow → green badges)
   - ✅ Tension reduction visible (thick amber → thin green edges)

**✅ All Interactive Features Working:**

- ✅ Scenario selector dropdown (3 scenarios)
- ✅ Tick navigation (prev/next buttons)
- ✅ Timeline sparkline click-to-jump
- ✅ Edge hover tooltips
- ✅ Ethics badge hover descriptions
- ✅ Calibration drawer toggle
- ✅ Crux toggle placeholder with tooltip

**✅ All 8 Nova Entry 4 Success Criteria Met:**

1. ✅ Triangle view renders with all 3 nodes
2. ✅ Edges show tension lines with volume encoding
3. ✅ Edge notes display on hover (tooltips)
4. ✅ Confidence halos visually encode node confidence
5. ✅ Timeline sparkline navigates between ticks
6. ✅ Calibration drawer shows PRO vs ANTI side-by-side
7. ✅ Ethics badges render per tick (examined/deferred/missing)
8. ✅ Crux toggle greyed out with tooltip

**User Feedback:**

**Positive:**
- "OMG this is so cool!" (initial reaction)
- "elegant!" (tooltip interaction)
- All tick transitions smooth
- All visual encodings clear
- Calibration drawer comparison intuitive

**UX Improvement Suggestion:**
- Tooltip resize: Mouse pointer slightly obstructs some text characters
- **Phase 2 Polish:** Adjust tooltip offset or arrow positioning for better readability

**Screenshots Captured:**
- Scenario 1: Ticks 1-3 with tooltip demonstration
- Scenario 2: Single screenshot (convergence changes validated)
- Scenario 3: Ticks 1-3 showing Crux resolution

**Nova Entry 6 Ping Trigger Conditions Met:**

- ✅ **(a) Local rendering log captured** - Screenshots + validation notes documented
- ✅ **(b) Scenario 1 live in prototype** - scenario_1_tension_escalation.json tested and confirmed
- ✅ **(c) First 3 Tier-1 files carry front-matter** - VUDU_CFA.md, VUDU_PROTOCOL.md, WAYFINDING_GUIDE.md annotated (commit a90f56e)

**Phase 1 Status:** ✅ **COMPLETE - READY FOR NOVA ENTRY 7 PING**

**Next Steps:**
1. Update B-STORM_6 with Entry 7 (Phase 1 completion report)
2. Ping Nova with validation results
3. Await Phase 2 strategic direction (live data integration, automation scripts, additional view modes)

**Commits:**
- `97a54fd` - Phase 1 Prototype (16 files, 1,923 insertions)
- `62e1ce3` - Phase 1 Continuation (8 files, 795 insertions)
- `a90f56e` - Ethics Annotations (3 files, 105 insertions)

**Total Lines Implemented:** ~2,820 lines across 27 files

**Implementation Time:** ~4 hours (scaffold → components → scenarios → testing)

**Prototype Stability:** Production-ready for Phase 1 goals (mock data visualization validation)

---

### Session 5: Nova Entry 8 — Phase 2 Roadmap (2025-11-11)

**Status:** ✅ **STRATEGIC DIRECTION RECEIVED**

**Crux Toggle Rationale (per Nova Entry 8):**

Nova clarified that the "Consider Crux" toggle being greyed out is **intentional design**, not a Phase 1 limitation:

**Philosophy:** "Data-first, not placeholder-first"

- **Current State:** Toggle disabled with tooltip "Available once pilot data arrives"
- **Unlock Condition:** CT↔MdN pilot produces real convergence metrics with/without Crux influence
- **Why Wait:** Crux Impact View requires actual include/exclude data to demonstrate value
  - Mock data can't authentically show Crux resolution dynamics
  - Pilot will generate first real Crux declaration (if BFI impasse occurs)
  - Include/exclude comparison needs baseline (with Crux) vs. counterfactual (without Crux)

**Phase 2 Implementation Plan:**

1. **Pilot Generates Data:**
   - CT↔MdN adversarial scoring declares Crux (if <98% convergence persists)
   - Process Claude logs metrics_include_crux vs. metrics_exclude_crux
   - SMV Claude extracts convergence deltas

2. **Toggle Activates:**
   - Button enabled when `crux.status === "declared"` or `"resolved"`
   - Click toggles between two convergence visualizations:
     - **Include Crux:** Baseline convergence (what actually happened)
     - **Exclude Crux:** Counterfactual convergence (if Crux mechanism didn't exist)

3. **Visual Changes:**
   - Sparkline shows two lines (baseline vs. counterfactual)
   - Convergence meter displays delta (e.g., "Crux contributed +12% convergence")
   - Triangle view highlights which auditor pair benefited from Crux resolution

**Example Scenario (from SMV_DESIGN_SPEC.md Scenario C):**
```json
"convergence": {
  "percentage": 95.0,
  "metrics_include_crux": ["BFI", "CA", "IP", "ES", "PS", "LS", "MS"],
  "metrics_exclude_crux": ["CA", "IP", "ES", "PS", "LS", "MS"]
}
```

**↓ Crux Impact Calculation:**
- With Crux: 7 metrics converged (100%)
- Without Crux: 6 metrics converged (85.7%)
- **Crux Contribution:** +14.3% convergence (BFI resolution unlocked progress)

**UI Mockup (Phase 2):**
- Toggle ON: Sparkline shows single green line (95% convergence)
- Toggle OFF: Sparkline shows amber line dropping to 85.7% at tick where BFI would stall
- Annotation: "Crux resolved BFI impasse, enabling 7/7 convergence"

**Documentation:**
- Full Crux workflow in [docs/smv/SMV_DESIGN_SPEC.md](../../docs/smv/SMV_DESIGN_SPEC.md) (lines 450-520)
- Crux architecture in [docs/architecture/CRUX_ARCHITECTURE.md](../../docs/architecture/CRUX_ARCHITECTURE.md)
- Phase 2 unlock conditions in [auditors/relay/B-STORM_6.md](../../auditors/relay/B-STORM_6.md) Entry 8

**Status:** Rationale logged. Toggle remains disabled until pilot produces real Crux data.

---
