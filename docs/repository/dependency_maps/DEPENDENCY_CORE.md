# DEPENDENCY CORE - Quick Reference Map

**Version:** v1.0
**Last Updated:** 2025-11-12
**Purpose:** Quick-access pointer to critical dependencies in MASTER_DEPENDENCY_MAP.md
**Owner:** Doc Claude (Documentation Orchestration)

---

## 🎯 PURPOSE

**This is a POINTER FILE - it contains NO duplicate data.**

All actual dependency information lives in [MASTER_DEPENDENCY_MAP.md](MASTER_DEPENDENCY_MAP.md). This file simply provides:
1. Quick links to critical sections (anchor-based, no line numbers)
2. Section summaries (what you'll find there)
3. Fast navigation for common lookup tasks

**Philosophy:** "Point, don't duplicate. Anchors, not line numbers."

---

## 🚀 CRITICAL SECTIONS (Most Frequently Accessed)

### **1. Bootstrap Dependencies**
**What you need:** Understanding bootstrap file relationships

**Jump to:** [🎯 KEY CONCEPTUAL DEPENDENCY CHAINS](MASTER_DEPENDENCY_MAP.md#-key-conceptual-dependency-chains) → "Bootstrap System"

**Summary:** How bootstrap files reference each other, living maps, and role files

---

### **2. Calibration Dependencies**
**What you need:** Files required before Grok VUDU activation

**Jump to:** [🚨 CRITICAL DEPENDENCIES FOR CALIBRATION](MASTER_DEPENDENCY_MAP.md#-critical-dependencies-for-calibration)

**Summary:** 17 critical files that must be present/correct before mission launch

---

### **3. Living Maps Relationships**
**What you need:** Which living maps depend on each other

**Jump to:** [📋 COMPREHENSIVE DEPENDENCY TABLES](MASTER_DEPENDENCY_MAP.md#-comprehensive-dependency-tables) → Search for "Living Maps"

**Summary:** BOOTSTRAP_SEQUENCE, WORLDVIEW_CATALOG, FILE_INVENTORY, DASHBOARD dependencies

---

### **4. Profile Dependencies**
**What you need:** Worldview profile structure and dependencies

**Jump to:** [📋 COMPREHENSIVE DEPENDENCY TABLES](MASTER_DEPENDENCY_MAP.md#-comprehensive-dependency-tables) → Search for "Profiles"

**Summary:** How CLASSICAL_THEISM, METHODOLOGICAL_NATURALISM, etc. relate to comparisons

---

### **5. Ethics System Dependencies**
**What you need:** Tier-1 ethics front-matter and validation chain

**Jump to:** [📋 COMPREHENSIVE DEPENDENCY TABLES](MASTER_DEPENDENCY_MAP.md#-comprehensive-dependency-tables) → Search for "Ethics"

**Summary:** ETHICAL_INVARIANT_SCHEMA → 8 Tier-1 files → ETHICS_FRONT_MATTER_VALIDATION

---

### **6. SMV Prototype Dependencies**
**What you need:** UI_SMV prototype file structure and data dependencies

**Jump to:** [📋 COMPREHENSIVE DEPENDENCY TABLES](MASTER_DEPENDENCY_MAP.md#-comprehensive-dependency-tables) → Search for "SMV"

**Summary:** Design docs (smv/) vs implementation (dashboard/SMV/) relationships

---

## 📊 QUICK STATS (Pointers to Metrics)

**Want repository-wide statistics?**

**Jump to:** [📊 METRICS SUMMARY](MASTER_DEPENDENCY_MAP.md#-metrics-summary)

**Contains:**
- Total files mapped
- Dependency coverage percentage
- Critical path counts
- Health assessment scores

---

## 🔍 COMMON LOOKUP TASKS

### **"What depends on this file?"**
1. Open [MASTER_DEPENDENCY_MAP.md](MASTER_DEPENDENCY_MAP.md)
2. Search (Ctrl+F) for the filename
3. Look in "NEEDED_BY" column of dependency tables

### **"What does this file depend on?"**
1. Open [MASTER_DEPENDENCY_MAP.md](MASTER_DEPENDENCY_MAP.md)
2. Search (Ctrl+F) for the filename
3. Look in "DEPENDS_ON" column of dependency tables

### **"Is the repository ready for [milestone]?"**
1. Jump to: [✅ CALIBRATION GO/NO-GO ASSESSMENT](MASTER_DEPENDENCY_MAP.md#-calibration-gono-go-assessment)
2. Check milestone-specific checklist

### **"Where's the full dependency tree?"**
1. Jump to: [🗺️ REPOSITORY TREE STRUCTURES](MASTER_DEPENDENCY_MAP.md#️-repository-tree-structures)
2. Navigate to relevant section (auditors/, docs/, profiles/)

---

## 🔄 MAINTENANCE PROTOCOL

**When MASTER_DEPENDENCY_MAP.md is updated:**

This file (DEPENDENCY_CORE.md) needs NO updates if:
- ✅ Section headers remain the same (anchor links stay valid)
- ✅ Content within sections changes (that's fine, we just point to sections)

This file NEEDS updates only if:
- ⚠️ Section headers renamed (update anchor links)
- ⚠️ New critical section added (add pointer here)
- ⚠️ Section removed (remove pointer)

**Philosophy:** Anchor-based links are resilient to content changes, only break if headers change.

---

## 📋 SECTION ANCHOR REFERENCE

**Quick copy-paste links to all major sections:**

```markdown
[Main Overview](MASTER_DEPENDENCY_MAP.md)
[Repository Trees](MASTER_DEPENDENCY_MAP.md#️-repository-tree-structures)
[Conceptual Chains](MASTER_DEPENDENCY_MAP.md#-key-conceptual-dependency-chains)
[Dependency Tables](MASTER_DEPENDENCY_MAP.md#-comprehensive-dependency-tables)
[Critical Calibration](MASTER_DEPENDENCY_MAP.md#-critical-dependencies-for-calibration)
[Calibration Chains](MASTER_DEPENDENCY_MAP.md#-calibration-dependency-chains)
[Health Assessment](MASTER_DEPENDENCY_MAP.md#-dependency-health-assessment)
[Map Maintenance](MASTER_DEPENDENCY_MAP.md#-map-maintenance)
[Go/No-Go Check](MASTER_DEPENDENCY_MAP.md#-calibration-gono-go-assessment)
[Metrics Summary](MASTER_DEPENDENCY_MAP.md#-metrics-summary)
```

---

## 🎯 WHEN TO USE WHICH FILE

**Use DEPENDENCY_CORE.md (this file) when:**
- You know what you need, want fast navigation
- You're doing common lookups (bootstrap, calibration, profiles)
- You want quick stats without reading 58KB file

**Use MASTER_DEPENDENCY_MAP.md when:**
- You need comprehensive dependency details
- You're doing deep dependency tracing
- You're updating dependency information
- You want the full repository tree structures

---

## 💡 QUICK TIPS

**Pro tip 1:** Bookmark this file for instant access to critical sections

**Pro tip 2:** Use anchor links in commit messages:
```
See [Calibration Dependencies](docs/repository/dependency_maps/MASTER_DEPENDENCY_MAP.md#-critical-dependencies-for-calibration)
```

**Pro tip 3:** Section anchors work in GitHub web view and local markdown renderers

**Pro tip 4:** If anchor link breaks, section header changed - check MASTER_DEPENDENCY_MAP.md git log

---

## 🔗 RELATED FILES

**Other living maps:**
- [BOOTSTRAP_SEQUENCE.md](BOOTSTRAP_SEQUENCE.md) - Bootstrap procedures
- [WORLDVIEW_CATALOG.md](WORLDVIEW_CATALOG.md) - Worldview profiles
- [FILE_INVENTORY.md](../FILE_INVENTORY.md) - Repository file listing
- [REPO_HEALTH_DASHBOARD.md](../REPO_HEALTH_DASHBOARD.md) - Health metrics

**Tools:**
- [88MPH.md](../librarian_tools/88MPH.md) - Rapid assessment
- [DEEP_CLEAN_PROTOCOL.md](../Health_Reports/DEEP_CLEAN_PROTOCOL.md) - Comprehensive scan

---

**Last Updated:** 2025-11-12
**Maintainer:** Doc Claude (update only if MASTER section headers change)
**Philosophy:** "Point, don't duplicate. Anchors, not line numbers. Single source, fast access."

**This is the way.** 🗺️
