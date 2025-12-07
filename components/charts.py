"""
CFA v5.0 - Plotly Visualization Helpers
New chart types for Console enhancement
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colors import (
    CFA_COLORS, LEVER_COLORS, LEVER_SHORT_NAMES, SCENARIO_COLORS,
    get_framework_color, get_auditor_color
)


def create_convergence_radar(
    trinity_scores: dict,
    title: str = "Trinity Auditor Convergence"
) -> go.Figure:
    """
    Create a radar chart showing Claude, Grok, Nova scores overlapping

    Args:
        trinity_scores: Dict like {
            'Claude': [8.0, 7.5, 10.0, 3.0, 7.0, 4.0],
            'Grok': [8.0, 7.5, 10.0, 3.0, 7.0, 4.0],
            'Nova': [8.0, 7.5, 10.0, 3.0, 7.0, 4.0]
        }
        title: Chart title

    Returns:
        Plotly Figure
    """
    categories = ['CCI', 'EDB', 'PF-I', 'PF-E', 'AR', 'MG']

    fig = go.Figure()

    for auditor, scores in trinity_scores.items():
        color = get_auditor_color(auditor)
        # Close the polygon by repeating first value
        r_values = list(scores) + [scores[0]]
        theta_values = categories + [categories[0]]

        # Convert hex to rgba for fill (older Plotly compatibility)
        hex_color = color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        fill_rgba = f'rgba({r},{g},{b},0.2)'

        fig.add_trace(go.Scatterpolar(
            r=r_values,
            theta=theta_values,
            name=auditor,
            fill='toself',
            fillcolor=fill_rgba,
            line=dict(color=color, width=2),
            opacity=0.8
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(size=10),
                gridcolor=CFA_COLORS['chart_grid']
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
                gridcolor=CFA_COLORS['chart_grid']
            ),
            bgcolor='rgba(248, 249, 250, 0.5)'
        ),
        title=dict(
            text=title,
            font=dict(size=16, family='Georgia, serif'),
            x=0.5
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5
        ),
        margin=dict(t=60, b=60, l=60, r=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig


def create_sensitivity_heatmap(
    sensitivity_matrix: list,
    frameworks: list,
    toggles: list = None,
    title: str = "Toggle Sensitivity by Framework"
) -> go.Figure:
    """
    Create a heatmap showing YPA delta when each toggle is flipped

    Args:
        sensitivity_matrix: 2D list of ΔYPA values [frameworks x toggles]
        frameworks: List of framework names
        toggles: List of toggle names (default: standard 4)
        title: Chart title

    Returns:
        Plotly Figure
    """
    if toggles is None:
        toggles = ['Parity', 'PF-Type', 'Fallibilism', 'BFI Weight']

    # Convert to numpy for easier handling
    z = np.array(sensitivity_matrix)

    fig = px.imshow(
        z,
        labels=dict(x='Toggle', y='Framework', color='ΔYPA'),
        x=toggles,
        y=frameworks,
        aspect='auto',
        color_continuous_scale='RdYlGn_r',
        color_continuous_midpoint=0,
        zmin=-1.0,
        zmax=1.0
    )

    # Add value annotations
    for i, fw in enumerate(frameworks):
        for j, toggle in enumerate(toggles):
            val = z[i, j]
            text_color = 'white' if abs(val) > 0.5 else 'black'
            fig.add_annotation(
                x=j, y=i,
                text=f'{val:+.2f}',
                showarrow=False,
                font=dict(size=11, color=text_color)
            )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, family='Georgia, serif'),
            x=0.5
        ),
        xaxis=dict(
            tickfont=dict(size=11),
            side='bottom'
        ),
        yaxis=dict(
            tickfont=dict(size=11)
        ),
        margin=dict(t=60, b=40, l=120, r=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig


def create_battle_card_html(
    name_a: str,
    name_b: str,
    levers_a: dict,
    levers_b: dict,
    ypa_a: float,
    ypa_b: float
) -> str:
    """
    Create an ASCII-style battle card comparing two frameworks

    Args:
        name_a: Framework A name
        name_b: Framework B name
        levers_a: Dict with CCI, EDB, PF_instrumental, PF_existential, AR, MG
        levers_b: Same structure for B
        ypa_a: YPA score for A
        ypa_b: YPA score for B

    Returns:
        HTML string with styled battle card
    """
    color_a = get_framework_color(name_a)
    color_b = get_framework_color(name_b)

    # Map lever keys to display names
    lever_map = [
        ('CCI', 'CCI'),
        ('EDB', 'EDB'),
        ('PF_instrumental', 'PF-I'),
        ('PF_existential', 'PF-E'),
        ('AR', 'AR'),
        ('MG', 'MG')
    ]

    rows = []
    wins_a = 0
    wins_b = 0

    for key, label in lever_map:
        # Handle both dict key formats
        val_a = levers_a.get(key, levers_a.get(label, 5.0))
        val_b = levers_b.get(key, levers_b.get(label, 5.0))

        # Create bar visualization (10 chars = 10 points)
        bar_a = '█' * int(val_a) + '░' * (10 - int(val_a))
        bar_b = '█' * int(val_b) + '░' * (10 - int(val_b))

        # Determine winner
        if val_a > val_b:
            winner = f'<span style="color: {color_a}; font-weight: bold;">← {name_a.split()[0][:3]}</span>'
            wins_a += 1
        elif val_b > val_a:
            winner = f'<span style="color: {color_b}; font-weight: bold;">{name_b.split()[0][:3]} →</span>'
            wins_b += 1
        else:
            winner = '<span style="color: #666;">TIE</span>'

        rows.append(f'''
        <tr>
            <td style="padding: 8px; font-weight: bold; color: {CFA_COLORS['text']};">{label}</td>
            <td style="padding: 8px; font-family: monospace; color: {color_a};">{val_a:.1f} {bar_a}</td>
            <td style="padding: 8px; text-align: center;">vs</td>
            <td style="padding: 8px; font-family: monospace; color: {color_b};">{bar_b} {val_b:.1f}</td>
            <td style="padding: 8px; text-align: right;">{winner}</td>
        </tr>
        ''')

    # YPA final row
    ypa_winner = name_a.split()[0][:3] if ypa_a > ypa_b else (name_b.split()[0][:3] if ypa_b > ypa_a else "TIE")
    ypa_color = color_a if ypa_a > ypa_b else (color_b if ypa_b > ypa_a else '#666')

    return f'''
    <div style="
        background: {CFA_COLORS['card']};
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        font-family: 'Courier New', monospace;
    ">
        <div style="
            text-align: center;
            padding-bottom: 15px;
            border-bottom: 2px solid {CFA_COLORS['border']};
            margin-bottom: 15px;
        ">
            <span style="color: {color_a}; font-weight: bold; font-size: 1.1em;">{name_a}</span>
            <span style="margin: 0 15px; color: {CFA_COLORS['text_secondary']};">vs</span>
            <span style="color: {color_b}; font-weight: bold; font-size: 1.1em;">{name_b}</span>
        </div>
        <table style="width: 100%; border-collapse: collapse;">
            {''.join(rows)}
            <tr style="border-top: 2px solid {CFA_COLORS['border']};">
                <td style="padding: 12px 8px; font-weight: bold; font-size: 1.1em;">YPA</td>
                <td style="padding: 12px 8px; font-size: 1.2em; color: {color_a}; font-weight: bold;">{ypa_a:.2f}</td>
                <td style="padding: 12px 8px; text-align: center;">vs</td>
                <td style="padding: 12px 8px; font-size: 1.2em; color: {color_b}; font-weight: bold;">{ypa_b:.2f}</td>
                <td style="padding: 12px 8px; text-align: right;">
                    <span style="color: {ypa_color}; font-weight: bold;">→ {ypa_winner}</span>
                </td>
            </tr>
        </table>
        <div style="
            margin-top: 15px;
            padding-top: 10px;
            border-top: 1px solid {CFA_COLORS['border']};
            text-align: center;
            color: {CFA_COLORS['text_secondary']};
            font-size: 0.85em;
        ">
            Lever Wins: <span style="color: {color_a};">{name_a.split()[0]} {wins_a}</span> |
            <span style="color: {color_b};">{name_b.split()[0]} {wins_b}</span>
        </div>
    </div>
    '''


def create_preset_compass(
    current_angle: float,
    current_label: str = "You Are Here"
) -> go.Figure:
    """
    Create a polar compass showing position relative to preset modes

    Args:
        current_angle: Angle in degrees (0=Diplomat, 90=Seeker, 180=Zealot, 270=Skeptic)
        current_label: Label for current position marker

    Returns:
        Plotly Figure
    """
    # Preset positions
    presets = {
        'Diplomat': 0,
        'Seeker': 90,
        'Zealot': 180,
        'Skeptic': 270
    }

    fig = go.Figure()

    # Add preset markers
    for name, angle in presets.items():
        color = CFA_COLORS.get(name.lower(), '#666')
        fig.add_trace(go.Scatterpolar(
            r=[0.8],
            theta=[angle],
            mode='markers+text',
            marker=dict(size=15, color=color, symbol='diamond'),
            text=[name],
            textposition='top center',
            textfont=dict(size=11, color=color),
            name=name,
            showlegend=False
        ))

    # Add current position marker
    fig.add_trace(go.Scatterpolar(
        r=[0.6],
        theta=[current_angle],
        mode='markers+text',
        marker=dict(size=20, color=CFA_COLORS['convergent'], symbol='star'),
        text=[current_label],
        textposition='bottom center',
        textfont=dict(size=10, color=CFA_COLORS['convergent']),
        name='Current',
        showlegend=False
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, 1]
            ),
            angularaxis=dict(
                visible=True,
                tickmode='array',
                tickvals=[0, 90, 180, 270],
                ticktext=['Balanced', 'Meaning', 'Existential', 'Empirical'],
                tickfont=dict(size=10),
                direction='clockwise',
                rotation=90
            ),
            bgcolor='rgba(248, 249, 250, 0.5)'
        ),
        title=dict(
            text='Epistemic Compass',
            font=dict(size=14, family='Georgia, serif'),
            x=0.5
        ),
        margin=dict(t=50, b=30, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)',
        height=300
    )

    return fig


def create_guardrail_grid(
    frameworks: list,
    guardrail_status: list
) -> str:
    """
    Create an HTML grid showing pass/fail for each guardrail per framework

    Args:
        frameworks: List of framework names
        guardrail_status: 2D list [guardrails x frameworks] with ✅, ⚠️, or ❌

    Returns:
        HTML string for the guardrail grid
    """
    guardrails = ['Lever-Coupling', 'BFI-Sensitivity', 'Weight-Inversion', 'Symmetry']

    header_cells = ''.join([
        f'<th style="padding: 10px; text-align: center; color: {get_framework_color(fw)}; font-weight: bold;">{fw.split()[0]}</th>'
        for fw in frameworks
    ])

    rows = []
    for i, guard in enumerate(guardrails):
        cells = ''.join([
            f'<td style="padding: 10px; text-align: center; font-size: 1.2em;">{guardrail_status[i][j]}</td>'
            for j in range(len(frameworks))
        ])
        rows.append(f'''
        <tr>
            <td style="padding: 10px; font-weight: bold; color: {CFA_COLORS['text']};">{guard}</td>
            {cells}
        </tr>
        ''')

    return f'''
    <div style="
        background: {CFA_COLORS['card']};
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    ">
        <h4 style="margin: 0 0 15px 0; font-family: Georgia, serif; color: {CFA_COLORS['text']};">
            Guardrail Status
        </h4>
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="border-bottom: 2px solid {CFA_COLORS['border']};">
                    <th style="padding: 10px; text-align: left;">Guardrail</th>
                    {header_cells}
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </div>
    '''


def create_scenario_comparison_bars(
    ya_results: dict,
    yb_results: dict,
    name_a: str,
    name_b: str
) -> go.Figure:
    """
    Create horizontal bar chart showing YPA across three scenarios

    Args:
        ya_results: Dict with Neutral, Empirical, Existential YPA for A
        yb_results: Same for B
        name_a: Framework A name
        name_b: Framework B name

    Returns:
        Plotly Figure
    """
    scenarios = ['Neutral', 'Empirical', 'Existential']
    color_a = get_framework_color(name_a)
    color_b = get_framework_color(name_b)

    fig = go.Figure()

    # Framework A bars
    fig.add_trace(go.Bar(
        name=name_a,
        y=scenarios,
        x=[ya_results[s]['YPA'] for s in scenarios],
        orientation='h',
        marker_color=color_a,
        text=[f"{ya_results[s]['YPA']:.2f}" for s in scenarios],
        textposition='inside',
        textfont=dict(color='white')
    ))

    # Framework B bars
    fig.add_trace(go.Bar(
        name=name_b,
        y=scenarios,
        x=[yb_results[s]['YPA'] for s in scenarios],
        orientation='h',
        marker_color=color_b,
        text=[f"{yb_results[s]['YPA']:.2f}" for s in scenarios],
        textposition='inside',
        textfont=dict(color='white')
    ))

    fig.update_layout(
        barmode='group',
        title=dict(
            text='Scenario Impact: YPA Across Weightings',
            font=dict(size=16, family='Georgia, serif'),
            x=0.5
        ),
        xaxis=dict(
            title='YPA Score',
            range=[0, 10],
            gridcolor=CFA_COLORS['chart_grid']
        ),
        yaxis=dict(
            title=''
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5
        ),
        margin=dict(t=60, b=80, l=100, r=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300
    )

    return fig
