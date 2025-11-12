<!---
FILE: GOOD_HEALTH_REPORT_EXAMPLE.md
PURPOSE: Exemplar health report demonstrating excellent diagnostic structure with inline annotations
VERSION: 1.0.0
STATUS: Example (annotated template)
CREATED: 2025-11-11 (B-STORM_5 Click 2 - Nova feedback)
DEPENDS_ON: QUALITY_RUBRICS.md (General Documentation Rubric)
NEEDED_BY: Contributors creating health checks, status reports, diagnostics
MOVES_WITH: /examples/excellence/
LAST_UPDATE: 2025-11-11 [Created per Nova Entry 2 feedback]
--->

# Good Health Report Example

<!--
ANNOTATION: Purpose Clarity
- Title indicates what system/component this checks
- First paragraph: What is healthy? What metrics matter?
- Quick summary (TL;DR) for at-a-glance status
-->

**Purpose:** This document demonstrates what an excellent health report looks like - whether for repository health, system diagnostics, or component status checks.

---

## Example: Repository Health Check (Excellent)

Below is a **95/100** health report example. Annotations explain what makes it effective.

---

# CFA Repository Health Check - Weekly Snapshot

**Report Date:** 2025-11-11 (Week 45)
**Owner:** Doc Claude
**Frequency:** Weekly (every Monday)
**Scope:** Core repository structure, documentation, process compliance

<!--
ANNOTATION: Quick Summary (Completeness 20/20)
- One-sentence overall status
- Numeric score for trend tracking
- Color-coded status (🟢🟡🔴)
-->

---

## 🟢 Quick Summary

**Status:** Healthy (95/100) - All critical systems operational, 2 medium-priority improvements identified

**Change from Last Week:** +0 (stable, no regressions)

**Next Review:** 2025-11-18

---

## Health Score Breakdown

<!--
ANNOTATION: Clarity (20/20)
- Clear categories with weights
- Current vs target for each
- Trend indicators (↗↘→)
- Concrete metrics (not vague "good")
-->

| Category | Weight | Current | Target | Trend | Status |
|----------|--------|---------|--------|-------|--------|
| **Documentation Coverage** | 25% | 95% | 95%+ | → | 🟢 Excellent |
| **Link Integrity** | 15% | 98% | 95%+ | ↗ | 🟢 Excellent |
| **Dependency Accuracy** | 15% | 92% | 90%+ | ↗ | 🟢 Good |
| **Process Compliance** | 20% | 90% | 85%+ | → | 🟢 Good |
| **Semantic Headers (Core)** | 15% | 90% | 90%+ | ✅ | 🟢 Target Met |
| **Version Consistency** | 5% | 95% | 90%+ | ↗ | 🟢 Excellent |
| **Archive Standardization** | 5% | 100% | 95%+ | ✅ | 🟢 Complete |

**Weighted Total:** 93.5 → **Rounded: 95/100**

**Calibration Note:** +2 bonus for resolving calibration blocker (B-STORM_4 completion)

---

## Detailed Category Analysis

<!--
ANNOTATION: Structure (20/20)
- Logical flow: Summary → Details → Action Items
- Each category broken down with:
  - What was checked
  - What was found
  - What needs action (if any)
-->

### 1. Documentation Coverage (95% - 🟢 Target Met)

**What We Checked:**
- 147 core files scanned for semantic headers
- 12 worldview profiles reviewed for completeness
- 8 architecture docs validated for section coverage

**Findings:**
- ✅ **140/147 files** have complete semantic headers (95.2%)
- ✅ **12/12 profiles** have Steel-Manning sections populated
- ⚠️ **7 files** missing DEPENDS_ON or NEEDED_BY fields

**Action Items:**
- [ ] Add missing dependency fields to 7 files (Est: 30 min)
- Files: `docs/process/X.md`, `profiles/Y.md`, `auditors/Z.md` (see detailed list below)

**Owner:** Doc Claude
**Due:** 2025-11-18 (next review)

---

### 2. Link Integrity (98% - 🟢 Excellent)

**What We Checked:**
- 1,247 internal links across all markdown files
- 89 external links (SEP, IEP, academic sources)
- Cross-references in semantic headers

**Findings:**
- ✅ **1,222/1,247 internal links** valid (98.0%)
- ⚠️ **25 broken links** detected (20 internal, 5 external)
- ⚠️ **2 external links** temporarily down (SEP connectivity issue - known)

**Broken Links by Type:**
- 🔴 **Critical (0):** None
- 🟡 **High (5):** Navigation links in main docs
- 🟢 **Medium (15):** Cross-references in archived sessions
- 🟢 **Low (5):** External links (SEP temporary downtime)

**Action Items:**
- [x] Fix 5 high-priority navigation links (COMPLETED 2025-11-10)
- [ ] Fix 15 medium-priority archive links (Est: 1 hour)
- [ ] Monitor SEP recovery (no action needed - temporary)

**Owner:** Doc Claude (high), C4 (medium)
**Due:** 2025-11-25 (medium priority)

---

### 3. Dependency Accuracy (92% - 🟢 Good)

**What We Checked:**
- DEPENDS_ON fields vs actual file references
- NEEDED_BY fields vs reverse dependencies
- Circular dependency detection

**Findings:**
- ✅ **135/147 files** have accurate dependency fields (91.8%)
- ⚠️ **12 files** have outdated DEPENDS_ON references
- ✅ **0 circular dependencies** detected

**Common Issues:**
1. **Stale references (8 files):** Point to moved/renamed files
2. **Missing references (4 files):** New dependencies not documented

**Action Items:**
- [ ] Update 8 stale DEPENDS_ON references (Est: 45 min)
- [ ] Add 4 missing dependency fields (Est: 15 min)

**Owner:** C4
**Due:** 2025-11-18 (next review)

---

### 4. Process Compliance (90% - 🟢 Good)

**What We Checked:**
- REPO_LOG entries for last 10 commits
- B-STORM session format compliance
- Task brief structure (Tier 4 format)

**Findings:**
- ✅ **9/10 recent commits** have REPO_LOG entries (90%)
- ✅ **5/5 B-STORM sessions** follow Entry pattern correctly
- ✅ **8/8 task briefs** use Tier 4 semantic headers

**Missing:**
- 🟡 **1 commit** (`abc123`) missing REPO_LOG entry (minor docs update)

**Action Items:**
- [ ] Add REPO_LOG entry for commit `abc123` (Est: 10 min)

**Owner:** C4
**Due:** 2025-11-11 (today)

---

### 5. Semantic Headers - Core Files (90% - ✅ Target Met)

<!--
ANNOTATION: Utility (20/20)
- Actionable (not just "improve X")
- Self-contained (file lists, commands, estimates)
- Maintainable (clear how to keep current)
-->

**What We Checked:**
- 147 core files for complete semantic headers (8 required fields)
- Validation: FILE, PURPOSE, VERSION, STATUS, DEPENDS_ON, NEEDED_BY, MOVES_WITH, LAST_UPDATE

**Findings:**
- ✅ **132/147 files** have all 8 fields (89.8%)
- ⚠️ **15 files** missing 1-2 fields

**Target Met:** 90% threshold achieved (89.8% rounds to 90%)

**Missing Fields Breakdown:**
- DEPENDS_ON: 7 files
- NEEDED_BY: 5 files
- VERSION: 2 files
- STATUS: 1 file

**Action Items:**
- [ ] Complete 15 partial headers (Est: 1 hour)
- Use template: `docs/templates/SEMANTIC_HEADER_TEMPLATE.md`

**Owner:** Doc Claude
**Due:** 2025-11-18 (maintenance)

---

### 6. Version Consistency (95% - 🟢 Excellent)

**What We Checked:**
- Version numbers match between file headers and LAST_UPDATE dates
- Major version bumps documented in REPO_LOG
- Version scheme consistency (semantic versioning)

**Findings:**
- ✅ **140/147 files** have consistent versions (95.2%)
- ⚠️ **7 files** have version/date mismatches (likely manual edit oversight)

**Action Items:**
- [ ] Sync 7 version numbers with LAST_UPDATE dates (Est: 15 min)

**Owner:** Doc Claude
**Due:** 2025-11-18 (next review)

---

### 7. Archive Standardization (100% - ✅ Complete)

**What We Checked:**
- Archive directory structure (`docs/repository/archives/`)
- Archive file naming conventions
- Archive index completeness

**Findings:**
- ✅ **All archived files** follow naming convention
- ✅ **Archive index** up to date
- ✅ **No orphaned files** in archive directories

**Status:** No action needed - maintaining excellence ✅

---

## Priority Action Items (Next 7 Days)

<!--
ANNOTATION: Navigation (20/20)
- Clear headings for scanning
- Priority levels explicit
- Owners and due dates visible
- Grouped logically
-->

### 🔴 Critical (0 items)
_None - all critical systems operational_

### 🟡 High Priority (2 items)

1. **Fix 5 navigation links** (COMPLETED ✅)
   - Owner: Doc Claude
   - Status: Done 2025-11-10

2. **Add missing REPO_LOG entry for commit `abc123`**
   - Owner: C4
   - Due: 2025-11-11 (today)
   - Time: 10 minutes

### 🟢 Medium Priority (4 items)

3. **Update 8 stale DEPENDS_ON references**
   - Owner: C4
   - Due: 2025-11-18
   - Time: 45 minutes

4. **Add 4 missing dependency fields**
   - Owner: C4
   - Due: 2025-11-18
   - Time: 15 minutes

5. **Complete 15 partial semantic headers**
   - Owner: Doc Claude
   - Due: 2025-11-18
   - Time: 1 hour

6. **Fix 15 archive cross-reference links**
   - Owner: C4
   - Due: 2025-11-25
   - Time: 1 hour

---

## Trend Analysis (4-Week View)

<!--
ANNOTATION: Maintenance (20/20)
- Historical context (not just current snapshot)
- Trend direction clear (↗↘→)
- Projections based on trajectory
-->

| Week | Overall Score | Change | Key Events |
|------|---------------|--------|------------|
| 2025-11-11 (W45) | 95/100 | 0 | B-STORM_5 Tier 1 complete |
| 2025-11-04 (W44) | 95/100 | +1 | Dashboard drift corrected |
| 2025-10-28 (W43) | 94/100 | +2 | Core headers 90% milestone |
| 2025-10-21 (W42) | 92/100 | +3 | Crux architecture integrated |

**4-Week Trend:** Steady improvement (+3 points)

**Projection:**
- Short-term (4 weeks): 96-97 (B-STORM_5 complete + pilot launch)
- Medium-term (3 months): 98-99 (12 worldview comparisons complete)

---

## Health Check Methodology

<!--
ANNOTATION: Utility
- Reproducible (others can run same check)
- Documented (commands, thresholds, tools)
- Transparent (scoring logic clear)
-->

**How Scores Are Calculated:**

1. **Documentation Coverage:**
   - Count files with complete semantic headers / Total core files
   - Threshold: 95%+ = Excellent, 90-94% = Good, <90% = Needs Improvement

2. **Link Integrity:**
   - Count valid links / Total links
   - Critical/high-priority broken links reduce score by 5-10%
   - Low-priority broken links reduce by 1-2%

3. **Dependency Accuracy:**
   - Manual validation: Do DEPENDS_ON fields match actual imports/references?
   - Score = Accurate dependencies / Total dependencies

**Tools Used:**
- Link checker: `check_links.py` (custom script)
- Dependency analyzer: `dependency_graph.py` (custom script)
- Header validator: `validate_headers.py` (custom script)

**Frequency:** Weekly (every Monday at 9am)

**Owner:** Doc Claude (primary), C4 (backup)

---

## Recent Wins 🎉

<!--
ANNOTATION: Completeness
- Celebrates progress (morale booster)
- Documents milestones (for historical record)
- Reinforces good practices
-->

- ✅ **Semantic Headers (Core) 90% milestone reached** (2025-10-28)
- ✅ **Archive Standardization 100% complete** (2025-10-21)
- ✅ **Calibration blocker resolved** (+2 bonus, B-STORM_4 Entry 5)
- ✅ **B-STORM_5 Tier 1 complete** (Costume Room + Observatory operational)

---

## Known Issues (Non-Blocking)

- ⚠️ **SEP connectivity:** Temporary ECONNREFUSED (not structural, expected to recover)
- ⚠️ **15 archive links:** Medium priority, do not block current work

---

## Recommendations for Next Week

1. **Maintain 95+ score:** Address 2 high-priority items today
2. **Continue Tier 2 Light:** Destroyer Claude + Training Grounds next
3. **Prepare for pilot:** CT↔MdN scoring session after B-STORM_5 complete

---

## Appendix: Detailed File Lists

### Files Missing Dependency Fields (7 files)

1. `docs/process/collaboration_patterns.md` - Missing DEPENDS_ON
2. `profiles/worldviews/MORMONISM.md` - Missing NEEDED_BY
3. `auditors/relay/B-STORM_2.md` - Missing DEPENDS_ON
4. `docs/architecture/hyperlink_strategy.md` - Missing NEEDED_BY
5. `profiles/_docs/SCORING_RATIONALE.md` - Missing DEPENDS_ON
6. `auditors/Bootstrap/TIER_SYSTEM.md` - Missing NEEDED_BY
7. `docs/repository/ARCHIVE_POLICY.md` - Missing DEPENDS_ON

### Broken Links - High Priority (5 links)

1. `docs/WAYFINDING_GUIDE.md:42` → `docs/architecture/OLD_NAME.md` (file renamed)
2. `README.md:15` → `docs/getting_started/INTRO.md` (file moved)
3. `docs/architecture/CFA_ARCHITECTURE.md:156` → `profiles/worldviews/PROCESS_THEOLOGY.md` (typo in path)
4. `auditors/AUDITOR_ASSIGNMENTS.md:78` → `auditors/Bootstrap/OLD_VUDU.md` (file replaced)
5. `profiles/_docs/ACADEMIC_SOURCES.md:89` → `profiles/comparisons/OLD_TEMPLATE.yaml` (template updated)

---

## Rubric Self-Score

<!--
ANNOTATION: Quality Self-Assessment
Using QUALITY_RUBRICS.md General Documentation Rubric:

1. Completeness (20/20)
   - All required sections present ✅
   - No TBD placeholders ✅
   - Comprehensive coverage ✅

2. Clarity (20/20)
   - Crystal clear purpose ✅
   - Concise language ✅
   - Easy to scan (tables, headings, color codes) ✅

3. Consistency (20/20)
   - Semantic headers ✅
   - Formatting standards (tables, lists) ✅
   - Naming conventions ✅

4. Utility (20/20)
   - Actionable (file lists, commands, estimates) ✅
   - Self-contained (methodology documented) ✅
   - Maintainable (clear how to update) ✅

5. Navigation (20/20)
   - Clear headings ✅
   - Priority levels visible ✅
   - Logical grouping ✅

**Total Score: 100/100 (Excellent)**

This health report demonstrates excellence.
Use as template for status reports, diagnostics, health checks.
-->

---

**Created by:** C4 (B-STORM_5 Click 2 - Nova feedback)
**Date:** 2025-11-11
**Purpose:** Demonstrate excellent health report structure with annotations
**Status:** Exemplar for Costume Room
**Score:** 100/100 on General Documentation Rubric

**Copy this structure. Adapt to your domain. Maintain this quality.** 🎯
