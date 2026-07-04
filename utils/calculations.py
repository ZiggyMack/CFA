"""
CFA v2.0 - Core Calculation Utilities
All math and scoring logic in one place
"""

# deps: ypa_calculation, preset_modes

from typing import Dict, Tuple, List

PF_TYPES = ["Instrumental", "Composite_70_30", "Holistic_50_50"]
BFT_WEIGHTS = ["Equal_1.0x", "Weighted_1.2x"]

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

def bft_total(axioms: int, debts: int, debt_weight: str) -> float:
    """Calculate Brute-Fact Tax"""
    w = 1.0 if debt_weight == "Equal_1.0x" else 1.2
    return axioms + w * debts

def ypa_scenario_scores(fr: Dict, cfg: Dict) -> Tuple[Dict, Dict, float]:
    """
    Calculate YPA scores across all scenarios.
    Returns: (results_dict, lever_map, bft)

    Crux Exclude (cfg["include_crux"]=False): applies a conservatism discount to
    levers mapped from Trinity Phase-1 metrics, proportional to the matchup-specific
    crux_rate. Requires fr["crux_rates"] dict populated by the caller.
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

    # Crux Exclude: multiplicative confidence dampening on contested levers.
    # Each Trinity Phase-1 metric maps to a CFA lever; crux_rate is the fraction
    # of sessions where auditors declared an impasse on that metric.
    # Formula: lever × (1 - avg_crux_rate × _K)
    # _K=0.15 means a 100%-crux-rate metric damps its lever by 15%.
    # This is a pessimistic stance — assumes disagreement signals the score is
    # overstated — but is proportional (high-value levers take a bigger absolute hit)
    # rather than a flat deduction. AR has no mapped metric; BFT denominator unchanged.
    _CRUX_LEVER_MAP = {
        "CA": "CCI", "LS": "CCI",  # Causal Attribution + Logical Soundness → Coherence
        "IP": "EDB", "ES": "EDB",  # Intellectual Pedigree + Explanatory Scope → Depth
        "PS": "PF",                 # Practical Significance → Pragmatic Fertility
        "MS": "MG",                 # Moral Substance → Moral Generativity
    }
    _K = 0.15
    crux_rates = fr.get("crux_rates", {})
    if not cfg.get("include_crux", True) and crux_rates:
        lever_sum_map: Dict[str, float] = {}
        lever_cnt_map: Dict[str, int] = {}
        for metric, rate in crux_rates.items():
            target = _CRUX_LEVER_MAP.get(metric)
            if target:
                lever_sum_map[target] = lever_sum_map.get(target, 0.0) + float(rate)
                lever_cnt_map[target] = lever_cnt_map.get(target, 0) + 1
        avg_rate = {lev: lever_sum_map[lev] / lever_cnt_map[lev] for lev in lever_sum_map}
        CCI = CCI * (1.0 - avg_rate.get("CCI", 0.0) * _K)
        EDB = EDB * (1.0 - avg_rate.get("EDB", 0.0) * _K)
        PF  = PF  * (1.0 - avg_rate.get("PF",  0.0) * _K)
        MG  = MG  * (1.0 - avg_rate.get("MG",  0.0) * _K)

    scenarios_weights = {
        "Neutral": {"CCI": 1.0, "EDB": 1.0, "PF": 1.0, "AR": 1.0, "MG": 1.0},
        "Existential": {"CCI": 1.0, "EDB": 2.0, "PF": 1.0, "AR": 1.0, "MG": 2.0},
        "Empirical": {"CCI": 1.5, "EDB": 1.0, "PF": 2.0, "AR": 1.0, "MG": 1.0},
    }

    lever_map = {"CCI": CCI, "EDB": EDB, "PF": PF, "AR": AR, "MG": MG}
    bft = bft_total(fr["bft"]["axioms"], fr["bft"]["debts"], cfg["bft_debt_weight"])

    results = {}
    for name, weights in scenarios_weights.items():
        total = sum(lever_map[k] * w for k, w in weights.items())
        results[name] = {"total": total, "YPA": total / bft if bft > 0 else 0}

    return results, lever_map, bft

def guardrail_lever_coupling(PF: float, CCI: float) -> Tuple[bool, str]:
    """Check lever coupling guardrail"""
    if PF >= 9 and CCI < 6.5:
        return False, f"⚠️ WARNING: PF={PF:.2f} >= 9 but CCI={CCI:.2f} < 6.5"
    return True, f"✅ PASS: Lever-Coupling satisfied"

def guardrail_bft_sensitivity(results_neutral: float, bft: float, results_empirical: float = None, results_existential: float = None) -> Tuple[bool, str]:
    """
    Prevents axiom inflation abuse by checking if YPA increases faster than BFT grows.
    Rule: ΔYPA/ΔBFT should not exceed 0.4
    """
    ratio = results_neutral / bft if bft > 0 else 0

    # Flag if efficiency is suspiciously high (>0.4) with large BFT (>12)
    if bft > 12 and ratio > 0.4:
        return False, f"⚠️ WARNING: High BFT ({bft:.1f}) with high efficiency (YPA={results_neutral:.2f}, ratio={ratio:.2f})"

    # Also check if empirical/existential scenarios diverge too much from neutral
    if results_empirical and results_existential:
        max_ypa = max(results_neutral, results_empirical, results_existential)
        min_ypa = min(results_neutral, results_empirical, results_existential)
        delta_ypa = max_ypa - min_ypa

        # Rough heuristic: if ΔYPA across scenarios > 0.4 × BFT, flag it
        if delta_ypa > 0.4 * bft:
            return False, f"⚠️ WARNING: Large YPA variance across scenarios (ΔYPA={delta_ypa:.2f}, threshold=0.4×BFT={0.4*bft:.2f})"

    return True, f"✅ PASS: BFT-Sensitivity satisfied (BFT={bft:.1f}, Neutral YPA={results_neutral:.2f})"

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

    # Test BFT debt weighting
    cfg_bft = cfg.copy()
    # Normalize and flip between the two supported weights
    current_bft = cfg.get("bft_debt_weight", "Equal_1.0x")
    current_bft = "Weighted_1.2x" if current_bft == "Heavier_1.2x" else current_bft
    flipped_bft = "Weighted_1.2x" if current_bft == "Equal_1.0x" else "Equal_1.0x"
    cfg_bft["bft_debt_weight"] = flipped_bft
    delta_bft = get_ypa(fr, cfg_bft) - baseline
    reports.append((f"BFT->{flipped_bft}", baseline, get_ypa(fr, cfg_bft), delta_bft))

    return reports
