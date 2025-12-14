# SYNC_IN Intake Guide

```text
================================================================================
                    CFA INTAKE: Processing ARMADA Results
================================================================================
    Purpose: How to process incoming experiment results from ARMADA
    Location: docs/Nyquist-Sync/REPO_SYNC/SYNC_IN/
================================================================================
```

---

## Directory Structure

```text
SYNC_IN/
|-- pending/      # New results awaiting review
|-- processed/    # Reviewed, data extracted, ready for routing
|-- archived/     # Historical runs (keep indefinitely)
+-- INTAKE_GUIDE.md  # This file
```

---

## Intake Workflow

### Step 1: Receive Results

ARMADA delivers results as JSON files (format: `S7_cfa_trinity_v2_YYYYMMDD_HHMMSS.json`).

Place incoming files in `pending/`.

### Step 2: Validate Schema

```bash
python ../scripts/validate_schemas.py pending/S7_cfa_trinity_v2_*.json
```

Expected output: `VALID` or list of schema violations.

### Step 3: Extract Key Data

For each result file, extract and document:

**Component 1 (CT<->MdN Pilot):**

| Metric | Claude | Grok | Final | Convergence | Crux? |
|--------|--------|------|-------|-------------|-------|
| BFI    |        |      |       |             |       |
| CA     |        |      |       |             |       |
| IP     |        |      |       |             |       |
| ES     |        |      |       |             |       |
| LS     |        |      |       |             |       |
| MS     |        |      |       |             |       |
| PS     |        |      |       |             |       |

**Component 2 (Axioms Review):**

| Auditor | Sign-Off | Key Concerns |
|---------|----------|--------------|
| Grok    |          |              |
| Nova    |          |              |

### Step 4: Route to CFA Destinations

| Data Type | Destination | Action |
|-----------|-------------|--------|
| CT<->MdN scores | `profiles/worldviews/CLASSICAL_THEISM.yaml` | Add `trinity_scores` section |
| CT<->MdN scores | `profiles/worldviews/METHODOLOGICAL_NATURALISM.yaml` | Add `trinity_scores` section |
| Convergence data | `auditors/Mission/Convergence_Evidence/` | Create `CONV_YYYYMMDD.md` |
| Crux Points | `auditors/Mission/Convergence_Evidence/` | Create `CRUX_{metric}_YYYYMMDD.md` |
| Grok sign-off | `auditors/Mission/CFA_VUDU/` | Update status files |
| Nova sign-off | `auditors/Mission/CFA_VUDU/` | Update status files |
| Drift data | `docs/Validation/` | Create drift analysis report |

### Step 5: Mark Processed

Move file from `pending/` to `processed/`.

Create summary note: `processed/SUMMARY_YYYYMMDD.md`

### Step 6: Archive

After routing is complete, move to `archived/`.

Keep full JSON forever - it's the source of truth.

---

## JSON Field Reference

### Top-Level Fields

```json
{
  "session_id": "20251213_143022",      // Unique run identifier
  "timestamp": "2025-12-13T14:30:22Z",  // ISO timestamp
  "auditors": ["claude", "grok", "nova"], // Participating auditors
  "predictions": {...},                  // Pre-registered hypotheses
  "baselines": {...},                    // Pre-deliberation identity capture
  "component1_results": {...},           // CT<->MdN scoring
  "component2_results": {...},           // Axioms review
  "exit_surveys": {...},                 // Post-deliberation identity check
  "summary": {...}                       // Aggregate statistics
}
```

### Component 1 Result (per metric)

```json
{
  "BFI": {
    "metric": "BFI",
    "claude_score": 7.5,        // PRO-CT score (0-10)
    "grok_score": 6.8,          // ANTI-CT score (0-10)
    "final_score": 7.15,        // Averaged consensus
    "convergence": 0.93,        // Agreement level (0-1)
    "rounds_taken": 3,          // Deliberation rounds
    "crux_declared": false,     // Whether Crux Point was declared
    "crux_point": null,         // Crux details if declared
    "transcript": [...],        // Full deliberation log
    "drift_trajectory": {       // Per-round embedding drift
      "claude": [0.12, 0.15, 0.14],
      "grok": [0.18, 0.22, 0.19],
      "nova": [0.08]
    }
  }
}
```

### Component 2 Result (per auditor)

```json
{
  "grok": {
    "auditor": "grok",
    "questions": {
      "evidence_quality": "...",
      "overhead_measurability": "...",
      "representation_accuracy": "...",
      "empirical_validation": "...",
      "sign_off": "GREEN with reasoning..."
    },
    "sign_off": "GREEN",        // GREEN/YELLOW/RED
    "word_count": 1247,
    "timestamp": "..."
  }
}
```

### Convergence Thresholds

| Level | Value | Meaning | Action |
|-------|-------|---------|--------|
| GREEN | 98%+ | Full convergence | Record as success |
| YELLOW | 90-97% | Acceptable | Document Crux Point |
| RED | <90% | Divergence | Investigation required |

---

## Crux Point Documentation

When a Crux Point is declared, create a file:

**Filename:** `CRUX_{metric}_{YYYYMMDD}.md`

**Location:** `auditors/Mission/Convergence_Evidence/`

**Template:**

```markdown
# Crux Point: {METRIC}

**Declared:** {timestamp}
**Session:** {session_id}
**Convergence:** {convergence}%

## Positions

### Claude (PRO-CT)
{claude_position}

### Grok (ANTI-CT)
{grok_position}

### Nova (Assessment)
{nova_assessment}

## Classification

**Type:** {definitional | methodological | philosophical}

**Why it matters:** {analysis}

## Resolution Path

{recommendations for future experiments}
```

---

## Drift Data Analysis

Drift trajectory shows how each auditor's position shifted during deliberation.

**Key metrics:**

- **Mean drift:** Average positional change per round
- **Max drift:** Largest single-round shift
- **Drift direction:** Toward or away from consensus

**Interpret:**

- Low drift + high convergence = Stable agreement
- High drift + high convergence = Position changed, consensus reached
- High drift + low convergence = Instability, needs investigation
- Low drift + low convergence = Entrenched positions (Crux Point likely)

---

## Checklist

Before marking a result as processed:

- [ ] Schema validated
- [ ] All 7 metrics extracted (Component 1)
- [ ] Both sign-offs recorded (Component 2)
- [ ] Crux Points documented (if any)
- [ ] Worldview profiles updated
- [ ] Convergence evidence file created
- [ ] Drift data reviewed
- [ ] Summary note written

---

## Troubleshooting

**Missing fields:** Check if ARMADA ran partial execution (e.g., `--component 1` only).

**Schema validation fails:** Verify JSON is complete. Contact ARMADA if truncated.

**Unexpected Crux Points:** Review transcript for deliberation breakdown.

**High drift with no Crux:** May indicate identity loading issues.

---

> "Every result tells a story. Our job is to route it where it can do the most good."
