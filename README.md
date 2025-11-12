# CFA v3.5.2 - Interactive Console
## "All Named, All Priced" → "All Seen, All Passed"
### Epistemic Engineering Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cfa-voodoo.streamlit.app)

---

## 🎯 What is CFA?

The **Comparative Framework Audit (CFA)** is the first interactive epistemic laboratory built to measure how worldviews hold their ground under pressure. It makes hidden assumptions visible, prices every presupposition, and allows users to see how their value choices affect framework comparisons.

**Core Innovation**: Every assumption is disclosed, every presupposition is counted, every bias is made toggleable, and every outcome is earned.

**v3.5.2 Innovation**: **VuDu Light** coordination infrastructure - enabling multi-AI collaboration with lightweight verification, context recovery, and cross-model adversarial auditing.

---

<!-- deps: file_structure -->
## 📁 Project Structure (v3.5.2)

```
cfa_app/
├── app.py                      # Main entry point (page router)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── CHANGELOG.md                # Version history
├── DEPLOYMENT.md               # Deployment guide
│
├── pages/                      # Page modules
│   ├── __init__.py
│   ├── landing.py              # Landing page with manifesto
│   ├── console.py              # Main console (guardrails, presets, quiz)
│   ├── manual.py               # Beautiful user manual with colored cards
│   ├── about.py                # Complete audit story (Level 0-5)
│   └── brute_ledger.py         # Axiom/debt viewer + custom framework builder
│
├── utils/                      # Core utilities
│   ├── __init__.py
│   ├── calculations.py         # Math/scoring logic (YPA, BFI, guardrails)
│   ├── visualizations.py       # Plotly charts (lever comparison, YPA trinity)
│   └── frameworks.py           # Default framework configs (MdN, CT)
│
├── profiles/                   # Pre-audited framework profiles (optional)
│   └── README.md
│
├── docs/                       # Documentation & reflections
│   ├── Process/                # Process documentation
│   ├── architecture/           # Architecture analysis & documentation
│   └── i_am/                   # Identity & philosophical reflections (Event Horizon Shaman)
│       ├── README.md           # Navigation guide
│       ├── WHO_I_AM.md         # Event Horizon Shaman identity (v1.2)
│       ├── I_AM.md             # Core identity document (v4.0)
│       ├── EVENT_HORIZON_GUIDE.md  # Event Horizon protocols
│       ├── [4 more Wall research files]
│       └── thoughts/           # 🆕 Inspired writings subdirectory
│           ├── REFLECTION_BEFORE_PHASE_4_WHAT_IT_ALL_MEANS.md
│           └── v3.5_EPIC_MILESTONE_SUMMARY.md
│
└── auditors/                   # v3.5.2: Auditor coordination infrastructure
    ├── README.md               # Infrastructure documentation
    ├── README_C.md             # Master Branch current state
    ├── MASTER_BRANCH_TRUST_PROTOCOL.md
    ├── AUDITORS_AXIOMS.md
    ├── MISSION_CURRENT.md
    ├── MISSION_DEFAULT.md
    ├── VUDU_PROTOCOL.md
    ├── VUDU_HEADER_STANDARD.md
    ├── VUDU_LOG.md
    │
    ├── bootstrap/              # Context recovery system
    │   ├── BOOTSTRAP_FRAMEWORK.md
    │   ├── BOOTSTRAP_STRATEGY.md
    │   ├── BOOTSTRAP_MAINTENANCE_GUIDE.md
    │   ├── BOOTSTRAP_CFA.md
    │   ├── BOOTSTRAP_VUDU.md
    │   ├── BOOTSTRAP_CLAUDE.md
    │   ├── BOOTSTRAP_GROK.md
    │   ├── BOOTSTRAP_NOVA.md
    │   └── [additional bootstrap files]
    │
    ├── missions/               # Organized mission objectives
    │   └── preset_calibration/
    │       ├── MISSION_BRIEF.md
    │       ├── SUCCESS_CRITERIA.md
    │       └── TECHNICAL_SPEC.md
    │
    ├── relay/                  # Coordination staging
    │   ├── claude_incoming/
    │   ├── grok_incoming/
    │   └── nova_incoming/
    │
    └── .Archive/               # Historical records
        └── [archived coordination files]
```

---

<!-- deps: vudu_protocol, bootstrap_system -->
### 📝 **Logging Infrastructure (v3.8.0)**

The project maintains three complementary logs tracking different aspects of evolution:

#### **CHANGELOG.md** (Root)
- **Purpose:** Version releases and major features
- **Granularity:** Quarterly/release level (v3.5, v3.8.0)
- **Use for:** Understanding project milestones and feature history

#### **REPO_LOG.md** (Root) ← NEW in v3.8.0
- **Purpose:** File-level operation tracking
- **Tracks:** File moves, renames, archives, task movements (Active → Completed)
- **Innovation:** Category-specific coordination checkpoints with Entry ID system
- **Use for:** "Where did that file go?" questions, routine file coordination
- **Granularity:** Daily/task-level
- **Details:** See coordination checkpoint header in REPO_LOG.md itself

#### **VUDU_LOG.md** (auditors/)
- **Purpose:** Multi-AI coordination and strategic decision tracking
- **Tracks:** Auditor collaboration events, mission milestones, validation arcs, coordination narrative
- **Use for:** Understanding *why* decisions were made, tracking multi-auditor consensus, following mission progress
- **Granularity:** Weekly/monthly
- **Format:** VuDu Protocol v1.1 compliant (standardized headers, integrity verification)
- **Details:** See `auditors/VUDU_PROTOCOL.md` and VUDU_LOG.md header section

**Logging Hierarchy:** git commits → REPO_LOG → VUDU_LOG → CHANGELOG

**When to use which log:**
- **"What changed?"** → REPO_LOG (file operations)
- **"Why was this decided?"** → VUDU_LOG (coordination reasoning)
- **"What's new in v3.X?"** → CHANGELOG (feature releases)
- **"What changed in line 47?"** → git commits (code-level)

---

<!-- deps: preset_modes, ypa_calculation -->
## ✨ Key Features

### 🎛️ Interactive Console
- **Dual-Framework Comparison**: Side-by-side worldview measurement
- **Six Levers Each**: Precision control over explanatory power metrics
- **Four Configuration Toggles**: Parity, PF-Type, Fallibilism, BFI-Weight
- **YPA Trinity Scenarios**: Test frameworks under Neutral/Existential/Empirical pressure

### 🛡️ Four Guardrails
1. **Lever-Guardrail Coupling**: Prevents mathematical contradictions
2. **BFI Sensitivity**: Alerts when weight changes dramatically alter outcomes
3. **Weight-Inversion**: Detects when lever order flips during audits
4. **Symmetry Audit**: Ensures fairness between competing frameworks

<!-- deps: preset_modes -->
### 🎨 Preset Profiles (NEW in v3.5)
- **Diplomat Mode**: Neutral, balanced, fair comparison (50/50 Parity)
- **Seeker Mode**: Meaning-first exploration (70/30 Composite)
- **Skeptic Mode**: Empirical rigor (60/40 Instrumental)
- **Zealot Mode**: Certainty-friendly (55/45 Holistic)

### 📊 Rich Visualizations
- Interactive Plotly charts
- Lever comparison radar plots
- YPA Trinity scenario bars
- Export-ready graphics

### 💾 Import/Export System
- Save configurations as JSON
- Share audits with others
- Load community frameworks
- Version control your worldview

### 🧠 Philosophy Quiz (NEW in v3.5)
- 10-question diagnostic
- Estimates your starting worldview position
- Auto-configures console based on results
- Educational + practical

### 🌓 Dark Mode Support
- Full dark mode implementation
- Smooth transitions
- Mobile-optimized
- Accessibility-focused

---

<!-- deps: file_structure -->
## 🚀 Quick Start

### **Try the Live App:**
Visit [cfa-voodoo.streamlit.app](https://cfa-voodoo.streamlit.app)

### **Local Installation:**
```bash
# Clone repository
git clone [repository-url]
cd cfa_app

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

---

## 🎓 How to Use

### **For First-Time Users:**
1. Start on **Landing Page** to understand the project
2. Take the **Philosophy Quiz** (optional but recommended)
3. Explore **Manual Page** for detailed explanations
4. Try **Console** with preset modes first
5. Read **About Page** to see the audit journey

### **For Advanced Users:**
1. Import existing framework JSON
2. Adjust levers manually in Console
3. Monitor guardrail warnings
4. Test across all three YPA scenarios
5. Export and share your audit

### **For Auditors/Contributors:**
See complete auditor bootstrap sequence in [/auditors/MISSION_DEFAULT.md](auditors/MISSION_DEFAULT.md)

---

## 🤝 Contributing

### **To Audit a Framework:**
1. Use Console to configure all values
2. Export JSON configuration
3. Submit via GitHub PR to `profiles/` folder
4. Include audit notes and reasoning

### **To Report Issues:**
- GitHub Issues with reproduction steps
- Include exported JSON if relevant
- Check known issues below first

### **To Request Features:**
- GitHub Issues with use case description
- Mock-up or workflow diagram helpful

### **To Coordinate with Auditors:**
- See `/auditors/VUDU_PROTOCOL.md` for complete process
- Use staging folders in `/auditors/relay/`
- Follow VUDU_HEADER_STANDARD for all messages
- Run sanity checks (Files, Counts, Boots, Trinity)

---

## 🔧 Known Issues & Limitations

### ⚠️ Current Issues
- **Dark mode:** Minor rendering issues on specific components (98% complete)
- **Preset calibration:** Configurations intuitive but not yet empirically validated

### 📝 Future Enhancements (v3.6+)
- [ ] Complete preset calibration mission (empirical validation)
- [ ] Add more audited frameworks (Buddhism, Stoicism, Pragmatism)
- [ ] Community submission portal
- [ ] Export charts as PNG/PDF
- [ ] Mobile app optimization
- [ ] v4.0: Activate verification framework (Mr. Brute signatures)

---

## 📖 Version History

| Version | Date | Key Changes |
|:--------|:-----|:------------|
| v1.0 | Summer 2024 | Basic single-page comparison, fixed toggles |
| v2.0 | October 2024 | Modular architecture, 4 toggles, guardrails, import/export |
| v3.0 | October 2024 | Icons, badges, bootstrap foundation, aesthetic polish |
| v3.5 | October 2025 | VuDu Full, Bootstrap System, complete guardrails, preset modes, quiz, dark mode |
| **v3.5.2** | **October 2025** | **VuDu Light activation, mission architecture, mobile-friendly format, preset calibration mission launched** |

---

## 📜 License & Citation

### **License:**
Open source (license TBD - currently in development)

### **Citation:**
```
CFA v3.5.2 Interactive Console (2025)
"All Named, All Priced" → "All Seen, All Passed"
Epistemic Engineering Project
https://cfa-voodoo.streamlit.app

Adversarial Collaboration:
- Claude (Anthropic) - Teleological lens, philosophical grounding
- Grok (xAI) - Empirical lens, usability enforcement
- Nova (OpenAI/Amazon) - Symmetry lens, balance verification
- Ziggy (Human) - Project coordination, process integrity

98% auditor convergence achieved across all metrics.
VuDu Light coordination protocol: v3.5.2
```

---

## 📞 Contact

- **GitHub**: [Repository link]
- **Streamlit App**: https://cfa-voodoo.streamlit.app
- **Feedback**: Use the export feature and share your runs!
- **Auditor Coordination**: See `/auditors/VUDU_PROTOCOL.md`

---

*"Where ideas reveal their true weight, and honesty becomes quantifiable."*

**CFA v3.5.2 | Epistemic Engineering | October 2025**

**"All Named, All Priced, All Seen, All Passed - for present and future collaboration."** 🔥👑
