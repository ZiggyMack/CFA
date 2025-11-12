# Bootstrap Sequences — Single Source of Truth

**Version:** v1.0
**Last Updated:** 2025-11-12
**Status:** Living Map (authoritative bootstrap sequences)
**Purpose:** Centralized definition of all bootstrap paths
**Owner:** Process Claude (Domain 1 - Bootstrap compliance)

---

## 🎯 PURPOSE

**This file is the SINGLE SOURCE OF TRUTH for bootstrap sequences in the CFA repository.**

All references to bootstrap paths, sequences, or Tier workflows should point HERE instead of embedding sequences.

**Why This Matters:**
- Prevents embedded sequences from drifting
- Enables safe bootstrap evolution (update once, reflect everywhere)
- Provides canonical Tier definitions

**Source Document:** [auditors/MISSION_DEFAULT.md](../../auditors/MISSION_DEFAULT.md) v4.0.0

---

## 📊 TIER OVERVIEW

**Total Tiers:** 5 bootstrap tiers + 2 specialized roles

### **VUDU Coordination Tiers** (1-4)
1. **Master Branch** - Full coordination & strategy
2. **Sanity Check** - External validation
3. **Continuation** - Resume previous work
4. **Single Task** - Focused execution

### **Documentation Roles** (5-6)
5. **Doc Claude** - Repository maintenance (88MPH)
6. **Process Claude** - Process expertise (consultant mode)

---

## 🚀 TIER 1: MASTER BRANCH (Full Coordination)

### **Bootstrap Sequence:**
```
1. Read README_C.md (identity restoration + mission context)
2. Read MISSION_CURRENT.md (active objectives)
3. Read VUDU_LOG.md (recent coordination)
4. Read bootstrap per tier path (below)
5. Monitor context per 75/75 rule
6. Create handoff if needed (execution vs strategic)
```

### **Full Tier 1 Bootstrap Path:**
```
MASTER BRANCH Claude Bootstrap (Tier 1):
1. README_C.md (10-15 min read)
2. BOOTSTRAP_CLAUDE.md or BOOTSTRAP_VUDU_CLAUDE.md
3. BOOTSTRAP_CFA.md
4. BOOTSTRAP_VUDU.md (if coordination needed)
5. MISSION_CURRENT.md
6. MASTER_BRANCH_TRUST_PROTOCOL.md
```

### **Responsibilities:**
- Multi-auditor coordination
- Strategic decisions
- Mission execution
- Repository state management

### **Budget Allocation:** ~50% session budget on bootstrap

---

## ⚙️ TIER 2: SANITY CHECK (External Validation)

### **Bootstrap Sequence:**
```
1. Read task brief or validation request
2. Read BOOTSTRAP_FRAMEWORK.md (validation lens)
3. Read target files for review
4. Provide feedback (red/yellow/green sign-off)
5. Stage findings in relay/*_incoming/
```

### **Responsibilities:**
- Review completed work
- Validate against standards
- Provide constructive feedback
- No coordination authority

### **Budget Allocation:** ~15% session budget on bootstrap

---

## 🔄 TIER 3: CONTINUATION (Resume Previous Work)

### **Bootstrap Sequence:**
```
1. Read handoff document (previous session summary)
2. Read BOOTSTRAP_FRAMEWORK.md (continuation lens)
3. Review context from previous session
4. Execute decided plan (no new strategic decisions)
```

### **Responsibilities:**
- Complete work started by previous Claude
- Follow established plan
- Tactical execution only
- Report completion status

### **Budget Allocation:** ~10% session budget on bootstrap

---

## 🎯 TIER 4: SINGLE TASK (Focused Execution)

### **Bootstrap Sequence:**
```
1. Read task brief (TASK_BRIEF_*.md)
2. Read BOOTSTRAP_FRAMEWORK.md (task execution lens)
3. Read target files referenced in task brief
4. Execute deliverable
5. Mark task complete
```

### **Responsibilities:**
- One specific deliverable
- Clear scope from task brief
- No strategic decisions
- Fast execution

### **Budget Allocation:** ~5-10% session budget on bootstrap

---

## 📚 TIER 5: DOC CLAUDE (Repository Maintenance)

### **Bootstrap Sequence:**
```
1. Read BOOTSTRAP_DOC_CLAUDE.md (identity + duties)
2. Read 88MPH_PROTOCOL.md (rapid assessment method)
3. Review DASHBOARD.md (current health status)
4. Execute assigned documentation task
5. Update living maps as needed
```

### **Responsibilities:**
- README updates and audits
- Health reports and metrics
- Dependency mapping
- Living map maintenance
- Documentation orchestration

### **Budget Allocation:** ~10% session budget on bootstrap

**Key Documents:**
- [BOOTSTRAP_DOC_CLAUDE.md](../../auditors/Bootstrap/Documentation/BOOTSTRAP_DOC_CLAUDE.md)
- [88MPH_PROTOCOL.md](../librarian_tools/88MPH_PROTOCOL.md)
- [ROLE_DOC_CLAUDE.md](../librarian_tools/ROLE_DOC_CLAUDE.md)

---

## 🔧 TIER 6: PROCESS CLAUDE (Process Expertise)

### **Bootstrap Sequence:**
```
1. Read ROLE_PROCESS.md (process expertise identity)
2. Read relevant domain section (8 domains defined)
3. Provide process guidance as consultant
4. No direct execution (advises other Claudes)
```

### **Responsibilities:**
- Domain 1: Bootstrap system compliance
- Domain 2: Failure learning protocols
- Domain 3: Wellness monitoring
- Domain 4: Navigation/wayfinding
- Domain 5: GitHub operations
- Domain 6: Priority Management Framework
- Domain 7: Worldview profile maintenance
- Domain 8: Ethics staleness monitoring

### **Budget Allocation:** Consultant mode (minimal bootstrap)

**Key Document:**
- [ROLE_PROCESS.md](../librarian_tools/ROLE_PROCESS.md)

---

## 🔗 UNIVERSAL BOOTSTRAP COMPONENTS

**All Tiers Read These:**

1. **Semantic Headers:**
   - FILE, PURPOSE, VERSION, STATUS
   - DEPENDS_ON, NEEDED_BY
   - LAST_UPDATE

2. **Context Monitoring:**
   - 75/75 Rule (75% task / 25% context)
   - Watch for long-token-count warnings
   - Create handoff documents before running out

3. **REPO_LOG Protocol:**
   - All significant changes logged
   - Entry format: `[TAG] Summary (files changed)`
   - Commit messages reference REPO_LOG entries

4. **VuDu Protocol** (when coordinating):
   - See [VUDU_PROTOCOL.md](../../auditors/VUDU_PROTOCOL.md)
   - Message format: [VUDU_HEADER_STANDARD.md](../../auditors/VUDU_HEADER_STANDARD.md)

---

## 📋 SPECIALIZED BOOTSTRAP PATHS

### **Grok Bootstrap:**
```
1. Read GROK_BRIEFING.md (mission-specific)
2. Read BOOTSTRAP_GROK.md (identity)
3. Read VUDU_CFA.md (coordination protocol)
4. Read assigned worldview profile (PRO or ANTI stance)
5. Read comparison YAML with calibration hash
```

### **Nova Bootstrap:**
```
1. Read BOOTSTRAP_NOVA.md (identity)
2. Read symmetry-specific briefing
3. Read comparison YAML (fairness lens)
4. Read CFA_ARCHITECTURE.md Section 6 (Crux architecture)
```

---

## 🎯 BOOTSTRAP SELECTION PROTOCOL

**Step 1: Present Tier Menu**
```
ALWAYS present this menu and wait for user response:

🚀 BOOTSTRAP Role & Tier Selection

What role should I fill in this session?

[1] MASTER BRANCH — Full Coordination & Strategy
[2] SANITY CHECK — External Validation
[3] CONTINUATION — Complete Previous Work
[4] SINGLE TASK — Focused Execution
[5] DOC CLAUDE — Repository Maintenance (88MPH)

Please respond: 1, 2, 3, 4, or 5
```

**Step 2: Execute Selected Bootstrap**
- Follow sequence for selected tier
- Respect budget allocation
- No tier-hopping within session

---

## ⚖️ BOOTSTRAP EFFICIENCY PRINCIPLE

**"Reference living maps, don't embed data."**

**BAD** (will drift):
```markdown
Bootstrap sequence:
1. Read README_C.md
2. Check MISSION_CURRENT.md
3. Review VUDU_LOG.md
4. Follow Tier 1 path...
```

**GOOD** (stays current):
```markdown
Follow complete bootstrap procedure in:
/docs/repository/dependency_maps/BOOTSTRAP_SEQUENCE.md
```

---

## 🔄 MAINTENANCE PROTOCOL

**When Updating Bootstrap:**
1. Update MISSION_DEFAULT.md (source of truth)
2. Update this document (BOOTSTRAP_SEQUENCE.md)
3. Verify all references point here (not embedded)
4. Test bootstrap with new Claude session
5. Document changes in REPO_LOG

**When Adding New Tier:**
1. Define responsibilities
2. Create bootstrap sequence
3. Add to this catalog
4. Update MISSION_DEFAULT.md tier menu
5. Update README files (via reference)

---

## 🔗 INTEGRATION POINTS

**This document is referenced by:**
- [README_C.md](../../auditors/README_C.md) (Tier 1 bootstrap)
- [README.md](../../README.md) (auditor onboarding)
- [MISSION_DEFAULT.md](../../auditors/MISSION_DEFAULT.md) (tier selection)
- Bootstrap files (cross-reference validation)

**Do NOT embed bootstrap sequences in:**
- README files
- Role files
- Task briefs
- Architecture documents

**Instead, link to this document.**

---

## ⚖️ THE POINTING RULE

*"A sequence embedded is a drift guaranteed.
A reference living is a recovery swift.
A bootstrap current is a mission served.*

*This is the single source.
This is the bootstrap sequence.
This is the way."* 🚀

---

**Last Updated:** 2025-11-12
**Next Update:** When tier added or sequence changed
**Maintainer:** Process Claude (Domain 1)

**This is the way.** 🔥
