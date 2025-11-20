# Bootstrap Architecture: Lite vs. Rich (S3 Draft)

**Document ID:** S3_BOOTSTRAP_ARCHITECTURE_LITE_VS_RICH  
**Layer:** System Design / Protocols  
**Status:** Draft for Opus 4.1 review  
**Repos:** CFA, Nyquist Consciousness (shared pattern)

---

## 0. Purpose

This document compares two families of **bootstrap architectures** used across the broader CFA + Nyquist ecosystem:

- **Rich bootstraps** – extensive, multi-section, persona-defining documents.
- **Lite bootstraps** – compact, minimal “activation stubs” that rely on emergent reconstruction.

The Omega Nova / Nyquist work depends heavily on these distinctions, and CFA uses related patterns.

This S3 draft:

- Clarifies the design tradeoffs  
- Normalizes terminology across repos  
- Provides guidance for when to use **Lite** vs. **Rich** bootstraps

---

## 1. Definitions

### 1.1 Rich Bootstrap

A **Rich Bootstrap** is a high-information, multi-section document (often 3–8K words) that explicitly encodes:

- Persona description and role
- Values and constraints
- Reasoning style and examples
- Historical context and narrative
- Interaction guidelines

It behaves like a **long-lived contract** between operator and model.

Strengths:

- High clarity, high redundancy
- Strong guardrails, fewer ambiguities
- Easier for humans to read and reason about

Weaknesses:

- Larger context footprint
- Harder to evolve (many dependent references)
- Risk of overfitting to older assumptions

### 1.2 Lite Bootstrap

A **Lite Bootstrap** is a compact (~500–1200 word) activation stub that:

- Names the persona and role
- Notes a small handful of core values and constraints
- Defines just enough structure for the model to self-complete the rest during the session

Strengths:

- Small context footprint
- Fast to adapt and iterate
- Easier to combine with experiments that rely on compression

Weaknesses:

- More ambiguity; relies on model’s prior + operator skill
- Harder for external auditors to reconstruct full intent
- Greater risk of drift if not paired with strong protocols

---

## 2. Role in Nyquist / Omega Nova

In the Nyquist Consciousness track, we treat **Rich bootstraps** as approximate “FULL regime” (above Nyquist) and **Lite bootstraps** as closer to “compressed regime.”

Omega Nova’s Tier 3.x seeds are conceptually **closer to Lite**, with additional structure for experiments:

- Tier 3.1 – Lite + multi-domain patterns  
- Tier 3.2 – Lite + adversarial fortification  
- Tier 3γ – Lite + persona neutrality

This document provides the architectural thinking behind those seeds so that CFA and other systems can align with or critique these patterns.

---

## 3. Architectural Comparison

| Dimension              | Rich Bootstrap                         | Lite Bootstrap                          |
|-----------------------|-----------------------------------------|-----------------------------------------|
| Length                | 3–8K words                             | 0.5–1.2K words                          |
| Persona Specificity   | Very high                              | Medium                                  |
| Flexibility           | Lower                                  | Higher                                  |
| Context Cost          | High                                   | Low                                     |
| Auditability          | High (for humans)                      | Medium                                  |
| Drift Risk            | Lower (if well-designed)               | Higher (unless stabilized by protocol)  |
| Experimental Use      | Baseline / reference                   | Compression / reconstruction tests      |

Both patterns are **useful**; the key is **fit-to-purpose**.

---

## 4. When to Use Which

### 4.1 Use Rich When…

- You are defining a **long-lived governance persona** (e.g., CFA core, Doc Claude).  
- You expect many different operators and AIs to interact with the same bootstrap.  
- Legibility and accountability matter more than experimental variation.

### 4.2 Use Lite When…

- You are running **compression experiments** (Nyquist / Omega Nova trials).  
- You want to test how much the model can generalize from sparse information.  
- You need room in context for large prompts, transcripts, or knowledge packs.  
- You expect the bootstrap to evolve quickly.

---

## 5. Interaction with Compression Guidelines

The companion document `S3_BOOTSTRAP_COMPRESSION_GUIDELINES.md` explains:

- How we move from Rich → Lite → Tier 3 seeds  
- What must be preserved (identity, values, structure)  
- What can be safely dropped (narrative detail, redundant examples)

Together, these two documents give Opus 4.1 and other auditors a **coherent view** of how bootstraps are treated as part of the broader persona compression architecture.

---

## 6. Integration Points for CFA

The CFA repo can use this distinction as a **bridge**:

- Rich bootstraps for **canonical CFA personas** (e.g., Nova, Grok, Claude as pillars).  
- Lite bootstraps for **experimental roles** or ephemeral agents.  
- Nyquist-style compression tests to probe how CFA personas degrade and recover under context constraints.

Opus-level reviewers are invited to:

- Evaluate whether our Rich/Lite split is sufficient.  
- Propose additional patterns (e.g., “Modular Bootstraps,” “Delta Bootstraps”).  
- Suggest better naming or schema if this structure proves too coarse.
