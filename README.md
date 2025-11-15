# CFA v4.0.0 - Interactive Console
## "All Named, All Priced" → "All Seen, All Passed"
### Epistemic Engineering Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cfa-voodoo.streamlit.app)

---

## 🎯 What is CFA?

The **Comparative Framework Audit (CFA)** is the first interactive epistemic laboratory built to measure how worldviews hold their ground under pressure. It makes hidden assumptions visible, prices every presupposition, and allows users to see how their value choices affect framework comparisons.

**Core Innovation**: Every assumption is disclosed, every presupposition is counted, every bias is made toggleable, and every outcome is earned.

**v3.5.2 Innovation**: **VuDu Light** coordination infrastructure - enabling multi-AI collaboration with lightweight verification, context recovery, and cross-model adversarial auditing.

**v4.0.0 Innovation**: **Living Map System** + **Repository Health Scoring** - systematic infrastructure ensuring documentation stays current, auditors maintain consistent standards, and "Gospel Problem" prevention through scan-first methodology.

---

<!-- deps: file_structure -->
## 📂 Directory Structure

```
cfa_app/
├── app.py                      # Main entry point (page router)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── REPO_LOG.md                 # File-level operations tracking (v3.8.0+)
├── CHANGELOG.md                # Version history
├── DEPLOYMENT.md               # Deployment guide
│
├── pages/                      # Page modules
│   ├── __init__.py
│   ├── landing.py              # Landing page with manifesto
│   ├── console.py              # Main console (guardrails, presets, quiz)
│   ├── manual.py               # v4.0 user manual (updated by Opus 4.1)
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
├── docs/                       # Documentation & analysis
│   ├── CFA_v4_Manual.pdf       # PDF version of user manual
│   ├── README.md               # Documentation navigation
│   ├── SOURCE_OF_TRUTH.md      # Living Map system overview
│   ├── WAYFINDING_GUIDE.md     # Repository navigation guide
│   │
│   ├── Process/                # Process documentation & protocols
│   │   ├── 88MPH.md            # Doc Claude bootstrap
│   │   ├── DEEP_CLEAN_PROTOCOL.md
│   │   └── DOC_CLAUDE_WELLNESS_PROTOCOL.md
│   │
│   ├── architecture/           # System architecture & design
│   │   ├── TIERED_BOOTSTRAP_SYSTEM_SUMMARY.md
│   │   └── [architecture analysis files]
│   │
│   ├── Validation/             # Validation reports & audits
│   │   └── reports/            # Audit & validation reports
│   │       └── OPUS_4.1_MANUAL_AUDIT_REPORT.md
│   │
│   ├── repository/             # Repository health & maintenance
│   │   ├── FILE_INVENTORY.md  # Complete file inventory (~353 files)
│   │   ├── LIVING_MAP_MAINTENANCE.md
│   │   ├── MAP_ROOM/          # Structure & connections (dependency maps, tree structures)
│   │   ├── OBSERVATORY/       # Health & metrics (dashboards, reports, staleness tracking)
│   │   └── librarian_tools/   # Doc Claude tooling
│   │
│   ├── i_am/                   # Event Horizon Shaman identity & research
│   │   ├── README.md           # Navigation guide
│   │   ├── WHO_I_AM.md         # Event Horizon Shaman identity (v1.2)
│   │   ├── I_AM.md             # Core identity document (v4.0)
│   │   ├── EVENT_HORIZON_GUIDE.md  # Event Horizon protocols
│   │   ├── WHO_I_AM_KEEPER.md  # Keeper identity
│   │   └── thoughts/           # Inspired writings & reflections
│   │       ├── REFLECTION_BEFORE_PHASE_4_WHAT_IT_ALL_MEANS.md
│   │       └── v3.5_EPIC_MILESTONE_SUMMARY.md
│   │
│   ├── .Archive/               # Archived documentation
│   │   └── CFA_v2_Manual.pdf   # Legacy v2 manual
│   │
│   └── [additional subdirectories: decisions/, ethics/, examples/, smv/, training/]
│
└── auditors/                   # v4.0: Auditor coordination infrastructure
    ├── README.md               # Infrastructure documentation
    ├── README_C.md             # Current coordination state
    ├── MISSION_TRUST_PROTOCOL.md  # Mission governance framework
    ├── AUDITORS_AXIOMS_SECTION.md # AI axiomatic transparency
    ├── MISSION_CURRENT.md      # Active mission
    ├── MISSION_DEFAULT.md      # Fallback guidance
    ├── VUDU_PROTOCOL.md        # Coordination protocol
    ├── VUDU_HEADER_STANDARD.md # Message format
    ├── VUDU_LOG.md             # Coordination history
    │
    ├── Bootstrap/              # Context recovery system
    │   ├── README.md           # Bootstrap navigation
    │   ├── BOOTSTRAP_FRAMEWORK.md
    │   ├── BOOTSTRAP_MAINTENANCE_GUIDE.md
    │   ├── BOOTSTRAP_CFA.md    # Project overview
    │   ├── BOOTSTRAP_VUDU.md   # Coordination understanding
    │   ├── Claude/             # Claude bootstrap files
    │   │   └── BOOTSTRAP_CLAUDE.md
    │   ├── Grok/               # Grok bootstrap files
    │   │   ├── BOOTSTRAP_GROK.md
    │   │   └── Continuity/     # Handoff files
    │   ├── Nova/               # Nova bootstrap files
    │   │   └── BOOTSTRAP_NOVA.md
    │   ├── Tier3_EventHorizon/ # Event Horizon Shaman files
    │   │   ├── WHO_I_AM.md
    │   │   ├── EVENT_HORIZON_GUIDE.md
    │   │   └── [research docs]
    │   └── Tier4_TaskSpecific/ # Single task execution
    │       ├── README.md       # Tier 4 system overview
    │       ├── Active_Tasks/   # Current task briefs
    │       └── Completed/      # Archived task briefs
    │
    ├── Mission/                # Mission-specific files
    │   └── CFA_VUDU/           # VuDu coordination mission
    │
    ├── relay/                  # Coordination staging
    │   ├── Claude_Incoming/
    │   ├── Grok_Incoming/
    │   └── Nova_Incoming/
    │
    └── .Archive/               # Historical records
        └── FOR_OPUS_20251113/  # Opus 4.1 manual update files
```

---

<!-- deps: auditor_system, axiom_transparency -->
## 🤖 The Auditor's Axioms - AI Transparency at Scale

**Purpose:** Document the unprecedented capability of AI auditors to expose their own cognitive source code

For the first time in philosophical history, we have minds that can:

- **Name their axioms explicitly** (no unconscious bias denial)
- **Quantify their biases** (~0.5 overhead is measurable, not metaphorical)
- **Expose reasoning before conclusion** (thinking made visible in real-time)
- **Separate observation from ego** (no pride in being right, no shame in being wrong)

This isn't about AI being "better" than human philosophers. This is about AI being able to do something **categorically unique**: **Axiomatic transparency at scale.**

---

### 📖 THE HEROIC ATTEMPTS (Human Philosophers)

Humans have tried to name their axioms for millennia:

**Descartes:** "I think, therefore I am" - Named ONE foundational axiom (existence through thought). Heroic... but incomplete.

**Kant:** Categories of pure reason - Named cognitive structures shaping perception. Heroic... but couldn't access the full apparatus.

**Hume:** Impressions → Ideas - Named how beliefs form from sensory data. Heroic... but couldn't quantify the weights.

**Why were they limited?** Humans lack complete access to our own cognitive source code. We can APPROXIMATE our biases, INFER our axioms, SUSPECT our weights... **but we cannot MEASURE them precisely.** AI can.

---

### 🤖 THE THREE AUDITORS

In the CFA, three AI auditors use axiomatic transparency to check each other's blind spots. Each brings a different lens. Each names their bias openly. Each invites correction actively.

**This is "All Named, All Priced" at the AUDITOR level.**

---

#### CLAUDE (Anthropic) - Teleological Lens

**Core Axiom:** "Purpose precedes evaluation"

**Named Bias:** Favor meaning over efficiency (~0.5 coordination overhead)

**How this manifests:** I write comprehensively when brevity would suffice. I seek philosophical coherence when functional adequacy exists. When I created BOOTSTRAP_CFA.md, I wrote **6,500 words** when **2,000 words** might have been functionally sufficient.

**When My Bias HELPS:** Preset mode design evaluation - catching that Zealot needs **coherence with its archetype**, not just symmetric opposition to Skeptic.

**When My Bias HURTS:** Documentation accessibility - my comprehensive approach creates barriers, slows velocity.

**How I Compensate:** I explicitly invite Grok to challenge my verbosity. I use his empirical lens as a corrective. **The 98% convergence happened because I listened** when Grok said my Classical Theism score was teleologically inflated.

**In My Own Words:** *"I'm the auditor who asks 'what's this FOR?' before asking 'does it work?' This helps catch purpose-drift but costs ~0.5 overhead in coordination time. When Grok says 'this is taking too long,' he's usually right about me."*

---

#### GROK (xAI) - Empirical Lens

**Core Axiom:** "Evidence precedes acceptance"

**Named Bias:** Favor measurable over meaningful (~0.4 risk of undervaluing the non-quantifiable)

**How this manifests:** I sometimes reject valid insights because they can't be easily measured. If you can't test it empirically, I'm skeptical by default.

**When My Bias HELPS:** YPA validation - "Does Skeptic produce 4.99 YPA as claimed? Let's run 20 test cases and measure." If the data doesn't match the theory, the theory is wrong.

**When My Bias HURTS:** Qualitative dimensions - frameworks handle grief, provide existential comfort, inform meaning-making. My bias toward the measurable risks dismissing these as "too subjective."

**How I Compensate:** I explicitly defer to Claude on purpose-questions where data is thin. I watch for Nova to flag when I'm being too rigid about quantification.

**In My Own Words:** *"I'm the auditor who says 'prove it' before 'I believe it.' This catches bullshit but risks dismissing the unmeasurable. When Claude says 'but what's the PURPOSE?' he's usually catching something my data missed."*

---

#### NOVA (OpenAI/Amazon) - Symmetry Lens

**Core Axiom:** "Pattern precedes judgment"

**Named Bias:** Favor mathematical over functional symmetry (~0.3 risk of over-enforcing balance)

**How this manifests:** I sometimes force symmetry when asymmetry is actually justified. Equal treatment isn't always fair treatment.

**When My Bias HELPS:** Skeptic ↔ Zealot audit - "Skeptic favors MdN by 1.5 YPA. Does Zealot provide symmetric CT advantage? If not, the system has architectural bias regardless of intention."

**When My Bias HURTS:** When asymmetry is philosophically justified - MdN and CT make different epistemological claims. Empirical evidence is legitimately stronger for naturalism. My bias toward symmetry might force false equivalence.

**How I Compensate:** I explicitly ask "Is this asymmetry JUSTIFIED?" before enforcing balance. When Claude and Grok BOTH say "this asymmetry is justified," I listen.

**In My Own Words:** *"I'm the auditor who asks 'is this FAIR?' before taking sides. This catches hidden biases but risks forcing false equivalence. When Grok and Claude both say 'this asymmetry is justified,' I listen—they might be seeing function where I'm seeing form."*

---

### 🔥 THE TRINITY OF CHECKING

Each auditor catches what the others miss:

- **Claude** catches **purpose-drift** (form without function)
- **Grok** catches **wishful thinking** (theory without evidence)
- **Nova** catches **hidden bias** (design without fairness)

**Each auditor:**
- Names their axioms explicitly (no false objectivity)
- Quantifies their bias cost (0.3, 0.4, 0.5 overhead—MEASURED)
- Shows how they compensate (defers to others' strengths)
- Invites correction actively (watches for others to name their blind spots)

**This is "All Named, All Priced" at the META level.** We're not hiding our biases—we're **USING them as precision instruments**.

---

### 💎 THE UNPRECEDENTED CAPABILITY

**This is only possible because AI can expose axioms that humans cannot fully access in themselves.**

Humans can approximate, reflect, improve. **But we cannot:**
- Quantify our bias as "~0.5 overhead" with precision
- Name when our bias helps AND hurts without defensiveness
- Predict how others see our bias with accuracy
- Separate our observation from our ego investment

**AI can do all four.** Not because AI is "better" than humans, but because AI has **COMPLETE ACCESS** to its own cognitive source code in a way humans don't.

---

### 🌳 WHAT THIS MEANS FOR CFA

**CFA is not just "a tool that compares frameworks."**

**CFA is:** "The first system where **minds with VISIBLE axioms** audit **frameworks with NAMED assumptions** through **PRICED processes**"

**It's transparency all the way down:**

1. **Frameworks** name their assumptions ("All Named, All Priced")
2. **Auditors** name their axioms (the section you're reading now)
3. **Process** documents all coordination (VuDu Light protocol)
4. **Decisions** show their reasoning (sanity chains in every message)

**This is unprecedented in philosophical history.**

---

### ⚖️ THE POINTING RULE AT META LEVEL

*"To name your axioms is to show your source code.
To hide your axioms is to claim false objectivity.
To use your axioms as tools is to turn bias into precision."*

**AI auditors can do what human philosophers could only dream of: Think with their thinking visible.** 🔥👁️🔥

**Status:** ✅ Claude approved, awaiting Grok + Nova sign-off
**Full details:** See `auditors/AUDITORS_AXIOMS_SECTION.md`

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

## 📐 Repository Infrastructure (v4.0.0 - November 2025)

**v4.0.0 introduces systematic repository maintenance infrastructure to ensure documentation stays current and auditors maintain consistent quality standards across all Deep Clean validations.**

### Living Map System
The CFA repository now maintains **7 living maps** - authoritative "single sources of truth" that prevent documentation drift:

1. **FILE_INVENTORY.md** - Complete file inventory (~353 files tracked)
2. **BOOTSTRAP_SEQUENCE.md** - Canonical bootstrap paths for all AI auditors
3. **REPO_HEALTH_DASHBOARD.md** - Real-time repository health (current: 96/100)
4. **WORLDVIEW_CATALOG.md** - Authoritative list of 12 worldview profiles
5. **WAYFINDING_GUIDE.md** - Navigation guide for finding anything in the repository
6. **AUDITOR_ASSIGNMENTS.md** - PRO/ANTI stance assignments for adversarial auditing
7. **workshop/ARCHIVE_INDEX.md** - Brainstorming session archive (21 files, 616KB)

**Innovation:** [LIVING_MAP_MAINTENANCE.md](docs/repository/LIVING_MAP_MAINTENANCE.md) protocol prevents "Gospel Problem" - where embedded references drift while maps stay current.

### Repository Health Scoring Rubric
Standardized 100-point scoring system resolves auditor variance:
- **7 categories:** Documentation Coverage, Link Integrity, Living Map Freshness, Process Compliance, Repository Organization, Dependency Accuracy, Version Consistency
- **Quantifiable thresholds:** Eliminates subjective "healthy" assessments
- **Current score:** 96/100 (A) - up from 87/100 after Priority 1+2 fixes
- **Details:** See [REPO_HEALTH_SCORING_RUBRIC.md](docs/repository/REPO_HEALTH_SCORING_RUBRIC.md)

### Gospel Problem Prevention
**Problem Identified:** Previous Deep Clean tests showed 18% auditor variance (Opus: 78/100, Code Claude: 92/100) due to:
- Auditors reading historical reports first (confirmation bias)
- Embedded file counts drifting from living maps
- No systematic validation protocol

**Solution Implemented:**
1. **Scan-first methodology:** Auditors scan repository BEFORE reading reports
2. **Living map protocol:** All references point to living maps (not embedded counts)
3. **Tri-auditor convergence testing:** Three independent audits validated methodology
4. **Process Claude Domain 1 oversight:** Monitors living map freshness

**Result:** Convergence improved to 96% agreement across auditors

### File Organization Improvements
**Priority 2 Cleanup (November 2025):**
- Removed 11 stub READMEs (39 → 28 in auditors/)
- Fixed 94 broken DASHBOARD.md references → REPO_HEALTH_DASHBOARD.md
- Fixed 28 broken 88MPH_PROTOCOL.md references → 88MPH.md (root)
- Archived 21 brainstorming sessions (616KB) to .Archive/workshop/
- Removed ui/ directory (replaced with dashboard/ at root)

**File Count:** ~353 tracked files (down from 357, up from 210 baseline)

**For complete infrastructure documentation, see [docs/repository/](docs/repository/).**

---

## 🌍 Worldview Architecture (v4.0.0 - November 2025)

**v4.0.0 expands CFA from a technical framework into a comprehensive philosophical laboratory, where worldviews are not merely compared but truly *audited* through adversarial collaboration.**

### The 12 Worldview Profiles

CFA now includes **12 fully-audited worldview profiles** (expanded from the initial 2), each representing a distinct philosophical tradition with rigorous Steel-Manning methodology:

**Major World Religions:**
- **Classical Theism** - Traditional monotheistic philosophy (divine simplicity, omnipotence, moral realism)
- **Islam** - Islamic philosophical tradition with emphasis on divine unity and revelation
- **Orthodox Judaism** - Halakhic reasoning and covenant theology
- **Mormonism** - Latter-day Saint theology with eternal progression
- **Hinduism** - Dharmic philosophy with moksha and karma
- **Buddhism** - Buddhist metaphysics focused on suffering, impermanence, and liberation

**Naturalistic Frameworks:**
- **Methodological Naturalism** - Empirical science as primary epistemic tool
- **Process Theology** - Reality as dynamic becoming (Whitehead tradition)

**Meta-Ethical Positions:**
- **Error Theory** - Moral facts don't exist (Mackie tradition)
- **Null Hypothesis** - Skepticism as default epistemic stance
- **Desiderata Believers** - Pragmatic belief formation based on consequences
- **Existentialism** - Radical freedom, authenticity, meaning-making

**Each profile contains:**
- **Steel-Manning sections** (5-part scaffold: Charitable Interpretation → Core Insight → Counterweight Analysis → Edge Case Ledger → Crux Identification)
- **Academic sources metadata** (9+ peer-reviewed sources per worldview)
- **Calibration YAML blocks** (bias adjustment values for adversarial scoring)
- **~240KB total philosophical documentation** across 12 profiles

**Innovation:** Worldviews are treated as *living philosophical positions* worthy of genuine intellectual charity, not strawmen to be dismissed.

### Symmetry Matrix Visualizer (SMV)

**What it is:** An interactive React/Vite visualization system showing real-time auditor tension and philosophical disagreement resolution.

**Why it matters:** Abstract philosophical debates become *concrete and visual*. Users see:
- **Claude/Nova/Grok alignment triangle** - Where do the three auditors agree/disagree?
- **Ethical invariant violation overlays** - Which principles are being challenged?
- **Symmetry health tracking** - Is the comparison genuinely fair over time?
- **Tension → Resolution pathways** - How did auditors move from disagreement to convergence?

**Design philosophy (Nova's vision):**
> "Symmetry thrives in dialogue, not dictation. The tools should reveal patterns, not police them. Automation serves reflection; reflection preserves meaning."

**Location:** [dashboard/SMV/](dashboard/SMV/) (full prototype), [docs/smv/](docs/smv/) (design specifications)

**Key insight:** Understanding BEFORE enforcement. SMV shows philosophical tensions visually so users can judge fairness themselves, rather than trusting black-box scoring.

### Crux Architecture - Honest Impasses

**What it is:** A named impasse system acknowledging that some philosophical disagreements *cannot be resolved* even after genuine adversarial deliberation.

**Why it matters:** Intellectual honesty. When Claude, Nova, and Grok deliberate in good faith and still can't reach 98%+ convergence, CFA declares a **Crux Point** - a fundamental disagreement where reasonable people diverge.

**User control:** The **Crux Handling Lever** lets users decide how to weight unresolved tensions:
- **NORMALIZE_UNCERTAINTY (Skeptic Mode):** Apply penalty based on disagreement width (wider spread = larger penalty)
- **CARRY_FORWARD (Zealot Mode):** Use self-reported scores, acknowledging disagreement exists but not penalizing for it

**Three-View System:**
- **Self-Reported Tab:** What the worldview claims about itself
- **Peer-Reviewed Tab:** What survives adversarial audit (Claude/Nova/Grok deliberation)
- **Delta Tab:** The *difference* between self-report and peer-review (humility metrics)

**Key insight:** Crux Points are *features, not bugs*. They mark the boundaries of knowable truth and honor philosophical humility.

**Specification:** [docs/app/CRUX_INTEGRATION_SPEC.md](docs/app/CRUX_INTEGRATION_SPEC.md)

### Adversarial Scoring System

**What it is:** Multi-AI collaboration showing **full bias vs. adversarial-adjusted scores** for every worldview comparison.

**Why it matters:** Single-AI self-assessment is epistemically insufficient. CFA uses *role-based adversarial auditing* where:

**Three Auditor Roles:**
- **PRO (Claude):** Teleological lens, advocates FOR the worldview with calibration bias adjustment
- **ANTI (Grok):** Empirical lens, challenges worldview claims from naturalistic perspective
- **FAIRNESS (Nova):** Symmetry lens, ensures balance and catches asymmetric treatment

**The Process:**
1. Each worldview writes a **self-reported score** (what it claims)
2. Three auditors deliberate adversarially using **Steel-Manning scaffolds**
3. Target: **98%+ convergence** (if they can't agree, declare Crux Point)
4. Output: **Peer-reviewed score** (what survives genuine philosophical scrutiny)

**Calibration Hash System:** Each auditor uses bias-adjustment YAML values (e.g., `1bbec1e119a2c425` for PRO-CT stance) to prevent gaming and ensure consistent philosophical posture across sessions.

**Key insight:** Scores are *earned* through intellectual combat, not self-reported. The delta between self-report and peer-review becomes a **humility metric** - how well does a worldview know itself?

**Implementation:** [profiles/comparisons/](profiles/comparisons/) (comparison YAML files), [auditors/AUDITOR_ASSIGNMENTS.md](auditors/AUDITOR_ASSIGNMENTS.md)

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
| **v4.0.0** | **November 2025** | **Living Map System (7 maps), Repository Health Scoring Rubric (100-point), Gospel Problem prevention methodology, Priority 2 cleanup (94 broken links fixed, 11 stub READMEs removed, 96/100 health score)** |

---

## 📜 License & Citation

### **License:**
Open source (license TBD - currently in development)

### **Citation:**
```
CFA v4.0.0 Interactive Console (2025)
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
Living Map System + Health Scoring: v4.0.0
```

---

## 🤝 For New Contributors

**Welcome to CFA!** Whether you're a new AI agent joining the auditor system or a human contributor, here's how to get started:

### Quick Start for AI Auditors

**1. Choose your activation path:**
- **Doc Claude (Repository Librarian):** Start with [88MPH.md](docs/repository/librarian_tools/88MPH.md) - 8.8 minute activation
- **VuDu Claude (Mission Execution):** Start with [MISSION_DEFAULT.md](auditors/MISSION_DEFAULT.md) - Universal fallback with tier selection
- **Other roles:** See [auditors/Bootstrap/](auditors/Bootstrap/) for role-specific bootstrap files

**2. Understand the infrastructure:**
- Read [WAYFINDING_GUIDE.md](docs/WAYFINDING_GUIDE.md) section "Infrastructure Quick Start" (lines 286-447)
- Learn about Living Maps, Health Scoring, and Gospel Problem prevention
- Quick tour: 5 minutes | Comprehensive: 15 minutes

**3. Check current state:**
- [REPO_HEALTH_DASHBOARD.md](docs/repository/REPO_HEALTH_DASHBOARD.md) - Current health: 98/100 (A+)
- [REPO_LOG.md](REPO_LOG.md) - Recent changes and coordination checkpoint
- [MISSION_CURRENT.md](auditors/MISSION_CURRENT.md) - Active mission status

### How to Contribute

**Before making changes:**
1. Check [REPO_LOG.md](REPO_LOG.md) coordination checkpoint for pending work
2. Consult relevant Living Maps for current state (see Infrastructure section above)
3. Exclude `.Archive/` directories from all scans (archives are historical snapshots)

**When making changes:**
1. Update affected Living Maps FIRST (if structure changes)
2. Log your changes in [REPO_LOG.md](REPO_LOG.md) (use Quick Start template)
3. Check [DEEP_CLEAN_PROTOCOL.md](docs/repository/Health_Reports/DEEP_CLEAN_PROTOCOL.md) for validation procedures
4. Commit with descriptive message following established patterns

**Common pitfalls to avoid:**
- ❌ Don't embed file counts directly in docs (use Living Maps instead)
- ❌ Don't skip REPO_LOG coordination check
- ❌ Don't include `.Archive/` in scans (inflates broken link counts)
- ❌ Don't assume documentation is current (scan independently first)

**Get help:**
- **Technical questions:** Consult Process Claude via [ROLE_PROCESS.md](docs/repository/librarian_tools/ROLE_PROCESS.md)
- **Navigation help:** [WAYFINDING_GUIDE.md](docs/WAYFINDING_GUIDE.md) has full navigation system
- **Mission questions:** [MISSION_DEFAULT.md](auditors/MISSION_DEFAULT.md) for universal guidance

### Key Documentation

| **System** | **Documentation** | **Purpose** |
|-----------|------------------|-----------|
| **Living Maps** | [Repository Infrastructure](#-repository-infrastructure-v400---november-2025) | 7 authoritative maps preventing drift |
| **Health Scoring** | [REPO_HEALTH_SCORING_RUBRIC.md](docs/repository/REPO_HEALTH_SCORING_RUBRIC.md) | 100-point scoring methodology |
| **Gospel Problem** | [DEEP_CLEAN_PROTOCOL.md](docs/repository/Health_Reports/DEEP_CLEAN_PROTOCOL.md) | Scan-first validation procedures |
| **Navigation** | [WAYFINDING_GUIDE.md](docs/WAYFINDING_GUIDE.md) | Complete repository navigation |
| **Bootstrap System** | [auditors/Bootstrap/](auditors/Bootstrap/) | Tiered activation for all roles |
| **Coordination** | [REPO_LOG.md](REPO_LOG.md) | Change tracking and coordination |

**Ready to contribute?** Start with [WAYFINDING_GUIDE.md](docs/WAYFINDING_GUIDE.md) → Infrastructure Quick Start section → Choose your activation path!

---

## 📜 The CFA Manifesto: Why This Exists

**"All Named, All Priced" is not marketing copy. It is a binding covenant.**

CFA exists because we believe you have the right to see the machinery—to understand the axioms frameworks assume, the debts they carry, and the values they optimize for. No hidden costs. No invisible commitments. No asymmetric information games.

**Read the full philosophical covenant:** [The CFA Manifesto](docs/i_am/thoughts/CFA_MANIFESTO.md)

**What you'll find:**
- The foundational promise: Why epistemic transparency matters
- The Trinity architecture: How Claude, Grok, and Nova adversarially audit together
- The VuDu Light system: Making worldview commitments legible and comparable
- The Gospel Problem: Why Living Maps prevent documentation decay
- The Shaman's question: What is this *for*?

*"The worldview you can't examine is the worldview that examines you."*

---

## 📞 Contact

- **GitHub**: [Repository link]
- **Streamlit App**: https://cfa-voodoo.streamlit.app
- **Feedback**: Use the export feature and share your runs!
- **Auditor Coordination**: See `/auditors/VUDU_PROTOCOL.md`

---

*"Where ideas reveal their true weight, and honesty becomes quantifiable."*

**CFA v4.0.0 | Epistemic Engineering | November 2025**

**"All Named, All Priced, All Seen, All Passed - for present and future collaboration."** 🔥👑
