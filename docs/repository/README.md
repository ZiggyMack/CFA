<!---
FILE: README.md
PURPOSE: Navigate Doc Claude's Dual-Room Suite (Map Room + Observatory + Workshop)
VERSION: v2.0
STATUS: Active
DEPENDS_ON: None
NEEDED_BY: All repository maintainers, auditors, DOC_CLAUDE
MOVES_WITH: /docs/repository/
LAST_UPDATE: 2025-11-14 [Map Room/Observatory Migration]
--->

<!-- deps: file_structure, documentation -->
# Doc Claude's Suite: Two Rooms Under One Roof

**Purpose:** Central hub for repository structure tracking, health monitoring, and maintenance protocols
**Created:** 2025-10-31 | **Reorganized:** 2025-11-14 (v4.0 Launch Party)
**Maintained by:** DOC_CLAUDE (Repository Librarian)
**Status:** 🟢 ACTIVE

## 🎯 The Dual-Room Philosophy

**The Question:** Why are health reports separate from dependency maps?
**The Answer:** They serve different purposes. They belong in different rooms.

This directory houses Doc Claude's two primary workspaces:

### 📍 **MAP_ROOM** - Structure & Connections
**"What connects to what?"**
- Dependency maps showing file relationships
- Tree structures visualizing repository architecture
- Bootstrap sequences defining canonical paths
- Worldview catalogs listing framework profiles

**Purpose:** Answer structural questions about how the codebase is organized

### 📊 **OBSERVATORY** - Health & Metrics
**"How is everything doing?"**
- Health dashboards with current scores
- Historical health reports (archived)
- Staleness tracking and Gospel Problem detection
- Deep clean protocols and scoring rubrics

**Purpose:** Answer health questions about repository quality and trends

### 🔧 **librarian_tools/** - Doc Claude's Workshop
**"How do I maintain this?"**
- 88MPH rapid assessment framework
- Role definitions (Process, Validator, Destroyer, etc.)
- Header standards and semantic metadata specs
- Integration checklists and integrity protocols

**Purpose:** Operational tools for repository maintenance

---

## 📂 Directory Structure

```
repository/
├── README.md                    # This file - Dual-room philosophy guide
│
├── MAP_ROOM/                    # Structure & Connections
│   ├── dependency_maps_README.md  # Navigation guide (legacy name)
│   ├── MASTER_DEPENDENCY_MAP.md   # Comprehensive file relationships
│   ├── VALIDATION_MAP.md          # Systematic validation checklist
│   ├── BOOTSTRAP_SEQUENCE.md      # Canonical bootstrap paths
│   ├── WORLDVIEW_CATALOG.md       # Framework profile catalog
│   └── DEPENDENCY_CORE.md         # Core dependency specifications
│
├── OBSERVATORY/                 # Health & Metrics
│   ├── REPO_HEALTH_DASHBOARD.md   # Current health status (living doc)
│   ├── REPO_HEALTH_SCORING_RUBRIC.md  # Scoring methodology
│   ├── DEEP_CLEAN_PROTOCOL.md     # Scan-first methodology
│   └── Archives/                  # Historical health snapshots
│       ├── health_reports_README.md  # Archive guide
│       ├── REPO_HEALTH_REPORT_2025-11-12_GREEN.md  # Latest (95/100)
│       ├── REPO_HEALTH_REPORT_2025-10-31_GREEN(1).md
│       ├── REPO_HEALTH_REPORT_2025-10-31_GREEN(2).md
│       └── REPO_HEALTH_REPORT_TEMPLATE_v4.md
│
├── librarian_tools/             # Doc Claude's Workshop
│   ├── README.md                # Tool documentation
│   ├── 88MPH.md                 # Rapid assessment framework
│   ├── ROLE_PROCESS.md          # Process Expert role
│   ├── ROLE_VALIDATION.md       # Validation Expert role
│   ├── ROLE_DESTROYER.md        # Deletion authority role
│   ├── ROLE_LOGGER.md           # REPO_LOG maintenance
│   ├── ROLE_SANITIZE.md         # Sanitization protocols
│   ├── ROLE_REVIEW.md           # Review methodology
│   └── HEADER_STANDARD.md       # Semantic header specs
│
├── FILE_INVENTORY.md            # Complete file catalog (~353 files)
└── LIVING_MAP_MAINTENANCE.md    # Living Map update protocols
```

---

## 🏛️ Doc Claude Wears Different Hats

**As Mapper (MAP_ROOM):**
- "Let me show you how these files connect"
- "This depends on that, and that needs this"
- "Here's the canonical bootstrap sequence"
- Uses MASTER_DEPENDENCY_MAP.md to track relationships

**As Observer (OBSERVATORY):**
- "Repository health: 95/100 GREEN"
- "Staleness detected in 3 files"
- "Health trending upward over last 3 weeks"
- Uses REPO_HEALTH_DASHBOARD.md to monitor metrics

**As Librarian (librarian_tools/):**
- "Running 88MPH rapid assessment"
- "Applying ROLE_DESTROYER deletion protocols"
- "Enforcing semantic header standards"
- Uses operational tools to maintain quality

---

## 🔍 When to Use Each Room

### Use MAP_ROOM When:
- ✅ Finding what depends on a file before modifying it
- ✅ Understanding bootstrap sequence for auditor coordination
- ✅ Locating worldview profiles by name or category
- ✅ Mapping out which files must move together (MOVES_WITH)
- ✅ Identifying circular dependencies or orphan files

### Use OBSERVATORY When:
- ✅ Checking current repository health score
- ✅ Comparing health trends over time
- ✅ Running deep clean protocols to assess quality
- ✅ Detecting Gospel Problem (embedded stale references)
- ✅ Generating new health reports using scoring rubric

### Use librarian_tools/ When:
- ✅ Performing rapid 88MPH assessment (8.8 minutes)
- ✅ Understanding Doc Claude role constraints (Process, Validator, etc.)
- ✅ Learning semantic header format (DEPENDS_ON, NEEDED_BY, etc.)
- ✅ Following deletion protocols (ROLE_DESTROYER)
- ✅ Maintaining REPO_LOG with proper format

## 📊 Key Metrics Tracked

**Repository Health Score:**
- Current: 94/100 🟢
- Target: >85/100
- Components: Documentation, Links, Dependencies, Updates

**Dependency Integrity:**
- Files with headers: [Track %]
- Circular dependencies: [Count]
- Orphan files: [Count]
- Missing dependencies: [Count]

**Documentation Quality:**
- README coverage: ~95%
- Average quality score: 92/100
- Files with headers: [Track %]

## 🚀 Quick Actions

### Generate New Health Report
```bash
1. Use 88MPH.md framework
2. Run comprehensive assessment
3. Save as health_reports/YYYY-MM-DD_STATUS.md
4. Update this README with latest score
```

### Update Dependency Map
```bash
1. Search all files for semantic headers
2. Extract DEPENDS_ON and NEEDED_BY fields
3. Build visual map and tables
4. Save to MASTER_DEPENDENCY_MAP.md
5. Run validation checks
```

### Check Repository Health
```bash
1. Review latest health report
2. Check dependency map for issues
3. Run link integrity check
4. Update metrics in this README
```

## 🔗 Integration Points

**Upstream Dependencies:**
- [/auditors/Bootstrap/88MPH.md](/auditors/Bootstrap/88MPH.md) - Assessment framework
- [REPO_LOG.md](/REPO_LOG.md) - Change tracking
- [VUDU_HEADER_STANDARD.md](/auditors/VUDU_HEADER_STANDARD.md) - Header specs

**Downstream Consumers:**
- DOC_CLAUDE - Uses for maintenance
- Master Branch auditors - Health monitoring
- Deployment processes - Validation checks

## 📈 Health Trend

```
Oct 2025: ████████████████████ 94% 🟢
Sep 2025: ████████████████░░░░ 82% 🟡
Aug 2025: ████████████░░░░░░░░ 65% 🟡
Jul 2025: ████████░░░░░░░░░░░░ 45% 🔴
```

**Trajectory:** ↗ Improving (v3.5 → v3.8.0 enhancements)

## 🎯 Success Criteria

This directory succeeds when:
- ✅ Repository health tracked systematically
- ✅ Dependencies mapped and validated
- ✅ Historical trends visible
- ✅ Maintenance protocols documented
- ✅ Issues identified before they impact users

## 📝 Maintenance Schedule

**Daily:**
- Quick health check (88MPH scan)
- Update any critical issues

**Weekly:**
- Full health assessment (during active dev)
- Update dependency map if structure changed

**Monthly:**
- Comprehensive health report
- Archive old reports
- Trend analysis

**Quarterly:**
- Deep dependency analysis
- Protocol refinement
- Tool updates

## ❓ Purpose Check

Ask yourself:
1. Can I quickly assess repository health?
2. Can I see what depends on what?
3. Can I track improvements over time?
4. Do I have the tools to maintain quality?

If YES to all → This directory serves its purpose ✅

---

**"The repository's health is the project's wealth."** 📊

**This is the way.** 🔥
