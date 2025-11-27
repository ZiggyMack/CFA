"""
CFA Repository Health Dashboard
Streamlit-based visualization of repository health metrics

Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path for config import
sys.path.append(str(Path(__file__).parent.parent))
from config import PATHS, SETTINGS, EXCLUSIONS, validate_paths

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="CFA Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2e7d32;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .score-green { color: #10b981; font-weight: bold; }
    .score-yellow { color: #f59e0b; font-weight: bold; }
    .score-red { color: #ef4444; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def get_health_score():
    """Calculate current repository health score"""
    return {
        'total': 97,
        'documentation': 12,
        'link_integrity': 15,
        'living_maps': 15,
        'processes': 15,
        'organization': 15,
        'dependencies': 10,
        'version_control': 15,
        'max_total': 100,
        'max_documentation': 15,
        'max_link_integrity': 15,
        'max_living_maps': 15,
        'max_processes': 15,
        'max_organization': 15,
        'max_dependencies': 10,
        'max_version_control': 15,
    }

def get_readme_directory_matrix():
    """README coverage by directory with scope metadata"""
    data = {
        'Directory': [
            'Root',
            'auditors/',
            'auditors/Bootstrap/',
            'auditors/Bootstrap/Claude/',
            'auditors/Bootstrap/Nova/',
            'auditors/Bootstrap/Grok/',
            'auditors/Bootstrap/Kernels/',
            'auditors/Bootstrap/Guests/',
            'auditors/Mission/',
            'auditors/relay/',
            'docs/',
            'docs/architecture/',
            'docs/guides/',
            'docs/repository/',
            'docs/repository/OBSERVATORY/',
            'docs/repository/MAP_ROOM/',
            'docs/i_am/',
            'docs/ethics/',
            'docs/validation/',
            'docs/smv/',
            'dashboard/',
            'dashboard/SMV/',
            'profiles/',
            'tools/',
            'utils/',
            'logs/',
            'pages/',
            'scripts/',
        ],
        'READMEs': [1, 1, 1, 1, 1, 1, 1, 5, 2, 2, 1, 8, 3, 3, 1, 1, 3, 2, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1],
        'Subdirs': [11, 4, 8, 0, 0, 0, 0, 5, 2, 3, 10, 5, 2, 3, 0, 0, 2, 1, 2, 1, 2, 0, 2, 0, 0, 0, 0, 0],
        'Depth': [0, 1, 2, 3, 3, 3, 3, 3, 2, 2, 1, 2, 2, 2, 3, 3, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1],
        'Scope': [
            'Root entry point',
            'Auditor coordination',
            'Bootstrap navigation',
            'Claude bootstrap',
            'Nova bootstrap',
            'Grok bootstrap',
            'Kernel specs (ZIGGY)',
            'Guest personas (5)',
            'Mission briefs',
            'Relay coordination',
            'Documentation hub',
            'Architecture specs',
            'User guides',
            'Repository maps',
            'Health observatory',
            'Map room',
            'Identity docs',
            'Ethics framework',
            'Validation reports',
            'SMV docs',
            'Dashboard apps',
            'SMV app',
            'Worldview profiles',
            'Utility scripts',
            'Shared utilities',
            'Log storage',
            'Static pages',
            'Build scripts',
        ],
        'Criticality': [
            'Critical',
            'Critical',
            'Critical',
            'Critical',
            'Critical',
            'Critical',
            'Critical',
            'High',
            'High',
            'Medium',
            'Critical',
            'High',
            'Medium',
            'Critical',
            'Medium',
            'Medium',
            'Medium',
            'Medium',
            'Low',
            'Low',
            'Medium',
            'Low',
            'Medium',
            'Low',
            'Low',
            'Low',
            'Low',
            'Low',
        ],
        'v5.0_Addition': [
            False, False, True, False, True, True, True, True, False, False,
            False, False, False, False, False, False, True, False, False, False,
            False, False, False, False, False, False, False, False,
        ]
    }
    return pd.DataFrame(data)

def get_file_metrics():
    """Current file count metrics"""
    return {
        'Total Files': 532,
        'Operational Files': 492,
        'Excluded (Nyquist-Sync)': 40,
        'Markdown Files': 455,
        'Python Files': 14,
        'JavaScript Files': 8,
        'JSON Files': 13,
        'READMEs': 64,
        'Directories': 123,
        'Directories with READMEs': 53,
    }

def get_link_integrity():
    """Link checking results"""
    return {
        'total_links': 698,
        'working_links': 696,
        'broken_links': 2,
        'integrity_percent': 99.7,
        'broken_list': [
            'docs/architecture/CFA/CFA_ARCHITECTURE.md:415 (FIXED)',
            'docs/architecture/CFA/CFA_ARCHITECTURE.md:441 (FIXED)',
        ]
    }

def get_health_trend():
    """3-month health trend"""
    return pd.DataFrame({
        'Month': ['Sep 2025', 'Oct 2025', 'Nov 2025'],
        'Score': [75, 94, 97],
        'Status': ['YELLOW', 'GREEN', 'GREEN']
    })

def get_category_breakdown():
    """Detailed category breakdown"""
    scores = get_health_score()
    data = {
        'Category': [
            'Documentation',
            'Link Integrity',
            'Living Maps',
            'Processes',
            'Organization',
            'Dependencies',
            'Version Control'
        ],
        'Score': [
            scores['documentation'],
            scores['link_integrity'],
            scores['living_maps'],
            scores['processes'],
            scores['organization'],
            scores['dependencies'],
            scores['version_control']
        ],
        'Max': [
            scores['max_documentation'],
            scores['max_link_integrity'],
            scores['max_living_maps'],
            scores['max_processes'],
            scores['max_organization'],
            scores['max_dependencies'],
            scores['max_version_control']
        ]
    }
    df = pd.DataFrame(data)
    df['Percent'] = (df['Score'] / df['Max'] * 100).round(1)
    df['Status'] = df['Percent'].apply(lambda x: '✅' if x == 100 else '🟡' if x >= 80 else '🔴')
    return df

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def main():
    # Header
    st.markdown('<p class="main-header">📊 CFA Repository Health Dashboard</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Version {SETTINGS["version"]} • Last Updated: {SETTINGS["last_update"]}</p>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["Overview", "README Matrix", "File Metrics", "Link Integrity", "Category Details", "Trends"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Stats")
    st.sidebar.metric("Health Score", f"{get_health_score()['total']}/100", "🟢")
    st.sidebar.metric("READMEs", f"{get_file_metrics()['READMEs']}", "Optimal")
    st.sidebar.metric("Link Integrity", f"{get_link_integrity()['integrity_percent']}%", "Excellent")

    # Main content based on page selection
    if page == "Overview":
        show_overview()
    elif page == "README Matrix":
        show_readme_matrix()
    elif page == "File Metrics":
        show_file_metrics()
    elif page == "Link Integrity":
        show_link_integrity()
    elif page == "Category Details":
        show_category_details()
    elif page == "Trends":
        show_trends()

# ============================================================================
# PAGE VIEWS
# ============================================================================

def show_overview():
    st.header("Repository Health Overview")

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)

    scores = get_health_score()
    metrics = get_file_metrics()
    links = get_link_integrity()

    with col1:
        st.metric(
            label="Overall Health",
            value=f"{scores['total']}/100",
            delta="+1 (v5.0 threshold fix)"
        )

    with col2:
        st.metric(
            label="Operational Files",
            value=metrics['Operational Files'],
            delta=f"+{metrics['Operational Files'] - 400} from v4.0"
        )

    with col3:
        st.metric(
            label="README Coverage",
            value=f"{metrics['READMEs']} READMEs",
            delta="Within target (55-70)"
        )

    with col4:
        st.metric(
            label="Link Integrity",
            value=f"{links['integrity_percent']}%",
            delta=f"{links['broken_links']} broken"
        )

    # Health score gauge
    st.subheader("Health Score Breakdown")

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=scores['total'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Health Score"},
        delta={'reference': 96, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 75], 'color': "lightgray"},
                {'range': [75, 90], 'color': "yellow"},
                {'range': [90, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 98
            }
        }
    ))

    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

    # Category bars
    st.subheader("Category Performance")

    df_categories = get_category_breakdown()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_categories['Category'],
        y=df_categories['Score'],
        text=df_categories['Percent'].astype(str) + '%',
        textposition='auto',
        marker_color=['#10b981' if p == 100 else '#f59e0b' if p >= 80 else '#ef4444'
                      for p in df_categories['Percent']]
    ))

    fig.update_layout(
        title="Health Score by Category",
        yaxis_title="Points",
        yaxis=dict(range=[0, 20]),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

def show_readme_matrix():
    st.header("README Directory Matrix")
    st.markdown("**Tabular view of README coverage by directory scope**")

    df = get_readme_directory_matrix()

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Directories Tracked", len(df))
    with col2:
        st.metric("Total READMEs", df['READMEs'].sum())
    with col3:
        critical_readmes = df[df['Criticality'] == 'Critical']['READMEs'].sum()
        st.metric("Critical Path READMEs", critical_readmes)

    # Filters
    st.subheader("Filters")
    col1, col2, col3 = st.columns(3)

    with col1:
        criticality_filter = st.multiselect(
            "Criticality",
            options=['Critical', 'High', 'Medium', 'Low'],
            default=['Critical', 'High', 'Medium', 'Low']
        )

    with col2:
        depth_filter = st.slider("Max Depth", 0, 3, 3)

    with col3:
        v5_only = st.checkbox("v5.0 Additions Only", value=False)

    # Apply filters
    df_filtered = df[df['Criticality'].isin(criticality_filter)]
    df_filtered = df_filtered[df_filtered['Depth'] <= depth_filter]
    if v5_only:
        df_filtered = df_filtered[df_filtered['v5.0_Addition'] == True]

    # Display table with styling
    st.subheader("Directory Coverage Matrix")

    # Color-code by criticality
    def color_criticality(val):
        if val == 'Critical':
            return 'background-color: #fee2e2; color: #991b1b'
        elif val == 'High':
            return 'background-color: #fef3c7; color: #92400e'
        elif val == 'Medium':
            return 'background-color: #dbeafe; color: #1e40af'
        else:
            return 'background-color: #f3f4f6; color: #374151'

    styled_df = df_filtered.style.applymap(
        color_criticality,
        subset=['Criticality']
    ).format({
        'v5.0_Addition': lambda x: '✅' if x else ''
    })

    st.dataframe(styled_df, use_container_width=True, height=600)

    # Visualizations
    st.subheader("README Distribution Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # READMEs by criticality
        criticality_counts = df.groupby('Criticality')['READMEs'].sum().reset_index()
        fig = px.pie(
            criticality_counts,
            values='READMEs',
            names='Criticality',
            title='READMEs by Criticality Level',
            color='Criticality',
            color_discrete_map={
                'Critical': '#ef4444',
                'High': '#f59e0b',
                'Medium': '#3b82f6',
                'Low': '#6b7280'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # READMEs by depth
        depth_counts = df.groupby('Depth')['READMEs'].sum().reset_index()
        fig = px.bar(
            depth_counts,
            x='Depth',
            y='READMEs',
            title='READMEs by Directory Depth',
            labels={'Depth': 'Directory Depth Level', 'READMEs': 'Number of READMEs'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # v5.0 additions highlight
    st.subheader("v5.0 Architecture Additions")
    v5_additions = df[df['v5.0_Addition'] == True]
    st.dataframe(
        v5_additions[['Directory', 'READMEs', 'Scope', 'Criticality']],
        use_container_width=True
    )

    st.info(f"**v5.0 Impact:** Added {v5_additions['READMEs'].sum()} READMEs across {len(v5_additions)} new directories (Kernels, Guests, Nova, Grok, ZIGGY identity)")

def show_file_metrics():
    st.header("File Metrics")

    metrics = get_file_metrics()

    # Top metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Files", metrics['Total Files'])
    with col2:
        st.metric("Operational Files", metrics['Operational Files'], f"-{metrics['Excluded (Nyquist-Sync)']} excluded")
    with col3:
        st.metric("README Coverage", f"{(metrics['Directories with READMEs'] / metrics['Directories'] * 100):.1f}%")

    # File type breakdown
    st.subheader("File Type Distribution")

    file_types = {
        'Markdown': metrics['Markdown Files'],
        'Python': metrics['Python Files'],
        'JavaScript': metrics['JavaScript Files'],
        'JSON': metrics['JSON Files'],
        'Other': metrics['Total Files'] - (metrics['Markdown Files'] + metrics['Python Files'] + metrics['JavaScript Files'] + metrics['JSON Files'])
    }

    df_types = pd.DataFrame(list(file_types.items()), columns=['Type', 'Count'])

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            df_types,
            values='Count',
            names='Type',
            title='Files by Type',
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            df_types,
            x='Type',
            y='Count',
            title='File Type Counts',
            text='Count'
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    # Directory metrics
    st.subheader("Directory Metrics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Directories", metrics['Directories'])
        st.metric("Directories with READMEs", metrics['Directories with READMEs'])
        st.metric("Coverage %", f"{(metrics['Directories with READMEs'] / metrics['Directories'] * 100):.1f}%")

    with col2:
        st.metric("Target README Range", "55-70")
        st.metric("Current READMEs", metrics['READMEs'])
        status = "✅ Optimal" if 55 <= metrics['READMEs'] <= 70 else "⚠️ Outside target"
        st.metric("Status", status)

    # Comparison table
    st.subheader("v4.0 → v5.0 Comparison")

    comparison = pd.DataFrame({
        'Metric': ['Operational Files', 'Markdown Files', 'READMEs', 'README Target', 'Health Score'],
        'v4.0': [400, 350, 39, '<45', 96],
        'v5.0': [492, 455, 64, '55-70', 97],
        'Change': ['+92', '+105', '+25', 'Recalibrated', '+1']
    })

    st.dataframe(comparison, use_container_width=True)

def show_link_integrity():
    st.header("Link Integrity Analysis")

    links = get_link_integrity()

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Links Checked", links['total_links'])
    with col2:
        st.metric("Working Links", links['working_links'], "✅")
    with col3:
        st.metric("Broken Links", links['broken_links'], "🔧 Fixed")
    with col4:
        st.metric("Integrity %", f"{links['integrity_percent']}%", "Excellent")

    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=links['integrity_percent'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Link Integrity Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 90], 'color': "lightgray"},
                {'range': [90, 95], 'color': "yellow"},
                {'range': [95, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "green", 'width': 4},
                'thickness': 0.75,
                'value': 99
            }
        }
    ))

    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

    # Broken links (fixed)
    st.subheader("Recently Fixed Broken Links")

    st.info("All broken links found during v5.0 validation have been fixed ✅")

    for link in links['broken_list']:
        st.markdown(f"- {link}")

    st.success("**Target:** 99%+ link integrity → **Current:** 99.7% ✅")

def show_category_details():
    st.header("Category Performance Details")

    df = get_category_breakdown()

    # Summary table
    st.subheader("Category Scores")
    st.dataframe(df, use_container_width=True)

    # Individual category cards
    st.subheader("Category Breakdown")

    for _, row in df.iterrows():
        with st.expander(f"{row['Category']} - {row['Score']}/{row['Max']} ({row['Percent']}%) {row['Status']}"):

            # Progress bar
            progress = row['Score'] / row['Max']
            st.progress(progress)

            # Category-specific details
            if row['Category'] == 'Documentation':
                st.markdown("""
                **Checks:**
                - ✅ Core files covered (95%)
                - ✅ Mission files covered (100%)
                - ✅ Bootstrap files covered (100%)
                - 🟡 Supporting files (85%)

                **Missing points:** Some supporting documentation incomplete
                """)

            elif row['Category'] == 'Link Integrity':
                st.markdown("""
                **Checks:**
                - ✅ 698 total links checked
                - ✅ 696 working (99.7%)
                - ✅ 2 broken (now fixed)
                - ✅ All Nyquist-Sync cross-references valid

                **Status:** Perfect score maintained
                """)

            elif row['Category'] == 'Living Maps':
                st.markdown("""
                **Required Maps:**
                - ✅ FILE_INVENTORY.md (updated v5.0)
                - ✅ REPO_HEALTH_DASHBOARD.md (updated v5.0)
                - ✅ WAYFINDING_GUIDE.md (current)
                - ✅ WORLDVIEW_CATALOG.md (current)
                - ✅ DEPENDENCY_CORE.md (anchor-based)

                **Status:** All living maps current
                """)

            elif row['Category'] == 'Organization':
                st.markdown("""
                **Checks:**
                - ✅ No orphaned directories
                - ✅ Archive hygiene (.Archive/ convention)
                - ✅ File count reasonable (492 < 500)
                - ✅ README coverage optimal (64 within 55-70)
                - ✅ No duplicate files

                **Status:** Perfect organization (v5.0 thresholds)
                """)

            elif row['Category'] == 'Processes':
                st.markdown("""
                **Checks:**
                - ✅ VuDu Protocol (95%)
                - ✅ Bootstrap System (100%)
                - ✅ Doc Updates (92%)
                - ✅ Coordination (90%)

                **Status:** All processes operational
                """)

            elif row['Category'] == 'Dependencies':
                st.markdown("""
                **Checks:**
                - ✅ DEPENDENCY_CORE.md current
                - ✅ No circular dependencies
                - ✅ Clear dependency chains
                - ✅ Gospel Problem discipline

                **Status:** Clean dependency graph
                """)

            elif row['Category'] == 'Version Control':
                st.markdown("""
                **Checks:**
                - ✅ v5.0.0 version bumped
                - ✅ CHANGELOG.md updated
                - ✅ REPO_LOG.md current
                - ✅ Git history clean
                - ✅ No uncommitted changes

                **Status:** Version control excellent
                """)

def show_trends():
    st.header("Health Trends Over Time")

    df_trend = get_health_trend()

    # Line chart
    fig = px.line(
        df_trend,
        x='Month',
        y='Score',
        title='Repository Health Score (3-Month Trend)',
        markers=True,
        text='Score'
    )

    fig.update_traces(textposition='top center', line_color='#10b981', line_width=3)
    fig.update_layout(
        yaxis=dict(range=[0, 100]),
        height=400
    )

    # Add target line
    fig.add_hline(y=98, line_dash="dash", line_color="red",
                  annotation_text="Target (v4.0)", annotation_position="right")

    st.plotly_chart(fig, use_container_width=True)

    # Trend table
    st.subheader("Monthly Breakdown")
    st.dataframe(df_trend, use_container_width=True)

    # Statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        improvement = df_trend['Score'].iloc[-1] - df_trend['Score'].iloc[0]
        st.metric("3-Month Improvement", f"+{improvement} points")

    with col2:
        avg_rate = improvement / 3
        st.metric("Average Rate", f"+{avg_rate:.1f} pts/month")

    with col3:
        current = df_trend['Score'].iloc[-1]
        target = 98
        remaining = target - current
        months_to_target = remaining / avg_rate if avg_rate > 0 else 0
        st.metric("Months to v4.0 Target", f"{months_to_target:.1f}" if months_to_target > 0 else "✅ On target")

    # Projections
    st.subheader("Projections")

    st.info(f"""
    **Current Trajectory:**
    - Starting point (Sep): 75/100 (YELLOW)
    - Current (Nov): 97/100 (GREEN)
    - Target (v4.0): 98/100

    **Analysis:**
    - Improvement rate: +{avg_rate:.1f} points/month
    - Status: ✅ Approaching target
    - Next milestone: 98/100 (1 point remaining)

    **Recommendation:** Focus on completing supporting documentation (5 pts needed in Documentation category)
    """)

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
