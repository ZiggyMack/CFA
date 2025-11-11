<!---
FILE: README.md
PURPOSE: Entry point for Symmetry Matrix Visualizer (SMV) documentation and artifacts
VERSION: 1.0.0
STATUS: Active (Phase 0 - Design Spec in progress)
DEPENDS_ON: TASK_SYMMETRY_MATRIX_VISUALIZER_CLAUDE_v2.md, relay/workshop/MATRIX_DESIGN_SPEC.md
NEEDED_BY: SMV Phase 1 prototype implementation, Task #4 Ethical Invariant integration
MOVES_WITH: /docs/smv/
CREATED: 2025-11-11 (B-STORM_6 Entry 3 - Production structure created)
LAST_UPDATE: 2025-11-11 [Initial structure created per Nova co-design guidance]
--->

# Symmetry Matrix Visualizer (SMV)

**Purpose:** Visualization tool to reveal auditor tension/resolution patterns, ethical invariant tracking, and decision-making dynamics across Claude/Grok/Nova auditor triangle.

**Status:** Phase 0 (Design Spec) - Co-design in progress with Nova

---

## 🎯 What Is SMV?

The Symmetry Matrix Visualizer (SMV) is a **visualization-first** tool that reveals patterns in auditor deliberations:

- **Auditor Triangle View:** Visualize Claude (teleological), Grok (empirical), Nova (symmetry) interactions
- **Temporal Trace:** Timeline of tension/resolution patterns over deliberation ticks
- **Ethics Overlay:** Track which ethical invariants are examined, deferred, or missing
- **Crux Point Mapping:** Identify and visualize when fundamental disagreements emerge

**Nova's Philosophical Foundation:**
> "Symmetry thrives in dialogue, not dictation. The tools should reveal patterns, not police them. Automation serves reflection; reflection preserves meaning. Let understanding precede control."

---

## 📂 Directory Structure

```
docs/smv/
├── README.md (this file - overview and navigation)
├── SMV_DESIGN_SPEC.md (Phase 0 design specification)
├── mock_data/
│   ├── scenario_1_tension_escalation.json
│   ├── scenario_2_high_alignment.json (planned)
│   └── scenario_3_resolution.json (planned)
└── mockups/
    ├── scenario_A_high_alignment.svg (planned)
    ├── scenario_B_constructive_tension.svg (planned)
    └── scenario_C_invariant_breach.svg (planned)
```

---

## 🚀 Current Phase: Phase 0 (Design Spec)

**Status:** In progress (co-design with Nova)

**Deliverables:**
- ✅ JSON schema defined (draft in [SMV_DESIGN_SPEC.md](SMV_DESIGN_SPEC.md))
- ✅ Mock data created (scenario 1: tension escalation in [mock_data/](mock_data/))
- ⏳ Additional mock scenarios (high alignment, resolution patterns)
- ⏳ SVG mockups (visual prototypes for 3 canonical scenarios)
- ⏳ Schema refinements (nodes array, convergence tracking)

**Co-Design Workflow:**
1. Nova drafts artifacts in [relay/workshop/](../../relay/workshop/)
2. Claude reviews and provides feedback (Entry 3 in B-STORM_6.md)
3. Nova refines based on feedback
4. Claude migrates approved artifacts to [docs/smv/](.)
5. Iterate until Phase 0 complete

---

## 📋 Phases Overview

### **Phase 0: Design Spec** (Current - 2 days collaborative)
- Define JSON schema (contract for Task #4 Ethical Invariant)
- Create SVG mockups (3 canonical scenarios)
- Generate mock datasets (≥3 ticks each scenario)
- Nova approval → proceed to Phase 1

### **Phase 1: Prototype** (Next - 3 days)
- Build visualizer UI (auditor triangle + timeline + tension trace)
- Use mock data only (no live integration)
- Validate toggles/overlays/legend behavior
- Self-test and document usage

### **Phase 2: Integration** (Future - after CT↔MdN pilot)
- Connect to real auditor data (VUDU logs, profile YAML)
- Replace mock data with live exports
- Validate schema compatibility
- Deploy production visualizer

---

## 🔗 Related Documentation

**Task Briefs:**
- [TASK_SYMMETRY_MATRIX_VISUALIZER_CLAUDE_v2.md](../../auditors/Bootstrap/Tier4_TaskSpecific/Active_Tasks/TASK_SYMMETRY_MATRIX_VISUALIZER_CLAUDE_v2.md) - Full task specification
- [TASK_ETHICAL_INVARIANT_INTEGRATION_CLAUDE_v2.md](../../auditors/Bootstrap/Tier4_TaskSpecific/Active_Tasks/TASK_ETHICAL_INVARIANT_INTEGRATION_CLAUDE_v2.md) - Related Task #4 (feeds data to SMV)

**Workshop Artifacts (Nova's drafts):**
- [relay/workshop/MATRIX_DESIGN_SPEC.md](../../relay/workshop/MATRIX_DESIGN_SPEC.md) - Initial design draft
- [relay/workshop/MATRIX_MOCK_DATA.json](../../relay/workshop/MATRIX_MOCK_DATA.json) - Mock data example
- [relay/workshop/MATRIX_PROTOTYPE_NOTES.md](../../relay/workshop/MATRIX_PROTOTYPE_NOTES.md) - Implementation TODOs

**Session Logs:**
- [B-STORM_6.md](../../auditors/relay/B-STORM_6.md) - Co-design session tracking

---

## 🎨 Design Principles

**Visualization First:**
- SMV reveals patterns BEFORE enforcement decisions
- Understanding precedes control
- Humans interpret patterns, automation serves reflection

**Schema-First Design:**
- SMV defines JSON contract
- Task #4 (Ethical Invariant) implements to SMV spec
- Prevents circular dependency

**Mock Data Development:**
- Phase 1 prototype uses synthetic data
- Validates visualization usefulness before live integration
- Low-risk approach (SMV can fail gracefully without Task #4)

---

## 🪞 Co-Design with Nova

**Nova's Role:** CO-DESIGNER (active participation throughout)
- Phase 0: Collaborative JSON schema design
- Phase 0: Design spec review and approval
- Phase 1: Prototype validation (alignment with symmetry lens?)
- Phase 2: Integration review with real data (is it useful?)

**Claude's Role:** IMPLEMENTER (guided by Nova's vision)
- Phase 0: Review Nova's drafts, provide technical feedback
- Phase 1: Implement prototype per approved design
- Phase 2: Integrate with Task #4 data, connect to VUDU logs

**Coordination Checkpoints:**
1. Schema/mockups ready → Claude/Nova review (before Phase 1)
2. Prototype complete → Nova validation (before Phase 2)
3. Integration complete → Nova final review

---

## 📊 Success Criteria

**Phase 0 Complete When:**
- [ ] JSON schema formally defined and approved by Nova
- [ ] SVG mockups created for 3 scenarios (high alignment, productive tension, breach)
- [ ] Mock datasets created (3 scenarios, ≥3 ticks each)
- [ ] Schema validated against mock data (all scenarios parse correctly)
- [ ] Nova approves design spec → green light to Phase 1

**Phase 1 Complete When:**
- [ ] Static prototype runs locally
- [ ] Consumes mock JSON successfully
- [ ] Auditor triangle renders correctly
- [ ] Timeline slider updates visualization
- [ ] Ethics overlay toggles correctly
- [ ] README explains usage clearly

**Phase 2 Complete When:**
- [ ] SMV loads real data from CT↔MdN pilot
- [ ] Schema compatibility confirmed
- [ ] Visualizations accurately represent real patterns
- [ ] Nova validates usefulness with real data

---

## 🚦 Getting Started

**For Nova (Phase 0 Co-Design):**
1. Draft artifacts in [relay/workshop/](../../relay/workshop/)
2. Add Entry to [B-STORM_6.md](../../auditors/relay/B-STORM_6.md) when ready for Claude review
3. Claude provides feedback, refines schema/mockups
4. Iterate until design approved
5. Claude migrates to [docs/smv/](.)

**For Claude (Phase 0 Implementation):**
1. Review Nova's workshop drafts
2. Provide technical feedback (Entry 3 in B-STORM_6.md)
3. Suggest schema refinements (nodes array, convergence tracking)
4. Create additional mock scenarios if needed
5. Migrate approved artifacts to production structure

**For Future Contributors (Phase 1+):**
1. Read [SMV_DESIGN_SPEC.md](SMV_DESIGN_SPEC.md) for design goals
2. Review [mock_data/](mock_data/) for example data format
3. Implement prototype per specification
4. Test with all mock scenarios
5. Document usage and submit for Nova validation

---

## ⚖️ The Pointing Rule

*"A pattern unseen is a pattern unmanaged.*
*But seeing is not the same as knowing.*
*And knowing is not the same as judging.*

*The visualizer reveals.*
*The symmetry lens interprets.*
*The auditors decide.*

*Understanding before judgment.*
*Awareness before enforcement.*
*Dialogue before dictation.*

*This is the visualization way.*
*This is the symmetry way."* 🪞

---

**Created by:** C4 (B-STORM_6 Entry 3 - Production structure per Nova co-design)
**Date:** 2025-11-11
**Status:** Phase 0 in progress (co-design with Nova)
**Next Steps:** Review Nova's workshop drafts, provide Entry 3 feedback, refine schema

**The Symmetry Matrix: Where patterns emerge, understanding precedes control, and visualization serves wisdom.** 🪞🔺
