#!/usr/bin/env python3
"""Fix all remaining DASHBOARD.md references to REPO_HEALTH_DASHBOARD.md"""

import re
from pathlib import Path

files_to_fix = [
    'docs/architecture/Future_Expansion.md',
    'docs/repository/dependency_maps/VALIDATION_MAP.md',
    'docs/repository/FILE_INVENTORY.md',
    'docs/repository/Health_Reports/DEEP_CLEAN_PROTOCOL.md',
    'docs/repository/librarian_tools/ROLE_VALIDATION.md',
    'docs/SOURCE_OF_TRUTH.md',
    'docs/Validation/DOC_CLAUDE_WELLNESS_PROTOCOL.md',
    'docs/Validation/README.md',
    'docs/Validation/reports/2025-11-02_SEMANTIC_HEADER_NOISE_ASSESSMENT.md',
    'docs/Validation/reports/2025-11-12_C5_REPORT_ANALYSIS.md',
    'docs/Validation/reports/2025-11-12_DEEP_CLEAN_REPORT.md',
]

def fix_file(filepath):
    """Fix all DASHBOARD.md references in a file"""
    path = Path(filepath)
    if not path.exists():
        print(f"SKIP: {filepath} (not found)")
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Global replacement: DASHBOARD.md -> REPO_HEALTH_DASHBOARD.md
    # But protect already-correct REPO_HEALTH_DASHBOARD.md references
    content = re.sub(r'\bDASHBOARD\.md\b', 'REPO_HEALTH_DASHBOARD.md', content)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: {filepath}")
        return True
    else:
        print(f"NO CHANGE: {filepath}")
        return False

def main():
    print("Fixing remaining DASHBOARD.md references...")
    print("=" * 50)

    fixed_count = 0
    for filepath in files_to_fix:
        if fix_file(filepath):
            fixed_count += 1

    print()
    print(f"Fixed {fixed_count}/{len(files_to_fix)} files")
    print()
    print("Verification:")
    print('  grep -r "DASHBOARD\\.md" docs/ | grep -v "REPO_HEALTH_DASHBOARD.md" | wc -l')

if __name__ == '__main__':
    main()
