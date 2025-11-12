<!---
FILE: QUALITY_RUBRICS.md
PURPOSE: Objective scoring criteria for CFA documentation quality (0-100 scale)
VERSION: 1.0.0
STATUS: Active
CREATED: 2025-11-10 (B-STORM_5 Click 1)
DEPENDS_ON: examples/excellence/README.md
NEEDED_BY: Contributors (self-assessment), reviewers (evaluation)
MOVES_WITH: /examples/excellence/
LAST_UPDATE: 2025-11-10 [B-STORM_5: Tier 1 Costume Room creation]
--->

# Quality Rubrics - Objective Scoring Criteria

**Purpose:** Provide objective, measurable quality standards for CFA documentation. Score your work (or others') on a 0-100 scale to assess excellence.

**How To Use:**
1. Select the appropriate rubric for your document type
2. Score each category (0-20 points each, 5 categories = 100 total)
3. Identify lowest-scoring categories for improvement
4. Aim for 80+ (Very Good) or 90+ (Excellent)

---

## General Documentation Rubric

**Use For:** Any documentation file (README, guide, architecture doc, etc.)

### 1. Completeness (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | All required sections present, no "TBD" or placeholders, comprehensive coverage |
| 15-19 | Most sections complete, minimal placeholders, covers 80%+ of topic |
| 10-14 | Core sections present, some placeholders, covers 60-79% of topic |
| 5-9 | Basic structure only, many placeholders, covers 40-59% of topic |
| 0-4 | Incomplete structure, mostly placeholders, covers <40% of topic |

**Required Sections (typical):**
- Semantic header (FILE, PURPOSE, VERSION, etc.)
- Purpose statement
- Main content (organized logically)
- Cross-references (DEPENDS_ON, NEEDED_BY)
- Change log or version history

---

### 2. Clarity (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Crystal clear purpose, concise language, no jargon without explanation, easy to scan |
| 15-19 | Clear purpose, mostly concise, occasional jargon explained, good scanability |
| 10-14 | Purpose stated but could be clearer, some wordiness, jargon sometimes unexplained |
| 5-9 | Vague purpose, significant wordiness, jargon often unexplained, hard to scan |
| 0-4 | No clear purpose, very wordy, jargon everywhere, impossible to scan |

**Clarity Checks:**
- Can a new contributor understand the purpose in <30 seconds?
- Are sentences concise (avoid "in order to" → use "to")?
- Is jargon defined on first use or linked to glossary?
- Can you scan headings and understand structure?

---

### 3. Consistency (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Perfect semantic headers, formatting matches standards, naming conventions followed |
| 15-19 | Semantic headers present, formatting mostly standard, naming mostly consistent |
| 10-14 | Some semantic headers, formatting partially standard, naming somewhat consistent |
| 5-9 | Minimal semantic headers, formatting inconsistent, naming often breaks conventions |
| 0-4 | No semantic headers, no formatting standards, naming chaotic |

**Consistency Checks:**
- Does semantic header include FILE, PURPOSE, VERSION, DEPENDS_ON, LAST_UPDATE?
- Do cross-references use proper syntax ([\[file\](path)] not bare text)?
- Are headings capitalized consistently (Title Case or Sentence case, not mixed)?
- Do file/folder names follow repository conventions (snake_case for files, PascalCase for roles)?

---

### 4. Utility (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Highly actionable, self-contained, immediately useful, easy to maintain |
| 15-19 | Actionable, mostly self-contained, useful with minimal context, maintainable |
| 10-14 | Somewhat actionable, requires some context, moderately useful, maintenance unclear |
| 5-9 | Vague actions, requires significant context, limited usefulness, hard to maintain |
| 0-4 | No clear actions, cannot use without extensive context, not useful, unmaintainable |

**Utility Checks:**
- Can someone follow the document without asking questions?
- Are examples provided (not just abstract concepts)?
- Is it clear when/how to update this document?
- Does it solve a real problem (not documentation for documentation's sake)?

---

### 5. Navigation (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Table of contents, clear headings, proper anchors, excellent discoverability |
| 15-19 | ToC or clear headings, some anchors, good discoverability |
| 10-14 | Basic headings, minimal anchors, moderate discoverability |
| 5-9 | Poor headings, no anchors, hard to navigate |
| 0-4 | No headings, wall of text, impossible to navigate |

**Navigation Checks:**
- For docs >200 lines: Is there a Table of Contents?
- Are headings descriptive (not "Section 1", but "Purpose and Use Cases")?
- Do links work (no broken references)?
- Can someone find this document via WAYFINDING_GUIDE.md?

---

### **Score Interpretation:**

| Score | Rating | Meaning |
|-------|--------|---------|
| 90-100 | Excellent | Exemplar quality - use as template for others |
| 80-89 | Very Good | Meets all standards - minor improvements possible |
| 70-79 | Good | Acceptable quality - targeted improvements needed |
| 60-69 | Fair | Needs improvement - multiple issues to address |
| 0-59 | Poor | Substantial rework required |

**Target:** 80+ for all documentation, 90+ for Costume Room examples

---

## README-Specific Rubric

**Use For:** README.md files (repository, directory, component)

### 1. Purpose Clarity (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Purpose stated in first 2 sentences, answers "What is this?" and "Why does it exist?" |
| 15-19 | Purpose stated early, answers "What is this?" clearly |
| 10-14 | Purpose stated but vague or buried after intro |
| 5-9 | Purpose unclear, requires reading entire doc |
| 0-4 | No purpose statement |

---

### 2. Quick Start (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Step-by-step quick start, can get value in <5 minutes, examples provided |
| 15-19 | Quick start present, can get value in <10 minutes, basic examples |
| 10-14 | Basic getting started section, takes 10-20 minutes, minimal examples |
| 5-9 | Vague instructions, takes 20+ minutes, no examples |
| 0-4 | No quick start section |

---

### 3. Structure (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Logical flow (Purpose → Quick Start → Details → References), ToC for long READMEs |
| 15-19 | Logical flow, ToC if appropriate |
| 10-14 | Mostly logical, some sections out of order |
| 5-9 | Illogical flow, hard to follow |
| 0-4 | No structure, stream of consciousness |

---

### 4. Completeness (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Covers purpose, usage, examples, troubleshooting, references - nothing missing |
| 15-19 | Covers purpose, usage, examples - minor gaps |
| 10-14 | Covers purpose and usage - missing examples or references |
| 5-9 | Basic coverage only - significant gaps |
| 0-4 | Minimal coverage - mostly incomplete |

---

### 5. Maintenance (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Last updated date, owner identified, update triggers clear, version history |
| 15-19 | Last updated date, owner identified, basic maintenance info |
| 10-14 | Last updated date, unclear ownership |
| 5-9 | Stale (updated >6 months ago), no owner |
| 0-4 | No maintenance info, appears abandoned |

---

## Task Brief Rubric (Tier 4)

**Use For:** Tier 4 task briefs in Active_Tasks/ directory

### 1. Task Definition (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Crystal clear objective, specific deliverable, measurable success criteria |
| 15-19 | Clear objective, specific deliverable, basic success criteria |
| 10-14 | Objective stated, deliverable somewhat vague, unclear success criteria |
| 5-9 | Vague objective, unclear deliverable, no success criteria |
| 0-4 | No clear objective or deliverable |

---

### 2. Files Specified (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Exact files listed (2-5), search commands provided, purpose of each explained |
| 15-19 | Exact files listed, search commands provided |
| 10-14 | Files listed but some ambiguity, search commands missing |
| 5-9 | Vague file references, no search commands |
| 0-4 | No files specified or too many (>5) |

---

### 3. Scope Boundaries (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Clear "You CAN" and "You CANNOT" sections, prevents scope creep |
| 15-19 | Boundaries stated, mostly clear what's in/out of scope |
| 10-14 | Some boundaries, but room for interpretation |
| 5-9 | Vague boundaries, likely scope creep |
| 0-4 | No boundaries, open-ended task |

---

### 4. Bootstrap Efficiency (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Bootstrap <10% (2-5 files only), 90%+ budget available for work |
| 15-19 | Bootstrap 10-15%, 85%+ budget for work |
| 10-14 | Bootstrap 15-20%, 80%+ budget for work |
| 5-9 | Bootstrap 20-30%, <80% budget for work |
| 0-4 | Bootstrap >30%, inefficient Tier 4 task |

---

### 5. Deliverable Clarity (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Exact deliverable name, location, format, success criteria specified |
| 15-19 | Deliverable name and location specified, format clear |
| 10-14 | Deliverable specified but some ambiguity |
| 5-9 | Vague deliverable description |
| 0-4 | No deliverable specified |

---

## REPO_LOG Entry Rubric

**Use For:** Entries in REPO_LOG.md

### 1. Change Clarity (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Crystal clear what changed, why, and impact - no ambiguity |
| 15-19 | Clear what changed, why stated, impact mentioned |
| 10-14 | What changed is clear, why or impact vague |
| 5-9 | What changed is vague, why/impact missing |
| 0-4 | Cryptic change description |

---

### 2. Categorization (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Correct category (FEATURE/FIX/REFACTOR/DOCS/TEST), justification clear |
| 15-19 | Correct category, justification present |
| 10-14 | Correct category, justification weak |
| 5-9 | Wrong category or no categorization |
| 0-4 | No category |

---

### 3. Context (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Links to related issues/tasks, affected files listed, dependencies noted |
| 15-19 | Links to related work, affected files listed |
| 10-14 | Some context, missing links or files |
| 5-9 | Minimal context |
| 0-4 | No context |

---

### 4. Traceability (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Author identified, timestamp, session ID, commit hash (if applicable) |
| 15-19 | Author, timestamp, session ID |
| 10-14 | Author and timestamp only |
| 5-9 | Author only |
| 0-4 | No traceability info |

---

### 5. Utility for Future (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Future readers will understand change and rationale without questions |
| 15-19 | Future readers will mostly understand |
| 10-14 | Future readers will need some additional context |
| 5-9 | Future readers will be confused |
| 0-4 | Entry is useless for future reference |

---

## B-STORM Entry Rubric

**Use For:** Entries in B-STORM session files (relay/ directory)

### 1. Summary Clarity (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | 1-2 sentence summary captures essence, easy to scan |
| 15-19 | Clear summary, captures main points |
| 10-14 | Summary present but could be clearer |
| 5-9 | Vague summary |
| 0-4 | No summary |

---

### 2. Problem/Solution Structure (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Clear problem statement, proposed solutions, decision/outcome documented |
| 15-19 | Problem and solution present, outcome clear |
| 10-14 | Problem or solution vague, outcome present |
| 5-9 | Missing problem statement or solution |
| 0-4 | No structure |

---

### 3. Decision Tracking (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | All decisions documented in Awaiting block (KG/KD), status clear (open/closed) |
| 15-19 | Key decisions in Awaiting block, status mostly clear |
| 10-14 | Some decisions tracked, status sometimes unclear |
| 5-9 | Decisions made but not tracked formally |
| 0-4 | No decision tracking |

---

### 4. Cross-References (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Links to files modified, previous entries, related sessions - full traceability |
| 15-19 | Links to files modified and related work |
| 10-14 | Some links, missing key references |
| 5-9 | Minimal links |
| 0-4 | No links |

---

### 5. Handoff Quality (0-20 points)

| Score | Criteria |
|-------|----------|
| 20 | Next steps clear, blockers identified, owner assigned - perfect handoff |
| 15-19 | Next steps clear, blockers mentioned |
| 10-14 | Next steps present, blockers vague |
| 5-9 | Next steps vague, no blocker identification |
| 0-4 | No handoff info |

---

## How To Apply Rubrics

### **Self-Assessment (Before Submission):**

1. **Score your work** using the appropriate rubric
2. **Identify weak areas** (categories scoring <15)
3. **Improve** those areas before submitting
4. **Re-score** to verify improvements
5. **Aim for 80+** before considering work complete

### **Peer Review (When Reviewing):**

1. **Score the contribution** using the rubric
2. **Provide specific feedback** citing rubric criteria
   - Good: "This scores 12/20 on Clarity because the purpose statement is buried (line 47) instead of in the first 2 sentences. Moving it up would improve to 18/20."
   - Bad: "This isn't clear enough." (no specifics)
3. **Suggest improvements** with example references
   - "See [GOOD_README_EXAMPLE.md](GOOD_README_EXAMPLE.md):1-5 for a strong purpose statement."
4. **Re-score after revisions** to track improvement

### **Quality Tracking (Repository Health):**

1. **Sample random documentation** monthly
2. **Score using rubrics**
3. **Track trends** in REPO_HEALTH_DASHBOARD.md
4. **Celebrate improvements** (scores rising over time)
5. **Target issues** (categories consistently scoring <15)

---

## Rubric Evolution

**How To Propose Changes:**

1. **Identify gap:** What's not measured that should be?
2. **Draft criteria:** Create scoring scale (0-20 with clear levels)
3. **Test on examples:** Apply to 3-5 existing docs to validate
4. **Submit proposal:** Add to REPO_LOG with rationale
5. **Doc Claude integrates:** After review and approval

**Recent Changes:**
- v1.0.0 (2025-11-10): Initial rubrics created (B-STORM_5 Tier 1)

---

## ⚖️ The Pointing Rule

*"To measure is to improve.
To score objectively is to reduce bias.
To track trends is to celebrate growth.
Excellence is quantifiable
when rubrics are clear."*

**Quality Rubrics: Where subjectivity becomes objective.** 📊

---

**Created by:** C4 (B-STORM_5 Click 1)
**Date:** 2025-11-10
**Purpose:** Establish objective quality standards for CFA documentation
**Status:** Active - 5 rubrics defined
**Next:** Apply to examples, track repository health trends

**Measure. Improve. Repeat.** 📈
