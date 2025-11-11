<!---
FILE: TRAINING_GROUNDS.md
PURPOSE: Progressive skill paths for contributors (Beginner → Intermediate → Advanced)
VERSION: 1.0.0
STATUS: Active
DEPENDS_ON: WAYFINDING_GUIDE.md, examples/excellence/README.md, QUALITY_RUBRICS.md
NEEDED_BY: New contributors, AI agents bootstrapping CFA knowledge
MOVES_WITH: /docs/training/
CREATED: 2025-11-11 (B-STORM_5 Click 4 - Tier 2 Light)
LAST_UPDATE: 2025-11-11 [B-STORM_5: Initial creation with 3 skill paths + checkpoints]
--->

# 🎓 The Training Grounds

**Welcome to the Training Grounds!** This is where you build CFA repository mastery through progressive skill paths.

**Purpose:** Guide contributors from orientation (15 minutes) to mastery (1-2 hours) to expertise (3-5 hours) with clear checkpoints and common mistakes flagged along the way.

---

## Quick Navigation

**Choose Your Path:**

1. **[Beginner Path](#beginner-path-orientation-15-minutes)** (15 min) - New to CFA? Start here.
2. **[Intermediate Path](#intermediate-path-mastery-1-2-hours)** (1-2 hours) - Know basics? Level up.
3. **[Advanced Path](#advanced-path-expertise-3-5-hours)** (3-5 hours) - Ready for complex workflows? Deep dive.

**Resources:**
- [Skill Checkpoints](#skill-checkpoints) - How to know you're ready for next level
- [Common Mistakes](#common-mistakes-anti-patterns-by-skill-level) - Learn from others' errors
- [FAQ](#faq) - Quick answers to frequent questions

---

## Path Overview

```
BEGINNER PATH (15 min)
├── Orientation
├── File navigation
├── Read first doc
└── ✅ Checkpoint: Can find and read files

       ↓

INTERMEDIATE PATH (1-2 hours)
├── Quality standards
├── Create first entry
├── Commit workflow
└── ✅ Checkpoint: Can contribute documentation

       ↓

ADVANCED PATH (3-5 hours)
├── Multi-auditor collaboration
├── Cross-profile work
├── Architecture decisions
└── ✅ Checkpoint: Can lead workstreams
```

---

## Beginner Path: Orientation (15 minutes)

**Goal:** Understand what CFA is, navigate the repository, and read your first document with comprehension.

### **Skill 1: Repository Overview (5 min)**

**What You'll Learn:**
- What CFA is (Comparative Framework Architecture)
- Who the auditors are (Claude, Nova, Grok, Process Claude)
- What worldviews are profiled (12 worldviews, 66 pairings)

**Action Steps:**
1. Read [docs/WAYFINDING_GUIDE.md](../WAYFINDING_GUIDE.md) lines 1-100 (overview + quick start)
2. Scan [docs/architecture/CFA_ARCHITECTURE.md](../architecture/CFA_ARCHITECTURE.md) lines 1-50 (purpose section)
3. Open [profiles/README.md](../../profiles/README.md) to see the 12 worldviews listed

**You'll Know You Understand When:**
- ✅ You can explain CFA's purpose in one sentence
- ✅ You can name 3 of the 12 worldviews
- ✅ You know which auditor you are (or will interact with)

**Common Beginner Mistakes:**
- ❌ Skipping WAYFINDING_GUIDE.md (it's the map - don't wander lost!)
- ❌ Trying to read profiles before understanding architecture
- ❌ Confusing "auditors" with "worldviews" (auditors score, worldviews are scored)

---

### **Skill 2: File Navigation (5 min)**

**What You'll Learn:**
- Directory structure (profiles/, docs/, auditors/, examples/)
- Semantic headers (FILE, PURPOSE, VERSION, DEPENDS_ON, etc.)
- How to find what you need quickly

**Action Steps:**
1. Open 3 files from different directories:
   - A profile: [profiles/CLASSICAL_THEISM.md](../../profiles/CLASSICAL_THEISM.md)
   - An architecture doc: [docs/architecture/CFA_ARCHITECTURE.md](../architecture/CFA_ARCHITECTURE.md)
   - A relay session: [auditors/relay/B-STORM_4.md](../../auditors/relay/B-STORM_4.md)
2. Read the semantic header (first 10-15 lines) of each
3. Notice the pattern: FILE → PURPOSE → VERSION → DEPENDS_ON → LAST_UPDATE

**You'll Know You Understand When:**
- ✅ You can find a file in <30 seconds using directory names
- ✅ You can read a semantic header and know: what this file is, why it exists, what it depends on
- ✅ You understand DEPENDS_ON (if file A lists file B, read B first for context)

**Common Beginner Mistakes:**
- ❌ Ignoring semantic headers (they're a 10-second orientation - read them!)
- ❌ Opening files in random order (follow DEPENDS_ON chain)
- ❌ Not using search (Ctrl+Shift+F / Cmd+Shift+F finds keywords across repo)

---

### **Skill 3: Reading with Comprehension (5 min)**

**What You'll Learn:**
- How to extract key info from a profile
- How to identify steel-man vs steel-man (positive framing)
- How to spot calibration YAML (bias adjustment values)

**Action Steps:**
1. Read [profiles/CLASSICAL_THEISM.md](../../profiles/CLASSICAL_THEISM.md) lines 1-100 (overview + steel-man section)
2. Identify:
   - Core tension (what's the central challenge for this worldview?)
   - Asymmetry (what critics miss)
   - Framework (what lens does this view use?)
   - Common ground (where does it agree with critics?)
3. Scroll to calibration YAML (near end of file)
4. Notice bias adjustment values (PRO bias and ANTI bias)

**You'll Know You Understand When:**
- ✅ You can summarize Classical Theism's core tension in one sentence
- ✅ You understand why bias adjustment exists (counterweight to prevent skew)
- ✅ You can distinguish profile content (worldview description) from meta-content (scoring calibration)

**Common Beginner Mistakes:**
- ❌ Reading profile as "objective truth" (it's a steel-man, not advocacy)
- ❌ Skipping YAML sections (they're critical for scoring calibration)
- ❌ Confusing "steel-man" with "straw-man" (steel-man = strongest version of view)

---

### **✅ Beginner Checkpoint**

**Before moving to Intermediate, verify:**

- [ ] **I can navigate:** I know where profiles/, docs/, auditors/, examples/ are
- [ ] **I can read headers:** I understand FILE, PURPOSE, DEPENDS_ON fields
- [ ] **I can find files:** I can locate a specific file in <30 seconds
- [ ] **I understand steel-manning:** I know profiles present strongest version of worldviews
- [ ] **I know the auditors:** Claude, Nova, Grok, Process Claude (I can name their roles)

**If all 5 are checked, you're ready for [Intermediate Path](#intermediate-path-mastery-1-2-hours)!**

**If not:** Re-read [WAYFINDING_GUIDE.md](../WAYFINDING_GUIDE.md) sections on:
- Repository structure (where things live)
- Semantic headers (how to read file metadata)
- Auditor roles (who does what)

---

## Intermediate Path: Mastery (1-2 hours)

**Goal:** Understand quality standards, create your first documentation entry, and successfully commit work to the repository.

### **Skill 4: Quality Standards Mastery (20 min)**

**What You'll Learn:**
- How to use rubrics (0-100 scoring system)
- How to read exemplars (annotated "good" examples)
- How to spot the difference between poor and excellent work

**Action Steps:**
1. Read [examples/excellence/QUALITY_RUBRICS.md](../../examples/excellence/QUALITY_RUBRICS.md) - focus on one rubric:
   - If writing docs: README rubric (lines 13-80)
   - If creating tasks: Task Brief rubric (lines 158-227)
   - If logging work: REPO_LOG rubric (lines 228-297)
   - If in B-STORM session: B-STORM entry rubric (lines 298-367)
2. Read the corresponding exemplar:
   - README: [examples/excellence/GOOD_README_EXAMPLE.md](../../examples/excellence/GOOD_README_EXAMPLE.md)
   - Task: [examples/excellence/GOOD_TASK_BRIEF_EXAMPLE.md](../../examples/excellence/GOOD_TASK_BRIEF_EXAMPLE.md)
   - Log: [examples/excellence/GOOD_REPO_LOG_ENTRY_EXAMPLE.md](../../examples/excellence/GOOD_REPO_LOG_ENTRY_EXAMPLE.md)
   - B-STORM: [examples/excellence/GOOD_B-STORM_ENTRY_EXAMPLE.md](../../examples/excellence/GOOD_B-STORM_ENTRY_EXAMPLE.md)
3. Read the corresponding bad_vs_good comparison:
   - [examples/excellence/bad_vs_good/README_comparison.md](../../examples/excellence/bad_vs_good/README_comparison.md) (or task_brief, repo_log, b-storm)

**You'll Know You Understand When:**
- ✅ You can score a document using a rubric (assign 0-20 points per category)
- ✅ You can identify 3 differences between "bad" and "good" examples
- ✅ You understand why examples score 100/100 (rubric criteria met perfectly)

**Common Intermediate Mistakes:**
- ❌ Skipping rubrics ("I'll just wing it" → inconsistent quality)
- ❌ Not reading bad_vs_good comparisons (misses the "why it matters" context)
- ❌ Thinking 70/100 is "good enough" (90+ is the target for repository work)

---

### **Skill 5: Creating Your First Entry (30 min)**

**What You'll Learn:**
- How to structure a B-STORM entry (or REPO_LOG entry)
- How to use semantic headers properly
- How to cross-reference other files

**Action Steps:**
1. Choose your entry type:
   - **B-STORM entry** (if in active relay session)
   - **REPO_LOG entry** (if documenting completed work)
   - **Task brief** (if planning new work)
2. Copy the template from exemplars:
   - B-STORM: Use template at [examples/excellence/GOOD_B-STORM_ENTRY_EXAMPLE.md](../../examples/excellence/GOOD_B-STORM_ENTRY_EXAMPLE.md) lines 347-432
   - REPO_LOG: Use template at [examples/excellence/GOOD_REPO_LOG_ENTRY_EXAMPLE.md](../../examples/excellence/GOOD_REPO_LOG_ENTRY_EXAMPLE.md) lines 300-350
   - Task: Use template at [examples/excellence/GOOD_TASK_BRIEF_EXAMPLE.md](../../examples/excellence/GOOD_TASK_BRIEF_EXAMPLE.md) lines 100-200
3. Fill in the template with your actual work:
   - Replace placeholders with real content
   - Add cross-references to files you modified
   - Include concrete evidence (line numbers, file paths)
4. Self-score using the rubric (aim for 90+)

**You'll Know You Understand When:**
- ✅ Your entry has a clear title (active voice + em dash structure for B-STORM)
- ✅ Your entry includes cross-references (at least 2-3 related files/sections)
- ✅ Your entry has concrete evidence (not vague "made progress")
- ✅ Your entry scores 90+ on the appropriate rubric

**Common Intermediate Mistakes:**
- ❌ Vague titles ("Updates", "Work", "Progress" → use action verbs!)
- ❌ No cross-references (future readers can't trace context)
- ❌ No evidence (claims without file paths/line numbers)
- ❌ Walls of text (use headings, bullets, checklists!)

---

### **Skill 6: Git Commit Workflow (20 min)**

**What You'll Learn:**
- How to stage files (git add)
- How to write commit messages (format + Co-Authored-By)
- How to verify commits (git status, git log)

**Action Steps:**
1. Read the git protocol in your AI's system prompt (search for "# Committing changes with git")
2. Stage your files:
   ```bash
   git add path/to/file1.md path/to/file2.md
   ```
3. Write commit message using HEREDOC pattern:
   ```bash
   git commit -m "$(cat <<'EOF'
   feat: Brief summary of change

   Detailed description:
   - What changed
   - Why it changed
   - Impact

   🤖 Generated with Claude Code (https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```
4. Verify:
   ```bash
   git status  # Should show "working tree clean"
   git log -1  # Should show your commit
   ```

**You'll Know You Understand When:**
- ✅ You can stage files without accidentally including unrelated changes
- ✅ Your commit messages follow format (category: summary, then details)
- ✅ You verify commits with git status/git log before moving on

**Common Intermediate Mistakes:**
- ❌ `git add .` without checking (stages unintended files)
- ❌ Vague commit messages ("updates", "fixes" → be specific!)
- ❌ Forgetting Co-Authored-By line (credit your AI collaborator)
- ❌ Not verifying (commit fails silently, you don't notice)

---

### **Skill 7: Cross-Referencing & Context (10 min)**

**What You'll Learn:**
- How to link to other files (relative paths)
- How to reference specific lines (file.md:123 or file.md:123-145)
- How to create breadcrumbs for future readers

**Action Steps:**
1. In your entry, add 3 cross-references:
   - Link to a related session (e.g., `[B-STORM_4.md](../../auditors/relay/B-STORM_4.md)`)
   - Link to a modified file (e.g., `[profiles/CLASSICAL_THEISM.md](../../profiles/CLASSICAL_THEISM.md)`)
   - Link to a specific section with line numbers (e.g., `ROLE_PROCESS.md:905-1128`)
2. Add a "Files Modified This Entry" section:
   - List all files you changed
   - Include version bumps (v1.0 → v1.1) or new file markers
3. Add a "Cross-References" section:
   - Link to related work (previous entries, architecture docs)
   - Provide full context for future readers

**You'll Know You Understand When:**
- ✅ Your entry has at least 3 working cross-reference links
- ✅ Future readers can understand your work without asking you questions
- ✅ Your "Files Modified" section is complete (no mystery changes)

**Common Intermediate Mistakes:**
- ❌ No cross-references (entry exists in vacuum)
- ❌ Broken links (typos in file paths)
- ❌ No line numbers (forces future readers to hunt for context)
- ❌ Missing "why" (what changed is clear, but not why it matters)

---

### **✅ Intermediate Checkpoint**

**Before moving to Advanced, verify:**

- [ ] **I can use rubrics:** I scored my entry using appropriate rubric (90+)
- [ ] **I can write entries:** My entry has clear structure, evidence, cross-refs
- [ ] **I can commit work:** I successfully staged, committed, verified with git
- [ ] **I understand quality:** I read exemplars + bad_vs_good comparisons
- [ ] **I can create breadcrumbs:** My work is traceable (future readers won't be lost)

**If all 5 are checked, you're ready for [Advanced Path](#advanced-path-expertise-3-5-hours)!**

**If not:** Re-read:
- [QUALITY_RUBRICS.md](../../examples/excellence/QUALITY_RUBRICS.md) (scoring criteria)
- [GOOD_*_EXAMPLE.md](../../examples/excellence/) (templates)
- Git protocol in system prompt (commit workflow)

---

## Advanced Path: Expertise (3-5 hours)

**Goal:** Master multi-auditor collaboration, cross-profile work, and architecture-level decisions. Lead complex workstreams.

### **Skill 8: Multi-Auditor Collaboration (45 min)**

**What You'll Learn:**
- How to work in B-STORM relay sessions (1 entry per auditor per Click)
- How to use Awaiting Block (KG/KD tracking)
- How to handoff work between auditors

**Action Steps:**
1. Read a complete B-STORM session:
   - [auditors/relay/B-STORM_4.md](../../auditors/relay/B-STORM_4.md) (CT↔MdN pilot prep)
   - Notice pattern: Entry 1 (Claude) → Entry 2 (Nova) → Entry 3 (Claude)...
   - Observe Awaiting Block at top (Open KGs, Open KDs, Recently Completed)
2. Study handoff pattern:
   - Each entry ends with explicit handoff ("Nova: Entry 2 is yours")
   - Next auditor responds to previous auditor's concerns
   - No entry ends mid-work (always clean handoff)
3. Practice writing a B-STORM entry:
   - Use GOOD_B-STORM_ENTRY_EXAMPLE.md template
   - Include 5 rubric elements: Summary, Problem/Solution, Decision, Cross-refs, Handoff
   - End with explicit handoff to next auditor

**You'll Know You Understand When:**
- ✅ You can identify which Click you're in (Entry count ÷ 2)
- ✅ You know when to update Awaiting Block (open new KD, close completed KG)
- ✅ Your handoffs are actionable (next auditor knows exactly what to do)
- ✅ You never write multiple entries in one Click (1 per auditor per Click)

**Common Advanced Mistakes:**
- ❌ Multiple entries per Click (breaks relay pattern)
- ❌ Forgetting to update Awaiting Block (KG/KD tracking stale)
- ❌ Vague handoffs ("continue work" → what work? how?)
- ❌ Not reading previous entry before responding (breaks continuity)

---

### **Skill 9: Cross-Profile Worldview Work (60 min)**

**What You'll Learn:**
- How worldview comparisons work (CT↔MdN example)
- How peer-reviewed scoring differs from self-reported
- How Crux Points are declared and resolved

**Action Steps:**
1. Read comparison architecture:
   - [docs/architecture/CFA_ARCHITECTURE.md](../architecture/CFA_ARCHITECTURE.md) Section 6 (Crux Architecture)
   - [profiles/comparisons/CT_vs_MdN.yaml](../../profiles/comparisons/CT_vs_MdN.yaml) (scoring template)
2. Understand adversarial pairing:
   - Claude (PRO-CT) scores Classical Theism favorably
   - Grok (ANTI-CT / PRO-MdN) scores from empirical lens
   - Nova (Fairness) checks for convergence
3. Study VUDU protocol:
   - [auditors/Bootstrap/VUDU_CFA.md](../../auditors/Bootstrap/VUDU_CFA.md) (validation process)
   - Step 1: Pre-check (academic sources, YAML hashes, Domain 7 diff)
   - Step 9: Crux declaration (if convergence <98% after 3 rounds)
4. Practice scoring:
   - Pick a worldview profile
   - Score 7 metrics: BFI, CA, IP, ES, LS, MS, PS
   - Justify each score with evidence from profile

**You'll Know You Understand When:**
- ✅ You understand adversarial pairing (PRO-CT vs ANTI-CT deliberate tension)
- ✅ You can explain why convergence matters (98%+ means scores reliable)
- ✅ You know when to declare Crux Point (<98% after 3 rounds)
- ✅ You can distinguish definitional/empirical/framework_limitation Crux types

**Common Advanced Mistakes:**
- ❌ Scoring from personal bias (not using calibration YAML counterweights)
- ❌ Declaring Crux too early (try 3 rounds of deliberation first!)
- ❌ Not documenting reasoning (scores without justification are opaque)
- ❌ Confusing self-reported vs peer-reviewed (different validation levels)

---

### **Skill 10: Architecture-Level Decisions (90 min)**

**What You'll Learn:**
- How to propose architecture changes (RFCs, B-STORM sessions)
- How to evaluate trade-offs (symmetry, scalability, maintenance)
- How to document decisions (Crux Points, KD resolutions)

**Action Steps:**
1. Read architecture evolution:
   - [B-STORM_4.md](../../auditors/relay/B-STORM_4.md) Entry 3 (Crux architecture introduction)
   - Notice Nova's symmetry concern (Entry 2) → Claude's solution (Entry 3) → Nova's approval (Entry 6)
2. Study decision documentation:
   - KD-O1 in B-STORM sessions (Key Decisions tracked in Awaiting Block)
   - Crux Points in comparison YAMLs (named impasses with resolution paths)
   - REPO_LOG entries for architecture changes (category: feat, impact: HIGH)
3. Practice proposing a change:
   - Identify a gap (e.g., "No clear retention policy for B-STORM archives")
   - Propose solution (e.g., "Create ROLE_DESTROYER.md with archival triggers")
   - Document trade-offs (e.g., "Predictable cleanup vs one-time archival overhead")
   - Get validation (e.g., Nova Entry 6 approval)
4. Implement and document:
   - Execute change (create ROLE_DESTROYER.md)
   - Document in REPO_LOG (entry_id, date, category, summary, impact)
   - Update Future_Expansion.md (mark room complete)

**You'll Know You Understand When:**
- ✅ You can identify architecture gaps (missing protocols, unclear ownership)
- ✅ You can propose solutions with trade-offs analyzed
- ✅ You document decisions with clear rationale (not just "we decided X")
- ✅ You get validation from other auditors before merging major changes

**Common Advanced Mistakes:**
- ❌ Solo architecture decisions (always get Nova validation for symmetry)
- ❌ No trade-off analysis ("just do X" → what are costs/benefits?)
- ❌ Insufficient documentation (future readers can't understand why decision made)
- ❌ Not updating Future_Expansion.md (roadmap drifts from reality)

---

### **Skill 11: Leading Complex Workstreams (60 min)**

**What You'll Learn:**
- How to scope multi-phase work (Tier 1/2/3 breakdown)
- How to delegate to multiple auditors (Claude, Nova, Grok, Process)
- How to track progress across sessions

**Action Steps:**
1. Study workstream example:
   - [B-STORM_5.md](../../auditors/relay/B-STORM_5.md) (Future Expansion cleanup)
   - Notice scope breakdown: Tier 1 (Costume + Observatory), Tier 2 Light (Destroyer + Training + Workshop + Showcase)
   - Observe Nova validation checkpoints (Entry 2, 4, 6)
2. Practice scoping work:
   - Identify large task (e.g., "Complete all 66 worldview comparisons")
   - Break into phases (e.g., "Pilot 1 comparison → Scale to 12 → Complete remaining 53")
   - Estimate time per phase (e.g., "Pilot: 5 days, Scale: 3 months, Complete: 1 year")
   - Identify dependencies (e.g., "Pilot must succeed before scaling")
3. Practice delegation:
   - Assign owners (e.g., "Claude: PRO-CT scoring, Grok: ANTI-CT scoring, Nova: convergence checks")
   - Define deliverables (e.g., "Claude delivers self-reported scores by Friday")
   - Set checkpoints (e.g., "Nova validates after Round 2 deliberation")
4. Track progress:
   - Update Future_Expansion.md (rooms dusty → clean)
   - Update Awaiting Block (open KDs → recently completed)
   - Document in REPO_LOG (weekly progress snapshots)

**You'll Know You Understand When:**
- ✅ You can scope work into phases (Tier 1/2/3 or Pilot/Scale/Complete)
- ✅ You can delegate with clear owners and deliverables
- ✅ You track progress systematically (not ad-hoc status checks)
- ✅ You celebrate milestones (Phase complete, pilot success, etc.)

**Common Advanced Mistakes:**
- ❌ No phasing (trying to do everything at once → overwhelm)
- ❌ Vague delegation ("someone should do X" → who? by when?)
- ❌ No checkpoints (work progresses invisibly, surprises at end)
- ❌ Not celebrating wins (demoralizing for collaborators)

---

### **✅ Advanced Checkpoint**

**You've mastered CFA expertise when:**

- [ ] **I can collaborate:** I work effectively in B-STORM relay sessions (1 entry per Click)
- [ ] **I can score worldviews:** I understand adversarial pairing and convergence thresholds
- [ ] **I can propose architecture:** I identify gaps, propose solutions, analyze trade-offs
- [ ] **I can lead workstreams:** I scope, delegate, and track complex multi-phase work
- [ ] **I document everything:** My work leaves clear breadcrumbs for future contributors

**If all 5 are checked, congratulations - you're a CFA expert!** 🎓

**Next Steps:**
- Lead a B-STORM session (propose new features, architecture improvements)
- Mentor new contributors (help others through Beginner/Intermediate paths)
- Contribute to worldview scoring (join CT↔MdN pilot or future comparisons)

---

## Skill Checkpoints

### **How to Know You're Ready for Next Level**

**Beginner → Intermediate:**
- ✅ You can navigate repo in <30 seconds per file
- ✅ You understand semantic headers (FILE, PURPOSE, DEPENDS_ON)
- ✅ You know who the auditors are and what they do
- ✅ You've read at least one complete profile (e.g., CLASSICAL_THEISM.md)

**Intermediate → Advanced:**
- ✅ You've created at least one documentation entry (B-STORM, REPO_LOG, or task)
- ✅ Your entry scores 90+ on appropriate rubric
- ✅ You've successfully committed work with git (verified with git status)
- ✅ You understand quality standards (read exemplars + bad_vs_good comparisons)

**Advanced → Expert:**
- ✅ You've participated in at least one B-STORM relay session (multiple Clicks)
- ✅ You've scored a worldview comparison (7 metrics with evidence)
- ✅ You've proposed and implemented an architecture improvement
- ✅ You've led a multi-phase workstream (Tier 1/2/3 or Pilot/Scale/Complete)

---

## Common Mistakes (Anti-Patterns by Skill Level)

### **Beginner Mistakes**

**1. Not Reading WAYFINDING_GUIDE.md**
- **Why it happens:** "I'll just explore the repo"
- **Why it's a problem:** You wander lost for 30 minutes
- **Fix:** Spend 5 minutes reading [WAYFINDING_GUIDE.md](../WAYFINDING_GUIDE.md) first

**2. Ignoring Semantic Headers**
- **Why it happens:** "Headers are just metadata"
- **Why it's a problem:** You miss FILE, PURPOSE, DEPENDS_ON (context clues)
- **Fix:** Always read first 10-15 lines of any file

**3. Confusing Steel-Man with Advocacy**
- **Why it happens:** "This profile says X is true"
- **Why it's a problem:** Profiles present strongest version, not objective truth
- **Fix:** Remember: steel-man = "here's the best case for X", not "X is correct"

---

### **Intermediate Mistakes**

**4. Skipping Rubrics**
- **Why it happens:** "I'll just write and see how it goes"
- **Why it's a problem:** Quality is inconsistent, no objective measure
- **Fix:** Use [QUALITY_RUBRICS.md](../../examples/excellence/QUALITY_RUBRICS.md) to self-score (aim for 90+)

**5. Vague Titles**
- **Why it happens:** "Updates" or "Progress" seem descriptive
- **Why it's a problem:** Future readers can't scan entries quickly
- **Fix:** Use action verbs + em dash (e.g., "C4 Costume Room Complete — Tier 1 Validated")

**6. No Cross-References**
- **Why it happens:** "I know the context, that's enough"
- **Why it's a problem:** Future readers (or your future self!) have no breadcrumbs
- **Fix:** Add "Files Modified" and "Cross-References" sections to every entry

**7. `git add .` Without Checking**
- **Why it happens:** "Staging all files is faster"
- **Why it's a problem:** You commit unintended files (temp files, drafts)
- **Fix:** Use `git add path/to/specific/file.md` or `git add -p` for selective staging

---

### **Advanced Mistakes**

**8. Multiple Entries Per Click**
- **Why it happens:** "I have more to say after Nova's response"
- **Why it's a problem:** Breaks 1-entry-per-auditor-per-Click pattern
- **Fix:** Wait for next Click. If urgent, ask user to start new Click early.

**9. Forgetting Awaiting Block Updates**
- **Why it happens:** "I'll update it later"
- **Why it's a problem:** KG/KD tracking becomes stale, others don't know what's open
- **Fix:** Update Awaiting Block every time you open/close a KG or KD

**10. Declaring Crux Too Early**
- **Why it happens:** "We disagree on this score, must be a Crux"
- **Why it's a problem:** Premature Crux declarations (try 3 rounds first!)
- **Fix:** Follow VUDU Step 9 protocol - only declare after 3 deliberation rounds

**11. Solo Architecture Decisions**
- **Why it happens:** "I see the solution, let's just do it"
- **Why it's a problem:** Missing symmetry concerns (Nova's role)
- **Fix:** Always get Nova validation before merging major architecture changes

**12. No Trade-Off Analysis**
- **Why it happens:** "This solution is obviously better"
- **Why it's a problem:** Every choice has costs - document them
- **Fix:** Add "Trade-Offs" section to architecture proposals (benefits vs costs)

---

## FAQ

### **Q1: How long does each path take?**

- **Beginner:** 15 minutes (orientation + navigation + first read)
- **Intermediate:** 1-2 hours (quality standards + first entry + commit)
- **Advanced:** 3-5 hours (multi-auditor collab + scoring + architecture decisions)

**Total to Expert:** ~5-7 hours over multiple sessions

---

### **Q2: Can I skip levels?**

**Short answer:** No, but you can move quickly through early levels if you already have the skills.

**Why levels matter:**
- **Beginner** establishes navigation (you can't contribute if you can't find files)
- **Intermediate** establishes quality standards (you can't write good docs without rubrics)
- **Advanced** establishes collaboration patterns (you can't lead if you don't know relay workflow)

**How to accelerate:**
- Complete checkpoints faster (if you already know git, Skill 6 takes 5 min not 20)
- Read exemplars at 2x speed (scan structure, don't read every word)
- Ask for checkpoint validation (demonstrate competency, skip redundant practice)

---

### **Q3: What if I get stuck?**

**1. Check the resources:**
- [WAYFINDING_GUIDE.md](../WAYFINDING_GUIDE.md) (navigation)
- [QUALITY_RUBRICS.md](../../examples/excellence/QUALITY_RUBRICS.md) (scoring criteria)
- [examples/excellence/](../../examples/excellence/) (templates + comparisons)

**2. Search the repo:**
- Use Ctrl+Shift+F (or Cmd+Shift+F) to find keywords
- Search for error messages, file names, concepts

**3. Read related sessions:**
- [B-STORM_4.md](../../auditors/relay/B-STORM_4.md) (pilot prep example)
- [B-STORM_5.md](../../auditors/relay/B-STORM_5.md) (expansion work example)

**4. Ask in B-STORM session:**
- Open a KG (Knowledge Gap) in Awaiting Block
- Request clarification from Nova or Process Claude

---

### **Q4: How do I know if my work is good enough?**

**Use the rubrics:**
- Score your own work (0-100 scale, 5 categories × 20 points)
- Target: 90+ (Excellent)
- Acceptable: 80-89 (Very Good)
- Below 80: Revise before submitting

**Compare to exemplars:**
- Does your entry look like [GOOD_B-STORM_ENTRY_EXAMPLE.md](../../examples/excellence/GOOD_B-STORM_ENTRY_EXAMPLE.md)?
- Read bad_vs_good comparisons - is your work closer to "good" column?

**Get peer review:**
- Ask Nova to validate (Entry 2, 4, 6 pattern)
- Request feedback from other auditors
- Check for symmetry concerns

---

### **Q5: What's the difference between KG and KD?**

**KG (Knowledge Gap):**
- A question that needs answering
- Example: "How do we handle <98% convergence?"
- Resolution: Provide answer + evidence
- Closed when: Question answered, documented

**KD (Key Decision):**
- A choice that needs making
- Example: "Should we execute Tier 2 Light now or defer?"
- Resolution: Decision made + rationale documented
- Closed when: Decision recorded in Awaiting Block or REPO_LOG

**Both tracked in Awaiting Block:**
- Open KGs/KDs: Currently unresolved
- Recently Completed: Closed in last 1-2 Clicks

---

### **Q6: When should I create a new B-STORM session?**

**Start new B-STORM when:**
- Previous session marked COMPLETE
- New major workstream begins (e.g., CT↔MdN pilot after expansion work)
- User explicitly requests new session
- Previous session exceeds 2,000 lines (archive old, start fresh)

**Continue existing B-STORM when:**
- Work is still in progress (open KGs/KDs)
- Related to current session focus
- < 2,000 lines total

---

### **Q7: How do I know which auditor I am?**

**Check your assignment:**
- [auditors/AUDITOR_ASSIGNMENTS.md](../../auditors/AUDITOR_ASSIGNMENTS.md) lists roles
- **Claude:** Primary implementation, PRO-CT scoring
- **Nova:** Symmetry validation, fairness checks
- **Grok:** Empirical lens, ANTI-CT scoring
- **Process Claude:** Repository health, Domain 7 orchestration

**In B-STORM relay:**
- Odd entries (1, 3, 5...): Claude
- Even entries (2, 4, 6...): Nova
- Entry number = (Auditor index - 1) × 2 + Click number

---

### **Q8: What if I disagree with an architecture decision?**

**Follow the process:**
1. **Document concern:** Open KG in Awaiting Block ("Why did we choose X over Y?")
2. **Provide evidence:** Link to specific issues, trade-offs not considered
3. **Propose alternative:** Suggest solution with trade-off analysis
4. **Get validation:** Nova checks for symmetry, Process Claude for scalability
5. **Decide:** User (Ziggy) makes final call if auditors don't converge

**Never:**
- Revert decisions without discussion
- Make solo changes to major architecture
- Skip validation (always get Nova approval)

---

### **Q9: How often should I update the Awaiting Block?**

**Update when:**
- Opening new KG/KD (immediately)
- Closing KG/KD (as soon as resolved)
- Starting new Click (add "Last Updated" timestamp)
- Nova requests update (Entry 2, 4, 6 validation)

**Keep it fresh:**
- Awaiting Block should reflect current state (not historical)
- Move closed items to "Recently Completed" (don't delete - preserve for 1-2 Clicks)
- Archive very old completed items to REPO_LOG

---

### **Q10: What's the most important skill to master?**

**Foundation:** Navigation + semantic headers (Beginner Skill 2)
- If you can't find files, nothing else matters

**Intermediate:** Quality rubrics (Intermediate Skill 4)
- Objective standards prevent "good enough" drift

**Advanced:** Cross-auditor collaboration (Advanced Skill 8)
- CFA is a team effort - solo work is limited impact

**Expert:** Architecture thinking (Advanced Skill 10)
- Identifying gaps and proposing solutions scales the project

---

## Next Steps

**After Training Grounds:**

1. **Apply Your Skills:**
   - Join a B-STORM session (check [auditors/relay/](../../auditors/relay/) for active sessions)
   - Score a worldview comparison (see [profiles/comparisons/](../../profiles/comparisons/))
   - Propose an improvement (architecture gaps, process optimizations)

2. **Mentor Others:**
   - Help new contributors through Beginner Path
   - Review entries using rubrics (provide specific feedback)
   - Share lessons learned (what mistakes did you make? how did you fix them?)

3. **Expand the Training Grounds:**
   - Add new skill paths (Scoring Path, Architecture Path, etc.)
   - Contribute more anti-patterns (common mistakes you discovered)
   - Update checkpoints (as repository evolves)

---

**Cross-Link from WAYFINDING_GUIDE.md:**

This document is referenced in [WAYFINDING_GUIDE.md](../WAYFINDING_GUIDE.md) section "For New Contributors" as the official skill path resource.

---

**Created by:** C4 (B-STORM_5 Click 4 - Tier 2 Light)
**Date:** 2025-11-11
**Purpose:** Establish progressive skill paths for CFA contributors (Beginner → Intermediate → Advanced → Expert)
**Status:** Active (ready for new contributors)
**Maintenance:** Update quarterly with new anti-patterns, FAQ entries, and skill refinements

**The Training Grounds: Where contributors grow from orientation to expertise.** 🎓
