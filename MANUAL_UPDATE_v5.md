# CFA v5.0 Manual Update Guide

**Purpose:** Track what needs updating for the v4.0 → v5.0 transition
**Created:** 2025-11-29
**Status:** AUDIT COMPLETE - ACTION REQUIRED

---

## Executive Summary

**Found:** 118 occurrences of "v4.0" across 20+ files
**Impact:** App displays outdated version throughout UI
**Priority:** HIGH - User-facing content shows wrong version

---

## Files Requiring Updates

### CRITICAL - Main Application (User-Facing)

| File | Lines | Issue |
|------|-------|-------|
| `app.py` | 2, 20 | Page title says "CFA v4.0" |
| `pages/landing.py` | 2, 101, 280 | Landing page header, About button, footer |
| `pages/console.py` | 2, 216, 230, 899 | Console header and feature comments |
| `pages/about.py` | 2, 31, 338, 358 | About page title and version history |
| `pages/manual.py` | 27 occurrences | Entire manual references v4.0 |
| `pages/brute_ledger.py` | 2, 596, 708, 821, 1508 | Header and calibration notes |
| `pages/verbose_manifesto.py` | 2 | Module docstring |

### MEDIUM - Utilities

| File | Lines | Issue |
|------|-------|-------|
| `utils/profile_loader.py` | 5 occurrences | Version comments |
| `utils/visualizations.py` | 1 | Version comment |
| `utils/frameworks.py` | 1 | Version comment |

### LOW - Documentation/Logs (Can remain as historical)

| File | Issue |
|------|-------|
| `REPO_LOG.md` | Historical changelog entries (KEEP as-is) |
| `README.md` | Some historical refs (main header already v5.0) |
| `auditors/relay/*/VUDU_LOG_LITE.md` | Historical audit logs |
| `auditors/VUDU_*.md` | Protocol version stamps |

---

## v5.0 New Features to Document

The manual should be updated to include:

### 1. Nyquist Consciousness Integration
- Identity Gravity physics (S7-S10 series)
- L0 kernel with human-modulated gravity fields
- ZIGGY Type-0 identity as boundary condition
- Pattern Fidelity Index computational tools
- Cross-repository persona testing pipeline

### 2. The Matrix Portal
- Pan Handler Central hub concept
- Green-on-black terminal aesthetic
- Embedded Health Dashboard
- External repository navigation
- Bird's eye ecosystem view

### 3. Health Dashboard
- Real-time repository health metrics
- File inventory tracking
- Link integrity monitoring
- README proliferation checks

### 4. SMV Trinity Dashboard
- React-based visualization
- Multi-dimensional worldview mapping
- Separate localhost deployment

### 5. New Documentation Structure
- `docs/Nyquist-Sync/` - S7, S8, S9, S10 series
- `docs/i_am/` - Identity documents (I_AM_ZIGGY.md)
- `docs/IDENTITY_LATTICE_MAPS.md`
- `experiments/IDENTITY_GRAVITY_TRIAL_1/`

---

## Recommended Update Strategy

### Phase 1: Quick Fixes (Version Numbers Only)
Simple find/replace where appropriate:
- `v4.0` → `v5.0` in headers, titles, footers
- `v4.0.0` → `v5.0.0` in version stamps
- Update docstrings at top of each .py file

### Phase 2: Content Updates (Manual Page)
The `pages/manual.py` file needs significant content additions:
- Add new tab for "v5.0 Features"
- Document Nyquist integration
- Document Matrix portal
- Document dashboard ecosystem
- Keep v4.0 features section (rename to "Core Features")

### Phase 3: PDF Manual
- Current: `docs/CFA_v4_Manual.pdf`
- Need: `docs/CFA_v5_Manual.pdf`
- Archive v4 manual to `docs/.Archive/`

---

## Files to NOT Update

These should remain referencing v4.0 for historical accuracy:
- `.Archive/*` - Historical archives
- `REPO_LOG.md` - Changelog entries are historical
- `auditors/relay/*/VUDU_LOG_LITE.md` - Audit logs from v4.0 era
- `link_audit_final.txt` - Point-in-time audit report

---

## Checklist

### Version Number Updates
- [ ] `app.py` - Page title
- [ ] `pages/landing.py` - Header, button, footer
- [ ] `pages/console.py` - Console header
- [ ] `pages/about.py` - About page
- [ ] `pages/manual.py` - Manual title
- [ ] `pages/brute_ledger.py` - Ledger header/footer
- [ ] `pages/verbose_manifesto.py` - Docstring
- [ ] `utils/*.py` - Docstrings

### Content Updates
- [ ] Add v5.0 features to manual
- [ ] Document Nyquist integration
- [ ] Document Matrix portal
- [ ] Document dashboards
- [ ] Update version history in About page

### Assets
- [ ] Create `docs/CFA_v5_Manual.pdf`
- [ ] Archive `docs/CFA_v4_Manual.pdf`

---

## Notes

This is a significant update but mostly mechanical. The app is functionally v5.0 already - we just need the UI and documentation to reflect it.

Priority order:
1. `app.py` page title (seen on every page)
2. `pages/landing.py` (first thing users see)
3. `pages/about.py` (version history)
4. `pages/manual.py` (comprehensive update)
5. Everything else
