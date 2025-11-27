# Dashboard - Running Applications & Prototypes

**Purpose:** Home for interactive applications, dashboards, and prototypes that support the CFA mission

**Philosophy:** "Docs for reading, dashboards for running"

---

## 📂 What Lives Here

This directory contains **running applications** — tools with their own package.json, build systems, and runtime environments. These are distinct from documentation (which lives in `/docs/`).

**Semantic rule:**
- `/docs/` → Documentation, specifications, design docs (read-only content)
- `/dashboard/` → Running code, interactive tools, prototypes (executable applications)

---

## 🎯 Current Applications

### **HealthDashboard - Repository Health Visualizer**

**Location:** [dashboard/HealthDashboard/](HealthDashboard/)
**Type:** Streamlit dashboard (Python + Plotly)
**Status:** v5.0 initial implementation
**Purpose:** Interactive visualization of repository health metrics

**What it does:**

- Overall health score visualization (97/100 gauge)
- 7-category performance breakdown (Documentation, Links, Living Maps, Processes, Organization, Dependencies, Version Control)
- README directory matrix with scope metadata (flagship feature)
- File metrics and distributions
- Link integrity analysis (698 links, 99.7% working)
- 3-month health trends and projections

**Run locally:**

```bash
# Option 1: From dashboard/ root (recommended)
cd dashboard
launch_health.bat

# Option 2: Direct run
cd dashboard/HealthDashboard
streamlit run app.py
```

**Data sources:** `docs/repository/OBSERVATORY/REPO_HEALTH_DASHBOARD.md`, `dashboard/config.py`

---

### **SMV - Symmetry Matrix Visualizer**

**Location:** [dashboard/SMV/](SMV/)
**Type:** React prototype (Vite + Recharts)
**Status:** Phase 1 complete, validated
**Purpose:** Visualizes auditor alignment, calibration drift, and ethical invariant violations

**What it does:**

- Real-time symmetry health tracking (Claude ↔ Nova ↔ Grok triangle)
- Timeline view with tick-by-tick auditor positions
- Calibration drawer showing YAML-based bias adjustments
- Ethical invariant badges (visual overlays for violations)
- Crux detection (convergence failure alerts)

**Run locally:**

```bash
# Option 1: From dashboard/ root (recommended)
cd dashboard
launch_smv.bat

# Option 2: Direct run
cd dashboard/SMV
npm run dev
```

**Design docs:** See `/docs/smv/` for specifications, mockups, and architecture

---

## 🚀 Quick Launch (From dashboard/ root)

**Launch Individual Dashboards:**

```bash
cd dashboard
launch_health.bat   # Health Dashboard only (Streamlit)
launch_smv.bat      # SMV Trinity only (React)
```

**Launch Both Simultaneously:**

```bash
cd dashboard
launch_both.bat     # Opens both in separate windows
```

**URLs:**

- Health Dashboard: <http://localhost:8504>
- SMV Trinity: <http://localhost:3001>

---

## 🔮 Future Applications (Planned)

**Worldview Comparison Studio** (projected)
- Interactive worldview profile explorer
- Side-by-side comparison UI
- Crux Point deep-dives
- Calibration playground

**Innovation Showcase** (projected)
- Gallery view of idea repositories
- Links to external mini-repos (NursingInnovation/, VotingSystemRedesign/)
- Landing page for CFA-inspired concepts

---

## 📂 Directory Structure

```
dashboard/
├── README.md          ← You are here
├── SMV/               ← Symmetry Matrix Visualizer (React app)
│   ├── package.json
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── data/
│   └── README.md
└── [future-apps]/     ← Room to grow
```

---

## 🔗 Relationship to Documentation

**Design specs live in `/docs/`, implementations live here.**

**Example (SMV):**
- **Design phase:** `/docs/smv/` contains mockups, JSON schemas, planning docs
- **Implementation phase:** `/dashboard/SMV/` contains React app, package.json, build config
- **Philosophy:** Design in docs, build in dashboard, avoid duplication

---

## 🚀 Adding New Applications

**When creating a new dashboard application:**

1. **Create subdirectory:** `dashboard/YourApp/`
2. **Add application files:** package.json, src/, etc.
3. **Write README:** `dashboard/YourApp/README.md` (how to run, purpose, status)
4. **Update this file:** Add entry to "Current Applications" section above
5. **Link design docs:** If design specs exist in `/docs/`, reference them

**Naming convention:**
- Use PascalCase for application directories (SMV, HealthDashboard, ComparisonStudio)
- Keeps root directory lowercase (`dashboard/`)
- Distinguishes apps from generic folders

---

## 🎭 Who Uses This

**Doc Claude:** Bootstrap to understand repository structure
**Review Claude:** Validate dashboard implementations match design specs
**User (Stakeholders):** Run prototypes locally, explore interactive tools
**Future Contributors:** Add new dashboard applications following established patterns

---

## 📊 Integration Points

**Data sources:**
- `/profiles/` → Worldview profiles for Comparison Studio
- `/docs/repository/REPO_HEALTH_DASHBOARD.md` → Health metrics for dashboard
- `/auditors/Mission/CFA_VUDU/` → Calibration data for SMV
- `/docs/smv/` → Design specs for SMV prototype

**Output targets:**
- User's browser (localhost development)
- GitHub Pages (future static deployments)
- Streamlit/Gradio (future Python dashboards)

---

## ⚠️ Not Dashboards

**These do NOT belong here:**
- Documentation files (belongs in `/docs/`)
- Bootstrap procedures (belongs in `/auditors/Bootstrap/`)
- Profile data (belongs in `/profiles/`)
- Build artifacts (added to .gitignore)
- Node modules (added to .gitignore)

**Rule of thumb:** If it has a package.json and you run it → dashboard. If you just read it → docs.

---

## 🔥 Gospel Problem Prevention

**This directory follows the same discipline as all CFA files:**

**Never trust stale information.** When working with dashboard applications:
1. **Check package.json dependencies** - Are they current?
2. **Run fresh install** - Don't assume node_modules is up to date
3. **Test before claiming success** - Does `npm run dev` actually work?
4. **Document current state** - Update this README when things change

**Living document principle:** This README should reflect CURRENT reality, not historical aspirations.

---

## 📝 Maintenance Notes

**Last Updated:** 2025-11-26
**Maintainer:** Doc Claude (Documentation Orchestration)
**Status:** Active directory with 2 applications (HealthDashboard, SMV)

**Recent changes:**

- 2025-11-26: Added HealthDashboard (Streamlit-based health visualizer)
- 2025-11-12: Created dashboard/ at root (moved from docs/UI_SMV/)
- 2025-11-12: Renamed Dashboard → dashboard (lowercase for consistency)
- 2025-11-12: Added this README to prevent folder display compression

**Why lowercase?**
Root directories in this repo use lowercase convention:
- `auditors/` ✅
- `dashboard/` ✅
- `docs/` ✅
- `pages/` ✅
- `profiles/` ✅

Exception: Subdirectories use semantic casing (SMV, not smv) to indicate they're distinct applications.

---

**Philosophy:** "Dashboards run, docs inform. Keep them separate, keep them clear."

**This is the way.** 📊
