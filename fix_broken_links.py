#!/usr/bin/env python3
"""
Broken Link Fix Script - CFA Repository
Fixes DASHBOARD.md -> REPO_HEALTH_DASHBOARD.md
Fixes 88MPH_PROTOCOL.md -> 88MPH.md
"""

import os
import re
from pathlib import Path

def fix_dashboard_references(content):
    """Fix DASHBOARD.md references but preserve REPO_HEALTH_DASHBOARD.md"""
    changes = []

    # Fix path references
    if '/docs/repository/DASHBOARD.md' in content:
        content = content.replace('/docs/repository/DASHBOARD.md', '/docs/repository/REPO_HEALTH_DASHBOARD.md')
        changes.append('path reference')

    # Fix link text [DASHBOARD.md]
    if '[DASHBOARD.md]' in content:
        content = content.replace('[DASHBOARD.md]', '[REPO_HEALTH_DASHBOARD.md]')
        changes.append('link text')

    # Fix DEPENDS_ON references (but only DASHBOARD.md, not REPO_HEALTH_DASHBOARD.md)
    content = re.sub(r'DEPENDS_ON:([^R]*?)DASHBOARD\.md', r'DEPENDS_ON:\1REPO_HEALTH_DASHBOARD.md', content)

    # Fix standalone DASHBOARD.md references (but not already REPO_HEALTH_)
    # Be careful not to double-replace
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'DASHBOARD.md' in line and 'REPO_HEALTH_DASHBOARD.md' not in line:
            # Simple replacement for common patterns
            if '- DASHBOARD.md' in line or '* DASHBOARD.md' in line or 'DASHBOARD.md -' in line:
                lines[i] = line.replace('DASHBOARD.md', 'REPO_HEALTH_DASHBOARD.md')
                if 'simple reference' not in changes:
                    changes.append('simple reference')

    content = '\n'.join(lines)
    return content, changes

def fix_88mph_references(content):
    """Fix 88MPH_PROTOCOL.md references"""
    changes = []

    # Fix path references
    patterns = [
        ('/docs/repository/librarian_tools/88MPH_PROTOCOL.md', '/88MPH.md'),
        ('docs/repository/librarian_tools/88MPH_PROTOCOL.md', '88MPH.md'),
        ('librarian_tools/88MPH_PROTOCOL.md', '../../../88MPH.md'),
        ('/docs/repository/88MPH_PROTOCOL.md', '/88MPH.md'),
        ('docs/repository/README.md:    ├── 88MPH_PROTOCOL.md', 'docs/repository/README.md:    ├── 88MPH.md'),
    ]

    for old, new in patterns:
        if old in content:
            content = content.replace(old, new)
            changes.append(f'path: {old}')

    # Fix general references (last resort)
    if '88MPH_PROTOCOL.md' in content:
        content = content.replace('88MPH_PROTOCOL.md', '88MPH.md')
        if 'general reference' not in changes:
            changes.append('general reference')

    return content, changes

def main():
    print("CFA Broken Link Fixer (Python)")
    print("=" * 50)
    print()

    dashboard_fixed = 0
    protocol_fixed = 0
    files_modified = []

    # Process all markdown files in docs/
    docs_path = Path('docs')
    if not docs_path.exists():
        print("ERROR: docs/ directory not found")
        print("   Make sure to run this script from the CFA repository root")
        return

    print("Processing markdown files...")
    for md_file in docs_path.rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            dashboard_changes = []
            protocol_changes = []

            # Fix DASHBOARD references
            if 'DASHBOARD.md' in content and 'REPO_HEALTH_DASHBOARD.md' not in content:
                content, dashboard_changes = fix_dashboard_references(content)

            # Fix 88MPH_PROTOCOL references
            if '88MPH_PROTOCOL.md' in content:
                content, protocol_changes = fix_88mph_references(content)

            # Write back if changes were made
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                files_modified.append(str(md_file))

                if dashboard_changes:
                    print(f"  OK {md_file.relative_to(docs_path)}")
                    print(f"     DASHBOARD fixes: {', '.join(dashboard_changes)}")
                    dashboard_fixed += 1

                if protocol_changes:
                    print(f"  OK {md_file.relative_to(docs_path)}")
                    print(f"     88MPH_PROTOCOL fixes: {', '.join(protocol_changes)}")
                    protocol_fixed += 1

        except Exception as e:
            print(f"  WARNING: Error processing {md_file}: {e}")

    print()
    print("Fix Complete!")
    print("=" * 50)
    print("Summary:")
    print(f"  - Files with DASHBOARD.md fixes: {dashboard_fixed}")
    print(f"  - Files with 88MPH_PROTOCOL.md fixes: {protocol_fixed}")
    print(f"  - Total files modified: {len(set(files_modified))}")
    print()
    print("Verification:")
    print("  Check remaining broken links:")
    print('  grep -r "DASHBOARD\\.md" docs/ | grep -v "REPO_HEALTH_DASHBOARD.md"')
    print('  grep -r "88MPH_PROTOCOL\\.md" docs/')

if __name__ == '__main__':
    main()
