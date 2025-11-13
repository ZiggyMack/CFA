<!---
FILE: TECHNICAL_SPEC.md
PURPOSE: Complete technical reference for AI auditors - preset modes, YPA calculation, system architecture
VERSION: v4.0.0
STATUS: Active
DEPENDS_ON: utils/frameworks.py, utils/calculations.py, pages/console.py
NEEDED_BY: MISSION_BRIEF.md, SUCCESS_CRITERIA.md, all technical auditors
MOVES_WITH: /auditors/Mission/Preset_Calibration/
LAST_UPDATE: 2025-11-02
--->

# CFA v3.5 - TECHNICAL SPECIFICATION 🔧

**Purpose:** Complete technical reference for AI auditors  
**Audience:** Claude, Grok, Nova (technical analysis)  
**Version:** v3.5.1  
**Date:** October 26, 2025  

---

## 🏗️ **ARCHITECTURE OVERVIEW**

**Stack:**
- **Frontend:** Streamlit (Python web framework)
- **Backend:** Python 3.11+
- **Deployment:** Streamlit Cloud
- **Repository:** GitHub (cfa-voodoo)

**Application Type:** Single-page web application with multi-page routing

---

## 📂 **FILE STRUCTURE & DEPENDENCIES**

### **app.py (Root Entry Point)**
```python
# Main router
# Imports: pages/*, streamlit
# Responsibilities:
#   - Page configuration
#   - Session state initialization
#   - Page routing based on st.session_state.page
```

### **pages/ (Page Modules)**

**landing.py:**
- Manifesto and project intro
- Navigation buttons
- Marketing/credibility callouts (at bottom)

**console.py (PRIMARY INTERFACE):**
- Main interactive console
- 4 tabs: Settings, Results, Guardrails, Quiz
- Preset Mode Spectrum in sidebar
- All lever controls
- YPA calculation and display

**manual.py:**
- User manual with examples
- Formula documentation
- Calibration history

**about.py:**
- Project background
- Audit journey (Level 0-4)
- Convergence story

**brute_ledger.py:**
- Assumption tracker ("Mr. Brute's Ledger")
- Lists all axioms with costs

### **utils/ (Core Logic)**

**calculations.py (CRITICAL):**
```python
# Functions:
ypa_scenario_scores(...)  # Main YPA calculation
guardrail_lever_coupling(...)  # Guardrail #1
guardrail_bfi_sensitivity(...)  # Guardrail #2
guardrail_weight_inversion(...)  # Guardrail #3
symmetry_audit(...)  # Guardrail #4

# Constants:
PF_TYPES = {
    "Instrumental": {...},
    "Holistic_50_50": {...},
    "Composite_70_30": {...}
}
```

**visualizations.py:**
```python
# Chart generation
create_lever_comparison_chart(...)
create_ypa_trinity_chart(...)
# Uses plotly for interactive charts
```

**frameworks.py:**
```python
# Framework definitions
MDN_DEFAULT = {...}  # Mere Divine Naturalism
CT_DEFAULT = {...}   # Classical Theism
# Stores base scores for all 5 dimensions
```

---

## 🎚️ **LEVER SYSTEM (Detailed)**

### **Lever 1: Parity**

**Purpose:** Symmetry enforcement toggle

**Implementation:**
```python
if lever_parity == "ON":
    # Apply same evaluation criteria to both frameworks
    # PF-Type applies equally
    # Fallibilism bonus applies equally
else:
    # Frameworks can be evaluated differently
    # Allows asymmetric criteria
```

**Impact on YPA:**
- Moderate (affects fairness perception, not raw scores)
- Can change relative positioning by ~0.5-1.0 YPA

**Current Usage in Modes:**
- Skeptic: OFF (allows asymmetric evaluation)
- Diplomat, Seeker, Zealot: ON (enforces symmetry)

---

### **Lever 2: PF-Type**

**Purpose:** Defines "Philosophical Fruitfulness" evaluation method

**Types:**

**Instrumental:**
```python
{
    "instrumental_weight": 1.0,
    "intrinsic_weight": 0.0
}
# Pure prediction/explanation focus
# Rewards testability, falsifiability
```

**Holistic_50_50:**
```python
{
    "instrumental_weight": 0.5,
    "intrinsic_weight": 0.5
}
# Balanced instrumental + intrinsic value
# Considers meaning alongside prediction
```

**Composite_70_30:**
```python
{
    "instrumental_weight": 0.3,
    "intrinsic_weight": 0.7
}
# Heavily weighted toward holistic value
# Prioritizes existential/meaning dimensions
```

**Impact on YPA:**
- High (3-5 YPA swing possible)
- Directly affects PF dimension scoring
- Cascades through weighted scenarios

**Current Usage in Modes:**
- Skeptic: Instrumental (pure empirical)
- Diplomat: Holistic_50_50 (balanced)
- Seeker: Composite_70_30 (meaning-leaning)
- Zealot: Holistic_50_50 (balanced, but with other levers CT-favoring)

---

### **Lever 3: Fallibilism Bonus**

**Purpose:** Rewards epistemic humility and self-correction

**Implementation:**
```python
if fallibilism_bonus == "ON":
    # Add +0.5 to frameworks that embrace revision
    # Rewards: error-correction, uncertainty acknowledgment
    # MdN typically benefits more (explicit falsifiability)
```

**Impact on YPA:**
- Low-Moderate (0.3-0.8 YPA)
- Affects specific scenarios (e.g., "paradigm shift" contexts)

**Current Usage in Modes:**
- Skeptic, Diplomat, Seeker: ON (rewards revision)
- Zealot: OFF (no bonus for uncertainty)

---

### **Lever 4: BFI-Debt Weight**

**Purpose:** Adjusts penalty for unprovable starting assumptions

**Weights:**

**Equal_1.0x:**
```python
bfi_multiplier = 1.0
# Standard axiom counting
```

**Heavier_1.2x:**
```python
bfi_multiplier = 1.2
# 20% increased axiom penalty
# Makes axiom-heavy frameworks pay more
```

**Lighter_0.8x:**
```python
bfi_multiplier = 0.8
# 20% reduced axiom sensitivity
# More forgiving of starting assumptions
```

**Impact on YPA:**
- Moderate (1-2 YPA possible)
- Affects BFI (Brute-Fact Index) calculation
- CT typically has higher BFI than MdN

**Current Usage in Modes:**
- Skeptic: Heavier_1.2x (penalize axioms more)
- Diplomat, Seeker, Zealot: Equal_1.0x (standard)

---

## 🛡️ **GUARDRAIL SYSTEM (Detailed)**

### **Guardrail #1: Lever-Coupling**

**Rule:** `if PF >= 9 then CCI >= 6.5`

**Rationale:**
- Can't claim high fruitfulness without coherence
- Prevents: "It's super productive but incoherent"

**Implementation:**
```python
def guardrail_lever_coupling(framework_dict):
    pf = framework_dict['PF']
    cci = framework_dict['CCI']
    if pf >= 9 and cci < 6.5:
        return {
            "triggered": True,
            "message": "⚠️ Lever-Coupling violated..."
        }
    return {"triggered": False}
```

**Trigger Frequency:** Rare (tight scores usually don't violate)

---

### **Guardrail #2: BFI-Sensitivity**

**Rule:** `ΔYPA / ΔBFI < 0.4`

**Rationale:**
- YPA should respond to axiom changes
- Prevents: Axiom inflation (adding assumptions without cost)

**Implementation:**
```python
def guardrail_bfi_sensitivity(ypa_delta, bfi_delta):
    if bfi_delta == 0:
        return {"triggered": False}
    sensitivity = abs(ypa_delta / bfi_delta)
    if sensitivity > 0.4:
        return {
            "triggered": True,
            "message": "⚠️ BFI-Sensitivity too high..."
        }
    return {"triggered": False}
```

**Trigger Frequency:** Moderate (activates when BFI changes don't affect YPA enough)

---

### **Guardrail #3: Weight-Inversion Alarm**

**Rule:** `0.3x <= scenario_weight <= 3.0x`

**Rationale:**
- Prevents extreme scenario cherry-picking
- Ensures balanced consideration of contexts

**Implementation:**
```python
def guardrail_weight_inversion(scenario_weights):
    violations = []
    for scenario, weight in scenario_weights.items():
        if weight < 0.3 or weight > 3.0:
            violations.append(scenario)
    if violations:
        return {
            "triggered": True,
            "violations": violations
        }
    return {"triggered": False}
```

**Trigger Frequency:** Low (users rarely weight extremes)

---

### **Guardrail #4: Symmetry Audit Summary**

**Rule:** Display toggle sensitivity

**Rationale:**
- Transparency about bias
- Shows how each toggle affects each framework

**Implementation:**
```python
def symmetry_audit(framework1, framework2, lever_states):
    # Run mini-experiments: flip each toggle
    # Measure YPA change for each framework
    # Display: "Parity OFF→ON: MdN +0.8, CT -0.3"
    return {
        "parity_impact": {...},
        "pf_impact": {...},
        "fallibilism_impact": {...},
        "bfi_impact": {...}
    }
```

**Display:** Always shown in Guardrails tab

---

## 📐 **YPA CALCULATION (Detailed)**

### **Core Formula:**

```python
def ypa_scenario_scores(framework_dict, lever_states):
    # Step 1: Extract dimension scores
    cci = framework_dict['CCI']
    dep = framework_dict['DEP']
    pf = framework_dict['PF']  # Modified by PF-Type lever
    bae = framework_dict['BAE']
    mef = framework_dict['MEF']
    
    # Step 2: Apply PF-Type modifier
    if lever_states['pf_type'] == 'Instrumental':
        pf_modified = pf * 1.0  # No change
    elif lever_states['pf_type'] == 'Holistic_50_50':
        pf_modified = pf * 0.9  # Slight reduction
    elif lever_states['pf_type'] == 'Composite_70_30':
        pf_modified = pf * 0.8  # Moderate reduction
    
    # Step 3: Apply Fallibilism Bonus
    if lever_states['fallibilism_bonus'] == 'ON':
        if framework_has_revision_mechanism(framework_dict):
            dep += 0.5  # Boost for self-correction
    
    # Step 4: Apply BFI Weight
    bfi = framework_dict['BFI']
    bfi_penalty = bfi * lever_states['bfi_weight_multiplier']
    
    # Step 5: Calculate weighted scenario scores
    scenarios = {
        'baseline': 0.4,
        'crisis': 0.2,
        'paradigm_shift': 0.15,
        'existential': 0.15,
        'edge_case': 0.1
    }
    
    total_ypa = 0
    for scenario, weight in scenarios.items():
        scenario_score = (
            cci * 0.25 +
            dep * 0.25 +
            pf_modified * 0.25 +
            bae * 0.125 +
            mef * 0.125
        ) - bfi_penalty
        
        total_ypa += scenario_score * weight
    
    # Step 6: Check guardrails
    guardrails = [
        guardrail_lever_coupling(framework_dict),
        guardrail_bfi_sensitivity(...),
        guardrail_weight_inversion(scenarios),
        symmetry_audit(framework1, framework2, lever_states)
    ]
    
    return {
        'ypa': total_ypa,
        'guardrails': guardrails
    }
```

---

## 🎨 **PRESET MODES (Implementation)**

### **Location:** `pages/console.py` lines 185-222

### **Implementation Pattern:**
```python
if st.button("🔬 Skeptic Mode"):
    st.session_state["lever_parity"] = "OFF"
    st.session_state["pf_type"] = "Instrumental"
    st.session_state["fallibilism_bonus"] = "ON"
    st.session_state["bfi_debt_weight"] = "Heavier_1.2x"
    st.success("✅ Skeptic Mode loaded!")
    st.rerun()
```

### **Current Configurations:**

**Skeptic Mode:**
- Parity: OFF (asymmetric allowed)
- PF: Instrumental (pure prediction)
- Fallibilism: ON (reward revision)
- BFI Weight: Heavier_1.2x (penalize axioms)
- **Expected YPA:** MdN ~7-8, CT ~4-5

**Diplomat Mode:**
- Parity: ON (enforce symmetry)
- PF: Holistic_50_50 (balanced)
- Fallibilism: ON (reward revision)
- BFI Weight: Equal_1.0x (standard)
- **Expected YPA:** MdN ~6, CT ~6

**Seeker Mode:**
- Parity: ON (enforce symmetry)
- PF: Composite_70_30 (meaning-first)
- Fallibilism: ON (reward revision)
- BFI Weight: Equal_1.0x (standard)
- **Expected YPA:** MdN ~5, CT ~7

**Zealot Mode:**
- Parity: ON (enforce symmetry)
- PF: Holistic_50_50 (balanced)
- Fallibilism: OFF (no uncertainty bonus)
- BFI Weight: Equal_1.0x (standard)
- **Expected YPA:** MdN ~4, CT ~8

**NOTE:** Expected YPA values are HYPOTHETICAL (not yet empirically tested)

---

## 🧪 **QUIZ SYSTEM (Implementation)**

### **Location:** `pages/console.py` lines 615-665

### **Questions:**

**Q1: Evidence Priority**
- A: Prediction (→ Skeptic +2)
- B: Meaning (→ Seeker +2, Zealot +1)

**Q2: Moral Foundations**
- A: Evolved (→ Skeptic +2)
- B: Transcendent (→ Zealot +2, Seeker +1)

**Q3: Uncertainty Tolerance**
- A: Comfortable (→ Skeptic +2, Diplomat +1)
- B: Prefer certainty (→ Zealot +2)

**Q4: Success Explanation**
- A: Approximates reality (→ Skeptic +2)
- B: Reveals patterns (→ Seeker +1, Diplomat +1)

**Q5: Starting Assumptions**
- A: Minimize (→ Skeptic +2)
- B: Embrace necessary ones (→ Zealot +1, Seeker +1)

### **Scoring:**
```python
scores = {
    'skeptic': 0,
    'diplomat': 0,
    'seeker': 0,
    'zealot': 0
}

# Tally based on answers
# Highest score wins
# Ties go to Diplomat (default)
```

---

## 📊 **DATA FLOW**

### **User Session Flow:**

```
1. Landing Page (landing.py)
   ↓
2. Click "Launch Console"
   ↓
3. Console Loads (console.py)
   ↓
4. User adjusts levers OR selects preset mode
   ↓
5. Click "Run Analysis"
   ↓
6. calculations.ypa_scenario_scores() called
   ↓
7. Guardrails checked
   ↓
8. Results displayed in Results tab
   ↓
9. Charts generated (visualizations.py)
   ↓
10. Guardrails tab shows all 4 checks
```

---

## 🔧 **KEY FUNCTIONS REFERENCE**

### **calculations.py**

```python
def ypa_scenario_scores(framework_dict, lever_states, scenarios):
    """
    Calculate YPA score for a framework
    
    Args:
        framework_dict: {CCI, DEP, PF, BAE, MEF, BFI}
        lever_states: {parity, pf_type, fallibilism, bfi_weight}
        scenarios: {scenario_name: weight}
    
    Returns:
        {ypa: float, details: dict}
    """

def guardrail_lever_coupling(framework_dict):
    """Check PF vs CCI coupling"""

def guardrail_bfi_sensitivity(ypa_delta, bfi_delta):
    """Check axiom sensitivity"""

def guardrail_weight_inversion(scenario_weights):
    """Check scenario weight extremes"""

def symmetry_audit(fw1, fw2, levers):
    """Calculate toggle sensitivity"""
```

### **visualizations.py**

```python
def create_lever_comparison_chart(mdn_ypa, ct_ypa):
    """Bar chart comparing YPA scores"""

def create_ypa_trinity_chart(mdn_data, ct_data):
    """Trinity diagram with scenarios"""
```

---

## 🎯 **CALIBRATION TARGETS (For VuDu Mission)**

### **What We Need to Define:**

**1. YPA Spread Between Modes:**
- How much should Skeptic favor MdN? (2 YPA? 4 YPA?)
- How much should Zealot favor CT?
- Should Diplomat be exactly equal?
- What's acceptable tolerance? (±0.5 YPA?)

**2. Lever Value Justifications:**
- Why Skeptic Parity OFF not ON?
- Why Zealot Fallibilism OFF?
- Why Seeker 70/30 not 65/35 or 75/25?
- Why BFI 1.2x not 1.3x or 1.1x?

**3. Symmetry Requirements:**
- If Skeptic has X, should Zealot have opposite?
- Or are asymmetries philosophically justified?

**4. Empirical Validation:**
- Run each mode, measure actual YPA
- Compare to expected/claimed behavior
- Document discrepancies

---

## 📁 **FILE DEPENDENCIES (Import Map)**

```
app.py
├── pages.landing
├── pages.console
│   └── utils.calculations (core logic)
│   └── utils.visualizations (charts)
│   └── utils.frameworks (default configs)
├── pages.manual
├── pages.about
└── pages.brute_ledger

utils.calculations
├── numpy (math)
└── pandas (data)

utils.visualizations
└── plotly (charts)

utils.frameworks
└── (no deps, pure data)
```

---

## ⚙️ **DEPLOYMENT DETAILS**

**Streamlit Cloud Configuration:**
- Python: 3.11
- Main file: app.py
- Port: 8501 (default)
- Auto-deploys on GitHub push

**Local Testing:**
```bash
streamlit run app.py
```

**Environment:**
- No secrets required
- No external APIs
- Pure Python calculation

---

## 🎯 **AUDITOR ACTION ITEMS**

### **For Mode Calibration:**

**Claude (Teleological):**
- Review each mode's philosophical intent
- Verify lever choices serve archetype goals
- Propose teleologically-justified values

**Grok (Empirical):**
- Run YPA tests with current configurations
- Measure actual vs expected behavior
- Challenge unjustified assumptions with data

**Nova (Symmetry):**
- Compare Skeptic ↔ Zealot symmetry
- Verify Diplomat as true center
- Flag asymmetries (justified or violations)

---

## ✅ **TECHNICAL SPEC COMPLETE**

**This document provides:**
- ✅ Complete architecture overview
- ✅ Detailed lever mechanics
- ✅ Full guardrail specifications
- ✅ YPA calculation breakdown
- ✅ Preset mode implementations
- ✅ Quiz system logic
- ✅ Data flow mapping
- ✅ Function reference
- ✅ Calibration targets

**Ready for:** Deep technical analysis, VuDu collaboration, mode calibration

---

**Version:** v3.5.1  
**Last Updated:** October 26, 2025  
**Status:** Complete ✅
