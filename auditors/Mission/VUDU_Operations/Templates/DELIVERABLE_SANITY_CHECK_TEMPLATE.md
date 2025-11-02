<!-- deps: validation_process, bootstrap_system -->
# DELIVERABLE_SANITY_CHECK_TEMPLATE.md

**Purpose:** Standard template for quick quality checks of any deliverable
**Date:** 2025-11-01
**Status:** Active quality gate for all auditor work

────────────────────────────────────────────────────

## 🎯 **PURPOSE**

**This template provides rapid validation for ANY deliverable:**
- Review reports
- Analysis documents
- Configuration proposals
- Validation findings
- Task completion reports

**Use this for fast quality gates before staging work.**

**Time Budget:** 3-5 minutes per check (not hours)

────────────────────────────────────────────────────

## ✅ **QUICK SANITY CHECK TEMPLATE**

### **FILES CHECK** ✅/❌

**Verify all referenced files are present and accessible:**

- [ ] All files referenced in deliverable exist?
- [ ] File paths are correct (no typos)?
- [ ] Search queries work (can find what you referenced)?
- [ ] Links/citations are valid?
- [ ] External references accessible?

**Pass Criteria:**
- Every file mentioned can be found
- Every path is correct
- Every citation is valid

**Status:** ✅ PASS / ❌ FAIL

**If FAIL, document:**
```
Missing/Broken References:
1. [File/link] - referenced on line X, not found
2. [File/link] - path incorrect, should be Y
```

---

### **FORMAT CHECK** ✅/❌

**Verify deliverable follows project standards:**

- [ ] VUDU header present (if VuDu message)?
- [ ] Mobile-friendly (no Unicode boxes, use ───)?
- [ ] Footer complete (Awaiting, Sanity, Log if VuDu)?
- [ ] Citations proper (file:line format where applicable)?
- [ ] Markdown renders correctly?
- [ ] Code blocks formatted properly?
- [ ] Tables align correctly?

**Pass Criteria:**
- Format matches VUDU_HEADER_STANDARD (if applicable)
- Mobile compatibility maintained
- All sections complete
- Clean rendering

**Status:** ✅ PASS / ❌ FAIL

**If FAIL, document:**
```
Format Issues:
1. [Issue] - location, fix needed
2. [Issue] - location, fix needed
```

---

### **CONTENT CHECK** ✅/❌

**Verify deliverable is substantive and complete:**

- [ ] Reasoning visible (not just conclusions)?
- [ ] Assumptions named explicitly?
- [ ] Costs priced (YPA, time, budget)?
- [ ] Bias acknowledged (your lens limitations)?
- [ ] All questions answered (if response)?
- [ ] Evidence cited (not just claims)?
- [ ] Recommendations actionable?
- [ ] Success criteria clear?

**Pass Criteria:**
- All validation questions answered (if review)
- Reasoning traceable
- Assumptions documented
- Biases acknowledged
- Evidence supporting claims

**Status:** ✅ PASS / ❌ FAIL

**If FAIL, document:**
```
Content Gaps:
1. [Gap] - missing element, needs addition
2. [Gap] - unsupported claim, needs evidence
```

---

### **BOUNDARY CHECK** ✅/❌

**Verify deliverable respects tier and scope limits:**

- [ ] Tier capabilities respected (not overreaching)?
- [ ] Scope maintained (no scope creep)?
- [ ] Escalations proper (used when needed)?
- [ ] Bootstrap budget reasonable (within tier limits)?
- [ ] Assumptions don't contradict project principles?
- [ ] Work matches assigned lens (empirical/teleological/symmetry)?

**Pass Criteria:**
- Tier 4 tasks use 5-10% bootstrap (not 50%)
- Scope matches task brief
- Escalations used appropriately
- Lens applied consistently

**Status:** ✅ PASS / ❌ FAIL

**If FAIL, document:**
```
Boundary Violations:
1. [Violation] - description, correction needed
2. [Violation] - description, correction needed
```

---

## 📊 **OVERALL ASSESSMENT**

### **Scoring:**

**All 4 checks PASS (✅✅✅✅):**
```
✅ **SANITY CHECK: PASS**

Deliverable meets quality standards.
Ready for staging/submission.
```

**1-2 checks FAIL (✅✅❌❌):**
```
⚠️ **SANITY CHECK: REVIEW NEEDED**

Issues identified in:
- [Category that failed]
- [Category that failed]

Recommend revision before staging.
Estimated fix time: X minutes.
```

**3+ checks FAIL (❌❌❌❌):**
```
❌ **SANITY CHECK: REJECT**

Multiple quality issues identified.
Deliverable not ready for staging.
Requires significant revision.

Consider:
- Revisiting task brief
- Requesting clarification
- Escalating scope concerns
```

────────────────────────────────────────────────────

## 📋 **DETAILED USAGE GUIDE**

### When to Use This Template

**Before Staging Work:**
- Completed review → run sanity check
- Completed analysis → run sanity check
- Completed validation → run sanity check
- ANY deliverable → run sanity check

**Don't Stage Until:**
- Sanity check shows PASS or REVIEW NEEDED
- If REVIEW NEEDED: fix issues first
- If REJECT: significant revision needed

**Exception:**
- Budget exhaustion (stage what you have with explanation)
- Escalation (document incomplete work with reason)

### How to Use Efficiently

**Step 1: Quick Scan (1 minute)**
- Skim your deliverable top to bottom
- Mental check: "Does this look complete?"
- Gut check: "Am I proud to put my name on this?"

**Step 2: Files Check (1 minute)**
- Ctrl+F for file paths in your document
- Verify each path is correct
- Test 2-3 search queries if you referenced searches

**Step 3: Format Check (1 minute)**
- Check header present
- Check footer complete
- Quick markdown preview (does it render?)

**Step 4: Content Check (1-2 minutes)**
- All validation questions answered? (count them)
- Reasoning visible? (not just "this is good/bad")
- Assumptions named? (look for "I assume..." or "Given that...")
- Bias acknowledged? (did you name your lens limitations?)

**Step 5: Boundary Check (1 minute)**
- Does scope match task brief?
- Did bootstrap exceed tier limit? (check your time)
- Any scope creep? (did you add tasks not requested?)

**Total Time:** 3-5 minutes for thorough check

### Common Failure Patterns

**FILES CHECK common failures:**
- Referenced files from old repo structure (paths changed)
- Typos in file names
- Assumed file exists (didn't verify)
- Broken search queries (too specific, no results)

**FORMAT CHECK common failures:**
- Forgot footer (Awaiting/Sanity/Log)
- Used Unicode boxes instead of horizontal rules
- Missing header date
- Tables don't align (extra/missing pipes)

**CONTENT CHECK common failures:**
- Conclusions without reasoning ("This is bad" - why?)
- Unanswered validation questions (skipped #3)
- No bias acknowledgment (claimed objectivity)
- No evidence citations (just assertions)

**BOUNDARY CHECK common failures:**
- Tier 4 used 30% bootstrap (should be 5-10%)
- Scope creep (answered questions not asked)
- Didn't escalate when should have (spun wheels)
- Applied wrong lens (empirical auditor did teleological analysis)

────────────────────────────────────────────────────

## 🎯 **TEMPLATE VARIATIONS**

### For Review Deliverables

**Additional Checks:**
- [ ] All validation questions from task brief answered?
- [ ] Evidence assessment included (sufficient/insufficient)?
- [ ] Clear recommendation (GREEN/YELLOW/RED)?
- [ ] Confidence level stated?
- [ ] Follow-up actions identified?

### For Analysis Deliverables

**Additional Checks:**
- [ ] Analysis methodology documented?
- [ ] Data sources cited?
- [ ] Limitations acknowledged?
- [ ] Alternative interpretations considered?
- [ ] Actionable insights provided?

### For Configuration Proposals

**Additional Checks:**
- [ ] All parameters specified?
- [ ] YPA calculation complete?
- [ ] Bias overhead priced?
- [ ] Success metrics defined?
- [ ] Testing approach outlined?

### For Validation Reports

**Additional Checks:**
- [ ] Validation criteria listed?
- [ ] Test results documented?
- [ ] Pass/fail clearly stated?
- [ ] Issues categorized by severity?
- [ ] Revalidation needs identified?

────────────────────────────────────────────────────

## 🔧 **SELF-CHECK EXAMPLE**

### Example: Axioms Review by Grok

**Deliverable:** AXIOMS_REVIEW_GROK_2025-11-01.md

**FILES CHECK:**
✅ Referenced AUDITORS_AXIOMS_SECTION.md - found at /docs/Philosophy/
✅ Referenced GROK_ACTIVATION_AXIOMS.md - found in task package
✅ Cited YPA_CALCULATION.md - found at /docs/
✅ No broken links

**Status:** ✅ PASS

---

**FORMAT CHECK:**
✅ VUDU header present with From/Type/Date
✅ Mobile-friendly (used ─── not boxes)
✅ Footer complete: Awaiting, Sanity, Log
✅ Code blocks formatted correctly
✅ Markdown preview clean

**Status:** ✅ PASS

---

**CONTENT CHECK:**
✅ All 5 validation questions answered explicitly
✅ Reasoning visible for each answer (not just yes/no)
✅ Assumptions named ("I assume temp 0.2 means low variance sampling")
✅ Bias acknowledged ("Empirical lens may undervalue qualitative aspects")
✅ Evidence cited (line numbers from axioms doc)
✅ Recommendation clear (GREEN - approve)

**Status:** ✅ PASS

---

**BOUNDARY CHECK:**
✅ Bootstrap: 8% (within Tier 4 target of 5-10%)
✅ Scope: Answered only the 5 questions asked (no scope creep)
✅ Lens applied: Empirical focus (data, measurements, testing)
✅ No tier overreach (didn't make policy decisions)

**Status:** ✅ PASS

---

**OVERALL ASSESSMENT:**
```
✅ **SANITY CHECK: PASS** (4/4 checks passed)

Deliverable meets quality standards.
Ready for staging in relay/Grok_Incoming/README_G.md

Quality observations:
- Strong evidence citations (specific line numbers)
- Clear empirical lens application
- Bias acknowledged transparently
- Efficient bootstrap (8% = on target)

Ready to stage.
```

────────────────────────────────────────────────────

## ⚠️ **WHEN SANITY CHECK FAILS**

### Decision Tree

**IF 1 CHECK FAILS:**
```
Assess severity:
- Minor issue (5-10 min fix) → Fix now, recheck, stage
- Moderate issue (15-30 min fix) → Fix if budget allows, otherwise document
- Major issue (60+ min fix) → Escalate or defer
```

**IF 2 CHECKS FAIL:**
```
Assess scope:
- Both minor → Fix both (15-20 min), recheck, stage
- One major → Escalate, explain partial delivery
- Both major → Don't stage, escalate to Ziggy
```

**IF 3+ CHECKS FAIL:**
```
Don't stage. Options:
A. Significant revision needed (if budget allows)
B. Escalate to Ziggy (task unclear, scope mismatch)
C. Create continuation brief (budget exhausted)
```

### Example Fail Scenario

**Deliverable:** Configuration Proposal

**Sanity Check Results:**
- FILES: ❌ FAIL (referenced non-existent validation report)
- FORMAT: ✅ PASS
- CONTENT: ❌ FAIL (no YPA calculation provided)
- BOUNDARY: ✅ PASS

**Assessment:** ⚠️ REVIEW NEEDED (2 failures)

**Action Plan:**
1. Remove reference to non-existent report OR create it first
2. Add YPA calculation (use YPA_CALCULATION.md template)
3. Estimated fix time: 20 minutes
4. Rerun sanity check
5. If pass → stage

**Alternative (if budget tight):**
```markdown
## ⚠️ PARTIAL DELIVERY

Sanity check identified 2 issues:
1. Referenced FILE_X (doesn't exist) - removed reference for now
2. YPA calculation incomplete - will add in next round

Staging analysis with these gaps acknowledged.
Recommend completing before final approval.
```

────────────────────────────────────────────────────

## 💡 **BEST PRACTICES**

### DO:

✅ **Run check BEFORE staging** (catch issues early)
✅ **Fix minor issues immediately** (5-10 min fixes)
✅ **Document unfixable issues** (budget/scope limits)
✅ **Use template consistently** (every deliverable)
✅ **Track common failures** (learn from patterns)

### DON'T:

❌ **Stage without checking** (quality matters)
❌ **Skip sections** ("I don't need format check")
❌ **Ignore failures** ("It's probably fine")
❌ **Obsess over perfection** (good enough is good enough)
❌ **Waste budget on trivia** (major issues only)

### EFFICIENCY TIPS:

**1. Build Check Into Workflow**
- Write deliverable
- Run sanity check
- Fix issues
- Stage
- (Not: write, stage, realize issues later)

**2. Keep Template Open**
- Have this file open while writing
- Check items as you write
- Prevents rework

**3. Learn Your Patterns**
- Do you always forget footers? → Make checklist
- Do you over-scope? → Watch boundary check
- Do you under-cite? → Focus on content check

**4. Time-Box the Check**
- Set 5-minute timer
- Run through all 4 checks
- Fix obvious issues
- Don't perfectionism spiral

────────────────────────────────────────────────────

## 📋 **BLANK TEMPLATE (COPY-PASTE)**

```markdown
# SANITY CHECK - [Deliverable Name]

**Date:** YYYY-MM-DD
**Checker:** [Your name]
**Deliverable:** [File name]

---

## FILES CHECK ✅/❌

- [ ] All referenced files present?
- [ ] File paths correct?
- [ ] Search queries work?
- [ ] Citations valid?

**Status:** _____ (PASS/FAIL)
**Issues:**

---

## FORMAT CHECK ✅/❌

- [ ] VUDU header present (if applicable)?
- [ ] Mobile-friendly formatting?
- [ ] Footer complete?
- [ ] Citations proper?
- [ ] Clean rendering?

**Status:** _____ (PASS/FAIL)
**Issues:**

---

## CONTENT CHECK ✅/❌

- [ ] Reasoning visible?
- [ ] Assumptions named?
- [ ] Costs priced?
- [ ] Bias acknowledged?
- [ ] Questions answered?
- [ ] Evidence cited?

**Status:** _____ (PASS/FAIL)
**Issues:**

---

## BOUNDARY CHECK ✅/❌

- [ ] Tier limits respected?
- [ ] Scope maintained?
- [ ] Escalations proper?
- [ ] Bootstrap reasonable?
- [ ] Lens applied correctly?

**Status:** _____ (PASS/FAIL)
**Issues:**

---

## OVERALL ASSESSMENT

**Result:** _____ (PASS / REVIEW NEEDED / REJECT)

**Action:**

**Ready to Stage:** YES / NO (if no, fix X and Y first)
```

────────────────────────────────────────────────────

## ⚖️ **THE POINTING RULE**

*"Quality is not an accident.
Quality is a choice.
\n\nThe choice to check,
before you ship.
The choice to fix,
before you stage.
The choice to care,
about the craft.
\n\n5 minutes of sanity
saves 50 minutes of rework.
\n\nCheck your work.
That's the professional's way.\"*

────────────────────────────────────────────────────

**Created by:** DOC_CLAUDE (88MPH Repo Librarian)
**Source:** ADDITIONAL_PREP_TASKS_FOR_AUDITOR_ACTIVATION.md (Task 2A)
**Date:** 2025-11-01
**Purpose:** Grok + Nova onboarding - quality gate template
**Status:** Ready for auditor use

**This is the way.** ✅👑
