"""
CFA Dashboard Configuration
Single Source of Truth for all paths, settings, and constants

This file centralizes all configuration to make the dashboard:
- Portable: Easy to deploy elsewhere
- Maintainable: Change paths once, works everywhere
- Validated: Built-in path checking
- Documented: All settings in one place

Usage:
    from config import PATHS, SETTINGS, validate_paths
"""

import os
from pathlib import Path

# ============================================================================
# BASE PATHS
# ============================================================================

# Repository root (dashboard/ is one level down from root)
REPO_ROOT = Path(__file__).parent.parent.resolve()

# Dashboard directory
DASHBOARD_ROOT = Path(__file__).parent.resolve()

# ============================================================================
# DIRECTORY PATHS
# ============================================================================

PATHS = {
    # Root directories
    'root': REPO_ROOT,
    'dashboard': DASHBOARD_ROOT,

    # Core directories
    'auditors': REPO_ROOT / 'auditors',
    'docs': REPO_ROOT / 'docs',
    'profiles': REPO_ROOT / 'profiles',
    'tools': REPO_ROOT / 'tools',
    'utils': REPO_ROOT / 'utils',
    'logs': REPO_ROOT / 'logs',

    # Documentation
    'docs_architecture': REPO_ROOT / 'docs' / 'architecture',
    'docs_guides': REPO_ROOT / 'docs' / 'guides',
    'docs_validation': REPO_ROOT / 'docs' / 'Validation',
    'docs_repository': REPO_ROOT / 'docs' / 'repository',
    'docs_i_am': REPO_ROOT / 'docs' / 'i_am',
    'docs_nyquist': REPO_ROOT / 'docs' / 'Nyquist-Sync',  # Research reference (not tracked in health)

    # Auditor structure
    'bootstrap': REPO_ROOT / 'auditors' / 'Bootstrap',
    'bootstrap_claude': REPO_ROOT / 'auditors' / 'Bootstrap' / 'Claude',
    'bootstrap_nova': REPO_ROOT / 'auditors' / 'Bootstrap' / 'Nova',
    'bootstrap_grok': REPO_ROOT / 'auditors' / 'Bootstrap' / 'Grok',
    'bootstrap_kernels': REPO_ROOT / 'auditors' / 'Bootstrap' / 'Kernels',
    'bootstrap_guests': REPO_ROOT / 'auditors' / 'Bootstrap' / 'Guests',

    # Living Maps
    'file_inventory': REPO_ROOT / 'docs' / 'repository' / 'FILE_INVENTORY.md',
    'repo_health_dashboard': REPO_ROOT / 'docs' / 'repository' / 'OBSERVATORY' / 'REPO_HEALTH_DASHBOARD.md',
    'wayfinding_guide': REPO_ROOT / 'docs' / 'WAYFINDING_GUIDE.md',
    'worldview_catalog': REPO_ROOT / 'docs' / 'repository' / 'MAP_ROOM' / 'WORLDVIEW_CATALOG.md',

    # Key files
    'readme': REPO_ROOT / 'README.md',
    'changelog': REPO_ROOT / 'CHANGELOG.md',
    'repo_log': REPO_ROOT / 'REPO_LOG.md',

    # SMV Dashboard (if exists)
    'smv_dashboard': DASHBOARD_ROOT / 'SMV',

    # Tools
    'measure_fidelity': REPO_ROOT / 'tools' / 'measure_fidelity.py',
    'compute_gravity': REPO_ROOT / 'tools' / 'compute_gravity.py',
}

# ============================================================================
# SETTINGS
# ============================================================================

SETTINGS = {
    # Version
    'version': 'v5.0.0',
    'last_update': '2025-11-26',

    # Health scoring
    'health_target': 98,
    'health_green_threshold': 90,
    'health_yellow_threshold': 75,

    # File counts (for monitoring - operational only, excludes Nyquist-Sync research)
    'expected_file_count': 492,  # Operational files (v5.0 baseline)
    'expected_markdown_count': 455,

    # README limits (organizational health)
    'readme_target_min': 55,  # v5.0 minimum for architecture depth
    'readme_target_max': 70,  # v5.0 maximum before proliferation
    'readme_current': 64,     # Current count (within v5.0 target range)

    # Link integrity target
    'link_integrity_target': 0.99,  # 99% working links

    # Colors (for visualizations)
    'colors': {
        'green': '#10b981',
        'yellow': '#f59e0b',
        'red': '#ef4444',
        'blue': '#3b82f6',
        'purple': '#8b5cf6',
    },

    # Dashboard settings
    'dashboard_refresh_interval': 300,  # 5 minutes
    'enable_auto_refresh': False,
}

# ============================================================================
# EXCLUSIONS (Not tracked in health metrics)
# ============================================================================

EXCLUSIONS = {
    # Directories excluded from health scoring
    'excluded_dirs': [
        '.git',
        '.Archive',
        'node_modules',
        '__pycache__',
        '.venv',
        'venv',
        'docs/Nyquist-Sync',  # Research reference only (per v5.0 decision)
    ],

    # File patterns excluded from link checking
    'excluded_patterns': [
        '*.pyc',
        '*.log',
        '.DS_Store',
        'Thumbs.db',
    ],
}

# ============================================================================
# VALIDATION
# ============================================================================

def validate_paths():
    """
    Validate that all configured paths exist.
    Returns: (bool, list) - (success, missing_paths)
    """
    missing = []

    for name, path in PATHS.items():
        if not path.exists():
            missing.append(f"{name}: {path}")

    if missing:
        print(f"WARNING: {len(missing)} configured paths not found:")
        for path in missing:
            print(f"  - {path}")
        return False, missing

    print(f"SUCCESS: All {len(PATHS)} configured paths validated")
    return True, []

def get_path(key):
    """
    Get a path by key, with validation.
    Raises KeyError if key doesn't exist.
    """
    if key not in PATHS:
        raise KeyError(f"Path '{key}' not found in config. Available keys: {list(PATHS.keys())}")
    return PATHS[key]

def is_excluded(path_str):
    """
    Check if a path should be excluded from health scoring.
    """
    path_str = str(path_str)

    # Check excluded directories
    for excluded_dir in EXCLUSIONS['excluded_dirs']:
        if excluded_dir in path_str:
            return True

    # Check excluded patterns
    for pattern in EXCLUSIONS['excluded_patterns']:
        if path_str.endswith(pattern.replace('*', '')):
            return True

    return False

# ============================================================================
# AUTO-VALIDATION ON IMPORT
# ============================================================================

if __name__ == "__main__":
    print("CFA Dashboard Configuration Validation")
    print("=" * 50)
    print(f"Repository Root: {REPO_ROOT}")
    print(f"Dashboard Root: {DASHBOARD_ROOT}")
    print(f"Version: {SETTINGS['version']}")
    print()

    success, missing = validate_paths()

    if success:
        print("\nSUCCESS: Configuration valid and ready to use!")
    else:
        print(f"\nWARNING: Found {len(missing)} missing paths. Please review.")
        exit(1)
