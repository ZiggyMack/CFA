<!---
FILE: task_brief_comparison.md
PURPOSE: Side-by-side comparison of bad vs good task brief patterns
VERSION: 1.0.0
STATUS: Example (learning tool)
CREATED: 2025-11-11 (B-STORM_5 Click 2 - Nova feedback)
DEPENDS_ON: ../GOOD_TASK_BRIEF_EXAMPLE.md, ../QUALITY_RUBRICS.md
NEEDED_BY: Contributors creating Tier 4 task briefs
MOVES_WITH: /examples/excellence/bad_vs_good/
LAST_UPDATE: 2025-11-11 [Created per Nova Entry 2 feedback]
--->

# Bad vs Good: Task Brief Comparison

**Purpose:** Learn what makes a task brief excellent by seeing common mistakes side-by-side with best practices.

---

## Comparison 1: Task Definition

### ❌ BAD (Score: 5/20)

```markdown
# TASK: Fix the thing

Do some work on the component.

Success: When it's done.
```

**Why This Fails:**
- "Fix the thing" - WHAT thing?
- "Do some work" - WHAT work?
- "When it's done" - HOW do we know?
- No problem statement, no context

---

### ✅ GOOD (Score: 20/20)

```markdown
# TASK BRIEF: Refactor Authentication Middleware - Remove Code Duplication

**Mission:**
> Consolidate 5 duplicate auth check functions into single reusable middleware, reducing code from 250 lines to ~50 lines.

**Problem This Solves:**
Currently, 5 routes duplicate JWT validation logic (parse token → verify signature → check expiry → extract user). This creates maintenance burden: a security patch must be applied 5 times, risking inconsistency.

**Success Criteria:**
✅ Single `authMiddleware.js` created with reusable function
✅ All 5 routes migrated to use new middleware
✅ Tests pass (15 existing auth tests + 3 new middleware tests)
✅ Code reduction: 250 lines → ~50 lines (80% reduction)
```

**Why This Succeeds:**
- Clear mission (one sentence with measurable outcome)
- Problem explained (why this matters)
- Success criteria concrete (files, tests, metrics)
- Reader knows exactly what "done" looks like

**Rubric: Task Definition 20/20**

---

## Comparison 2: Files Specified

### ❌ BAD (Score: 5/20)

```markdown
## Files

Change some files in /src/.
Maybe update docs.
```

**Why This Fails:**
- "Some files" - WHICH files?
- "Maybe update" - Required or optional?
- No CREATE vs MODIFY distinction
- No dependencies specified

---

### ✅ GOOD (Score: 20/20)

```markdown
## Files to CREATE

1. **`src/middleware/authMiddleware.js`** (~80 lines)
   - Purpose: Reusable JWT validation middleware
   - Dependencies: `jsonwebtoken` library, `config/auth.js`
   - Template: Use existing `src/middleware/corsMiddleware.js` as pattern

## Files to MODIFY

1. **`src/routes/dashboard.js`** (lines 15-35)
   - Remove: Local `checkAuth()` function
   - Add: `const auth = require('../middleware/authMiddleware');`
   - Replace: `app.get('/dashboard', checkAuth, ...)` → `app.get('/dashboard', auth.protect, ...)`

2. **`tests/auth.test.js`**
   - Add: 3 new tests for middleware (valid token, expired token, missing token)

## Files to READ (for context)

1. **`src/routes/*.js`** - Review 5 duplicate auth functions to extract common logic
2. **`docs/architecture/AUTH.md`** - Understand token structure
```

**Why This Succeeds:**
- Exact paths (no guessing)
- CREATE vs MODIFY explicit
- Dependencies listed
- Line numbers where helpful
- Templates referenced

**Rubric: Files Specified 20/20**

---

## Comparison 3: Scope Boundaries

### ❌ BAD (Score: 8/20)

```markdown
## Scope

Do the auth refactor.
```

**Why This Fails:**
- No IN SCOPE list (what IS included?)
- No OUT OF SCOPE list (what to defer?)
- Invites scope creep ("while I'm here, I'll also...")

---

### ✅ GOOD (Score: 20/20)

```markdown
## Scope Boundaries

### ✅ IN SCOPE
- ✅ Consolidate 5 duplicate auth functions
- ✅ Create reusable middleware
- ✅ Migrate 5 routes to new middleware
- ✅ Add 3 middleware tests

### ❌ OUT OF SCOPE (Explicitly Deferred)
- ❌ OAuth integration - Reason: Different task (TASK_OAUTH_v1.md)
- ❌ Role-based permissions - Reason: Needs design spec first
- ❌ Rate limiting - Reason: Not auth concern (separate middleware)

**Why These Boundaries:**
This task focuses on *consolidation only*. New features (OAuth, roles) are deferred to avoid scope creep and maintain clear mission.
```

**Why This Succeeds:**
- IN SCOPE explicit (no ambiguity)
- OUT OF SCOPE with reasons (prevents "while I'm here" additions)
- Rationale provided (explains boundaries)

**Rubric: Scope Boundaries 20/20**

---

## Comparison 4: Bootstrap Efficiency

### ❌ BAD (Score: 5/20)

```markdown
## Steps

1. Figure out what to do
2. Do it
3. Test it
4. Done
```

**Why This Fails:**
- "Figure out" - not actionable
- "Do it" - no specifics
- No decision points
- No time estimates

---

### ✅ GOOD (Score: 20/20)

```markdown
## Execution Plan

### Phase 1: Analysis (Est: 30 min)

**Step 1.1: Extract common logic**
- [ ] Read 5 duplicate functions in `src/routes/*.js`
- [ ] List common steps: parse header → verify token → check expiry → extract user
- **Output:** Shared logic documented (create `ANALYSIS_NOTES.md` temp file)

**Step 1.2: Review middleware pattern**
- [ ] Read `src/middleware/corsMiddleware.js` for Express middleware structure
- [ ] Note: Must call `next()` on success, `res.status(401)` on failure
- **Output:** Pattern understood

---

### Phase 2: Implementation (Est: 1.5 hours)

**Step 2.1: Create middleware**
- [ ] Create `src/middleware/authMiddleware.js`
- [ ] Implement: `protect(req, res, next)` function
- [ ] Add error handling for: missing token, invalid signature, expired token
- **Expected output:** Middleware functional (manual test with curl)

**DECISION POINT:** If JWT library API changed since last use, consult docs before proceeding.

**Step 2.2: Migrate routes**
- [ ] Modify `src/routes/dashboard.js` (replace local function)
- [ ] Repeat for 4 remaining routes
- [ ] Remove duplicate code
- **Expected output:** All routes use new middleware

---

### Phase 3: Testing (Est: 45 min)

**Step 3.1: Run existing tests**
```bash
npm test -- auth.test.js
```
- **Expected:** 15/15 tests pass

**Step 3.2: Add middleware tests**
- [ ] Add 3 tests: valid token (200), expired token (401), missing token (401)
- **Expected:** 18/18 tests pass
```

**Why This Succeeds:**
- Actionable steps (not vague "figure out")
- Logical order (analysis → implement → test)
- Decision points flagged
- Time estimates per phase
- Expected outputs documented

**Rubric: Bootstrap Efficiency 20/20**

---

## Comparison 5: Deliverable Clarity

### ❌ BAD (Score: 5/20)

```markdown
## Deliverables

Better auth code.
```

**Why This Fails:**
- "Better" - not measurable
- No acceptance tests
- No rollback plan

---

### ✅ GOOD (Score: 20/20)

```markdown
## Success Criteria

**✅ Task Complete When:**

1. **Middleware Created:** `src/middleware/authMiddleware.js` exists
   - Acceptance test: `curl -H "Authorization: Bearer <valid_token>" http://localhost:3000/dashboard` → 200

2. **Routes Migrated:** All 5 routes use new middleware
   - Acceptance test: `grep -r "checkAuth" src/routes/*.js` → 0 results (old function removed)

3. **Tests Pass:** 18/18 auth tests pass
   - Acceptance test: `npm test -- auth.test.js` → "18 passed"

4. **Code Reduced:** 250 lines → ~50 lines (80% reduction)
   - Acceptance test: `cloc src/routes/*.js` → compare before/after

**❌ NOT Complete Until:**
- [ ] REPO_LOG entry created
- [ ] Semantic headers updated (version bumps, LAST_UPDATE dates)

---

## Rollback Plan

**If Task Blocked:**
- Scenario 1: JWT library API breaking change → Consult docs, adjust middleware
- Scenario 2: Tests fail after migration → Revert routes, debug middleware in isolation

**If Need to Undo:**
```bash
git revert <commit_hash>
git checkout HEAD~1 -- src/middleware/authMiddleware.js
```
```

**Why This Succeeds:**
- Concrete deliverables (files, tests, metrics)
- Observable outcomes (curl commands, grep checks)
- Acceptance tests runnable
- Rollback plan included

**Rubric: Deliverable Clarity 20/20**

---

## Summary: Task Brief Rubric Application

| Criterion | Bad Example | Good Example | Difference |
|-----------|-------------|--------------|------------|
| **Task Definition** | 5/20 | 20/20 | +15 (vague vs mission/problem/success) |
| **Files Specified** | 5/20 | 20/20 | +15 (vague vs exact paths + dependencies) |
| **Scope Boundaries** | 8/20 | 20/20 | +12 (implicit vs explicit IN/OUT) |
| **Bootstrap Efficiency** | 5/20 | 20/20 | +15 (vague vs actionable steps) |
| **Deliverable Clarity** | 5/20 | 20/20 | +15 (vague vs concrete acceptance tests) |
| **TOTAL** | **28/100** | **100/100** | **+72 points** |

**Key Insight:** Task briefs aren't documentation - they're *executable instructions*. Vagueness ("figure out", "maybe", "some files") forces reader to make assumptions. Specificity ("Step 1.1", "src/routes/dashboard.js:15-35", "curl command") enables autonomous execution.

---

**See Also:**
- [GOOD_TASK_BRIEF_EXAMPLE.md](../GOOD_TASK_BRIEF_EXAMPLE.md) - Full annotated exemplar
- [QUALITY_RUBRICS.md](../QUALITY_RUBRICS.md) - Complete rubric with all criteria

---

**Created by:** C4 (B-STORM_5 Click 2)
**Date:** 2025-11-11
**Purpose:** Teach task brief excellence through contrast
