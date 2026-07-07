<!---
FILE: SUMMARY_20260706_gnostic_experiments.md
PURPOSE: SYNC_IN processing summary — gnostic_full_care_package.md intake
DATE: 2026-07-06
SOURCE: docs/REPO_SYNC/SYNC_IN/pending/gnostic_full_care_package.md
--->

# SYNC_IN Processing Summary — Gnostic Experiment Care Package

**Date:** 2026-07-06
**Source file:** `gnostic_full_care_package.md`
**Origin:** Repo Claude (CFA-GNOSTIC-BATCH-20260702-20260703, 181 clean v3 runs)
**Supersedes:** `gnostic_experiment_care_package.md` (2026-07-05, partial 120-run package)
**Status:** PROCESSED ✅

---

## Source Also Included (Pre-Ingested — No Action Needed)

Three worldview research packages were in SYNC_IN/pending alongside the care package:

| Package | Status | Notes |
|---------|--------|-------|
| `worldview/Gnostic-1/` | Pre-ingested (2026-01-02) | LLM Book pipeline output. GNOSTICISM.yaml was built from this material. `.ingested` marker present. |
| `worldview/Gnostic-2/` | Pre-ingested (2026-01-02) | Same. Routing matrix references GOLDEN_GEOMETRY/Nyquist as primary destination. CFA consumed what was needed. |
| `worldview/Gnostic-1-2-x3/` | Pre-ingested (2026-01-02) | Integration synthesis. GNOSTICISM.yaml `source_calibration_notes` documents the Jungian interpretive filter from this material. |

No further processing needed for worldview packages from CFA Claude's side.

---

## Actions Taken (Care Package)

| Finding | Action | Destination |
|---------|--------|-------------|
| Finding 1: Controls pristine (0% crux, ~0 divergence, 89 runs) | Noted as baseline validation | GNOSTICISM.yaml audit_status updated |
| Finding 2: Identity effect ~1.0-1.5 pts, always directional (7 matchups) | Documented; significance thresholds noted | GNOSTICISM.yaml matchup blocks |
| Finding 3: BFI and MS most identity-sensitive; PS/IP most robust | Added to CRUX_YPA_METHODOLOGY.md §6 with full metric ranking table | `docs/architecture/CFA/CRUX_YPA_METHODOLOGY.md` |
| Finding 4: G has most extreme score profile (4.3-pt spread) | Control baseline added to GNOSTICISM.yaml | `profiles/worldviews/GNOSTICISM.yaml` |
| Finding 5: Crux marks definitional fights, not philosophy | Added as §6 to CRUX_YPA_METHODOLOGY.md with cross-matchup confirmation | `docs/architecture/CFA/CRUX_YPA_METHODOLOGY.md` |
| Finding 6: Reverse-direction symmetry (G↔MdN nearly perfect mirror) | Noted in G vs MdN matchup block | `profiles/worldviews/GNOSTICISM.yaml` |
| Finding 7: PT as opponent generates lowest crux (25.7%) | Noted in matchup context; PT flagged as calibration reference | GNOSTICISM.yaml notes |

## GNOSTICISM.yaml Changes

- `status`: DRAFT → TRINITY-PARTIAL
- `version`: 0.1.0 → 0.2.0
- `trinity_scores_by_matchup`: Populated from empty `{}` to include:
  - `control_baseline_pooled` (30 runs, pooled G-as-subject controls)
  - `vs_methodological_naturalism` (20+20 runs, validated)
  - `vs_classical_theism` (10+10 runs, validated)
  - `g_vs_pt` (2 runs, flagged insufficient)
- `audit_status`: Updated to reflect Trinity-partial status

---

## Not Yet Acted On

- Per-metric per-matchup breakdowns — full detail pending extraction from raw JSONs in `9_gnostic/`
- CT, MdN, PT YAML updates for G-as-opponent matchup results — those frameworks' YAMLs should get their respective matchup blocks updated (CT vs G: +1.21 avg div, 48.6% crux; MdN vs G: -1.47, 61.4%; PT vs G: +1.02, 32.9%)
- Targeted G vs PT batch — only 2 runs exist; reverse symmetry unconfirmed
- `_K` recalibration using full 181-run dataset — Finding 3 (BFI avg |Δ|=1.47, 63.6% crux) suggests current K=0.15 may be worth revisiting with broader data

---

## Source Files

- Raw JSONs: `docs/REPO_SYNC/SYNC_IN/pending/9_gnostic/{matchup}/S7_cfa_trinity_*.json`
- Care package: `docs/REPO_SYNC/SYNC_IN/processed/gnostic_full_care_package.md`

---

## Key Takeaways for Future Reference

1. **Controls are the ground truth.** 89 pristine control runs across all matchups = zero false positives. Any delta in external condition is identity effect only.
2. **G's bipolar profile** (high BFI/IP, very low LS/MS/PS) makes it the best stress-test FUT for methodology changes.
3. **BFI and MS are Phase 1 priority targets** for definitional anchoring. This is now empirically confirmed across 7 matchups, not just theoretical.
4. **PT is the most isomorphically stable framework** — lowest crux as opponent (25.7%). Consider as calibration reference for Phase 1a work.
