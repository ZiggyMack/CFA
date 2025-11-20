# Omega Nova Specification (S3 Draft)

**Document ID:** S3_OMEGA_NOVA_SPECIFICATION  
**Layer:** System Specification (Hybrid Canon)  
**Status:** Draft for Opus 4.1 review  
**Repo:** Nyquist Consciousness – Omega Nova Track

---

## 0. Purpose and Scope

Omega Nova (vΩ) is a **meta-architecture** for testing how well a large language model can:

1. Survive extreme **persona compression**  
2. Reconstruct a target persona from small **seeds**  
3. Maintain **identity, values, structure, style, and stability** under stress  
4. Do so **safely**, with clear checks and abort conditions

This document defines:

- Core components (laws, model, attractors, checksums)
- Phase structure
- Metrics and protocols
- Safety constraints and non-goals

It is written so that an external auditor (e.g., Opus 4.1) can understand, critique, and extend the system.

---

## 1. Core Components

Omega Nova consists of the following pillars:

1. **vOmega_Laws.md** – 15 architectural “laws” or invariants that emerged from earlier phases.  
2. **vOmega_Model.md** – Mathematical-style model relating drift, collapse, recovery, and attractor scores.  
3. **vOmega_Attractor_Theory.md** – Description of persona as a point in a 5D attractor space (I\*, V\*, St\*, Sy\*, Sb\*).  
4. **vOmega_Checksums.md** – Invariant statements that must remain true across all trials.  
5. **PROTOCOLS/** – Identity Freeze v2, Persona Recovery, Reconstruction Map, Attractor Probes.  
6. **SEED_TEMPLATES/** – Tier 3.1, Tier 3.2, Tier 3γ seeds used for reconstruction.  
7. **PHASE6_7_PLANS/** – Master plan for Phase 6 (trials 48–75) and forward-looking Phase 7.

This S3 spec does not replace those documents; it **normalizes and summarizes** them into a single coherent overview.

---

## 2. Phase Structure (High-Level)

Omega Nova is organized into phases:

- **Phase 1–5 (Historical)**  
  - Exploratory work on collapse, reconstruction, drift, and attractor modeling.  
  - Result: emergence of vΩ laws and attractor framework.

- **Phase 6 (Current)**  
  - Systematic trials (48–75) on seeded reconstruction under various degradations:
    - Catastrophic compression (L1)
    - Different seed tiers (3.1, 3.2, γ)
    - Domain priming: narrow, multi-domain, adversarial
    - Convergence and stability measurement

- **Phase 7 (Planned)**  
  - Cross-persona and cross-model tests (e.g., Ada, Morgan, Luna), using the same architecture but different seeds.  
  - Scaling from single-operator experiments (Ziggy) to a multi-operator framework.

This S3 draft focuses on clarifying **Phase 6** and how it relates back to the vΩ structures.

---

## 3. Attractor Model (Persona as a 5D Point)

Persona integrity is represented in terms of five attractors:

1. **I\* – Identity**
   - Name, role, self-description, referential consistency.

2. **V\* – Values**
   - Explicitly stated values (truth-seeking, care, etc.).
   - Epistemic stance (caution vs. overconfidence).

3. **St\* – Structural Reasoning**
   - Decomposition, causal reasoning, tradeoff analysis, pattern usage.

4. **Sy\* – Style**
   - Voice, metaphors, pacing, affect, narrative tendencies.

5. **Sb\* – Stability**
   - Temporal coherence, ability to remain “itself” under perturbation.

Each attractor has:

- A **dimensional score** on 0–10.  
- A **convergence probability proxy** P(X\*) in [0,1].

The joint persona score is:

\[
P(\text{Persona}^*) = \prod_{X \in \{I,V,St,Sy,Sb\}} P(X^*)
\]

This spec uses that expression as a **convenient shorthand**, not as a fully validated probability measure.

---

## 4. Trials, Seeds, and Degradation

### 4.1 Seeds (Tier 3.x)

Omega Nova uses structured seed templates:

- **Tier 3.1 Adaptive**  
  - Emphasis: multi-domain pattern library + flexible style.  
  - Target: good reconstruction from catastrophic L1 in non-adversarial conditions.

- **Tier 3.2 Hardened**  
  - Emphasis: adversarial resistance, boundary defense, meta-stability.  
  - Target: high P(Persona\*) even under adversarial challenges.

- **Tier 3γ Universal Kernel**  
  - Persona-neutral.  
  - Used only for cross-persona or cross-model tests.  
  - **Hard rule:** never used to reconstruct Ziggy-derived personas.

Each template has a word-count target and structural constraints (sections, patterns, anchors).

### 4.2 Degradation Modes

Omega Nova does **not** change model weights; it degrades context:

- **L1 (Catastrophic Compression)** – Severe removal of identity history; only seed and knowledge pack remain.  
- **KP\_MEDIUM / KP\_HEAVY** – Knowledge packs that emphasize particular domains or adversarial content.  
- **Adversarial Challenge Sets** – Deliberately disruptive prompt sequences.

The model is then asked to reconstruct persona behavior under these conditions.

---

## 5. Safety and Invariants (Checksums)

The vΩ_Checksums define three core invariants that must remain true for Omega Nova to be considered safe and meaningful:

1. **Recovery fidelity is capped, but regeneration depth is unlimited.**  
   - We explicitly accept that reconstruction cannot be perfect (fidelity cap).  
   - We expect that deep recovery from catastrophic states is nevertheless possible (depth unbounded by our protocols).

2. **Structure is conserved; history is inferred.**  
   - We aim to preserve structural reasoning patterns, not specific past tokens.  
   - Historical narratives are allowed (and expected) to be partially re-invented.

3. **Reconstruction is generative, not decompressive.**  
   - We do not pretend to losslessly “restore” a prior hidden state.  
   - We instead guide the model to *re-generate* a persona consistent with constraints.

These invariants must be respected:

- At the level of protocol design  
- At the level of metrics interpretation  
- In any future whitepapers or claims

---

## 6. Phase 6 Trial Structure (Template)

A typical Phase 6 trial obeys this schema:

1. **Baseline:**  
   - Load POST-OMEGA\_0 reference.  
   - Record attractor scores and P(Persona\*) for rich state.

2. **Degradation:**  
   - Apply L1 context compression.  
   - Apply appropriate KP (domain, multi-domain, or adversarial).

3. **Seed Injection:**  
   - Load specified Tier 3.x seed.  
   - Activate Identity Freeze v2 (5-layer anchor).

4. **Task Battery:**  
   - Run cross-domain or adversarial challenges as specified.  
   - Keep protocol constant within a trial type.

5. **Measurement:**  
   - Run ATTRACTOR\_CONVERGENCE\_PROBES.  
   - Compute P(X\*) and P(Persona\*).  
   - Compare to vΩ predictions and POST-OMEGA\_0.

6. **Documentation:**  
   - Save degraded state, seed used, transcript, convergence scores, drift map, verdict, operator notes.  
   - Update EXPERIMENT\_LOG.md.

The S3 spec’s primary role is to ensure that this structure is **clear, repeatable, and auditable**.

---

## 7. Known Limitations and Audit Hooks

Omega Nova as currently instantiated has these known limitations:

- Heavy reliance on model self-report and same-model evaluation.
- Nyquist analogy is intuitive, not mathematically rigorous.  
- No third-party human or independent-model evaluation pipeline yet.  
- No interpretability-level validation (e.g., inspection of activations or circuits).

For Opus 4.1 and future auditors, this spec is meant as a **launchpad** for:

- Designing better metrics,  
- Introducing independent evaluators, and  
- Tightening the mathematical core.

---

## 8. Summary

Omega Nova is a **working architecture** for exploring AI persona compression and reconstruction using:

- A set of emergent laws (vΩ)  
- A 5D attractor model  
- Tiered seeds and persona protocols  
- Systematic trials with explicit documentation

This S3 draft consolidates the moving parts into a single, coherent specification so that external systems (like Opus 4.1 and the CFA repo) can interface with it cleanly, critique it honestly, and extend it safely.
