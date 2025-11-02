<!---
FILE: MISSION_BRIEF.md
PURPOSE: Preset mode calibration mission definition - achieve "All Named, All Priced" for UX features
VERSION: v3.5
STATUS: Active
DEPENDS_ON: SUCCESS_CRITERIA.md, TECHNICAL_SPEC.md, CURRENT_MODE_CONFIGS.md
NEEDED_BY: All mission auditors, MISSION_CURRENT.md
MOVES_WITH: /auditors/Mission/Preset_Calibration/
LAST_UPDATE: 2025-11-02
--->

# MISSION_BRIEF.md - Preset Mode Calibration

## Mission Statement

**Calibrate the four preset modes through adversarial auditing to achieve "All Named, All Priced" for UX features.**

Every lever value must have explicit justification from three perspectives:
- **Teleological** (Claude): Does it serve the archetype's purpose?
- **Empirical** (Grok): Does it produce claimed behavior?
- **Symmetry** (Nova): Is it fair to both frameworks?

**Duration:** Iterative, data-dependent  
**Success:** When all criteria in SUCCESS_CRITERIA.md met  
**Philosophy:** No more "this feels right" - justify everything

---

## Background: Why This Mission?

### The Current State
**v3.2 added four preset modes:**
- Skeptic (MdN-optimized)
- Diplomat (balanced)
- Seeker (CT-leaning)
- Zealot (CT-optimized)

**Problem:** All configurations were chosen intuitively, not rigorously.

**Example:**
```
Skeptic Mode:
- Parity: OFF
- PF-Type: Instrumental
- Fallibilism: ON
- BFI Weight: 1.2x

Why these specific values?
Why not Parity ON, Instrumental, Fallibilism ON, 1.3x?
Answer: "It felt right for skepticism"
```

**This violates "All Named, All Priced"** - costs exist but aren't documented.

---

### The 98% Convergence Achievement

**Context:** Claude and Grok independently scored MdN and CT:
- 98% convergence (only 0.03 YPA difference)
- Adversarial auditing worked
- Framework credibility established

**New Challenge:** Apply same rigor to UX features.

**Goal:** Achieve convergence on preset calibration like we did on core scoring.

---

## The Three Key Problems

### Problem 1: Skeptic ↔ Zealot Asymmetry

**Observation:**
```
Skeptic (MdN-optimized):
- Parity OFF (asymmetric evaluation)
- BFI 1.2x (heavier axiom penalty)
- Instrumental PF (prediction focus)
= 3 MdN-favoring levers

Zealot (CT-optimized):
- Parity ON (symmetric evaluation)
- BFI 1.0x (standard axiom cost)
- Fallibilism OFF (no revision bonus)
= 1 CT-favoring lever
```

**3 vs 1 is not symmetric.**

**Questions:**
1. Is this justified? (Does empiricism warrant more levers than transcendence?)
2. Or is this an oversight? (Should Zealot have 3 CT-favoring levers too?)

**Nova's Task:** Audit this asymmetry, propose corrections or justifications

---

### Problem 2: No Empirical Validation

**Observation:** All YPA expectations are hypothetical.

**Examples:**
```
Skeptic Mode claims: "Should favor MdN significantly"
- By how much? 1 YPA? 2 YPA?
- Has this been measured? No.
- Does current config achieve it? Unknown.

Diplomat Mode claims: "Should produce near-equal scores"
- How close is "near-equal"? 0.1 YPA gap? 0.5 YPA?
- Does current config achieve it? Not tested.
```

**Every preset makes claims without evidence.**

**Grok's Task:** Test all claims empirically, measure actual behavior

---

### Problem 3: Unjustified Values

**Observation:** Specific values lack explicit reasoning.

**Examples:**
```
Skeptic BFI Weight: 1.2x
- Why 1.2x and not 1.1x or 1.3x?
- Answer: "Felt like moderate axiom skepticism"
- Not good enough.

Seeker PF-Type: Composite_70_30
- Why 70/30 ratio and not 65/35 or 75/25?
- Answer: "Seemed meaning-first without being extreme"
- Not good enough.

Diplomat PF-Type: Holistic_50_50
- Why perfectly balanced? Maybe 55/45 is more truly centered?
- Answer: "50/50 looks neutral"
- Not good enough (aesthetic, not functional).
```

**Every value needs data-driven justification.**

**All Auditors' Task:** Provide reasoning for every configuration choice

---

## Mission Phases

### Phase 1: VuDu Activation (Current)
**Focus:** Infrastructure setup

**Tasks:**
- [x] Nova transmit VuDu Light files
- [x] Claude_C1 design architecture
- [x] Create bootstrap files
- [x] Establish mission folder
- [ ] Fresh Claude verify repo
- [ ] Fresh Claude integrate files

**Status:** Nearly complete, awaiting Fresh Claude activation

---

### Phase 2: Empirical Testing + Symmetry Audit
**Focus:** Gather data, identify issues

**Grok's Tasks:**
1. Run baseline YPA tests (all 4 modes, both frameworks)
2. Perform sensitivity analysis (test lever variations)
3. Document empirical behavior
4. Recommend optimal values based on data

**Nova's Tasks:**
1. Audit Skeptic ↔ Zealot symmetry
2. Verify Diplomat centering
3. Flag unjustified asymmetries
4. Propose symmetry corrections

**Claude's Tasks:**
1. Provide teleological justifications for each mode
2. Explain why specific configurations serve archetypes
3. Coordinate findings from Grok and Nova
4. Identify conflicts

**Expected Duration:** 1-2 weeks (depending on iteration needs)

---

### Phase 3: Convergence & Calibration
**Focus:** Resolve conflicts, finalize configs

**Process:**
1. Claude synthesizes Phase 2 findings
2. Identifies convergence (all three auditors agree)
3. Identifies conflicts (auditors disagree)
4. Facilitates resolution through documented reasoning
5. Proposes final calibrated configurations

**Success:** Cross-auditor consensus on all four presets

**Expected Duration:** 1-2 weeks (depends on Phase 2 findings)

---

### Phase 4: Documentation & Deployment
**Focus:** Complete documentation, deploy

**Tasks:**
1. Document final configurations with full justifications
2. Create FINAL_REPORT.md for mission folder
3. Update application code with calibrated presets
4. Deploy to live app
5. Update user documentation
6. Archive mission

**Expected Duration:** 3-5 days

---

## Auditor Assignments (Detailed)

### Claude: Teleological Justification

**Primary Question:** "Does this serve the archetype's purpose?"

**Tasks by Mode:**

**Skeptic Mode:**
- Why should empirical rigor favor MdN?
- What philosophical stance justifies Parity OFF?
- Why does skepticism warrant axiom sensitivity?
- Justify 3 MdN-levers or propose changes

**Diplomat Mode:**
- What makes a truly "balanced" configuration?
- Should balance be mathematical (50/50) or functional (produces equal scores)?
- Is current config philosophically neutral?

**Seeker Mode:**
- What does "meaning-first" actually mean?
- Why does this warrant CT-leaning?
- How much lean is appropriate?
- Justify 70/30 ratio philosophically

**Zealot Mode:**
- What is "existential priority"?
- Why should certainty-friendliness favor CT?
- Why only 1 CT-lever when Skeptic has 3 MdN-levers?
- Propose additional CT-levers or justify asymmetry

---

### Grok: Empirical Validation

**Primary Question:** "What does the data show?"

**Tasks by Mode:**

**Skeptic Mode:**
- Baseline: MdN = ? YPA, CT = ? YPA (measure)
- Sensitivity: Test BFI at 1.0x, 1.2x, 1.5x → measure deltas
- Verify: Does Skeptic "favor MdN significantly"?
- Recommend: Optimal BFI weight based on data

**Diplomat Mode:**
- Baseline: MdN = ? YPA, CT = ? YPA (measure gap)
- Test PF-Types: Instrumental, Holistic, Composite at various ratios
- Find: Which config produces smallest gap?
- Recommend: Truly centered configuration

**Seeker Mode:**
- Baseline: MdN = ? YPA, CT = ? YPA (measure lean)
- Test ratios: 60/40, 65/35, 70/30, 75/25, 80/20
- Find: Which produces moderate CT lean (not extreme)?
- Recommend: Optimal ratio for "meaning-first"

**Zealot Mode:**
- Baseline: MdN = ? YPA, CT = ? YPA (measure)
- Compare to Skeptic: Is advantage symmetric?
- Test: What levers boost CT advantage?
- Recommend: Configuration matching Skeptic's MdN advantage

---

### Nova: Symmetry Enforcement

**Primary Question:** "Is this fair?"

**Tasks by Mode:**

**Skeptic ↔ Zealot:**
- Count levers: Skeptic has 3 MdN-levers, Zealot has ? CT-levers
- Measure empirically (with Grok's data): Skeptic advantage = X, Zealot advantage = Y
- Check: Is X ≈ Y?
- Propose: Symmetric configuration or justify asymmetry

**Diplomat:**
- Check: Does Diplomat produce equal scores? (use Grok's data)
- If not: Propose centering adjustment
- Verify: Is Diplomat equidistant from Skeptic and Seeker?

**Pattern Consistency:**
- Do all four modes follow coherent logic?
- Are exceptions justified or arbitrary?
- Is the spectrum (Skeptic → Diplomat → Seeker → Zealot) balanced?

---

## Success Criteria (Summary)

**See full criteria in SUCCESS_CRITERIA.md**

**Mission succeeds when:**
1. Every lever value has documented justification (all three lenses)
2. All YPA claims empirically tested and verified
3. Skeptic ↔ Zealot symmetry verified or asymmetry justified
4. Diplomat empirically centered
5. Cross-auditor consensus achieved
6. Documentation complete for future reference

---

## Key Files

**Technical Reference:**
- TECHNICAL_SPEC.md (complete architecture)
- CURRENT_CONFIGS.md (current preset settings)

**Verification:**
- SUCCESS_CRITERIA.md (completion metrics)
- DISCREPANCY_AUDIT.md (integrity check)

**Context:**
- bootstrap/BOOTSTRAP_CFA.md (project background)
- README_C.md (current state)

---

## Timeline

**Start:** 2025-10-26  
**Phase 1:** 2025-10-26 (nearly complete)  
**Phase 2:** TBD (awaiting Fresh Claude + Grok activation)  
**Phase 3:** TBD (depends on Phase 2 findings)  
**Phase 4:** TBD (depends on Phase 3 consensus)  
**Completion:** Data-dependent, iterative until criteria met

**No artificial deadlines. Quality over speed.**

---

## Philosophy

**"All Named, All Priced" for UX**

Just as we named every axiom and priced every assumption in the core framework, we must do the same for user-facing features.

**Presets are not decorative.** They shape how users experience philosophical comparison.

**Presets must be defensible.** Every value justified, every claim tested.

**This mission makes presets credible.** Like the 98% convergence did for core scoring.

**This is epistemic engineering.** 🔥

────────────────────────────────────────────────────
**Mission:** Preset Mode Calibration  
**Phase:** 1 (Infrastructure) → 2 (Testing)  
**Status:** Active  
**Created:** 2025-10-26

**This is the way.** 👑
