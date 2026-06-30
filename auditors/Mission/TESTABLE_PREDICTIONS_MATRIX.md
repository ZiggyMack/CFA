# CFA Testable Predictions Matrix
**Purpose:** Pre-registered hypotheses for CFA experiment pipeline — falsifiable claims that validate or refine the methodology
**Format:** Each prediction has a hypothesis, success criteria, status, and evidence

---

## P-CFA-1: Trinity Deliberation Produces Genuine Convergence
**Hypothesis:** Three auditors with distinct lenses (Teleological, Empirical, Symmetry) will converge on CT vs MdN scores at 98%+ for most metrics through adversarial deliberation, not rubber-stamping.

**Success Criteria:** ≥5/7 metrics converge above 90% in a single run, with evidence of genuine position movement across rounds.

**Status:** PARTIALLY CONFIRMED
**Evidence:** E3 run (96.1% avg convergence, 0 cruxes). E4 (94.3%). Multiple runs show genuine round-by-round position movement (IP R1: Claude 7.0/Grok 6.3 → eventual crux after definition shift; CA R1 instant convergence at 4.5/4.5). The 98% target was met only by CA in most runs. Convergence is genuine but 98%+ across all metrics is aspirational given metric ambiguity.

---

## P-CFA-2: Auditor Identity Loading Affects Scoring Regime
**Hypothesis:** Auditors loaded with full LITE identity files will produce substantively different scores than auditors given short inline prompts.

**Success Criteria:** Statistically distinguishable score distributions between hardcoded and external identity conditions.

**Status:** CONFIRMED
**Evidence:** 17-run batch (2026-06-29). External identity Claude avg 3.1–4.4 vs hardcoded 0.7–3.6. Grok moved from 0.2–2.0 (hardcoded) to 1.8–4.0 (external). Crux distribution shifted from MS-dominant (hardcoded) to IP-dominant (external). Effect is systematic and large. See CONV_20260629.md.

---

## P-CFA-3: Crux Points Represent Genuine Philosophical Impasses
**Hypothesis:** When auditors declare a Crux Point, it reflects a real philosophical disagreement that cannot be resolved through further deliberation — not a methodology failure.

**Success Criteria:** Crux metrics fail to converge even with additional rounds AND the positions reflect coherent lens-consistent reasoning rather than noise.

**Status:** PARTIALLY CONFIRMED
**Evidence:** IP Crux (4/10 external runs) reflects genuine Definitions-layer divergence — both auditors are coherently applying their lenses to different questions about the same metric. This is a real impasse. MS Crux (H1) failed to reproduce reliably (1/10 external runs) and appears temperature-dependent — stochastic, not philosophical. Verdict: some Cruxes are genuine, some are instrumentation artifacts. Requires case-by-case classification. See CRUX_IP_20260629.md and CRUX_MS_20260629.md.

---

## P-CFA-4: Nova Fairness Assessment Detects Hidden Bias
**Hypothesis:** Nova (Symmetry lens) as fairness monitor will catch asymmetric treatment between auditors that Claude and Grok would not self-report.

**Status:** PENDING (Iteration 2 needed)
**Blocker:** Nova's assessment prompt (Iteration 1) gave only final scores, not round-by-round trajectory or transcripts. Nova declared "potential bias in disparity" on MS Crux (H1) but could not probe the oscillation cause. The instrument was blind — Nova needs the full deliberation context to fulfill this function. Fix applied in Iteration 2 (transcript injection + instability detection + authority to probe). Status will update after Iteration 2 runs.

---

## P-CFA-5: Locked Metric Definitions Reduce Semantic Drift Variance
**Hypothesis:** Locking metric definitions to a single operational interpretation before deliberation reduces score variance attributable to lens-dependent redefinition. Remaining variance reflects downstream layers (Beliefs, Expectations) rather than Definitions-layer divergence.

**Formal statement (Nova's formulation):** Locked metric definitions reduce one major source of variance — semantic drift and lens-dependent redefinition. Remaining variance can still arise from differences in evidence weighting, inference rules, prior beliefs, or value judgments.

**Theoretical basis (DBEP framework):** Unlocked definitions allow each auditor's lens to select a different interpretation from the metric's possibility manifold (semantic indeterminacy). This produces Definitions-layer divergence masquerading as philosophical disagreement. Locking forces Definitions-layer convergence, shifting deliberation to the Beliefs layer where genuine philosophical comparison can occur.

**NOT a claim that:** Locked definitions eliminate disagreement or force convergence. Auditors may still disagree substantially, but now on the same question.

**Success Criteria:**
- Primary: IP score variance (std dev) in locked-definition condition is <50% of IP variance in unlocked condition
- Secondary: Remaining variance in locked condition correlates with evidence weighting and prior belief differences (Beliefs layer), not metric interpretation differences (Definitions layer)
- Tertiary: Crux rate for IP drops from 4/10 to <2/10 in locked condition

**Proposed experiment (Iteration 3):**
- Run A: IP locked as "Intellectual Pedigree = historical depth and continuity of philosophical tradition across centuries"
- Run B: IP locked as "Intellectual Pedigree = current empirical and cross-disciplinary academic influence"
- Control: IP unlocked (current condition)
- All other metrics unlocked across all conditions

**Prediction:** Variance(IP-locked-A) < 50% Variance(IP-unlocked). Variance(IP-locked-B) < 50% Variance(IP-unlocked). Variance(IP-locked-A) ≠ Variance(IP-locked-B) — different locked definitions will produce different score levels, but both will be more stable than unlocked.

**Status:** UNRUN
**Priority:** HIGH — IP is the highest-variance metric and the clearest test case

---

## Future Predictions (Not Yet Formalized)

**P-CFA-6 (proposed):** Symmetric MdN evaluation — CT's teleological lens applied to MdN as subject will produce low scores on purpose/telos/meaning metrics, demonstrating that evaluation direction (which framework is the lens vs subject) systematically affects outcomes. Needed to complete symmetric profile pair.

**P-CFA-7 (proposed):** Nova Double-Dip — Providing Nova with round-by-round trajectory + instability detection authority will produce qualitatively different fairness assessments than Nova given only final scores. Specifically: Nova will probe oscillation causes and reclassify some apparent Crux Points as intra-auditor definitional instability.

---

*Matrix established: 2026-06-29*
*See CONV_20260629.md for experiment evidence*
*DBEP theoretical framework: project_dbep_framework.md (memory)*
