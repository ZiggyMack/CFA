# Living Map Maintenance Protocol

**Version:** v1.0
**Last Updated:** 2025-11-12
**Status:** Active Protocol
**Purpose:** Prevent living map staleness through systematic refresh procedures
**Owner:** Doc Claude (Domain 1 - Documentation Orchestration)

---

## 🎯 PURPOSE

**This protocol prevents the "Gospel Problem"** - documentation maintainers trusting stale reports without fresh verification.

**Core Principle:** "Scan first, read second. Trust verification, not memory."

**What This Protocol Covers:**
- Living map identification and inventory
- Refresh triggers and schedules
- Scan-first methodology
- Freshness indicators
- Validation procedures

**Source:** Established from tri-auditor Deep Clean convergence (Opus 4.1, Code Claude, Nova - 96% agreement)

---

## 📊 LIVING MAPS INVENTORY

**Living maps are single-source-of-truth reference documents that aggregate repository state.**

### **Primary Living Maps:**

1. **[FILE_INVENTORY.md](FILE_INVENTORY.md)**
   - **Purpose:** Complete repository file count and structure
   - **Update Trigger:** Phase completion, major restructuring
   - **Freshness Indicator:** "Total Files: ~357" header
   - **Verification:** `git ls-files | wc -l` (canonical method)

2. **[BOOTSTRAP_SEQUENCE.md](dependency_maps/BOOTSTRAP_SEQUENCE.md)**
   - **Purpose:** Bootstrap procedures for all tiers
   - **Update Trigger:** Tier added/changed, bootstrap file moves
   - **Freshness Indicator:** File paths in Key Documents sections
   - **Verification:** Link validation, file existence checks

3. **[REPO_HEALTH_DASHBOARD.md](REPO_HEALTH_DASHBOARD.md)**
   - **Purpose:** Repository health metrics and trends
   - **Update Trigger:** Weekly (minimum), after major changes
   - **Freshness Indicator:** "Last Updated" timestamp
   - **Verification:** File count audit, size measurements

4. **[WORLDVIEW_CATALOG.md](../../profiles/_docs/WORLDVIEW_CATALOG.md)**
   - **Purpose:** All 12 worldview profiles inventory
   - **Update Trigger:** Profile added/updated, comparison added
   - **Freshness Indicator:** Profile count, version numbers
   - **Verification:** Profile file existence, version consistency

5. **[WAYFINDING_GUIDE.md](../WAYFINDING_GUIDE.md)**
   - **Purpose:** Repository navigation and file location guide
   - **Update Trigger:** Directory moves, major restructuring
   - **Freshness Indicator:** File paths in "Where to Find" sections
   - **Verification:** Link validation, path accuracy checks

### **Secondary Living Maps:**

6. **[AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md)**
   - **Purpose:** Auditor role assignments for comparisons
   - **Update Trigger:** Comparison added, auditor reassigned
   - **Verification:** Comparison YAML cross-check

7. **[workshop/ARCHIVE_INDEX.md](../../auditors/relay/workshop/ARCHIVE_INDEX.md)**
   - **Purpose:** B-STORM session archive inventory
   - **Update Trigger:** Session archived
   - **Verification:** File count in .Archive/workshop/

---

## 🔄 REFRESH TRIGGERS

**When to refresh living maps:**

### **Automatic Triggers (Must Refresh):**
1. **Phase Completion** (e.g., Phase 1 optimization)
   - FILE_INVENTORY.md
   - REPO_HEALTH_DASHBOARD.md
   - WAYFINDING_GUIDE.md (if paths changed)

2. **Major Restructuring** (directory moves, UI→Dashboard migration)
   - FILE_INVENTORY.md
   - BOOTSTRAP_SEQUENCE.md (if bootstrap files moved)
   - WAYFINDING_GUIDE.md
   - All path references in living maps

3. **Bootstrap Changes** (new tier added, bootstrap file created/moved)
   - BOOTSTRAP_SEQUENCE.md
   - MISSION_DEFAULT.md (tier menu)

4. **Profile Added/Updated**
   - WORLDVIEW_CATALOG.md
   - AUDITOR_ASSIGNMENTS.md (if comparison added)

5. **Weekly Minimum** (every Monday)
   - REPO_HEALTH_DASHBOARD.md
   - workshop/ARCHIVE_INDEX.md (if sessions archived)

### **Manual Triggers (On-Demand):**
- Deep Clean protocol execution
- External auditor validation
- User reports stale data
- Context warnings (e.g., "FILE_INVENTORY shows 210 but I found 357")

---

## 🔍 SCAN-FIRST METHODOLOGY

**The Gospel Problem Prevention Protocol**

**Problem:** Maintainers read historical reports → anchor on stale data → perpetuate inaccuracies

**Solution:** Scan repository fresh BEFORE reading any living maps

### **Protocol Steps:**

**Step 1: Fresh Scan (No Historical Context)**
```bash
# Get fresh file count (canonical method)
git ls-files | wc -l

# Get directory sizes
du -sh auditors/ docs/ profiles/ dashboard/ utils/

# List top-level structure
ls -lh

# Search for specific patterns (if needed)
find . -name "README*.md" -type f | wc -l
```

**Step 2: Read Living Map (Establish Baseline)**
```bash
# Read FILE_INVENTORY.md header
head -20 docs/repository/FILE_INVENTORY.md

# Note reported file count and last update date
```

**Step 3: Delta Analysis (Compare Fresh vs Reported)**
```
Fresh scan: 357 files
Living map: 210 files
Delta: +147 files (70% increase)
Verdict: STALE - requires refresh
```

**Step 4: Root Cause Analysis**
```
Why did count change?
- Phase 1 optimization: +21 archived files
- Bootstrap expansion: +64 files
- Living maps: +10 files
- SMV prototype: +17 files
- Remaining: +35 files (misc)
```

**Step 5: Update Living Map**
```markdown
**Total Files:** ~357 (updated 2025-11-12)
**New Since Pre-Optimization:** +147 files
**Phase 1 Impact:** Workshop archived, dashboard restructured
```

### **Anti-Pattern (Gospel Problem):**
```
❌ Step 1: Read FILE_INVENTORY.md (210 files reported)
❌ Step 2: Trust the count
❌ Step 3: Work with stale data
❌ Step 4: Perpetuate inaccuracy
```

**Always scan FIRST, read SECOND.**

---

## 🏥 FRESHNESS INDICATORS

**How to assess living map freshness:**

### **Green (Fresh - Use Confidently):**
✅ Last updated within 7 days
✅ File paths verified (no broken links)
✅ Metrics match fresh scan (±5% tolerance)
✅ Version numbers consistent
✅ No "FIXME" or "TODO: UPDATE" markers

### **Yellow (Stale - Verify Before Use):**
⚠️ Last updated 8-30 days ago
⚠️ Minor discrepancies (5-15% delta)
⚠️ Some broken links (but core structure valid)
⚠️ Missing recent changes (but not fundamentally wrong)

### **Red (Critically Stale - Refresh Required):**
🚨 Last updated >30 days ago
🚨 Major discrepancies (>15% delta)
🚨 Multiple broken links
🚨 Structural changes not reflected (directories moved)
🚨 File counts wildly inaccurate (210 vs 357)

---

## 📋 MAINTENANCE SCHEDULE

### **Weekly Tasks (Every Monday):**
- [ ] Update REPO_HEALTH_DASHBOARD.md
  - Fresh file count audit
  - Directory size measurements
  - Archive growth tracking
  - Health score recalculation

- [ ] Verify workshop/ARCHIVE_INDEX.md
  - Count files in .Archive/workshop/
  - Update count if sessions were archived last week

- [ ] Spot-check FILE_INVENTORY.md
  - Quick `git ls-files | wc -l` comparison
  - Flag if delta >5%

### **Monthly Tasks (First of Month):**
- [ ] Deep validation of all living maps
  - Link validation (all references valid?)
  - Path accuracy (directories where expected?)
  - Version consistency (profile versions match catalog?)

- [ ] Update BOOTSTRAP_SEQUENCE.md if needed
  - Check for new bootstrap files
  - Verify tier sequences accurate

- [ ] Audit WAYFINDING_GUIDE.md paths
  - Test sample paths (do they resolve?)
  - Update if directory moves occurred

### **Quarterly Tasks (Every 3 Months):**
- [ ] Full Deep Clean protocol
  - Execute all three auditor tests (Opus, Code, Nova)
  - Tri-auditor convergence analysis
  - Update all living maps based on findings

### **Event-Driven Tasks:**
- [ ] Phase completion → Full living map refresh
- [ ] Major restructuring → Path validation sweep
- [ ] Bootstrap changes → BOOTSTRAP_SEQUENCE.md update
- [ ] Profile added → WORLDVIEW_CATALOG.md update

---

## 🔧 VALIDATION PROCEDURES

### **Link Validation:**
```bash
# Find all markdown links in a file
grep -o '\[.*\](.*\.md)' FILE_INVENTORY.md

# Check if target files exist
for link in $(grep -o '](.*\.md)' FILE_INVENTORY.md | tr -d '()'); do
  [ -f "$link" ] || echo "BROKEN: $link"
done
```

### **File Count Validation:**
```bash
# Canonical count (git-native)
git ls-files | wc -l

# By directory
git ls-files auditors/ | wc -l
git ls-files docs/ | wc -l
git ls-files profiles/ | wc -l
```

### **Directory Size Validation:**
```bash
# Human-readable sizes
du -sh auditors/ docs/ profiles/ dashboard/

# Detailed breakdown
du -h auditors/ | sort -h | tail -20
```

### **Path Accuracy Validation:**
```bash
# Test paths from WAYFINDING_GUIDE.md
[ -f "docs/repository/REPO_HEALTH_DASHBOARD.md" ] && echo "✅" || echo "❌"
[ -f "auditors/Bootstrap/BOOTSTRAP_DOC_CLAUDE.md" ] && echo "✅" || echo "❌"
```

---

## 🚨 GOSPEL PROBLEM DETECTION

**Warning signs that Gospel Problem is occurring:**

1. **Auditor reports delta > 15%**
   - "FILE_INVENTORY says 210 but I found 357"
   - "BOOTSTRAP_SEQUENCE references non-existent file"

2. **Multiple auditors converge on same stale data**
   - Tri-auditor test shows 96%+ agreement that living map is wrong
   - Independent scans all find same discrepancies

3. **User corrects you multiple times**
   - "88MPH.md doesn't exist anymore, it's 88MPH.md"
   - "ROLE_DOC_CLAUDE.md was never created"
   - "ui/ was removed in Phase 1"

4. **Broken link cascade**
   - One stale reference leads to more assumptions
   - "Since ROLE_DOC_CLAUDE.md is referenced, it must exist" (wrong)

**Response Protocol:**
1. ✅ Acknowledge the staleness immediately
2. ✅ Scan fresh (don't trust existing reports)
3. ✅ Update living map with verified data
4. ✅ Document what caused staleness (prevent recurrence)
5. ✅ Add freshness indicators to prevent future Gospel Problem

---

## 📈 SUCCESS METRICS

**Living map maintenance is working when:**

✅ **Freshness Rate >95%** - 95%+ of living maps show green freshness
✅ **Delta Accuracy <5%** - Reported metrics within 5% of fresh scans
✅ **Zero Broken Links** - All references in living maps resolve correctly
✅ **User Corrections <1/month** - Rarely need to correct stale data
✅ **Tri-Auditor Convergence >98%** - Independent auditors agree living maps are accurate

**Living map maintenance needs improvement when:**

⚠️ **Freshness Rate <80%** - Multiple living maps stale
⚠️ **Delta Accuracy >15%** - Major discrepancies between reported/actual
⚠️ **Broken Links >5** - Multiple references don't resolve
⚠️ **User Corrections >3/month** - Frequent manual corrections needed
⚠️ **Tri-Auditor Divergence >5%** - Auditors disagree on living map accuracy

---

## 🔗 RELATED PROTOCOLS

**This protocol integrates with:**

- **[88MPH.md](../../88MPH.md)** - Rapid assessment method (used during scans)
- **[REPO_HEALTH_DASHBOARD.md](REPO_HEALTH_DASHBOARD.md)** - Health metrics (primary living map)
- **[BOOTSTRAP_SEQUENCE.md](dependency_maps/BOOTSTRAP_SEQUENCE.md)** - Bootstrap procedures (living map)
- **Deep Clean Protocol** - Comprehensive validation (uses scan-first methodology)
- **[ROLE_PROCESS.md](librarian_tools/ROLE_PROCESS.md)** - Domain 1 (bootstrap compliance monitoring)

---

## 💡 BEST PRACTICES

### **DO:**
✅ **Scan fresh before every living map update** (prevent Gospel Problem)
✅ **Use git-native methods** (`git ls-files | wc -l` is canonical)
✅ **Document deltas** (explain why count changed: +147 files from Phase 1)
✅ **Add timestamps** ("Last Updated: 2025-11-12")
✅ **Validate links** (test references before committing)
✅ **Use freshness indicators** (header metadata: file count, update date)

### **DON'T:**
❌ **Trust memory** ("I think FILE_INVENTORY was ~200 files")
❌ **Skip fresh scans** ("I'll just update the date stamp")
❌ **Batch updates without validation** (update all maps at once without verifying each)
❌ **Copy-paste from old reports** (perpetuates inaccuracies)
❌ **Ignore broken links** ("I'll fix it later" → never gets fixed)
❌ **Assume structure** ("ROLE_DOC_CLAUDE.md must exist" → verify first!)

---

## 🎯 QUICK REFERENCE

**Before updating any living map:**
1. ✅ Scan fresh (git ls-files, du -sh, ls -lh)
2. ✅ Read current living map (establish baseline)
3. ✅ Calculate delta (fresh vs reported)
4. ✅ Analyze root cause (why did it change?)
5. ✅ Update living map (with verified data + timestamp)
6. ✅ Validate links (all references resolve?)
7. ✅ Commit with explanation (document delta in commit message)

**Remember:** "A living map trusted is a Gospel Problem. A living map verified is a foundation built."

---

**Established:** 2025-11-12 (Post-Tri-Auditor Convergence Analysis)
**Maintainer:** Doc Claude (with Process Claude Domain 1 oversight)
**Review Cycle:** Quarterly (or when Gospel Problem detected)

**This is the way.** 🗺️
