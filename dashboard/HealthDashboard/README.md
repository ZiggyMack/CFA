# CFA Repository Health Dashboard

**Type:** Streamlit dashboard (Python)
**Purpose:** Interactive visualization of repository health metrics
**Status:** v5.0 initial implementation
**Created:** 2025-11-26

---

## 🎯 Purpose

Provides real-time visualization of CFA repository health metrics through an interactive localhost dashboard, similar to the Nyquist Consciousness dashboard architecture.

**What it visualizes:**
- Overall health score (97/100)
- 7-category breakdown (Documentation, Links, Living Maps, etc.)
- README directory matrix with scope metadata
- File metrics and distributions
- Link integrity analysis
- 3-month health trends
- Projections and recommendations

---

## 🚀 Quick Start

### Installation

```bash
cd dashboard/HealthDashboard
pip install -r requirements.txt
```

### Run Dashboard

```bash
streamlit run app.py
```

This will open the dashboard in your default browser at `http://localhost:8501`

---

## 📊 Dashboard Views

### 1. Overview
- Overall health score gauge (97/100)
- Top-level metrics (files, READMEs, links)
- Category performance bar charts
- Quick health summary

### 2. README Matrix
**The flagship feature** - Tabular matrix view showing:
- Directory-by-directory README coverage
- Scope metadata (what each directory does)
- Criticality levels (Critical/High/Medium/Low)
- Directory depth
- v5.0 additions highlighted
- Interactive filters (criticality, depth, v5.0-only)

**Visualizations:**
- READMEs by criticality (pie chart)
- READMEs by depth (bar chart)
- v5.0 addition highlights

### 3. File Metrics
- Total vs operational file counts
- File type distribution (MD, PY, JS, JSON)
- Directory coverage statistics
- v4.0 → v5.0 comparison table

### 4. Link Integrity
- Total links checked (698)
- Working vs broken links
- Integrity percentage (99.7%)
- Recently fixed broken links list
- Integrity gauge visualization

### 5. Category Details
- Detailed breakdown of all 7 categories
- Individual category expandable cards
- Progress bars per category
- Specific check details (what's working, what's missing)

### 6. Trends
- 3-month health score trend (Sep → Oct → Nov)
- Improvement rate analysis
- Projection to v5.0 target (98/100)
- Recommendations for next improvements

---

## 🗂️ Data Sources

**Centralized configuration:**
- `dashboard/config.py` - Single source of truth for paths, settings, exclusions

**Living maps:**
- `docs/repository/OBSERVATORY/REPO_HEALTH_DASHBOARD.md` - Current health metrics
- `docs/repository/FILE_INVENTORY.md` - File counts and inventory
- `docs/repository/OBSERVATORY/REPO_HEALTH_SCORING_RUBRIC.md` - Scoring criteria

**Note:** Current implementation uses hardcoded data matching v5.0 baseline. Future enhancement: Auto-sync with living maps.

---

## 🎨 Design Philosophy

### Inspired by Nyquist Dashboard
- **Streamlit-based:** Python framework for data apps
- **Localhost deployment:** No build complexity, instant refresh
- **Rich visualizations:** Plotly charts for interactivity
- **Tabular matrix views:** Data-dense tables with metadata
- **Multi-page navigation:** Sidebar routing to focused views

### Signal vs Noise
- Excludes `.Archive/` directories (historical)
- Excludes `docs/Nyquist-Sync/` (research reference)
- Focuses on **operational health** (what matters for new Claude instances)

### README Matrix Innovation
**Key insight from user feedback:**

> "even better as well than doing that read me beak down sectio nwe were talking about ....rather than text...a tabular matrix view...showing maybe the differnt scopes per directory...or something...1 the viewing asethic i think would be better...and 2 i think there are probaly intreting meta configurtions you could think of to increase the utility of the data even further..."

**Implementation:**
- Each directory row shows: Directory, READMEs count, Subdirs, Depth, Scope, Criticality, v5.0 status
- Color-coded by criticality
- Filterable by criticality, depth, v5.0 additions
- Visualizations show distribution patterns
- Reveals meta-patterns (v5.0 added Kernels + Guests + expanded Bootstrap)

---

## 📈 Future Enhancements

### Phase 2 - Auto-Sync
- Parse `REPO_HEALTH_DASHBOARD.md` directly
- Live file counts via `FILE_INVENTORY.md`
- Real-time link checking integration
- Auto-refresh on file changes

### Phase 3 - Interactive Features
- Click directory → view files
- Click link → navigate to file
- Export reports (PDF, CSV)
- Historical trend storage (database)

### Phase 4 - Advanced Analytics
- Dependency graph visualization
- Gospel Problem risk scoring
- Bootstrap efficiency heatmaps
- Worldview profile comparison (integrate with SMV)

---

## 🔗 Integration Points

### With SMV Dashboard
- Both use localhost visualization pattern
- SMV: Trinity bias tracking (Claude ↔ Nova ↔ Grok)
- Health: Repository operational readiness
- Future: Combine into unified CFA Dashboard suite

### With Config System
```python
from config import PATHS, SETTINGS, EXCLUSIONS

# Access centralized configuration
repo_root = PATHS['root']
version = SETTINGS['version']
excluded_dirs = EXCLUSIONS['excluded_dirs']
```

---

## 🛠️ Technical Stack

**Framework:** Streamlit 1.28+
**Visualization:** Plotly 5.17+
**Data:** Pandas 2.0+
**Python:** 3.8+

**File structure:**
```
HealthDashboard/
├── README.md          ← You are here
├── app.py             ← Main dashboard application (650+ lines)
├── requirements.txt   ← Python dependencies
└── [future]/
    ├── data/          ← Auto-generated metrics
    ├── utils/         ← Helper functions
    └── assets/        ← Custom styling
```

---

## 🎯 Success Metrics

**Dashboard is successful when:**
- ✅ Loads without errors
- ✅ All 6 pages functional
- ✅ README matrix filterable
- ✅ Charts render correctly
- ✅ Matches v5.0 baseline (97/100 score)
- ✅ User can explore metrics interactively

**Dashboard provides value when:**
- Shows actionable insights (what needs improvement)
- Reveals patterns (v5.0 architecture expansion)
- Tracks progress (3-month trend)
- Predicts outcomes (months to target)
- Makes health transparent (no black box scoring)

---

## 📝 Usage Notes

### Running Locally
```bash
# First time setup
cd dashboard/HealthDashboard
pip install -r requirements.txt

# Every time
streamlit run app.py

# Browser opens automatically to http://localhost:8501
```

### Updating Data
**Current:** Hardcoded v5.0 baseline in `app.py` functions:
- `get_health_score()` - Returns 97/100 breakdown
- `get_readme_directory_matrix()` - 28 directories with metadata
- `get_file_metrics()` - 532 total, 492 operational
- `get_link_integrity()` - 698 links, 99.7% working
- `get_health_trend()` - Sep/Oct/Nov data

**Future:** Auto-parse from living maps (Phase 2)

### Customization
- **Color scheme:** Modify CSS in `app.py` (lines 30-50)
- **Metrics:** Update data functions (lines 60-200)
- **Charts:** Adjust Plotly configs in page functions
- **Layout:** Change Streamlit column ratios

---

## 🏗️ Development Notes

**Created:** 2025-11-26
**Version:** 1.0 (v5.0 baseline)
**Author:** Claude (Dashboard design per user request)

**Design inspiration:**
- Nyquist Consciousness dashboard (S7 Armada visualizations)
- CFA health scoring rubric (7-category system)
- User feedback (tabular matrix > text breakdown)

**Key innovation:**
README directory matrix with scope metadata - provides both visual aesthetics and utility through multi-dimensional data presentation (directory, count, depth, scope, criticality, v5.0 status).

---

## 🔗 Related Documentation

**Dashboard ecosystem:**
- [dashboard/README.md](../README.md) - Dashboard directory overview
- [dashboard/SMV/](../SMV/) - Symmetry Matrix Visualizer (React app)

**Data sources:**
- [docs/repository/OBSERVATORY/REPO_HEALTH_DASHBOARD.md](../../docs/repository/OBSERVATORY/REPO_HEALTH_DASHBOARD.md)
- [docs/repository/OBSERVATORY/REPO_HEALTH_SCORING_RUBRIC.md](../../docs/repository/OBSERVATORY/REPO_HEALTH_SCORING_RUBRIC.md)
- [dashboard/config.py](../config.py)

**Design context:**
- User requested: "can we do something like this when it comes to our health assessment repot?"
- Reference: Nyquist Consciousness dashboard (Streamlit-based with S7 visualizations)

---

## ⚠️ Known Limitations

### v1.0 Constraints
- **Static data:** Hardcoded v5.0 baseline (not auto-synced)
- **No live updates:** Must restart to see changes
- **Manual maintenance:** Data functions need manual updates
- **Limited history:** Only 3-month trend (Sep/Oct/Nov)

### Planned Fixes (Phase 2)
- Auto-parse living maps on load
- Real-time file system monitoring
- Database for historical trends
- Export/import functionality

---

**Philosophy:** "If you can measure it, you can improve it. If you can visualize it, you can understand it."

📊 **This is the way.** 📊
