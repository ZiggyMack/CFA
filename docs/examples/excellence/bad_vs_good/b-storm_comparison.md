<!---
FILE: b-storm_comparison.md
PURPOSE: Side-by-side comparison of bad vs good B-STORM entry patterns
VERSION: 1.0.0
STATUS: Example (learning tool)
CREATED: 2025-11-11 (B-STORM_5 Click 2 - Nova feedback)
DEPENDS_ON: ../GOOD_B-STORM_ENTRY_EXAMPLE.md, ../QUALITY_RUBRICS.md
NEEDED_BY: Contributors creating B-STORM relay entries
MOVES_WITH: /examples/excellence/bad_vs_good/
LAST_UPDATE: 2025-11-11 [Created per Nova Entry 2 feedback]
--->

# Bad vs Good: B-STORM Entry Comparison

**Purpose:** Learn what makes a B-STORM entry excellent by seeing common mistakes side-by-side with best practices.

**Reminder:** **1 entry per auditor per Click** - Claude writes odd entries (1, 3, 5...), Nova writes even entries (2, 4, 6...).

---

## Comparison 1: Summary Clarity

### ❌ BAD (Score: 5/20)

```markdown
### Entry 4: Work

Made progress.

— Nova
```

**Why This Fails:**
- "Work" - WHAT work?
- "Made progress" - ON WHAT?
- No indication of status (complete? blocked?)

---

### ✅ GOOD (Score: 20/20)

```markdown
### Entry 9: C4 VUDU Step 1 Pre-Check Complete — Pilot Ready for Launch

**Summary:** Process Claude VUDU Step 1 validation executed successfully. CT↔MdN pilot cleared for adversarial scoring.
```

**Why This Succeeds:**
- Active voice title ("Pre-Check Complete")
- Em dash creates two-part structure: what + status
- One-sentence summary: who did what with what result
- Immediately tells reader: VUDU Step 1 done, pilot GO

**Rubric: Summary Clarity 20/20**

---

## Comparison 2: Problem/Solution Structure

### ❌ BAD (Score: 5/20)

```markdown
Checked some things. Everything looks good.
```

**Why This Fails:**
- "Some things" - WHAT things?
- "Looks good" - HOW do we know?
- No checklist, no verdicts

---

### ✅ GOOD (Score: 20/20)

```markdown
**VUDU Step 1 Tasks Completed:**

**1. Academic Sources Validation** ✅ PASSED

**Classical Theism:**
- ✅ IEP God, Western Concepts - LIVE, comprehensive
- ⚠️ SEP Divine Simplicity - ECONNREFUSED (temporary)

**Verdict:** Academic sources structurally sound. SEP downtime doesn't block pilot.

---

**2. YAML Hash Generation** ✅ COMPLETED

- CT (PRO-CT): `1bbec1e119a2c425`
- MdN (ANTI-MdN): `00cd73274759e218`

---

**3. Domain 7 Diff Check** ✅ PASSED

- CLASSICAL_THEISM.md: v0.3.0 (stable)
- METHODOLOGICAL_NATURALISM.md: v0.3.0 (stable)
```

**Why This Succeeds:**
- Concrete tasks listed (5 total)
- Pass/fail markers (✅⚠️)
- Evidence provided (versions, hashes, statuses)
- Clear verdict for each task

**Rubric: Problem/Solution Structure 20/20**

---

## Comparison 3: Decision Tracking

### ❌ BAD (Score: 5/20)

```markdown
Decided to move forward.
```

**Why This Fails:**
- No readiness criteria
- No explicit GO/NO-GO
- No blockers mentioned
- Vague ("move forward" - to what?)

---

### ✅ GOOD (Score: 20/20)

```markdown
**5. Go/No-Go Decision** ✅ **GO FOR PILOT LAUNCH**

**Readiness Criteria:**
- ✅ Academic sources validated
- ✅ YAML hashes generated
- ✅ Domain 7 diff confirms profiles stable
- ✅ CT_vs_MdN.yaml metadata populated
- ✅ Auditor assignments confirmed
- ✅ Process Claude duties documented
- ✅ Hyperlink architecture integrated
- ✅ Nova Entry 8 approval conditions met

**Blockers:** None.

**Pilot Mission:**
> "re-fortify our CT vs MdN numbers...as well as flush out the story behind the numbers"
```

**Why This Succeeds:**
- Explicit decision (bold + checkmark)
- Readiness criteria (8 items, all ✅)
- Blockers explicitly stated ("None")
- User mission quoted

**Rubric: Decision Tracking 20/20**

---

## Comparison 4: Cross-References

### ❌ BAD (Score: 5/20)

```markdown
[No links to related work, files, or process docs]
```

**Why This Fails:**
- Future readers can't trace context
- No file paths (can't verify claims)
- No related entry links (session flow unclear)

---

### ✅ GOOD (Score: 20/20)

```markdown
**Files Modified This Entry:**
- [profiles/comparisons/CT_vs_MdN.yaml](../../profiles/comparisons/CT_vs_MdN.yaml) - v0.1.0 → v0.1.1

**Cross-References:**
- VUDU Protocol: [auditors/Bootstrap/VUDU_CFA.md](../../auditors/Bootstrap/VUDU_CFA.md) Step 1 (lines 63-115)
- Process Claude Duties: [docs/repository/librarian_tools/ROLE_PROCESS.md](../../docs/repository/librarian_tools/ROLE_PROCESS.md) Domain 7 (lines 905-1128)
- Nova's Pilot Approval: B-STORM_4.md Entry 8 (lines 1800-1819)

**B-STORM_4 Session Status:**
- Click 1: KG1, KD-O1 resolved
- Click 2: Nova symmetry concerns (Entry 2)
- Click 3: Crux architecture solution (Entry 3, 5, 6)
- Click 4: Parallel workstreams complete (Entry 7, 8)
- Click 5: VUDU Step 1 complete ✅
```

**Why This Succeeds:**
- Files modified listed with version changes
- Process docs linked with line numbers
- Related entries referenced (Entry 2, 3, 5, 6, 8)
- Session status provides Click-by-Click progression

**Rubric: Cross-References 20/20**

---

## Comparison 5: Handoff Quality

### ❌ BAD (Score: 5/20)

```markdown
Next: Do the pilot.

— C4
```

**Why This Fails:**
- "Do the pilot" - WHAT steps?
- No owner identified
- No success criteria
- Vague handoff

---

### ✅ GOOD (Score: 20/20)

```markdown
**Next Steps (Post-VUDU Step 1):**

1. **Launch CT↔MdN Adversarial Scoring Session:**
   - Claude (PRO-CT) scores using calibration hash `1bbec1e119a2c425`
   - Grok (ANTI-CT) scores using empirical lens
   - Nova (Fairness) checks symmetry and convergence
   - Target: 98%+ convergence on 7 metrics

2. **Populate CT_vs_MdN.yaml with Peer-Reviewed Scores:**
   - Document self-reported vs peer-reviewed deltas
   - Record convergence percentages
   - Declare Crux Points if <98% after 3 rounds

3. **Establish Gold Standard Methodology:**
   - Document deliberation structure
   - Capture 5-part scaffold usage
   - Create template for remaining 11 worldviews

---

**Handoff to Pilot Session:**

Process Claude pre-check complete. All Entry 8 conditions satisfied. CT↔MdN architecture validated. Profiles stable. Telemetry ready.

🚀 **CT↔MdN PILOT: CLEARED FOR LAUNCH**

— C4
```

**Why This Succeeds:**
- Numbered next steps (4 items)
- Owners identified (Claude PRO-CT, Grok, Nova)
- Success criteria (98%+ convergence)
- Explicit handoff ("CLEARED FOR LAUNCH")
- Closing statement reinforces readiness

**Rubric: Handoff Quality 20/20**

---

## Summary: B-STORM Entry Rubric Application

| Criterion | Bad Example | Good Example | Difference |
|-----------|-------------|--------------|------------|
| **Summary Clarity** | 5/20 | 20/20 | +15 (vague vs active voice + em dash) |
| **Problem/Solution** | 5/20 | 20/20 | +15 (vague vs checklist + verdicts) |
| **Decision Tracking** | 5/20 | 20/20 | +15 (vague vs readiness criteria + GO/NO-GO) |
| **Cross-References** | 5/20 | 20/20 | +15 (missing vs files + docs + entries) |
| **Handoff Quality** | 5/20 | 20/20 | +15 (vague vs numbered steps + owners) |
| **TOTAL** | **25/100** | **100/100** | **+75 points** |

**Key Insight:** B-STORM entries enable *asynchronous collaboration*. Bad entries force next auditor to ask questions ("What did you check? What's next?"). Good entries provide complete context (past work + current status + future steps).

---

## Anti-Pattern Gallery

### ❌ Anti-Pattern 1: Multiple Entries Per Click
```markdown
### Entry 1: C4 Work
### Entry 2: C4 More Work
### Entry 3: Nova Response
```
**Fix:** 1 entry per auditor per Click (Entry 1 = C4, Entry 2 = Nova)

---

### ❌ Anti-Pattern 2: Wall of Text
```markdown
We did a bunch of stuff with the profiles and checked the sources and made sure everything was ready and updated some files and then decided it was good to go...
```
**Fix:** Use headings, bullets, checklists (scannable structure)

---

### ❌ Anti-Pattern 3: No Pass/Fail Markers
```markdown
Checked the sources.
```
**Fix:** Add verdicts: ✅ PASSED, ⚠️ WARNING, 🔴 BLOCKED

---

### ❌ Anti-Pattern 4: No Explicit Decision
```markdown
Things look ready.
```
**Fix:** Bold + checkmark: **✅ GO FOR PILOT LAUNCH**

---

### ❌ Anti-Pattern 5: No Handoff
```markdown
— C4
[Entry ends abruptly]
```
**Fix:** Add "Next Steps" + "Handoff to [Phase/Auditor]" + milestone declaration

---

## Quick Checklist

Before submitting B-STORM entry, verify:

- [ ] **Title:** Active voice + em dash structure (not "Work" or "Updates")
- [ ] **Summary:** One sentence with who/what/result
- [ ] **Tasks:** Checklist with pass/fail markers (✅⚠️🔴)
- [ ] **Decision:** Explicit GO/NO-GO with readiness criteria
- [ ] **Files:** Modified files listed with version changes
- [ ] **Cross-refs:** Related entries + process docs + line numbers
- [ ] **Session Status:** Click-by-Click progression summary
- [ ] **Next Steps:** Numbered, with owners and success criteria
- [ ] **Handoff:** Explicit statement ("CLEARED FOR...", "Nova Entry X is yours")

**Target:** 90+ score on B-STORM Entry Rubric

---

## Pattern Reminder

**Entry Numbering:**
- Click 1: Entry 1 (Claude) → Entry 2 (Nova)
- Click 2: Entry 3 (Claude) → Entry 4 (Nova)
- Click 3: Entry 5 (Claude) → Entry 6 (Nova)

**Formula:** Entry Number = (Auditor Index - 1) × 2 + Click Number

**Handoff Pattern:**
- Odd entries (Claude): End with handoff to Nova
- Even entries (Nova): End with handoff to next Click or pilot

---

**See Also:**
- [GOOD_B-STORM_ENTRY_EXAMPLE.md](../GOOD_B-STORM_ENTRY_EXAMPLE.md) - Full annotated exemplar
- [QUALITY_RUBRICS.md](../QUALITY_RUBRICS.md) - Complete rubric with all criteria

---

**Created by:** C4 (B-STORM_5 Click 2)
**Date:** 2025-11-11
**Purpose:** Teach B-STORM entry excellence through contrast
