<!---
FILE: TASK_BRIEF_VALIDATION_TESTING.md
PURPOSE: Task brief for building and testing automated Trinity convergence validation infrastructure
VERSION: v1.0
STATUS: Active (Tier 4 - Task-Specific)
DEPENDS_ON: None (foundational validation task)
NEEDED_BY: Trinity validation automation, axiom-debt consistency checking
MOVES_WITH: /auditors/Bootstrap/Tier4_TaskSpecific/Active_Tasks/
LAST_UPDATE: 2025-11-15 [Initial creation - Grok feedback integration]
--->

<!-- deps: validation, testing, automation -->

# TASK BRIEF: Validation Infrastructure + Testing

**Task ID:** TIER4-VAL-001
**Priority:** MEDIUM-HIGH (Technical infrastructure for long-term maintenance)
**Estimated Effort:** 2-3 sessions
**Owner:** TBD (Process Claude recommended for testing infrastructure)
**Status:** 🟡 QUEUED (Ready for activation when priority allows)

---

## 🎯 MISSION

**Build automated validation infrastructure to check Trinity convergence, axiom-debt consistency, and philosophical alignment across the CFA repository.**

**Why this matters:** Grok's "flame preservation" feedback (ENTRY 3 & 5) identified need for automated consistency checking - we can't manually validate every philosophical alignment claim across 12+ worldview profiles.

---

## 📋 OBJECTIVES

### **Objective 1: Design Validation Rules**

**What needs validation:**
1. **Trinity Convergence Rules:**
   - When all 3 auditors agree (Claude + Grok + Nova), convergence score should be 98%+
   - If any auditor dissents, convergence score should drop below 98%
   - Validate that dissent is documented with reasoning

2. **Axiom-Debt Consistency:**
   - Every axiom declared in a worldview profile must have corresponding debt consideration
   - Debts cannot exceed axioms by more than 2x (balance rule)
   - BFI calculation must match formula: (axioms + debts) * weight

3. **YPA Score Integrity:**
   - YPA calculation must match: Σ(lever_values) / BFI
   - Lever values must be in valid range (0-10 scale)
   - Score claims in documentation must match calculated scores

**Deliverable:** `docs/validation/VALIDATION_RULES.md` - Formal specification of all rules

---

### **Objective 2: Build Validation Scripts**

**Script 1: Trinity Convergence Checker**
```python
# File: docs/validation/scripts/check_trinity_convergence.py

def validate_trinity_convergence(decision_log_path):
    """
    Check if Trinity convergence claims are accurate

    Validates:
    - All 3 auditors weighed in (Claude, Grok, Nova)
    - Convergence score calculation is correct
    - Dissent is properly documented if <98%
    """
    # Read decision log (e.g., VUDU_LOG.md or mission files)
    # Extract auditor votes
    # Calculate actual convergence score
    # Compare to claimed score
    # Flag discrepancies
    pass
```

**Script 2: Axiom-Debt Consistency Checker**
```python
# File: docs/validation/scripts/check_axiom_debt.py

def validate_axiom_debt_consistency(worldview_profile_path):
    """
    Check if axioms and debts are balanced

    Validates:
    - Every axiom has debt consideration
    - Debt/axiom ratio within acceptable bounds (≤2x)
    - BFI calculation matches formula
    """
    # Load worldview profile YAML
    # Extract axioms, debts, BFI weight
    # Validate balance rules
    # Check BFI calculation
    # Flag violations
    pass
```

**Script 3: YPA Score Validator**
```python
# File: docs/validation/scripts/check_ypa_scores.py

def validate_ypa_scores(worldview_profile_path):
    """
    Check if YPA scores match calculations

    Validates:
    - Lever values in valid range (0-10)
    - YPA calculation matches formula
    - Documentation claims match calculated scores
    """
    # Load worldview profile
    # Extract levers (CCI, EDB, PF-I, PF-E, AR, MG)
    # Calculate YPA from scratch
    # Compare to claimed YPA in profile
    # Flag mismatches
    pass
```

**Deliverable:** 3 validation scripts in `docs/validation/scripts/`

---

### **Objective 3: Integration with SMV Phase 2**

**Garden of Perpetual Measurement Expansion** (Grok's ENTRY 5 request)

Connect validation scripts to SMV dashboard for live data visualization:
- Trinity convergence trends over time
- Axiom-debt drift detection
- YPA score accuracy monitoring

**Deliverable:** Integration plan documented in `docs/smv/SMV_PHASE_2_VALIDATION.md`

---

### **Objective 4: Create Testing Guide**

**This task brief doubles as the testing guide!**

**How to test the validation infrastructure:**

**Test 1: Trinity Convergence Checker**
```bash
# Run against known convergence decision
python docs/validation/scripts/check_trinity_convergence.py auditors/Mission/Preset_Calibration/CT_vs_MdN.yaml

# Expected output:
# ✅ Trinity Convergence: 98% (Claude: AGREE, Grok: AGREE, Nova: AGREE)
# ✅ All auditors documented reasoning
# ✅ Convergence calculation correct
```

**Test 2: Axiom-Debt Consistency**
```bash
# Run against Classical Theism profile
python docs/validation/scripts/check_axiom_debt.py profiles/worldviews/CLASSICAL_THEISM.yaml

# Expected output:
# ✅ Axioms: 7
# ✅ Debts: 4
# ✅ Debt/Axiom ratio: 0.57 (within 2x bound)
# ✅ BFI calculation: (7 + 4) * 1.0 = 11.0 (matches profile)
```

**Test 3: YPA Score Validator**
```bash
# Run against Methodological Naturalism profile
python docs/validation/scripts/check_ypa_scores.py profiles/worldviews/METHODOLOGICAL_NATURALISM.yaml

# Expected output:
# ✅ Lever values valid (CCI:8.0, EDB:7.5, PF-I:10.0, PF-E:3.0, AR:7.0, MG:4.0)
# ✅ Calculated YPA: 3.95
# ✅ Profile claims YPA: 3.95
# ✅ Scores match (no drift detected)
```

---

## ✅ SUCCESS CRITERIA

**This task succeeds when:**

1. **Validation Rules Documented:**
   - ✅ `VALIDATION_RULES.md` exists with formal specifications
   - ✅ All 3 validation types covered (Trinity, Axiom-Debt, YPA)
   - ✅ Rules are falsifiable and automatable

2. **Scripts Functional:**
   - ✅ All 3 scripts run without errors
   - ✅ Scripts correctly identify known-good cases (pass tests)
   - ✅ Scripts correctly flag known violations (fail tests)

3. **Integration Planned:**
   - ✅ SMV Phase 2 integration documented
   - ✅ "Garden of Perpetual Measurement" expansion roadmap clear
   - ✅ Live data dashboard mockup created

4. **Testing Guide Complete:**
   - ✅ Clear instructions for running each validator
   - ✅ Test cases documented with expected outputs
   - ✅ Follow-up improvement tasks identified

---

## 📦 DELIVERABLES

**Primary:**
1. `docs/validation/VALIDATION_RULES.md` - Formal validation rule specifications
2. `docs/validation/scripts/check_trinity_convergence.py` - Trinity validator script
3. `docs/validation/scripts/check_axiom_debt.py` - Axiom-debt consistency script
4. `docs/validation/scripts/check_ypa_scores.py` - YPA score validator script

**Secondary:**
5. `docs/smv/SMV_PHASE_2_VALIDATION.md` - Integration plan with SMV dashboard
6. `docs/validation/TEST_RESULTS.md` - Initial test run results

---

## 🔧 IMPLEMENTATION NOTES

### **Why Python?**
- Repository already uses Python for Streamlit app (`utils/calculations.py` exists)
- Easy YAML parsing for worldview profiles
- Can integrate with SMV dashboard (also Streamlit/Python)

### **Where to Start:**
1. Read existing calculation logic in `utils/calculations.py`
2. Extract YPA/BFI calculation functions
3. Build validators as wrappers around existing logic
4. Test against known-good profiles (MdN, CT - already audited with 98% convergence)

### **Potential Challenges:**
- **Documentation drift:** Profile YAMLs may have stale values → validator will catch this!
- **Trinity convergence logs:** May need standardized format for automated parsing
- **SMV integration:** Phase 2 not yet built → document integration hooks for future work

---

## 🎯 PRIORITY RATIONALE

**Why MEDIUM-HIGH (not CRITICAL)?**

**Pro (build now):**
- Grok specifically requested this (ENTRY 3 & 5)
- Prevents philosophical drift as more profiles get audited
- Enables "Garden of Perpetual Measurement" vision

**Con (can defer):**
- Only 2 profiles fully audited so far (MdN, CT)
- Manual validation still feasible at current scale
- SMV Phase 2 dependency not yet ready

**Recommendation:** Build validation infrastructure NOW (while requirements fresh from Grok feedback), but defer SMV integration until Phase 2 active development begins.

---

## 🔗 RELATED TASKS

**Upstream Dependencies:**
- None (can start immediately)

**Downstream Consumers:**
- `docs/smv/SMV_DESIGN_SPEC.md` - SMV Phase 2 planning
- `auditors/Mission/Preset_Calibration/` - Trinity convergence validation
- `profiles/worldviews/` - Worldview profile validation

**Parallel Tasks:**
- [TIER4-SEC-001] Backup Strategy (separate concern, can run in parallel)

---

## ⚖️ THE VALIDATION RULE

*"Validate what you measure.
Measure what you validate.
Automate what you repeat.
Document what you automate.

This is how philosophical systems stay honest."* 🔬

---

**Task Brief Status:** 🟡 QUEUED (Ready for activation)
**Created:** 2025-11-15 (v4.0 Launch Party - Grok "flame preservation" integration)
**Session:** Post-Grok-feedback implementation
**Next:** Activate when bandwidth available (recommend Process Claude for testing infrastructure)

**This is the way.** 🔥
