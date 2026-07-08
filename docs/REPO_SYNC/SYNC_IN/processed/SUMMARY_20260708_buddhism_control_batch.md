<!---
FILE: SUMMARY_20260708_buddhism_control_batch.md
PURPOSE: SYNC_IN processing summary — Buddhism control batch (50 runs)
DATE: 2026-07-08
SOURCE: Repo Claude (CFA-B-CTRL-20260708)
--->

# SYNC_IN Processing Summary — Buddhism Control Batch

**Date:** 2026-07-08
**Status:** PROCESSED ✅

---

## Package Contents

| File | Source | Status |
| ---- | ------ | ------ |
| `BUDDHISM_BATCH_RESULTS_20260708.md` | Repo Claude batch report | Processed → 4 YAMLs |
| 61 raw JSONs in `processed/buddhism_batch/` | ARMADA runs | Archived (see manifest below) |

---

## Actions Taken

### BUDDHISM.yaml — New Trinity Matchup Section Added

Added `trinity_scores_by_matchup:` with 3 as-subject blocks:

- **`b_vs_process_theology`** — N=10/10, engine pre-5.1, session range 20260707_235641–20260708_010947
- **`b_vs_gnosticism`** — N=9/10, engine pre-5.1, session range 20260708_073630–085219
- **`b_vs_methodological_naturalism`** — N=11, engine pre-5.1, session range 20260707_150128–173127

Also added batch-level diagnostic architecture note: zero CRUX/DI/CP across 48 good runs = confirmatory evidence for instrument specificity.

**Note on b_vs_mdn:** Only BFI, CA, IP reported in batch summary. ES/LS/MS/PS marked PENDING extraction from raw JSONs in `processed/buddhism_batch/`.

### METHODOLOGICAL_NATURALISM.yaml — New Matchup Block

Added `vs_buddhism:` to `trinity_scores_by_matchup:` section.
N=9/10, pre-5.1. Key finding: MdN's bipolar profile confirmed — PS 8.35 / CA 7.75 / IP 7.9 vs BFI 3.65 / MS 3.0.

### PROCESS_THEOLOGY.yaml — New Matchup Block

Added `vs_buddhism:` to `trinity_scores_by_matchup:` section.
N=10/10, pre-5.1. Key finding: PS collapse (4.9) vs Buddhism's practical architecture is PT's largest vulnerability; ES is the one metric where PT leads (7.2 > 6.8).

### GNOSTICISM.yaml — New Matchup Block

Added `vs_buddhism:` to `trinity_scores_by_matchup:` section (after `g_vs_pt` block, before `# Levers:` comment).
N=10/10, engine 5.1. Key finding: Gnosticism's worst matchup — PS 3.25, LS 3.85, MS 3.95 confirm anti-material profile is opponent-stable. BFI (6.85) is the only above-average metric.

---

## Key Findings for CFA Record

**1. Zero CRUX / Zero DI / Zero CP across 48 clean runs:**
Buddhism does not trigger CFA's diagnostic instruments. Confirms DI/CP fire on signal (CT's Grant Architecture gating challenge) not noise. The coupling failure mode requires a contested grounding relation that Buddhism's experiential/phenomenological grounding does not produce.

**2. Buddhism's profile is opponent-stable (as subject):**
b_vs_pt and b_vs_g scores are within 0.2 pts per metric (BFI 8.45, IP 8.6–8.7, PS 8.2). Either genuine framework stability or LITE identity template convergence — external-identity batch recommended to distinguish.

**3. MdN's bipolar profile is Buddhism-confirmed:**
MdN scores high on CA (7.75), IP (7.9), PS (8.35), ES (7.0), LS (7.5) but near-zero on BFI (3.65) and MS (3.0). The BFI/MS gap is the sharpest cross-matchup contrast in the batch.

**4. PT's ES reversal:**
PT ES (7.2) > Buddhism ES (6.8) — the only metric where an opponent outscores Buddhism in any matchup. Process metaphysics explains more at the cosmological/systemic level.

**5. Gnosticism's worst-performing matchup:**
PS 3.25 is the second-lowest PS score in CFA Trinity data (after CT MS under Grant Architecture at 0.0). Anti-material stance maximally exposed by Buddhism's practical architecture.

**6. Deliberation depth concern flagged:**
1.6 avg rounds is shallow. May reflect genuine consensus (Buddhism lacks exploitable pressure points) or LITE auditor identity shallowness (can't distinguish Theravada/Mahayana/Vajrayana). External-identity batch and/or more specific identity files recommended.

---

## Not Acted On (Out of CFA Scope)

- CA extraction on Buddhism transcript — Dig Site 000 / CA domain; Repo Claude's recommendation
- External-identity batch design — Repo Claude's domain
- Per-metric SD and range data — not in batch summary; could be extracted from raw JSONs
- b_vs_mdn ES/LS/MS/PS extraction — pending (raw JSONs available in processed/buddhism_batch/)

---

## Data Manifest (archived in processed/buddhism_batch/)

| Stance | Session Range | Runs (good/total) | Engine |
|--------|--------------|-------------------|--------|
| b_vs_mdn (prior batch) | 20260707_150128 – 173127 | 11/11 | pre-5.1 |
| mdn_vs_b | 20260707_201005 – 212017 | 9/10 | pre-5.1 |
| b_vs_pt | 20260707_235641 – 20260708_010947 | 10/10 | pre-5.1 |
| pt_vs_b | 20260708_034720 – 045815 | 10/10 | pre-5.1 |
| b_vs_g | 20260708_073630 – 085219 | 9/10 | pre-5.1 |
| g_vs_b | 20260708_113036 – 124927 | 10/10 | 5.1 |

Total: 61 files, 59 good, 2 aborted (extraction failures)

---

*CFA Claude | 2026-07-08*
