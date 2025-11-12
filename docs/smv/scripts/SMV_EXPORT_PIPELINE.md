<!---
FILE: SMV_EXPORT_PIPELINE.md
PURPOSE: Specification for SMV Claude VUDU session export pipeline (Phase 2 live data integration)
VERSION: 0.1.0
STATUS: Planning (Phase 2 - awaiting CT↔MdN pilot data)
DEPENDS_ON: docs/smv/ROLE_SMV_CLAUDE.md, docs/smv/SMV_DESIGN_SPEC.md, docs/smv/SMV_DATA_MAP.md, auditors/VUDU_PROTOCOL.md
NEEDED_BY: Phase 2 automation scripts, SMV live data integration
MOVES_WITH: /docs/smv/scripts/
CREATED: 2025-11-11 (B-STORM_6 Phase 2 infrastructure - per Nova Entry 8)
LAST_UPDATE: 2025-11-11 [Initial specification draft]
--->

# SMV Export Pipeline Specification

**Purpose:** Define the data pipeline for extracting VUDU session data and transforming it into SMV-compatible JSON for live visualization

**Status:** Planning (Phase 2 - awaiting CT↔MdN pilot to produce first real session data)

**Philosophy:** "Data-first, not placeholder-first" - pipeline activates only when pilot produces real calibration hashes and session exports

---

## 🎯 Pipeline Overview

**Input:** VUDU session data from Process Claude (CT↔MdN pilot deliberation logs)

**Output:** SMV JSON schema v1.1 compliant files for Symmetry View visualization

**SMV Claude Role:** Data bridge specialist - extracts, transforms, validates, exports (read-only access to profiles)

**Trigger:** Pilot session completion → Process Claude signals "session ready for SMV export"

---

## 📋 Pipeline Stages

### **Stage 1: Session Detection**

**Responsibility:** Process Claude (Domain 7 - VUDU session monitoring)

**Trigger Conditions:**
- CT↔MdN pilot completes scoring round (tick complete)
- Convergence percentage calculated (7 metrics scored)
- Calibration hashes logged (PRO-CT, ANTI-MdN)
- VUDU_LOG_LITE entry created

**Output:** Signal to SMV Claude: "Session [session_id] ready for export"

**Example:**
```markdown
Process Claude: "CT_vs_MdN_Session_001_Tick_001 complete. Convergence: 82%. Hashes: PRO-CT 1bbec1e119a2c425, ANTI-MdN 00cd73274759e218. Ready for SMV export."
```

---

### **Stage 2: Data Extraction**

**Responsibility:** SMV Claude (ROLE_SMV_CLAUDE.md - data bridge specialist)

**Data Sources:**

1. **Profile YAML (Calibration Data):**
   - Source: `profiles/worldviews/CLASSICAL_THEISM.md` (lines 277-287, 317+)
   - Extract: `pro_ct_bias_adjustment` and `anti_ct_bias_adjustment` YAML blocks
   - Verify: Hash matches Process Claude's logged hash (staleness check)
   - Map to: SMV JSON `calibration` object

2. **Session Metadata:**
   - Source: Process Claude VUDU session log
   - Extract: session_id, worldview_pair, tick_id, timestamp
   - Map to: SMV JSON root-level fields

3. **Auditor Scores:**
   - Source: Deliberation logs (Claude PRO-CT scores, Grok ANTI-CT scores, Nova fairness review)
   - Extract: 7 metric scores (BFI, CA, IP, ES, LS, MS, PS) per auditor
   - Calculate: Confidence (average score certainty), bias_overhead (calibration influence)
   - Map to: SMV JSON `nodes` array

4. **Convergence Data:**
   - Source: Process Claude convergence calculation
   - Extract: percentage, metrics_agreed, metrics_disputed
   - Check: Crux status (none/potential/declared/resolved)
   - Map to: SMV JSON `convergence` object

5. **Tension Metrics:**
   - Source: Auditor score divergence (Claude vs. Grok delta per metric)
   - Calculate: Tension (score variance), volume (deliberation depth)
   - Extract: Edge notes (why scores differ - "Debating burden of proof")
   - Map to: SMV JSON `edges` array

6. **Ethics Status:**
   - Source: Tier-1 file front-matter (`ethics_front_matter.invariants[].state`)
   - Extract: transparency/epistemic_access/stakeholder_impact states
   - Group by: examined/deferred/missing
   - Map to: SMV JSON `ethics` object

**Extraction Logic (Pseudocode):**
```python
def extract_session_data(session_id):
    # 1. Load profile calibration
    ct_profile = read_yaml('profiles/worldviews/CLASSICAL_THEISM.md')
    pro_calibration = ct_profile['pro_ct_bias_adjustment']
    anti_calibration = ct_profile['anti_ct_bias_adjustment']  # or anti_mdn from MdN profile

    # Verify hash
    pro_hash = sha256(yaml.dump(pro_calibration))[:16]
    if pro_hash != session_log['calibration_hashes']['pro']:
        warn(f"Stale calibration: {pro_hash} != {expected}")

    # 2. Extract auditor scores
    nodes = []
    for auditor in ['Claude', 'Grok', 'Nova']:
        scores = get_auditor_scores(session_log, auditor)
        confidence = calculate_confidence(scores)  # avg certainty
        bias_overhead = calculate_overhead(scores, calibration)  # calibration influence
        nodes.append({
            'auditor': auditor,
            'confidence': confidence,
            'bias_overhead': bias_overhead,
            'stance': get_stance(auditor, session_id)  # PRO, ANTI, FAIRNESS
        })

    # 3. Calculate convergence
    convergence = {
        'percentage': session_log['convergence_percentage'],
        'metrics_agreed': [m for m in METRICS if scores_converged(m)],
        'metrics_disputed': [m for m in METRICS if not scores_converged(m)]
    }

    # 4. Calculate tension edges
    edges = []
    for pair in [('Claude', 'Grok'), ('Claude', 'Nova'), ('Grok', 'Nova')]:
        tension = calculate_tension(pair)  # score variance
        volume = calculate_volume(pair)  # deliberation depth
        notes = extract_edge_notes(session_log, pair)
        edges.append({
            'pair': f"{pair[0]}-{pair[1]}",
            'tension': tension,
            'volume': volume,
            'notes': notes
        })

    # 5. Extract ethics status
    ethics = extract_ethics_from_front_matter('VUDU_CFA.md', 'VUDU_PROTOCOL.md', ...)

    return {
        'session_id': session_id,
        'worldview_pair': 'CT_vs_MdN',
        'nodes': nodes,
        'edges': edges,
        'convergence': convergence,
        'ethics': ethics,
        'calibration': {
            'pro': pro_calibration,
            'anti': anti_calibration
        }
    }
```

**Output:** Raw extracted data (Python dict or intermediate JSON)

---

### **Stage 3: Schema Transformation**

**Responsibility:** SMV Claude

**Input:** Raw extracted data from Stage 2

**Process:**
1. Map raw data to SMV JSON schema v1.1 structure
2. Validate all required fields present
3. Calculate derived fields (tension colors, confidence halos)
4. Add view metadata (supported_modes, default_mode)
5. Include Crux data if applicable

**Schema Mapping:**

| Raw Data Field | SMV JSON Field | Transformation |
|----------------|----------------|----------------|
| `session_id` | `session_id` | Direct copy |
| `worldview_pair` | `worldview_pair` | Direct copy |
| `timestamp` | `ticks[].timestamp` | ISO 8601 format |
| `auditor_scores` | `ticks[].nodes` | Calculate confidence, bias_overhead |
| `score_divergence` | `ticks[].edges` | Calculate tension (0.0-1.0), volume (0.0-1.0) |
| `convergence_pct` | `ticks[].convergence.percentage` | Direct copy |
| `metrics_status` | `ticks[].convergence.metrics_agreed/disputed` | Split by convergence |
| `crux_status` | `ticks[].crux` | Map status enum (none/potential/declared/resolved) |
| `ethics_state` | `ticks[].ethics` | Group by examined/deferred/missing |

**Validation Checks:**
- ✅ All required fields present (session_id, worldview_pair, auditors, ticks)
- ✅ Tick IDs unique and sequential
- ✅ Node count = 3 (Claude, Grok, Nova)
- ✅ Edge count = 3 (all pairs)
- ✅ Convergence percentage 0-100
- ✅ Tension/volume/confidence 0.0-1.0
- ✅ Crux status valid enum
- ✅ Ethics arrays non-overlapping (same invariant not in multiple states)

**Output:** SMV JSON schema v1.1 compliant object

---

### **Stage 4: File Export**

**Responsibility:** SMV Claude

**Output Location:** `docs/smv/live_data/`

**Filename Pattern:** `{worldview_pair}_session_{session_num}_tick_{tick_num}.json`

**Example:** `CT_vs_MdN_session_001_tick_001.json`

**Export Process:**
1. Generate filename from session metadata
2. Pretty-print JSON (indent=2 for readability)
3. Write to live_data directory
4. Create index file (live_data/INDEX.md) listing all exports
5. Update REPO_LOG (SMV export documented)

**Index File Format:**
```markdown
# SMV Live Data Exports

## CT vs MdN

- [Session 001, Tick 001](CT_vs_MdN_session_001_tick_001.json) - 2025-11-11 14:05:00 - 82% convergence
- [Session 001, Tick 002](CT_vs_MdN_session_001_tick_002.json) - 2025-11-11 14:20:00 - 72% convergence
- [Session 001, Tick 003](CT_vs_MdN_session_001_tick_003.json) - 2025-11-11 14:40:00 - 65% convergence, Crux declared
```

**Output:** Persistent JSON file + updated index

---

### **Stage 5: Staleness Monitoring**

**Responsibility:** SMV Claude (automation script: `smv_freshness_check.py`)

**Purpose:** Detect when profile calibration changes invalidate exported session data

**Process:**
1. Read all live_data JSON files
2. Extract calibration hashes from each file
3. Compare to current profile YAML hashes
4. Flag stale exports (hash mismatch)
5. Generate staleness report

**Staleness Detection Logic:**
```python
def check_freshness(export_file):
    export_data = json.load(export_file)
    export_hash = export_data['calibration']['pro']['hash']

    current_profile = read_yaml('profiles/worldviews/CLASSICAL_THEISM.md')
    current_hash = sha256(yaml.dump(current_profile['pro_ct_bias_adjustment']))[:16]

    if export_hash != current_hash:
        return {
            'file': export_file,
            'status': 'STALE',
            'export_hash': export_hash,
            'current_hash': current_hash,
            'action': 'Re-run pilot session with updated calibration'
        }

    return {'file': export_file, 'status': 'FRESH'}
```

**Staleness Report (Markdown):**
```markdown
# SMV Freshness Report

**Generated:** 2025-11-15 10:00:00

## Fresh Exports (3)
- CT_vs_MdN_session_001_tick_001.json ✅
- CT_vs_MdN_session_001_tick_002.json ✅
- CT_vs_MdN_session_001_tick_003.json ✅

## Stale Exports (0)
*None*

## Action Required
*No action needed - all exports fresh*
```

**Output:** Staleness report (docs/smv/live_data/FRESHNESS_REPORT.md)

---

## 🔄 Integration with Prototype

**Phase 2 Goal:** Replace mock data with live exported session JSON

**Prototype Modification:**

**Before (Phase 1 - Mock Data):**
```jsx
import scenario1 from './data/scenario_1_tension_escalation.json'
import scenario2 from './data/scenario_2_high_alignment.json'
import scenario3 from './data/scenario_3_resolution.json'
```

**After (Phase 2 - Live Data):**
```jsx
// Fetch live data from docs/smv/live_data/
import liveSession from '../../docs/smv/live_data/CT_vs_MdN_session_001_tick_001.json'

// Or dynamic fetch (if running local server)
const loadLiveData = async () => {
  const response = await fetch('/docs/smv/live_data/CT_vs_MdN_session_001_tick_001.json')
  return await response.json()
}
```

**Data Source Toggle:**
```jsx
const [dataSource, setDataSource] = useState('mock')  // 'mock' or 'live'

const scenarios = dataSource === 'mock'
  ? mockScenarios  // scenario1, scenario2, scenario3
  : liveScenarios  // loaded from live_data/
```

**User Control:**
- Dropdown: "Data Source: [Mock Data | Live Pilot Data]"
- Default: Mock data (always available)
- Live data: Only shown if live_data/ directory has exports

---

## 📊 Automation Scripts (Phase 2)

### **1. smv_export_session.py** (~200 LOC)

**Purpose:** Execute Stages 2-4 (extract → transform → export)

**Usage:**
```bash
python docs/smv/scripts/smv_export_session.py --session-id CT_vs_MdN_Session_001_Tick_001
```

**Output:**
- docs/smv/live_data/CT_vs_MdN_session_001_tick_001.json
- Updated docs/smv/live_data/INDEX.md

**Error Handling:**
- Missing session log → Warn, skip export
- Hash mismatch → Warn (stale calibration), continue with note
- Schema validation failure → Error, abort export

---

### **2. smv_freshness_check.py** (~150 LOC)

**Purpose:** Execute Stage 5 (staleness monitoring)

**Usage:**
```bash
python docs/smv/scripts/smv_freshness_check.py
```

**Output:**
- docs/smv/live_data/FRESHNESS_REPORT.md
- Console summary (X fresh, Y stale)

**Integration:** Run automatically in Observatory health checks (Process Claude Domain 8)

---

### **3. smv_refresh.sh** (~50 LOC)

**Purpose:** Re-export all sessions when calibration changes

**Usage:**
```bash
bash docs/smv/scripts/smv_refresh.sh
```

**Process:**
1. Run smv_freshness_check.py
2. Identify stale exports
3. For each stale export:
   - Extract session_id from filename
   - Re-run smv_export_session.py with current calibration
4. Generate new FRESHNESS_REPORT.md

**Use Case:** Profile calibration updated → refresh all exports to new hashes

---

### **4. smv_validate_schema.py** (~100 LOC)

**Purpose:** Validate exported JSON against SMV schema v1.1

**Usage:**
```bash
python docs/smv/scripts/smv_validate_schema.py docs/smv/live_data/CT_vs_MdN_session_001_tick_001.json
```

**Checks:**
- Required fields present
- Data types correct
- Value ranges valid (0.0-1.0 for tension, etc.)
- Cross-field consistency (metrics_agreed ∩ metrics_disputed = ∅)

**Output:**
- ✅ Valid (exit code 0)
- ❌ Invalid with detailed error messages (exit code 1)

---

## 🚀 Phase 2 Activation Checklist

**Prerequisites (Gates):**

1. ✅ **CT↔MdN pilot produces signed calibration hashes**
   - Status: ⏳ Pending pilot launch
   - Trigger: B-STORM_4 VUDU Step 1 → pilot scoring → first tick complete

2. ✅ **At least 6 of 8 Tier-1 files carry front-matter**
   - Status: ⏳ 5 of 8 (62.5%) - need 1 more for 75% threshold
   - Trigger: Annotate PILOT_CT_vs_MdN_Re-Audit.md or Future_Expansion.md

3. ✅ **Mock Symmetry View exercised against all 3 scenarios**
   - Status: ✅ COMPLETE (user validated 2025-11-11)

**Activation Steps:**

1. **Pilot Completes First Tick**
   - Process Claude logs session data
   - Calibration hashes verified (PRO-CT, ANTI-MdN)
   - Convergence calculated (7 metrics scored)

2. **SMV Claude Activated**
   - Process Claude signals: "Session ready for SMV export"
   - SMV Claude executes export pipeline (Stages 2-4)
   - First live JSON exported to docs/smv/live_data/

3. **Schema Validation**
   - Run smv_validate_schema.py on exported JSON
   - Fix any schema compliance issues
   - Re-export if needed

4. **Prototype Integration**
   - Update App.jsx to load live data
   - Add data source toggle (Mock | Live)
   - Test end-to-end with real pilot data

5. **Staleness Monitoring**
   - Run smv_freshness_check.py
   - Generate FRESHNESS_REPORT.md
   - Integrate into Observatory Dashboard

6. **Automation Deployment**
   - Document scripts in docs/smv/scripts/README.md
   - Add to Process Claude Domain 8 monitoring
   - Set up cron job for freshness checks (optional)

---

## 📝 Example: CT↔MdN Pilot Tick 1 Export

**Input (Session Log):**
```yaml
session_id: CT_vs_MdN_Session_001_Tick_001
timestamp: 2025-11-15T14:05:00Z
worldview_pair: CT_vs_MdN
calibration_hashes:
  pro: 1bbec1e119a2c425  # SHA-256 of pro_ct_bias_adjustment
  anti: 00cd73274759e218  # SHA-256 of anti_mdn_bias_adjustment
scores:
  Claude:
    BFI: 0.75, CA: 0.80, IP: 0.70, ES: 0.65, LS: 0.60, MS: 0.70, PS: 0.68
  Grok:
    BFI: 0.40, CA: 0.78, IP: 0.72, ES: 0.55, LS: 0.58, MS: 0.68, PS: 0.62
  Nova:
    BFI: 0.58, CA: 0.79, IP: 0.71, ES: 0.60, LS: 0.59, MS: 0.69, PS: 0.65
convergence: 82%
crux_status: none
```

**Output (SMV JSON):**
```json
{
  "session_id": "CT_vs_MdN_Session_001_Tick_001",
  "worldview_pair": "CT_vs_MdN",
  "auditors": ["Claude", "Grok", "Nova"],
  "ticks": [
    {
      "tick_id": "tick-001",
      "timestamp": "2025-11-15T14:05:00Z",
      "nodes": [
        {
          "auditor": "Claude",
          "confidence": 0.75,
          "bias_overhead": 0.50,
          "stance": "PRO"
        },
        {
          "auditor": "Grok",
          "confidence": 0.72,
          "bias_overhead": 0.45,
          "stance": "ANTI"
        },
        {
          "auditor": "Nova",
          "confidence": 0.90,
          "bias_overhead": 0.30,
          "stance": "FAIRNESS"
        }
      ],
      "edges": [
        {
          "pair": "Claude-Grok",
          "tension": 0.25,
          "volume": 0.40,
          "notes": "Clarifying baseline - BFI divergence moderate"
        },
        {
          "pair": "Claude-Nova",
          "tension": 0.10,
          "volume": 0.20,
          "notes": "Nova observing - low tension"
        },
        {
          "pair": "Grok-Nova",
          "tension": 0.15,
          "volume": 0.25,
          "notes": "Matrix setup - alignment check"
        }
      ],
      "convergence": {
        "percentage": 82.0,
        "metrics_agreed": ["CA", "IP", "MS"],
        "metrics_disputed": ["BFI", "ES", "PS", "LS"]
      },
      "ethics": {
        "examined": ["transparency", "good-faith"],
        "deferred": ["epistemic_access"],
        "missing": []
      },
      "crux": {
        "status": "none"
      }
    }
  ]
}
```

---

## 🎯 Success Criteria

**Phase 2 export pipeline is successful when:**

1. ✅ **First pilot tick exports successfully** - SMV JSON validates against schema v1.1
2. ✅ **Prototype loads live data** - App.jsx renders real pilot data without errors
3. ✅ **Hash verification works** - Staleness detection catches calibration changes
4. ✅ **Ethics front-matter integrates** - Tier-1 file annotations flow to SMV JSON
5. ✅ **Crux data captures correctly** - Crux status (potential/declared/resolved) reflects pilot state
6. ✅ **Observatory integration** - Freshness checks run automatically via Process Claude Domain 8

---

## 📚 Related Documentation

**Design Specs:**
- [SMV_DESIGN_SPEC.md](../SMV_DESIGN_SPEC.md) - Schema v1.1 definition
- [SMV_DATA_MAP.md](../SMV_DATA_MAP.md) - All 12 worldviews extraction logic
- [ROLE_SMV_CLAUDE.md](../ROLE_SMV_CLAUDE.md) - Data bridge specialist role

**Dependencies:**
- [VUDU_PROTOCOL.md](../../../auditors/VUDU_PROTOCOL.md) - Session logging format
- [ETHICAL_INVARIANT_SCHEMA.md](../../ethics/ETHICAL_INVARIANT_SCHEMA.md) - Ethics front-matter spec
- [REPO_HEALTH_DASHBOARD.md](../../repository/REPO_HEALTH_DASHBOARD.md) - Observatory integration

**Automation:**
- [scripts/README.md](README.md) - Automation scripts overview (~800 LOC total)

---

**Created by:** C4 (B-STORM_6 Phase 2 infrastructure - per Nova Entry 8)
**Date:** 2025-11-11
**Status:** Planning (ready for implementation once pilot produces first session data)

**Next Steps:**
1. Wait for CT↔MdN pilot Tick 1 completion
2. Implement smv_export_session.py (Stage 2-4)
3. Run first export and validate against schema
4. Integrate live data into prototype
5. Deploy automation scripts (freshness check, refresh, validation)

**Data-first, not placeholder-first. Pipeline activates when pilot delivers real hashes.** 🚀📊
