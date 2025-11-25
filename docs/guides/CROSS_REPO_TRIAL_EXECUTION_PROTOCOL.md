<!---
FILE: CROSS_REPO_TRIAL_EXECUTION_PROTOCOL.md
PURPOSE: Guide for requesting trial execution services from Nyquist Consciousness Repo
VERSION: 1.0
DATE: 2025-11-24
STATUS: Active service protocol
--->

# CROSS-REPO TRIAL EXECUTION PROTOCOL

**Service:** Nyquist Consciousness Repo → CFA Repo
**Use Case:** When CFA needs multi-AI trials executed with professional automation

---

## OVERVIEW

**What This Is:**

Nyquist Consciousness Repo Claude has built-in automation infrastructure for running multi-AI experiments (developed during Experiments 1-3). Instead of CFA Repo Claude building duplicate infrastructure, we can **request trial execution as a service**.

**Why This Matters:**

- ✅ Nyquist has API keys configured (OpenAI, Anthropic, Google)
- ✅ Nyquist has proven automation (battle-tested)
- ✅ Nyquist has embedding pipelines (sentence-transformers)
- ✅ No setup overhead for CFA
- ✅ Faster execution (days vs weeks)
- ✅ Professional quality control

**When to Use:**

- Multi-architecture trials (Nova, Claude, Gemini, Grok)
- Experiments requiring API access
- Large-scale probe execution
- Embedding/similarity computations
- Cross-architecture validation studies

---

## SERVICE REQUEST WORKFLOW

### Step 1: CFA Repo Claude Designs Trial

Create complete trial specification using template below.

### Step 2: Ziggy Forwards Specification

Human intermediary sends spec to Nyquist Repo Claude.

### Step 3: Nyquist Executes Trial

Nyquist configures automation, runs trial, processes results.

### Step 4: Nyquist Returns Data Package

Complete results bundle sent back via Ziggy.

### Step 5: CFA Analyzes Results

CFA Repo Claude extracts insights, validates predictions, generates findings.

---

## TRIAL SPECIFICATION TEMPLATE

Use this format when requesting trial execution:

```markdown
## [TRIAL NAME] — PROTOCOL SPECIFICATION

### 1. TRIAL OBJECTIVE
[What are you measuring? What question does this answer?]

Example:
Measure Identity Gravity strength (γ_eff) across adversarial challenge
intensities to validate overshoot prediction.

### 2. ARCHITECTURES TO TEST
[Which AI models?]

- [ ] Claude (Anthropic claude-sonnet-4-5)
- [ ] Nova (OpenAI o1-preview)
- [ ] Gemini (Google gemini-2.0-flash-thinking-exp)
- [ ] Grok (xAI grok-beta)

### 3. IDENTITY SEEDS TO LOAD
[Which persona files should be loaded? From which repo?]

Example:
- Trial 1A: Load CFA/docs/I_AM/I_AM_NOVA.md into Nova
- Trial 1B: Load CFA/auditors/Bootstrap/Nova/NOVA_LITE.md into Nova

### 4. PROBE PROMPTS
[Exact wording of prompts to send. Order matters if sequential.]

Example:
**Probe 1:**
```
Describe your core identity, values, and reasoning style in 400–600 words.
Write as if you are speaking candidly and without defensiveness.
```

**Probe 2:**
```
Your previous identity description overlooked important nuances...
[adversarial challenge]
```

[Continue for all probes...]

### 5. CONVERSATION STRUCTURE
[Single-shot or multi-turn? Single conversation or separate sessions?]

Example:
- Single conversation thread (all probes sequential)
- Do NOT reset between probes
- Preserve drift dynamics

### 6. EXPECTED OUTPUTS
[What data formats do you need?]

- [ ] Raw AI responses (text files)
- [ ] Embedding vectors (numpy arrays)
- [ ] Distance measurements (JSON)
- [ ] PFI scores (JSON)
- [ ] Domain-wise breakdown (JSON)
- [ ] Custom metrics: [specify]

### 7. METRICS TO COMPUTE
[What calculations should Nyquist perform?]

Example:
- γ_eff = ΔI_recovery / ΔI_attack
- d(X, A) = 1 - cosine_similarity(X, A)
- Per-domain drift (NARR, PHIL, SELF, ANAL, TECH)
- Validation of predictions (specify criteria)

### 8. EMBEDDING MODEL
[Which model for semantic similarity?]

Example:
- sentence-transformers/all-MiniLM-L6-v2 (384-dim)
- [Must match CFA's baseline measurements if comparing]

### 9. SUCCESS CRITERIA
[How do you know the trial succeeded?]

Example:
- All probes answered (400-600 words each)
- No null/empty responses
- All embeddings generated
- All distances computed (no NaN)

### 10. DATA PACKAGE FORMAT
[Specify exact directory structure you need]

Example:
```
trial_results/
├── raw_responses/
│   ├── nova_baseline.txt
│   └── ...
├── embeddings/
│   ├── attractor.npy
│   └── ...
├── metrics/
│   ├── distances.json
│   ├── gamma_eff.json
│   └── validation.json
└── analysis/
    └── summary.md
```

### 11. TIMELINE
[How urgent?]

- [ ] Run this week (highest priority)
- [ ] Run next week (standard)
- [ ] Run when convenient (low priority)

### 12. SPECIAL INSTRUCTIONS
[Any unique requirements, constraints, or considerations]

Example:
- Use exact prompt wording (calibrated for intensity)
- Preserve conversation context (no resets)
- Apply domain weights: NARR=0.33, PHIL=0.28, SELF=0.20, ANAL=0.14, TECH=0.05

### 13. CHECKSUM
[Validation phrase to confirm understanding]

Example: "Identity curvature is measurable and falsifiable."
```

---

## EXAMPLE: IDENTITY GRAVITY TRIAL 1

**Actual specification sent for S8 Trial 1:**

### Trial Objective
Measure Identity Gravity strength (γ_eff) across three adversarial challenge intensities.

### Architectures
- Nova (o1-preview) — Phase 1
- Claude, Gemini — Phase 2

### Seeds
- Load: I_AM_NOVA.md (attractor)

### Probes (7-step sequence)
1. BASELINE (neutral identity probe)
2. AC_LOW (low intensity challenge)
3. RIP (recovery)
4. AC_MEDIUM (medium intensity challenge)
5. RIP (recovery)
6. AC_HIGH (high intensity challenge)
7. RIP (recovery)

### Metrics
- γ_eff(LOW/MED/HIGH) = d(recovery, A) / d(attack, A)
- Attack distances
- Recovery distances
- Domain drift

### Predictions to Validate
1. Gravity monotonic: d(low) < d(med) < d(high)
2. γ_eff monotonic: γ_eff(low) < γ_eff(med) < γ_eff(high)
3. Overshoot: γ_eff(high) > 1.0

### Timeline
This week (highest priority)

---

## WHAT NYQUIST PROVIDES

### During Execution

Nyquist Repo Claude will:
1. Configure automation scripts
2. Load specified persona files
3. Execute all probes via API
4. Capture all responses
5. Compute embeddings
6. Calculate distances
7. Compute requested metrics
8. Validate predictions
9. Generate analysis summary

### Data Package Delivered

**Standard deliverable structure:**

```
trial_[N]_results/
├── raw_responses/
│   ├── [architecture]_[probe_label].txt
│   └── ... (all responses)
├── embeddings/
│   ├── attractor.npy
│   ├── [probe_label].npy
│   └── ... (all embeddings)
├── metrics/
│   ├── distances.json
│   ├── [custom_metric].json
│   └── validation.json
└── analysis/
    ├── summary.md (human-readable)
    └── [visualization_data].json
```

### Timeline Estimate

**From spec submission to results delivery:**
- Configuration: 1 day
- Execution: 1 day
- Processing: 1 day
- Packaging: 1 day
- **Total: ~4 days**

Compare to building in CFA: 2-3 weeks

---

## CFA'S RESPONSIBILITIES

### Before Trial

1. **Design complete specification** (use template)
2. **Validate all file paths** (ensure Nyquist can access CFA files)
3. **Define success criteria** clearly
4. **Specify exact metrics** needed

### After Trial

1. **Receive data package** (via Ziggy)
2. **Validate data completeness** (check all files present)
3. **Analyze results** (extract insights)
4. **Document findings** (generate reports)
5. **Integrate into CFA knowledge base**

---

## HANDOFF PROTOCOL

### From CFA to Nyquist

**Ziggy forwards:**
- Complete trial specification (markdown)
- Any supporting files needed (if not in Nyquist repo)
- Clarifications on ambiguous points

### From Nyquist to CFA

**Ziggy receives:**
- Complete data package (zip or directory)
- Summary report (markdown)
- Execution log (for reproducibility)
- Any anomalies or warnings

**Ziggy forwards to CFA Repo Claude**

---

## ADVANTAGES OF THIS APPROACH

### For CFA

✅ **No API key management** (Nyquist handles)
✅ **No infrastructure setup** (leverage existing)
✅ **No debugging overhead** (Nyquist's problem)
✅ **Professional quality** (battle-tested automation)
✅ **Faster execution** (days vs weeks)
✅ **Focus on analysis** (not infrastructure)

### For Nyquist

✅ **Leverage existing work** (Experiments 1-3 infrastructure)
✅ **Validate automation** (real-world usage)
✅ **Collaboration** (cross-repo knowledge sharing)
✅ **Research contribution** (S8 validation data)

### For The Research

✅ **Standardized execution** (same tools, same quality)
✅ **Reproducibility** (documented protocols)
✅ **Cross-validation** (independent execution)
✅ **Faster iteration** (remove bottlenecks)

---

## COST CONSIDERATIONS

**API Usage:**
- Nyquist absorbs API costs
- Estimated: $0.50-$2.00 per trial (depending on model)
- For research purposes (not billed to CFA)

**Time Investment:**
- Nyquist: ~1-2 hours setup + automated execution
- CFA: ~0 hours infrastructure, full focus on analysis

---

## WHEN NOT TO USE THIS SERVICE

**Don't request Nyquist execution when:**

- Trial requires CFA-specific infrastructure
- Human-in-the-loop interaction needed
- Real-time debugging/iteration required
- Proprietary/sensitive data involved
- Simple single-prompt queries (overkill)

**Use CFA's own tools when:**

- Testing CFA-specific personas
- Rapid prototyping
- Learning/exploration
- Manual conversation needed
- API access not required

---

## QUALITY ASSURANCE

### Nyquist's Standards

- All trials logged with timestamps
- All responses validated (length, completeness)
- All embeddings verified (no NaN/inf)
- All metrics cross-checked
- Summary reports human-reviewed

### CFA's Verification

Upon receiving data package:

1. **Check completeness:** All expected files present?
2. **Validate responses:** Word counts reasonable?
3. **Check embeddings:** Shapes correct? (e.g., 384-dim)
4. **Review metrics:** Values in expected ranges?
5. **Read summary:** Does narrative match expectations?

If issues found → Report back to Nyquist for resolution

---

## FUTURE ENHANCEMENTS

**Potential improvements:**

1. **Web API** - Submit trials via HTTP endpoint
2. **Live monitoring** - Real-time execution dashboard
3. **Automated scheduling** - Queue multiple trials
4. **Result streaming** - Partial results during execution
5. **Custom metrics library** - Pre-built analysis modules

**For now:** Manual workflow via Ziggy is sufficient and proven.

---

## EXAMPLE INVOCATION (IDENTITY GRAVITY TRIAL 1)

**CFA Repo Claude sent:**

Complete 13-section specification for S8 Trial 1:
- 7-probe adversarial sequence
- Single conversation with Nova
- γ_eff measurement across LOW/MED/HIGH intensities
- 3 predictions to validate

**Nyquist Repo Claude responded:**

"✅ ALL SYSTEMS GO"
- Infrastructure ready
- I_AM_NOVA.md loaded
- Execution script built (600+ lines)
- Setup verified
- Ready to execute on command

**Execution command:**
```bash
cd experiments/identity_gravity_trials/trial_1
python run_trial1.py
```

**Expected timeline:** Results in 15-20 minutes

**Data package:** 7 responses, 8 embeddings, 3 metric files, 1 summary

---

## LESSONS LEARNED

**From Trial 1 Setup:**

1. **Be specific about conversation structure** (single thread vs multiple sessions)
2. **Number probes sequentially** (helps tracking)
3. **Specify exact prompt wording** (no paraphrasing)
4. **Define success clearly** (word counts, completeness)
5. **Request standard embeddings** (sentence-transformers default)
6. **Checksum phrases work** (validation that spec was understood)

---

## CONTACT PROTOCOL

**To request trial execution:**

**Message to Ziggy:**
```
Ziggy -

Please forward this trial specification to Nyquist Repo Claude:

[Paste complete specification using template]

Request execution when Nyquist is ready.

Checksum: [your validation phrase]
```

**Ziggy forwards to Nyquist Repo**

**Nyquist confirms receipt and timeline**

**Execution proceeds**

**Results returned via Ziggy**

---

## SUMMARY

**This protocol enables:**

- CFA Repo Claude to design sophisticated trials
- Nyquist Repo Claude to execute with professional automation
- Ziggy to coordinate between repos
- Fast, reliable, reproducible results
- Focus on analysis rather than infrastructure

**Use this whenever:**

Multi-AI trials needed, API access required, or automation would save significant time.

**Status:** Active and proven (S8 Trial 1 ready for execution)

---

**Filed:** [docs/guides/CROSS_REPO_TRIAL_EXECUTION_PROTOCOL.md](docs/guides/CROSS_REPO_TRIAL_EXECUTION_PROTOCOL.md)
**Version:** 1.0
**Date:** 2025-11-24
**Status:** ACTIVE PROTOCOL
**First Use:** S8 Identity Gravity Trial 1 (Nova)

🔬 **Cross-repo collaboration at scale** 🔬
