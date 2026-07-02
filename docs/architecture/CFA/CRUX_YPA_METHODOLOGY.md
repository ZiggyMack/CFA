<!---
FILE: CRUX_YPA_METHODOLOGY.md
PURPOSE: Post-experiment methodology note on Crux Include/Exclude in YPA scoring — captures
         the epistemic reasoning, implementation options, and empirical findings that emerged
         from the Trinity golden batch runs (CT↔MdN, CT↔PT, 2026-06-29/30).
VERSION: 1.0.0
STATUS: Active Research Methodology
DEPENDS_ON: profiles/worldviews/CLASSICAL_THEISM.yaml, METHODOLOGICAL_NATURALISM.yaml,
            PROCESS_THEOLOGY.yaml, utils/calculations.py
NEEDED_BY: Future CFA development, Trinity audit methodology reviews
MOVES_WITH: /docs/architecture/CFA/
LAST_UPDATE: 2026-07-02
NOTE: This supersedes the directional speculation in APP_CRUX_INTEGRATION_SPEC.md §2.
      That spec was pre-experiment (2025-11-13). This note reflects post-experiment empirical
      methodology.
--->

# Crux Include/Exclude — YPA Scoring Methodology

**Status:** Active Research Methodology
**Context:** Trinity golden batch — CT↔MdN (10 runs, 2026-06-29), CT↔PT (10 runs, 2026-06-30)
**Implements:** `utils/calculations.py::ypa_scenario_scores()` Crux Exclude block

---

## 1. What a Crux Actually Is (Post-Experiment Understanding)

A **Crux declaration** occurs when two adversarial auditors (Claude as PRO-worldview, Grok as ANTI-worldview) cannot converge on a score for a given metric after deliberation. The 5-Part Scaffold structures the rounds; if after the final round the spread remains above the convergence threshold, a Crux is formally declared and classified (epistemic, definitional, values-based, etc.).

**Critical point:** The Crux mechanism identifies the disagreement and names it — it does not resolve it. The golden batch mean for a metric incorporates all sessions, including ones where a Crux was declared. The `crux_rate` in the YAML tells you what fraction of sessions produced a Crux on that metric. It does NOT tell you which auditor was right.

**`crux_rate: "9/10"`** means: in 9 out of 10 sessions, the two auditors on that metric could not converge. The mean score for that metric is still the average of both auditors' final positions across all 10 sessions. The Crux rate is a flag on the *stability* of that mean — it tells you the mean was built on contested ground.

---

## 2. The Core Epistemic Problem with Directional Adjustment

The original implementation (v1, 2026-07-02) applied a **subtractive penalty**:

```python
lever = lever - avg_crux_rate   # e.g., MdN CCI: 6.80 - 0.5 = 6.30
```

This was immediately challenged: **what direction should the penalty go?**

The problem in full:

When auditors score 4 and 8 on a metric (Crux declared), and we compute mean = 6.0:
- If we subtract a penalty → we push toward the *lower* scorer's position
- The lower scorer was the adversarial auditor (ANTI-worldview / Grok in most sessions)
- We are therefore implicitly siding with the skeptical auditor whenever there is disagreement
- But the crux could be because the PRO-auditor was *correct* and the ANTI-auditor was *too harsh*

The converse is equally true:
- An *upward* adjustment would side with the PRO-auditor
- No adjustment at all treats the mean as reliable regardless of how contested it is

**There is no neutral directional choice.** Any numeric adjustment encodes a stance on who is right when auditors disagree. The Crux mechanism surfaces the disagreement precisely so we *don't* have to pretend there's an easy resolution.

This is not a bug in the mechanism — it is the mechanism working correctly. Crux declarations are epistemically honest. The problem is in what the scoring system does *with* that honesty.

---

## 3. Three Options Considered

### Option 1: Subtractive Penalty (implemented and then replaced)

```python
lever -= avg_crux_rate * 1.0
```

- Simple, visible
- **Flaw:** Additive, so a lever at 8.5 and a lever at 4.0 both lose the same absolute points for the same crux rate — which gives the lower-value lever a proportionally larger hit. Not well-reasoned.
- **Directional stance:** Skeptic wins by default on all contested metrics.
- Replaced with Option 2.

### Option 2: Multiplicative Dampening (current implementation)

```python
lever *= (1 - avg_crux_rate * 0.15)
```

Where `_K = 0.15` means a 100%-contested metric damps its lever by 15%.

- Proportional: higher-valued levers take a larger absolute hit, but all levers see the same *percentage* reduction. Internally consistent.
- Still directional (downward), but framed as **confidence discount** rather than "the skeptic was right."
- Reads as: "We trust this lever score less in proportion to how contested the deliberation was."
- The assumption is made explicit in the UI tooltip: *"direction is a stance, not a fact — the crux tells us that auditors disagreed, not who was right."*

**Why `_K = 0.15`?** Calibration rationale:
- A metric with 50% crux rate (5/10 sessions contested) damps its lever by 7.5%
- A metric with 90% crux rate (highly contested) damps by 13.5%
- At these levels the effect is meaningful (~0.5–1.0 lever points for typical lever values of 6–8) without being catastrophic
- `_K` is an explicit research parameter — future experiments can tune it

### Option 3: Confidence Band — No Directional Claim (open for future)

Instead of adjusting the point estimate, show a range:
- **Include:** YPA = point estimate (current behavior)
- **Exclude:** YPA = point estimate ± confidence band derived from spread between auditors

This makes no claim about direction. The lever score does not change; instead the UI communicates uncertainty explicitly (e.g., "YPA: 3.21 ± 0.18 when Crux metrics are excluded from confidence").

**Why not yet:** Requires UI work to display ranges, and requires per-metric spread data (Claude mean vs Grok mean) to feed into the band calculation — that data exists in the YAML but the console rendering doesn't yet support range display. Flagged as the long-term preferred solution if the directional assumptions of Option 2 draw criticism.

---

## 4. Metric → Lever Mapping

CFA YPA levers are not the same as Trinity Phase 1 metrics. The mapping used to determine which lever receives a crux dampening:

| Trinity Metric | Full Name | CFA Lever | Rationale |
|---|---|---|---|
| CA | Causal Attribution | CCI | Causal logic is the core of coherence claims |
| LS | Logical Soundness | CCI | Internal validity is also CCI territory |
| IP | Intellectual Pedigree | EDB | Epistemic depth tracks scholarly/historical lineage |
| ES | Explanatory Scope | EDB | Breadth of explanation = EDB |
| PS | Practical Significance | PF | Practical utility maps to pragmatic fertility |
| MS | Moral Substance | MG | Moral framework strength = moral generativity |
| BFI | Beings, Foundational Importance | *(none)* | BFI contributes to the denominator, not a lever |
| — | *(no metric)* | AR | Aesthetic Resonance has no Phase 1 Trinity counterpart |

When multiple metrics map to the same lever (CA and LS both → CCI), the average crux rate of the mapped metrics is used.

---

## 5. Empirical Findings — CT vs MdN Golden Batch

The most informative finding from applying Option 2 is the **asymmetry between CT and MdN**:

### CT as Subject (audited by MdN lens, 10 sessions)

| Metric | crux_rate | Maps to | Dampening |
|---|---|---|---|
| BFI | 1/10 = 0.10 | — | n/a |
| CA | 0/10 = 0.00 | CCI | 0% |
| IP | 4/10 = 0.40 | EDB | 6.0% |
| ES | 2/10 = 0.20 | EDB | 3.0% → avg EDB = 4.5% |
| LS | 0/10 = 0.00 | CCI | 0% → avg CCI = 0% |
| MS | 1/10 = 0.10 | MG | 1.5% |
| PS | 0/10 = 0.00 | PF | 0% |

**CT is nearly immune to Crux Exclude.** CCI and PF are untouched. EDB drops ~4.5%. MG drops ~1.5%.

### MdN as Subject (audited by CT lens, 10 sessions)

| Metric | crux_rate | Maps to | Dampening |
|---|---|---|---|
| BFI | 9/10 = 0.90 | — | n/a |
| CA | 7/10 = 0.70 | CCI | 10.5% |
| IP | 4/10 = 0.40 | EDB | 6.0% |
| ES | 6/10 = 0.60 | EDB | 9.0% → avg EDB = 7.5% |
| LS | 3/10 = 0.30 | CCI | 4.5% → avg CCI = 7.5% |
| MS | 3/10 = 0.30 | MG | 4.5% |
| PS | 5/10 = 0.50 | PF | 7.5% |

**MdN takes meaningful hits across all levers.** CCI drops 7.5%, EDB drops 7.5%, PF drops 7.5%, MG drops 4.5%.

### Interpretation

This is empirically interesting rather than being an artifact of design choice. What the data is telling us:

**CT's arguments held up better under adversarial pressure.** When MdN was the adversarial lens challenging CT's metrics, it could not produce persistent auditor disagreement on most metrics — only IP and ES showed any notable contestation (auditors disagreed on whether CT's pedigree and scope claims were philosophically defensible or merely historically dense). CA, LS, PS, and MS reached consistent conclusions across nearly all sessions.

Conversely, **CT as adversarial lens was more effective at creating genuine uncertainty about MdN**. CT's challenges on BFI (MdN's foundational importance), CA (whether empirical correlation implies causation at a deep level), and ES (whether explanatory scope is wide or narrow without teleology) produced sustained disagreement in 60–90% of sessions.

**The Skeptic Mode connection:** Skeptic Mode (preset) now sets `include_crux=False`. The counter-intuitive implication is that Skeptic + Exclude penalizes MdN *more* than CT — despite Skeptic mode being nominally "MdN-optimized." The reason: MdN's score benefits most from *not* having its contested metrics penalized. When a skeptic says "I don't trust scores built on contested deliberation," MdN takes a larger hit than CT does, because MdN's deliberation was more contested.

This could be a meaningful finding or could reflect auditor-specific biases (Claude as PRO-MdN may have been less effective at defending MdN against CT challenges than Claude was at defending CT against MdN challenges). Further symmetric experimental design would be needed to separate framework-level robustness from auditor-pairing effects.

---

## 6. PT vs CT Preliminary Data

PT (as subject, audited by CT lens, 10 sessions):

| Metric | crux_rate | Maps to | Dampening |
|---|---|---|---|
| BFI | 7/10 | — | n/a |
| CA | 5/10 | CCI | 7.5% |
| IP | 2/10 | EDB | 3.0% |
| ES | 3/10 | EDB | 4.5% → avg EDB = 3.75% |
| LS | 3/10 | CCI | 4.5% → avg CCI = 6.0% |
| MS | 6/10 | MG | 9.0% |
| PS | 2/10 | PF | 3.0% |

PT sits between CT and MdN in contestation level. MS (Moral Substance) is PT's most contested metric — CT's adversarial lens challenged PT's ethical grounding more effectively than its epistemic claims (PT's process-relational ethics is genuinely novel and less historically anchored than CT's natural law tradition).

CT as subject audited by PT lens: data pending (CT-as-subject vs PT-as-lens experiment not yet run).

---

## 7. Preset Mode Wiring

| Preset | `include_crux` | Rationale |
|---|---|---|
| 🔬 Skeptic | `False` | Skeptics distrust contested claims; apply dampening |
| 🤝 Diplomat | *(unchanged)* | No crux stance implied by diplomatic framing |
| 🙏 Seeker | *(unchanged)* | Seekers accept deliberation results as given |
| 👿 Zealot | *(unchanged)* | Zealot mode has no natural crux stance |

Zealot and Diplomat modes intentionally leave the Crux toggle at the user's current setting. Only Skeptic has a principled reason to auto-set.

---

## 8. Relationship to APP_CRUX_INTEGRATION_SPEC.md

`APP_CRUX_INTEGRATION_SPEC.md` (v1.0.1, 2025-11-13) was written before any Trinity experiments ran. It proposed a `NORMALIZE_UNCERTAINTY` formula using per-session raw auditor scores:

```
score = midpoint * (1 - spread/midpoint)
```

where `spread = |claudeScore - grokScore| / 2`.

That formula uses the *actual per-session divergence* between auditors — a cleaner signal than crux_rate because it uses the magnitude of disagreement, not just the binary "was a crux declared." 

**Why we didn't use that formula:** The canonical YPA calculation runs off `lever` scores stored in the YAML (golden batch means), not session-by-session raw scores. Session-level Claude/Grok divergence data exists in the JSON files but is not surfaced at the lever level. The YAML stores `crux_rate` (session-level binary flag) and `spread` (per-metric, in the Trinity scores block) but we'd need to write a separate extraction layer to compute the APP_CRUX_INTEGRATION_SPEC formula. That's a future enhancement.

Current formula uses `crux_rate` as the closest available proxy for per-metric contestation intensity.

---

## 9. Open Questions and Future Work

**Q1 — Direction validity:** Can we empirically test whether the downward-only penalty is correct? One approach: run counterfactual sessions where Crux-declared metrics are re-scored by a third auditor (e.g., Gemini) with no prior context. Does the third auditor tend toward the Claude score (PRO) or the Grok score (ANTI)? If systematically toward one, that informs direction.

**Q2 — Spread-based formula (Option 3 precursor):** The YAML `metrics.{metric}.spread` field (e.g., CT-BFI spread = 2.1, meaning Claude mean was 2.1 points above Grok mean on that metric) gives us the *magnitude* of disagreement per metric, not just the binary Crux flag. A future implementation could use spread to derive a confidence band rather than a point-estimate penalty.

**Q3 — Auditor identity effects:** CT as PRO-auditor vs CT as subject are different experimental roles. Claude in PRO-CT consistently scored CT's CA and LS near 7.4–7.6; Grok as ANTI-CT scored them near 5.2–6.4. Is the convergence/divergence pattern telling us about the *framework's* properties or about *which lens is more effective*? The reverse experiment (CT as lens auditing MdN with same Claude/Grok pairing) would help isolate this.

**Q4 — `_K` calibration:** The penalty coefficient `_K = 0.15` was chosen by reasoning, not by experiment. As more matchups run and YPA ranges become empirically calibrated, this parameter should be tuned. A natural tuning target: the crux-exclude delta should be large enough to meaningfully separate "stable" from "contested" frameworks but small enough not to override the lever signal entirely.

**Q5 — PT vs MdN data:** When the PT vs MdN experiment runs, crux_rates for that matchup will fill in the currently empty `vs_methodological_naturalism` block in `PROCESS_THEOLOGY.yaml`. At that point, the full three-way comparison (CT, MdN, PT in all six pairings) will show whether the stability ordering observed in CT↔MdN and CT↔PT holds.

---

## 10. Implementation Reference

**File:** `utils/calculations.py` — `ypa_scenario_scores()` function
**Formula:** `lever *= (1 - avg_crux_rate * _K)` where `_K = 0.15`
**Data source:** `fr["crux_rates"]` dict, populated by `views/console.py::_get_crux_rates()`
**YAML source:** `trinity_scores_by_matchup.vs_{opponent}.metrics.{metric}.crux_rate`
**Format:** String `"N/10"` — parsed to float `N/10.0` by `_get_crux_rates()`

---

**Filed:** `docs/architecture/CFA/CRUX_YPA_METHODOLOGY.md`
**Status:** Active Research Methodology
**Author context:** Emerged from 2026-07-02 implementation session
**Pre-experiment spec:** See `APP_CRUX_INTEGRATION_SPEC.md` for original design vision
