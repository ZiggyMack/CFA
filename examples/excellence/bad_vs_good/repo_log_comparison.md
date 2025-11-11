<!---
FILE: repo_log_comparison.md
PURPOSE: Side-by-side comparison of bad vs good REPO_LOG entry patterns
VERSION: 1.0.0
STATUS: Example (learning tool)
CREATED: 2025-11-11 (B-STORM_5 Click 2 - Nova feedback)
DEPENDS_ON: ../GOOD_REPO_LOG_ENTRY_EXAMPLE.md, ../QUALITY_RUBRICS.md
NEEDED_BY: Contributors adding entries to REPO_LOG.md
MOVES_WITH: /examples/excellence/bad_vs_good/
LAST_UPDATE: 2025-11-11 [Created per Nova Entry 2 feedback]
--->

# Bad vs Good: REPO_LOG Entry Comparison

**Purpose:** Learn what makes a REPO_LOG entry excellent by seeing common mistakes side-by-side with best practices.

---

## Comparison 1: Change Clarity

### ❌ BAD (Score: 5/20)

```markdown
### Entry: 2025-11-10 - Updates

Made some changes to files.
```

**Why This Fails:**
- "Updates" - WHAT updates?
- "Some changes" - WHAT changes?
- "to files" - WHICH files?
- No action verbs, no specifics

---

### ✅ GOOD (Score: 20/20)

```markdown
### Entry: 2025-11-10 - Crux Architecture Integration (feat)

**Created:**
1. `profiles/comparisons/CT_vs_MdN.yaml` - Peer-reviewed scoring template
   - Session metadata: YAML hashes, academic sources, Domain 7 diff
   - Crux point structure: id, type, positions, resolution

2. `docs/architecture/CRUX_ARCHITECTURE.md` (Section 6)
   - 3 Crux types: definitional, empirical, framework_limitation
   - Voting protocol: CARRY FORWARD vs NORMALIZE_UNCERTAINTY

**Modified:**
1. `auditors/AUDITOR_ASSIGNMENTS.md` - Added PRO/ANTI pairs for CT vs MdN
2. `docs/repository/librarian_tools/ROLE_PROCESS.md` - Domain 7 Crux duties
```

**Why This Succeeds:**
- Specific title (not "Updates")
- Action verbs (Created, Modified)
- File paths included
- Bullet points with key features

**Rubric: Change Clarity 20/20**

---

## Comparison 2: Categorization

### ❌ BAD (Score: 5/20)

```markdown
**Category:** misc

Did some stuff.
```

**Why This Fails:**
- "misc" category unhelpful (what KIND of change?)
- No rationale (WHY this change?)
- No strategic context

---

### ✅ GOOD (Score: 20/20)

```markdown
**Category:** `feat` (New feature/capability)
**Impact:** HIGH (Affects scoring methodology for all 66 worldview comparisons)

#### Why This Change

**Problem Solved:**
- **Symmetry Concern (Nova Entry 2):** Self-reported scores could drift from peer-reviewed scores without named impasses
- **Transparency Gap:** No mechanism to document *why* scores converge or diverge

**Strategic Goal:**
- Establish gold standard methodology for CT↔MdN pilot
- Scale peer review process to all 66 worldview comparisons

**Related Context:**
- Triggered by Nova Entry 2 (B-STORM_4.md lines 420-485)
- Resolves KD-O1 blocker (how to handle <98% convergence)
```

**Why This Succeeds:**
- Clear category (feat, not "misc")
- Impact level explicit (HIGH)
- Problem explained (symmetry concern)
- Strategic goal stated
- Related context linked

**Rubric: Categorization 20/20**

---

## Comparison 3: Context

### ❌ BAD (Score: 5/20)

```markdown
See commit for details.
```

**Why This Fails:**
- Forces archaeology (must hunt through git history)
- No actionable guidance
- No examples of how to use change

---

### ✅ GOOD (Score: 20/20)

```markdown
#### How to Use This Change

**For Future Scoring Sessions:**

1. **Before Session (Process Claude):**
   ```bash
   # Run VUDU Step 1 validation
   - Validate academic sources
   - Generate YAML hashes
   - Check Domain 7 diff
   ```

2. **During Session (Claude, Grok, Nova):**
   ```yaml
   # If convergence <98% after Round 2:
   - Declare Crux Point
   - Classify type: definitional | empirical | framework_limitation
   - Vote: CARRY FORWARD or NORMALIZE_UNCERTAINTY
   ```

**Documentation:**
- Architecture: [docs/architecture/CFA_ARCHITECTURE.md](../../docs/architecture/CFA_ARCHITECTURE.md) Section 6
- Protocol: [auditors/Bootstrap/VUDU_CFA.md](../../auditors/Bootstrap/VUDU_CFA.md) Step 9
```

**Why This Succeeds:**
- Actionable guidance (concrete commands)
- Examples provided (bash, YAML)
- Documentation links included
- No archaeology required

**Rubric: Context 20/20**

---

## Comparison 4: Traceability

### ❌ BAD (Score: 5/20)

```markdown
[No commit hash, no related work mentioned]
```

**Why This Fails:**
- Can't find code changes (no git commit)
- Can't trace upstream work (no B-STORM/task links)
- Can't identify dependencies

---

### ✅ GOOD (Score: 20/20)

```markdown
#### Traceability

**Git Commit:** `ec4e17a` (B-STORM_4 Click 4 complete)

**Related Sessions:**
- B-STORM_4.md Entry 2 (Nova symmetry concern)
- B-STORM_4.md Entry 3 (Crux architecture solution)
- B-STORM_4.md Entry 6 (Nova pilot approval)

**Dependencies:**
- **Requires:** AUDITOR_ASSIGNMENTS.md (auditor roles), VUDU_CFA.md (Step 1)
- **Enables:** CT↔MdN pilot launch, peer-reviewed scoring
- **Blocks:** None (additive feature)

**Follow-Up Work:**
- [ ] CT↔MdN pilot execution (validate Crux workflow)
- [ ] Quarterly tracking dashboard (if 5+ Crux declared)
```

**Why This Succeeds:**
- Git commit hash (code archaeology)
- Related sessions linked (context)
- Dependencies explicit (upstream/downstream)
- Follow-up work identified

**Rubric: Traceability 20/20**

---

## Comparison 5: Utility for Future

### ❌ BAD (Score: 5/20)

```markdown
[No questions answered, no knowledge preserved, no mistakes prevented]
```

**Why This Fails:**
- Future maintainers must rediscover context
- No lessons captured
- No anti-patterns documented

---

### ✅ GOOD (Score: 20/20)

```markdown
#### Utility for Future Maintainers

**Questions This Entry Answers:**

1. **"When did we add peer-reviewed scoring?"**
   - Answer: 2025-11-10, Crux architecture integration

2. **"Why do we have CRUX_BFI_001 in CT_vs_MdN.yaml?"**
   - Answer: <98% convergence after 3 rounds triggers Crux declaration

3. **"How do I handle disagreements in adversarial scoring?"**
   - Answer: See ROLE_PROCESS.md Domain 7 → Crux orchestration

**Knowledge Preserved:**
- Nova's symmetry concern drove this design
- Crux enables transparency without blocking progress
- VUDU Step 1 pre-check prevents stale profile scoring

**Mistakes Prevented:**
- ❌ Don't delete Crux Points (they're historical record)
- ❌ Don't skip VUDU Step 1 (stale profiles → unreliable scores)
- ❌ Don't rotate auditors before 3+ Crux on same metric
```

**Why This Succeeds:**
- Answers common questions
- Preserves decision context
- Prevents future mistakes
- Saves archaeology time

**Rubric: Utility for Future 20/20**

---

## Summary: REPO_LOG Entry Rubric Application

| Criterion | Bad Example | Good Example | Difference |
|-----------|-------------|--------------|------------|
| **Change Clarity** | 5/20 | 20/20 | +15 (vague vs concrete file list) |
| **Categorization** | 5/20 | 20/20 | +15 ("misc" vs feat + rationale) |
| **Context** | 5/20 | 20/20 | +15 ("see commit" vs actionable guidance) |
| **Traceability** | 5/20 | 20/20 | +15 (missing vs commit + sessions + dependencies) |
| **Utility for Future** | 5/20 | 20/20 | +15 (missing vs questions + knowledge + mistakes) |
| **TOTAL** | **25/100** | **100/100** | **+75 points** |

**Key Insight:** REPO_LOG isn't just "what changed" - it's *why it changed* and *how future maintainers use it*. Bad entries force archaeology (read code, hunt commits, ask people). Good entries answer questions proactively.

---

## Anti-Pattern Gallery

### ❌ Anti-Pattern 1: Vague Title
```markdown
### Entry: 2025-11-10 - Stuff
```
**Fix:** Use action verb + component: "Crux Architecture Integration"

---

### ❌ Anti-Pattern 2: No File Paths
```markdown
Modified some files in the profiles directory.
```
**Fix:** List exact paths: `profiles/comparisons/CT_vs_MdN.yaml`

---

### ❌ Anti-Pattern 3: "See Commit"
```markdown
For details, see commit abc123.
```
**Fix:** Provide actionable guidance + examples in REPO_LOG itself

---

### ❌ Anti-Pattern 4: No Git Hash
```markdown
[No commit reference]
```
**Fix:** Include hash: `**Git Commit:** ec4e17a`

---

### ❌ Anti-Pattern 5: No Future Utility
```markdown
[No questions/knowledge/mistakes section]
```
**Fix:** Add "Questions This Entry Answers" + "Mistakes Prevented"

---

## Quick Checklist

Before submitting REPO_LOG entry, verify:

- [ ] **Title:** Action verb + component (not "Updates")
- [ ] **Category:** feat/fix/refactor/docs/chore (not "misc")
- [ ] **Files:** Exact paths with CREATE/MODIFY/DELETE
- [ ] **Why:** Problem + strategic goal + related context
- [ ] **How:** Actionable guidance with examples
- [ ] **Git:** Commit hash included
- [ ] **Related:** Sessions/tasks/dependencies linked
- [ ] **Questions:** 2-3 common questions answered
- [ ] **Knowledge:** Key decisions preserved
- [ ] **Mistakes:** Anti-patterns documented

**Target:** 90+ score on REPO_LOG Entry Rubric

---

**See Also:**
- [GOOD_REPO_LOG_ENTRY_EXAMPLE.md](../GOOD_REPO_LOG_ENTRY_EXAMPLE.md) - Full annotated exemplar
- [QUALITY_RUBRICS.md](../QUALITY_RUBRICS.md) - Complete rubric with all criteria

---

**Created by:** C4 (B-STORM_5 Click 2)
**Date:** 2025-11-11
**Purpose:** Teach REPO_LOG excellence through contrast
