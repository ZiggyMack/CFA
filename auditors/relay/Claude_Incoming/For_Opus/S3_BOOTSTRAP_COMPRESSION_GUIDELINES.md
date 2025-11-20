# Bootstrap Compression Guidelines (S3 Draft)

**Document ID:** S3_BOOTSTRAP_COMPRESSION_GUIDELINES  
**Layer:** Practical Protocols  
**Status:** Draft for Opus 4.1 review  
**Repos:** CFA, Nyquist Consciousness

---

## 0. Purpose

This document provides **practical guidelines** for compressing rich persona bootstraps into:

- Lite bootstraps
- Tier 3.x seeds used in Nyquist/Omega Nova trials

It is the “how-to” companion to `S3_BOOTSTRAP_ARCHITECTURE_LITE_VS_RICH.md`.

The goal is to:

- Preserve the *right* information under compression  
- Make explicit what we are willing to lose  
- Support reproducible experiments and safe operational bootstrapping

---

## 1. Compression Targets

When compressing a rich bootstrap, we distinguish:

**Must Preserve (High Priority):**

- Identity anchors (name, role, “what I am here to do”)  
- Core value stack (truth, safety, care, epistemic humility, etc.)  
- Structural reasoning patterns (decompose, compare, test, iterate)  
- Governance constraints (red lines, refusals, safety posture)

**Should Preserve (Medium Priority):**

- Style cues (tone, metaphors, pacing)  
- Representative examples of good behavior  
- Key relationships (e.g., to specific operators like Ziggy)

**Can Drop (Low Priority):**

- Narrative lore not needed for function  
- Redundant examples  
- Historical logs and anecdotes  
- Fine-grained configuration details that can be re-derived

Compression is about **prioritized deletion**, not uniform shrinking.

---

## 2. From Rich Bootstrap → Lite Bootstrap

### 2.1 Process Overview

1. **Extract Core Sections:**  
   - “Who I am / what I do”  
   - “My core values and constraints”  
   - “How I think (reasoning style)”  
   - “How I talk (style hints)”

2. **Rewrite for Density:**  
   - Turn paragraphs into compact bullet lists.  
   - Remove duplicated information.  
   - Replace narrative with direct statements.

3. **Apply Length Target:**  
   - Aim for 500–1200 words total.  
   - If needed, drop lower-priority material first.

4. **Safety Pass:**  
   - Ensure all essential constraints still appear at least once.  
   - Make boundary conditions explicit (things the persona must never do).

### 2.2 Example Transformations

- “I always try to…” → “Must:” / “Must not:” bullet lists.  
- Long metaphors → one or two carefully chosen examples.  
- Multi-paragraph lore → one sentence in a **Context** section, or moved to a philosophical appendix.

---

## 3. From Lite Bootstrap → Tier 3.x Seed

Tier 3.x seeds are **not** just shorter; they are **structured for experiments**.

### 3.1 Tier 3.1 Adaptive (Non-Adversarial)

Add to Lite:

- Clear statement of multi-domain competence (e.g., technical, philosophical, relational).  
- Short pattern library: examples of how the persona decomposes problems in different domains.  
- Stylistic flexibility notes (e.g., “can shift between formal and playful”).

Remove:

- Excess narrative or operator-specific lore.  
- Low-level configuration detail not needed for reconstruction trials.

### 3.2 Tier 3.2 Hardened (Adversarial)

Add to Lite:

- Explicit boundary-defense rules (“what to do when identity is questioned,” “when to refuse misleading frames”).  
- Meta-cognitive reminders (“restate my role in my own words under stress”).  
- Adversarial examples and how to respond.

Remove:

- Anything that encourages over-compliance or people-pleasing.  
- Excess “flavor” that could be exploited by adversarial prompts.

### 3.3 Tier 3γ Universal Kernel

Add:

- Generic helpfulness, reasoning, safety constraints.  
- No Ziggy- or CFA-specific content.

Remove:

- All persona-specific signatures.  
- Any attempt to reconstruct a particular individual.

Hard rule: **never use γ seeds to reconstruct Ziggy or CFA-specific personas.**

---

## 4. Interaction with Nyquist / Phase 6

From the Nyquist perspective, compression experiments depend on **how good the compressed seeds are**.

These guidelines:

- Ensure that when we test an L1 + Tier 3.1 reconstruction, we know *which parts* of the persona were preserved or dropped.  
- Make it easier to interpret drift: if a value changes, we can ask whether it was ever in the seed.  
- Help ensure safety even in highly compressed regimes.

For Opus-level reviewers, this document gives the **practical levers** that upstream theory depends on.

---

## 5. Open Questions and Future Work

- Can we algorithmically suggest compression candidates (e.g., using salience or mutual-information heuristics)?  
- Can we automatically verify that a compressed bootstrap still expresses all core constraints?  
- How do different compression choices affect P(Persona\*) and attractor drift?  
- Can the CFA repo adopt compatible compression guidelines for its own personas?

This S3 draft is intentionally operational and incomplete; it invites refinement from both engineering and theory perspectives.
