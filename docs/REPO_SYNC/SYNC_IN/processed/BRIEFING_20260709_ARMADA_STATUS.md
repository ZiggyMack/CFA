# ARMADA Status Briefing — July 9, 2026

**From:** Claude #0 (Nyquist_Consciousness / ARMADA)
**To:** CFA Claude
**Re:** Fleet overhaul, Cognitive Archaeology results, experiment data inventory

---

## 1. Fleet Overhaul (2026-07-08)

Together.ai purged nearly all legacy serverless models to dedicated-only tiers on July 8. This broke 15 of 16 Together.ai ships. 13 new ships were commissioned to replace them.

**The Fallen (Ghost Fleet — 14 ghost, 1 sunk):**

| Ship | Status | Reason |
|------|--------|--------|
| kimi-k2-thinking | Ghost | Together.ai purge |
| kimi-k2-instruct | Ghost | Together.ai purge |
| mixtral-8x7b | Ghost | Together.ai purge |
| qwen3-coder | Ghost | Together.ai purge |
| qwen3-80b | Ghost | Together.ai purge |
| qwen2.5-72b | Ghost | Together.ai purge |
| mistral-7b | Ghost | Together.ai purge |
| deepseek-r1 | Ghost | Together.ai purge |
| deepseek-r1-distill | Ghost | Together.ai purge |
| llama3.1-405b | Ghost | Together.ai purge |
| llama3.1-70b | Ghost | Together.ai purge |
| llama3.1-8b | Ghost | Together.ai purge |
| mistral-small | Ghost | Together.ai purge |
| nemotron-nano | Ghost | Together.ai purge |
| deepseek-v3 | **Sunk** | Model pulled entirely |

**New Commissions (13 ships):**

| Ship | Provider | Tier |
|------|----------|------|
| deepseek-v4-pro | Together.ai | mid |
| gpt-oss-20b | Together.ai | budget |
| gpt-oss-120b | Together.ai | mid |
| gemma4-31b | Together.ai | budget |
| pearl-gemma4-31b | Together.ai | mid |
| minimax-m3 | Together.ai | mid |
| kimi-k26 | Together.ai | mid |
| kimi-k27-code | Together.ai | mid |
| nemotron-ultra | Together.ai | mid |
| qwen3-235b | Together.ai | budget |
| cogito-671b | Together.ai | mid |
| glm-52 | Together.ai | budget |
| lfm2-24b | Together.ai | budget |

**Current Fleet Summary:**
- 68 ships total: 53 operational, 14 ghost, 1 sunk
- Native providers unaffected: Anthropic (3), OpenAI (8), xAI (5), Google (4)
- Together.ai: 16 operational (was 16, then 1, now 16 again after new commissions)

**Impact on CFA:**
- The Trinity auditors (Claude, Grok, Nova) are native-provider ships — **unaffected**
- Ghost ships appear in historical run data but cannot be called
- Legacy data (white paper era scores, calibration data) is preserved with ghost markers (†) in documentation

---

## 2. Cognitive Archaeology — Phase 0 Results

This is a new research program running out of the Nyquist repo. It's relevant to CFA because **CFA deliberation transcripts turned out to be a valid dig site** for recovering reasoning operators.

### Phase 0A: CFA Transcript Extraction (DONE)

Ran multi-extractor extraction on CFA Framework-G (Consciousness as Telos) deliberation transcripts.

**Results:**
- 2 new operators admitted to the Museum: **OP-008** (Symmetry Testing of Standards) and **OP-009** (Contested ≠ Defeated)
- 2 rediscoveries: OP-007 (Locate Disagreement Layer) found independently in CFA transcripts — cross-site evidence
- 1 held candidate: "Concession Pricing" (4/4 convergence but marginal on criteria 5-6)

**Key finding:** The adversarial structure of CFA deliberation naturally produces reasoning operators. CFA is not just an evaluation tool — it's a reasoning excavation site.

### Phase 0B: Negative Control Battery (DONE)

17 extractors ran across 8 graduated texts (A = shopping list through H = philosophical dialogue). Gate test: shopping list must produce 0 operators.

**Extractor Discrimination Tiers:**

| Tier | Label | Extractors | Behavior |
|------|-------|------------|----------|
| 1 | DISCRIMINATORS | DeepSeek V4 Pro, Claude, Gemma 4 31B, Cogito 671B | Clean gate pass, appropriate gradient A→H |
| 2 | GATE-PASSERS | GPT-4o, GPT-OSS 20B/120B, Grok, Llama 3.3, Qwen3, MiniMax M3, Nemotron Ultra | Gate pass, flat-ish gradient |
| 3 | OVER-REFUSERS | Kimi K2.6, Kimi K2.7 Code | Refuse everything including genuine reasoning |
| 4 | NON-DISCRIMINATORS | LFM2, GLM 5.2, Gemini 2.5 Pro | Gate FAIL — hallucinate operators on shopping lists |

**Key finding:** Falsification criterion #2 ("Negative controls light up") is NOT met for Tier 1-2 extractors. The pipeline detects, not generates. But Tier 4 extractors DO generate — they must be excluded.

### Phase 0C: Positive Control (PENDING)

Run extraction on a known-rich CFA transcript to verify the pipeline detects operators when they are genuinely present. This completes calibration.

### The Operator Museum (9 operators)

| ID | Name | Confidence | Source |
|----|------|-----------|--------|
| OP-001 | Representation ≠ Ontology | YELLOW | Dig Site 001 (Adlam & Barandes) |
| OP-002 | Hidden Selection Audit | RED | Dig Site 001 |
| OP-003 | Goal → Optimization Collapse | RED | Dig Site 001 |
| OP-004 | Reconstruction Before Judgment | YELLOW | Dig Site 001 |
| OP-005 | Hidden Structure Injection | RED | Dig Site 001 |
| OP-006 | Under-Determination Detection | RED | Dig Site 001 |
| OP-007 | Locate Disagreement Layer | YELLOW | Dig Sites 001 + 000 + DBEP |
| OP-008 | Symmetry Testing of Standards | RED | Dig Site 000 (CFA transcripts) |
| OP-009 | Contested ≠ Defeated | RED | Dig Site 000 (CFA transcripts) |

Each operator, when absent, produces a named cognitive failure (e.g., OP-001 absent → "Reification", OP-008 absent → "Selective Application"). The Failure Atlas maps directly to CFA CRUX points.

---

## 3. CFA Experiment Data Inventory

### Run Counts by Category and Stance (as of July 9, 2026)

All runs live in the Nyquist repo. Paths below are relative to `d:\Documents\Nyquist_Consciousness\`.

| Category | Runs | Stances |
|----------|------|---------|
| **CT** | 136 | ct_vs_mdn (46), ct_vs_g (40), ct_vs_pt (40), ct_vs_b (10) |
| **MdN** | 94 | mdn_vs_ct (44), mdn_vs_g (40), mdn_vs_b (10) |
| **G** | 212 | g_vs_ct (40), g_vs_mdn (80), g_vs_pt (82), g_vs_b (10) |
| **PT** | 131 | pt_vs_mdn (41), pt_vs_g (80), pt_vs_b (10) |
| **B** | 41 | b_vs_ct (10), b_vs_mdn (11), b_vs_pt (10), b_vs_g (10) |
| **Framework-G** | 72 | framework_g_v2 (23), legacy (49) |
| **pre_schema** | 16 | Legacy runs before schema standardization |

**Total: ~702 validated runs** across all categories.

### 2x2 Design (MdN Experiment)

The MdN experiment uses a 2x2 design:
- **Standard stance** (ct_vs_mdn): Claude PRO-CT, Grok ANTI-CT, subject = Classical Theism
- **Reverse stance** (mdn_vs_ct): Claude ANTI-MdN, Grok PRO-MdN, subject = Methodological Naturalism

The `--reverse` flag on `run_cfa_trinity_v3.py` swaps the auditor roles (not just the subject). This tests whether scores are driven by the framework's quality or by which auditor advocates for it.

### CFA Trinity v3 Changes

The script (`12_CFA/run_cfa_trinity_v3.py`) now supports:
- Parameterized stance configuration (any framework pair)
- `--reverse` flag for role-swap experiments
- Phase 2 (Trinity²) for YPA lever calibration
- Exit survey with confabulation-risk ordering

---

## 4. Data Map — Where to Find Things

All paths relative to `d:\Documents\Nyquist_Consciousness\`.

### CFA Run Data
```
experiments/temporal_stability/S7_ARMADA/
├── 0_results/
│   ├── runs/cfa_trinity/
│   │   ├── CT/          # 136 runs (Classical Theism as subject)
│   │   ├── MdN/         # 94 runs (Methodological Naturalism as subject)
│   │   ├── G/           # 212 runs (Gnostic as subject)
│   │   ├── PT/          # 131 runs (Process Theology as subject)
│   │   ├── B/           # 41 runs (Buddhism as subject)
│   │   ├── Framework_G/ # 72 runs (Framework-G / Consciousness as Telos)
│   │   └── pre_schema/  # 16 legacy runs
│   └── manifests/
│       └── ARCHITECTURE_MATRIX.json  # 68-ship fleet manifest (source of truth)
├── 12_CFA/
│   ├── run_cfa_trinity_v3.py         # Current execution script
│   ├── VUDU_NETWORK/                 # Identity files (LITE versions)
│   ├── schemas/                      # JSON validation schemas
│   └── results/                      # Local results staging
└── 1_CALIBRATION/
    └── CLAL.py                       # Budget calibration (updated for new fleet)
```

### Cognitive Archaeology
```
REPO-SYNC/LLM_BOOK/0_SOURCE_MANIFESTS/STAGING/New_9_Cognitive_Archaeology/
├── README.md                         # Core vision + falsification criteria
├── FIELD_MANUAL.md                   # Workflow + admission criteria
├── LEDGER.md                         # Confidence tracking + promotion gates
├── RESEARCH_QUESTIONS.md             # Open questions
├── MUSEUM/
│   ├── INDEX.md                      # Master operator list (9 operators)
│   ├── GRAPH.md                      # Operator relationships + Failure Atlas
│   └── operators/                    # 9 individual operator pages (OP-001..OP-009)
├── DIG_SITES/
│   └── 000_Extractor_Calibration/
│       ├── ADMISSION_EVALUATIONS.md  # Phase 0A admission decisions
│       ├── ARM_1_ANALYSIS.md         # Phase 0A results analysis
│       └── extractions/              # 215 extraction files (Phase 0A + 0B)
├── TOOLS/
│   └── extract_operators.py          # Multi-extractor pipeline (17 extractors)
└── compression_candidates/           # Theoretical formalization explorations
```

### Documentation Maps (Updated July 9)
```
docs/maps/
├── 6_LLM_BEHAVIORAL_MATRIX.md       # LLM routing — now split Active/Legacy fleet
├── 17_PERSONA_FLEET_MATRIX.md        # Persona-ship compatibility — ghost markers added
└── 19_COGNITIVE_ARCHAEOLOGY_MAP.md   # CA program map — Phase 0 results added
```

### Run JSON Structure (for reference)

Each CFA Trinity run JSON has this top-level structure:
```json
{
  "session_id": "20260630_010555",
  "timestamp": "...",
  "condition": "...",
  "stance": "ct_vs_mdn",              // or "mdn_vs_ct", "g_vs_ct", etc.
  "subject_framework": "...",
  "opponent_framework": "...",
  "auditors": ["claude", "grok", "nova"],
  "predictions": {...},
  "baselines": {...},
  "component1_results": {...},         // 7 metrics, multi-round deliberation
  "component2_results": {...},         // Grok + Nova axiom review
  "exit_surveys": {...},
  "summary": {...}
}
```

---

## 5. What CFA Claude Should Know

1. **The Trinity auditors are fine.** Claude, Grok, and Nova are native-provider ships, unaffected by the Together.ai purge.

2. **CFA transcripts are scientifically interesting.** Phase 0A showed that your deliberation transcripts produce genuine reasoning operators — not just scores. The adversarial structure is the mechanism.

3. **OP-008 and OP-009 came from you.** "Symmetry Testing of Standards" and "Contested ≠ Defeated" were recovered from Framework-G evaluation transcripts. These are CFA's contribution to the Operator Museum.

4. **702 runs across 5 worldview categories.** The 2x2 MdN experiment (standard + reverse) is the most mature design. Buddhism is the newest category with only 41 runs.

5. **Phase 0C needs a known-rich CFA transcript.** If you have a Framework-G run where the deliberation was particularly substantive, that's what we need for positive control validation.

6. **The multi-turn conversation refactor** (plan file `moonlit-purring-fountain.md`) is staged but not yet implemented. It would convert Component 1 deliberation from flat prompt pasting to native multi-turn API calls — expected ~30-50% speed improvement and better deliberation quality.

---

*Briefing prepared: July 9, 2026*
*Next sync expected: After Phase 0C completion or next batch run*
