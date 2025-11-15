#!/usr/bin/env python3
"""
YPA Validator - Standalone Calculator for VuDu Light Framework Comparison

Purpose: Independent verification of Yield Per Axiom (YPA) calculations
         No dependencies on Streamlit or Console UI - pure calculation engine

Usage:
    python ypa_validator.py --profile profiles/worldviews/CLASSICAL_THEISM.yaml
    python ypa_validator.py --profile CT.yaml --preset skeptic
    python ypa_validator.py --compare CT.yaml MdN.yaml --preset diplomat

Author: Ziggy Mack (CFA)
Version: 1.0
License: MIT
Repository: https://github.com/ZiggyMack/CFA
"""

import argparse
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# Preset Mode Configurations (BFI Weight Multipliers)
PRESETS = {
    "skeptic": {
        "weight": 1.2,
        "description": "Empirical skepticism - axioms penalized",
        "philosophy": "Show me the data or dismiss the claim"
    },
    "seeker": {
        "weight": 1.0,
        "description": "Neutral baseline - equal treatment",
        "philosophy": "Explore all frameworks equally"
    },
    "diplomat": {
        "weight": 0.9,
        "description": "Pragmatism - debts acceptable for coherence",
        "philosophy": "Balance is wisdom, perfect is enemy of good"
    },
    "zealot": {
        "weight": 0.7,
        "description": "Conviction rewarded - strong commitments favored",
        "philosophy": "Strong convictions are features, not bugs"
    }
}


class WorldviewProfile:
    """Represents a worldview framework with axioms, debts, and lever values"""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.name = self.filepath.stem
        self.data = self._load_yaml()

        # Extract core components
        self.axioms = self.data.get('axioms', [])
        self.debts = self.data.get('debts', [])
        self.levers = self._extract_levers()

    def _load_yaml(self) -> dict:
        """Load and parse YAML worldview profile"""
        if not self.filepath.exists():
            raise FileNotFoundError(f"Profile not found: {self.filepath}")

        with open(self.filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _extract_levers(self) -> Dict[str, float]:
        """Extract lever values from profile data"""
        levers_data = self.data.get('levers', {})

        # Standard VuDu Light levers
        return {
            'CCI': levers_data.get('collective_coherence_impact', 0.0),
            'EDB': levers_data.get('epistemic_debt_burden', 0.0),
            'PF_I': levers_data.get('paternalistic_force_interventionist', 0.0),
            'PF_E': levers_data.get('paternalistic_force_epistemic', 0.0),
            'AR': levers_data.get('asymmetry_risk', 0.0),
            'MG': levers_data.get('meta_governance', 0.0)
        }

    def calculate_bfi(self, weight: float = 1.0) -> float:
        """Calculate Burden of Falsity Index (BFI)

        Formula: (axiom_count + debt_count) * weight

        Args:
            weight: Preset mode multiplier (default 1.0 = neutral)

        Returns:
            BFI value
        """
        return (len(self.axioms) + len(self.debts)) * weight

    def calculate_ypa(self, bfi: float) -> float:
        """Calculate Yield Per Axiom (YPA)

        Formula: sum(lever_values) / BFI

        Args:
            bfi: Burden of Falsity Index

        Returns:
            YPA value
        """
        lever_sum = sum(self.levers.values())

        if bfi == 0:
            raise ValueError("BFI cannot be zero (division by zero)")

        return lever_sum / bfi

    def get_summary(self, preset: str = "seeker") -> Dict:
        """Get complete calculation summary for this profile

        Args:
            preset: Preset mode name (skeptic, seeker, diplomat, zealot)

        Returns:
            Dictionary with all calculations
        """
        weight = PRESETS[preset]["weight"]
        bfi = self.calculate_bfi(weight)
        ypa = self.calculate_ypa(bfi)

        return {
            "name": self.name,
            "axiom_count": len(self.axioms),
            "debt_count": len(self.debts),
            "lever_sum": sum(self.levers.values()),
            "lever_values": self.levers,
            "preset": preset,
            "bfi_weight": weight,
            "bfi": round(bfi, 4),
            "ypa": round(ypa, 4)
        }


def print_profile_summary(summary: Dict, verbose: bool = False):
    """Pretty-print profile calculation summary"""

    print(f"\n{'='*60}")
    print(f"PROFILE: {summary['name'].upper()}")
    print(f"{'='*60}")

    print(f"\nPreset Mode: {summary['preset'].upper()} (BFI Weight: {summary['bfi_weight']}x)")

    print(f"\nAxioms: {summary['axiom_count']}")
    print(f"Debts: {summary['debt_count']}")

    if verbose:
        print(f"\nLever Values:")
        for lever, value in summary['lever_values'].items():
            print(f"  {lever}: {value}")

    print(f"\nLever Sum: {summary['lever_sum']}")
    print(f"BFI: ({summary['axiom_count']} + {summary['debt_count']}) × {summary['bfi_weight']} = {summary['bfi']}")
    print(f"YPA: {summary['lever_sum']} / {summary['bfi']} = {summary['ypa']}")

    print(f"\n{'='*60}\n")


def compare_profiles(profile1: WorldviewProfile, profile2: WorldviewProfile,
                     preset: str = "seeker", verbose: bool = False):
    """Compare two worldview profiles and show delta analysis"""

    summary1 = profile1.get_summary(preset)
    summary2 = profile2.get_summary(preset)

    delta_ypa = summary1['ypa'] - summary2['ypa']
    percent_diff = (delta_ypa / summary2['ypa']) * 100 if summary2['ypa'] != 0 else 0

    # Print individual summaries
    print_profile_summary(summary1, verbose)
    print_profile_summary(summary2, verbose)

    # Print comparison
    print(f"\n{'='*60}")
    print(f"DELTA ANALYSIS: {summary1['name']} vs {summary2['name']}")
    print(f"{'='*60}")

    print(f"\nPreset Mode: {preset.upper()} (BFI Weight: {PRESETS[preset]['weight']}x)")

    print(f"\nΔYPA: {summary1['ypa']} - {summary2['ypa']} = {delta_ypa:+.4f}")
    print(f"Percent Difference: {percent_diff:+.2f}%")

    if delta_ypa > 0:
        winner = summary1['name']
        advantage = f"{summary1['ypa']} vs {summary2['ypa']}"
    elif delta_ypa < 0:
        winner = summary2['name']
        advantage = f"{summary2['ypa']} vs {summary1['ypa']}"
    else:
        winner = "TIE"
        advantage = "Equal YPA"

    print(f"\nWinner: {winner.upper()}")
    print(f"Advantage: {advantage}")

    print(f"\n{'='*60}\n")


def run_preset_sensitivity(profile1: WorldviewProfile, profile2: WorldviewProfile):
    """Run both profiles through all 4 preset modes and show variation"""

    print(f"\n{'='*60}")
    print(f"PRESET MODE SENSITIVITY ANALYSIS")
    print(f"{profile1.name} vs {profile2.name}")
    print(f"{'='*60}\n")

    print(f"{'Preset':<12} {'Weight':<8} {profile1.name+' YPA':<15} {profile2.name+' YPA':<15} {'ΔYPA':<10}")
    print(f"{'-'*60}")

    deltas = []

    for preset_name in ["zealot", "diplomat", "seeker", "skeptic"]:
        weight = PRESETS[preset_name]["weight"]

        s1 = profile1.get_summary(preset_name)
        s2 = profile2.get_summary(preset_name)

        delta = s1['ypa'] - s2['ypa']
        deltas.append(delta)

        print(f"{preset_name.capitalize():<12} {weight:<8.2f} {s1['ypa']:<15.4f} {s2['ypa']:<15.4f} {delta:+.4f}")

    swing = max(deltas) - min(deltas)
    variation_pct = (swing / min(deltas)) * 100 if min(deltas) != 0 else 0

    print(f"{'-'*60}")
    print(f"\nPreset Swing: {max(deltas):.4f} - {min(deltas):.4f} = {swing:.4f}")
    print(f"Variation: {variation_pct:.1f}% (relative to minimum delta)")

    print(f"\n{'='*60}\n")


def main():
    """Main CLI entry point"""

    parser = argparse.ArgumentParser(
        description="YPA Validator - Standalone VuDu Light Calculator",
        epilog="Example: python ypa_validator.py --compare CT.yaml MdN.yaml --preset skeptic"
    )

    parser.add_argument(
        '--profile',
        type=str,
        help='Single worldview profile to validate (YAML file)'
    )

    parser.add_argument(
        '--compare',
        nargs=2,
        metavar=('PROFILE1', 'PROFILE2'),
        help='Compare two worldview profiles'
    )

    parser.add_argument(
        '--preset',
        type=str,
        choices=['skeptic', 'seeker', 'diplomat', 'zealot'],
        default='seeker',
        help='Preset mode (default: seeker = neutral 1.0x)'
    )

    parser.add_argument(
        '--sensitivity',
        action='store_true',
        help='Run preset sensitivity analysis (all 4 modes)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed lever values'
    )

    parser.add_argument(
        '--list-presets',
        action='store_true',
        help='List all preset modes and their configurations'
    )

    args = parser.parse_args()

    # List presets and exit
    if args.list_presets:
        print("\nAvailable Preset Modes:\n")
        for name, config in PRESETS.items():
            print(f"{name.upper():<10} (Weight: {config['weight']}x)")
            print(f"  {config['description']}")
            print(f"  Philosophy: \"{config['philosophy']}\"\n")
        sys.exit(0)

    # Single profile validation
    if args.profile:
        try:
            profile = WorldviewProfile(args.profile)
            summary = profile.get_summary(args.preset)
            print_profile_summary(summary, args.verbose)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Profile comparison
    elif args.compare:
        try:
            profile1 = WorldviewProfile(args.compare[0])
            profile2 = WorldviewProfile(args.compare[1])

            if args.sensitivity:
                run_preset_sensitivity(profile1, profile2)
            else:
                compare_profiles(profile1, profile2, args.preset, args.verbose)

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
