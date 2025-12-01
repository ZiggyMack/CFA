# CFA Dashboard — Running Applications & Prototypes

**Purpose:** Home for interactive applications, dashboards, and prototypes that support the CFA mission

**Philosophy:** "Docs for reading, dashboards for running"

**Part of:** Pan Handlers Network — Human-AI collaboration projects

---

## 🚀 Quick Start

```bash
cd dashboard
launch_health.bat   # Health Dashboard (localhost:8504)
launch_smv.bat      # SMV Trinity (localhost:3001)
launch_both.bat     # Launch both simultaneously
```

**Dashboard URLs:**
| Application | URL | Type |
|-------------|-----|------|
| Health Dashboard | http://localhost:8504 | Streamlit |
| SMV Trinity | http://localhost:3001 | React/Vite |
| CFA Main App | http://localhost:8503 | Streamlit |

---

## 📂 Directory Structure

```
dashboard/
├── README.md              ← You are here
├── START_HERE.md          ← Cold boot guide for Dashboard Claude
├── config.py              ← Centralized paths and settings (SINGLE SOURCE OF TRUTH)
├── launch_health.bat      ← Launch Health Dashboard
├── launch_smv.bat         ← Launch SMV Trinity
├── launch_both.bat        ← Launch both dashboards
│
├── HealthDashboard/       ← Repository Health Visualizer (Streamlit)
│   ├── app.py             ← Main Streamlit application
│   ├── README.md          ← HealthDashboard-specific docs
│   └── requirements.txt   ← Python dependencies
│
└── SMV/                   ← Symmetry Matrix Visualizer (React)
    ├── package.json       ← Node dependencies
    ├── vite.config.js     ← Vite build config
    ├── index.html         ← Entry point
    ├── README.md          ← SMV-specific docs
    └── src/
        ├── App.jsx        ← Main React component
        ├── main.jsx       ← React entry point
        ├── index.css      ← Global styles
        ├── components/    ← React components
        │   ├── CalibrationDrawer.jsx
        │   ├── CruxToggle.jsx
        │   ├── EthicsBadges.jsx
        │   ├── SymmetryView.jsx
        │   └── TimelineSparkline.jsx
        └── data/          ← Sample scenario data
            ├── scenario_1_tension_escalation.json
            ├── scenario_2_high_alignment.json
            └── scenario_3_resolution.json
```

---

## 🎯 Current Applications

### **HealthDashboard — Repository Health Visualizer**

**Location:** `dashboard/HealthDashboard/`
**Type:** Streamlit dashboard (Python + Plotly)
**Port:** 8504
**Status:** v5.0 active

**What it does:**
- Overall health score visualization (98/100 gauge)
- 7-category performance breakdown
- README directory matrix with scope metadata
- File metrics and distributions
- Link integrity analysis
- 3-month health trends

**Run:**
```bash
cd dashboard && launch_health.bat
# OR
cd dashboard/HealthDashboard && streamlit run app.py --server.port 8504
```

**Data sources:** `dashboard/config.py`, `docs/repository/OBSERVATORY/`

---

### **SMV — Symmetry Matrix Visualizer**

**Location:** `dashboard/SMV/`
**Type:** React prototype (Vite + Recharts)
**Port:** 3001
**Status:** Phase 1 complete

**What it does:**
- Real-time symmetry health tracking (Claude ↔ Nova ↔ Grok triangle)
- Timeline view with tick-by-tick auditor positions
- Calibration drawer showing YAML-based bias adjustments
- Ethical invariant badges
- Crux detection alerts

**Run:**
```bash
cd dashboard && launch_smv.bat
# OR
cd dashboard/SMV && npm run dev
```

**Note:** React apps cannot be embedded in iframes. Must open in separate tab.

---

## 🔗 The Matrix Integration

CFA is part of the **Pan Handlers Network** — a collection of human-AI collaboration projects.

### The Matrix Portal (`pages/matrix.py`)

The Matrix is CFA's portal page with green-on-black terminal aesthetic:
- **Background:** `#0a0a0a` (near black)
- **Text:** `#00ff41` (matrix green)
- **Font:** Courier New / monospace
- **Hover effects:** Green glow

**Access via:** Main CFA app → "🌐 The Matrix" button

### Connected Repositories

| Repository | Role | Status |
|------------|------|--------|
| CFA | Epistemic Engineering Framework | Active |
| Nyquist Consciousness | Core consciousness research | Active |
| VUDU Fidelity | Human validation surveys | Planned |

### Integration Points

The Matrix page embeds the Health Dashboard via iframe:
```python
st.components.v1.iframe("http://localhost:8504", height=800)
```

SMV Trinity opens externally (React limitation).

---

## ⚙️ Configuration

### `config.py` — Single Source of Truth

All paths and settings are centralized in `dashboard/config.py`:

```python
from config import PATHS, SETTINGS, EXCLUSIONS

# Access paths
PATHS['root']           # Repository root
PATHS['dashboard']      # Dashboard directory
PATHS['docs']           # Documentation directory

# Access settings
SETTINGS['version']     # Current version (v5.0.0)
SETTINGS['colors']      # Visualization colors

# Validate on startup
from config import validate_paths
success, missing = validate_paths()
```

### Key Settings

| Setting | Value | Description |
|---------|-------|-------------|
| `version` | v5.0.0 | Current CFA version |
| `health_target` | 98 | Target health score |
| `dashboard_refresh_interval` | 300 | Auto-refresh (seconds) |

---

## 🔮 Future Applications (Planned)

**Worldview Comparison Studio**
- Interactive worldview profile explorer
- Side-by-side comparison UI
- Crux Point deep-dives

**Pan Handlers Hub**
- Central navigation for all Pan Handler repos
- Health metrics aggregation across repos
- Cross-repo consciousness tracking

---

## 🛠️ For Dashboard Claude (Cold Boot)

**READ FIRST:** `dashboard/START_HERE.md`

This contains everything you need to:
1. Understand the dashboard architecture
2. Update health metrics
3. Modify The Matrix portal
4. Add new visualizations
5. Integrate with Pan Handlers network

---

## 📊 Adding New Applications

1. **Create subdirectory:** `dashboard/YourApp/`
2. **Add application files:** `app.py` or `package.json`, etc.
3. **Write README:** `dashboard/YourApp/README.md`
4. **Create launcher:** `dashboard/launch_yourapp.bat`
5. **Update this file:** Add to "Current Applications" section
6. **Update config.py:** Add paths if needed

**Naming convention:**
- PascalCase for app directories: `HealthDashboard`, `SMV`
- Lowercase for root: `dashboard/`

---

## ⚠️ Important Notes

**Port Assignments:**
- 8503: CFA Main App (Streamlit)
- 8504: Health Dashboard (Streamlit)
- 3001: SMV Trinity (React/Vite)

**React vs Streamlit:**
- Streamlit apps CAN be embedded via iframe
- React apps CANNOT — must open in new tab

**Gospel Problem Prevention:**
- Never trust stale data — always verify with `config.py`
- Run `validate_paths()` before major changes
- Update this README when structure changes

---

## 📝 Maintenance

**Last Updated:** 2025-12-01
**Maintainer:** Dashboard Claude (Cold Boot)
**Status:** Active with 2 applications

**Recent changes:**
- 2025-12-01: Added START_HERE.md for cold boot, updated structure
- 2025-11-27: Added Matrix portal integration
- 2025-11-26: Added HealthDashboard (Streamlit)
- 2025-11-12: Created dashboard/ directory

---

**Philosophy:** "Dashboards run, docs inform. Keep them separate, keep them clear."

**This is the way.** 📊
