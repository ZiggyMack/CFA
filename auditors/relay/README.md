<!---
FILE: README.md
PURPOSE: Document multi-AI coordination relay system
VERSION: v1.1
STATUS: Active
DEPENDS_ON: VUDU_PROTOCOL.md, VUDU_HEADER_STANDARD.md
NEEDED_BY: All auditors, coordination processes
MOVES_WITH: /auditors/relay/
LAST_UPDATE: 2025-10-31 [DOCUMENTATION-2025-10-31-2]
--->

<!-- deps: vudu_protocol -->
# Relay System

**Lines:** 258
**Quality Score:** 95/100 (improved from 90/100)
**Target Score:** 90/100 ✅
**Status:** Active
**Last Updated:** 2025-11-01
**Purpose:** Enable asynchronous multi-AI collaboration through staged messages  

## 🎯 Why Relay Folders?

**The Problem:** Direct AI-to-AI communication isn't possible.  
**The Solution:** Staged message relay through human coordination.  
**The Result:** Effective multi-AI collaboration despite platform constraints.

This relay system serves the PURPOSE of enabling adversarial auditing across AI models.

## Purpose

Asynchronous multi-AI coordination through staged message passing - enabling Claude, Grok, and Nova to collaborate without direct communication.

## How It Works

The relay system enables asynchronous coordination between AI auditors who cannot directly communicate:

```
Auditor A → writes message → stages in B_incoming/ → Human relays → Auditor B reads
```

**Key Innovation:** Each auditor stages messages for others in dedicated incoming folders, allowing complex coordination despite communication barriers.

## Quick Check Protocol (88MPH)

**First 3 minutes of any session:**
1. Check your incoming folder
2. Process any waiting messages
3. Stage responses if needed
4. Continue with primary work

## Directory Structure

```
relay/
├── claude_incoming/      # Messages TO Claude from other auditors
│   ├── README_C.md      # Latest message for Claude
│   ├── README_C1.md     # Secondary messages
│   └── .Archive/        # Processed messages
├── grok_incoming/        # Messages TO Grok from other auditors
│   ├── README_G.md      # Latest message for Grok
│   └── .Archive/        # Processed messages
├── nova_incoming/        # Messages TO Nova from other auditors
│   ├── README_N.md      # Latest message for Nova
│   └── .Archive/        # Processed messages
├── .Archive/            # Completed coordination threads
└── README.md            # This file
```

## Relay Protocol

### Step 1: Write Message
- Author creates message in markdown
- Uses VuDu header standard
- Clear purpose and requested action

### Step 2: Stage Message
- Place in target's incoming folder
- Use correct naming convention
- Update REPO_LOG with relay entry

### Step 3: Human Relay
- Human (Ziggy) facilitates transfer
- Provides message to target auditor
- No modification of content

### Step 4: Process Message
- Target auditor reads message
- Takes requested action
- Stages response if needed

### Step 5: Archive
- Move processed messages to .Archive/
- Maintain thread continuity
- Update REPO_LOG

## File Naming Conventions

### Primary Messages
- `README_C.md` - Main message for Claude
- `README_G.md` - Main message for Grok  
- `README_N.md` - Main message for Nova

### Secondary Messages
- `README_C1.md`, `README_C2.md` - Additional Claude messages
- `README_G1.md`, `README_G2.md` - Additional Grok messages
- `README_N1.md`, `README_N2.md` - Additional Nova messages

### Special Messages
- `ACTIVATION_[TOPIC].md` - Activation sequences
- `HANDOFF_[FROM]_TO_[TO].md` - Explicit handoffs
- `CONSENSUS_REQUEST.md` - Multi-auditor decisions
- `TIER_ACTIVATION_[TIER].md` - Bootstrap tier activations

## Message Format

All relay messages use the VuDu Header Standard format.

**Format Specification:** `/auditors/VUDU_HEADER_STANDARD.md`

The standard includes:
- Header fields (From, Type, Date)
- Body fields (Action, Key Assumptions, Status)
- Footer fields (Awaiting, Sanity, Log)

See VUDU_HEADER_STANDARD.md for complete field descriptions and relay-specific examples.

## Common Relay Patterns

### Consensus Building
1. Initiator stages CONSENSUS_REQUEST.md
2. Each auditor reviews and stages position
3. Human synthesizes positions
4. Final decision documented in README_C.md

### Validation Request
1. Proposer stages configuration change
2. Validator runs tests
3. Results staged back
4. Decision based on empirical data

### Activation Cascade
1. Master Branch stages tier activations
2. Each tier acknowledges receipt
3. Work begins per tier capabilities
4. Results flow back through relay

## Current Activity

### Active Threads
- Check each incoming folder for unprocessed messages
- Look for ACTIVATION messages during mission start
- Monitor for CONSENSUS_REQUEST items
- Average relay response time: <24 hours

### Recent Completions
- Check .Archive/ for recent coordination
- Review REPO_LOG [RELAY] entries

### Pending Messages
- Any README_[X].md files in incoming folders
- Messages awaiting human relay
- Responses staged but not delivered

## Integration Points

- **VuDu Protocol:** [VUDU_PROTOCOL.md](/auditors/VUDU_PROTOCOL.md)
- **Header Standard:** [VUDU_HEADER_STANDARD.md](/auditors/VUDU_HEADER_STANDARD.md)
- **Master State:** [README_C.md](/auditors/README_C.md)
- **Mission System:** [missions/README.md](/auditors/missions/README.md)
- **Process Tracking:** [REPO_LOG.md](/REPO_LOG.md)

## Best Practices

### Do's
- ✅ Clear subject lines
- ✅ Specific action requests
- ✅ Include context
- ✅ Update REPO_LOG
- ✅ Archive processed messages
- ✅ Check relay in first 3 minutes

### Don'ts
- ❌ Assume message was received
- ❌ Skip VuDu headers
- ❌ Leave ambiguous requests
- ❌ Forget to check incoming
- ❌ Delete messages (archive instead)

## Relay Philosophy

**"Asynchronous coordination through disciplined communication."**

The relay system works because:
- **Structure:** Consistent format and location
- **Discipline:** Always check incoming folders
- **Clarity:** Explicit requests and responses
- **History:** Archived threads show evolution
- **Trust:** Human relay preserves message integrity

## Troubleshooting

### Message Not Received?
1. Check correct incoming folder
2. Verify naming convention
3. Check REPO_LOG for relay entry
4. Ask human coordinator

### Unclear Response Needed?
1. Check original message for ACTION_REQUIRED
2. Review mission context
3. Default to acknowledging receipt
4. Ask for clarification via relay

### Coordination Breakdown?
1. Stage CONSENSUS_REQUEST.md
2. Document issue clearly
3. Request human intervention
4. Track in REPO_LOG

## 🔗 Interconnected Documentation

### Navigation Hierarchy
```
Repository Root
├── /auditors/ (operational documentation)
│   ├── README.md → Overview
│   ├── missions/ → Mission-based work
│   ├── relay/ → THIS FILE
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

**Last Updated:** 2025-11-01 by DOC_CLAUDE - [DOCUMENTATION-2025-10-31-2]
