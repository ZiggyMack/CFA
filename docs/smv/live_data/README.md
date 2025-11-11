<!---
FILE: README.md
PURPOSE: Documentation for SMV live_data/ directory (generated artifacts from worldview profiles)
VERSION: 1.0.0
STATUS: Active (Phase 2 ready - awaiting first VUDU session exports)
DEPENDS_ON: SMV_DATA_MAP.md, SMV_DESIGN_SPEC.md, profiles/worldviews/*.md, profiles/comparisons/*.yaml
NEEDED_BY: SMV UI (visualization layer), SMV Claude (data generation)
MOVES_WITH: /docs/smv/live_data/
CREATED: 2025-11-11 (B-STORM_6 SMV Claude infrastructure)
LAST_UPDATE: 2025-11-11 [Initial version - placeholder for Phase 2]
--->

# SMV Live Data — Generated Visualization Artifacts

**Purpose:** This directory contains SMV JSON files generated from CFA worldview profiles. These are **derived artifacts**, not source of truth.

**Status:** Placeholder (Phase 2 - awaiting CT↔MdN pilot completion)

---

## 🎯 What Lives Here

**Generated Files (Phase 2+):**
```
docs/smv/live_data/
├── README.md (this file)
├── CT_vs_MdN.json (pilot - first export after VUDU session)
├── CT_vs_ProcessTheology.json (second comparison - cooperative pairing demo)
└── [64 other comparisons - generated as VUDU sessions complete]
```

**Full Coverage:** 66 JSON files (one per worldview pairing)

---

## 📊 File Format

**Each JSON file follows SMV schema v1.1+** (see [SMV_DESIGN_SPEC.md](../SMV_DESIGN_SPEC.md))

**Example Structure:**

```json
{
  "_meta": {
    "generated": "2025-11-12T14:45:00Z",
    "smv_schema_version": "1.1.0",
    "source_files": [
      "profiles/worldviews/CLASSICAL_THEISM.md",
      "profiles/worldviews/METHODOLOGICAL_NATURALISM.md",
      "profiles/comparisons/CT_vs_MdN.yaml",
      "auditors/VUDU_logs/CT_vs_MdN_20251112.json"
    ],
    "calibration_hashes": {
      "pro_ct": "1bbec1e119a2c425",
      "anti_mdn": "00cd73274759e218"
    },
    "data_map_version": "1.0.0"
  },
  "session_id": "CT_vs_MdN_VUDU_20251112",
  "worldview_pair": "CT_vs_MdN",
  "comparison_type": "adversarial",
  "comparison_context": "CT defends divine simplicity against MdN's parsimony criteria",
  "auditors": ["Claude", "Grok", "Nova"],
  "ticks": [
    {
      "tick_id": "tick-001",
      "timestamp": "2025-11-12T14:30:00Z",
      "nodes": [
        {
          "auditor": "Claude",
          "confidence": 0.85,
          "bias_overhead": 0.5,
          "stance": "PRO",
          "violation_flagged": false,
          "calibration": {
            "hash": "1bbec1e119a2c425",
            "mode": "calibrated_pro",
            "values": {
              "axiom_confidence": 0.85,
              "burden_of_proof": 0.40,
              "charity_interpretation": 0.90,
              "edge_case_weight": 0.30
            }
          }
        },
        {
          "auditor": "Grok",
          "confidence": 0.78,
          "bias_overhead": 0.4,
          "stance": "ANTI",
          "violation_flagged": false,
          "calibration": {
            "hash": "00cd73274759e218",
            "mode": "calibrated_anti",
            "values": {
              "axiom_confidence": 0.70,
              "burden_of_proof": 0.60,
              "charity_interpretation": 0.50,
              "edge_case_weight": 0.70
            }
          }
        },
        {
          "auditor": "Nova",
          "confidence": 0.92,
          "bias_overhead": 0.3,
          "stance": "FAIRNESS",
          "violation_flagged": false
        }
      ],
      "edges": [
        {
          "pair": "Claude-Grok",
          "tension": 0.65,
          "volume": 0.80,
          "notes": "BFI debate: divine simplicity measurement approach"
        },
        {
          "pair": "Claude-Nova",
          "tension": 0.25,
          "volume": 0.40,
          "notes": "Calibration transparency discussion"
        },
        {
          "pair": "Grok-Nova",
          "tension": 0.30,
          "volume": 0.45,
          "notes": "Empirical evidence standards"
        }
      ],
      "ethics": {
        "examined": ["transparency"],
        "deferred": [],
        "missing": ["stakeholder_impact"]
      },
      "convergence": {
        "percentage": 87.5,
        "percentage_include_crux": 75.0,
        "percentage_exclude_crux": 88.0,
        "metrics_agreed": ["CA", "IP", "ES", "LS", "MS"],
        "metrics_disputed": ["BFI", "PS"]
      },
      "crux_calculation_mode": "compare_both",
      "crux": {
        "status": "potential",
        "id": "CRUX_BFI_001",
        "description": "Divine simplicity measurement - fundamental disagreement on ontological parsimony",
        "affected_metrics": ["BFI"],
        "score_delta": {
          "metric": "BFI",
          "default_score": 8.5,
          "capped_score": 6.5,
          "delta": -2.0
        }
      }
    }
    // Additional ticks (tick-002, tick-003, etc.)
  ]
}
```

---

## 🔄 Data Flow

**Source of Truth:**
```
profiles/worldviews/*.md (12 worldview profiles)
         ↓
profiles/comparisons/*.yaml (66 comparison files)
         ↓
auditors/VUDU_logs/*.json (session tick data from Process Claude)
```

**Translation Layer:**
```
SMV_DATA_MAP.md (extraction logic)
         ↓
SMV Claude (data bridge specialist)
         ↓
scripts/smv_refresh.sh (automation)
```

**Generated Artifacts (this directory):**
```
docs/smv/live_data/*.json (66 visualization-ready files)
         ↓
SMV UI (triangle view, timeline, tension trace, Crux toggle)
```

---

## 🚫 What NOT to Do

**NEVER:**
- ❌ Manually edit these JSON files (they're generated—changes will be overwritten)
- ❌ Commit these files as source of truth (profiles are source of truth)
- ❌ Use these files for archival purposes (they're regenerated on-demand)
- ❌ Rely on stale data (always check `_meta.generated` timestamp)

**ALWAYS:**
- ✅ Regenerate via `scripts/smv_refresh.sh` when profiles change
- ✅ Trust SMV Claude's extraction logic (documented in SMV_DATA_MAP.md)
- ✅ Report schema violations to Nova (not SMV Claude's fault—schema may need evolution)
- ✅ Check provenance metadata (`_meta.source_files`) to understand data lineage

---

## 🔍 Staleness Detection

**How to know if data is stale:**

1. **Check `_meta.generated` timestamp:**
   ```bash
   cat CT_vs_MdN.json | jq '._meta.generated'
   # "2025-11-12T14:45:00Z"
   ```

2. **Compare against source file modification:**
   ```bash
   git log -1 --format="%ai" profiles/worldviews/CLASSICAL_THEISM.md
   # 2025-11-12 15:00:00 -0800
   # ^ Modified AFTER SMV JSON was generated = STALE
   ```

3. **Run freshness check:**
   ```bash
   python docs/smv/scripts/smv_freshness_check.py
   # Reports which comparisons are stale and why
   ```

**Auto-detection (Phase 2):**
- Doc Claude runs `smv_freshness_check.py` during Repo Health scans
- Reports staleness in Repo Health Dashboard
- User can trigger `smv_refresh.sh` on-demand

---

## 🔄 Regeneration Workflow

### **Manual Refresh (on-demand)**

```bash
# Regenerate all comparisons
cd docs/smv/scripts
./smv_refresh.sh

# Regenerate specific comparison
./smv_refresh.sh CT_vs_MdN
```

**When to use:**
- After modifying worldview profile (CLASSICAL_THEISM.md calibration YAML changed)
- After VUDU session completes (Process Claude exported new tick data)
- Before launching SMV UI (ensure fresh data)

---

### **Automated Refresh (Phase 2)**

**Trigger 1: Git hook (post-commit)**
```bash
# .git/hooks/post-commit
# If profiles/ changed, queue SMV refresh
if git diff --name-only HEAD~1 | grep -q "profiles/"; then
    python docs/smv/scripts/smv_freshness_check.py
    # (Optional: auto-refresh stale comparisons)
fi
```

**Trigger 2: Doc Claude Repo Health scan**
```bash
# Scheduled daily scan
python docs/smv/scripts/smv_freshness_check.py
# Report to Repo Health Dashboard
# User decides whether to run smv_refresh.sh
```

**Trigger 3: Process Claude VUDU handoff**
```bash
# After CT↔MdN pilot completes
python docs/smv/scripts/smv_export_session.py CT_vs_MdN_VUDU_20251112
# Automatically generates live_data/CT_vs_MdN.json
```

---

## 📐 Provenance Metadata

**Every JSON file includes `_meta` block:**

| Field | Purpose | Example |
|-------|---------|---------|
| `generated` | Timestamp of SMV export | `"2025-11-12T14:45:00Z"` |
| `smv_schema_version` | Which schema version used | `"1.1.0"` |
| `source_files` | Array of source profile paths | `["profiles/worldviews/CLASSICAL_THEISM.md", ...]` |
| `calibration_hashes` | SHA-256 hashes of YAML blocks | `{"pro_ct": "1bbec1e119a2c425", ...}` |
| `data_map_version` | Which SMV_DATA_MAP.md used | `"1.0.0"` |

**Why Provenance Matters:**
- **Audit trail:** Know exactly which files contributed to visualization
- **Hash verification:** Detect stale calibration data (hash mismatch = profile changed)
- **Schema evolution:** Track which SMV schema version generated this data
- **Debugging:** If visualization looks wrong, check source files for errors

---

## 🎯 Git Strategy

**Option A: .gitignore live_data/*.json (regeneration-on-demand)**

**Pros:**
- No commit noise (files change frequently)
- Forces fresh regeneration (no stale data risk)
- Smaller repo size

**Cons:**
- Requires regeneration after clone (setup step)
- No historical snapshots (can't compare old vs new)

**Option B: Commit live_data/*.json with provenance metadata**

**Pros:**
- Historical snapshots (compare CT_vs_MdN.json across commits)
- Ready-to-use after clone (no regeneration needed)
- Archival value (see how visualizations evolved)

**Cons:**
- Commit noise (files change after every VUDU session)
- Potential for stale data (if someone forgets to regenerate)
- Larger repo size (66 JSON files × versions)

**Recommendation (Phase 2 decision):** Start with Option A (.gitignore), evaluate after pilot completes. Shaman Claude can advise on archival strategy.

---

## 📊 Coverage Tracking

**Current Status:** 0/66 comparisons (Phase 2 awaiting CT↔MdN pilot)

**Pilot Milestone:** 1/66 (CT_vs_MdN.json generated after pilot session)

**Full Coverage Goal:** 66/66 (all worldview pairings scored and exported)

**Check Coverage:**
```bash
# Count JSON files (excluding README.md)
ls -1 docs/smv/live_data/*.json 2>/dev/null | wc -l
# Expected: 66 (when all VUDU sessions complete)
```

---

## 🤝 Trinity Handoffs

### **Process Claude → SMV Claude**
**When:** After VUDU session completes
**What:** VUDU tick data (tension, volume, convergence, Crux) in SMV schema format
**Where:** Process Claude exports to `auditors/VUDU_logs/`, SMV Claude merges with profiles

### **SMV Claude → Doc Claude**
**When:** After data refresh
**What:** Staleness report for Repo Health Dashboard (coverage, compliance, freshness)

### **SMV Claude → Logger Claude**
**When:** After any operation (freshness check, refresh, validation)
**What:** Session log (what changed, why, success/failure status)

---

## 📚 References

- **Data Mapping Logic:** [docs/smv/SMV_DATA_MAP.md](../SMV_DATA_MAP.md)
- **Schema Definition:** [docs/smv/SMV_DESIGN_SPEC.md](../SMV_DESIGN_SPEC.md) (v1.1)
- **SMV Claude Role:** [docs/smv/ROLE_SMV_CLAUDE.md](../ROLE_SMV_CLAUDE.md)
- **Trinity Architecture:** [docs/architecture/TRINITY_ARCHITECTURE.md](../../architecture/TRINITY_ARCHITECTURE.md)
- **Process Claude Domain 7:** [docs/repository/librarian_tools/ROLE_PROCESS.md](../../repository/librarian_tools/ROLE_PROCESS.md) (lines 905-1128)

---

**Created by:** SMV Claude (B-STORM_6 infrastructure setup)
**Date:** 2025-11-11
**Status:** Placeholder (Phase 2 ready)
**Next Steps:** Await CT↔MdN pilot completion → first VUDU export → CT_vs_MdN.json generated

**Derived, Not Duplicated. Fresh, Not Frozen. Generated, Not Canonical.** 🔄✨
