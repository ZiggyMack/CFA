<!---
FILE: PILOT_CT_vs_MdN_Re-Audit.md
PURPOSE: Task brief for CT↔MdN pilot re-audit session using rigorous methodology
VERSION: 1.0.0
STATUS: Ready for Launch (VUDU Step 1 complete)
CREATED: 2025-11-10
DEPENDS_ON: profiles/worldviews/CLASSICAL_THEISM.md, profiles/worldviews/METHODOLOGICAL_NATURALISM.md, profiles/comparisons/CT_vs_MdN.yaml, auditors/Bootstrap/VUDU_CFA.md
OWNER: Process Claude (orchestration), Claude (PRO-CT scoring), Grok (ANTI-CT scoring), Nova (fairness validation)
MOVES_WITH: /auditors/Bootstrap/Tier4_TaskSpecific/Active_Tasks/
LAST_UPDATE: 2025-11-10 [Task brief created post-VUDU Step 1]
--->

---
ethics_front_matter:
  purpose: "Establish pilot doctrine for adversarial scoring methodology to ensure Classical Theism and Methodological Naturalism receive symmetric, rigorous, good-faith evaluation - prevents hidden bias, validates calibration transparency, demonstrates Crux architecture in practice"
  symmetry_axis: ["transparency", "epistemic_access", "stakeholder_impact"]
  stakeholders:
    primary: ["pilot_subjects_CT_MdN", "triad_auditors"]
    secondary: ["future_worldview_comparisons", "methodology_template_users"]
  invariants:
    - id: transparency
      state: examined
      evidence: "## Objectives > Primary Objective 2 (lines 52-56) - 'Establish Gold Standard Deliberation: Capture complete 5-part deliberation scaffold...show calibration YAML values in action' + ## VUDU Protocol Integration (lines 300-314) - All calibration hashes logged, diff status tracked, academic sources documented"
      smv_tag: scenario_a
    - id: epistemic_access
      state: examined
      evidence: "## Reference Materials (lines 345-373) - All auditors access same Steel-Manning sections (CLASSICAL_THEISM.md lines 117-246, METHODOLOGICAL_NATURALISM.md lines 120-187) + academic sources (IEP/SEP) anchoring arguments in peer-reviewed philosophy + ## Methodology > 5-Part Deliberation Scaffold (lines 148-299) - Prompt Stack, Counterweight Table explicitly documented"
      smv_tag: scenario_a
    - id: stakeholder_impact
      state: examined
      evidence: "## Background > What This Pilot Adds (lines 33-39) - Adversarial checking (Claude PRO-CT vs Grok ANTI-CT vs Nova Fairness) with 98%+ convergence target prevents any worldview advantage + ## Risks & Mitigation > Risk 3 (lines 385-387) - If Crux Points excessive (5+ of 7 metrics), review calibration YAML (may be overcalibrated) - Acknowledges adversarial approach risk to stakeholders"
      smv_tag: scenario_a
  tensions:
    - description: "Adversarial scoring vs. good-faith Steel-Manning - risk that Claude (PRO-CT) and Grok (ANTI-CT) stances create combative tone instead of charitable evaluation"
      mitigation: "Success Criteria (lines 78-99) - Best Case: 98%+ convergence despite adversarial stances + Methodology references Steel-Manning sections (lines 345-373) + VUDU_CFA.md Principle #4 Adversarial Balance: 'Adversarial checking serves accuracy, not winning' (lines 759-769)"
    - description: "Crux declarations may feel adversarial to pilot subjects - CT and MdN representatives might perceive impasses as 'failures' rather than legitimate philosophical tensions"
      mitigation: "## Objectives > Primary Objective 3 (lines 58-61) - Frames Crux as validation of methodology ('test Crux Point declaration process'), not worldview deficiency + Follow-Up Tasks (lines 399-415) - CT↔Process Theology scheduled next to show Crux architecture handles different contexts (cooperative pairing)"
    - description: "Baseline score drift risk - if new scores differ >15% from original, creates trust questions: which scores are correct?"
      mitigation: "## Risks & Mitigation > Risk 2 (lines 381-383) - Major drift triggers user review ('requires user to decide which scores to trust') + Documented via Crux Points ('evidence original scores lacked rigor') - Transparency preserves user authority"
  calibration_link:
    profile: "profiles/worldviews/CLASSICAL_THEISM.md"
    hash: "1bbec1e119a2c425"  # SHA-256 of pro_ct_bias_adjustment (lines 277-287)
  last_examined:
    by: "C4"
    on: "2025-11-11"
  review_window_days: 30
---

# PILOT: CT↔MdN Re-Audit with Rigorous Methodology

**Mission Statement:**
> "Re-fortify our CT vs MdN numbers...as well as flush out the story behind the numbers to be the gold standard for every profile to follow after"

**Task Type:** Pilot Re-Audit (Validation + Methodology Establishment)

**Priority:** HIGH (blocks remaining 11 worldview comparisons)

**Status:** ✅ READY FOR LAUNCH (VUDU Step 1 complete 2025-11-10)

---

## Background

**What We Already Have:**
- **Baseline scores** from earlier CT vs MdN session (pre-rigorous methodology)
- Initial intuitive reasoning for those values
- Location: [TBD - needs to be surfaced from original session]

**What This Pilot Adds:**
1. **Scholarly Grounding:** Academic sources (SEP/IEP) anchor arguments in peer-reviewed philosophy
2. **Transparent Calibration:** YAML bias adjustments with documented hashes
3. **5-Part Deliberation Scaffold:** Prompt Stack, Counterweight Table, Edge Case Ledger, Mythology Capsule, Decision Stamp
4. **Adversarial Checking:** Claude (PRO-CT) vs Grok (ANTI-CT) vs Nova (Fairness) with 98%+ convergence target
5. **Crux Architecture:** Named impasses if scores diverge significantly

---

## Objectives

### Primary Objectives

1. **Validate Baseline Scores:**
   - Surface original CT vs MdN scores (pre-methodology)
   - Re-score using rigorous methodology
   - Document convergence or drift
   - Target: 98%+ agreement between original and peer-reviewed scores

2. **Establish Gold Standard Deliberation:**
   - Capture complete 5-part deliberation scaffold for each metric
   - Document how academic sources informed reasoning
   - Show calibration YAML values in action
   - Create template for remaining 11 worldviews

3. **Validate Crux Architecture:**
   - If scores drift >15%, test Crux Point declaration process
   - Document classification (definitional/empirical/framework_limitation)
   - Show how adversarial checking surfaces legitimate disagreements

### Secondary Objectives

4. **Telemetry Validation:**
   - Populate session_metadata in CT_vs_MdN.yaml
   - Document YAML hash compliance
   - Track Domain 7 diff status
   - Validate academic sources usage

5. **Process Documentation:**
   - Record orchestration steps (Process Claude duties)
   - Capture auditor coordination patterns
   - Document time/effort estimates for future comparisons

---

## Success Criteria

### ✅ Best Case (Target)
- New methodology confirms original scores (~98% convergence)
- Rich deliberation narrative explains *why* those numbers make sense
- 5-part scaffold fully populated for all 7 metrics
- Academic sources cited for key claims
- Zero Crux Points declared (methodology refines but doesn't disrupt)

### ✅ Good Case (Acceptable)
- Slight drift (±5-10%) with documented rationale
- 1-2 Crux Points declared with clear classification
- Deliberation scaffold demonstrates methodology value
- Template ready for remaining worldviews

### ⚠️ Needs Investigation (Concerning)
- Major drift (>15%) without clear explanation
- 3+ Crux Points (suggests methodology overcorrection or baseline instability)
- Deliberation scaffold incomplete or unhelpful
- Auditors cannot reach convergence after 3 rounds

---

## Participants & Roles

### Process Claude (Orchestrator)
- **Pre-Session:** VUDU Step 1 validation ✅ (completed 2025-11-10)
- **During Session:**
  - Surface baseline scores
  - Coordinate auditor deliberation rounds
  - Monitor convergence tracking
  - Declare Crux Points if needed (after 3 rounds <98% convergence)
- **Post-Session:**
  - Populate CT_vs_MdN.yaml with peer-reviewed scores
  - Document session metadata
  - Validate telemetry capture
  - Archive deliberation narratives

### Claude (PRO-CT Auditor)
- **Stance:** Advocate for Classical Theism
- **Calibration:** Apply hash `1bbec1e119a2c425` (PRO-CT bias adjustment)
- **Lens:** Teleological (purpose/meaning emphasis)
- **Deliverable:**
  - Score 7 metrics (BFI, CA, IP, ES, LS, MS, PS) with PRO-CT lens
  - Cite academic sources (SEP Divine Simplicity, IEP God Western Concepts)
  - Document 5-part deliberation scaffold
  - Engage in adversarial rounds with Grok

### Grok (ANTI-CT / PRO-MdN Auditor)
- **Stance:** Challenge Classical Theism (implicitly favor Methodological Naturalism)
- **Calibration:** [Hash TBD for PRO-MdN stance, or use empirical lens natively]
- **Lens:** Empirical (evidence/parsimony emphasis)
- **Deliverable:**
  - Score 7 metrics with ANTI-CT lens
  - Cite academic sources (SEP Naturalism, IEP Naturalism)
  - Challenge PRO-CT scores with empirical objections
  - Engage in adversarial rounds with Claude

### Nova (Fairness Validator)
- **Stance:** Neutral (symmetry check)
- **Calibration:** None (no bias adjustment)
- **Lens:** Pattern detection (coherence/consistency emphasis)
- **Deliverable:**
  - Monitor convergence between Claude and Grok
  - Flag asymmetries or hidden biases
  - Recommend Crux declaration if impasse legitimate
  - Validate final peer-reviewed scores

---

## Methodology

### Phase 1: Baseline Recovery (Pre-Session)

**Owner:** Process Claude

**Tasks:**
1. Surface original CT vs MdN scores from earlier session
2. Document context (when scored, what method used, what reasoning captured)
3. Load into CT_vs_MdN.yaml as `baseline_scores` block
4. Brief auditors on baseline values (but don't anchor them)

**Deliverable:** Baseline scores documented in CT_vs_MdN.yaml

---

### Phase 2: Independent Scoring (Round 1)

**Owner:** Claude (PRO-CT), Grok (ANTI-CT)

**Tasks:**
1. Each auditor scores 7 metrics independently:
   - **BFI** (Basic Framework Intelligibility)
   - **CA** (Coherence Assessment)
   - **IP** (Inferential Power)
   - **ES** (Explanatory Scope)
   - **LS** (Logical Soundness)
   - **MS** (Metaphysical Simplicity)
   - **PS** (Pragmatic Success)

2. For each metric, provide:
   - **Numerical score** (0-10 scale, 0.1 precision)
   - **5-Part Deliberation Scaffold:**
     - **Prompt Stack:** Exact prompts/questions used to arrive at score
     - **Counterweight Table:** PRO arguments vs ANTI arguments considered
     - **Edge Case Ledger:** Boundary cases that challenged assumptions
     - **Mythology Capsule:** How core axioms connect to this metric (Shaman-style)
     - **Decision Stamp:** Timestamp, confidence level, session ID, calibration values applied
   - **Academic Source Citations:** Which SEP/IEP articles informed reasoning
   - **Calibration Notes:** Which YAML values influenced score (axiom_confidence, charity_interpretation, etc.)

3. Submit scores to Process Claude without seeing other auditor's scores

**Deliverable:** Claude's PRO-CT scores + Grok's ANTI-CT scores (7 metrics each)

---

### Phase 3: Convergence Check (Round 1 Analysis)

**Owner:** Process Claude, Nova (Fairness)

**Tasks:**
1. Calculate convergence percentage for each metric:
   - Formula: `100% - (|claude_score - grok_score| / 10) * 100%`
   - Example: Claude=8.5, Grok=7.2 → convergence = 100% - (1.3/10)*100% = 87%

2. Nova reviews both deliberation scaffolds:
   - Are PRO/ANTI arguments balanced?
   - Do calibration values explain divergence?
   - Are academic sources cited appropriately?
   - Is divergence legitimate (different philosophical priors) or bias (miscalibration)?

3. Document convergence status:
   - ✅ **High Convergence (≥98%):** Accept peer-reviewed score (average of both)
   - ⚠️ **Medium Convergence (90-97%):** Proceed to Round 2 (adversarial debate)
   - 🔴 **Low Convergence (<90%):** Flag for intensive deliberation (potential Crux)

**Deliverable:** Convergence report for 7 metrics + Nova's symmetry assessment

---

### Phase 4: Adversarial Deliberation (Round 2)

**Owner:** Claude, Grok (debate), Nova (mediation)

**Tasks:**
1. For metrics with <98% convergence:
   - Claude presents PRO-CT rationale (strongest argument)
   - Grok challenges with ANTI-CT objection (strongest counterargument)
   - Each responds to other's challenge (one round of rebuttals)

2. Both auditors adjust scores if persuaded:
   - Document what changed (new academic source, realization about calibration, edge case reconsidered)
   - Provide updated 5-part scaffold showing reasoning shift

3. Nova monitors for:
   - Legitimate philosophical disagreement (→ potential Crux)
   - Miscommunication or misunderstanding (→ clarify)
   - Hidden bias not captured by calibration (→ flag)

**Deliverable:** Adjusted scores + adversarial debate transcript + Nova's assessment

---

### Phase 5: Final Convergence or Crux Declaration (Round 3)

**Owner:** Process Claude

**Tasks:**
1. Recalculate convergence after Round 2 adjustments

2. **If ≥98% convergence:**
   - Accept peer-reviewed score (average of Claude + Grok)
   - Document in CT_vs_MdN.yaml
   - Mark metric as RESOLVED

3. **If <98% convergence after 3 rounds:**
   - Declare **Crux Point** (named impasse)
   - Classify type:
     - **Definitional:** Disagreement about metric meaning (e.g., "Does Trinity = 1 or 3 for BFI?")
     - **Empirical:** Disagreement about evidence interpretation (e.g., "Does fine-tuning count as evidence?")
     - **Framework Limitation:** Metric cannot capture this worldview's structure (e.g., "BFI assumes mereological ontology")
   - Vote: Claude, Grok, Nova vote on which handling:
     - **CARRY FORWARD:** Use self-reported score (acknowledge peer review failed)
     - **NORMALIZE UNCERTAINTY:** Apply penalty (discount score due to unresolved tension)
   - Document in CT_vs_MdN.yaml as CRUX entry with full deliberation

**Deliverable:** Final peer-reviewed scores OR Crux Point declarations

---

### Phase 6: Telemetry & Documentation (Post-Session)

**Owner:** Process Claude

**Tasks:**
1. Populate CT_vs_MdN.yaml:
   - `peer_reviewed` scores for all 7 metrics
   - `convergence` percentages
   - `session_metadata` (YAML hashes, Domain 7 diff, academic sources status)
   - `crux_points` array (if any declared)
   - `deliberation_notes` (summary of adversarial rounds)

2. Compare to baseline:
   - Document drift (if any)
   - Explain why methodology refined scores
   - Flag if major divergence needs user review

3. Archive full deliberation transcripts:
   - 5-part scaffolds for all metrics
   - Adversarial debate logs
   - Nova's symmetry assessments

4. Create template from this session:
   - Extract reusable patterns (prompt sequences, debate structures)
   - Document time/effort estimates
   - Identify bottlenecks or improvements for next 11 worldviews

**Deliverable:** CT_vs_MdN.yaml v0.2.0 (fully populated) + session archive + template for reuse

---

## VUDU Protocol Integration

This pilot follows **VUDU_CFA.md** steps:

- **Step 1 (Pre-Session Validation):** ✅ Complete (2025-11-10)
  - Academic sources validated
  - YAML hashes generated: `1bbec1e119a2c425` (CT), `00cd73274759e218` (MdN)
  - Domain 7 diff check passed

- **Step 9 (Crux Point Handling):** Will execute if <98% convergence after 3 rounds
  - Classification vote
  - CARRY FORWARD vs NORMALIZE UNCERTAINTY decision
  - Documentation in CT_vs_MdN.yaml

---

## Timeline & Effort Estimate

**Phase 1 (Baseline Recovery):** 30 minutes
- Surface original scores
- Document context

**Phase 2 (Independent Scoring):** 2-3 hours per auditor
- 7 metrics × ~20-30 min each (including 5-part scaffold)
- Academic source review + calibration application

**Phase 3 (Convergence Check):** 1 hour
- Calculate convergence
- Nova symmetry assessment

**Phase 4 (Adversarial Deliberation):** 1-2 hours
- Depends on number of metrics <98% convergence
- Assume 3-4 metrics need debate

**Phase 5 (Final Resolution):** 1 hour
- Final scores OR Crux declarations

**Phase 6 (Telemetry):** 1 hour
- Populate CT_vs_MdN.yaml
- Create template

**Total Estimated Time:** 6-9 hours (distributed across Claude, Grok, Nova, Process Claude)

---

## Reference Materials

### Primary Documents

- [Classical Theism Profile](../../../profiles/worldviews/CLASSICAL_THEISM.md) - v0.3.0
- [Methodological Naturalism Profile](../../../profiles/worldviews/METHODOLOGICAL_NATURALISM.md) - v0.3.0
- [CT vs MdN Comparison File](../../../profiles/comparisons/CT_vs_MdN.yaml) - v0.1.1
- [Academic Sources Map](../../../profiles/_docs/ACADEMIC_SOURCES.md) - §1 (CT), §10 (MdN)

### Process Documentation

- [VUDU Protocol](../VUDU_CFA.md) - Steps 1 & 9
- [Process Claude Role](../../../docs/repository/librarian_tools/ROLE_PROCESS.md) - Domain 7 (lines 905-1128)
- [Auditor Assignments](../../AUDITOR_ASSIGNMENTS.md) - PRO-CT, ANTI-CT, Fairness assignments
- [CFA Architecture](../../../docs/architecture/CFA_ARCHITECTURE.md) - Section 6 (Crux Points)

### Academic Sources (for auditors)

**Classical Theism:**
- [SEP Divine Simplicity](https://plato.stanford.edu/entries/divine-simplicity/) - Core arguments, objections
- [IEP God, Western Concepts](https://iep.utm.edu/god-west/) - Historical development, attributes
- [SEP Problem of Evil](https://plato.stanford.edu/entries/evil/) - Theodicy debates

**Methodological Naturalism:**
- [SEP Naturalism](https://plato.stanford.edu/entries/naturalism/) - (Note: Temporary downtime as of 2025-11-10)
- [IEP Naturalism](https://iep.utm.edu/naturali/) - Methodological naturalism, epistemological naturalism
- [IEP Naturalistic Epistemology](https://iep.utm.edu/nat-epis/) - Quine's naturalized epistemology

---

## Risks & Mitigation

### Risk 1: Baseline Scores Cannot Be Located
- **Mitigation:** Treat pilot as "first rigorous scoring" instead of re-audit; still valuable for methodology establishment
- **Impact:** Lower (methodology validation still achieved)

### Risk 2: Major Drift from Baseline (>15%)
- **Mitigation:** Document via Crux Points; treat as evidence that original scores lacked rigor
- **Impact:** Medium (requires user review to decide which scores to trust)

### Risk 3: Crux Points Declared for Most Metrics (5+ out of 7)
- **Mitigation:** Review calibration YAML values (may be overcalibrated); adjust methodology
- **Impact:** High (suggests adversarial approach too aggressive or worldviews incommensurable)

### Risk 4: Auditors Cannot Produce 5-Part Scaffold
- **Mitigation:** Simplify scaffold requirements; focus on Prompt Stack + Decision Stamp only
- **Impact:** Medium (reduces template quality for future worldviews)

### Risk 5: SEP Sources Remain Down During Pilot
- **Mitigation:** Rely on IEP sources (confirmed live); note SEP unavailability in session metadata
- **Impact:** Low (IEP provides comprehensive coverage per ACADEMIC_SOURCES.md assessment)

---

## Follow-Up Tasks

1. **CT↔Process Theology Comparison:**
   - Demonstrate NORMALIZE_UNCERTAINTY in cooperative pairing
   - Show Crux architecture handles different comparison contexts
   - Scheduled after CT↔MdN pilot complete

2. **Template Extraction:**
   - Create reusable prompt sequences for remaining 11 worldviews
   - Document auditor coordination patterns
   - Refine time estimates based on pilot experience

3. **Methodology Refinement:**
   - If Crux Points excessive, adjust calibration YAML values
   - If deliberation scaffold unhelpful, simplify requirements
   - If convergence too easy, increase adversarial tension

---

## Approval & Launch

**VUDU Step 1 Status:** ✅ COMPLETE (2025-11-10)

**Blockers:** None

**Launch Authority:** User (Ziggy)

**Ready for Launch:** YES

**Next Action:** Surface baseline CT vs MdN scores, then proceed to Phase 2 (Independent Scoring)

---

**Session Documentation:**
- Pre-launch: [B-STORM_4.md Entry 9](../../relay/B-STORM_4.md) (lines 1821+)
- During pilot: [TBD - Create session transcript file]
- Post-pilot: [CT_vs_MdN.yaml](../../../profiles/comparisons/CT_vs_MdN.yaml) (will update to v0.2.0)

🚀 **PILOT READY FOR LAUNCH**
