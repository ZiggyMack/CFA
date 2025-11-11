<!---
FILE: TASK_WORKSHOP_AUTOMATION_v1.md
PURPOSE: Task brief for repository automation and validation scripts (NO EXECUTION YET - planning only)
VERSION: 1.0.0
STATUS: Planned (brief only, awaiting pain point validation)
DEPENDS_ON: ROLE_PROCESS.md, QUALITY_RUBRICS.md, Future_Expansion.md
NEEDED_BY: Future automation specialist, Process Claude (Domain 8)
MOVES_WITH: /auditors/Bootstrap/Tier4_TaskSpecific/Active_Tasks/
CREATED: 2025-11-11 (B-STORM_5 Click 4 - Tier 2 Light)
LAST_UPDATE: 2025-11-11 [B-STORM_5: Initial brief - no execution yet per KD-O1]
--->

# TASK BRIEF: Workshop Automation & Validation Scripts

**Mission:**
> Create automation scripts for repository validation (semantic header checks, link integrity, format linting) and quality enforcement (pre-commit hooks, CI/CD integration) - **ONLY when pain points emerge** (not speculative automation).

**Status:** PLANNED (brief only, awaiting execution trigger)
**Owner:** TBD (Process Claude or future automation specialist)
**Created:** 2025-11-11 (B-STORM_5 Click 4)
**Execution Trigger:** User request OR 3+ manual quality issues caught by reviewers

---

## Problem This Solves

**Current State (Manual Quality Checks):**
- Semantic headers validated by human review (Nova, Process Claude)
- Link integrity checked manually (click links, hope they work)
- Format consistency enforced through rubrics + peer review
- Pre-commit hooks: None (relying on contributor discipline)

**Pain Points (If They Emerge):**
1. **Inconsistent Headers:** Files submitted without VERSION, DEPENDS_ON, LAST_UPDATE
2. **Broken Links:** Cross-references break when files move (discovered post-merge)
3. **Format Drift:** Markdown formatting varies (3 spaces vs 4 spaces, bullet style inconsistencies)
4. **Regression Risk:** Changes break existing docs (no automated smoke tests)

**Solution (When Needed):**
- Automated validation scripts catch issues before commit
- Pre-commit hooks enforce standards (prevent bad commits)
- CI/CD pipeline runs checks on PRs (gate merging)
- Reduce reviewer burden (machines check mechanics, humans check meaning)

---

## Scope Boundaries

### ✅ IN SCOPE (When Executed)

**1. Semantic Header Validator (header_validator.py)**
- Check FILE, PURPOSE, VERSION, STATUS, DEPENDS_ON, LAST_UPDATE present
- Verify VERSION format (e.g., v1.0.0 or 1.0.0)
- Warn if LAST_UPDATE > 90 days old (stale file)
- Exit code 0 (pass) or 1 (fail) for CI/CD integration

**2. Link Integrity Checker (link_checker.py)**
- Scan all Markdown links \[text\](path/to/file.md)
- Verify target file exists (relative path resolution)
- Check for 404s (broken internal links)
- Generate report: "Broken links: 3 | Fixed: 2 | Remaining: 1"

**3. Format Linter (format_linter.py)**
- Enforce 4-space indentation (not 3 or 2)
- Check bullet list style consistency (- vs * vs +)
- Verify code block syntax highlighting (```python not ```py)
- Flag trailing whitespace, mixed line endings (CRLF vs LF)

**4. Pre-Commit Hook Integration**
- Install pre-commit framework (.pre-commit-config.yaml)
- Run validators on staged files (not entire repo)
- Block commit if critical issues found (semantic headers missing)
- Allow commit with warnings (format inconsistencies, stale dates)

**5. CI/CD Pipeline (GitHub Actions or equivalent)**
- Run all validators on PR creation
- Post results as PR comment ("3 issues found - see artifacts")
- Require passing checks before merge (or allow admin override)

### ❌ OUT OF SCOPE (Explicitly Deferred)

**Why These Boundaries:**
This task focuses on *mechanical validation* (headers present, links work, format consistent). Deferred items require human judgment or are speculative.

**Deferred Items:**
- ❌ **Content quality validation** - Reason: Rubrics require human judgment (no AI scoring yet)
- ❌ **Semantic analysis** - Reason: Checking if profile accurately represents worldview = complex NLP
- ❌ **Automated REPO_LOG generation** - Reason: Logger role works well (no pain point)
- ❌ **Dependency graph visualization** - Reason: Nice-to-have, not urgent
- ❌ **Auto-fix scripts** - Reason: Risky (auto-corrections could introduce errors)

---

## Execution Trigger (When to Start)

**DO NOT execute this task until ONE of these conditions is met:**

1. **User Explicitly Requests:**
   - User says "let's automate X" in B-STORM session
   - User frustrated by manual checks ("can we script this?")

2. **Pain Point Threshold (3+ incidents):**
   - 3+ files merged with missing semantic headers (caught post-merge)
   - 3+ broken links discovered after file moves (manual fix required)
   - 3+ format inconsistencies noted in reviews (wasted reviewer time)

3. **Process Claude Recommendation:**
   - Domain 8 health check identifies automation as HIGH-value
   - Quarterly review shows manual validation burden >30 min/week

**Why Wait:**
- Speculative automation = waste (solving problems that don't exist)
- Repository is small (~150 files) - manual checks still feasible
- Automation maintenance has cost (scripts break, need updates)

**Current Status (2025-11-11):**
- ✅ Quality standards established (rubrics, exemplars)
- ✅ Manual reviews working well (Nova, Process Claude catch issues)
- ⏳ No pain points yet (wait for 3+ incidents before automating)

---

## Files to CREATE (When Executed)

**Directory Structure:**
```
/scripts/validation/
├── header_validator.py (~150 lines)
├── link_checker.py (~200 lines)
├── format_linter.py (~180 lines)
├── run_all_checks.sh (orchestration script)
└── README.md (usage instructions)

/.pre-commit-config.yaml (~30 lines)
/.github/workflows/quality-checks.yml (~50 lines) (if using GitHub Actions)
```

**1. scripts/validation/header_validator.py**
- Purpose: Check semantic headers (FILE, PURPOSE, VERSION, etc.)
- Dependencies: Python 3.8+, no external libraries
- Template: See examples/excellence/GOOD_TASK_BRIEF_EXAMPLE.md for structure

**2. scripts/validation/link_checker.py**
- Purpose: Verify all Markdown links resolve
- Dependencies: Python 3.8+, pathlib, re
- Edge cases: Handle ../relative/paths, anchors (#section), external URLs

**3. scripts/validation/format_linter.py**
- Purpose: Enforce format consistency (indentation, bullets, code blocks)
- Dependencies: Python 3.8+, no external libraries
- Output: Warnings (not errors) - format issues don't block commits

**4. scripts/validation/run_all_checks.sh**
- Purpose: Orchestrate all validators (single command)
- Output: Summary report ("Passed: 2 | Failed: 1 | Warnings: 3")
- Exit code: 0 (all pass) or 1 (any fail)

**5. .pre-commit-config.yaml**
- Purpose: Configure pre-commit hooks (header_validator required, format_linter optional)
- Installation: `pre-commit install` (one-time setup)
- Behavior: Run on `git commit`, block if critical issues

**6. .github/workflows/quality-checks.yml** (if using GitHub)
- Purpose: Run validators on PR creation
- Trigger: PR opened, PR updated, push to main
- Output: PR comment with results + link to full logs

---

## Files to MODIFY (When Executed)

**1. docs/repository/REPO_HEALTH_DASHBOARD.md**
- Add automation metrics:
  - Pre-commit hook compliance: X% of commits pass
  - Link integrity: X% of links valid
  - Header compliance: X% of files have complete headers
- Add to "Future Enhancements" section (if already exists)

**2. docs/WAYFINDING_GUIDE.md**
- Add section: "Quality Automation" (reference scripts/validation/)
- Link to validator usage (how to run locally)

**3. docs/training/TRAINING_GROUNDS.md**
- Add Intermediate Skill: "Running Quality Checks" (how to use validators)
- Add to FAQ: "What if pre-commit hook blocks my commit?"

**4. docs/architecture/Future_Expansion.md**
- Mark "Workshop" room as complete
- Document automation coverage (which validations automated, which manual)

---

## Execution Plan (When Triggered)

### **Phase 1: Requirements Validation (Est: 1 hour)**

**Step 1.1: Identify Pain Points**
- [ ] Review last 10 merged PRs (what issues slipped through?)
- [ ] Interview Nova + Process Claude (what's tedious to check manually?)
- [ ] List top 3 pain points (header errors? broken links? format drift?)
- **Output:** Pain point priority list (focus on top 3 only)

**Step 1.2: Scope Refinement**
- [ ] For each pain point, ask: "Is automation worth the maintenance cost?"
- [ ] Defer low-value automation (e.g., formatting if inconsistencies rare)
- [ ] Confirm scope with user (show pain points + proposed automation)
- **Output:** Approved scope (which scripts to build, which to defer)

---

### **Phase 2: Core Validators (Est: 3-4 hours)**

**Step 2.1: Header Validator**
- [ ] Create scripts/validation/header_validator.py
- [ ] Implement checks: FILE, PURPOSE, VERSION, DEPENDS_ON, LAST_UPDATE
- [ ] Test on 10 sample files (profiles/, docs/, auditors/)
- [ ] Verify exit codes (0 = pass, 1 = fail)
- **Expected output:** "Header validation: 8/10 passed, 2 missing VERSION"

**Step 2.2: Link Checker**
- [ ] Create scripts/validation/link_checker.py
- [ ] Parse Markdown links: \[text\](path), handle relative paths, anchors
- [ ] Test on files with known broken links (intentionally introduce 404s)
- [ ] Handle edge cases: external URLs (skip), same-file anchors (#section)
- **Expected output:** "Link validation: 47/50 valid, 3 broken"

**DECISION POINT:** If header_validator + link_checker solve top 2 pain points, defer format_linter. If format drift is #3 pain point, proceed to Step 2.3.

**Step 2.3: Format Linter (Optional)**
- [ ] Create scripts/validation/format_linter.py
- [ ] Check indentation (4 spaces), bullet style (consistent - or *), code blocks (```lang not ```l)
- [ ] Output warnings only (don't block commits)
- **Expected output:** "Format check: 12 warnings (indentation: 7, bullets: 5)"

---

### **Phase 3: Integration (Est: 2-3 hours)**

**Step 3.1: Orchestration Script**
- [ ] Create scripts/validation/run_all_checks.sh
- [ ] Run header_validator, link_checker, format_linter sequentially
- [ ] Aggregate results: "Passed: 2 | Failed: 1 | Warnings: 3"
- [ ] Exit code: 0 (all critical pass) or 1 (any fail)

**Step 3.2: Pre-Commit Hooks**
- [ ] Install pre-commit framework: `pip install pre-commit`
- [ ] Create .pre-commit-config.yaml (hook header_validator)
- [ ] Test: `git commit` → hook runs → blocks if headers missing
- [ ] Document in WAYFINDING_GUIDE.md: "How to install pre-commit hooks"

**Step 3.3: CI/CD Pipeline (Optional)**
- [ ] Create .github/workflows/quality-checks.yml (if using GitHub)
- [ ] Configure triggers: PR opened, PR updated, push to main
- [ ] Post results as PR comment: "Quality check: 2 issues found"
- [ ] Require passing checks (or allow admin override)

---

### **Phase 4: Documentation (Est: 1 hour)**

**Step 4.1: Validator README**
- [ ] Create scripts/validation/README.md
- [ ] Usage instructions: `python header_validator.py path/to/file.md`
- [ ] Installation: Dependencies, pre-commit setup
- [ ] Troubleshooting: Common errors, how to override

**Step 4.2: Update Documentation**
- [ ] REPO_HEALTH_DASHBOARD.md: Add automation metrics
- [ ] WAYFINDING_GUIDE.md: Add "Quality Automation" section
- [ ] TRAINING_GROUNDS.md: Add "Running Quality Checks" skill
- [ ] Future_Expansion.md: Mark Workshop complete

---

### **Phase 5: Validation & Rollout (Est: 1 hour)**

**Step 5.1: Test on Sample PRs**
- [ ] Create 3 test PRs: (1) all pass, (2) header missing, (3) broken link
- [ ] Verify validators catch issues correctly
- [ ] Check pre-commit hook blocks bad commits
- [ ] Confirm CI/CD pipeline posts results

**Step 5.2: Rollout to Team**
- [ ] Announce in B-STORM session: "Quality automation live!"
- [ ] Guide contributors through pre-commit install
- [ ] Monitor first 5 commits (any false positives?)
- [ ] Iterate if validators too strict/too lenient

---

## Success Criteria

**✅ Task Complete When:**

1. **Validators Functional:**
   - header_validator.py catches missing headers (100% accuracy on test files)
   - link_checker.py finds broken links (0 false negatives)
   - format_linter.py flags inconsistencies (warnings only, no false positives)

2. **Integration Working:**
   - Pre-commit hooks block commits with critical issues (headers missing)
   - CI/CD pipeline runs on PRs, posts results
   - Contributors can override hooks if needed (`git commit --no-verify`)

3. **Documentation Complete:**
   - scripts/validation/README.md explains usage
   - WAYFINDING_GUIDE.md links to validators
   - TRAINING_GROUNDS.md teaches "Running Quality Checks"

4. **Metrics Tracked:**
   - REPO_HEALTH_DASHBOARD.md shows automation metrics
   - Pre-commit compliance: X% of commits pass
   - Link integrity: X% of links valid

**❌ NOT Complete Until:**
- [ ] REPO_LOG entry created (document automation rollout)
- [ ] Future_Expansion.md updated (Workshop room marked complete)
- [ ] Nova validates (symmetry check: does automation favor certain workflows?)

---

## Rollback Plan

**If Automation Causes Problems:**

**Scenario 1: Validators too strict (false positives)**
- **Symptom:** Contributors frustrated ("my file is fine, validator complains")
- **Fix:** Adjust validator thresholds (e.g., VERSION format accepts v1.0.0 OR 1.0.0)
- **Rollback:** Temporarily disable pre-commit hooks (`pre-commit uninstall`)

**Scenario 2: Validators too lenient (false negatives)**
- **Symptom:** Issues still slip through (broken links not caught)
- **Fix:** Tighten validation logic (handle more edge cases)
- **Rollback:** Fall back to manual reviews (validators as warnings only)

**Scenario 3: Pre-commit hooks break workflow**
- **Symptom:** Hooks block legitimate commits (e.g., intentional temp files)
- **Fix:** Add .pre-commit-config.yaml exclusions (exclude: '^temp/')
- **Rollback:** `git commit --no-verify` (bypass hooks temporarily)

**If Need to Undo:**
```bash
# Remove pre-commit hooks
pre-commit uninstall

# Delete validator scripts
rm -rf scripts/validation/

# Revert .pre-commit-config.yaml
git checkout HEAD -- .pre-commit-config.yaml

# Remove CI/CD workflow
git rm .github/workflows/quality-checks.yml
```

---

## Trade-Offs

**Benefits:**
- ✅ Catch issues before merge (reduce reviewer burden)
- ✅ Consistent quality enforcement (machines don't get tired)
- ✅ Faster reviews (mechanics automated, humans focus on meaning)
- ✅ Onboarding easier (new contributors get instant feedback)

**Costs:**
- ⚠️ Maintenance burden (scripts need updates as standards evolve)
- ⚠️ False positives (validators may complain about edge cases)
- ⚠️ Learning curve (contributors must install pre-commit, understand errors)
- ⚠️ Reduced flexibility (strict automation may hinder experimentation)

**Decision Criteria:**
- If repository <200 files + manual reviews work well → defer automation
- If 3+ quality issues per week slip through → automate
- If reviewer burden >30 min/week on mechanics → automate

**Current Recommendation (2025-11-11):** DEFER automation until pain points emerge. Manual reviews via rubrics + Nova validation working well for current scale.

---

## Dependencies & Prerequisites

**Before Starting Execution:**

**1. Python 3.8+ Installed:**
- Check: `python --version` (must be ≥3.8)
- If not installed: Follow Python installation guide

**2. Pre-Commit Framework (Optional):**
- Install: `pip install pre-commit`
- Verify: `pre-commit --version`

**3. GitHub Actions (Optional, if using CI/CD):**
- Repo must be on GitHub
- Confirm Actions enabled: Settings → Actions → Allow all actions

**4. Quality Standards Documented:**
- ✅ QUALITY_RUBRICS.md exists (validation targets)
- ✅ Exemplars exist (validators can reference "good" structure)
- ✅ Semantic header standard documented (validators know what to check)

**Current Status (2025-11-11):**
- ✅ Python available
- ✅ Quality standards documented (QUALITY_RUBRICS.md, exemplars)
- ⏳ Pre-commit not yet installed (will install if automation triggered)
- ⏳ CI/CD not yet configured (will configure if automation triggered)

---

## Owner & Timeline

**Owner:** TBD
- **Candidate 1:** Process Claude (Domain 8 responsibility)
- **Candidate 2:** Future automation specialist (if role created)
- **Candidate 3:** User delegates to specific auditor

**Timeline (If Triggered):**
- Phase 1 (Requirements): 1 hour
- Phase 2 (Core Validators): 3-4 hours
- Phase 3 (Integration): 2-3 hours
- Phase 4 (Documentation): 1 hour
- Phase 5 (Rollout): 1 hour
- **Total:** ~8-10 hours

**Blocked By:**
- Nothing (task is ready to execute when triggered)

**Blocks:**
- Nothing (no downstream tasks depend on this)

---

## Appendix: Sample Validator Output

### **header_validator.py (Example Run)**

```bash
$ python scripts/validation/header_validator.py profiles/CLASSICAL_THEISM.md

✅ Header Validation: PASS

FILE: CLASSICAL_THEISM.md ✅
PURPOSE: Classical Theism worldview profile for CFA comparative scoring ✅
VERSION: v0.3.0 ✅
STATUS: Active ✅
DEPENDS_ON: profiles/_docs/ACADEMIC_SOURCES.md, REPO_LOG.md ✅
LAST_UPDATE: 2025-11-10 ✅ (Last updated 1 days ago)

All required fields present. File compliant.
```

**Failure Example:**
```bash
$ python scripts/validation/header_validator.py docs/new_doc.md

❌ Header Validation: FAIL

FILE: new_doc.md ✅
PURPOSE: (missing) ❌
VERSION: (missing) ❌
STATUS: Draft ✅
DEPENDS_ON: (missing) ⚠️ (optional, but recommended)
LAST_UPDATE: (missing) ❌

Critical issues: 2 (PURPOSE, VERSION, LAST_UPDATE missing)
Warnings: 1 (DEPENDS_ON missing)

Fix issues before committing. See docs/WAYFINDING_GUIDE.md for semantic header standards.
```

---

### **link_checker.py (Example Run)**

```bash
$ python scripts/validation/link_checker.py auditors/relay/B-STORM_5.md

🔗 Link Integrity Check

Scanning: auditors/relay/B-STORM_5.md
Found 47 links...

✅ Valid: 44/47 (93.6%)
❌ Broken: 3/47 (6.4%)

Broken Links:
1. [Future_Expansion.md](../../docs/architecture/Future_Expansion.md) → 404
   Line 87: Link target does not exist
   Suggested fix: Check file moved or renamed?

2. [TASK_WORKSHOP_AUTOMATION.md](../../auditors/Bootstrap/Active_Tasks/TASK_WORKSHOP_AUTOMATION.md) → 404
   Line 142: Link target does not exist
   Suggested fix: File in subdirectory? Check path.

3. [B-STORM_1.md](B-STORM_1.md) → 404
   Line 256: Link target does not exist
   Note: B-STORM_1.md does not exist (session numbering starts at B-STORM_2.md?)

Fix broken links before merging.
```

---

### **format_linter.py (Example Run)**

```bash
$ python scripts/validation/format_linter.py docs/training/TRAINING_GROUNDS.md

📝 Format Linter (Warnings Only)

Scanning: docs/training/TRAINING_GROUNDS.md

⚠️ Indentation inconsistency (Line 142): Expected 4 spaces, found 3
⚠️ Bullet style mixed (Line 205): Using '*' but document uses '-' elsewhere
⚠️ Code block language (Line 387): '```py' should be '```python' for consistency

Total warnings: 3
Note: Format issues do not block commits. Consider fixing for consistency.
```

---

## Future Enhancements (Post-Automation)

**If Automation Succeeds:**

1. **Auto-Fix Mode:**
   - Add `--fix` flag to validators
   - Automatically correct trivial issues (trailing whitespace, LAST_UPDATE dates)
   - Require manual review before applying fixes (preview changes)

2. **Dependency Graph Validator:**
   - Check DEPENDS_ON chains for cycles (A → B → A)
   - Verify all DEPENDS_ON files exist
   - Generate visual dependency graph (PNG export)

3. **Content Quality Scoring (AI-powered):**
   - Use LLM to score entries against rubrics (0-100 scale)
   - Flag entries <80 for human review
   - Provide specific improvement suggestions

4. **Automated REPO_LOG Generation:**
   - Parse git commits, generate draft REPO_LOG entry
   - Activate Logger role, fill template with commit metadata
   - Require human review before finalizing

**Current Status:** All future enhancements deferred until core automation validates value.

---

**Created by:** C4 (B-STORM_5 Click 4 - Tier 2 Light)
**Date:** 2025-11-11
**Purpose:** Plan automation for future pain points (NO EXECUTION YET per KD-O1)
**Status:** Planned (brief only, awaiting execution trigger)
**Next Steps:** Monitor for 3+ quality issues slipping through manual reviews, then execute

**The Workshop: Where automation serves necessity, not speculation.** 🔧
