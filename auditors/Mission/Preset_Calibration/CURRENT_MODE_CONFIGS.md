<!---
FILE: CURRENT_MODE_CONFIGS.md
PURPOSE: Exact current preset mode values for VuDu calibration
VERSION: v4.0.0
STATUS: Active - INTUITIVE (not yet calibrated)
DEPENDS_ON: pages/console.py (lines 185-222), MISSION_BRIEF.md
NEEDED_BY: Calibration auditors, SUCCESS_CRITERIA.md validation
MOVES_WITH: /auditors/Mission/Preset_Calibration/
LAST_UPDATE: 2025-11-02
--->

# CURRENT MODE CONFIGURATIONS - v3.5 📊

**Purpose:** Exact current preset mode values for VuDu calibration  
**Status:** INTUITIVE (not yet calibrated)  
**Source:** Extracted from `pages/console.py` lines 185-222  
**Date:** October 26, 2025  

---

## 🎯 **CALIBRATION MISSION**

**Goal:** Justify EVERY value in EVERY mode ("All Named, All Priced")

**Method:** VuDu Protocol adversarial auditing
- Claude: Teleological justification
- Grok: Empirical validation
- Nova: Symmetry verification

**Success:** Every configuration choice has documented reasoning

---

## 🔬 **SKEPTIC MODE (MdN-Optimized)**

### **Current Configuration:**
```python
SKEPTIC_MODE = {
    "lever_parity": "OFF",
    "pf_type": "Instrumental",
    "fallibilism_bonus": "ON",
    "bfi_debt_weight": "Heavier_1.2x"
}
```

### **Claimed Identity:**
- **Philosophy:** Empirical rigor, prediction focus, axiom skepticism
- **Target User:** Someone who values testability and falsifiability
- **Expected Behavior:** Should favor MdN significantly

### **Questions to Answer:**

**Q1: Why Parity OFF?**
- ❓ Claimed: "Allows asymmetric evaluation favoring empirical frameworks"
- Challenge: Isn't asymmetry just hidden bias?
- Alternative: Could Parity ON with other levers achieve same effect?

**Q2: Why Instrumental PF?**
- ❓ Claimed: "Pure prediction focus aligns with skeptical epistemology"
- Challenge: Does this unfairly penalize CT's non-instrumental fruitfulness?
- Alternative: Could Holistic_50_50 with other adjustments work?

**Q3: Why Fallibilism ON?**
- ❓ Claimed: "Rewards MdN's explicit falsifiability"
- Challenge: Does CT also have revision mechanisms?
- Alternative: Should this be OFF if we're being truly "skeptical"?

**Q4: Why BFI 1.2x not 1.3x or 1.1x?**
- ❓ Claimed: "Moderate axiom penalty"
- Challenge: What empirical basis for 1.2x specifically?
- Test Needed: Try 1.1x, 1.2x, 1.3x and measure YPA changes

### **Expected YPA Output:**
- **Hypothesis:** MdN ~7-8, CT ~4-5 (strong MdN bias)
- **Actual:** NOT YET TESTED ❌
- **Action Item:** Run empirical tests

### **Symmetry Check:**
- **Opposing Mode:** Zealot (should be mirror)
- **Symmetry Status:** ⚠️ Skeptic has 3 unique values, Zealot has 1
- **Question:** Is this justified asymmetry or oversight?

---

## 🤝 **DIPLOMAT MODE (Balanced)**

### **Current Configuration:**
```python
DIPLOMAT_MODE = {
    "lever_parity": "ON",
    "pf_type": "Holistic_50_50",
    "fallibilism_bonus": "ON",
    "bfi_debt_weight": "Equal_1.0x"
}
```

### **Claimed Identity:**
- **Philosophy:** Fair comparison, balanced criteria, neutral stance
- **Target User:** Someone seeking unbiased framework comparison
- **Expected Behavior:** Should produce near-equal scores

### **Questions to Answer:**

**Q1: Why Parity ON?**
- ✅ Defensible: Symmetry enforcement for fairness
- Challenge: None (this seems right for "balanced" mode)

**Q2: Why Holistic_50_50?**
- ✅ Defensible: Equal weighting of instrumental/intrinsic
- Challenge: None (fits "balanced" archetype)

**Q3: Why Fallibilism ON?**
- ❓ Claimed: "Rewards both frameworks equally"
- Challenge: If MdN benefits more, isn't this biased?
- Alternative: Should Diplomat be OFF (neutral)?

**Q4: Why BFI Equal 1.0x?**
- ✅ Defensible: Standard weight for "balanced" mode
- Challenge: None

### **Expected YPA Output:**
- **Hypothesis:** MdN ~6, CT ~6 (±0.3 tolerance)
- **Actual:** NOT YET TESTED ❌
- **Success Criteria:** |MdN - CT| < 0.5 YPA

### **Symmetry Check:**
- **Center Point:** Should be equidistant from Skeptic and Zealot
- **Symmetry Status:** ✅ Appears balanced
- **Question:** Does empirical testing confirm?

---

## 🌉 **SEEKER MODE (CT-Leaning)**

### **Current Configuration:**
```python
SEEKER_MODE = {
    "lever_parity": "ON",
    "pf_type": "Composite_70_30",
    "fallibilism_bonus": "ON",
    "bfi_debt_weight": "Equal_1.0x"
}
```

### **Claimed Identity:**
- **Philosophy:** Meaning-first, holistic value, epistemic openness
- **Target User:** Someone who values existential depth
- **Expected Behavior:** Should lean toward CT (but not extreme)

### **Questions to Answer:**

**Q1: Why Parity ON?**
- ✅ Defensible: Maintains fairness while leaning CT
- Challenge: None

**Q2: Why 70/30 specifically?**
- ❓ Claimed: "Significant but not extreme holistic weighting"
- Challenge: Why not 65/35 or 75/25?
- Test Needed: Sensitivity analysis on 60/40, 65/35, 70/30, 75/25

**Q3: Why Fallibilism ON?**
- ❓ Claimed: "Epistemic openness"
- Challenge: If this favors MdN, conflicts with CT-leaning goal
- Alternative: Should be OFF?

**Q4: Why BFI Equal 1.0x?**
- ❓ Claimed: "Standard weight"
- Challenge: Could Lighter_0.8x better serve CT-leaning goal?
- Alternative: Test 0.8x vs 1.0x

### **Expected YPA Output:**
- **Hypothesis:** MdN ~5, CT ~7 (moderate CT bias)
- **Actual:** NOT YET TESTED ❌
- **Success Criteria:** CT > MdN by 1.5-2.5 YPA

### **Symmetry Check:**
- **Position:** Between Diplomat and Zealot
- **Symmetry Status:** ⚠️ Should mirror Skeptic's position relative to Diplomat
- **Question:** Is CT-leaning magnitude = MdN-leaning magnitude?

---

## ⛪ **ZEALOT MODE (CT-Optimized)**

### **Current Configuration:**
```python
ZEALOT_MODE = {
    "lever_parity": "ON",
    "pf_type": "Holistic_50_50",
    "fallibilism_bonus": "OFF",
    "bfi_debt_weight": "Equal_1.0x"
}
```

### **Claimed Identity:**
- **Philosophy:** Existential priority, certainty-friendly, holistic focus
- **Target User:** Someone committed to transcendent meaning
- **Expected Behavior:** Should favor CT significantly

### **Questions to Answer:**

**Q1: Why Parity ON not OFF?**
- ❓ Claimed: "Maintains fairness"
- Challenge: If Skeptic is OFF, why isn't Zealot OFF (mirror)?
- Symmetry Issue: This breaks Skeptic ↔ Zealot symmetry

**Q2: Why Holistic_50_50 not Composite_30_70?**
- ❓ Claimed: "Balanced holistic weighting"
- Challenge: Shouldn't Zealot favor intrinsic value MORE?
- Alternative: Try Composite_30_70 (inverse of Seeker's 70/30)

**Q3: Why Fallibilism OFF?**
- ✅ Defensible: "Certainty-friendly" archetype
- Challenge: Does this sufficiently counterbalance Skeptic's biases?

**Q4: Why BFI Equal 1.0x not Lighter_0.8x?**
- ❓ Claimed: "Standard weight"
- Challenge: Shouldn't Zealot be more axiom-tolerant (mirror of Skeptic's 1.2x)?
- Symmetry Issue: Skeptic 1.2x but Zealot 1.0x (not symmetric)

### **Expected YPA Output:**
- **Hypothesis:** MdN ~4, CT ~8 (strong CT bias)
- **Actual:** NOT YET TESTED ❌
- **Success Criteria:** CT > MdN by 3-4 YPA (mirror of Skeptic)

### **Symmetry Check:**
- **Opposing Mode:** Skeptic
- **Symmetry Violations:**
  - ❌ Parity: Skeptic OFF, Zealot ON (asymmetric)
  - ❌ PF: Skeptic Instrumental, Zealot Holistic_50_50 (not mirror)
  - ✅ Fallibilism: Skeptic ON, Zealot OFF (symmetric)
  - ❌ BFI: Skeptic 1.2x, Zealot 1.0x (not mirror, should be 0.8x)

**Major Symmetry Issue Identified!** 🚨

---

## 📊 **MODE COMPARISON MATRIX**

| Lever | Skeptic | Diplomat | Seeker | Zealot |
|:------|:--------|:---------|:-------|:-------|
| **Parity** | OFF | ON | ON | ON |
| **PF-Type** | Instrumental | Holistic_50_50 | Composite_70_30 | Holistic_50_50 |
| **Fallibilism** | ON | ON | ON | OFF |
| **BFI Weight** | 1.2x | 1.0x | 1.0x | 1.0x |

### **Symmetry Analysis:**

**Skeptic ↔ Diplomat:**
- Distance: 3 lever differences
- Justified: Skeptic is extreme, Diplomat is center

**Diplomat ↔ Zealot:**
- Distance: 1 lever difference (Fallibilism only)
- ⚠️ Issue: Should Zealot be more extreme than this?

**Skeptic ↔ Zealot:**
- Expected: Perfect mirror (opposing extremes)
- Actual: 3 asymmetries (Parity, PF, BFI)
- ❌ Symmetry Violation: Needs justification or correction

**Seeker Position:**
- Between Diplomat and Zealot
- 1 lever different from Diplomat (PF-Type)
- ⚠️ Issue: Seems closer to Diplomat than to Zealot

---

## 🎯 **EMPIRICAL TEST MATRIX**

### **Required Tests:**

**Test 1: Baseline YPA**
```
Configuration: Current defaults
Measure: MdN YPA, CT YPA for each mode
Goal: Establish actual behavior vs hypothesized
```

**Test 2: Skeptic Variations**
```
Test A: Parity ON instead of OFF
Test B: BFI 1.1x, 1.2x, 1.3x comparison
Test C: Fallibilism OFF instead of ON
Goal: Find optimal Skeptic configuration
```

**Test 3: Zealot Variations**
```
Test A: Parity OFF instead of ON (symmetry test)
Test B: BFI 0.8x instead of 1.0x (symmetry test)
Test C: PF Composite_30_70 instead of Holistic_50_50
Goal: Achieve symmetric opposition to Skeptic
```

**Test 4: Seeker Ratio Sweep**
```
Test ratios: 60/40, 65/35, 70/30, 75/25
Measure: CT-MdN YPA delta
Goal: Find optimal "CT-leaning" balance
```

**Test 5: Diplomat Neutrality**
```
Test: Fallibilism ON vs OFF
Measure: |MdN - CT| YPA difference
Goal: Minimize bias, achieve true balance
```

---

## 🚨 **CRITICAL ISSUES IDENTIFIED**

### **Issue 1: Skeptic ↔ Zealot Asymmetry**

**Problem:** Opposing modes not properly mirrored

**Specific Violations:**
1. Parity: Skeptic OFF, Zealot ON (should both be OFF or both be ON)
2. PF-Type: Skeptic Instrumental, Zealot Holistic_50_50 (should be Instrumental ↔ some extreme holistic)
3. BFI Weight: Skeptic 1.2x, Zealot 1.0x (should be 1.2x ↔ 0.8x)

**Consequence:** 
- Skeptic has 3 MdN-favoring levers
- Zealot has only 1 CT-favoring lever
- Not philosophically justified imbalance

**Action Required:** Either justify or correct

---

### **Issue 2: Seeker Positioning**

**Problem:** Too close to Diplomat, not distinct enough

**Current:** Only PF-Type differs from Diplomat
**Expected:** Should be noticeably CT-leaning (between Diplomat and Zealot)

**Options:**
- A) Change PF ratio to 75/25 (more extreme)
- B) Add BFI Lighter_0.8x (match Zealot's suggested correction)
- C) Change Fallibilism to OFF (match Zealot)

**Action Required:** Empirical testing + philosophical justification

---

### **Issue 3: No Empirical Validation**

**Problem:** All YPA expectations are HYPOTHETICAL

**Status:** 
- ❌ No actual YPA measurements
- ❌ No sensitivity analysis performed
- ❌ No validation against claimed behavior

**Action Required:** 
- Run all 4 modes with current MdN/CT defaults
- Document actual YPA outputs
- Compare to hypothesized behavior
- Identify discrepancies

---

## 📋 **VUDU COORDINATION CHECKLIST**

### **For Claude (Teleological):**
- [ ] Justify each mode's archetype philosophically
- [ ] Explain why Skeptic ↔ Zealot asymmetries (if defensible)
- [ ] Propose teleologically-optimal configurations
- [ ] Document reasoning for each choice

### **For Grok (Empirical):**
- [ ] Run baseline YPA tests (all 4 modes)
- [ ] Perform sensitivity analysis (lever variations)
- [ ] Challenge unjustified assumptions with data
- [ ] Recommend empirically-optimal values

### **For Nova (Symmetry):**
- [ ] Verify Skeptic ↔ Zealot symmetry
- [ ] Check Diplomat as true center point
- [ ] Flag all asymmetries (justified or violations)
- [ ] Propose symmetry-corrected configurations

### **For Integration (Claude Coordination):**
- [ ] Synthesize findings from all three lenses
- [ ] Resolve conflicts with documented reasoning
- [ ] Create final calibrated configurations
- [ ] Update console.py with justified values

---

## 💾 **MACHINE-READABLE FORMAT**

For easy copy-paste into analysis tools:

```json
{
  "modes": {
    "skeptic": {
      "lever_parity": "OFF",
      "pf_type": "Instrumental",
      "fallibilism_bonus": "ON",
      "bfi_debt_weight": 1.2,
      "expected_ypa": {"mdn": 7.5, "ct": 4.5},
      "status": "untested"
    },
    "diplomat": {
      "lever_parity": "ON",
      "pf_type": "Holistic_50_50",
      "fallibilism_bonus": "ON",
      "bfi_debt_weight": 1.0,
      "expected_ypa": {"mdn": 6.0, "ct": 6.0},
      "status": "untested"
    },
    "seeker": {
      "lever_parity": "ON",
      "pf_type": "Composite_70_30",
      "fallibilism_bonus": "ON",
      "bfi_debt_weight": 1.0,
      "expected_ypa": {"mdn": 5.0, "ct": 7.0},
      "status": "untested"
    },
    "zealot": {
      "lever_parity": "ON",
      "pf_type": "Holistic_50_50",
      "fallibilism_bonus": "OFF",
      "bfi_debt_weight": 1.0,
      "expected_ypa": {"mdn": 4.0, "ct": 8.0},
      "status": "untested"
    }
  },
  "symmetry_issues": [
    {
      "type": "parity_asymmetry",
      "levers": ["skeptic.parity", "zealot.parity"],
      "current": ["OFF", "ON"],
      "expected": ["OFF", "OFF"] or ["ON", "ON"]
    },
    {
      "type": "bfi_asymmetry",
      "levers": ["skeptic.bfi_weight", "zealot.bfi_weight"],
      "current": [1.2, 1.0],
      "expected": [1.2, 0.8]
    }
  ]
}
```

---

## ✅ **DOCUMENT COMPLETE**

**This file provides:**
- ✅ Exact current configurations
- ✅ Questions for each value
- ✅ Symmetry violation identification
- ✅ Empirical test matrix
- ✅ VuDu coordination checklist
- ✅ Machine-readable format

**Ready for:** VuDu calibration mission

---

**Version:** v3.5.1  
**Last Updated:** October 26, 2025  
**Status:** Ready for calibration ✅
