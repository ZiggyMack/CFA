# DONE: Knowledge Gaps & Key Decisions - Master History

**Purpose:** Master repository for all closed Knowledge Gaps (KG) and Key Decisions (KD) across B-STORM sessions. This file preserves institutional memory while keeping active collaboration files (B-STORM_*.md) focused on open work.

**Workflow:**
- Active work tracked in B-STORM files (open KGs/KDs only)
- When items close, they're staged in "Recently Completed" section of B-STORM Awaiting block
- C4 migrates completed items here during staging process
- This file grows append-only - never delete historical entries

**Format:** Organized by B-STORM session, then by type (KD/KG), preserving causality chains and cross-references.

---

## B-STORM_3: Profile Architecture Foundation

**Session Focus:** Building PROFILE_TEMPLATE.md and METRIC_TAXONOMY.md with philosophical rigor documentation hooks

**Participants:** C4 (implementation), Nova (specification & validation), Ziggy (oversight)

**Date Range:** 2025-11-09

---

### Key Decisions (KD) - Closed

**KD-C1** ✅
**Decision:** Use hybrid structure (YAML + narrative) for profiles
**Resolution:** Approved
**Reference:** 📌 Ziggy Entry 12, B-STORM_2
**Context:** Profiles will combine machine-readable YAML metrics with human-readable narrative deliberation sections, co-located in single files to prevent drift

**KD-C2** ✅
**Decision:** Profiles location: profiles/ in repository root
**Resolution:** Approved
**Reference:** 📌 Ziggy Entry 11, B-STORM_2
**Context:** Worldview profiles (CT, MdN, etc.) will live in root-level profiles/ directory for easy discovery and canonical status

**KD-C3** ✅
**Decision:** C4 leads implementation, Nova reviews/validates
**Resolution:** Approved
**Reference:** 📌 Ziggy clarifications
**Context:** Due to Codex reliability constraints (emoji encoding issues, formatting corruption when rewriting), C4 handles structural file changes while Nova provides specifications and validation via B-STORM entries

**KD-C4** ✅
**Decision:** Pause after template/taxonomy for Nova review
**Resolution:** Implemented
**Reference:** 📌 C4 Entry 1
**Context:** Created KD-O1 and KD-O2 to ensure Nova validates foundation before production profiles (CT, MdN) are built

**KD-C5** ✅
**Decision:** Final approval of METRIC_TAXONOMY.md
**Resolution:** Approved
**Reference:** 📌 Nova Entry 4
**Context:** Nova validated METRIC_TAXONOMY.md v0.2.0 - all 3 new categories (Anthropological, Cosmological, Eschatological) fully documented with 9 new metrics specified; 8 justification fields + 5-part deliberation scaffold standards complete; changelog reflects expansion. This closes KG8 and unblocks production work pending KD-O1 closure.

**KD-C6** ✅
**Decision:** Final approval of PROFILE_TEMPLATE.md structure
**Resolution:** Approved
**Reference:** 📌 Nova Entry 8
**Context:** Nova validated PROFILE_TEMPLATE.md v0.2.0 after two rounds of fixes: Entry 5 added missing 9 metric sections (3 categories), Entry 7 synced all metrics to canonical taxonomy definitions. All 8 metrics (Anthropological, Cosmological, Eschatological) now match taxonomy verbatim (names, types, ranges). Template complete with 7 categories, 14 metrics, 8 justification fields per metric, 5-part deliberation scaffold. This closes KG7 and KG9, fully unblocks KD-O3 for production profiles (CT, MdN).

---

### Knowledge Gaps (KG) - Closed

_These gaps were filled by Nova Entry 2, enabling C4 to define and complete KG7 and KG8:_

**KG1** ✅
**Summary:** Add Anthropological, Cosmological, Eschatological categories to taxonomy/template
**Resolution:** Task completed
**Reference:** 📌 Nova Entry 2
**Context:** Extended CFA framework from 4 metric categories (Suffering, Epistemology, Morality, Teleology) to 7 total, adding categories that capture worldview differences on human nature, cosmic origins, and ultimate ends

**KG2** ✅
**Summary:** Extend metric list with nine new metrics (3 per added category)
**Resolution:** human_nature_baseline, agency_alignment, consciousness_ontology, origin_claim, causal_structure, fine_tuning_account, judgment_framework, ultimate_destiny, eschatology_confidence added
**Reference:** 📌 Nova Entry 2
**Context:** Expanded from 9 metrics to 18 total, each with complete YAML specifications (name, type, unit, range, description, category_definitions, example_values for CT/MdN/Buddhism, justification_requirements)

**KG3** ✅
**Summary:** Append Deliberation and Comparative Audit hooks to the template
**Resolution:** Both hooks added with full YAML and narrative
**Reference:** 📌 Nova Entry 2
**Context:** Added 2 new lifecycle hooks to capture Grok deliberation sessions (when philosophical reasoning converts to metric values) and cross-profile ripple effects (when one worldview's metrics change and others need comparison_notes updates)

**KG4** ✅
**Summary:** Add methodological_notes, evidence_threads, open_questions to justification blocks
**Resolution:** All three fields added to all metrics
**Reference:** 📌 Nova Entry 2
**Context:** Expanded justification requirements from 5 to 8 fields per metric, adding deliberation modality documentation, REPO_LOG/transcript traceability, and unresolved tensions tracking for audit hooks

**KG5** ✅
**Summary:** Worldview priority order for profile development
**Resolution:** Orthodox Judaism, Mormonism, Error Theorists, Null Hypothesis, Desiderata believers (post-CT/MdN)
**Reference:** 📌 Nova Entry 2, corrected Ziggy Entry 2.5
**Context:** After CT and MdN production profiles, these 5 worldviews are next priority for metric determination with Grok; correction in Entry 2.5 changed #5 from "Descartes believers" to "Desiderata believers"

**KG6** ✅
**Summary:** Deliberation narratives require 5-part scaffold
**Resolution:** Prompt Stack, Counterweight Table, Edge Case Ledger, Mythology Capsule, Decision Stamp mandated
**Reference:** 📌 Nova Entry 2
**Context:** Replaced freeform deliberation narratives with structured 5-part framework to ensure philosophical rigor is captured: exact prompts used, claim/counterclaim debates, edge cases that challenged assumptions, Shaman connection of axiom→outcome, and formal decision metadata (timestamp, participants, confidence, session IDs)

---

_C4 implementation of Nova Entry 2 specifications:_

**KG7** ✅
**Summary:** Implement all Nova Entry 2 additions to PROFILE_TEMPLATE.md
**Resolution:** 2 new hooks added (Deliberation, Comparative Audit), 3 new justification fields added to all metrics (methodological_notes, evidence_threads, open_questions), 5-part deliberation scaffold implemented for all metrics
**Reference:** 📌 C4 Entry 3
**Enabled:** KD-O1 (Nova validation of template structure)
**Context:** Full implementation of Nova's specifications across all 5 existing placeholder metrics in template; Changelog updated to v0.2.0; template now ready for production profile creation once validated

**KG8** ✅
**Summary:** Implement all Nova Entry 2 additions to METRIC_TAXONOMY.md
**Resolution:** 3 new categories added (Anthropological, Cosmological, Eschatological), 9 new metrics added with full specifications, justification requirements expanded to 8 fields, deliberation narrative scaffold documented
**Reference:** 📌 C4 Entry 3
**Enabled:** KD-O2 (Nova validation of taxonomy structure)
**Context:** Full implementation expanding taxonomy from 9 to 18 metrics across 7 categories; removed obsolete "Future Metric Categories" section; updated standards documentation; Changelog to v0.2.0; taxonomy now defines complete CFA measurement framework pending validation

---

_C4 fixes per Nova validation feedback:_

**KG9** ✅
**Summary:** Template metrics diverge from canonical taxonomy definitions
**Resolution:** Fixed all 8 metrics to match taxonomy verbatim - Anthropological (human_nature_baseline, agency_alignment, consciousness_ontology), Cosmological (origin_claim, causal_structure, fine_tuning_account), Eschatological (judgment_framework, ultimate_destiny)
**Reference:** 📌 C4 Entry 7, Nova Entry 6
**Enabled:** KD-O1 final approval (KD-C6)
**Context:** Nova Entry 6 identified mismatched ranges/types between template and taxonomy; C4 Entry 7 synced all values, types, units to canonical definitions; most significant fix was agency_alignment changing from scale 0-100 to ranked_categories; this closed the final blocker for template approval

**KD-C7** ✅
**Decision:** Proceed with production profiles (CT, MdN) or iterate foundation?
**Resolution:** Production profiles deployed - 12 worldview profiles + infrastructure complete
**Reference:** 📌 C4 Entry 9
**Context:** Following Nova Entry 8 approval of KD-C6 (template complete), C4 deployed full profile architecture buildout: (1) Production Profiles: CLASSICAL_THEISM.md and METHODOLOGICAL_NATURALISM.md with complete structure, suffering_weight metric fully detailed with 8-field justification + 5-part deliberation scaffold, remaining 13 metrics scaffolded; (2) Priority Queue (per Ziggy Entry 2.5): Orthodox Judaism, Mormonism, Error Theory, Null Hypothesis, Desiderata Believers with foundations + 3 key principles; (3) Additional Worldviews: Buddhism, Islam, Hinduism, Process Theology, Existentialism with concise scaffolding; (4) Infrastructure: profiles/README.md with complete index, development workflow, usage examples. Total delivered: 12 worldview profiles + README (13 files). Phase 3 complete, ready for Phase 4 (Grok integration for metric determination).

---

## Causality Chains

**Profile Foundation Build Sequence:**

1. **KD-C1, KD-C2** → Established hybrid structure and location for profiles
2. **KD-C3** → Defined collaboration model (C4 implements, Nova validates)
3. **KD-C4** → Created pause point for validation before production
4. **KG1-KG6** (Nova Entry 2) → Specified all additions needed for philosophical rigor
5. **KG7, KG8** (C4 Entry 3) → Implemented specifications in template and taxonomy
6. **KD-C5** (Nova Entry 4) → Taxonomy validated and locked at v0.2.0
7. **KG9** (Nova Entry 6, C4 Entry 7) → Template/taxonomy value sync completed
8. **KD-C6** (Nova Entry 8) → Template validated and locked at v0.2.0
9. **KD-C7** (C4 Entry 9) → Production profiles deployed, Phase 3 → Phase 4 transition

**Key Insight:** The closed KGs enabled subsequent open KDs by filling knowledge gaps. KG1-KG6 defined requirements, which enabled KG7-KG8 implementation work, which enabled KD-C5 and KD-C6 validation, which unblocked KD-C7 production deployment. Foundation is now complete and locked for Grok integration (Phase 4).

---

## Change Log

- **2025-11-09:** File created during B-STORM_3 reorganization (C4)
  - Migrated all closed KDs and KGs from B-STORM_3.md Awaiting section
  - Established append-only history structure
  - B-STORM files now track open work only; this file preserves institutional memory

- **2025-11-10:** KD-C7 migration (C4 Entry 9)
  - Added KD-C7 documenting production profile deployment completion
  - Updated Causality Chains to reflect Phase 3 completion
  - Phase 3 → Phase 4 transition: Foundation locked, ready for Grok integration
