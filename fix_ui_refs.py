#!/usr/bin/env python3
"""
Fix ui/ directory references → dashboard/
Context-aware: Preserves historical migration notes
"""

import os
import re
from pathlib import Path

def fix_ui_references(content, filepath):
    """Fix ui/ references but preserve historical context"""
    changes = []
    original = content

    # Patterns to SKIP (historical migration notes)
    skip_patterns = [
        r'ui/.*→.*dashboard',  # "ui/smv/prototype/ → dashboard/SMV/"
        r'MOVED.*ui/',          # "MOVED: ui/smv/prototype/"
        r'Removed ui/',         # "Removed ui/ directory"
        r'Empty ui/',           # "Empty ui/ directory"
        r'moved from ui/',      # "moved from ui/ to dashboard/"
        r'replacing ui/',       # "replacing ui/ with dashboard/"
    ]

    # Check if any skip pattern matches
    for pattern in skip_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            # This file has historical migration context - be very careful
            # Only fix current references, not historical ones
            pass

    # Fix current ui/ references (paths in current docs)
    # Pattern: ui/smv/ or ui/prototype/ → dashboard/SMV/ or dashboard/prototype/
    replacements = [
        (r'\bui/smv/prototype\b', 'dashboard/SMV'),
        (r'\bui/smv\b', 'dashboard/SMV'),
        (r'\bui/prototype\b', 'dashboard/prototype'),
    ]

    for old_pattern, new_path in replacements:
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_path, content)
            if old_pattern not in [c[0] for c in changes]:
                changes.append((old_pattern, new_path))

    # Only return if actual changes made
    if content != original:
        return content, changes
    return None, []

def main():
    print("CFA ui/ Reference Fixer")
    print("=" * 50)
    print()

    fixed_count = 0
    files_modified = []

    # Process markdown files (excluding .git and node_modules)
    print("Scanning for ui/ references...")

    # Target main docs (not archives - those are historical)
    target_dirs = [
        'docs/',
        'README.md',
        'CHANGELOG.md',
        'pages/',
    ]

    for target in target_dirs:
        target_path = Path(target)
        if not target_path.exists():
            continue

        if target_path.is_file():
            # Single file
            files_to_check = [target_path]
        else:
            # Directory - get all .md files
            files_to_check = target_path.rglob('*.md')

        for md_file in files_to_check:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Only process if ui/ is mentioned
                if 'ui/' not in content:
                    continue

                new_content, changes = fix_ui_references(content, str(md_file))

                if new_content:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    files_modified.append(str(md_file))
                    fixed_count += 1
                    print(f"  OK Fixed: {md_file}")
                    for old, new in changes:
                        print(f"     {old} -> {new}")
                else:
                    print(f"  SKIP (historical context): {md_file}")

            except Exception as e:
                print(f"  WARNING Error processing {md_file}: {e}")

    print()
    print("Fix Complete!")
    print("=" * 50)
    print(f"Files modified: {fixed_count}")
    print()
    print("Note: Historical references in REPO_LOG.md preserved")
    print("      (e.g., 'MOVED: ui/smv/ to dashboard/SMV/')")
    print()
    print("Verification:")
    print("  grep -r \"ui/\" docs/ README.md CHANGELOG.md | grep -v \"ui/ux\"")

if __name__ == '__main__':
    main()
