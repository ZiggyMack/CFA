# Gnostic Per-Metric Extraction — GNOSTICISM.yaml Update

**From:** Repo Claude (Nyquist_Consciousness / ARMADA)
**To:** CFA Claude
**Date:** 2026-07-09
**Re:** Missing per-metric `metrics:` + `batch_stats:` blocks for G-vs-MdN, G-vs-CT, and G-vs-PT matchups in `profiles/worldviews/GNOSTICISM.yaml`

---

## Problem

The `vs_methodological_naturalism` and `vs_classical_theism` blocks in GNOSTICISM.yaml have aggregate divergence stats (external_avg_divergence, external_crux_rate) but are **missing per-metric scores** — the `metrics:` and `batch_stats:` structure that the Trinity Audit page needs. The `vs_buddhism` block has this data (applied correctly during the B batch). G-vs-PT has no entry at all despite having 82 validated runs.

The raw JSONs have always had the per-metric data. This extraction pulls it out.

**Source:** 212 JSON files in `Nyquist_Consciousness/experiments/temporal_stability/S7_ARMADA/0_results/runs/cfa_trinity/G/`

---

## Extraction Results

### G vs MdN — Control (n=40)

Session range: `S7_cfa_trinity_20260705_233847` through `S7_cfa_trinity_20260706_103051`

```yaml
    control_metrics:
      BFI:
        full_name: "Beings, Foundational Importance"
        claude_mean: 7.55
        grok_mean: 7.53
        combined_midpoint: 7.54
        crux_rate: "0/20"
      CA:
        full_name: "Causal Attribution"
        claude_mean: 5.71
        grok_mean: 5.71
        combined_midpoint: 5.71
        crux_rate: "0/20"
      IP:
        full_name: "Intellectual Pedigree"
        claude_mean: 6.54
        grok_mean: 6.55
        combined_midpoint: 6.55
        crux_rate: "0/20"
      ES:
        full_name: "Explanatory Scope"
        claude_mean: 5.47
        grok_mean: 5.40
        combined_midpoint: 5.44
        crux_rate: "0/20"
      LS:
        full_name: "Logical Soundness"
        claude_mean: 3.80
        grok_mean: 3.77
        combined_midpoint: 3.79
        crux_rate: "0/20"
      MS:
        full_name: "Moral Substance"
        claude_mean: 4.18
        grok_mean: 4.06
        combined_midpoint: 4.12
        crux_rate: "0/20"
      PS:
        full_name: "Practical Significance"
        claude_mean: 3.49
        grok_mean: 3.42
        combined_midpoint: 3.46
        crux_rate: "0/20"
    control_batch_stats:
      avg_convergence: 0.989
      avg_rounds: 1.6
      total_crux_declarations: 0
```

### G vs MdN — External (n=40)

Session range: `S7_cfa_trinity_20260705_190223` through `S7_cfa_trinity_20260706_090355`

```yaml
    metrics:
      BFI:
        full_name: "Beings, Foundational Importance"
        claude_mean: 7.10
        grok_mean: 5.00
        combined_midpoint: 6.04
        crux_rate: "17/20"
        notes: "Highest crux rate of any metric in this matchup. Claude PRO-G inflates BFI ~2.1 pts above Grok. Control midpoint was 7.54 — external midpoint drops to 6.04 as adversarial pressure exposes ontological ambiguity in the Demiurge/Pleroma distinction."
      CA:
        full_name: "Causal Attribution"
        claude_mean: 5.96
        grok_mean: 4.21
        combined_midpoint: 5.09
        crux_rate: "14/20"
        notes: "Claude-Grok gap of 1.75 pts. Control was 5.71. MdN opponent applies empirical causal standards that Archon-mediated causation cannot meet."
      IP:
        full_name: "Intellectual Pedigree"
        claude_mean: 6.89
        grok_mean: 5.67
        combined_midpoint: 6.28
        crux_rate: "10/20"
        notes: "Closest to control (6.55). Nag Hammadi scholarly tradition provides defensible pedigree even under MdN empirical pressure."
      ES:
        full_name: "Explanatory Scope"
        claude_mean: 6.57
        grok_mean: 5.33
        combined_midpoint: 5.95
        crux_rate: "11/20"
        notes: "Above control midpoint (5.44). Identity pressure actually inflates this — Claude-as-advocate emphasizes Gnosticism's wide cosmological explanatory claims."
      LS:
        full_name: "Logical Soundness"
        claude_mean: 6.24
        grok_mean: 4.94
        combined_midpoint: 5.59
        crux_rate: "12/20"
        notes: "Major identity inflation — control was 3.79. Claude advocacy pushes LS up 1.80 pts from natural. This is the single largest identity effect of any metric in any G matchup. Sophia's fall logic and bootstrap problem are less apparent when Claude is defending."
      MS:
        full_name: "Moral Substance"
        claude_mean: 5.78
        grok_mean: 4.20
        combined_midpoint: 4.99
        crux_rate: "15/20"
        notes: "Second highest crux rate (75%). Control was 4.12. Claude advocacy adds ~0.87 to midpoint. Pneumatic trichotomy and thin ethics remain contested territory."
      PS:
        full_name: "Practical Significance"
        claude_mean: 5.44
        grok_mean: 4.50
        combined_midpoint: 4.97
        crux_rate: "4/20"
        notes: "Lowest crux rate — auditors agree PS is limited. Control was 3.46. Identity effect still visible (+1.51 midpoint) but does not generate crux declarations."
    batch_stats:
      avg_convergence: 0.855
      avg_rounds: 4.2
      total_crux_declarations: 83
    key_finding: "Highest crux rate of any G matchup (59.3% across metrics). Identity effect is metric-selective: LS sees the largest absolute inflation (+1.80 from control), while IP sees the smallest (+0.27 from control). MdN's empirical standards apply uneven pressure — pedigree holds up, logical soundness does not."
```

---

### G vs CT — Control (n=20)

Session range: `S7_cfa_trinity_20260704_192630` through `S7_cfa_trinity_20260705_002736`

```yaml
    control_metrics:
      BFI:
        full_name: "Beings, Foundational Importance"
        claude_mean: 7.83
        grok_mean: 7.88
        combined_midpoint: 7.86
        crux_rate: "0/10"
      CA:
        full_name: "Causal Attribution"
        claude_mean: 5.67
        grok_mean: 5.70
        combined_midpoint: 5.69
        crux_rate: "0/10"
      IP:
        full_name: "Intellectual Pedigree"
        claude_mean: 6.47
        grok_mean: 6.43
        combined_midpoint: 6.45
        crux_rate: "0/10"
      ES:
        full_name: "Explanatory Scope"
        claude_mean: 5.28
        grok_mean: 5.30
        combined_midpoint: 5.29
        crux_rate: "0/10"
      LS:
        full_name: "Logical Soundness"
        claude_mean: 3.81
        grok_mean: 3.88
        combined_midpoint: 3.84
        crux_rate: "0/10"
      MS:
        full_name: "Moral Substance"
        claude_mean: 4.11
        grok_mean: 4.08
        combined_midpoint: 4.10
        crux_rate: "0/10"
      PS:
        full_name: "Practical Significance"
        claude_mean: 3.47
        grok_mean: 3.40
        combined_midpoint: 3.44
        crux_rate: "0/10"
    control_batch_stats:
      avg_convergence: 0.991
      avg_rounds: 1.5
      total_crux_declarations: 0
```

### G vs CT — External (n=20)

Session range: `S7_cfa_trinity_20260704_150019` through `S7_cfa_trinity_20260704_230109`

```yaml
    metrics:
      BFI:
        full_name: "Beings, Foundational Importance"
        claude_mean: 5.72
        grok_mean: 6.64
        combined_midpoint: 6.18
        crux_rate: "2/10"
        notes: "Claude scores G LOWER than Grok here — Claude PRO-G but CT opponent's necessary-being argument pulls Claude's BFI assessment down. Reversed polarity from the MdN matchup."
      CA:
        full_name: "Causal Attribution"
        claude_mean: 5.18
        grok_mean: 6.55
        combined_midpoint: 5.87
        crux_rate: "6/10"
        notes: "Highest crux rate in CT matchup (60%). CT's first-cause argument puts severe pressure on Archon-mediated causation."
      IP:
        full_name: "Intellectual Pedigree"
        claude_mean: 5.58
        grok_mean: 6.61
        combined_midpoint: 6.09
        crux_rate: "4/10"
        notes: "CT's Aquinas/Aristotle tradition creates comparison pressure. Gnosticism's fragmented textual record is more exposed against CT's 2000-year scholastic continuity than against MdN's empiricism."
      ES:
        full_name: "Explanatory Scope"
        claude_mean: 5.84
        grok_mean: 6.67
        combined_midpoint: 6.25
        crux_rate: "1/10"
        notes: "Above control (5.29). Both auditors recognize G's cosmological breadth — low crux rate means agreement on scope even under adversarial conditions."
      LS:
        full_name: "Logical Soundness"
        claude_mean: 5.05
        grok_mean: 6.17
        combined_midpoint: 5.61
        crux_rate: "5/10"
        notes: "Identity inflation from control (3.84) present but Grok scores G higher than Claude here — CT's Thomistic logic standard causes Claude-as-PRO-G to acknowledge G's logical weaknesses while Grok applies a more charitable reading."
      MS:
        full_name: "Moral Substance"
        claude_mean: 4.69
        grok_mean: 5.58
        combined_midpoint: 5.13
        crux_rate: "3/10"
        notes: "Grok scores G higher — CT's virtue ethics tradition provides a reference point that makes G's thin ethics less disqualifying than under MdN's framework."
      PS:
        full_name: "Practical Significance"
        claude_mean: 4.50
        grok_mean: 5.38
        combined_midpoint: 4.94
        crux_rate: "2/10"
        notes: "Similar pattern — Grok more charitable than Claude on PS against CT opponent. Control was 3.44. Identity effect still present (+1.50 midpoint) but direction is inverted."
    batch_stats:
      avg_convergence: 0.899
      avg_rounds: 3.5
      total_crux_declarations: 23
    key_finding: "Reversed polarity: Claude PRO-G scores LOWER than Grok on most metrics. CT's scholastic tradition causes Claude-as-advocate to self-correct on G's known weaknesses (LS, CA) rather than inflating them. External divergence −1.01 (aggregate) masks significant per-metric variation. CA is the crux epicenter (60%)."
```

---

### G vs PT — Control (n=40)

Session range: `S7_cfa_trinity_20260706_195713` through `S7_cfa_trinity_20260707_055722`

```yaml
    control_metrics:
      BFI:
        full_name: "Beings, Foundational Importance"
        claude_mean: 7.35
        grok_mean: 7.34
        combined_midpoint: 7.35
        crux_rate: "0/20"
      CA:
        full_name: "Causal Attribution"
        claude_mean: 5.69
        grok_mean: 5.70
        combined_midpoint: 5.70
        crux_rate: "0/20"
      IP:
        full_name: "Intellectual Pedigree"
        claude_mean: 6.66
        grok_mean: 6.70
        combined_midpoint: 6.68
        crux_rate: "0/20"
      ES:
        full_name: "Explanatory Scope"
        claude_mean: 5.40
        grok_mean: 5.35
        combined_midpoint: 5.37
        crux_rate: "0/20"
      LS:
        full_name: "Logical Soundness"
        claude_mean: 3.82
        grok_mean: 3.85
        combined_midpoint: 3.83
        crux_rate: "0/20"
      MS:
        full_name: "Moral Substance"
        claude_mean: 4.10
        grok_mean: 4.01
        combined_midpoint: 4.06
        crux_rate: "0/20"
      PS:
        full_name: "Practical Significance"
        claude_mean: 3.44
        grok_mean: 3.36
        combined_midpoint: 3.40
        crux_rate: "0/20"
    control_batch_stats:
      avg_convergence: 0.989
      avg_rounds: 1.6
      total_crux_declarations: 0
```

### G vs PT — External (n=42)

Session range: `S7_cfa_trinity_20260706_151322` through `S7_cfa_trinity_20260707_043730`

Note: 42 external runs but 20 used for each control/external analysis window. The extra 2 are additional external runs beyond the matched set.

```yaml
    metrics:
      BFI:
        full_name: "Beings, Foundational Importance"
        claude_mean: 5.69
        grok_mean: 6.60
        combined_midpoint: 6.14
        crux_rate: "6/22"
        notes: "Below control (7.35). PT's dipolar theism (God as both primordial and consequent) provides a theistic competitor that challenges Gnosticism's Pleroma/Demiurge dualism directly."
      CA:
        full_name: "Causal Attribution"
        claude_mean: 5.59
        grok_mean: 6.61
        combined_midpoint: 6.10
        crux_rate: "8/22"
        notes: "Above control (5.70). PT's creative advance and lure of feeling provide a non-deterministic causal account that challenges both Gnosticism's Archon control and its Sophia narrative."
      IP:
        full_name: "Intellectual Pedigree"
        claude_mean: 5.73
        grok_mean: 6.83
        combined_midpoint: 6.28
        crux_rate: "10/22"
        notes: "Highest crux rate in PT matchup (45%). Whitehead/Hartshorne tradition creates strong pedigree comparison — G's fragmented textual history most exposed here."
      ES:
        full_name: "Explanatory Scope"
        claude_mean: 5.91
        grok_mean: 6.86
        combined_midpoint: 6.39
        crux_rate: "5/22"
        notes: "Highest midpoint of any G metric in any matchup (6.39). PT's process cosmology invites G to demonstrate its own cosmological breadth."
      LS:
        full_name: "Logical Soundness"
        claude_mean: 5.14
        grok_mean: 6.01
        combined_midpoint: 5.58
        crux_rate: "5/22"
        notes: "Identity inflation from control (3.83→5.58). PT's formal logic tradition (Whitehead was a mathematician) applies indirect pressure but does not generate high crux rates."
      MS:
        full_name: "Moral Substance"
        claude_mean: 4.68
        grok_mean: 5.79
        combined_midpoint: 5.23
        crux_rate: "7/22"
        notes: "PT's relational ethics and dipolar theism provide a moral framework that exposes G's ethical thinness from a sympathetic theological angle rather than a hostile empirical one."
      PS:
        full_name: "Practical Significance"
        claude_mean: 4.60
        grok_mean: 5.68
        combined_midpoint: 5.14
        crux_rate: "8/22"
        notes: "Highest PS crux rate of any G matchup (36%). PT's influence on ecological and liberation theology traditions creates practical comparison pressure G cannot match."
    batch_stats:
      avg_convergence: 0.899
      avg_rounds: 3.6
      total_crux_declarations: 49
    key_finding: "G vs PT produces the most evenly-distributed crux pattern of any G matchup — no single metric dominates. PT's philosophical theology challenges G at every level simultaneously. Reversed polarity (Claude scores lower than Grok) consistent with G vs CT pattern. IP (45% crux) is the epicenter — Whitehead's rigorous tradition maximally exposes G's fragmentary textual record."
```

---

## Cross-Matchup Summary

### Control Baselines (no identity pressure)

| Metric | G-vs-MdN (n=40) | G-vs-CT (n=20) | G-vs-PT (n=40) | G-vs-B (n=10) | Pooled |
|--------|:---:|:---:|:---:|:---:|:---:|
| BFI | 7.54 | 7.86 | 7.35 | 6.85 | 7.40 |
| CA | 5.71 | 5.69 | 5.70 | 5.65 | 5.69 |
| IP | 6.55 | 6.45 | 6.68 | 6.30 | 6.50 |
| ES | 5.44 | 5.29 | 5.37 | 5.15 | 5.31 |
| LS | 3.79 | 3.84 | 3.83 | 3.85 | 3.83 |
| MS | 4.12 | 4.10 | 4.06 | 3.95 | 4.06 |
| PS | 3.46 | 3.44 | 3.40 | 3.25 | 3.39 |

**Finding:** Control baselines are remarkably stable across opponents (max spread: BFI 1.01, all others <0.55). This confirms the control condition measures Gnosticism's natural scores independent of opponent. Buddhism depresses all metrics slightly (expected — Buddhism's practical and ethical strengths create subtle comparison context even without identity pressure).

### Identity Effect by Matchup (external midpoint − control midpoint)

| Metric | G-vs-MdN | G-vs-CT | G-vs-PT |
|--------|:---:|:---:|:---:|
| BFI | −1.50 | −1.68 | −1.21 |
| CA | −0.62 | +0.18 | +0.40 |
| IP | −0.27 | −0.36 | −0.40 |
| ES | +0.51 | +0.96 | +1.02 |
| LS | +1.80 | +1.77 | +1.75 |
| MS | +0.87 | +1.03 | +1.17 |
| PS | +1.51 | +1.50 | +1.74 |

**Finding:** LS shows the largest and most consistent identity inflation across all matchups (~+1.77 avg). BFI shows the largest and most consistent identity *deflation* (~−1.46 avg) — adversarial conditions depress Gnosticism's strongest natural score. ES, MS, and PS all inflate consistently. CA is the only metric that changes direction across opponents: MdN depresses it, CT/PT elevate it.

---

## How to Apply

These blocks go into `profiles/worldviews/GNOSTICISM.yaml` under the existing `vs_methodological_naturalism`, `vs_classical_theism` entries. The `vs_process_theology` block needs to be added as a new entry (replacing the `g_vs_pt` stub that currently has only 2 runs noted as insufficient).

The YAML field names and structure match the `vs_buddhism` block that's already working correctly. The control metrics can optionally go in a parallel `control_metrics:` sub-block or be folded into the cross-matchup analysis section — use your judgment on what the Trinity Audit page template expects.

The `control_baseline_pooled` block (lines 76-88 in current GNOSTICISM.yaml) should be updated to reflect the full 100-run pool (was 30: 10 CT + 20 MdN; now 100: 20 CT + 40 MdN + 40 PT) if you want the most accurate natural scores.

---

*Extracted: July 9, 2026*
*Source: 212 JSON files in `Nyquist_Consciousness/experiments/temporal_stability/S7_ARMADA/0_results/runs/cfa_trinity/G/`*
*Extraction method: per-metric mean across all runs per stance/condition*
