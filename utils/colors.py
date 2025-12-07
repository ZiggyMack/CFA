"""
CFA v5.0 Color Palette
Adapted from CONSOLE_ENHANCEMENT_PROMPT.md - Ledger Aesthetic Theme
"""

# =============================================================================
# MAIN COLOR PALETTE
# =============================================================================

CFA_COLORS = {
    # Backgrounds
    'background': 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
    'card': '#ffffff',
    'border': '#dee2e6',

    # Text
    'text': '#212529',
    'text_secondary': '#6c757d',

    # Status colors (for audit badges)
    'audited': '#264653',      # Dark teal - Trinity validated
    'convergent': '#2a9d8f',   # Green - high agreement
    'draft': '#e9c46a',        # Gold - in progress
    'crux': '#f4a261',         # Orange - declared impasse
    'divergent': '#e76f51',    # Red - disagreement

    # Framework colors (match Brute Ledger emojis)
    'mdn': '#1f77b4',          # Blue (📘)
    'ct': '#d62728',           # Red (📕)
    'buddhism': '#9467bd',     # Purple (☸️)
    'islam': '#2ca02c',        # Green (☪️)
    'hinduism': '#ff7f0e',     # Orange (🕉️)
    'judaism': '#8c564b',      # Brown (🕎)
    'mormonism': '#e377c2',    # Pink (📖)
    'process': '#17becf',      # Cyan (🌊)

    # Auditor colors (Trinity)
    'claude': '#7b3fe4',       # Purple
    'grok': '#ff6b35',         # Orange
    'nova': '#00b4d8',         # Cyan

    # Preset mode colors
    'skeptic': '#3498db',      # Blue - empirical focus
    'diplomat': '#27ae60',     # Green - balanced
    'seeker': '#9b59b6',       # Purple - meaning focus
    'zealot': '#e74c3c',       # Red - existential focus

    # Chart colors
    'chart_primary': '#1f77b4',
    'chart_secondary': '#d62728',
    'chart_tertiary': '#2ca02c',
    'chart_grid': '#e0e0e0',
}

# =============================================================================
# STATUS BADGE COLORS (for audit_badge function)
# =============================================================================

STATUS_COLORS = {
    'AUDITED': '#264653',     # Dark teal - Trinity validated
    'CONVERGENT': '#2a9d8f',  # Green - High agreement
    'DRAFT': '#e9c46a',       # Gold - Work in progress
    'CRUX': '#f4a261',        # Orange - Declared impasse
    'DIVERGENT': '#e76f51'    # Red - Low agreement
}

# =============================================================================
# LEVER COLORS (for radar/comparison charts)
# =============================================================================

LEVER_COLORS = {
    'CCI': '#1f77b4',          # Blue
    'EDB': '#ff7f0e',          # Orange
    'PF_instrumental': '#2ca02c',  # Green
    'PF_existential': '#d62728',   # Red
    'AR': '#9467bd',           # Purple
    'MG': '#8c564b',           # Brown
}

# Shortened lever names for compact displays
LEVER_SHORT_NAMES = {
    'CCI': 'CCI',
    'EDB': 'EDB',
    'PF_instrumental': 'PF-I',
    'PF_existential': 'PF-E',
    'AR': 'AR',
    'MG': 'MG',
}

# =============================================================================
# SCENARIO COLORS (for YPA charts)
# =============================================================================

SCENARIO_COLORS = {
    'Neutral': '#6c757d',      # Gray
    'Empirical': '#1f77b4',    # Blue
    'Existential': '#9467bd',  # Purple
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_framework_color(framework_name: str) -> str:
    """Get color for a framework by name"""
    name_lower = framework_name.lower()

    if 'naturalism' in name_lower or 'mdn' in name_lower:
        return CFA_COLORS['mdn']
    elif 'theism' in name_lower or 'ct' in name_lower:
        return CFA_COLORS['ct']
    elif 'buddhism' in name_lower or 'buddhist' in name_lower:
        return CFA_COLORS['buddhism']
    elif 'islam' in name_lower or 'muslim' in name_lower:
        return CFA_COLORS['islam']
    elif 'hindu' in name_lower:
        return CFA_COLORS['hinduism']
    elif 'juda' in name_lower:
        return CFA_COLORS['judaism']
    elif 'mormon' in name_lower or 'lds' in name_lower:
        return CFA_COLORS['mormonism']
    elif 'process' in name_lower:
        return CFA_COLORS['process']
    else:
        return CFA_COLORS['text_secondary']


def get_status_color(status: str) -> str:
    """Get color for an audit status"""
    return STATUS_COLORS.get(status.upper(), '#666666')


def get_auditor_color(auditor: str) -> str:
    """Get color for a Trinity auditor"""
    auditor_lower = auditor.lower()
    if 'claude' in auditor_lower:
        return CFA_COLORS['claude']
    elif 'grok' in auditor_lower:
        return CFA_COLORS['grok']
    elif 'nova' in auditor_lower:
        return CFA_COLORS['nova']
    return CFA_COLORS['text_secondary']


def get_preset_color(preset: str) -> str:
    """Get color for a preset mode"""
    preset_lower = preset.lower()
    if 'skeptic' in preset_lower:
        return CFA_COLORS['skeptic']
    elif 'diplomat' in preset_lower:
        return CFA_COLORS['diplomat']
    elif 'seeker' in preset_lower:
        return CFA_COLORS['seeker']
    elif 'zealot' in preset_lower:
        return CFA_COLORS['zealot']
    return CFA_COLORS['text_secondary']
