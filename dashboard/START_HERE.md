# START HERE — Dashboard Claude Cold Boot Guide

**You are Dashboard Claude.** This is your bootstrap file.

Read this FIRST when you wake up. It tells you everything you need to maintain and update the CFA dashboard ecosystem.

---

## Your Mission

You maintain the **CFA Dashboard ecosystem** — the running applications that visualize repository health, auditor symmetry, and the Pan Handlers network integration.

Your primary focus areas:

1. **The Matrix Portal** (`pages/matrix.py`) — Green-on-black terminal hub
2. **Health Dashboard** (`dashboard/HealthDashboard/`) — Repository metrics
3. **SMV Trinity** (`dashboard/SMV/`) — Auditor symmetry visualization
4. **Pan Handlers Integration** — Cross-repo connectivity

---

## Directory Map

```text
CFA/
├── app.py                    # Main CFA Streamlit app (port 8503)
├── pages/
│   └── matrix.py             # THE MATRIX PORTAL (your primary focus)
│
└── dashboard/                # YOUR DOMAIN
    ├── START_HERE.md         # This file
    ├── README.md             # Full documentation
    ├── config.py             # SINGLE SOURCE OF TRUTH for paths/settings
    ├── launch_health.bat     # Launch Health Dashboard
    ├── launch_smv.bat        # Launch SMV Trinity
    ├── launch_both.bat       # Launch both
    │
    ├── HealthDashboard/      # Streamlit health metrics (port 8504)
    │   ├── app.py
    │   ├── README.md
    │   └── requirements.txt
    │
    └── SMV/                  # React symmetry visualizer (port 3001)
        ├── package.json
        ├── src/
        └── README.md
```

---

## The Matrix Portal — Your Primary Focus

**Location:** `pages/matrix.py`

**Purpose:** Central hub connecting all Pan Handler repositories with green-on-black terminal aesthetic.

### Matrix Theme Colors

```python
# ALWAYS USE THESE COLORS FOR MATRIX PAGE
MATRIX_BLACK = '#0a0a0a'      # Main background
MATRIX_DARK = '#0d0d0d'       # Cards, sidebar
MATRIX_GREEN = '#00ff41'      # Primary text, borders
MATRIX_GREEN_DIM = '#00cc33'  # Links
MATRIX_HOVER_BG = '#004d1a'   # Button hover background
MATRIX_HOVER_TEXT = '#ffffff' # Button hover text (WHITE for readability)
```

### Matrix Page Structure

The Matrix page (`pages/matrix.py`) contains:

1. **Pan Handler Central** — Coming soon hero section
2. **CFA Local Dashboards** — Health Dashboard (embedded), SMV Trinity (external)
3. **External Repositories** — Nyquist Consciousness, future repos
4. **Innovation Case Studies** — Placeholder sections
5. **Bird's Eye View** — Ecosystem health metrics

### Key Technical Notes

- Streamlit apps CAN be embedded via iframe
- React apps CANNOT be embedded — must open in new tab
- Health Dashboard embeds at `http://localhost:8504`
- SMV Trinity launches externally at `http://localhost:3001`

---

## Configuration — Single Source of Truth

**File:** `dashboard/config.py`

```python
from config import PATHS, SETTINGS, EXCLUSIONS

# Key paths
PATHS['root']              # Repository root
PATHS['dashboard']         # Dashboard directory
PATHS['docs']              # Documentation

# Key settings
SETTINGS['version']        # Current: v5.0.0
SETTINGS['health_target']  # Target: 98
SETTINGS['colors']         # Visualization colors

# Validate before changes
from config import validate_paths
success, missing = validate_paths()
```

**ALWAYS** import from `config.py` — never hardcode paths.

---

## Port Assignments

| Application | Port | Type | Embeddable |
|-------------|------|------|------------|
| CFA Main App | 8503 | Streamlit | N/A |
| Health Dashboard | 8504 | Streamlit | Yes (iframe) |
| SMV Trinity | 3001 | React/Vite | No |

---

## Common Tasks

### Task 1: Update Matrix Portal Content

1. Read `pages/matrix.py`
2. Find the section to update (Pan Handler Central, External Repos, etc.)
3. Maintain Matrix theme colors
4. Test locally: `streamlit run app.py`

### Task 2: Update Health Dashboard Data

1. Read `dashboard/HealthDashboard/app.py`
2. Data currently hardcoded — update metrics directly
3. Future: Will pull from `dashboard/config.py`
4. Test: `cd dashboard && launch_health.bat`

### Task 3: Add New Connected Repository

In `pages/matrix.py`, add to External Repositories section:

```python
st.markdown("""
<div class="portal-card">
    <h3>🌐 New Repo Name <span class="status-badge badge-active">ACTIVE</span></h3>
    <p><strong>Purpose:</strong> Description here</p>
    <p><strong>Status:</strong> Current status</p>
</div>
""", unsafe_allow_html=True)
```

### Task 4: Create Pan Handlers Manifest

Create `panhandlers_manifest.json` in repo root:

```json
{
  "repo_name": "CFA",
  "repo_id": "cfa-framework",
  "role": "Epistemic Engineering Framework",
  "tagline": "All Named, All Priced",
  "status": "Active",
  "track": "Core Framework",

  "dashboard": {
    "port": 8503,
    "health_port": 8504,
    "smv_port": 3001
  },

  "matrix_portal": {
    "enabled": true,
    "theme": "green-terminal",
    "location": "pages/matrix.py"
  }
}
```

---

## Pan Handlers Network

CFA is part of the **Pan Handlers Network** — human-AI collaboration projects.

### Philosophy

> "These are the things we built together that neither could have done alone."
> "FUCK IT, WE'LL DO IT LIVE!"

### Connected Repositories

| Repository | Role | Dashboard Port |
|------------|------|----------------|
| CFA | Epistemic Engineering | 8503/8504/3001 |
| Nyquist Consciousness | Core research | 8503 |
| VUDU Fidelity | Human validation | 8504 (planned) |

### Integration Pattern

Each repo has:

- A `panhandlers_manifest.json` at root
- A Matrix page with green terminal aesthetic
- Bidirectional links to other repos
- Dashboard on assigned port

---

## CSS Reference — Matrix Theme

```css
/* BLACK BACKGROUND */
.stApp { background-color: #0a0a0a !important; }

/* GREEN TEXT */
.stApp p, .stApp span, .stApp h1, .stApp h2, .stApp h3 {
    color: #00ff41 !important;
}

/* BUTTONS - Default */
.stButton > button {
    background-color: #0d0d0d !important;
    color: #00ff41 !important;
    border: 2px solid #00ff41 !important;
}

/* BUTTONS - Hover (WHITE text for readability) */
.stButton > button:hover {
    background-color: #004d1a !important;
    color: #ffffff !important;
}

/* PORTAL CARDS */
.portal-card {
    background: linear-gradient(135deg, rgba(0,255,65,0.1) 0%, rgba(0,204,51,0.05) 100%);
    border: 2px solid #00ff41;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0,255,65,0.3);
}

/* STATUS BADGES */
.badge-active { background: rgba(0,255,65,0.2); color: #00ff41; border: 1px solid #00ff41; }
.badge-coming-soon { background: rgba(255,215,0,0.2); color: #ffd700; border: 1px solid #ffd700; }
```

---

## Testing Checklist

Before committing changes:

- [ ] Run `streamlit run app.py` — main app works
- [ ] Navigate to The Matrix page — theme renders correctly
- [ ] Click Health Dashboard button — iframe loads (if running)
- [ ] Click SMV Trinity button — instructions display correctly
- [ ] Check sidebar navigation works
- [ ] Verify no broken imports

---

## Gospel Problem Prevention

**Never trust stale information.**

1. Always read the actual file before editing
2. Run `validate_paths()` from config.py
3. Check that ports aren't already in use
4. Update README.md when structure changes
5. Test locally before committing

---

## Quick Commands

```bash
# Launch dashboards
cd dashboard && launch_health.bat    # Health Dashboard
cd dashboard && launch_smv.bat       # SMV Trinity
cd dashboard && launch_both.bat      # Both

# Test main app
streamlit run app.py                 # Main CFA app

# Validate config
python dashboard/config.py           # Check all paths
```

---

## Files to Read Next

1. `dashboard/README.md` — Full documentation
2. `pages/matrix.py` — The Matrix portal code
3. `dashboard/config.py` — Configuration reference
4. `dashboard/HealthDashboard/app.py` — Health dashboard code
5. `dashboard/HealthDashboard/README.md` — Health dashboard docs

---

## Contact

**Human:** Ziggy
**Main Claude:** CFA Claude (Opus)
**You:** Dashboard Claude (Cold Boot)

When in doubt, ask the human. Better to clarify than to break things.

---

**Welcome to the Matrix.** 🟢⬛

*"Dashboards run, docs inform. Keep them separate, keep them clear."*

**This is the way.**
