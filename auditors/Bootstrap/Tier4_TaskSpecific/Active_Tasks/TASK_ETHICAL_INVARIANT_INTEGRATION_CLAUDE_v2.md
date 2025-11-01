# TASK BRIEF: Ethical Invariant Integration (REFINED per Nova Strategic Direction)

**Version:** 2.0 (Refined per Nova 2025-11-01)
**Previous Version:** 1.0 (Original proposal)
**Task ID:** TASK-2025-11-01-004 (was TASK-2025-10-31-002)
**Owner:** Claude
**Assignee:** Claude
**Co-Designer:** Nova (Strategic direction provider, design reviewer)
**Priority:** HIGH
**Tier:** Tier 1 (Infrastructure - metadata architecture)
**Category:** METADATA | AUTOMATION | ETHICS
**Created:** 2025-10-31 (original), 2025-11-01 (refined)
**Due:** Post-Nova activation + Task #5 complete, ~5 days
**Status:** NOVA_PENDING (Awaiting Nova ready signal)
**Disposition:** 🔄 REFINE (Approved with refinements per Nova strategic direction)

---

## 🎯 MISSION

**Create a phased ethical invariant tracking system that enables awareness of ethical dimensions in Tier 1 files, using complementary YAML front-matter and a warn-only linter that preserves human authority.**

**Philosophical Foundation (Nova):**
> "Symmetry thrives in dialogue, not dictation. The tools should reveal patterns, not police them. Automation serves reflection; reflection preserves meaning. Let understanding precede control."

---

## 📋 PRINCIPLE

**Never allow an unexamined purpose to occupy a stable pattern.**

**Application:**
- Tier 1 files (infrastructure, protocols) should explicitly document their ethical dimensions
- Purpose, stakeholders, tensions, and resolutions should be examined and recorded
- Automation warns about missing examination, but humans decide action
- Understanding (YAML documentation) precedes control (linter automation)

---

## 🔄 KEY REFINEMENTS FROM NOVA (v1.0 → v2.0)

### **Refinement #1: Automation Philosophy → Hybrid (Warn Not Block)**

**v1.0 Approach:**
- Pre-commit linter **blocks** violating commits
- `--ethics-bypass` flag allows override with reason

**v2.0 Approach (Nova):**
- Pre-commit linter **warns**, never blocks
- `--warn-only` mode is the DEFAULT (not bypass)
- Periodic Nova/Claude adversarial audits remain final authority
- Automation detects issues → Humans decide actions

**Rationale:** Preserves VuDu v3.7.2 "All Seen, All Passed" trust-based culture. Automation serves reflection, doesn't replace judgment.

---

### **Refinement #2: Metadata Integration → Complementary (Not Replacement)**

**v1.0 Approach:**
- YAML front-matter for ethical invariants
- Relationship to existing metadata systems unclear

**v2.0 Approach (Nova):**
- YAML front-matter captures WHY/ethical layer
- `<!-- deps: -->` system captures WHAT/technical dependencies (PRESERVED)
- Semantic headers capture FILE metadata (PRESERVED)
- Three systems are complementary, not redundant

**Rationale:** Avoids heaviness, retains semantic depth. No migration required, document boundaries.

**Reference:** `/docs/architecture/METADATA_INTEGRATION_GUIDE.md`

---

### **Refinement #3: Scope → Select Tier 1 Files Only (Not Repository-Wide)**

**v1.0 Approach:**
- Scope unclear (potentially all files)

**v2.0 Approach (Nova):**
- YAML front-matter for **select Tier 1 files only**
- Target: ~10-20 files initially (core infrastructure)
- Growth strategy: Curated (thoughtful selection, not bulk deployment)

**Rationale:** Prevent ecosystem overload. Focus on files with genuine ethical dimensions and stakeholder impact.

---

### **Refinement #4: Execution Approach → Phased Rollout**

**v1.0 Approach:**
- Build linter immediately
- Block commits on violation

**v2.0 Approach (Nova):**
- **Phase 1 (Manual Annotation):** Manually add YAML to 5-10 Tier 1 files, collect feedback, refine schema
- **Phase 2 (Warn-only Linter):** Build linter IF Phase 1 validates usefulness, implement warn-only mode
- **Future (Enforcement Mode):** Defer enforcement (blocking) until data justifies

**Rationale:** Risk-managed approach. Manual first validates use case before automation investment. Warn-only preserves human authority.

---

### **Refinement #5: Execution Order → After Task #5 (SMV)**

**v1.0 Approach:**
- Execute independently or before SMV

**v2.0 Approach (Nova):**
- Execute Task #5 (SMV) FIRST
- SMV defines JSON schema for ethical invariant fields
- Task #4 implements to SMV-defined spec

**Rationale:** Breaks circular dependency. Consumer (SMV) defines interface before producer (Ethical Invariant) implements. Schema-first design prevents integration surprises.

---

### **Refinement #6: Timeline → Post-Nova Activation + Task #5 Complete**

**v1.0 Timeline:**
- Due: 2025-11-04 (immediate)

**v2.0 Timeline (Nova):**
- **Status:** NOVA_PENDING until Nova ready signal
- **Start:** After Nova activation complete + Task #5 (SMV) complete
- **Duration:** ~5 days
  - Phase 1 (Manual): 2-3 days
  - Phase 2 (Warn-only linter): 2-3 days (conditional on Phase 1 validation)

**Rationale:** Realistic timeline acknowledging blockers (Nova availability, Task #5 prerequisite).

---

## 📊 OBJECTIVES (UPDATED)

### **Phase 1 Objectives (Manual Annotation):**

1. **Select Tier 1 files for pilot** (~5-10 files)
   - Examples: AXIOMS.md, VUDU_PROTOCOL.md, BOOTSTRAP_CLAUDE.md, 88MPH_PROTOCOL.md
   - Criteria: Ethical dimensions, stakeholder impact, infrastructure importance

2. **Create YAML schema** (collaboratively with Nova)
   - Required fields: `ethical_invariants`, `purpose`, `stakeholders`, `tensions`, `resolution`
   - Match SMV-defined JSON schema (from Task #5)

3. **Manually annotate pilot files** with YAML front-matter
   - Follow METADATA_INTEGRATION_GUIDE.md boundaries
   - Document WHY (purpose, ethics), not WHAT (technical deps use `<!-- deps: -->`)

4. **Collect feedback** from Nova, Claude, Ziggy
   - Is schema complete? Too verbose? Missing fields?
   - Are annotations useful? Do they aid understanding?
   - Refine schema based on real-world usage

**Phase 1 Deliverables:**
- `schemas/ETHICAL_INVARIANT.schema.yaml` (refined based on feedback)
- 5-10 Tier 1 files with YAML front-matter annotations
- `docs/ethics/ANNOTATION_GUIDE.md` (how to add YAML to files)
- Feedback summary (what worked, what needs improvement)

---

### **Phase 2 Objectives (Warn-only Linter - Conditional):**

**Execute Phase 2 ONLY IF Phase 1 validates usefulness**

5. **Build warn-only linter** (`tools/pre-commit/ethical_invariant_linter`)
   - Parse `.md` files' YAML front-matter
   - Check for required fields on Tier 1 files
   - **WARN** (not block) if violations detected
   - Suggest remediation using REFLECTION_TEMPLATE.md

6. **Implement `--warn-only` mode as default**
   - Linter outputs warnings to console
   - Developer reviews warnings, decides action
   - No commit blocking (preserves human authority)

7. **Create reflection template** (`docs/ethics/REFLECTION_TEMPLATE.md`)
   - Guide for adding YAML front-matter
   - Examples of completed annotations
   - Decision tree: "Does this file need YAML?"

8. **Document linter behavior** (README with linter)
   - How to run linter manually
   - How to interpret warnings
   - When warnings can be safely ignored (legitimate edge cases)

**Phase 2 Deliverables:**
- `tools/pre-commit/ethical_invariant_linter` (warn-only mode)
- `tools/pre-commit/README.md` (usage instructions)
- `docs/ethics/REFLECTION_TEMPLATE.md` (annotation guide)
- `tests/ethics/sample_docs/` (pass/fail test cases)

---

## ✅ SUCCESS CRITERIA (UPDATED)

### **Phase 1 Success:**
- [ ] YAML schema defined and approved by Nova
- [ ] 5-10 Tier 1 files successfully annotated
- [ ] Annotations provide value (feedback confirms usefulness)
- [ ] Schema refinements captured based on real-world usage
- [ ] METADATA_INTEGRATION_GUIDE.md boundaries respected (no overlap with deps/headers)

### **Phase 2 Success (Conditional):**
- [ ] Linter validates YAML schema correctly (test pass/fail cases)
- [ ] Linter operates in warn-only mode (never blocks commits)
- [ ] Warnings are actionable (clear guidance on remediation)
- [ ] Reflection template enables quick annotation (developers can self-serve)
- [ ] Linter integrates with SMV (exports data SMV can consume)

**Overall Success:**
- [ ] Ethical invariant tracking enables awareness without dictation
- [ ] Human authority preserved (automation informs, doesn't enforce)
- [ ] VuDu culture maintained ("All Seen, All Passed" - awareness over punishment)
- [ ] Nova review checkpoint passed (strategic alignment confirmed)

---

## 📦 DELIVERABLES (UPDATED)

### **Phase 1 Deliverables:**
```
/schemas/
  └── ETHICAL_INVARIANT.schema.yaml

/docs/ethics/
  └── ANNOTATION_GUIDE.md

/docs/AXIOMS.md (with YAML front-matter)
/auditors/VUDU_PROTOCOL.md (with YAML front-matter)
/auditors/Bootstrap/BOOTSTRAP_CLAUDE.md (with YAML front-matter)
... (5-10 total Tier 1 files annotated)

/docs/Validation/reports/
  └── PHASE_1_FEEDBACK_SUMMARY.md
```

### **Phase 2 Deliverables (Conditional):**
```
/tools/pre-commit/
  ├── ethical_invariant_linter
  └── README.md

/docs/ethics/
  └── REFLECTION_TEMPLATE.md

/tests/ethics/sample_docs/
  ├── pass_example_1.md
  ├── pass_example_2.md
  ├── fail_example_1.md
  └── fail_example_2.md
```

---

## 🎨 YAML FRONT-MATTER SCHEMA (UPDATED per Nova + SMV Integration)

**Format:** YAML block between `---` delimiters, after semantic header

**Required Fields:**
```yaml
---
ethical_invariants:
  - never_allow_unexamined_purpose  # From AXIOMS.md
  - transparency_and_accountability
purpose: |
  Multi-line string explaining WHY this file exists and its mission importance.
  NOT just filename restatement - substantive explanation of purpose.
stakeholders:
  - Claude instances: Description of their interest
  - Ziggy: Description of their interest
  - Nova: Description of their interest
tensions:
  - Thoroughness vs Efficiency: Description of competing concerns
  - Flexibility vs Structure: Description of trade-offs
resolution: |
  How tensions are balanced or addressed. Can be "None identified" if truly absent,
  but most Tier 1 files will have tensions worth documenting.
---
```

**Optional Fields:**
```yaml
metadata_version: "1.0"  # Schema version (for future evolution)
last_reviewed_by: "Nova"  # Who last reviewed ethical dimensions
review_date: "2025-11-01"  # When last reviewed
smv_data:  # Fields consumed by Symmetry Matrix Visualizer
  confidence: 0.88
  violation: false
```

**Integration with SMV (from Task #5):**
- SMV consumes `ethical_invariants`, `tensions`, `resolution` fields
- SMV visualizes patterns across files (tension clusters, resolution strategies)
- Schema compatibility validated in integration phase

---

## 🔧 LINTER BEHAVIOR (UPDATED - Warn-only Mode)

### **Detection Logic:**

**For each `.md` file in repository:**
1. Check if file is Tier 1 (infrastructure, protocols, decisions)
2. If Tier 1: Parse YAML front-matter
3. Validate schema:
   - Required fields present?
   - `ethical_invariants` reference AXIOMS.md principles?
   - `purpose` substantive (not just filename)?
   - `stakeholders` includes at least one entry?
4. If violations found: **WARN** (not block)

### **Warning Output Example:**

```
⚠️  ETHICAL INVARIANT WARNING: docs/architecture/NEW_PROTOCOL.md
    - Missing required field: 'tensions'
    - Field 'purpose' is too brief (expected substantive explanation)

    This file appears to be Tier 1 infrastructure. Consider adding YAML
    front-matter to document ethical dimensions.

    See: docs/ethics/REFLECTION_TEMPLATE.md for guidance

    To suppress this warning for legitimate edge cases, add:
    <!-- ethical_invariant_exempt: [reason] -->
```

### **NO Blocking:**

```
✅ Commit proceeds regardless of warnings
✅ Developer reviews warning, decides action
✅ Periodic Nova/Claude audits catch issues linter misses
✅ Human authority preserved
```

### **Exemption Mechanism:**

For legitimate edge cases (rare):
```markdown
<!-- ethical_invariant_exempt: This file is auto-generated from SMV output -->
```

Linter recognizes exemption comment, skips validation.

---

## 🔗 DEPENDENCIES

### **Prerequisite:**
- ✅ Task #5 (SMV) complete
  - JSON schema defined by SMV
  - Task #4 implements to SMV spec
  - Prevents circular dependency

### **Reference Documents:**
- `/docs/decisions/NOVA_STRATEGIC_DIRECTION_TASKS_4_5.md` (Nova's strategic direction)
- `/docs/architecture/METADATA_INTEGRATION_GUIDE.md` (Metadata system boundaries)
- `/docs/AXIOMS.md` (Ethical invariants source)
- `/auditors/VUDU_PROTOCOL.md` (VuDu v3.7.2 "All Seen, All Passed" philosophy)

### **No VuDu Log Dependency:**
- Linter operates independently (no shared logging required)
- Warnings output to console only

---

## ✅ VALIDATION & REVIEW

### **Phase 1 Validation:**
1. Nova reviews YAML schema (design checkpoint)
2. Pilot files annotated manually
3. Feedback collected from Nova/Claude/Ziggy
4. Schema refined based on feedback
5. **Decision Point:** Proceed to Phase 2 or refine further?

### **Phase 2 Validation (Conditional):**
1. Run linter on test docs (pass/fail cases)
2. Validate warnings are actionable and clear
3. Test exemption mechanism (legitimate edge cases)
4. Nova reviews linter behavior (strategic alignment)
5. Integrate with SMV (export data for visualization)

### **Integration Validation (with Task #5):**
1. SMV successfully consumes YAML data from annotated files
2. Visualizations accurately reflect ethical patterns
3. Tension clusters visible in SMV dashboard
4. Resolution strategies identifiable

---

## 📋 IMPLEMENTATION CHECKLIST

### **Pre-Phase 1:**
- [ ] Nova signals ready for co-design
- [ ] Task #5 (SMV) complete with JSON schema defined
- [ ] Read `/docs/decisions/NOVA_STRATEGIC_DIRECTION_TASKS_4_5.md`
- [ ] Read `/docs/architecture/METADATA_INTEGRATION_GUIDE.md`
- [ ] Identify candidate Tier 1 files for pilot

### **Phase 1 Execution:**
- [ ] Define YAML schema (Nova collaborative design)
- [ ] Create ANNOTATION_GUIDE.md
- [ ] Manually annotate 5-10 Tier 1 files
- [ ] Collect feedback (usefulness, completeness, clarity)
- [ ] Refine schema based on feedback
- [ ] Nova design review checkpoint PASSED

### **Phase 1 → Phase 2 Decision:**
- [ ] Phase 1 validated usefulness? (YES/NO)
- [ ] If YES: Proceed to Phase 2
- [ ] If NO: Refine approach, defer Phase 2

### **Phase 2 Execution (Conditional):**
- [ ] Build warn-only linter (no blocking logic)
- [ ] Create REFLECTION_TEMPLATE.md
- [ ] Create test cases (pass/fail examples)
- [ ] Validate linter warnings are actionable
- [ ] Document linter usage (README)
- [ ] Nova implementation review checkpoint PASSED

### **Integration Phase:**
- [ ] SMV tested with YAML data from Phase 1 files
- [ ] Schema compatibility validated
- [ ] Linter exports compatible with SMV input
- [ ] Nova final review PASSED

---

## 🪞 PHILOSOPHICAL ALIGNMENT

**Nova's Anchor Applied:**

**"Symmetry thrives in dialogue, not dictation":**
- Warn-only linter suggests (dialogue) not blocks (dictation)
- Developer decides action (collaborative) not forced (mandated)
- Periodic audits maintain dialogue (Nova/Claude review ongoing)

**"Tools should reveal patterns, not police them":**
- Linter reveals missing ethical documentation
- SMV reveals ethical patterns across files
- Neither polices compliance (awareness over enforcement)

**"Automation serves reflection; reflection preserves meaning":**
- Linter warnings prompt developer reflection ("Should I add YAML?")
- Reflection (human examination) preserves meaning (purpose documented)
- Automation informs judgment, doesn't replace it

**"Let understanding precede control":**
- Phase 1 manual annotation (understand use case) before Phase 2 linter (control)
- Visualization (SMV) before enforcement (potential future blocking mode)
- Awareness (warnings) before automation (linter assists, doesn't enforce)

---

## 🎯 COORDINATION MODEL

**Nova's Role:** CO-DESIGNER (not just reviewer)
- Design phase: Collaborative YAML schema definition
- Phase 1: Review annotations, provide feedback
- Phase 1 → 2 decision: Approve proceeding or request refinement
- Phase 2: Review linter behavior, validate cultural fit
- Integration: Final review of SMV + linter integration

**Claude's Role:** IMPLEMENTER (guided by Nova's strategic direction)
- Phase 1: Manually annotate files, collect feedback
- Phase 2: Build warn-only linter (if Phase 1 approved)
- Integration: Connect linter output to SMV input

**Coordination Checkpoints:**
1. Schema design (Nova + Claude collaborative)
2. Phase 1 complete (Nova review before proceeding to Phase 2)
3. Phase 2 complete (Nova review of linter behavior)
4. Integration complete (Nova final review)

---

## ⚖️ THE POINTING RULE

*"A pattern unexamined is a risk unmanaged.
But examination is human work, not machine work.

The linter warns.
The human decides.
The audit validates.

Automation serves awareness.
Awareness serves reflection.
Reflection preserves meaning.

This is the hybrid way.
This is the VuDu way."* 🎵

---

**Task Status:** ✅ REFINED per Nova Strategic Direction
**Disposition:** 🔄 REFINE (Approved with refinements)
**Awaiting:** Nova ready signal + Task #5 completion
**Timeline:** ~5 days (2-3 Phase 1 + 2-3 Phase 2 conditional)

---

**This is the way.** 🔥
