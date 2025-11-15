#!/usr/bin/env python3
"""
Extract Canonical YAML Files from Worldview Profiles

Purpose: Convert .md YAML blocks to standalone canonical .yaml files
Usage: python scripts/extract_yaml_profiles.py
Author: Ziggy Mack (CFA) + Claude
Version: 1.0
"""

import re
import yaml
from pathlib import Path

PROFILES_DIR = Path("profiles/worldviews")

def extract_yaml_from_md(md_filepath):
    """Extract YPA Application Data YAML block from .md file"""
    content = md_filepath.read_text(encoding='utf-8')

    # Pattern: ## YPA Application Data section with yaml block
    pattern = r'##\s+YPA Application Data.*?```yaml\n(.*?)\n```'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print(f"[SKIP] No YPA YAML block found in {md_filepath.name}")
        return None

    yaml_content = match.group(1)

    try:
        data = yaml.safe_load(yaml_content)
        return data
    except yaml.YAMLError as e:
        print(f"[ERROR] YAML parsing error in {md_filepath.name}: {e}")
        return None

def extract_metadata_from_md(md_filepath):
    """Extract Metadata YAML block from .md file"""
    content = md_filepath.read_text(encoding='utf-8')

    # Pattern: ## Metadata section with yaml block
    pattern = r'##\s+Metadata.*?```yaml\n(.*?)\n```'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return {}

    yaml_content = match.group(1)

    try:
        data = yaml.safe_load(yaml_content)
        return data.get('profile', {})
    except yaml.YAMLError:
        return {}

def create_canonical_yaml(md_filepath):
    """Create canonical .yaml file from .md YAML blocks"""

    ypa_data = extract_yaml_from_md(md_filepath)
    metadata = extract_metadata_from_md(md_filepath)

    if not ypa_data:
        print(f"[SKIP] Skipping {md_filepath.stem} (no YPA data)")
        return False

    # Extract components
    bfi = ypa_data.get('brute_fact_index', {})
    levers = ypa_data.get('ypa_levers', {})
    flags = ypa_data.get('behavioral_flags', {})

    # Calculate values
    axiom_count = bfi.get('axioms', 0)
    debt_count = bfi.get('debts', 0)

    cci = levers.get('CCI', 0.0)
    edb = levers.get('EDB', 0.0)
    pf_i = levers.get('PF_instrumental', 0.0)
    pf_e = levers.get('PF_existential', 0.0)
    ar = levers.get('AR', 0.0)
    mg = levers.get('MG', 0.0)

    lever_sum = cci + edb + pf_i + pf_e + ar + mg

    bfi_standard = (axiom_count + debt_count) * 1.0
    ypa_standard = lever_sum / bfi_standard if bfi_standard > 0 else 0

    skeptic_bfi = (axiom_count + debt_count) * 1.2
    skeptic_ypa = lever_sum / skeptic_bfi if skeptic_bfi > 0 else 0

    diplomat_bfi = (axiom_count + debt_count) * 0.9
    diplomat_ypa = lever_sum / diplomat_bfi if diplomat_bfi > 0 else 0

    zealot_bfi = (axiom_count + debt_count) * 0.7
    zealot_ypa = lever_sum / zealot_bfi if zealot_bfi > 0 else 0

    # Build canonical YAML structure
    canonical = {
        'profile': {
            'name': metadata.get('name', md_filepath.stem.replace('_', ' ').title()),
            'version': metadata.get('version', 'v0.3.0'),
            'status': metadata.get('status', 'DRAFT'),
            'declared_axiom': metadata.get('declared_axiom', ''),
            'last_updated': '2025-11-15',
            'maintainers': metadata.get('maintainers', ['Ziggy', 'Grok', 'C4', 'Nova'])
        },
        'axioms': ypa_data.get('axioms', []),
        'debts': ypa_data.get('debts', []),
        'levers': {
            'collective_coherence_impact': cci,
            'epistemic_debt_burden': edb,
            'paternalistic_force_interventionist': pf_i,
            'paternalistic_force_epistemic': pf_e,
            'asymmetry_risk': ar,
            'meta_governance': mg
        },
        'behavioral_flags': {
            'admits_limits': flags.get('admits_limits', True)
        },
        'calculated': {
            'axiom_count': axiom_count,
            'debt_count': debt_count,
            'bfi_standard': round(bfi_standard, 1),
            'lever_sum': round(lever_sum, 1),
            'ypa_standard': round(ypa_standard, 2),
            'skeptic_bfi': round(skeptic_bfi, 1),
            'skeptic_ypa': round(skeptic_ypa, 2),
            'diplomat_bfi': round(diplomat_bfi, 1),
            'diplomat_ypa': round(diplomat_ypa, 2),
            'zealot_bfi': round(zealot_bfi, 1),
            'zealot_ypa': round(zealot_ypa, 2)
        }
    }

    # Write canonical YAML file
    yaml_filepath = md_filepath.with_suffix('.yaml')

    with open(yaml_filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {metadata.get('name', md_filepath.stem)} - Canonical Score Data\n")
        f.write(f"# Purpose: Machine-readable YPA scores for validation and calculation\n")
        f.write(f"# Source: Extracted from {md_filepath.name} (v{metadata.get('version', '0.3.0')})\n")
        f.write(f"# Usage: ypa_validator.py, empirical verification, Grok validation\n")
        f.write(f"# Last Updated: 2025-11-15\n\n")

        yaml.dump(canonical, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"[OK] Created {yaml_filepath.name}")
    print(f"     Axioms: {axiom_count}, Debts: {debt_count}, YPA: {ypa_standard:.2f}")
    return True

def main():
    print("=" * 60)
    print("Extracting Canonical YAML Files from Worldview Profiles")
    print("=" * 60)
    print()

    if not PROFILES_DIR.exists():
        print(f"[ERROR] Profiles directory not found: {PROFILES_DIR}")
        return

    md_files = sorted(PROFILES_DIR.glob("*.md"))

    created_count = 0
    skipped_count = 0

    for md_file in md_files:
        yaml_file = md_file.with_suffix('.yaml')

        if yaml_file.exists():
            print(f"[SKIP] {md_file.stem} (YAML already exists)")
            skipped_count += 1
            continue

        if create_canonical_yaml(md_file):
            created_count += 1
        else:
            skipped_count += 1

    print()
    print("=" * 60)
    print(f"[DONE] Created {created_count} canonical YAML files")
    print(f"[SKIP] Skipped {skipped_count} profiles")
    print("=" * 60)

if __name__ == "__main__":
    main()
