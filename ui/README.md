# UI - User Interface Components & Prototypes

**Current Status:** MIGRATED → See [/dashboard/](/dashboard/) instead

**Last Updated:** 2025-11-12

---

## 🚨 IMPORTANT NOTICE

**The SMV prototype has been migrated to `/dashboard/SMV/`**

**Previous location:** `ui/smv/prototype/` (now empty)
**New location:** [dashboard/SMV/](../dashboard/SMV/)

**Why the move?**
- Semantic clarity: `/dashboard/` for running applications, `/docs/` for documentation
- Better organization: Root-level dashboard directory scales better for multiple apps
- Naming consistency: Lowercase root folders (dashboard, auditors, docs, pages, profiles)

**What happened to ui/?**
- This directory is now a legacy folder
- May be repurposed in future for UI component libraries
- For now, kept to prevent broken references during transition

---

## 🔮 Future Purpose (TBD)

**Potential uses for ui/ directory:**

**Option 1: Component Library**
- Shared React components across multiple dashboard apps
- Reusable UI patterns (buttons, forms, layouts)
- Design system implementation

**Option 2: Remove Entirely**
- If no other UI prototypes planned
- Clean migration path: ui/ → dashboard/

**Option 3: Streamlit/Gradio Apps**
- Python-based dashboards
- Alternative to React for quick prototypes

**Decision pending:** User to determine future use case

---

## 📋 Current Structure

```
ui/
├── README.md          ← You are here
└── smv/               ← Legacy (empty after migration)
    └── prototype/     ← Migrated to /dashboard/SMV/
```

**Empty directories:**
- `ui/smv/prototype/` - All files moved to dashboard/SMV/

**May be safe to delete:**
- `ui/smv/` (entire tree)
- `ui/` (if no future plans)

---

## 🔗 Related Directories

**Current active locations:**
- [/dashboard/](/dashboard/) - Running applications & prototypes (SMV lives here now)
- [/docs/smv/](/docs/smv/) - SMV design specs, mockups, planning docs
- [/pages/](/pages/) - Streamlit app pages (separate from dashboard prototypes)

**Philosophy:**
- `/dashboard/` → Interactive React/JS applications
- `/pages/` → Streamlit Python pages
- `/ui/` → TBD (legacy or future component library)
- `/docs/` → Documentation only

---

## 🧹 Cleanup Recommendations

**If no UI component library planned:**

```bash
# Remove empty ui/ directory tree
git rm -r ui/
git commit -m "Remove legacy ui/ directory after dashboard migration"
```

**If keeping for future use:**
- Keep this README as placeholder
- Document intended purpose when decided
- Add .gitkeep to smv/prototype/ if preserving structure

---

## 📝 Migration Notes

**What was moved (2025-11-12):**
- 16 files from `ui/smv/prototype/` → `dashboard/SMV/`
- Includes: package.json, src/, components/, data/, README.md
- All references updated (9 files across repo)

**Commit history:**
- See commit: "refactor: Move SMV prototype to dashboard/ at root"
- See commit: "refactor: Rename Dashboard → dashboard (lowercase) + add README"

**Related docs:**
- [B-STORM_5.md](../auditors/relay/B-STORM_5.md) Entry 4-6 (migration discussion)
- [REPO_LOG.md](../REPO_LOG.md) (changelog entries)
- [2025-11-12_DESTROYER_EXECUTION_REPORT.md](../docs/Validation/reports/2025-11-12_DESTROYER_EXECUTION_REPORT.md)

---

## 🎯 For Future UI Work

**If adding new UI components/prototypes:**

1. **Decide location first:**
   - Full application? → `/dashboard/`
   - Shared components? → `/ui/`
   - Python dashboard? → `/pages/`

2. **Update this README:**
   - Document new purpose
   - Explain directory structure
   - Link to design docs

3. **Maintain separation:**
   - Design specs → `/docs/`
   - Implementation → `/ui/` or `/dashboard/`
   - Never duplicate

---

**Status:** Legacy directory awaiting cleanup or repurposing decision

**Last Active:** 2025-11-11 (before SMV migration)

**Next Steps:** User to decide - delete entirely or repurpose?

**This README prevents folder display compression while preserving history.** 📂
