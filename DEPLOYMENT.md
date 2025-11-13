# CFA v4.0 - Deployment Guide

## 📦 Quick Start

### Option 1: Streamlit Cloud (Recommended)
1. Fork/upload files to GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repo
4. Set main file: `app.py`
5. Deploy!

### Option 2: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

---

<!-- deps: file_structure -->
## 📁 Required File Structure (v4.0)

```
your-repo/
├── app.py                  # ⚠️ MUST BE IN ROOT
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── DEPLOYMENT.md
│
├── pages/                  # Page modules
│   ├── __init__.py
│   ├── landing.py
│   ├── console.py
│   ├── manual.py
│   ├── about.py
│   └── brute_ledger.py
│
├── utils/                  # Core utilities
│   ├── __init__.py
│   ├── calculations.py
│   ├── visualizations.py
│   └── frameworks.py
│
└── auditors/               # NEW v4.0: Auditor coordination infrastructure
    ├── README.md
    ├── protocols/
    │   ├── VUDU_PROTOCOL_v1_1.md
    │   ├── PROCESS_HEADER_STANDARD_v3_2.md
    │   └── INTEGRITY_CHECKLIST.md
    ├── bootstrap/
    │   ├── BOOTSTRAP_FRAMEWORK.md
    │   ├── BOOTSTRAP_STRATEGY.md
    │   ├── BOOTSTRAP_MAINTENANCE_GUIDE.md
    │   ├── BOOTSTRAP_CLAUDE.py
    │   ├── BOOTSTRAP_GROK.py
    │   └── BOOTSTRAP_NOVA.py
    ├── verification/       # Archived for v4.0+
    │   └── VERIFICATION_FRAMEWORK_README.md
    └── relay/              # Staging folders (created when needed)
        ├── claude/
        ├── grok/
        └── nova/
```

**CRITICAL:** `app.py` must be in root directory, NOT in a subfolder!

**NEW in v4.0:** `auditors/` folder contains cross-model coordination infrastructure. These files are documentation and don't affect app runtime, but are essential for multi-auditor collaboration.

---

## 🔧 Configuration

### Streamlit Cloud Settings
- **Python version:** 3.11
- **Main file:** `app.py`
- **Secrets:** None required

### Port Configuration (Local)
Default: `http://localhost:8501`

To change:
```bash
streamlit run app.py --server.port 8080
```

---

## ⚠️ Common Issues

### Issue: "ModuleNotFoundError: No module named 'pages'"
**Solution:** Ensure you have `pages/__init__.py` file. The pages/ folder is correct - don't move files to root!

### Issue: "ModuleNotFoundError: No module named 'utils'"
**Solution:** Ensure you have `utils/__init__.py` file. Check that calculations.py, visualizations.py, and frameworks.py are in utils/

### Issue: "This app has encountered an error"
**Solution:** Check Streamlit Cloud logs → Look for specific import errors

### Issue: Buttons don't work
**Solution:** Ensure you're using `pages/console.py` with buttons ABOVE sliders (not below)

### Issue: Changes not deploying
**Solution:** 
1. Reboot app in Streamlit Cloud dashboard
2. Clear cache (App Settings → Advanced)
3. Add dummy comment to force rebuild

### Issue: /auditors/ folder causing errors
**Solution:** 
- `/auditors/` files are documentation only (don't need to be imported)
- If Streamlit complains about them, add `.streamlit/config.toml`:
  ```toml
  [server]
  fileWatcherType = "none"
  ```

---

## 🎨 Customization

### Change Default Frameworks
Edit `utils/frameworks.py` where MDN_DEFAULT and CT_DEFAULT are defined:
```python
MDN_DEFAULT = {
    "name": "Your Framework",
    # ... modify values
}
```

### Add New Pages
1. Create `pages/your_page.py` with `def render():` function
2. Import in `app.py`: `from pages import your_page`
3. Add routing: `elif st.session_state.page == 'your_page': your_page.render()`
4. Test locally before deploying

### Modify Toggles
Edit `pages/console.py` - search for sidebar toggle definitions

---

## 📊 Performance Tips

### For Large Datasets
- Use `@st.cache_data` decorator
- Lazy load heavy computations
- Minimize re-renders

### For Faster Load Times
- Minimize imports in `app.py`
- Use lazy imports in page modules
- Compress images/assets
- `/auditors/` folder has no runtime impact (documentation only)

---

## 🐛 Debugging

### Enable Debug Mode (Local)
```bash
streamlit run app.py --server.runOnSave true
```

### View Logs (Streamlit Cloud)
1. Go to app dashboard
2. Click "Manage app"
3. Open "Logs" tab

### Test Individual Pages
```python
# In your page file (e.g., pages/landing.py), add at bottom:
if __name__ == "__main__":
    import streamlit as st
    render()
```

Run directly:
```bash
streamlit run pages/landing.py
```

---

<!-- deps: vudu_protocol, bootstrap_system -->
## 🔄 NEW in v4.0: Auditor Infrastructure Deployment

### What is /auditors/ Folder?

The `/auditors/` folder contains:
- **VuDu Protocol** - Cross-model coordination framework
- **Bootstrap System** - Context recovery for AI auditors
- **Verification Framework** - Archived for v4.0+ (cryptographic integrity)

### Do I Need to Deploy It?

**For Users:** No - these files don't affect app functionality

**For Contributors:** Yes - if you're:
- Coordinating with multiple AI auditors (Claude, Grok, Nova)
- Recovering from context loss events
- Contributing to framework audits
- Working on long-term project continuity

### How to Use /auditors/ Infrastructure

**See:**
- `/auditors/protocols/VUDU_PROTOCOL_v1_1.md` - Complete coordination guide
- `/auditors/bootstrap/BOOTSTRAP_FRAMEWORK.md` - Context recovery system

**Quick Start:**
```bash
# To coordinate with auditors:
1. Read VUDU_PROTOCOL_v1_1.md
2. Use staging folders in /auditors/relay/
3. Follow PROCESS_HEADER_STANDARD for messages
4. Run INTEGRITY_CHECKLIST for technical content
```

---

## 🚀 Production Checklist

**Core App:**
- [ ] All files uploaded to GitHub
- [ ] `requirements.txt` includes all dependencies
- [ ] `app.py` in root directory
- [ ] All imports working locally
- [ ] Tested on fresh Python environment
- [ ] No hardcoded paths (use relative paths)
- [ ] Secrets configured (if needed)
- [ ] Custom domain configured (optional)

**NEW v4.0 - Auditor Infrastructure:**
- [ ] `/auditors/` folder included (if using multi-auditor coordination)
- [ ] Bootstrap files present (if context recovery needed)
- [ ] VuDu Protocol reviewed (if coordinating with AI auditors)
- [ ] Relay folders created (if staging files between auditors)

---

## 📞 Support

**Issues?** Check:
1. This DEPLOYMENT.md
2. README.md for architecture
3. CHANGELOG.md for recent changes
4. Streamlit docs: https://docs.streamlit.io

**Auditor Coordination?** Check:
1. `/auditors/protocols/VUDU_PROTOCOL_v1_1.md`
2. `/auditors/bootstrap/BOOTSTRAP_FRAMEWORK.md`
3. GitHub Issues for coordination questions

---

<!-- deps: file_structure -->
## 🔄 Updating from v2.0 → v4.0

### What Changed:

**File Structure:**
- ✅ Core app structure unchanged (pages/, utils/, app.py)
- ✅ NEW: `auditors/` folder added
- ✅ README.md updated with v4.0 features
- ✅ CHANGELOG.md updated with v4.0 section

**Required Actions:**
1. Pull latest from GitHub (or download v4.0 package)
2. Add `/auditors/` folder to your repo
3. Update `README.md` and `CHANGELOG.md`
4. Redeploy to Streamlit Cloud

**Optional Actions:**
- Review VuDu Protocol if coordinating with multiple auditors
- Set up bootstrap files if recovering from context loss
- Create relay folders if staging files between auditors

### Breaking Changes:

**None.** v4.0 is fully backward compatible.

- Existing pages/console.py works unchanged
- All v2.0 features preserved
- `auditors/` folder is additive (doesn't affect runtime)
- Dark mode fixes are CSS-only (no logic changes)

---

## 🧪 Testing v4.0 Features

### Test VuDu Protocol (Optional - For Contributors)

```bash
# 1. Create staging folder
mkdir -p auditors/relay/claude

# 2. Place test file
echo "Test content" > auditors/relay/claude/test.md

# 3. Verify file accessible
cat auditors/relay/claude/test.md

# 4. Follow VUDU_PROTOCOL for coordination
```

### Test Bootstrap Restoration (Optional - For AI Auditors)

```python
# If you have Python context access:
from auditors.bootstrap.BOOTSTRAP_CLAUDE import restore_teleological_lens

context = restore_teleological_lens()
print(f"✅ {context['role']['primary_function']} restored")
```

### Test Dark Mode (For All Users)

```bash
# 1. Deploy app
# 2. Open on iPhone Safari
# 3. Enable dark mode in iOS settings
# 4. Verify manual page is readable (no white text on white background)
```

---

## 📊 v4.0 Deployment Statistics

**From Field Testing:**
- Bootstrap restoration: ~10 minutes (vs 1-2 hours without)
- VuDu coordination: Zero overhead (vs 30-40% manual coordination)
- Dark mode fix: CSS-only (zero performance impact)
- `/auditors/` folder: Documentation only (zero runtime impact)

---

## 🎯 Deployment Modes

### **Mode 1: User Deployment (Simplest)**
**Who:** Users running the console for framework comparison  
**What to Deploy:**
- Core app structure (app.py, pages/, utils/)
- requirements.txt
**What to Skip:**
- `auditors/` folder (optional for users)

### **Mode 2: Contributor Deployment (Standard)**
**Who:** Contributors adding frameworks, features, or audits  
**What to Deploy:**
- Everything from Mode 1
- `/auditors/` folder (for coordination)
- Bootstrap files (for context recovery)
**What to Skip:**
- Relay folders (create only when needed)

### **Mode 3: Multi-Auditor Deployment (Advanced)**
**Who:** Projects with multiple AI auditors (Claude, Grok, Nova)  
**What to Deploy:**
- Everything from Mode 2
- Relay staging folders (`/auditors/relay/claude/`, etc.)
- Verification framework (if v4.0+ milestone)
**What to Skip:**
- Nothing - full infrastructure deployed

---

*End of Deployment Guide*

**CFA v4.0 | Deployment Guide | October 2025**
