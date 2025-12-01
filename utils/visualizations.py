"""
CFA v5.0 - Visualization Utilities
All chart creation functions
"""

import plotly.graph_objects as go
from typing import Dict

def create_lever_comparison_chart(fa_levers: Dict, fb_levers: Dict, fa_name: str, fb_name: str) -> go.Figure:
    """Create side-by-side bar chart comparing lever scores"""
    levers = list(fa_levers.keys())
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=fa_name, 
        x=levers, 
        y=[fa_levers[l] for l in levers], 
        marker_color='rgb(55, 83, 109)'
    ))
    fig.add_trace(go.Bar(
        name=fb_name, 
        x=levers, 
        y=[fb_levers[l] for l in levers], 
        marker_color='rgb(26, 118, 255)'
    ))
    fig.update_layout(
        title="Lever Comparison", 
        xaxis_title="Lever", 
        yaxis_title="Score", 
        barmode='group', 
        height=400
    )
    return fig

def create_ypa_trinity_chart(fa_results: Dict, fb_results: Dict, fa_name: str, fb_name: str) -> go.Figure:
    """Create YPA comparison across three scenarios"""
    scenarios = ["Neutral", "Existential", "Empirical"]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=fa_name, 
        x=scenarios, 
        y=[fa_results[s]["YPA"] for s in scenarios], 
        marker_color='rgb(55, 83, 109)'
    ))
    fig.add_trace(go.Bar(
        name=fb_name, 
        x=scenarios, 
        y=[fb_results[s]["YPA"] for s in scenarios], 
        marker_color='rgb(26, 118, 255)'
    ))
    fig.update_layout(
        title="YPA Trinity", 
        xaxis_title="Scenario", 
        yaxis_title="YPA", 
        barmode='group', 
        height=400
    )
    return fig
