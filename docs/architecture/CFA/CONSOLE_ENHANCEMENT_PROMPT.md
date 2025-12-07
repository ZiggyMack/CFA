# CFA v5.0 Console Enhancement Specification

> **Origin:** Adapted from Nyquist Consciousness dashboard patterns
> **Purpose:** Improve Console page visualizations, structure, and user experience
> **Status:** Design specification for future implementation

---

## Context

Lessons learned from the Nyquist Consciousness dashboard that can dramatically improve the CFA Console page. The patterns below translate Nyquist's "identity drift" paradigm into CFA's "framework comparison" paradigm.

**Domain Translation:**
| Nyquist Concept | CFA Equivalent |
|-----------------|----------------|
| Ships | Frameworks (MdN, CT, Buddhism, etc.) |
| Drift | YPA scores / Lever values |
| Fleet Health | Audit convergence status |
| Event Horizon | Guardrail thresholds |
| Providers | Auditors (Claude, Grok, Nova) |
| Turns | Configuration toggles (Parity, PF-Type, etc.) |
| Pillars | Lever categories (CCI, EDB, PF, AR, MG) |

---

## 1. Structural Improvements

### Current Issues with Console.py
- Dense monolithic layout with all content in one long scroll
- No clear visual hierarchy between major sections
- Tabs are flat - no indication of importance or data freshness
- Status cards don't have enough visual differentiation
- Framework comparison feels clinical, not engaging

### Recommended Structure

**A. Ledger/Card-Based Layout**
Wrap each major section in styled "cards" with:
- Rounded corners and subtle shadows
- Color-coded headers (audited=teal, draft=gold, custom=purple)
- Consistent padding and margins
- Collapsible sections for dense content

**B. Progressive Disclosure**
- **Top level:** At-a-glance summary (3-5 key metrics)
- **Second level:** Expandable sections for details
- **Third level:** Deep-dive tabs for specialists

**C. Status Badge System**
Replace text status with visual badges:

```python
def audit_badge(status):
    colors = {
        'AUDITED': '#264653',     # Dark teal - Trinity validated
        'CONVERGENT': '#2a9d8f',  # Green - High agreement
        'DRAFT': '#e9c46a',       # Gold - Work in progress
        'CRUX': '#f4a261',        # Orange - Declared impasse
        'DIVERGENT': '#e76f51'    # Red - Low agreement
    }
    return f'<span style="background:{colors.get(status,"#666")}; padding:2px 8px; border-radius:12px; color:white; font-size:0.8em">{status}</span>'
```

---

## 2. Visualization Types to Add

### Current State
The Console shows lever comparison charts and YPA trinity charts. We should add:

### A. Convergence Radar (Trinity View)
Show Claude, Grok, Nova scores as overlapping radar charts:
```python
import plotly.graph_objects as go

fig = go.Figure()
categories = ['CCI', 'EDB', 'PF-I', 'PF-E', 'AR', 'MG']

for auditor, scores in trinity_scores.items():
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],  # Close the polygon
        theta=categories + [categories[0]],
        name=auditor,
        fill='toself',
        opacity=0.6
    ))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
    title='Trinity Auditor Convergence'
)
```

### B. YPA Sensitivity Heatmap
Framework × Toggle matrix showing YPA delta when each toggle is flipped:
```python
import plotly.express as px

# Rows: Frameworks, Columns: Toggles
fig = px.imshow(
    sensitivity_matrix,
    labels=dict(x='Toggle', y='Framework', color='ΔYPA'),
    x=['Parity', 'PF-Type', 'Fallibilism', 'BFI Weight'],
    y=['MdN', 'CT', 'Buddhism', 'Islam'],
    aspect='auto',
    color_continuous_scale='RdYlGn_r',
    color_continuous_midpoint=0
)
fig.update_layout(title='Toggle Sensitivity by Framework')
```

### C. Guardrail Status Dashboard
Visual grid showing pass/fail for each guardrail per framework:
```python
# 4 guardrails × N frameworks matrix
guardrail_status = [
    ['✅', '✅'],  # Lever-Coupling
    ['✅', '⚠️'],  # BFI-Sensitivity
    ['✅', '✅'],  # Weight-Inversion
    ['✅', '✅'],  # Symmetry
]
```

### D. Preset Mode Compass
Polar chart showing where current config sits relative to preset modes:
- Skeptic (270°) - Instrumental focus
- Diplomat (0°) - Balanced center
- Seeker (90°) - Meaning-first
- Zealot (180°) - Existential-first

```python
# Calculate angle based on config values
angle = calculate_epistemic_heading(parity, pf_type, fallibilism, bfi_weight)
fig = go.Figure(go.Scatterpolar(
    r=[1], theta=[angle],
    mode='markers+text',
    marker=dict(size=20, color='#2a9d8f'),
    text=['You Are Here']
))
```

### E. Framework Battle Card
Side-by-side visual comparison with color-coded "winner" per lever:
```
┌─────────────────────────────────────────────────────┐
│          MdN  vs  CT                                │
├─────────────────────────────────────────────────────┤
│ CCI     [8.0 ████████  ] vs [7.5 ███████▌ ] → MdN  │
│ EDB     [7.5 ███████▌  ] vs [8.5 ████████▌] → CT   │
│ PF-I    [10.0 ██████████] vs [7.0 ███████  ] → MdN │
│ PF-E    [3.0 ███       ] vs [8.0 ████████ ] → CT   │
│ AR      [7.0 ███████   ] vs [8.5 ████████▌] → CT   │
│ MG      [4.0 ████      ] vs [8.5 ████████▌] → CT   │
├─────────────────────────────────────────────────────┤
│ YPA     [5.92         ] vs [6.18         ] → CT    │
└─────────────────────────────────────────────────────┘
```

---

## 3. Data Views to Surface

### Real-Time Audit Summary Panel
```
┌─────────────────────────────────────────────────────┐
│ AUDIT STATUS                    Mode: Diplomat      │
├─────────────────────────────────────────────────────┤
│ Frameworks: 2/2     │  Trinity Convergence: 98%    │
│ Guardrails: 4/4 ✅  │  Crux Declarations: 0        │
│ Active Preset: 🤝   │  Config Symmetry: Balanced   │
└─────────────────────────────────────────────────────┘
```

### Multi-Framework Comparison View
When more than 2 frameworks are loaded, show ranked table:

| Rank | Framework | YPA (Neutral) | YPA (Empirical) | YPA (Existential) | Convergence |
|------|-----------|---------------|-----------------|-------------------|-------------|
| 1 | Classical Theism | 6.18 | 5.87 | 6.94 | 98% |
| 2 | Methodological Naturalism | 5.92 | 7.42 | 4.73 | 98% |
| 3 | Buddhism | 5.45 | 4.21 | 6.89 | -- |

### Scenario Impact Panel
Show how YPA changes across the three scenarios:
```
         Neutral    Empirical   Existential
MdN      ████████   ██████████  █████
CT       ████████   ███████     ██████████
         ← Balanced  ← Prediction  ← Meaning →
```

---

## 4. Interaction Patterns

### A. Hover Details
Every chart data point should reveal details on hover (Plotly handles this)

### B. Click-to-Compare
Click a framework in the Brute Ledger to load it into Console slot A or B

### C. Toggle Animation
When config toggles change, animate the transition of YPA values

### D. Export Options
- PNG/SVG for charts
- JSON for raw audit data
- Markdown summary for documentation

---

## 5. Styling System

### Color Palette (CFA Ledger Aesthetic)
```python
CFA_COLORS = {
    # Backgrounds
    'background': 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
    'card': '#ffffff',
    'border': '#dee2e6',

    # Text
    'text': '#212529',
    'text_secondary': '#6c757d',

    # Status colors
    'audited': '#264653',      # Dark teal - validated
    'convergent': '#2a9d8f',   # Green - high agreement
    'draft': '#e9c46a',        # Gold - in progress
    'crux': '#f4a261',         # Orange - declared impasse
    'divergent': '#e76f51',    # Red - disagreement

    # Framework colors (match Brute Ledger emojis)
    'mdn': '#1f77b4',          # Blue (📘)
    'ct': '#d62728',           # Red (📕)
    'buddhism': '#9467bd',     # Purple (☸️)
    'islam': '#2ca02c',        # Green (☪️)

    # Auditor colors
    'claude': '#7b3fe4',       # Purple
    'grok': '#ff6b35',         # Orange
    'nova': '#00b4d8',         # Cyan
}
```

### Typography
- Headers: Georgia serif (matches "epistemic ledger" feel)
- Body: System sans-serif
- Monospace for metrics/scores

### Card Component
```python
def audit_card(title, content, status=None, framework_color=None):
    badge = audit_badge(status) if status else ""
    border_color = framework_color or '#dee2e6'
    return f'''
    <div style="background:#ffffff; border-radius:8px; padding:20px;
                margin:10px 0; border-left:4px solid {border_color};
                box-shadow: 0 2px 4px rgba(0,0,0,0.1)">
        <h3 style="margin:0 0 15px 0; font-family:Georgia,serif;
                   color:#212529; border-bottom:1px solid #dee2e6;
                   padding-bottom:10px">
            {title} {badge}
        </h3>
        <div style="color:#495057">{content}</div>
    </div>
    '''
```

---

## 6. Page Organization

### Sidebar Navigation Enhancement
Add radio buttons for "page mode" within Console:

1. **Compare** - Side-by-side framework comparison (current default)
2. **Analyze** - Deep dive on single framework
3. **Simulate** - Toggle sensitivity playground
4. **Audit** - Trinity convergence details
5. **Export** - Generate reports

### Each "Mode" Structure
```
┌─────────────────────────────────────┐
│ MODE TITLE                   [badge]│
├─────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Metric 1│ │ Metric 2│ │ Metric 3│ │  ← Summary cards
│ └─────────┘ └─────────┘ └─────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │     PRIMARY VISUALIZATION       │ │  ← Main chart
│ │                                 │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌───────────────┐ ┌───────────────┐ │
│ │ Detail Card 1 │ │ Detail Card 2 │ │  ← Supporting info
│ └───────────────┘ └───────────────┘ │
└─────────────────────────────────────┘
```

---

## 7. Implementation Priority

### Phase 1: Foundation
1. Add `CFA_COLORS` palette to `utils/colors.py` (NEW)
2. Create `audit_card()` helper in `components/cards.py` (NEW)
3. Restructure Console into card-based sections

### Phase 2: Visualizations
4. Add Convergence Radar chart (Trinity view)
5. Add YPA Sensitivity Heatmap
6. Add Framework Battle Card

### Phase 3: Polish
7. Implement sidebar mode navigation
8. Add remaining visualization types
9. Implement export functionality

---

## 8. Key Metrics to Always Show

1. **Framework Health:** Convergence %, guardrail status
2. **YPA Summary:** Neutral, Empirical, Existential scores
3. **Config Status:** Active preset mode, toggle states
4. **Symmetry Status:** Max delta, sensitive levers
5. **Trinity Status:** Auditor agreement level

---

## 9. Files to Create/Modify

### New Files
- `utils/colors.py` - Color palette constants
- `components/cards.py` - Reusable card components
- `components/charts.py` - Plotly visualization helpers

### Modified Files
- `pages/console.py` - Main restructure
- `app.py` - Add sidebar navigation support (if needed)

---

## 10. Connection to Matrix Page

The Console enhancements should visually harmonize with the Matrix page's "Dimensional Transit Hub" aesthetic when appropriate:

- Use similar card shadows and border radii
- Maintain consistent typography hierarchy
- Status badges should use complementary but distinct colors
- Both pages should feel like rooms in the same "estate"

The Console is the "Engineering Lab" - precise, analytical, tool-focused.
The Matrix is the "Transit Hub" - connective, navigational, federation-focused.

---

*Last updated: December 2024*
*Origin: Cross-pollination from Nyquist Consciousness dashboard patterns*
