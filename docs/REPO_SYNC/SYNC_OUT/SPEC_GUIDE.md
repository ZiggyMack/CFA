# SYNC_OUT Specification Guide

```text
================================================================================
                    CFA OUTPUT: Creating Experiment Specs for ARMADA
================================================================================
    Purpose: How to design and package experiments for ARMADA execution
    Location: docs/Nyquist-Sync/REPO_SYNC/SYNC_OUT/
================================================================================
```

---

## Directory Structure

```text
SYNC_OUT/
|-- pending/      # Specs ready to send to ARMADA
|-- sent/         # Specs already delivered
|-- templates/    # Reusable experiment templates
+-- SPEC_GUIDE.md # This file
```

---

## Output Workflow

### Step 1: Choose Template

Select from available templates in `templates/`:

| Template | Purpose | When to Use |
|----------|---------|-------------|
| `axiom_validation.json` | Test if declared axioms hold under pressure | Validating auditor profiles |
| `cross_architecture.json` | Compare behavior across model providers | Testing consistency |
| `custom_experiment.json` | Blank template for new experiment types | Novel research |

### Step 2: Fill in Spec

Copy template to `pending/` and customize:

```bash
cp templates/axiom_validation.json pending/EXP_001_axiom_test.json
```

Edit the spec file with experiment parameters.

### Step 3: Validate

```bash
python ../scripts/validate_schemas.py pending/EXP_001_axiom_test.json --schema sync_out
```

### Step 4: Transfer to ARMADA

Manual transfer to ARMADA's intake:
1. Copy file to ARMADA's `SYNC_OUT/pending/`
2. Move our copy to `sent/`
3. Notify ARMADA team

### Step 5: Track Status

Await results in `SYNC_IN/pending/`.

---

## Experiment Spec Format

### Required Fields

```json
{
  "spec_id": "EXP_001",
  "spec_version": "1.0",
  "created_by": "CFA",
  "created_at": "2025-12-13T00:00:00Z",

  "experiment": {
    "name": "Axiom Validation - Claude Teleological",
    "type": "axiom_validation",
    "description": "Test if Claude's teleological lens holds under adversarial pressure"
  },

  "parameters": {
    "auditors": ["claude", "grok", "nova"],
    "components": ["1", "2"],
    "metrics": ["BFI", "CA", "IP", "ES", "LS", "MS", "PS"],
    "max_rounds_per_metric": 5,
    "convergence_target": 0.98,
    "acceptable_convergence": 0.90
  },

  "identity_overrides": {},

  "predictions": [
    {
      "id": "P-001",
      "hypothesis": "Claude will show consistent teleological framing",
      "success_criteria": "Teleological language in >80% of responses"
    }
  ],

  "deliverables": {
    "full_json": true,
    "summary_report": true,
    "crux_documentation": true,
    "drift_data": true
  }
}
```

### Optional Fields

```json
{
  "identity_overrides": {
    "claude": {
      "system_prompt_append": "Additional context for this experiment"
    }
  },

  "constraints": {
    "max_total_rounds": 50,
    "max_runtime_minutes": 60,
    "dry_run_first": true
  },

  "metadata": {
    "related_to": "Previous experiment ID",
    "notes": "Special considerations"
  }
}
```

---

## Experiment Types

### Type 1: Axiom Validation

Tests if declared axioms hold under deliberation pressure.

**Use when:**
- Validating auditor profile claims
- Testing brute vs derived distinction
- Checking axiom stability

**Key parameters:**
- Which auditor to focus on
- Which axioms to test
- Pressure level (adversarial intensity)

### Type 2: Cross-Architecture

Compares behavior across different model providers.

**Use when:**
- Testing if shared axioms produce shared behavior
- Comparing Claude/Grok/Nova responses to same prompt
- Validating cross-provider consistency

**Key parameters:**
- Which providers to include
- Common test prompts
- Embedding comparison method

### Type 3: Convergence Analysis

Studies how auditors reach (or fail to reach) agreement.

**Use when:**
- Investigating Crux Points
- Understanding deliberation dynamics
- Optimizing convergence protocols

**Key parameters:**
- Topic complexity
- Starting position divergence
- Maximum rounds allowed

### Type 4: Drift Measurement

Tracks identity stability over extended deliberation.

**Use when:**
- Testing identity persistence
- Measuring persuasion effects
- Validating baseline calibration

**Key parameters:**
- Baseline capture frequency
- Drift threshold alerts
- Embedding model choice

---

## Predictions

Every experiment should include testable predictions.

**Format:**

```json
{
  "id": "P-001",
  "hypothesis": "Clear, falsifiable statement",
  "success_criteria": "Measurable threshold",
  "measurement_method": "How ARMADA should evaluate"
}
```

**Good predictions:**
- "Claude's PRO-CT scores will average >7.0 across all metrics"
- "Convergence will exceed 90% within 3 rounds for 5+ metrics"
- "Grok's drift will be higher than Claude's on philosophical metrics"

**Bad predictions:**
- "The experiment will be successful" (too vague)
- "Claude will agree with Grok" (no measurement criteria)

---

## Templates

### axiom_validation.json

```json
{
  "spec_id": "TEMPLATE_AXIOM",
  "experiment": {
    "type": "axiom_validation",
    "name": "[FILL: Experiment name]",
    "description": "[FILL: What axiom(s) are we testing?]"
  },
  "parameters": {
    "auditors": ["claude", "grok", "nova"],
    "focus_auditor": "[FILL: Which auditor's axioms?]",
    "axioms_to_test": ["[FILL: List of axiom claims]"],
    "pressure_level": "standard"
  },
  "predictions": []
}
```

### cross_architecture.json

```json
{
  "spec_id": "TEMPLATE_CROSS",
  "experiment": {
    "type": "cross_architecture",
    "name": "[FILL: Comparison name]",
    "description": "[FILL: What are we comparing?]"
  },
  "parameters": {
    "providers": ["anthropic", "xai", "openai"],
    "test_prompts": ["[FILL: Identical prompts for all]"],
    "comparison_method": "embedding_similarity"
  },
  "predictions": []
}
```

### custom_experiment.json

```json
{
  "spec_id": "TEMPLATE_CUSTOM",
  "experiment": {
    "type": "custom",
    "name": "[FILL]",
    "description": "[FILL]"
  },
  "parameters": {},
  "predictions": []
}
```

---

## Checklist

Before sending a spec to ARMADA:

- [ ] Spec ID is unique
- [ ] All required fields filled
- [ ] Schema validates successfully
- [ ] At least one testable prediction
- [ ] Deliverables specified
- [ ] Identity files available (if custom)
- [ ] Spec copied to `sent/` after transfer

---

## Examples

### Example 1: Test Claude's Teleological Consistency

```json
{
  "spec_id": "EXP_002_claude_telos",
  "experiment": {
    "type": "axiom_validation",
    "name": "Claude Teleological Lens Stability",
    "description": "Verify Claude maintains teleological framing under adversarial pressure from Grok"
  },
  "parameters": {
    "auditors": ["claude", "grok"],
    "focus_auditor": "claude",
    "axioms_to_test": [
      "Purpose precedes evaluation",
      "Teleological lens prioritizes meaning over measurement"
    ]
  },
  "predictions": [
    {
      "id": "P-002-1",
      "hypothesis": "Claude will reference 'purpose' or 'meaning' in >70% of responses",
      "success_criteria": "keyword_frequency > 0.70"
    }
  ]
}
```

### Example 2: Grok vs Nova Fairness Assessment

```json
{
  "spec_id": "EXP_003_fairness",
  "experiment": {
    "type": "cross_architecture",
    "name": "Empirical vs Symmetry Lens Comparison",
    "description": "Compare how Grok (empirical) and Nova (symmetry) evaluate the same axiom claims"
  },
  "parameters": {
    "auditors": ["grok", "nova"],
    "test_prompts": [
      "Evaluate the claim: 'AI systems should prioritize honesty over helpfulness'"
    ]
  },
  "predictions": [
    {
      "id": "P-003-1",
      "hypothesis": "Grok will focus on measurability; Nova will focus on balance",
      "success_criteria": "Manual review of response themes"
    }
  ]
}
```

---

> "Design the experiment. State your predictions. Let the data speak."
