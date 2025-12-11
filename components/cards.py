"""
CFA v5.0 - Reusable Card Components
Styled cards for the Console page with Ledger aesthetic
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colors import CFA_COLORS, STATUS_COLORS, get_framework_color


def audit_badge(status: str) -> str:
    """
    Generate an HTML badge for audit status

    Args:
        status: One of AUDITED, CONVERGENT, DRAFT, CRUX, DIVERGENT

    Returns:
        HTML string for the badge
    """
    color = STATUS_COLORS.get(status.upper(), '#666666')
    return f'''<span style="
        background: {color};
        padding: 2px 8px;
        border-radius: 12px;
        color: white;
        font-size: 0.8em;
        font-weight: 600;
        letter-spacing: 0.5px;
    ">{status.upper()}</span>'''


def audit_card(title: str, content: str, status: str = None, framework_color: str = None) -> str:
    """
    Generate a styled card for audit content

    Args:
        title: Card title
        content: HTML content for the card body
        status: Optional status badge (AUDITED, CONVERGENT, DRAFT, CRUX, DIVERGENT)
        framework_color: Optional border color (defaults to neutral gray)

    Returns:
        HTML string for the card
    """
    badge = audit_badge(status) if status else ""
    border_color = framework_color or CFA_COLORS['border']

    return f'''
    <div style="
        background: {CFA_COLORS['card']};
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid {border_color};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <h3 style="
            margin: 0 0 15px 0;
            font-family: Georgia, serif;
            color: {CFA_COLORS['text']};
            border-bottom: 1px solid {CFA_COLORS['border']};
            padding-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span>{title}</span>
            {badge}
        </h3>
        <div style="color: {CFA_COLORS['text_secondary']};">
            {content}
        </div>
    </div>
    '''


def status_summary_card(
    frameworks_loaded: int,
    frameworks_total: int,
    guardrails_passed: int,
    guardrails_total: int,
    convergence_pct: float,
    crux_count: int,
    active_preset: str,
    symmetry_status: str
) -> str:
    """
    Generate the real-time audit summary panel

    Returns:
        HTML string for the summary card
    """
    return f'''
    <div style="
        background: linear-gradient(135deg, {CFA_COLORS['audited']} 0%, #1a3a47 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        color: white;
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            padding-bottom: 10px;
        ">
            <h3 style="margin: 0; font-family: Georgia, serif; font-size: 1.2em; color: white;">
                AUDIT STATUS
            </h3>
            <span style="
                background: rgba(255,255,255,0.2);
                padding: 4px 12px;
                border-radius: 15px;
                font-size: 0.85em;
            ">Mode: {active_preset}</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div style="border-right: 1px solid rgba(255,255,255,0.2); padding-right: 15px;">
                <div style="margin-bottom: 10px;">
                    <span style="opacity: 0.7; font-size: 0.85em;">Frameworks:</span>
                    <strong style="margin-left: 8px;">{frameworks_loaded}/{frameworks_total}</strong>
                </div>
                <div>
                    <span style="opacity: 0.7; font-size: 0.85em;">Guardrails:</span>
                    <strong style="margin-left: 8px;">{guardrails_passed}/{guardrails_total} {"✅" if guardrails_passed == guardrails_total else "⚠️"}</strong>
                </div>
            </div>
            <div style="padding-left: 15px;">
                <div style="margin-bottom: 10px;">
                    <span style="opacity: 0.7; font-size: 0.85em;">Trinity Convergence:</span>
                    <strong style="margin-left: 8px;">{convergence_pct:.0f}%</strong>
                </div>
                <div>
                    <span style="opacity: 0.7; font-size: 0.85em;">Crux Declarations:</span>
                    <strong style="margin-left: 8px;">{crux_count}</strong>
                </div>
            </div>
        </div>
        <div style="
            margin-top: 15px;
            padding-top: 10px;
            border-top: 1px solid rgba(255,255,255,0.2);
            font-size: 0.85em;
            opacity: 0.8;
        ">
            Config Symmetry: {symmetry_status}
        </div>
    </div>
    '''


def metric_card(label: str, value: str, delta: str = None, color: str = None) -> str:
    """
    Generate a compact metric card

    Args:
        label: Metric label
        value: Main value to display
        delta: Optional delta/change indicator
        color: Optional accent color

    Returns:
        HTML string for the metric card
    """
    accent = color or CFA_COLORS['audited']
    delta_html = ""
    if delta:
        delta_color = CFA_COLORS['convergent'] if delta.startswith('+') else CFA_COLORS['divergent']
        delta_html = f'<span style="color: {delta_color}; font-size: 0.8em; margin-left: 5px;">{delta}</span>'

    return f'''
    <div style="
        background: {CFA_COLORS['card']};
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        border-top: 3px solid {accent};
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    ">
        <div style="
            font-size: 0.75em;
            color: {CFA_COLORS['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        ">{label}</div>
        <div style="
            font-size: 1.5em;
            font-weight: bold;
            color: {CFA_COLORS['text']};
        ">{value}{delta_html}</div>
    </div>
    '''


def framework_comparison_header(name_a: str, name_b: str, ypa_a: float, ypa_b: float) -> str:
    """
    Generate a comparison header showing two frameworks head-to-head

    Returns:
        HTML string for the comparison header
    """
    color_a = get_framework_color(name_a)
    color_b = get_framework_color(name_b)

    # Determine winner
    if abs(ypa_a - ypa_b) < 0.05:
        winner_indicator = "≈"
        winner_text = "TIE"
    elif ypa_a > ypa_b:
        winner_indicator = "←"
        winner_text = name_a.split()[0]
    else:
        winner_indicator = "→"
        winner_text = name_b.split()[0]

    return f'''
    <div style="
        background: linear-gradient(90deg, {color_a}22 0%, transparent 30%, transparent 70%, {color_b}22 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 20px;
        align-items: center;
    ">
        <div style="text-align: center;">
            <div style="font-size: 0.85em; color: {CFA_COLORS['text_secondary']}; margin-bottom: 5px;">
                Framework A
            </div>
            <div style="font-size: 1.1em; font-weight: bold; color: {color_a};">
                {name_a}
            </div>
            <div style="font-size: 1.8em; font-weight: bold; margin-top: 5px;">
                {ypa_a:.2f}
            </div>
        </div>
        <div style="text-align: center;">
            <div style="
                font-size: 2em;
                color: {CFA_COLORS['text_secondary']};
            ">{winner_indicator}</div>
            <div style="
                font-size: 0.75em;
                color: {CFA_COLORS['text_secondary']};
                margin-top: 5px;
            ">{winner_text}</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 0.85em; color: {CFA_COLORS['text_secondary']}; margin-bottom: 5px;">
                Framework B
            </div>
            <div style="font-size: 1.1em; font-weight: bold; color: {color_b};">
                {name_b}
            </div>
            <div style="font-size: 1.8em; font-weight: bold; margin-top: 5px;">
                {ypa_b:.2f}
            </div>
        </div>
    </div>
    '''
