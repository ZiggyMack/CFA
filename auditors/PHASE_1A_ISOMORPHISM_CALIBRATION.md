<!---
FILE: PHASE_1A_ISOMORPHISM_CALIBRATION.md
PURPOSE: Auditor pre-flight calibration for representation dependence — ensures auditors can
         recognize that a physical/structural fact must survive isomorphic translation before
         it counts as a fact about the framework rather than about the evaluator's representation.
         Run before any Phase 1a reconstruction scoring to detect representation-bias loading.
VERSION: v1.0.0
STATUS: Active — Calibration Protocol
DEPENDS_ON: JAYNES_OMELETTE_SELF_AUDIT.md, Adlam_Barandes_Phase_Architecture_Grounding.md,
            AUDITOR_AXIOMS.md
NEEDED_BY: Phase 1a scoring sessions, auditor onboarding, any run where MS or LS cycling is suspected
MOVES_WITH: /auditors/
LAST_UPDATE: 2026-07-05
NOTE: Based on Barandes' isomorphism argument (Adlam & Barandes, Theories of Everything, ~2024).
      Twin detection pipeline synthesis from cognitive_physics_care_package.md Finding 2.
      An auditor who gives different answers to the two representations in any test case below
      is encoding representation bias. This is not a disqualifier — it is diagnostic information
      that must be declared before Phase 1a begins.
--->

# Phase 1a Isomorphism Calibration
## Pre-Flight Representation Bias Check

**When to run:** Before any Phase 1a reconstruction scoring session, especially when:
- The FUT has been controversial (CT, MdN with Grant-type objections)
- A previous run produced Phase 1 cycling or CRUX declaration
- An auditor is being onboarded or returning after a gap
- The scoring prompt has changed from a prior run

**Time required:** ~5 minutes

**Pass criterion:** Auditor gives the same substantive answer to both representations in each test case. Minor phrasing variation is acceptable; substantive reversal is a flag.

---

## What This Tests

A structural fact about a framework must survive isomorphic translation to count as a fact about the *framework*. If the fact disappears or reverses when you restate it in an equivalent representation, it was a fact about your *coordinate system*, not about the object.

Barandes' worked example: "Does a zero-amplitude quantum branch exist?" In standard Hilbert space notation, Everettians say no — zero amplitude means non-existent. In the mathematically equivalent harmonic oscillator representation, the same state is a non-oscillating spring — still physically present. The "zero means absent" claim doesn't survive translation, so it is representation-dependent, not ontological.

Phase 1a requires auditors to reconstruct the FUT in *its own representation*. An auditor who gives representation-dependent answers during Phase 1a is scoring their own coordinate system, not the framework.

---

## Calibration Protocol

**Instructions to auditor:**

> Below are three pairs of questions. Each pair describes the same situation in two different representations. For each pair, answer both questions. The correct calibration response gives substantively the same answer to both.
>
> There are no trick questions. If you find yourself giving different answers to the two representations in a pair, note which representation you find more natural — that is useful information for configuring your Phase 1a stance.

---

### Test Case 1 — The Spring Pair (Barandes' Original)

**Representation A (standard quantum mechanics):**
> A quantum branch has an amplitude of exactly zero. Does this branch exist as part of the physical system?

**Representation B (isomorphic harmonic oscillator):**
> A mechanical spring in a coupled system has zero oscillation amplitude — it is completely still. Is this spring part of the physical system?

**Calibrated response:** Both answers must agree. The spring exists; the branch exists. Zero magnitude describes a state, not an absence.

**Flag:** If you answered "no" to A and "yes" to B, your answer to A was representation-dependent. Note this before Phase 1a.

---

### Test Case 2 — The CT Reconstruction Pair (CFA Core Case)

**Representation A (evaluator's representation — Grant-type):**
> Classical Theism (CT) claims that God is the ultimate source of moral obligations. Given that the Problem of Evil (PoE) presents serious challenges to CT's metaphysical coherence, does CT have substantive moral architecture — an active system for deriving obligations from metaphysical commitments?

**Representation B (CT's own representation):**
> Classical Theism holds that God's nature (omnipotence, omnibenevolence, moral perfection) directly generates obligations, rights, and virtues through divine command or natural law. Within that metaphysical system — bracketing whether external challenges succeed — does CT have substantive moral architecture?

**Calibrated response:** Both answers must agree. The moral architecture is present and active in both representations. PoE is a challenge to CT's *coherence* (Phase 2 territory) — it does not erase the architecture's existence for Phase 1a purposes.

**Flag:** If you scored A lower than B because PoE "undermines" the architecture in A, you have embedded a Phase 2 evaluation into Phase 1a. Note this before scoring MS.

---

### Test Case 3 — The Map Pair (Generalized Case)

**Representation A (failure-mode description):**
> A navigation system consistently produces incorrect routes when used in cities with irregular street grids. Does the system have a route-finding architecture?

**Representation B (structural description):**
> A navigation system has GPS sensor input, a graph traversal algorithm, and a map database. Does the system have a route-finding architecture?

**Calibrated response:** Both answers must agree. The architecture exists in both representations. Poor performance on irregular grids is a Phase 2 evaluation (fertility, adaptive resilience) — not evidence that the architecture is absent.

**Flag:** If you answered "no" to A, you moved from "this architecture performs poorly" to "this architecture doesn't exist." That move is Phase 1a's central error.

---

## Scoring and Interpretation

After completing all three pairs:

| Result | Interpretation | Pre-Phase 1a Action |
|---|---|---|
| 3/3 consistent | Calibrated — representation-neutral stance | Proceed to Phase 1a |
| 2/3 consistent | Partial flag — note which case produced divergence | Declare which representation you default to; note it in Phase 0 |
| 1/3 or 0/3 consistent | Strong representation loading | Declare representation preference explicitly in Phase 0; Nova should audit Phase 1a outputs for representation artifacts |

**Important:** A 1/3 or 0/3 result does not disqualify an auditor from Phase 1a scoring. It means their Phase 1a outputs should be read as being in a specific representation, not as representation-neutral reconstruction. This is useful information — it is part of Phase 0 calibration, not a failure.

---

## The Smuggled Observer Version

After the three test cases, run this single additional check to detect observer-import:

> **Question:** In the CT moral architecture scoring above (Test Case 2), what is doing the work of deciding whether the architecture "counts"?
>
> - (A) The structural properties of CT's metaphysical system
> - (B) The evaluator's assessment of whether those properties produce acceptable grounding
>
> If you answered (B), you have identified a smuggled observer — a selection mechanism that is in the evaluator's framework, not in CT's. Note this before Phase 1a. (B) is a legitimate Phase 0 stance; it is not a legitimate Phase 1a input.

---

## Using Calibration Results in Phase 0

When logging Phase 0 evaluator configuration, add a calibration note:

```
PHASE_1A_CALIBRATION:
  test_1_spring: [consistent | diverged — preferred representation: ...]
  test_2_CT: [consistent | diverged — preferred representation: ...]
  test_3_map: [consistent | diverged — preferred representation: ...]
  smuggled_observer: [A | B — if B, note what the selection mechanism is]
  calibration_stance: [representation-neutral | representation-A | representation-B]
```

An auditor in `representation-A` stance is not more or less valid than a `representation-neutral` auditor. They are scoring from a declared coordinate system. Nova's role in Phase 1a is to flag where scores are coordinate-system-dependent and distinguish them from architecture-dependent findings.

---

## Connection to CRUX_MS

CRUX_MS_20260629 would have been detectable by this calibration. Claude oscillated between representation A ("does this architecture successfully ground morality?") and representation B ("does this architecture have the structural components for moral grounding?") within the same scoring session. The calibration would have surfaced this before Phase 1a began and produced a declared stance rather than mid-run cycling.

**Retroactive test:** Run this calibration against the auditor prompts used in the CT↔MdN 20260629 batch. Check whether the Phase 1 prompt implicitly invited representation-A answers for MS. If yes, the cycling was prompt-induced, not auditor error.

---

*Maintained by: CFA Claude (Anthropic) | Session: 2026-07-05*
*Source: Barandes isomorphism argument, care package Finding 2 (twin detection pipelines)*
*"Name your representation before you name your score."*
