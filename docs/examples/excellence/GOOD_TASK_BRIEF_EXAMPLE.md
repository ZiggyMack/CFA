<!---
FILE: GOOD_TASK_BRIEF_EXAMPLE.md
PURPOSE: Exemplar task brief demonstrating excellent Tier 4 structure with inline annotations
VERSION: 1.0.0
STATUS: Example (annotated template)
CREATED: 2025-11-11 (B-STORM_5 Click 2 - Nova feedback)
DEPENDS_ON: QUALITY_RUBRICS.md (Task Brief Rubric)
NEEDED_BY: Contributors creating new Tier 4 task briefs
MOVES_WITH: /examples/excellence/
LAST_UPDATE: 2025-11-11 [Created per Nova Entry 2 feedback]
--->

# TASK BRIEF: [Component/Feature Name] - Clear Action Verb

<!--
ANNOTATION: Task Definition Clarity (20/20)
- Title uses action verb (implement, refactor, validate, integrate)
- First section answers: What is the task? Why now? What's the context?
- Clear scope boundaries (what IS and IS NOT included)
-->

**Version:** 1.0.0
**Status:** Ready for Execution
**Owner:** [Role Name] (e.g., C4, Doc Claude, Process Claude)
**Priority:** HIGH | MEDIUM | LOW
**Estimated Time:** [X hours]

**Created:** 2025-11-11
**Context:** [What recent work/decision led to this task being created?]

---

## Mission Statement

<!--
ANNOTATION: Task Definition (20/20)
- One-sentence mission: What success looks like
- Problem statement: What pain/gap this solves
- Success criteria: How do we know it's done?
-->

**Mission (one sentence):**
> [Clear, concise statement of what this task accomplishes and why it matters]

**Problem This Solves:**
[2-3 sentences explaining the pain point, gap, or opportunity this addresses]

**Why This Task Exists:**
[Brief context: What strategic goal does this serve? What blocks without it?]

---

## Success Criteria

<!--
ANNOTATION: Deliverable Clarity (20/20)
- Concrete deliverables (files, functions, tests)
- Observable outcomes (not just "improve X" but "X metric reaches Y")
- Clear acceptance tests
-->

**✅ Task Complete When:**

1. **Deliverable 1:** [Specific file/component created with exact location]
   - Acceptance test: [How to verify it works]

2. **Deliverable 2:** [Specific functionality implemented]
   - Acceptance test: [Command to run / expected output]

3. **Deliverable 3:** [Documentation updated]
   - Acceptance test: [Check semantic headers, cross-references, version bump]

**❌ NOT Complete Until:**
- [ ] All files have semantic headers
- [ ] Cross-references updated in related docs
- [ ] Tests pass (if applicable)
- [ ] REPO_LOG entry created
- [ ] Version numbers bumped where appropriate

---

## Files to Create/Modify

<!--
ANNOTATION: Files Specified (20/20)
- Exact paths listed (not "somewhere in /docs/")
- CREATE vs MODIFY vs READ clearly indicated
- Dependencies explicit (read X before modifying Y)
-->

### Files to CREATE

1. **`path/to/new_file.md`** (~X lines estimated)
   - Purpose: [What this file does]
   - Dependencies: [What needs to exist first]
   - Template: [Link to template if applicable, or "from scratch"]

2. **`path/to/another_file.py`** (~Y lines estimated)
   - Purpose: [What this file does]
   - Dependencies: [External libraries, config files needed]
   - Testing: [How to test this file]

### Files to MODIFY

1. **`path/to/existing_file.md`**
   - What to change: [Section to update, lines to add]
   - Why: [Rationale for change]
   - Before/after: [Brief example if complex]

2. **`path/to/config.yaml`**
   - What to change: [New fields to add]
   - Format: [YAML structure example]

### Files to READ (for context)

1. **`path/to/reference_doc.md`** - Read sections X, Y to understand [concept]
2. **`path/to/related_component.py`** - Review [function] implementation pattern

---

## Scope Boundaries

<!--
ANNOTATION: Scope Boundaries (20/20)
- Explicit IN SCOPE list (what IS included)
- Explicit OUT OF SCOPE list (what to defer/skip)
- Clarifies edge cases
-->

### ✅ IN SCOPE (What This Task Includes)

- ✅ [Feature A implementation]
- ✅ [Documentation for Feature A]
- ✅ [Unit tests for Feature A]
- ✅ [Integration with existing Component X]

### ❌ OUT OF SCOPE (Explicitly Deferred)

- ❌ [Feature B] - Reason: [Needs separate design spec first]
- ❌ [Performance optimization] - Reason: [Premature, do in v2.0]
- ❌ [UI redesign] - Reason: [Waiting for user feedback on v1.0]

**Why These Boundaries:**
[Brief explanation of why scope is limited this way - avoids scope creep, maintains focus, etc.]

---

## Step-by-Step Execution Plan

<!--
ANNOTATION: Bootstrap Efficiency (20/20)
- Actionable steps (not vague "figure out X")
- Logical order (dependencies respected)
- Decision points flagged
- Time estimates per step
-->

### Phase 1: Context Gathering (Est: 30 min)

**Step 1.1: Read prerequisite docs**
- [ ] Read `path/to/doc1.md` sections 2-4
- [ ] Read `path/to/doc2.md` to understand [concept]
- **Why:** [What knowledge this provides]

**Step 1.2: Scan related implementations**
- [ ] Review `path/to/similar_component.py` for pattern
- [ ] Note any reusable functions/structures
- **Why:** [Avoid reinventing, maintain consistency]

---

### Phase 2: Core Implementation (Est: 2 hours)

**Step 2.1: Create skeleton structure**
- [ ] Create `path/to/new_file.md` with semantic header
- [ ] Add placeholder sections (Purpose, Usage, Examples)
- **Expected output:** File exists, structure clear

**Step 2.2: Implement core functionality**
- [ ] Write [specific function/section]
- [ ] Add inline comments explaining non-obvious logic
- [ ] Ensure semantic headers complete
- **Expected output:** Core logic functional

**Step 2.3: Add examples/documentation**
- [ ] Document usage pattern with concrete example
- [ ] Add troubleshooting section for common issues
- **Expected output:** Self-explanatory for new users

---

### Phase 3: Integration (Est: 1 hour)

**Step 3.1: Update cross-references**
- [ ] Modify `path/to/related_doc.md` to link new component
- [ ] Update `path/to/index.md` to include in navigation
- **Expected output:** Discoverable from existing docs

**Step 3.2: Test integration**
- [ ] Run `command_to_test` and verify output
- [ ] Check that [related system] still works
- **Expected output:** No regressions

---

### Phase 4: Documentation & Cleanup (Est: 30 min)

**Step 4.1: REPO_LOG entry**
- [ ] Create entry in `docs/repository/logs/REPO_LOG.md`
- [ ] Categorize: [enhancement/fix/refactor]
- [ ] Document: what changed, why, impact
- **Expected output:** Future maintainers understand change

**Step 4.2: Version bumps**
- [ ] Bump version in modified files (e.g., v1.0 → v1.1)
- [ ] Update LAST_UPDATE date in semantic headers
- **Expected output:** Versions reflect current state

**Step 4.3: Final checks**
- [ ] Run validation: semantic headers complete?
- [ ] Run validation: links work?
- [ ] Run validation: files in correct locations?
- **Expected output:** Passes quality checks

---

## Decision Points & Branching

<!--
ANNOTATION: Handles Uncertainty
- Flags decisions that need user input
- Provides default choices with rationale
- Documents what to do if X happens
-->

### Decision Point 1: [Architecture Choice]

**Question:** Should we use [Approach A] or [Approach B]?

**Option A:**
- Pros: [Benefits]
- Cons: [Drawbacks]
- Recommendation: Use if [condition]

**Option B:**
- Pros: [Benefits]
- Cons: [Drawbacks]
- Recommendation: Use if [condition]

**Default:** [Approach A] unless [specific reason to choose B]

---

### Decision Point 2: [Scope Adjustment]

**Trigger:** If [unexpected complexity discovered in Step 2.2]

**Options:**
1. **Proceed:** Complete as planned (Est: +2 hours)
2. **Simplify:** Reduce scope to [minimal version] (Est: +30 min)
3. **Defer:** Create follow-up task brief (Est: +15 min)

**Recommendation:** Simplify if complexity adds >50% time, defer if fundamental design needed

---

## Dependencies

<!--
ANNOTATION: Explicit Prerequisites
- What must exist before starting
- What can block progress
- What related tasks should be coordinated
-->

### Must Exist Before Starting

- ✅ [Component X] must be implemented (`path/to/component_x/`)
- ✅ [Config file] must be populated (`path/to/config.yaml`)
- ✅ [Design doc] must be reviewed and approved (`path/to/design.md`)

### May Block Progress

- ⚠️ [External API] availability - If down, work offline and test later
- ⚠️ [User decision] on [feature Y] - Proceed with default, refactor if decision changes

### Coordinate With

- 🔗 [Related Task Brief A] - Share [component] design
- 🔗 [Related Task Brief B] - Ensure [interface] compatibility

---

## Testing & Validation

<!--
ANNOTATION: Quality Assurance
- How to test the work
- What "passing" looks like
- Edge cases to check
-->

### Unit Tests (if applicable)

```bash
# Run tests
pytest path/to/tests/test_new_component.py

# Expected output
====== 5 passed in 0.3s ======
```

### Integration Tests

**Test 1: Verify Component X integration**
```bash
# Command
run_integration_test --component new_component

# Expected output
✅ All integrations working
```

**Test 2: Verify documentation links**
```bash
# Command
check_links path/to/new_file.md

# Expected output
✅ 12/12 links valid
```

### Manual Validation Checklist

- [ ] Open `path/to/new_file.md` and verify semantic header complete
- [ ] Check that cross-references in related docs point to new component
- [ ] Verify examples in documentation actually run
- [ ] Confirm REPO_LOG entry present and categorized correctly

---

## Rollback Plan

<!--
ANNOTATION: Risk Management
- What to do if task fails/blocked
- How to undo changes cleanly
- When to escalate vs. persist
-->

### If Task Blocked

**Scenario 1: Dependency unavailable**
- Action: Create placeholder, document blocker in task brief
- Resume when: [Dependency] becomes available

**Scenario 2: Unforeseen complexity**
- Action: Simplify to minimal viable version
- Create follow-up task for full implementation

### If Need to Undo Changes

1. Revert commit: `git revert <commit_hash>`
2. Remove created files: `rm path/to/new_file.md`
3. Restore modified files from backup: `git checkout HEAD~1 -- path/to/file`

### When to Escalate

- ⚠️ If time exceeds estimate by >100% → Pause and consult user
- ⚠️ If architectural decision needed → Create decision brief, get approval
- ⚠️ If breaks existing functionality → Rollback immediately, investigate

---

## Related Resources

<!--
ANNOTATION: Context & Learning
- Links to background docs
- Related examples/patterns
- Upstream/downstream dependencies
-->

### Background Reading

- [Architecture Doc](path/to/architecture.md) - Section 3 explains [concept]
- [Related Component Example](path/to/example.md) - Similar implementation pattern

### Design Decisions

- [ADR-001: Decision Title](path/to/adr/001.md) - Why we chose [approach]
- [RFC-042: Proposal](path/to/rfc/042.md) - Original feature proposal

### Dependencies

- **Upstream:** [Component A](path/to/component_a/) must exist
- **Downstream:** [Feature B](path/to/feature_b/) will use this component
- **Parallel:** [Task C](path/to/task_c.md) works on related area

---

## Post-Task Actions

<!--
ANNOTATION: Closure & Handoff
- What to do when task complete
- How to communicate completion
- What to update
-->

### Completion Checklist

- [ ] All deliverables created and verified
- [ ] All files have semantic headers
- [ ] Cross-references updated
- [ ] REPO_LOG entry created
- [ ] Version numbers bumped
- [ ] Tests pass (if applicable)
- [ ] Task brief status changed to "Complete"

### Communication

**Notify:**
- User (if task was user-requested)
- Related task owners (if coordination needed)
- Doc Claude (if documentation-heavy)

**Update:**
- `REPO_LOG.md` with completion entry
- Related roadmap/planning docs
- Task tracking system (if applicable)

---

## Rubric Self-Score

<!--
ANNOTATION: Quality Self-Assessment
Using QUALITY_RUBRICS.md Task Brief Rubric:

1. Task Definition (20/20)
   - Clear mission statement ✅
   - Problem and success criteria ✅
   - Context provided ✅

2. Files Specified (20/20)
   - Exact paths with CREATE/MODIFY/READ ✅
   - Dependencies explicit ✅
   - Estimates provided ✅

3. Scope Boundaries (20/20)
   - IN SCOPE clear ✅
   - OUT OF SCOPE explicit ✅
   - Rationale documented ✅

4. Bootstrap Efficiency (20/20)
   - Actionable steps (not vague) ✅
   - Logical order ✅
   - Decision points flagged ✅
   - Time estimates per phase ✅

5. Deliverable Clarity (20/20)
   - Concrete deliverables ✅
   - Observable outcomes ✅
   - Acceptance tests ✅
   - Rollback plan ✅

**Total Score: 100/100 (Excellent)**

This task brief is designed as a Costume Room exemplar.
Use as template for new Tier 4 task briefs.
-->

---

**Created by:** C4 (B-STORM_5 Click 2 - Nova feedback)
**Date:** 2025-11-11
**Purpose:** Demonstrate excellent task brief structure with annotations
**Status:** Exemplar for Costume Room
**Score:** 100/100 on Task Brief Rubric

**Copy this structure. Adapt to your task. Maintain this quality.** 🎯
