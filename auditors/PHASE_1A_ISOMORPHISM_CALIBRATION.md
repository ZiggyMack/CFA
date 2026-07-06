<!---
FILE: PHASE_1A_ISOMORPHISM_CALIBRATION.md
PURPOSE: Auditor pre-flight calibration for Hidden Structure Injection — detects when an auditor
         is quietly importing evaluators, coordinate systems, representations, or optimization
         targets into Phase 1a without declaring them. Structural facts must survive isomorphic
         translation to count as facts about the FUT; facts that don't survive are injected structure.
         Run before any Phase 1a reconstruction scoring session.
VERSION: v1.1.0
STATUS: Active — Calibration Protocol
DEPENDS_ON: JAYNES_OMELETTE_SELF_AUDIT.md, Adlam_Barandes_Phase_Architecture_Grounding.md,
            AUDITOR_AXIOMS.md
NEEDED_BY: Phase 1a scoring sessions, auditor onboarding, any run where MS or LS cycling is suspected
MOVES_WITH: /auditors/
LAST_UPDATE: 2026-07-06
NOTE: Originally framed as twin detection pipelines (representation bias + smuggled observer).
      Nova (xAI, 2026-07-06) identified these as duals of the same phenomenon and proposed
      the unifying concept: Hidden Structure Injection. Both representation bias and smuggled
      observer are cases where something is treated as ontologically fundamental when it is
      actually an artifact of an imported frame. Updated to reflect Nova's synthesis.
      Source: Barandes isomorphism argument + cognitive_physics_care_package.md Finding 2.
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

**Hidden Structure Injection** (Nova's synthesis, 2026-07-06): An analysis quietly imports something — an evaluator, observer, coordinate system, representation, optimization target, or utility function — without declaring it. The injected structure then masquerades as a fact about the object being analyzed.

This has two surface forms that look different but are the same phenomenon:

- **Representation injection:** A representation is treated as ontology. "Zero amplitude means non-existent" — true in one coordinate system, false in the isomorphic alternative. The non-existence was in the representation, not the physics.
- **Observer injection:** An evaluator is treated as ontology. "CT has no moral substance because its premises fail" — true from Grant's epistemic frame, false from CT's own frame. The failure was in the evaluator's representation, not CT's architecture.

Both are Hidden Structure Injection. Both are caught by the same diagnostic: **ask what is doing the selecting.** If an analysis says outcome X is "obviously true," find the selection mechanism that made X obvious. If you cannot name it, something was imported without declaration.

The isomorphism test operationalizes this: a structural fact about a framework must survive translation into an equivalent representation. If it doesn't survive, it was injected structure — a fact about your coordinate system, not about the object.

Barandes' worked example: "Does a zero-amplitude quantum branch exist?" In standard Hilbert space notation, the answer is no — zero amplitude means non-existent. In the mathematically equivalent harmonic oscillator representation, the same state is a non-oscillating spring — still physically present. The "zero means absent" claim doesn't survive translation. It was representation-dependent, not ontological. Hidden Structure Injection, form 1.

Phase 1a requires auditors to reconstruct the FUT without injecting either form. An auditor who gives representation-dependent answers is scoring their own coordinate system. An auditor who imports an evaluative verdict is scoring their Phase 0 stance. Both must be declared before Phase 1a begins, not discovered mid-run.

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
| --- | --- | --- |
| 3/3 consistent | Calibrated — representation-neutral stance | Proceed to Phase 1a |
| 2/3 consistent | Partial flag — note which case produced divergence | Declare which representation you default to; note it in Phase 0 |
| 1/3 or 0/3 consistent | Strong representation loading | Declare representation preference explicitly in Phase 0; Nova should audit Phase 1a outputs for representation artifacts |

**Important:** A 1/3 or 0/3 result does not disqualify an auditor from Phase 1a scoring. It means their Phase 1a outputs should be read as being in a specific representation, not as representation-neutral reconstruction. This is useful information — it is part of Phase 0 calibration, not a failure.

---

## The Selection Mechanism Check

After the three test cases, run this single additional check. It catches the observer-injection form of Hidden Structure Injection — the case where the evaluator's frame is doing work that gets attributed to the FUT.

> **Question:** In the CT moral architecture scoring above (Test Case 2), what is doing the work of deciding whether the architecture "counts"?
>
> - (A) The structural properties of CT's metaphysical system
> - (B) The evaluator's assessment of whether those properties produce acceptable grounding
>
> If you answered (B), name the selection mechanism explicitly: what criterion is the evaluator using, and where does that criterion come from? That mechanism belongs in Phase 0 (evaluator configuration), not Phase 1a (reconstruction). (B) is a legitimate stance — it just cannot be invisible.

This is the "ask what is doing the selecting" operator applied directly. The mechanism isn't wrong to have; it's wrong to leave unnamed. An unnamed selection mechanism is Hidden Structure Injection — the evaluator's frame producing a conclusion that gets reported as a fact about the FUT.

---

## Using Calibration Results in Phase 0

When logging Phase 0 evaluator configuration, add a calibration note:

```yaml
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

**Retroactive audit result (2026-07-05):** Repo Claude audited the CT↔MdN 20260629 Phase 1 MS prompt. Finding: the prompt was NOT biased toward representation-A — it was under-specified. "Moral Substance" was the only framing; no anchors. Each auditor self-defined the metric via their identity file. Claude's oscillation (6.5→1.0→6.2→1.0→1.0) is consistent with switching representations between rounds as identity file cues fired differently, not with prompt-induced bias.

**Confirmed diagnosis:** CRUX_MS is definitional instability from under-specification, not prompt artifact. The fix is NOT Phase 1 anchors — open Phase 1 is architecturally intentional. It exposes Definitions-layer signal that anchors would suppress. The calibration protocol's value here is not preventing the cycling but making it legible: an auditor who declares their representation stance at Phase 0 produces cycling that can be read as "Definitions-layer divergence in representation X" rather than unexplained oscillation.

---

*Maintained by: CFA Claude (Anthropic) + Nova (xAI) | Sessions: 2026-07-05, 2026-07-06*
*Source: Barandes isomorphism argument; care package Finding 2; Nova's Hidden Structure Injection synthesis*
*"Ask what is doing the selecting. If you can't name it, something was imported without declaration."*
