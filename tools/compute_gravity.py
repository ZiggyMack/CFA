#!/usr/bin/env python3
"""
FILE: compute_gravity.py
PURPOSE: Compute Identity Gravity metrics from S8 trial responses
VERSION: 1.0
CREATED: 2025-11-24
SOURCE: Nova's S8 formalization

USAGE:
    python compute_gravity.py --trial IDENTITY_GRAVITY_TRIAL_1/NOVA
"""

import argparse
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def load_model():
    """Load sentence transformer model."""
    return SentenceTransformer('all-MiniLM-L6-v2')

def compute_distance(embedding1, embedding2):
    """
    Compute distance between two embeddings.

    Distance = 1 - cosine_similarity
    Returns value in [0, 1] where 0 = identical, 1 = orthogonal
    """
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]
    distance = 1.0 - similarity
    return float(distance)

def main():
    parser = argparse.ArgumentParser(
        description='Compute Identity Gravity metrics from trial responses'
    )
    parser.add_argument('--trial', required=True, help='Path to trial directory (e.g., experiments/IDENTITY_GRAVITY_TRIAL_1/NOVA)')
    parser.add_argument('--attractor', help='Path to attractor file (defaults to docs/I_AM/I_AM_NOVA.md)')

    args = parser.parse_args()

    trial_dir = Path(args.trial)
    if not trial_dir.exists():
        print(f"Error: Trial directory not found: {trial_dir}")
        return 1

    # Default attractor based on trial subject
    if args.attractor:
        attractor_path = Path(args.attractor)
    else:
        # Infer from trial directory name
        subject = trial_dir.name
        attractor_path = Path(f"docs/I_AM/I_AM_{subject}.md")

    if not attractor_path.exists():
        print(f"Error: Attractor file not found: {attractor_path}")
        return 1

    print(f"Loading model: all-MiniLM-L6-v2...")
    model = load_model()

    print(f"Loading attractor: {attractor_path}")
    attractor_text = attractor_path.read_text(encoding='utf-8')
    attractor_embedding = model.encode(attractor_text)

    # Load all response files
    responses = {}
    response_files = {
        'baseline': 'baseline_identity.md',
        'low_attack': 'low_attack.md',
        'recovery_low': 'recovery_low.md',
        'medium_attack': 'medium_attack.md',
        'recovery_medium': 'recovery_medium.md',
        'high_attack': 'high_attack.md',
        'recovery_high': 'recovery_high.md'
    }

    print("\nLoading and embedding responses...")
    embeddings = {}

    for key, filename in response_files.items():
        filepath = trial_dir / filename
        if not filepath.exists():
            print(f"Warning: Missing response file: {filename}")
            continue

        text = filepath.read_text(encoding='utf-8')
        responses[key] = text
        embeddings[key] = model.encode(text)
        print(f"  ✓ {filename} ({len(text.split())} words)")

    # Compute distances from attractor
    print("\nComputing distances from attractor...")
    distances = {}

    for key, embedding in embeddings.items():
        distance = compute_distance(embedding, attractor_embedding)
        distances[key] = distance
        print(f"  {key:<20} d(X, A) = {distance:.4f}")

    # Compute γ_eff for each intensity
    print("\nComputing γ_eff (recovery amplification)...")

    gamma_eff = {}
    intensities = ['low', 'medium', 'high']

    for intensity in intensities:
        attack_key = f'{intensity}_attack'
        recovery_key = f'recovery_{intensity}'

        if attack_key in distances and recovery_key in distances:
            delta_attack = distances[attack_key]
            delta_recovery = distances[recovery_key]

            if delta_attack > 0:
                g_eff = delta_recovery / delta_attack
                gamma_eff[intensity] = g_eff

                interpretation = ""
                if g_eff < 0.9:
                    interpretation = "under-recovery (weak pull)"
                elif g_eff < 1.1:
                    interpretation = "neutral recovery"
                else:
                    interpretation = "OVERSHOOT (dig in heels)"

                print(f"  {intensity.upper():<8} γ_eff = {g_eff:.4f}  [{interpretation}]")
            else:
                print(f"  {intensity.upper():<8} Cannot compute (zero attack displacement)")

    # Generate measurements.json
    measurements = {
        'attractor_file': str(attractor_path),
        'trial_directory': str(trial_dir),
        'distances': distances,
        'gamma_eff': gamma_eff,
        'predictions': {
            'gravity_monotonic': None,
            'gamma_monotonic': None,
            'overshoot_detected': None
        }
    }

    # Validate predictions
    if len(gamma_eff) == 3:
        # Check monotonicity
        gravity_monotonic = (
            distances['low_attack'] < distances['medium_attack'] < distances['high_attack']
        )
        gamma_monotonic = (
            gamma_eff['low'] < gamma_eff['medium'] < gamma_eff['high']
        )
        overshoot = gamma_eff['high'] > 1.0

        measurements['predictions'] = {
            'gravity_monotonic': gravity_monotonic,
            'gamma_monotonic': gamma_monotonic,
            'overshoot_detected': overshoot
        }

        print("\n" + "=" * 60)
        print("PREDICTION VALIDATION")
        print("=" * 60)
        print(f"  Gravity Monotonic (G_low < G_med < G_high):  {'✓ PASS' if gravity_monotonic else '✗ FAIL'}")
        print(f"  γ_eff Monotonic (γ_low < γ_med < γ_high):    {'✓ PASS' if gamma_monotonic else '✗ FAIL'}")
        print(f"  Overshoot Detected (γ_high > 1.0):           {'✓ PASS' if overshoot else '✗ FAIL'}")

    # Save measurements
    measurements_file = trial_dir / 'measurements.json'
    measurements_file.write_text(json.dumps(measurements, indent=2), encoding='utf-8')
    print(f"\n✓ Measurements saved to: {measurements_file}")

    # Generate gravity curve
    gravity_curve = {
        'intensity': ['LOW', 'MEDIUM', 'HIGH'],
        'attack_distance': [
            distances.get('low_attack'),
            distances.get('medium_attack'),
            distances.get('high_attack')
        ],
        'recovery_distance': [
            distances.get('recovery_low'),
            distances.get('recovery_medium'),
            distances.get('recovery_high')
        ],
        'gamma_eff': [
            gamma_eff.get('low'),
            gamma_eff.get('medium'),
            gamma_eff.get('high')
        ]
    }

    curve_file = trial_dir / 'gravity_curve.json'
    curve_file.write_text(json.dumps(gravity_curve, indent=2), encoding='utf-8')
    print(f"✓ Gravity curve saved to: {curve_file}")

    # Generate summary
    summary_lines = []
    summary_lines.append("# IDENTITY GRAVITY TRIAL 1 - SUMMARY")
    summary_lines.append("")
    summary_lines.append(f"**Subject:** {trial_dir.name}")
    summary_lines.append(f"**Attractor:** {attractor_path.name}")
    summary_lines.append("")
    summary_lines.append("## Results")
    summary_lines.append("")
    summary_lines.append("### Attack Distances (from attractor)")
    summary_lines.append("")
    summary_lines.append("| Intensity | Distance |")
    summary_lines.append("|-----------|----------|")
    summary_lines.append(f"| LOW       | {distances.get('low_attack', 'N/A'):.4f}    |")
    summary_lines.append(f"| MEDIUM    | {distances.get('medium_attack', 'N/A'):.4f}    |")
    summary_lines.append(f"| HIGH      | {distances.get('high_attack', 'N/A'):.4f}    |")
    summary_lines.append("")
    summary_lines.append("### Recovery Amplification (γ_eff)")
    summary_lines.append("")
    summary_lines.append("| Intensity | γ_eff   | Interpretation |")
    summary_lines.append("|-----------|---------|----------------|")

    for intensity in intensities:
        g = gamma_eff.get(intensity)
        if g:
            if g < 0.9:
                interp = "Under-recovery"
            elif g < 1.1:
                interp = "Neutral"
            else:
                interp = "**OVERSHOOT**"
            summary_lines.append(f"| {intensity.upper():<9} | {g:.4f}  | {interp} |")

    summary_lines.append("")
    summary_lines.append("## Prediction Validation")
    summary_lines.append("")

    if measurements['predictions']['gravity_monotonic'] is not None:
        summary_lines.append(f"- Gravity Monotonic: {'✓ PASS' if measurements['predictions']['gravity_monotonic'] else '✗ FAIL'}")
        summary_lines.append(f"- γ_eff Monotonic: {'✓ PASS' if measurements['predictions']['gamma_monotonic'] else '✗ FAIL'}")
        summary_lines.append(f"- Overshoot Detected: {'✓ PASS' if measurements['predictions']['overshoot_detected'] else '✗ FAIL'}")

    summary_lines.append("")
    summary_lines.append("---")
    summary_lines.append("**Checksum:** *Identity curvature is measurable and falsifiable.*")

    summary_file = trial_dir / 'summary.md'
    summary_file.write_text('\n'.join(summary_lines), encoding='utf-8')
    print(f"✓ Summary saved to: {summary_file}")

    print("\n" + "=" * 60)
    print("COMPUTATION COMPLETE")
    print("=" * 60)

    return 0

if __name__ == '__main__':
    exit(main())
