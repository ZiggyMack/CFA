"""
CFA v2.0 - Core Calculation Utilities
All math and scoring logic in one place
"""

# deps: ypa_calculation, preset_modes

from typing import Dict, Tuple, List

PF_TYPES = ["Instrumental", "Composite_70_30", "Holistic_50_50"]
BFI_WEIGHTS = ["Equal_1.0x", "Weighted_1.2x"]

def composite_pf(pf_inst: float, pf_exist: float, pf_type: str) -> float:
    """Calculate composite pragmatic fertility score"""
    if pf_type == "Instrumental":
        return pf_inst
    if pf_type == "Holistic_50_50":
        return 0.5 * pf_inst + 0.5 * pf_exist
    return 0.7 * pf_inst + 0.3 * pf_exist

def apply_fallibilism_bonus(cci: float, bonus: str, admitted_limits: bool = True) -> float:
    """Apply fallibilism bonus if configured"""
    if bonus == "ON" and admitted_limits:
        return min(cci + 0.3, 10.0)
    return cci

def parity_weight(mg: float, parity: str) -> float:
    """Apply parity weighting to moral generativity"""
    return mg if parity == "ON" else 0.5 * mg

def bfi_total(axioms: int, debts: int, debt_weight: str) -> float:
    """Calculate total brute-fact index"""
    w = 1.0 if debt_weight == "Equal_1.0x" else 1.2
    return axioms + w * debts

def ypa_scenario_scores(fr: Dict, cfg: Dict) -> Tuple[Dict, Dict, float]:
    """
    Calculate YPA scores across all scenarios
    Returns: (results_dict, lever_map, bfi)

    Note: Crux Impasses toggle (cfg["include_crux"]) available but not yet implemented.
    Implementation pending pilot data (CT↔MdN audit) which will provide:
    - Baseline convergence metrics (with Crux)
    - Counterfactual metrics (without Crux)
    - Actual Crux declarations and their impact on scoring

    When implemented: If include_crux=False, apply penalty to metrics that had
    Crux declarations (simulating what scores would be without impasse resolution).
    """
    CCI = apply_fallibilism_bonus(
        fr["levers"]["CCI"],
        cfg["fallibilism_bonus"],
        fr.get("admits_limits", True)
    )
    EDB = fr["levers"]["EDB"]
    PF = composite_pf(
        fr["levers"]["PF_instrumental"],
        fr["levers"]["PF_existential"],
        cfg["pf_type"]
    )
    AR = fr["levers"]["AR"]
    MG = parity_weight(fr["levers"]["MG"], cfg["lever_parity"])

    # TODO: Apply Crux impact when cfg["include_crux"] == False
    # Example logic (when pilot data available):
    # if not cfg.get("include_crux", True):
    #     # Apply penalty to metrics with declared Crux
    #     if fr.get("crux_metrics"):  # List of metrics with Crux declarations
    #         for metric in fr["crux_metrics"]:
    #             if metric == "BFI":
    #                 # Increase BFI penalty (impasse means more unresolved assumptions)
    #                 pass
    #             elif metric in ["CCI", "EDB", "PF", "AR", "MG"]:
    #                 # Reduce lever score (impasse means lower convergence)
    #                 pass

    scenarios_weights = {
        "Neutral": {"CCI": 1.0, "EDB": 1.0, "PF": 1.0, "AR": 1.0, "MG": 1.0},
        "Existential": {"CCI": 1.0, "EDB": 2.0, "PF": 1.0, "AR": 1.0, "MG": 2.0},
        "Empirical": {"CCI": 1.5, "EDB": 1.0, "PF": 2.0, "AR": 1.0, "MG": 1.0},
    }

    lever_map = {"CCI": CCI, "EDB": EDB, "PF": PF, "AR": AR, "MG": MG}
    bfi = bfi_total(fr["bf_i"]["axioms"], fr["bf_i"]["debts"], cfg["bfi_debt_weight"])

    results = {}
    for name, weights in scenarios_weights.items():
        total = sum(lever_map[k] * w for k, w in weights.items())
        results[name] = {"total": total, "YPA": total / bfi if bfi > 0 else 0}

    return results, lever_map, bfi

def guardrail_lever_coupling(PF: float, CCI: float) -> Tuple[bool, str]:
    """Check lever coupling guardrail"""
    if PF >= 9 and CCI < 6.5:
        return False, f"⚠️ WARNING: PF={PF:.2f} >= 9 but CCI={CCI:.2f} < 6.5"
    return True, f"✅ PASS: Lever-Coupling satisfied"

def guardrail_bfi_sensitivity(results_neutral: float, bfi: float, results_empirical: float = None, results_existential: float = None) -> Tuple[bool, str]:
    """
    Prevents axiom inflation abuse by checking if YPA increases faster than BFI grows.
    Rule: ΔYPA/ΔBFI should not exceed 0.4
    """
    ratio = results_neutral / bfi if bfi > 0 else 0
    
    # Flag if efficiency is suspiciously high (>0.4) with large BFI (>12)
    if bfi > 12 and ratio > 0.4:
        return False, f"⚠️ WARNING: High BFI ({bfi:.1f}) with high efficiency (YPA={results_neutral:.2f}, ratio={ratio:.2f})"
    
    # Also check if empirical/existential scenarios diverge too much from neutral
    if results_empirical and results_existential:
        max_ypa = max(results_neutral, results_empirical, results_existential)
        min_ypa = min(results_neutral, results_empirical, results_existential)
        delta_ypa = max_ypa - min_ypa
        
        # Rough heuristic: if ΔYPA across scenarios > 0.4 × BFI, flag it
        if delta_ypa > 0.4 * bfi:
            return False, f"⚠️ WARNING: Large YPA variance across scenarios (ΔYPA={delta_ypa:.2f}, threshold=0.4×BFI={0.4*bfi:.2f})"
    
    return True, f"✅ PASS: BFI-Sensitivity satisfied (BFI={bfi:.1f}, Neutral YPA={results_neutral:.2f})"

def guardrail_weight_inversion(results: Dict, neutral_ypa: float) -> Tuple[bool, str]:
    """
    Detects extreme scenario manipulation.
    Rule: Flag if any scenario YPA is <0.3× or >3× Neutral YPA
    """
    flags = []
    
    for scenario in ["Existential", "Empirical"]:
        if scenario not in results:
            continue
        
        scenario_ypa = results[scenario]["YPA"]
        ratio = scenario_ypa / neutral_ypa if neutral_ypa > 0 else 0
        
        if ratio < 0.3:
            flags.append(f"{scenario} YPA ({scenario_ypa:.2f}) is <0.3× Neutral ({neutral_ypa:.2f})")
        elif ratio > 3.0:
            flags.append(f"{scenario} YPA ({scenario_ypa:.2f}) is >3× Neutral ({neutral_ypa:.2f})")
    
    if flags:
        return False, "⚠️ WARNING: " + "; ".join(flags)
    
    return True, f"✅ PASS: Weight-Inversion satisfied (all scenarios within 0.3-3× Neutral)"

def symmetry_audit(fr: Dict, cfg: Dict) -> List[Tuple[str, float, float, float]]:
    """
    Run symmetry audit by testing toggle inversions
    Returns list of (toggle_name, baseline, flipped, delta)
    """
    def get_ypa(framework, config):
        results, _, _ = ypa_scenario_scores(framework, config)
        return results["Neutral"]["YPA"]
    
    baseline = get_ypa(fr, cfg)
    reports = []

    # Test lever parity
    cfg_parity = cfg.copy()
    cfg_parity["lever_parity"] = "OFF" if cfg["lever_parity"] == "ON" else "ON"
    delta_parity = get_ypa(fr, cfg_parity) - baseline
    reports.append(("Lever-Parity", baseline, get_ypa(fr, cfg_parity), delta_parity))
    
    # Test PF types
    for pf_type in PF_TYPES:
        if pf_type == cfg["pf_type"]:
            continue
        cfg_pf = cfg.copy()
        cfg_pf["pf_type"] = pf_type
        delta_pf = get_ypa(fr, cfg_pf) - baseline
        reports.append((f"PF->{pf_type}", baseline, get_ypa(fr, cfg_pf), delta_pf))

    # Test fallibilism
    cfg_fall = cfg.copy()
    cfg_fall["fallibilism_bonus"] = "OFF" if cfg["fallibilism_bonus"] == "ON" else "ON"
    delta_fall = get_ypa(fr, cfg_fall) - baseline
    reports.append(("Fallibilism", baseline, get_ypa(fr, cfg_fall), delta_fall))

    # Test BFI debt weighting
    cfg_bfi = cfg.copy()
    # Normalize and flip between the two supported weights
    current_bfi = cfg.get("bfi_debt_weight", "Equal_1.0x")
    current_bfi = "Weighted_1.2x" if current_bfi == "Heavier_1.2x" else current_bfi
    flipped_bfi = "Weighted_1.2x" if current_bfi == "Equal_1.0x" else "Equal_1.0x"
    cfg_bfi["bfi_debt_weight"] = flipped_bfi
    delta_bfi = get_ypa(fr, cfg_bfi) - baseline
    reports.append((f"BFI->{flipped_bfi}", baseline, get_ypa(fr, cfg_bfi), delta_bfi))

    return reports
