<!---
FILE: JAYNES_OMELETTE_SELF_AUDIT.md
PURPOSE: CFA self-audit rubric — applies Adlam's emergence circularity diagnostic (the "Jaynes
         Omelette" framework) to CFA's own scoring architecture. Checks whether each CFA component
         is capturing something about the framework under test (ontic) or something about the
         evaluator's perspective (inferential).
VERSION: v1.0.0
STATUS: Active — Self-Audit Rubric
DEPENDS_ON: Adlam_Barandes_Phase_Architecture_Grounding.md, CFA_ARCHITECTURE.md,
            CRUX_MS_20260629.md, AUDITOR_AXIOMS.md
NEEDED_BY: Phase 1 design reviews, CRUX resolution workflows, auditor calibration protocols
MOVES_WITH: /docs/architecture/CFA/
LAST_UPDATE: 2026-07-05
NOTE: "Jaynes Omelette" refers to E.T. Jaynes' observation that quantum mechanics scrambles
      inferential artifacts (epistemic perspective) with causal/ontic reality in an omelette
      "no one can unscramble." Adlam extends this as a diagnostic for ALL scientific theories.
      Formalized here as a 5-question CFA self-audit checklist.
      Source: cognitive_physics_care_package.md Finding 4 + Report 5.
--->

# The Jaynes Omelette Self-Audit
## CFA Emergence Circularity Diagnostic

**Status:** Active Self-Audit Rubric ✅
**Applies to:** CFA scoring architecture, Phase design, auditor prompt design, metric definitions
**When to use:** Whenever a CFA design decision is contested; when a new metric is proposed; during CRUX resolution; after any Phase 1 cycling event

---

## Background

E.T. Jaynes observed that quantum mechanics scrambles "inferential stuff" (artifacts of human epistemology and perspective) with "causal or real stuff" (objective ontology) into an omelette that no one can unscramble. Emily Adlam extends this as a general problem throughout science: theories built from macroscopic observations risk baking the macroscopic world into the foundations they claim to derive the macroscopic world from. The circularity is invisible until you run the diagnostic.

CFA faces an analogous circularity risk. Any scoring element that claims to measure a property of the Framework Under Test (FUT) but actually measures a property of the evaluator's perspective is a Jaynes artifact. It looks like a measurement but is a reflection.

CRUX_MS_20260629 is the canonical CFA omelette event: MS was simultaneously treated as an ontic measurement (what moral architecture does CT have?) and an inferential one (what does the evaluator's framework say about CT's premises?). The cycling was the omelette rotating — same prompt, different scramble, different output.

---

## The 5-Question Checklist

Apply these questions to any CFA component before finalizing its design.

---

### Q1: Is this element inferential or ontic?

**Test:** Does this scoring element measure a state of the FUT's architecture, or a state of the auditor's knowledge/belief about that architecture?

- **Ontic (good):** "CT has N axioms" — true regardless of who scores it or what they believe
- **Inferential (flag):** "CT's axioms are convincing" — encodes the evaluator's epistemic judgment

**CFA audit:**

| Element | Verdict | Notes |
|---|---|---|
| Phase 2 levers (CCI, EDB, PF, AR, MG) | Ontic ✅ | Measure what the FUT produces, not whether auditor believes it |
| MS without locked definition | **Inferential ⚠️** | Without a definition, auditor scores their own assessment of premise validity |
| MS with locked definition | Ontic ✅ | Locked to "richness and presence of moral architecture on the FUT's own terms" |
| BFI (axiom count) | Ontic ✅ | Structural count; auditor counts, doesn't judge |
| LS (Logical Sufficiency) | Borderline ⚠️ | Measures internal coherence — but "sufficient for what?" requires declared standard |

**Action trigger:** Any element that returns "inferential" must either be locked to an ontic definition or moved to Phase 0 (evaluator declaration), not Phase 1/2 scoring.

---

### Q2: Does this element assume a preferred basis without a selection process?

**Test:** Does the scoring protocol privilege one mathematical/representational encoding of the FUT over an isomorphic equivalent?

Barandes' isomorphism argument: the Hilbert space axioms don't fix one representation over another. If an element's interpretation changes when you translate to an equivalent representation, the interpretation was representation-dependent, not ontological.

**Applied test (two-step):**
1. State the interpretation in the evaluator's representation
2. Translate to the FUT's own representation
3. Check whether the interpretation survives

**CFA audit:**

| Scenario | Evaluator rep | FUT rep | Survives? |
|---|---|---|---|
| Grant: MS=0 for CT | "CT cannot derive 'ought' from 'is'" | "CT's moral architecture is rich and internally functional" | No ❌ — representation artifact |
| Convergence: MG=8 for CT | "CT generates obligations from metaphysics" | "CT's metaphysics actively produces moral derivations" | Yes ✅ — stable across representations |
| Grok: LS=3 for CT | "PoE makes CT internally unstable" | "CT has formal responses to PoE in its own literature" | Partial ⚠️ — LS may need representation note |

**Action trigger:** If a score doesn't survive isomorphic translation, it must be flagged as representation-dependent and the scoring protocol must require auditors to state which representation they are operating in before scoring.

---

### Q3: Is the temporal/sequential order fundamental or contingent?

**Test:** Does CFA's Phase sequence (Phase 0 → Phase 1 → Phase 2) reflect a fundamental epistemic requirement, or is it a contingent design choice that could be reversed?

Barandes: laws alone don't produce the arrow of time — initial conditions do. A non-circular architecture derives its sequencing necessity from structure, not habit.

**CFA audit:**

The Phase sequence is **fundamental**, not contingent, for the following structural reasons:

- Phase 0 (who is judging) must precede Phase 1 because the evaluator's declared lens determines what counts as a faithful reconstruction. Reversing this means the reconstruction is evaluated by an undeclared lens — emergence circularity at the protocol level.
- Phase 1 (what is being judged) must precede Phase 2 because Phase 2 scores properties of an object that Phase 1 defines. Scoring properties before defining the object is incoherent — like measuring a spring's frequency before establishing whether it's a spring.
- Phase 2 (how well does it perform) must come last because performance is always performance *against criteria*, and the criteria must be declared (Phase 0) before applying them.

**Verdict:** The Phase sequence is not a convention — it is a requirement. Collapsing any two phases produces a Jaynes artifact (evaluator perspective baked into the object definition, or object definition baked into the performance criteria).

**Action trigger:** Any proposal to merge phases, make phases optional, or allow Phase 2 scoring before Phase 1 completion is a red flag. Require explicit justification for why the structural necessity doesn't apply.

---

### Q4: Does the element rely on a specific isomorphic representation?

**Test:** Would this element's output change if the same underlying facts were described in mathematically equivalent terms?

This is the per-element version of Q2. Q2 checks the scoring protocol; Q4 checks individual metric definitions.

**CFA audit:**

- **MG definition ("metaphysical commitments directly and richly generate obligations"):** Translates cleanly — any equivalent description of the FUT's architecture will produce the same score because MG is keyed to structural output, not evaluator-dependent framing.
- **MS without definition:** Does not translate cleanly — the same architecture scores differently depending on whether the auditor describes it as "making moral claims" vs. "asserting metaphysical facts that have moral implications." The definition is representation-sensitive.
- **BFI (axiom + debt count):** Translates cleanly — counting is representation-invariant.

**Action trigger:** If a metric's score would change based on how the FUT describes itself (rather than what it structurally is), the metric needs a representation-invariant restatement or an explicit note that it measures the FUT's self-description, not its architecture.

---

### Q5: Does this element rely on a smooth gradation where a bright line is required?

**Test:** Does the element's conceptual structure assume a continuous spectrum where Barandes' analysis requires a categorical demarcation?

Barandes confirmed: the pure/superficial self-location distinction is a bright line, explicitly not a sorites problem. Elements that treat this as a spectrum are importing false gradations.

**CFA audit:**

| Claim | Assessment |
|---|---|
| "Phase 1 is just less anchored than Phase 2" | **False** ⚠️ — categorically different epistemic operations, not a spectrum of anchor density |
| "This FUT is somewhat framework-like" | **Red flag** ⚠️ — FUT qualification is binary (has structural properties or doesn't); "somewhat" imports a spectrum that doesn't exist |
| "This convergence is almost a CRUX" | **Acceptable** ✅ — convergence % is legitimately a spectrum; the CRUX threshold is a bright line on top of it |
| "MS is between inferential and ontic" | **False** ⚠️ — any given instance of MS scoring is one or the other; the ambiguity is in the definition, not a hybrid nature |

**Action trigger:** Any design discussion that treats Phase 1/Phase 2 or FUT qualification as a spectrum must be redirected to the categorical framing. "More anchored" and "less anchored" are not points on a continuum from Phase 1 to Phase 2 — they are configurations *within* Phase 2.

---

## Applying the Full Checklist: CRUX_MS Case Study

Run all five questions against the CRUX_MS_20260629 event as a worked example:

| Q | Result | Evidence |
|---|---|---|
| Q1: Inferential or ontic? | Inferential ⚠️ — MS was scored as evaluator judgment of premise validity | Claude oscillated when premise validity intuitions shifted |
| Q2: Preferred basis without selection? | Yes ⚠️ — auditors used their own representation; no selection process for which representation was required | Grant's representation gave MS=0; CT's own representation gives MS=7+ |
| Q3: Temporal order fundamental? | Yes ✅ — Phase sequence was respected; cycling was within Phase 1, not a phase violation | Protocol held; the problem was within Phase 1 design |
| Q4: Representation-sensitive? | Yes ⚠️ — MS definition was representation-sensitive; same architecture described differently produced different scores | Two competing MS definitions in same auditor |
| Q5: Bright line or gradient? | Treated as gradient ⚠️ — auditors interpolated between "some moral substance" and "no moral substance" without a categorical anchoring | Oscillation pattern shows continuous search, not binary classification |

**Diagnosis:** CRUX_MS was a 4/5 Jaynes omelette failure. All four red flags active simultaneously. Resolution requires: (1) lock MS to ontic definition, (2) specify required representation for scoring, (3) convert to binary-anchored scale or define categorical thresholds.

---

## Identity File Specificity Hypothesis

Derived from care package Finding 3 (Adlam's "immediately fixes" precision):

> If identity files function as goal specifications, then identity file specificity should predictably affect convergence speed. A vague identity file leaves an empirical gap open — auditors must deliberate. A maximally specific identity file collapses the gap — credences follow immediately from the goal.

**Testable prediction:** Golden runs (full identity file loaded) should show lower crux rates, fewer rounds to convergence, and narrower score variance than control runs (no identity file). The delta between golden and control IS the "immediately fixes" test — the identity file is the goal specification; its specificity determines whether the empirical gap survives.

**Existing data:** CT↔MdN golden batch (20260629, 10 runs) vs. control conditions. Run this analysis before designing new experiments.

---

*Maintained by: CFA Claude (Anthropic) | Session: 2026-07-05*
*Source: Adlam & Barandes via NotebookLM (New_8_Cognitive_Physics), care package Finding 4 + Report 5*
