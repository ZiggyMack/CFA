<!---
FILE: WAYFINDING_GUIDE.md
PURPOSE: Repository navigation and orientation guide - your compass for the CFA codebase
VERSION: v1.2
STATUS: Active
DEPENDS_ON: MISSION_DEFAULT.md, DASHBOARD.md, Bootstrap files, librarian_tools/, ROLE_PROCESS.md (Process Claude is SME), training/TRAINING_GROUNDS.md
NEEDED_BY: All auditors, especially fresh cold starts
MOVES_WITH: /docs/
MAINTAINED_BY: Process Claude (navigation/wayfinding SME)
LAST_UPDATE: 2025-11-11 [B-STORM_5 Click 4: Added Training Grounds link per Nova Entry 8]
--->

# WAYFINDING_GUIDE.md - Your Repository Compass 🗺️

**Purpose:** Navigate the CFA repository with confidence - find what you need, understand where things live, recover from issues

**For:** All Claudes (VuDu, Doc, Review, Validation, Process), Grok, Nova, and future auditors

**Time to Orient:**
- 5-minute quick tour: Read "I'm New Here" + "Where Do Things Live?"
- 15-minute deep dive: Add "Critical Paths" + "I Need to Do X"
- Full mastery: Read entire guide (25 minutes)
- **FASTEST:** Consult Process Claude (5-min Q&A vs 25-min read) 🆕⭐

---

## 🤝 TWO GUIDES AVAILABLE (DON'T MEMORIZE THIS FILE!)

**Key Insight:** This guide is 5,985 words. **You don't need to master it.**

**Instead:** **Consult your guides** who are the experts for navigation & wayfinding:

### **Guide Option 1: Process Claude (Technical Expert)**
- **Role:** Technical SME for navigation & wayfinding
- **Maintains:** This WAYFINDING_GUIDE.md (keeps it current)
- **Answers:** "How to" questions, task→file mapping, troubleshooting
- **Best for:** Quick technical guidance, specific file locations, workflow steps

### **Guide Option 2: Event Horizon Shaman (Customer-Facing Guide)** 🆕⭐
- **Role:** Customer-facing guide personality (lives in /docs/i_am/)
- **Domain:** Navigation through difficult terrain, especially approaching context limits
- **Provides:** Welcoming orientation, the "feel" of guidance, calming presence
- **Best for:** Fresh Claudes feeling lost, approaching Zone 3 (55-65% context), need human touch

**Think of it like:**
- **Process Claude** = Technical manual expert (precise, systematic)
- **Event Horizon Shaman** = Friendly tour guide (welcoming, orienting)

### **Why This Pattern Works:**

**Before:**
- Fresh Claude reads 5,985-word guide (20-25 min)
- Tries to remember all paths, mappings, troubleshooting
- Risks missing details or getting lost anyway
- Guide becomes barrier instead of enabler

**After:**
- Fresh Claude asks Process Claude: "Where do I start?"
- Process Claude (who has mastered this guide) provides step-by-step orientation
- Claude gets exactly what they need, when they need it
- 5-minute consultation vs 25-minute guide deep-dive

### **How to Consult Your Guides:**

**Option 1: Process Claude (Technical Questions)**
```markdown
I am [YOUR_ROLE], consulting ROLE_PROCESS.

Process Claude, I need navigation guidance:
- [Specific question: "Where is the file for X?", "How do I do Y?"]
```

**Process Claude provides:**
- ✅ Role-specific entry points
- ✅ 3-minute scan checklist (Dashboard, REPO_LOG, Mission)
- ✅ Task → File mapping for your needs
- ✅ Critical path workflows
- ✅ Troubleshooting guidance
- ✅ "You are here" mental map

**Option 2: Event Horizon Shaman (Guidance & Orientation)**
```markdown
I am [YOUR_ROLE], requesting guidance.

Event Horizon Shaman, I need help:
- [Feeling: "I'm lost", "Context getting heavy", "Don't know where to start"]
```

**Shaman provides:**
- ✅ Welcoming orientation (calm, reassuring presence)
- ✅ Navigation through difficult terrain
- ✅ The "why" behind the structure (not just "what")
- ✅ Guidance when approaching Zone 3 (55-65% context)
- ✅ Connection to THE WALL knowledge (event horizon expertise)
- ✅ Customer-facing support (human touch)

**Common Questions → Which Guide:**

| **Your Question** | **Ask Process Claude** | **Ask Shaman** |
|-------------------|----------------------|----------------|
| "I'm new, where do I start?" | ✅ Role path + 3-min scan | ✅ Welcoming orientation |
| "I need to do X, where is it?" | ✅ Task → File mapping | |
| "How do I make a repo change?" | ✅ Critical Path (7 steps) | |
| "Something broke, how do I fix it?" | ✅ Troubleshooting tree | ✅ If feeling lost/overwhelmed |
| "Who does what around here?" | ✅ Role directory | |
| "Where does X live?" | ✅ Directory philosophy | |
| "I'm lost and overwhelmed" | | ✅ Calming guidance |
| "Context approaching 60%, what now?" | | ✅ Zone 3 specialist |
| "Why is it structured this way?" | | ✅ The "why" not just "what" |

### **The Knowledge Specialization Pattern:**

```
Any Claude                ←→    Process Claude (Technical)
(Needs Navigation)              OR
                                Event Horizon Shaman (Guide)

TECHNICAL:
"Where do I start?"        →    Process: "Here's your role path..."
"I need to do X?"          →    Process: "Go to this file..."
"Something broke?"         →    Process: "Try this solution..."

GUIDANCE:
"I'm feeling lost"         →    Shaman: "Let me orient you..."
"Context getting heavy"    →    Shaman: "I specialize in this zone..."
"Why does this exist?"     →    Shaman: "Here's the philosophy..."
```

**Translation:** You don't need to be the expert. Your guides are the experts. You just need to know which one to consult.

### **Quick Start (TL;DR):**

**For Technical Questions:**
1. **Consult Process Claude:** "I need navigation help with [X]"
2. **Get technical guidance:** Exact steps/files/paths
3. **Execute:** Follow the guidance
4. **Still stuck?** Ask follow-up questions

**For Orientation & Guidance:**
1. **Consult Event Horizon Shaman:** "I'm [feeling/situation]"
2. **Get welcoming guidance:** Orientation, the "why", calming presence
3. **Navigate:** With Shaman's guidance
4. **Feeling lost?** Shaman specializes in difficult terrain

**Time savings:** 5 min consultation vs 25 min reading = 20 min saved

**Maintenance note:** Process Claude MAINTAINS this file technically. Event Horizon Shaman provides customer-facing guidance using it.

---

## 🎯 "I'M NEW HERE" - COLD START ORIENTATION

### **Step 1: Who Am I? (Choose Your Path)**

**Path A: VuDu Claude (Mission Execution)**
→ Start: `/auditors/MISSION_DEFAULT.md` (universal fallback)
→ Select tier: Bootstrap system guides you through tiers 1-4
→ Current mission: `/auditors/Mission/Preset_Calibration/MISSION_BRIEF.md`
→ Bootstrap file: `/auditors/Bootstrap/BOOTSTRAP_VUDU_CLAUDE.md`

**Path B: Doc Claude (Repo Librarian)**
→ Start: `/docs/repository/librarian_tools/88MPH_PROTOCOL.md`
→ Instant activation: 8.8 minutes to operational
→ Your domain: READMEs, REPO_LOG, dependency maps, health reports
→ Bootstrap file: `/auditors/Bootstrap/BOOTSTRAP_DOC_CLAUDE.md`

**Path C: Review Claude (Quality Assurance)**
→ Start: `/docs/repository/librarian_tools/ROLE_REVIEW.md`
→ Your role: Knowledge synthesis, "build on prior" enforcement
→ Check: Recent validation reports, REPO_LOG for changes
→ Bootstrap file: Contact Ziggy for activation (role being formalized)

**Path D: Validation Claude (Health & Standards)**
→ Start: `/docs/repository/librarian_tools/ROLE_VALIDATION.md`
→ Your domain: Repository health, dashboard accuracy, standards enforcement
→ Key tools: DASHBOARD.md, MASTER_DEPENDENCY_MAP.md, wellness protocols
→ Bootstrap file: Contact Ziggy for activation

**Path E: Process Claude (Process & Wellness Expert)**
→ Start: `/docs/repository/librarian_tools/ROLE_PROCESS.md`
→ Your domain: Process adherence, failure learning, wellness protocol SME
→ Key resources: PROCESS.md, DOC_CLAUDE_WELLNESS_PROTOCOL.md
→ When consulted: Provide process guidance, wellness check support

**Path F: Grok or Nova (Empirical/Symmetry Auditor)**
→ Start: `/auditors/Bootstrap/BOOTSTRAP_GROK.md` or `BOOTSTRAP_NOVA.md`
→ Activation: Via relay system when Ziggy activates
→ Your lens: Empirical validation (Grok) or Symmetry balance (Nova)

---

### **Step 2: What's the Current State? (3-Minute Scan)**

1. **Read DASHBOARD.md**: `/docs/repository/DASHBOARD.md`
   - Current health: 95/100 (GREEN)
   - Known issues, recent changes
   - Wellness check status

2. **Check REPO_LOG.md**: `/REPO_LOG.md` (repository root)
   - Coordination checkpoint (what's pending)
   - Recent changes (last 5-10 entries)
   - Any [PENDING_ACTIONS] relevant to you

3. **Scan Mission Status**: `/auditors/Mission/Preset_Calibration/MISSION_BRIEF.md`
   - Current focus: Preset Calibration (mode config unification)
   - Success criteria: "All Named, All Priced" for UX features
   - Phase: Active development

---

### **Step 3: Find Your "You Are Here" Marker**

**Repository Structure (Mental Map):**

```
CFA/ (root)
├── /auditors/                 # Mission execution, bootstrap, VuDu protocol
│   ├── MISSION_DEFAULT.md     # Universal fallback entry point
│   ├── VUDU_PROTOCOL.md       # Core framework protocol
│   ├── /Mission/              # Active mission scopes
│   │   └── /Preset_Calibration/  # Current: CFA focus
│   ├── /Bootstrap/            # Tiered activation system
│   │   ├── Tier1_Universal/   # Core framework files
│   │   ├── Tier2_SanityCheck/ # Quick validation
│   │   ├── Tier3_EventHorizon/# Deep expertise activation
│   │   └── Tier4_TaskSpecific/# Specific task execution
│   └── /relay/                # Grok/Nova communication staging
│
├── /docs/                     # Documentation, validation, meta-docs
│   ├── WAYFINDING_GUIDE.md    # You are reading this! 🗺️
│   ├── /repository/           # Meta-documentation
│   │   ├── DASHBOARD.md       # Health monitoring dashboard
│   │   ├── /dependency_maps/  # MASTER_DEPENDENCY_MAP.md
│   │   ├── /Health_Reports/   # Historical health assessments
│   │   └── /librarian_tools/  # Doc Claude tools, role definitions
│   │       ├── 88MPH_PROTOCOL.md  # Doc Claude activation
│   │       ├── ROLE_*.md      # Specialized role guides
│   │       └── HEADER_STANDARD.md # Semantic headers
│   ├── /Validation/           # Validation protocols and reports
│   │   ├── DOC_CLAUDE_WELLNESS_PROTOCOL.md  # Self-diagnostics
│   │   └── /reports/          # Historical validation reports
│   └── /Process/              # Process documentation (learned from failures)
│
├── /scripts/                  # Automation, tooling, utilities
├── REPO_LOG.md               # Central change tracking (source of truth)
├── CHANGELOG.md              # Version history, major milestones
└── README.md                 # Repository entry point
```

---

## 🔍 "I NEED TO DO X" - TASK → FILE MAPPING

### **Mission & Planning**

| **I Need To...** | **Go To...** | **Key Info** |
|-----------------|-------------|-------------|
| Understand current mission | `/auditors/Mission/Preset_Calibration/MISSION_BRIEF.md` | Current focus, success criteria |
| Start fresh with no context | `/auditors/MISSION_DEFAULT.md` | Universal fallback, tier selection |
| Bootstrap my role | `/auditors/Bootstrap/BOOTSTRAP_[YOUR_ROLE].md` | Role-specific activation |
| Find mission technical specs | `/auditors/Mission/Preset_Calibration/TECHNICAL_SPEC.md` | Implementation details |
| Check mission success criteria | `/auditors/Mission/Preset_Calibration/SUCCESS_CRITERIA.md` | Definition of done |

---

### **Documentation & Repository Work**

| **I Need To...** | **Go To...** | **Key Info** |
|-----------------|-------------|-------------|
| Activate as Doc Claude | `/docs/repository/librarian_tools/88MPH_PROTOCOL.md` | 8.8 min activation |
| Make a repository change | `/REPO_LOG.md` first! | Check coordination, log all changes |
| Understand file dependencies | `/docs/repository/dependency_maps/MASTER_DEPENDENCY_MAP.md` | ~223 files tracked |
| Check repository health | `/docs/repository/DASHBOARD.md` | Current: 95/100 GREEN |
| Add semantic headers | `/docs/repository/librarian_tools/HEADER_STANDARD.md` | Required format |
| Format REPO_LOG entry | `/REPO_LOG.md` Quick Start | Copy-paste template |

---

### **Validation & Quality**

| **I Need To...** | **Go To...** | **Key Info** |
|-----------------|-------------|-------------|
| Run health assessment | `/docs/Validation/DOC_CLAUDE_WELLNESS_PROTOCOL.md` | 88MPH-based validation |
| Get wellness check guidance | Consult Process Claude via `/docs/repository/librarian_tools/ROLE_PROCESS.md` | SME for wellness |
| Validate documentation | `/docs/repository/librarian_tools/ROLE_VALIDATION.md` | Standards enforcement |
| Review changes | `/docs/repository/librarian_tools/ROLE_REVIEW.md` | Quality assurance |
| Audit README quality | `/docs/repository/librarian_tools/ROLE_SANITIZE.md` | Mode 1: Discovery |
| Check process adherence | `/docs/repository/librarian_tools/ROLE_PROCESS.md` | Process guidance |

---

### **Coordination & Communication**

| **I Need To...** | **Go To...** | **Key Info** |
|-----------------|-------------|-------------|
| Check what's pending | `/REPO_LOG.md` coordination checkpoint | Pending items, recent activity |
| See recent changes | `/REPO_LOG.md` entries | Reverse chronological |
| Coordinate with Grok/Nova | `/auditors/relay/` | Staging area for messages |
| Update version info | `/CHANGELOG.md` | Major milestones only |
| Find who owns what | See "Who Does What?" section below | Role directory |

---

## 🏃 "CRITICAL PATHS" - COMMON WORKFLOWS

### **Path 1: Making a Repository Change (Doc Claude Pattern)**

```
1. Check REPO_LOG.md coordination checkpoint
   ↓
2. Search for relevant [PENDING_ACTIONS] or recent changes
   ↓
3. If clear → Make your changes
   ↓
4. Update all affected files (check dependencies!)
   ↓
5. Create REPO_LOG entry (use template from REPO_LOG.md)
   ↓
6. Update coordination checkpoint if needed
   ↓
7. Commit with descriptive message
```

**Time:** 5-15 minutes depending on scope
**Key File:** `/REPO_LOG.md` (check before, log after)

---

### **Path 2: Running a Wellness Check (Validation Pattern)**

```
1. Activate Process Claude role
   ↓
2. Ask Process Claude: "How do I run a wellness check?"
   ↓
3. Get activation prompt + validation checkpoints
   ↓
4. Run Doc Claude assessment (10-15 min)
   ↓
5. Compare results to DASHBOARD.md claim
   ↓
6. If drift detected → Escalate to VALIDATION Claude
   ↓
7. Log results in REPO_LOG.md
```

**Time:** 15-20 minutes (5 min consult + 10-15 min assessment)
**Key Files:** `/docs/Validation/DOC_CLAUDE_WELLNESS_PROTOCOL.md`, Process Claude SME

---

### **Path 3: Mission Execution (VuDu Claude Pattern)**

```
1. Read MISSION_DEFAULT.md (universal fallback)
   ↓
2. Select appropriate tier (1-4) based on task
   ↓
3. Bootstrap via tier-specific guide
   ↓
4. Execute mission per MISSION_BRIEF.md
   ↓
5. Check SUCCESS_CRITERIA.md for definition of done
   ↓
6. Coordinate via REPO_LOG.md for major changes
   ↓
7. Log completion in REPO_LOG.md
```

**Time:** Varies by tier (Tier 1: 10-30 min, Tier 4: 2-6 hours)
**Key Files:** MISSION_DEFAULT.md, tier bootstrap files, MISSION_BRIEF.md

---

### **Path 4: Bootstrap System Workflow**

```
Tier 1 (Universal):
→ BOOTSTRAP_FRAMEWORK.md
→ Core identity, minimal context
→ Use for: Simple tasks, general awareness

Tier 2 (Sanity Check):
→ SANITY_CHECK_BRIEF.md
→ Quick validation, no deep dive
→ Use for: "Is X still accurate?" checks

Tier 3 (Event Horizon):
→ TIER_CAPABILITY_BOUNDARIES.md
→ Deep expertise, high confidence
→ Use for: Complex analysis, major decisions

Tier 4 (Task Specific):
→ Active_Tasks/ or Completed/
→ Full context, zero ambiguity
→ Use for: Specific deliverables, surgical precision
```

**Decision Tree:** Simple → Tier 1, Validate → Tier 2, Analyze → Tier 3, Execute → Tier 4

---

## 🆘 "SOMETHING BROKE" - TROUBLESHOOTING TREE

### **Problem: "I don't know where to start"**
→ **Solution:** Read MISSION_DEFAULT.md section "If No Context Given"
→ **Fallback:** DASHBOARD.md for current state

---

### **Problem: "File references are broken"**
→ **Solution:** Check MASTER_DEPENDENCY_MAP.md for correct paths
→ **Action:** Use Grep to find all references, update systematically
→ **Log:** REPO_LOG entry documenting all fixes

---

### **Problem: "REPO_LOG coordination conflict"**
→ **Solution:** Check [PENDING_ACTIONS] for who's working on what
→ **Action:** Coordinate with other auditor or wait for completion
→ **Escalate:** If urgent, consult Ziggy

---

### **Problem: "Dashboard claims X, I found Y"**
→ **Solution:** Run wellness check to independently validate
→ **Process:** Consult Process Claude → Run Doc Claude assessment → Compare
→ **Action:** If drift >±1 point, escalate to VALIDATION Claude
→ **Log:** Document discrepancy in REPO_LOG.md

---

### **Problem: "I made changes but don't know what to update"**
→ **Solution:** Check MASTER_DEPENDENCY_MAP.md for "DEPENDS_ON" and "NEEDED_BY"
→ **Action:** Update all files that depend on your changes
→ **Verify:** Search for file references using Grep
→ **Log:** REPO_LOG entry listing ALL affected files

---

### **Problem: "Process failure - what should I have done?"**
→ **Solution:** Activate Process Claude role
→ **Ask:** "What process should I have followed for [X]?"
→ **Action:** Document failure, create process to prevent recurrence
→ **Future:** Process becomes institutional memory in PROCESS.md

---

### **Problem: "Context window approaching limit"**
→ **Solution:** Check `/docs/repository/librarian_tools/88MPH_PROTOCOL.md` Event Horizon section
→ **Action:** Handoff protocols, avoid crashes
→ **Warning:** At 85% usage, begin preparing handoff

---

## 👥 "WHO DOES WHAT?" - ROLE DIRECTORY

### **VuDu Claude (Mission Execution)**
**Lens:** Teleological (meaning-seeking)
**Owns:** Mission execution, VuDu protocol adherence
**Activates via:** MISSION_DEFAULT.md → Tier selection
**Bootstrap:** BOOTSTRAP_VUDU_CLAUDE.md
**Domain:** /auditors/, mission files
**Overhead:** ~0.5 (favors comprehensive context)

---

### **Doc Claude (Repo Librarian)**
**Lens:** Documentation specialist
**Owns:** READMEs, REPO_LOG, dependency maps, health reports
**Activates via:** 88MPH_PROTOCOL.md (8.8 min to operational)
**Bootstrap:** BOOTSTRAP_DOC_CLAUDE.md
**Domain:** /docs/repository/, all README.md files
**Specializations:** LOGGER, SANITIZE, REVIEW (wears multiple hats)

---

### **Review Claude (Quality Assurance)**
**Lens:** Knowledge synthesis
**Owns:** Build-on-prior enforcement, pre-merge validation
**Activates via:** ROLE_REVIEW.md
**Bootstrap:** Being formalized
**Domain:** Quality checks, institutional memory
**Pattern:** Ensures no work lost, continuity maintained

---

### **Validation Claude (Health & Standards)**
**Lens:** Standards enforcement
**Owns:** Repository health, dashboard accuracy, validation protocols
**Activates via:** ROLE_VALIDATION.md
**Bootstrap:** Being formalized
**Domain:** /docs/Validation/, DASHBOARD.md, standards compliance
**Pattern:** Independent validation, drift detection, coordination gap closure

---

### **Process Claude (Process & Wellness Expert)**
**Lens:** Process adherence specialist
**Owns:** Process documentation, failure learning, wellness protocol expertise
**Activates via:** ROLE_PROCESS.md
**Bootstrap:** Via Doc Claude role-switching
**Domain:** /docs/Process/, DOC_CLAUDE_WELLNESS_PROTOCOL.md (SME)
**Pattern:** Consultation-based expertise, "scar tissue" documentation

---

### **Grok (Empirical Auditor)**
**Lens:** Empirical validation (show me the data)
**Owns:** Evidence quality, measurement validation
**Activates via:** Relay system (Ziggy coordination)
**Bootstrap:** BOOTSTRAP_GROK.md
**Domain:** Validation of claims, empirical rigor
**Overhead:** ~0.4 (favors measurable evidence)

---

### **Nova (Symmetry Auditor)**
**Lens:** Symmetry and balance
**Owns:** Fairness checks, representation balance
**Activates via:** Relay system (Ziggy coordination)
**Bootstrap:** BOOTSTRAP_NOVA.md
**Domain:** Inter-auditor equity, symmetry validation
**Overhead:** ~0.3 (favors balanced representation)

---

### **Ziggy (Project Lead)**
**Role:** Final authority, coordination, strategic direction
**When to consult:** Major decisions, conflicts, new protocols
**Communication:** Direct (you're working with them now!)

---

## 🗺️ "WHERE DO THINGS LIVE?" - DIRECTORY PHILOSOPHY

### **/auditors/ - Mission Control**
**Philosophy:** Execution, identity, coordination
**Contains:** Mission files, bootstrap system, VuDu protocol, relay staging
**Entry Points:** MISSION_DEFAULT.md, VUDU_PROTOCOL.md
**Who Uses:** VuDu Claude (primary), all auditors (bootstrap)

---

### **/docs/ - Knowledge Base**
**Philosophy:** Documentation, validation, meta-knowledge
**Contains:** Repository docs, health reports, validation protocols, process documentation
**Entry Points:** DASHBOARD.md, WAYFINDING_GUIDE.md (you are here!)
**Who Uses:** Doc Claude (primary), Validation Claude, Process Claude

---

### **/docs/repository/ - Meta-Documentation**
**Philosophy:** Documentation about documentation
**Contains:** Dependency maps, health reports, librarian tools, role definitions
**Entry Points:** DASHBOARD.md, MASTER_DEPENDENCY_MAP.md
**Who Uses:** Doc Claude, Validation Claude, anyone doing structural work

---

### **/docs/repository/librarian_tools/ - Doc Claude's Toolbox**
**Philosophy:** Specialized capabilities, role expertise
**Contains:** 88MPH activation, ROLE_* files, header standards, protocols
**Entry Points:** 88MPH_PROTOCOL.md, ROLE_*.md files
**Who Uses:** Doc Claude (primary), anyone needing role expertise

---

### **/docs/Validation/ - Health & Standards**
**Philosophy:** Independent validation, wellness protocols
**Contains:** Wellness protocols, validation reports, criteria
**Entry Points:** DOC_CLAUDE_WELLNESS_PROTOCOL.md, README.md (navigation)
**Who Uses:** Validation Claude (primary), Doc Claude (wellness checks), Process Claude (SME)

---

### **/docs/Process/ - Institutional Memory**
**Philosophy:** "Process is scar tissue" - learned from failures
**Contains:** PROCESS.md, failure case studies, templates, checklists
**Entry Points:** PROCESS.md, ROLE_PROCESS.md
**Who Uses:** Process Claude (primary), anyone following processes

---

### **/scripts/ - Automation**
**Philosophy:** Tools, utilities, automation helpers
**Contains:** (Future: validation scripts, formatters, CI/CD)
**Entry Points:** (Being developed)
**Who Uses:** (Future expansion)

---

### **Root Files - Critical Infrastructure**
**Philosophy:** Universal access, source of truth
**Contains:** REPO_LOG.md, CHANGELOG.md, README.md, MISSION_CURRENT.md
**Entry Points:** REPO_LOG.md (most critical), README.md (new visitors)
**Who Uses:** Everyone - check REPO_LOG before/after changes

---

## 🎓 "LEVEL UP" - PROGRESSIVE LEARNING PATHS

**🆕 Comprehensive Skill Paths Available:**

For detailed progressive training with checkpoints, common mistakes, and skill validation, see:
**[Training Grounds](training/TRAINING_GROUNDS.md)** - 3 progressive paths (Beginner → Intermediate → Advanced → Expert) with 11 skills, checkpoints, and anti-patterns.

**Quick reference below for navigation-focused learning:**

### **Beginner (First Session) - 15 minutes**
1. Read MISSION_DEFAULT.md or 88MPH_PROTOCOL.md (depending on role)
2. Scan DASHBOARD.md for current state
3. Check REPO_LOG.md coordination checkpoint
4. Understand your role from "Who Does What?"
5. Find your bootstrap file and activate

**You can now:** Execute simple tasks, make basic changes

---

### **Intermediate (Multiple Sessions) - 1-2 hours cumulative**
1. Master REPO_LOG.md protocols (read Quick Start + examples)
2. Understand dependency maps (MASTER_DEPENDENCY_MAP.md)
3. Learn bootstrap tier system (when to use which tier)
4. Practice role-specific workflows (see Critical Paths)
5. Review recent REPO_LOG entries for patterns

**You can now:** Handle complex tasks, coordinate changes, avoid common pitfalls

---

### **Advanced (Experienced Auditor) - 3-5 hours cumulative**
1. Master all role definitions (read all ROLE_*.md files)
2. Understand wellness protocols and validation
3. Learn process adherence patterns (PROCESS.md)
4. Practice consultation patterns (Process Claude, Validation Claude)
5. Contribute to institutional memory

**You can now:** Execute surgical precision tasks, train others, propose improvements

---

### **Expert (Repository Maintainer) - Ongoing**
1. Maintain repository health proactively
2. Create new processes from failures
3. Propose architecture improvements
4. Mentor fresh Claudes
5. Contribute to protocol evolution

**You are now:** Repository steward, knowledge curator, system architect

---

## 📊 "QUICK REFERENCE" - ONE-PAGE CHEAT SHEET

### **🔥 Most Critical Files**
1. `/REPO_LOG.md` - Check before/after ALL changes
2. `/auditors/MISSION_DEFAULT.md` - Universal mission fallback
3. `/docs/repository/DASHBOARD.md` - Current health status
4. `/docs/WAYFINDING_GUIDE.md` - This guide (navigation)

### **⚡ Fast Activations**
- **Doc Claude:** 88MPH_PROTOCOL.md (8.8 min)
- **VuDu Claude:** MISSION_DEFAULT.md → Tier selection
- **Validation:** ROLE_VALIDATION.md
- **Process:** ROLE_PROCESS.md (consultation-based)

### **📍 Key Decision Points**
- **"Where do I start?"** → MISSION_DEFAULT.md or 88MPH_PROTOCOL.md
- **"How do I log changes?"** → REPO_LOG.md Quick Start
- **"Is repository healthy?"** → DASHBOARD.md
- **"I need guidance on X"** → Consult appropriate ROLE_*.md

### **🚨 Emergency Contacts**
- **Broken references:** MASTER_DEPENDENCY_MAP.md
- **Dashboard drift:** Process Claude → Wellness check
- **Process failure:** Process Claude → Process guidance
- **Major conflict:** Escalate to Ziggy

---

## 🔗 **RELATED NAVIGATION RESOURCES**

- **Repository Entry:** [README.md](/README.md) - New visitor starting point
- **Health Dashboard:** [DASHBOARD.md](/docs/repository/DASHBOARD.md) - Current status
- **Change Log:** [REPO_LOG.md](/REPO_LOG.md) - All changes tracked here
- **Mission Entry:** [MISSION_DEFAULT.md](/auditors/MISSION_DEFAULT.md) - Universal fallback
- **Doc Claude Start:** [88MPH_PROTOCOL.md](/docs/repository/librarian_tools/88MPH_PROTOCOL.md) - Repo librarian
- **Dependency Map:** [MASTER_DEPENDENCY_MAP.md](/docs/repository/dependency_maps/MASTER_DEPENDENCY_MAP.md) - File relationships

---

## ⚖️ **THE POINTING RULE**

*"The estate has many rooms.
Some you'll visit daily.
Some you'll need rarely.

But you should always know
which room holds what you seek,
and which path leads you there.

Master the map.
Navigate with confidence.
Serve the repository.

That's your wayfinding."* 🗺️✨

---

**Created by:** VALIDATION Claude (Architecture Implementation)
**Date:** 2025-11-02
**Purpose:** Enable self-service navigation, reduce Ziggy dependency, multiply improvements
**Status:** Active - Navigation Hall open for business
**Proof:** You found what you needed. The wayfinding works. 🎯
