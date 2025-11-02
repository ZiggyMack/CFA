<!---
FILE: README.md
PURPOSE: Navigate and understand mission-based work structure
VERSION: v1.1
STATUS: Active
DEPENDS_ON: MISSION_CURRENT.md, VUDU_PROTOCOL.md
NEEDED_BY: All auditors, README_C.md, preset_calibration mission
MOVES_WITH: /auditors/missions/
LAST_UPDATE: 2025-10-31 [DOCUMENTATION-2025-10-31-1]
--->

<!-- deps: mission_system, vudu_protocol -->
# Missions Directory

**Lines:** 193
**Quality Score:** 90/100 (improved from 85/100)
**Target Score:** 90/100 ✅
**Status:** Active
**Last Updated:** 2025-11-01
**Purpose:** Organized mission-based work for focused VuDu coordination  

## 🎯 Why Missions?

**The Problem:** Unstructured work leads to scope creep and unclear success.  
**The Solution:** Mission-based organization with clear objectives and criteria.  
**The Result:** Focused work that converges on defined success.

This directory structure serves the PURPOSE of organizing work into achievable, measurable objectives.

## Purpose

Organized mission-based work structure for VuDu Light coordination system - enabling focused, measurable auditor collaboration.

## Current Mission

**Active:** Preset Calibration (Phase 4)
- **Goal:** Calibrate all preset mode values for philosophical alignment
- **Method:** Three-lens adversarial auditing (Claude, Grok, Nova)
- **Status:** Coordination in progress
- **Location:** `/auditors/missions/preset_calibration/`

## Directory Structure

```
missions/
├── preset_calibration/          # Current active mission
│   ├── MISSION_BRIEF.md        # What and why
│   ├── SUCCESS_CRITERIA.md     # How we know we're done
│   ├── TECHNICAL_SPEC.md       # Implementation details
│   └── results/                # Mission outputs
├── .Archive/                    # Completed missions (standardized naming)
│   └── [past_missions]/        # Historical reference
└── README.md                    # This file
```

## Mission Lifecycle

### 1. Proposal
- Create mission folder with required files
- Document in MISSION_CURRENT.md
- Track in REPO_LOG as [MISSION] entry

### 2. Activation
- Update MISSION_CURRENT.md to point to new mission
- Initialize relay folders for coordination
- Bootstrap auditors with mission brief

### 3. Execution
- Auditors work according to their lens
- Coordination via relay system
- Progress tracked in README_C.md

### 4. Completion
- Success criteria validated
- Results documented
- Mission folder moved to .Archive/

### 5. Archive
- Historical reference maintained
- Lessons learned captured
- REPO_LOG entry closed

## Creating New Missions

### Required Files

1. **MISSION_BRIEF.md**
   - Clear statement of purpose
   - Problem to solve
   - Expected outcome

2. **SUCCESS_CRITERIA.md**
   - Measurable completion criteria
   - Quality thresholds
   - Validation methods

3. **TECHNICAL_SPEC.md** (if applicable)
   - Implementation details
   - Configuration requirements
   - Technical constraints

### Approval Process

1. Propose mission in relay folder
2. Get consensus from auditors
3. Create mission structure
4. Update MISSION_CURRENT.md
5. Track in REPO_LOG

### REPO_LOG Requirements

```markdown
### [MISSION-YYYY-MM-DD-N] Mission Name

**Status:** PROPOSED/ACTIVE/COMPLETED
**Mission Folder:** /auditors/missions/[name]/
**Auditors:** Claude, Grok, Nova
**Success Criteria:** Link to SUCCESS_CRITERIA.md
**Entry ID Format:** [MISSION-2025-10-31-1]
```

## Mission Health Metrics

**Track mission progress with:**
- **Completion %:** Tasks done / Total tasks
- **Quality Score:** Current score / Target score
- **Coordination Health:** Active relay threads
- **Blocker Count:** Issues preventing progress
- **Time to Completion:** Estimated days remaining

## Navigation Links

- **Current Mission Details:** [MISSION_CURRENT.md](/auditors/MISSION_CURRENT.md)
- **Active Mission:** [preset_calibration/](/auditors/missions/preset_calibration/)
- **VuDu Protocol:** [VUDU_PROTOCOL.md](/auditors/VUDU_PROTOCOL.md)
- **Master State:** [README_C.md](/auditors/README_C.md)
- **Relay System:** [relay/README.md](/auditors/relay/README.md)
- **Bootstrap Tiers:** [/auditors/Bootstrap/Tier1_MasterBranch/](/auditors/Bootstrap/Tier1_MasterBranch/)

## Dependencies

- **Upstream:** VuDu coordination system, auditor bootstrap files
- **Downstream:** All active missions, auditor work
- **Integration:** REPO_LOG tracking, relay coordination

## Mission Philosophy

Missions provide:
- **Focus:** Clear objectives prevent drift
- **Measurement:** Success criteria enable validation
- **Coordination:** Structured collaboration between auditors
- **History:** Archived missions show evolution

**"A mission without criteria is just a wish."**

## 🔗 Interconnected Documentation

### Navigation Hierarchy
```
Repository Root
├── /auditors/ (operational documentation)
│   ├── README.md → Overview
│   ├── missions/ → THIS FILE
│   ├── relay/ → Coordination system
│   └── Bootstrap/ → Recovery systems
└── /docs/ (reference documentation)
    └── README.md → Architecture & philosophy
```

### Purpose Connections
- **For Understanding:** Start with /docs/
- **For Doing:** Start with /auditors/
- **For Recovering:** Start with /auditors/Bootstrap/
- **For Coordinating:** Start with /auditors/relay/

### Essential Links
- [README_C.md](/auditors/README_C.md) - Current state
- [MISSION_CURRENT.md](/auditors/MISSION_CURRENT.md) - Active work
- [REPO_LOG.md](/REPO_LOG.md) - Change tracking
- [VUDU_PROTOCOL.md](/auditors/VUDU_PROTOCOL.md) - Coordination

## ❓ Purpose Check

Ask yourself:
1. Does this README help you understand the PURPOSE of this directory?
2. Can you navigate to what you need based on your GOAL?
3. Is the structure serving its intended PURPOSE?

If any answer is "no" - this README needs improvement.

---

**Last Updated:** 2025-11-01 by DOC_CLAUDE - [DOCUMENTATION-2025-10-31-1]
