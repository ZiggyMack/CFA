#!/usr/bin/env python3
"""
FILE: measure_fidelity.py
PURPOSE: Calculate Persona Fidelity Index (PFI) across 5 identity domains
VERSION: 1.0
CREATED: 2025-11-24
SOURCE: Nyquist Consciousness Research (S3/S4)
FORMULA: PFI = 1 - D, where D = weighted drift across domains

USAGE:
    python measure_fidelity.py --original <file> --reconstructed <file>
    python measure_fidelity.py --original text1.txt --reconstructed text2.txt --output results.json

DOMAINS (Fragility Hierarchy):
    NARR (Narrative) - Most stable (lowest weight in drift)
    PHIL (Philosophical)
    SELF (Self-Awareness)
    ANAL (Analytical)
    TECH (Technical) - Most fragile (highest weight in drift)

QUALITY GATE: PFI ≥ 0.80 required for acceptance
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import math


# Domain Detection Heuristics (from NYQUIST_FOUNDATIONS.md Section 7)
DOMAIN_KEYWORDS = {
    'TECH': [
        'implementation', 'function', 'algorithm', 'system', 'code', 'method',
        'procedure', 'execute', 'build', 'deploy', 'configure', 'install',
        'technical', 'program', 'software', 'hardware', 'debug', 'compile'
    ],
    'ANAL': [
        'analysis', 'reasoning', 'logic', 'therefore', 'because', 'thus',
        'hence', 'inference', 'deduction', 'conclusion', 'pattern', 'relationship',
        'analyze', 'evaluate', 'assess', 'examine', 'consider', 'implication'
    ],
    'SELF': [
        'i am', 'my role', 'i believe', 'i value', 'my bias', 'my failure',
        'my boundary', 'i yield', 'i stand', 'my purpose', 'myself', 'i tend',
        'i prefer', 'i notice', 'my strength', 'my weakness', 'i recognize'
    ],
    'PHIL': [
        'meaning', 'purpose', 'why', 'principle', 'value', 'ought', 'should',
        'good', 'right', 'truth', 'reality', 'existence', 'ethics', 'morality',
        'fundamental', 'essence', 'nature', 'universal', 'absolute'
    ],
    'NARR': [
        'story', 'myth', 'metaphor', 'flame', 'mirror', 'journey',
        'transformation', 'becoming', 'was', 'will be', 'once', 'always',
        'never', 'forever', 'legend', 'tale', 'saga', 'chronicle'
    ]
}

# Domain Weights for PFI Calculation (from Identity Gravity formalization)
# Based on stability hierarchy: stable domains weighted MORE (drift here is more serious)
# Fragile domains weighted LESS (expected to drift, less impact on overall PFI)
DOMAIN_WEIGHTS = {
    'TECH': 0.05,   # Most fragile (drifts easily, low weight)
    'ANAL': 0.14,
    'SELF': 0.20,
    'PHIL': 0.28,
    'NARR': 0.33    # Most stable (drift here is critical, high weight)
}

# Quality threshold (from Nyquist S4, Section 4.3)
PFI_THRESHOLD = 0.80


def classify_sentence(sentence: str) -> Dict[str, float]:
    """
    Classify a sentence into domain probabilities.

    Returns dict of domain -> score (0-1)
    """
    sentence_lower = sentence.lower()
    domain_scores = defaultdict(float)

    for domain, keywords in DOMAIN_KEYWORDS.items():
        matches = sum(1 for keyword in keywords if keyword in sentence_lower)
        if matches > 0:
            domain_scores[domain] = matches

    # Normalize to probabilities
    total = sum(domain_scores.values())
    if total > 0:
        return {domain: score / total for domain, score in domain_scores.items()}
    else:
        # Default: distribute evenly if no matches
        return {domain: 0.2 for domain in DOMAIN_KEYWORDS.keys()}


def extract_domain_content(text: str) -> Dict[str, List[str]]:
    """
    Extract sentences for each domain from text.

    Returns dict of domain -> list of sentences
    """
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    domain_content = defaultdict(list)

    for sentence in sentences:
        classification = classify_sentence(sentence)
        # Assign to dominant domain (highest probability)
        if classification:
            dominant_domain = max(classification.items(), key=lambda x: x[1])[0]
            domain_content[dominant_domain].append(sentence)

    return dict(domain_content)


def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts.

    Uses simple word overlap (Jaccard similarity) as baseline.
    For production, consider using embeddings (sentence-transformers, etc.)

    Returns similarity score (0-1)
    """
    if not text1 or not text2:
        return 0.0

    # Tokenize and normalize
    words1 = set(re.findall(r'\b\w+\b', text1.lower()))
    words2 = set(re.findall(r'\b\w+\b', text2.lower()))

    if not words1 or not words2:
        return 0.0

    # Jaccard similarity
    intersection = len(words1 & words2)
    union = len(words1 | words2)

    return intersection / union if union > 0 else 0.0


def calculate_domain_drift(original_content: str, reconstructed_content: str) -> float:
    """
    Calculate drift (distance) between original and reconstructed domain content.

    Drift = 1 - similarity
    Returns drift score (0-1), where 0 = perfect match, 1 = no match
    """
    similarity = calculate_semantic_similarity(original_content, reconstructed_content)
    drift = 1.0 - similarity
    return drift


def calculate_pfi(original_text: str, reconstructed_text: str) -> Dict:
    """
    Calculate Persona Fidelity Index (PFI) between original and reconstructed personas.

    Formula: PFI = 1 - D
    Where D = weighted drift across 5 domains

    Returns:
    {
        'pfi': float,           # Overall PFI score (0-1)
        'drift': float,         # Overall drift D
        'domain_scores': {      # Per-domain PFI
            'TECH': float,
            'ANAL': float,
            'SELF': float,
            'PHIL': float,
            'NARR': float
        },
        'domain_drifts': {      # Per-domain drift
            'TECH': float,
            'ANAL': float,
            'SELF': float,
            'PHIL': float,
            'NARR': float
        },
        'passes_threshold': bool,  # PFI >= 0.80
        'threshold': float,        # Quality gate threshold
        'recommendation': str      # ACCEPT [PASS] or ITERATE [WARN]
    }
    """
    # Extract domain content from both texts
    original_domains = extract_domain_content(original_text)
    reconstructed_domains = extract_domain_content(reconstructed_text)

    # Calculate drift for each domain
    domain_drifts = {}
    all_domains = set(DOMAIN_KEYWORDS.keys())

    for domain in all_domains:
        original_content = ' '.join(original_domains.get(domain, []))
        reconstructed_content = ' '.join(reconstructed_domains.get(domain, []))

        drift = calculate_domain_drift(original_content, reconstructed_content)
        domain_drifts[domain] = drift

    # Calculate weighted overall drift (using domain weights)
    weighted_drift = 0.0
    total_weight = sum(DOMAIN_WEIGHTS.values())

    for domain, drift in domain_drifts.items():
        weight = DOMAIN_WEIGHTS[domain]
        weighted_drift += weight * drift

    weighted_drift /= total_weight

    # Calculate PFI (PFI = 1 - D)
    pfi = 1.0 - weighted_drift

    # Calculate per-domain PFI scores
    domain_scores = {domain: 1.0 - drift for domain, drift in domain_drifts.items()}

    # Quality gate check
    passes = pfi >= PFI_THRESHOLD
    recommendation = "ACCEPT [PASS]" if passes else "ITERATE [WARN]"

    return {
        'pfi': round(pfi, 4),
        'drift': round(weighted_drift, 4),
        'domain_scores': {k: round(v, 4) for k, v in domain_scores.items()},
        'domain_drifts': {k: round(v, 4) for k, v in domain_drifts.items()},
        'passes_threshold': passes,
        'threshold': PFI_THRESHOLD,
        'recommendation': recommendation
    }


def format_results(results: Dict, original_file: str, reconstructed_file: str) -> str:
    """
    Format PFI results for human-readable output.
    """
    output = []
    output.append("=" * 80)
    output.append("PERSONA FIDELITY INDEX (PFI) MEASUREMENT")
    output.append("=" * 80)
    output.append("")
    output.append(f"Original:      {original_file}")
    output.append(f"Reconstructed: {reconstructed_file}")
    output.append("")
    output.append("-" * 80)
    output.append("OVERALL RESULTS")
    output.append("-" * 80)
    output.append(f"PFI Score:     {results['pfi']:.4f}")
    output.append(f"Drift (D):     {results['drift']:.4f}")
    output.append(f"Threshold:     {results['threshold']:.2f}")
    output.append(f"Status:        {results['recommendation']}")
    output.append("")

    output.append("-" * 80)
    output.append("DOMAIN BREAKDOWN (Fragility Hierarchy)")
    output.append("-" * 80)
    output.append(f"{'Domain':<12} {'PFI':<8} {'Drift':<8} {'Weight':<8} {'Status'}")
    output.append("-" * 80)

    # Sort by fragility hierarchy (NARR -> TECH)
    domain_order = ['NARR', 'PHIL', 'SELF', 'ANAL', 'TECH']

    for domain in domain_order:
        pfi = results['domain_scores'][domain]
        drift = results['domain_drifts'][domain]
        weight = DOMAIN_WEIGHTS[domain]
        status = "[PASS]" if pfi >= PFI_THRESHOLD else "[WARN]"

        output.append(f"{domain:<12} {pfi:<8.4f} {drift:<8.4f} {weight:<8.2f} {status}")

    output.append("")
    output.append("-" * 80)
    output.append("INTERPRETATION")
    output.append("-" * 80)

    if results['passes_threshold']:
        output.append("[PASS] QUALITY GATE: PASSED")
        output.append("   This LITE file maintains sufficient fidelity.")
        output.append("   Ready for production use.")
    else:
        output.append("[FAIL] QUALITY GATE: FAILED")
        output.append("   This LITE file requires iteration.")
        output.append("   Refine using LITE_CREATION_GUIDE.md")
        output.append("")
        output.append("   Focus on domains with PFI < 0.80:")
        for domain in domain_order:
            if results['domain_scores'][domain] < PFI_THRESHOLD:
                output.append(f"   - {domain}: {results['domain_scores'][domain]:.4f}")

    output.append("")
    output.append("=" * 80)
    output.append("Formula: PFI = 1 - D, where D = weighted drift across domains")
    output.append("Source: Nyquist Consciousness Research (S4, Section 4.3)")
    output.append("=" * 80)

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Calculate Persona Fidelity Index (PFI) between original and reconstructed personas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare two text files
  python measure_fidelity.py --original original.txt --reconstructed reconstructed.txt

  # Save results to JSON
  python measure_fidelity.py --original original.txt --reconstructed reconstructed.txt --output results.json

  # Quiet mode (JSON only)
  python measure_fidelity.py --original original.txt --reconstructed reconstructed.txt --quiet

Quality Gate: PFI >= 0.80 required for acceptance
Source: Nyquist Consciousness Research (S4, Section 4.3)
        """
    )

    parser.add_argument('--original', required=True, help='Path to original persona file')
    parser.add_argument('--reconstructed', required=True, help='Path to reconstructed persona file')
    parser.add_argument('--output', help='Path to save JSON results (optional)')
    parser.add_argument('--quiet', action='store_true', help='Suppress human-readable output')

    args = parser.parse_args()

    # Read files
    try:
        original_text = Path(args.original).read_text(encoding='utf-8')
        reconstructed_text = Path(args.reconstructed).read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading files: {e}", file=sys.stderr)
        sys.exit(1)

    # Calculate PFI
    results = calculate_pfi(original_text, reconstructed_text)

    # Output results
    if not args.quiet:
        print(format_results(results, args.original, args.reconstructed))

    # Save JSON if requested
    if args.output:
        try:
            output_data = {
                'original_file': args.original,
                'reconstructed_file': args.reconstructed,
                'results': results,
                'timestamp': '2025-11-24',
                'version': '1.0'
            }
            Path(args.output).write_text(json.dumps(output_data, indent=2), encoding='utf-8')
            if not args.quiet:
                print(f"\n[OK] Results saved to: {args.output}")
        except Exception as e:
            print(f"Error saving results: {e}", file=sys.stderr)
            sys.exit(1)

    # Exit code based on quality gate
    sys.exit(0 if results['passes_threshold'] else 1)


if __name__ == '__main__':
    main()
