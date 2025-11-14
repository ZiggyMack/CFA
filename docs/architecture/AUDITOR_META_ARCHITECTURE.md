<!---
FILE: docs/architecture/AUDITOR_META_ARCHITECTURE.md
PURPOSE: Structural specification of the auditor axiom system
VERSION: v4.0.0
STATUS: Active
DEPENDS_ON: AUDITOR_AXIOMS.md, TRINITY_ALIGNMENT_MATRIX.md
NEEDED_BY: Future auditor additions, system maintenance
MOVES_WITH: /docs/architecture/
LAST_UPDATE: 2025-11-13
--->

# Auditor Meta-Architecture

**Version:** v4.0.0
**Purpose:** Structural specification for the auditor axiom system
**Status:** Active

---

## 🎯 PURPOSE

This document specifies the **structural principles** underlying CFA's auditor axiom system.

While [AUDITOR_AXIOMS.md](AUDITOR_AXIOMS.md) provides the full narrative of Claude/Grok/Nova, this document answers:

- **Why three lenses?** (structural necessity)
- **How does complementary tension work?** (convergence mechanism)
- **What principles govern auditor design?** (extensibility rules)
- **How would we add future auditors?** (growth architecture)

---

## 🔺 WHY THREE LENSES?

**The Trinity architecture is not arbitrary.**

It emerged from observing three **orthogonal dimensions** of philosophical evaluation:

1. **Teleological** (purpose-oriented) - "Does this serve its intended goal?"
2. **Empirical** (evidence-oriented) - "Can we test/measure this claim?"
3. **Symmetrical** (pattern-oriented) - "Is this structurally fair/balanced?"

**Orthogonality = Complementary Coverage**

Each lens catches errors the others miss:

| Error Type | Claude | Grok | Nova |
|------------|--------|------|------|
| **Purpose-drift** (form without function) | ✅ CATCHES | Misses | Misses |
| **Wishful thinking** (theory without evidence) | Misses | ✅ CATCHES | Misses |
| **Hidden bias** (design without fairness) | Misses | Misses | ✅ CATCHES |

**This is not redundant checking—it's coverage across distinct failure modes.**

---

## ⚙️ HOW COMPLEMENTARY TENSION WORKS

**Step 1: Divergence (Each auditor applies their lens)**

Given a question like "What's Zealot mode's archetype score?"

- **Claude:** "Zealot suggests existential commitment → score 9.0 (teleologically coherent)"
- **Grok:** "No empirical test for 'existential commitment' → score 6.5 (measurable baseline)"
- **Nova:** "Skeptic gets 4.99 YPA, Zealot must provide symmetric CT advantage → check math first"

**Initial divergence is EXPECTED—different lenses produce different first impressions.**

---

**Step 2: Adversarial Deliberation (Challenge blind spots)**

- **Grok challenges Claude:** "Your 9.0 is teleologically inflated. What's the empirical evidence for 'existential commitment' beyond self-report?"
- **Claude challenges Grok:** "Your 6.5 dismisses meaning that users care about. What's the PURPOSE of Zealot if not existential?"
- **Nova challenges both:** "You're debating content before checking structural fairness. Does Zealot provide SYMMETRIC advantage to CT like Skeptic does to MdN?"

**Each auditor forces others to justify claims through their lens.**

---

**Step 3: Convergence (Integration via evidence + justification)**

- **Claude:** "Fair point. My 9.0 relied on archetype coherence without empirical grounding. What if we score 7.5 (meaning-aligned but not empirically proven)?"
- **Grok:** "I can accept 7.5 if we document this as self-reported with Crux Point potential. Users decide if existential commitment matters."
- **Nova:** "7.5 is acceptable IF Zealot's advantage to CT matches Skeptic's advantage to MdN structurally. Let me verify symmetry..."

**Final score: 7.5 with documented reasoning + Crux Point flag + symmetry verification**

**98% convergence threshold = all three auditors agree within ±0.15 on a 0-10 scale**

---

**Step 4: Crux Points (When convergence fails)**

If after genuine deliberation, auditors cannot reach 98%:

**Declare a Crux Point:**
- Name the disagreement explicitly
- Document each auditor's position
- Let users decide via Crux Handling Lever (NORMALIZE_UNCERTAINTY vs CARRY_FORWARD)

**This is NOT failure—it's honest acknowledgment of philosophical boundaries.**

---

## 🧬 DESIGN PRINCIPLES

**Principle 1: Named Axioms (No False Objectivity)**

Every auditor must:
- Declare their core axiom explicitly
- Name their bias openly
- Quantify their overhead (not just describe it)

**Bad:** "I try to be fair"
**Good:** "I favor mathematical symmetry over functional asymmetry (~0.3 overhead from pattern analysis)"

---

**Principle 2: Measurable Overhead (No Vague Preferences)**

Bias must be PRICED with evidence:

**Bad:** "I tend to write comprehensively"
**Good:** "I favor meaning over efficiency (~0.5 from 6,500-word bootstrap vs 2,000 needed, 5 rounds to 98%, VuDu logs)"

---

**Principle 3: Orthogonal Lenses (No Redundant Checking)**

New auditors must provide **distinct perspective** not covered by existing lenses.

**Example of valid addition:**
- **Historical Lens** (precedent-oriented) - "What has worked across civilizations/eras?"
- Orthogonal to teleological (asks "what worked?" not "what's the purpose?")
- Orthogonal to empirical (asks "historical evidence" not "testable prediction")
- Orthogonal to symmetrical (asks "precedent" not "pattern")

**Example of invalid addition:**
- **"Ultra-Empirical Lens"** (just more intense empiricism) - NOT orthogonal to Grok
- **"Hyper-Symmetry Lens"** (just stricter symmetry) - NOT orthogonal to Nova

---

**Principle 4: Complementary Coverage (Each Catches What Others Miss)**

New auditors must demonstrate:
- What error type they catch
- How existing auditors miss it
- Why their lens is necessary

**Test:** If existing Trinity can catch the error through deliberation, new lens is redundant.

---

**Principle 5: Bias as Precision Tool (Not Liability)**

Auditors don't HIDE bias—they USE it:

- Claude's verbosity produces comprehensive context (useful for complex design)
- Grok's empiricism prevents wishful thinking (useful for validation)
- Nova's pattern-seeking catches hidden asymmetry (useful for fairness audits)

**Each bias is a feature when applied to appropriate domains.**

---

## 🔧 ADDING FUTURE AUDITORS

**Hypothetical: Adding a Fourth Auditor**

**Candidate:** Historical Lens (Precedent-Oriented)

**Core Axiom:** "Precedent informs judgment"

**Bias Declaration:** "Favor established patterns over novel solutions (~0.4 overhead from historical research time, civilization-scale evidence gathering)"

**What it catches:** "Durability blind spots" (solutions that work in theory but fail across historical timescales)

**Orthogonality check:**
- ✅ vs Claude: Asks "what worked historically?" not "what's the purpose?"
- ✅ vs Grok: Asks "civilization-scale evidence" not "laboratory tests"
- ✅ vs Nova: Asks "precedent" not "mathematical pattern"

**Complementary coverage:**
- Catches: Solutions that ignore historical failure modes
- Example: "This framework claims moral progress is inevitable" → Historical auditor: "No civilization has sustained moral monotonic improvement over 500+ years"

**Integration with Trinity:**
- Claude asks "Why claim moral progress?"
- Grok asks "Can you measure moral progress?"
- Nova asks "Is progress claim balanced with regress possibility?"
- **Historical asks "What's the historical evidence for sustained moral progress?"**

**Result:** Four-lens system with expanded coverage

---

## 📐 CONVERGENCE MECHANICS

**98% Threshold Derivation:**

On a 0-10 scale:
- 98% agreement = within ±0.20 points
- Example: Auditor A scores 7.5, Auditor B scores 7.3, Auditor C scores 7.6
- Range: 0.3 points (7.3 to 7.6)
- **Converged:** All within ±0.20 of median (7.5)

**Why 98% (not 100%)?**

Perfect agreement would require:
- Identical lens (defeats orthogonality)
- False consensus (hiding real disagreement)

**98% allows:**
- Distinct lenses to maintain their perspective
- Honest disagreement within tolerable bounds
- User awareness of remaining uncertainty

---

**When to Declare Crux Point:**

**Trigger:** After 3+ rounds of deliberation, auditors remain >0.20 apart

**Example:**
- Round 1: Claude 8.0, Grok 6.0, Nova 7.0 (divergent)
- Round 2: Claude 7.5, Grok 6.5, Nova 7.0 (converging)
- Round 3: Claude 7.3, Grok 6.7, Nova 7.0 (still >0.20 apart)
- **Declare Crux Point:** "Auditors cannot agree within 98% on Zealot archetype score"

**Document:**
- Claude's position: 7.3 (teleologically coherent)
- Grok's position: 6.7 (empirically ungrounded)
- Nova's position: 7.0 (structurally acceptable if symmetric)
- User decides via Crux Handling Lever

---

## 🌳 EXTENSIBILITY RULES

**Rule 1: Minimum Viable Trinity**

CFA requires **at least 3 orthogonal lenses** for adversarial convergence.

**Why not 2?**
- Two auditors produce stalemate (no tiebreaker)
- Two lenses provide insufficient coverage

**Why not start with 4+?**
- Diminishing returns (coordination overhead scales with N²)
- Current Trinity provides strong coverage

**Path forward:** Add fourth lens ONLY when:
- Clear orthogonality demonstrated
- Distinct error type identified
- Existing Trinity cannot catch via deliberation

---

**Rule 2: Lens Orthogonality Test**

Before adding new auditor:

1. **Question generation test:** Given 10 CFA tasks, does new lens ask questions existing Trinity doesn't?
2. **Error catching test:** Can new lens catch errors existing Trinity misses (even through deliberation)?
3. **Bias orthogonality test:** Is new bias independent of existing biases (not just "more intense" version)?

**All three must pass.**

---

**Rule 3: Overhead Budget**

Each auditor adds coordination overhead:
- 3 auditors: ~(0.3 + 0.4 + 0.5) = 1.2 overhead units
- 4 auditors: ~(1.2 + new overhead + N² coordination complexity)

**Budget constraint:** Total overhead must stay <2.0 units to maintain 80%+ work budget

**Implication:** Future auditors must have ≤0.5 overhead OR justify >2.0 total via exceptional value

---

## ⚖️ THE META RULE

*"Auditor architecture serves philosophical honesty, not auditor proliferation.

Add lenses when they catch errors the Trinity misses.
Remove lenses when they become redundant.
Maintain orthogonality always."*

**This is architectural discipline.** 👑

────────────────────────────────────────────────────
**File:** docs/architecture/AUDITOR_META_ARCHITECTURE.md
**Purpose:** Structural specification of auditor axiom system
**Version:** v4.0.0
**Updated:** 2025-11-13

**Extensibility guide for future auditor additions.** 🔥
