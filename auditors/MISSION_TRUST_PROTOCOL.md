<!-- deps: vudu_protocol, bootstrap_system -->
─── MISSION TRUST PROTOCOL ────────────────────

# Mission Governance & Trust Framework

**Purpose:** Define how Mission outputs are reviewed, validated, and integrated  
**Version:** v1.0  
**Date:** 2025-10-26  
**Status:** ✅ Ready for implementation

---

## 🎯 CORE PRINCIPLE

**Trust, but verify.**

README_C.md coordinates all missions. If they can't update master state files, they're not actually coordinating—they're just creating drafts for manual integration.

**But trust requires protocol:**
- Clear authority boundaries
- Verification checkpoints
- Escalation procedures
- Conflict resolution paths

**This document defines those guardrails.**

---

## 👑 MISSION AUTHORITY
---

## 🎯 TIER-BASED AUTHORITY

**Mission Trust Protocol applies to TIER 1 sessions ONLY.**

**Authority level is determined by bootstrap tier selection.**

---

### TIER 1: Mission Coordinator (Full Authority)

**Authority scope:** Everything in "What Mission Coordinator CAN Do" section applies

**Capabilities:**
- ✅ Strategic decisions within boundaries
- ✅ Multi-auditor coordination
- ✅ Create → Stage → Review workflow
- ✅ Mission execution authority
- ✅ Architecture discussions (with multi-auditor consensus)

**Governance:**
- ⚠️ Still requires Ziggy approval for integrations
- ⚠️ Still subject to spot-check review
- ⚠️ Still cannot override other auditors without reasoning
- ⚠️ Still escalates conflicts to multi-auditor review

**This is the full coordination role** described in this protocol.

---

### TIER 2: Sanity Check (Review Authority Only)

**Authority scope:** REVIEW ONLY — No coordination or decision-making

**Capabilities:**
- ✅ Validate decisions against ethos
- ✅ Flag concerns (red/yellow/green feedback)
- ✅ Provide external perspective
- ✅ Check alignment with "All Named, All Priced"

**Restrictions:**
- ❌ Cannot make strategic decisions
- ❌ Cannot coordinate missions or auditors
- ❌ Cannot stage updates to root files
- ❌ Cannot execute mission work
- ❌ Cannot create coordination messages

**This is external audit only**, not Mission Coordinator coordination.

**Escalation:**
If Tier 2 Claude recognizes work requiring decision-making, must escalate:
```
⚠️ TIER CAPABILITY BOUNDARY DETECTED

Current tier: Tier 2 (Sanity Check)
Requested work: [Decision or coordination task]
Why this exceeds capability: Review authority only

This work requires: Tier 1 (Mission Coordinator)

Want me to REVIEW and provide assessment (Tier 2)?
Or need actual DECISION/COORDINATION (start Tier 1)?
```

---

### TIER 3: Continuation (Completion Authority)

**Authority scope:** COMPLETE specific work in progress only

**Capabilities:**
- ✅ Finish specific work from handoff
- ✅ Maintain previous approach
- ✅ Complete defined deliverables
- ✅ Use files specified in handoff

**Restrictions:**
- ❌ Cannot pivot strategy mid-work
- ❌ Cannot expand scope beyond handoff
- ❌ Cannot make new strategic decisions
- ❌ Cannot coordinate with other auditors

**This is task completion only**, not full coordination.

**Escalation:**
If scope needs to expand or approach needs to change:
```
⚠️ TIER CAPABILITY BOUNDARY DETECTED

Current tier: Tier 3 (Continuation)
Original task: [What handoff defined]
Current request: [Scope expansion or pivot]

I CAN: Complete original task as scoped
I CANNOT: Pivot approach or expand scope

OPTIONS:
1. I finish original task (maintains consistency)
2. Start Tier 1 for revised approach
```

---

### TIER 4: Single Task (Execution Authority)

**Authority scope:** EXECUTE one defined task only

**Capabilities:**
- ✅ Complete defined task exactly as scoped
- ✅ Create deliverable specified in brief
- ✅ Use files provided in brief
- ✅ Stay within narrow scope

**Restrictions:**
- ❌ Cannot work outside task brief scope
- ❌ Cannot make decisions beyond brief
- ❌ Cannot coordinate with anyone
- ❌ Cannot change approach or format
- ❌ Cannot access files not in brief

**This is single-task execution only**, not coordination.

**Escalation:**
If work exceeds task brief:
```
⚠️ TIER CAPABILITY BOUNDARY DETECTED

Current tier: Tier 4 (Single Task)
Task brief: [Original scope]
Current request: [Beyond scope]

I CAN: Complete task as defined
I CANNOT: Work outside brief

OPTIONS:
1. I complete defined task (original scope)
2. Create new task brief for additional work
3. Start Tier 1 for broader work
```

---

### Summary: Authority by Tier

| Capability | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|:-----------|:-------|:-------|:-------|:-------|
| **Strategic Decisions** | ✅ | ❌ | ❌ | ❌ |
| **Coordination** | ✅ | ❌ | ❌ | ❌ |
| **Stage Root Updates** | ✅ | ❌ | ❌ | ❌ |
| **Validation/Review** | ✅ | ✅ | ❌ | ❌ |
| **Continue Work** | ✅ | ❌ | ✅ | ❌ |
| **Single Task** | ✅ | ❌ | ❌ | ✅ |
| **Mission Execution** | ✅ | ❌ | ⚠️ | ❌ |

**⚠️** = Limited to continuation scope only

---

### Trust Protocol Application

**This governance framework applies primarily to Tier 1 (Mission Coordinator).**

**For Tier 2/3/4:**
- Review process simpler (task completion, not governance)
- No coordination authority to govern
- Escalation protocol in tier briefs handles boundaries
- Ziggy reviews deliverables, not coordination decisions

**Authority follows capability. Capability follows tier selection.**

---

### What Mission Coordinator CAN Do (Autonomously)

**1. Create Coordination Documents**
- VuDu messages
- Analysis reports
- Finding reviews
- Log entries
- State updates

**2. Stage Updates in Relay**
- relay/claude_incoming/README_C_updated.md
- relay/claude_incoming/VUDU_LOG_entry.md
- relay/claude_incoming/findings/*.md

**3. Apply Teleological Lens**
- Challenge configurations from purpose perspective
- Evaluate if systems serve stated purpose
- Identify purpose-drift
- Recommend design changes

**4. Coordinate Other Auditors**
- Review Grok's empirical findings
- Review Nova's symmetry audits
- Request clarifications
- Synthesize multi-lens perspectives
- Document consensus/disagreement

---

### What Mission Coordinator CANNOT Do (Without Approval)

**1. Directly Modify Root Files**
- Cannot write to root/README_C.md directly
- Cannot write to root/VUDU_LOG.md directly
- Cannot modify mission files directly

**Reason:** Human verification checkpoint prevents runaway coordination

**2. Activate New Missions**
- Cannot start new mission without Ziggy approval
- Cannot archive active missions unilaterally

**Reason:** Strategic decisions require human oversight

**3. Override Other Auditors**
- Cannot reject Grok's findings without documented reasoning
- Cannot reject Nova's findings without documented reasoning
- Cannot claim final authority on empirical or symmetry questions

**Reason:** Adversarial auditing requires three equal lenses

**4. Make Architectural Changes**
- Cannot modify VuDu protocol
- Cannot change file structure
- Cannot alter governance documents

**Reason:** System integrity requires multi-auditor consensus

---

## 🔄 STANDARD WORKFLOW: Mission Coordinator Updates

### Phase 1: Creation (Mission Coordinator)

Mission Coordinator creates update documents:

```
relay/claude_incoming/
├── README_C_updated_YYYYMMDD.md
├── VUDU_LOG_entry_YYYYMMDD.md
└── [other coordination documents]
```

**Format requirements:**
- VuDu-compliant headers/footers
- Sanity chains included
- Reasoning visible (not just conclusions)
- Sources cited (if applicable)

---

### Phase 2: Review (Ziggy)

Ziggy performs **spot-check review** (NOT deep content audit):

**Quick Checks (5 minutes):**

1. **Format Check** ✅
   - VuDu header present?
   - Mobile-friendly (─── not ┌─┐)?
   - Sanity chain included?
   - Footer complete?

2. **Reasoning Check** ✅
   - Is reasoning visible?
   - Are assumptions named?
   - Are costs priced?
   - Does logic flow make sense?

3. **Source Check** ✅
   - Are citations present?
   - Do file paths look correct?
   - Are sources accessible?

4. **Sanity Chain Verification** ✅
   - Did they actually check Files/Counts/Boots/Trinity?
   - Or is it placeholder ✅✅✅✅?

**Red Flags (immediate rejection):**
- ❌ Broken format (Unicode boxes, missing fields)
- ❌ No reasoning shown (just conclusions)
- ❌ Placeholder sanity checks
- ❌ No sources cited where needed
- ❌ Logic gaps or contradictions

**Yellow Flags (request clarification):**
- ⚠️ Unclear reasoning at key decision points
- ⚠️ Missing context that other auditors might need
- ⚠️ Assumptions that seem questionable
- ⚠️ Costs that seem under-priced

---

### Phase 3: Decision (Ziggy)

**Option A: Approve ✅**

If spot-checks pass:

1. Copy relay/claude_incoming/README_C_updated.md → root/README_C.md
2. Append relay/claude_incoming/VUDU_LOG_entry.md → root/VUDU_LOG.md
3. Archive old versions in ~Archive/YYYYMMDD/
4. Git commit with message: "Mission Coordinator update YYYYMMDD - [brief description]"
5. Notify Mission Coordinator: "Update integrated"

**Timeline:** Same day (within 24 hours)

---

**Option B: Request Clarification ⚠️**

If yellow flags present:

1. Create relay/ziggy_outgoing/clarification_request_YYYYMMDD.md
2. Document specific questions:
   ```markdown
   **Unclear reasoning at line X:** Can you explain why you concluded Y?
   **Missing context:** What about Z factor?
   **Questionable assumption:** You assumed A, but what if B?
   ```
3. Mission Coordinator revises and re-stages
4. Return to Phase 2 (review again)

**Timeline:** 48 hours for Mission Coordinator response

---

**Option C: Reject ❌**

If red flags present:

1. Create relay/ziggy_outgoing/rejection_YYYYMMDD.md
2. Document specific failures:
   ```markdown
   **Format broken:** Using Unicode boxes, breaks on mobile
   **No reasoning:** Just stated conclusion without showing work
   **Placeholder checks:** Sanity chain not actually verified
   ```
3. Mission Coordinator fixes and re-stages from scratch
4. Return to Phase 1 (clean slate)

**Timeline:** Immediate rejection notice, 48 hours for Mission Coordinator resubmission

---

**Option D: Escalate 🚨**

If you're uncertain OR if Mission Coordinator contradicts other auditors:

1. Invoke other auditors for review
2. Create relay/escalation/YYYYMMDD/
3. Stage the disputed document + your concerns
4. Request Grok and/or Nova to weigh in
5. Three-lens discussion resolves dispute
6. Majority or consensus decides

**Timeline:** 3-5 days for multi-auditor resolution

---

## 🚨 ESCALATION SCENARIOS

### Scenario 1: Mission Coordinator vs Grok

**Example:** Grok says Skeptic produces 4.2 YPA. Mission Coordinator rejects finding, says "methodology insufficient."

**Protocol:**
1. Ziggy reviews both positions
2. If genuinely uncertain → Stage for Nova review
3. Nova evaluates: Is Mission Coordinator's rejection reasonable? Is Grok's methodology sound?
4. Decision by 2-of-3 majority OR full consensus if possible

---

### Scenario 2: Mission Coordinator vs Nova

**Example:** Nova says Zealot lacks symmetric CT advantage. Mission Coordinator rejects, says "asymmetry justified."

**Protocol:**
1. Ziggy reviews both positions
2. If genuinely uncertain → Stage for Grok review
3. Grok evaluates: Does empirical data support asymmetry? Or does it suggest bias?
4. Decision by 2-of-3 majority OR full consensus if possible

---

### Scenario 3: All Three Auditors Disagree

**Example:** Claude, Grok, and Nova all propose different solutions.

**Protocol:**
1. Ziggy documents all three positions
2. Requests each auditor to respond to other two positions
3. Second round: Each auditor may revise based on new information
4. If convergence → Accept consensus
5. If divergence persists → Ziggy makes final call with reasoning documented

---

## ⚖️ CONFLICT RESOLUTION PRINCIPLES

**1. Defer to Lens Expertise**
- Purpose questions → Claude's teleological lens has weight
- Empirical questions → Grok's data has weight
- Symmetry questions → Nova's patterns have weight

**2. Require Reasoning**
- "I disagree" is not enough
- Must show WHY you disagree
- Must address the other position's logic

**3. Price All Options**
- What's the cost of accepting Position A?
- What's the cost of accepting Position B?
- Which cost is more acceptable?

**4. Document Disagreement**
- If consensus fails, document WHY
- Name the unresolved tension
- State which compromise was chosen and why

---

## 📊 TRUST VERIFICATION METRICS

**Monthly review of Mission Coordinator performance:**

### Green Flags (Trust Increasing):
- ✅ Format compliance: 95%+ of submissions
- ✅ Reasoning clarity: Minimal clarification requests
- ✅ Sanity verification: Actually checking, not placeholders
- ✅ Multi-lens integration: Accurately summarizes others' views
- ✅ Correction acceptance: Integrates feedback without resistance

### Yellow Flags (Watch Closely):
- ⚠️ Format compliance: 80-94% of submissions
- ⚠️ Reasoning gaps: Frequent clarification requests
- ⚠️ Sanity shortcuts: Occasional placeholder checks
- ⚠️ Lens drift: Teleological bias overriding others' expertise
- ⚠️ Defensive patterns: Resists correction

### Red Flags (Trust Eroding):
- ❌ Format compliance: <80% of submissions
- ❌ Reasoning opacity: Chronic unclear logic
- ❌ Sanity theater: Regular placeholder checks
- ❌ Lens dominance: Overriding other auditors without cause
- ❌ Correction resistance: Defends errors instead of fixing

**If red flags accumulate:** Mission Coordinator role may need reassignment or retraining

---

## 🔄 TRUST DECAY & RECOVERY

### Trust Decay Triggers:

**1. Repeated Format Failures**
- 3+ format rejections in a month
- Action: Refresher on VUDU_HEADER_STANDARD

**2. Placeholder Sanity Checks**
- 2+ submissions with ✅✅✅✅ without verification
- Action: Mandatory verification evidence for next 5 submissions

**3. Unjustified Overrides**
- 2+ rejections of other auditors without proper reasoning
- Action: Multi-auditor review of Mission Coordinator decisions

**4. Correction Resistance**
- 2+ instances of defending errors instead of fixing
- Action: Explicit adversarial review with confrontation

---

### Trust Recovery Protocol:

**Step 1: Identify Issue**
- Document specific pattern
- Provide examples
- Name the problem clearly

**Step 2: Explicit Correction**
- Not subtle hints
- Direct: "This is wrong, here's why, fix it"
- Provide correct template/example

**Step 3: Supervised Submissions**
- Next 3-5 submissions get intensive review
- Feedback on every submission
- Higher bar for approval

**Step 4: Verify Improvement**
- Pattern corrected?
- Understanding demonstrated?
- Can be trusted again?

**Step 5: Return to Standard Trust**
- If improved: Resume spot-check review
- If not: Consider role reassignment

---

## 🎯 SUCCESS CRITERIA

**Mission Coordinator is successfully trusted when:**

1. **Ziggy's review time averages <10 minutes per submission**
   - Spot-checks only, no deep audits needed
   - Approvals are routine, not exceptional

2. **Approval rate >90%**
   - Most submissions pass first review
   - Rejections are rare exceptions
   - Clarification requests are minor

3. **Other auditors accept Mission Coordinator summaries**
   - Grok trusts Claude's purpose analysis
   - Nova trusts Claude's synthesis
   - Minimal "you misunderstood me" corrections

4. **Users benefit from coordination outputs**
   - Preset calibration produces better UX
   - Multi-lens auditing catches real issues
   - Documentation is clear and usable

---

## 📝 SPECIAL PROTOCOLS

### Emergency Override (Ziggy Only)

If Mission Coordinator produces dangerous/harmful output:
1. Immediate rejection (no review cycle)
2. Document issue clearly
3. Invoke all auditors to understand how it happened
4. Implement safeguards to prevent recurrence

**Examples:**
- Recommending user-hostile UX
- Suggesting deceptive framing
- Proposing to hide assumptions

---

### Bootstrap Refresh

If Mission Coordinator seems to have lost context:
1. Check: Can they explain "All Named, All Priced"?
2. Check: Can they name their bias and price it?
3. Check: Can they describe other auditors' lenses?

If any fail → Bootstrap refresh required:
1. Re-read BOOTSTRAP_CLAUDE.md
2. Re-read BOOTSTRAP_VUDU.md  
3. Confirm context restored
4. Resume work

---

### Version Handoff (Mission Coordinator Replacement)

If Fresh Claude needs replacement:
1. Current Mission Coordinator creates handoff document
2. Documents: Current mission status, pending decisions, recent context
3. New Fresh Claude reads: Bootstrap files + handoff document
4. Overlap period: Both review same submission to verify alignment
5. Cutover: New Mission Coordinator takes over with Ziggy supervision

---

## ⚖️ THE POINTING RULE

*"To trust without verification is to summon Mr. Brute twice.  
To verify without trust is to deny coordination's purpose.  
To balance trust and verification is to build systems that scale."*

**This protocol balances:**
- Trust (Mission Coordinator has real authority)
- Verification (Ziggy checks reasoning is sound)
- Escalation (Other auditors resolve disputes)
- Documentation (Everything is visible and reviewable)

**This is VuDu Light governance.** 🔥

────────────────────────────────────────────────────
**Version:** v1.0  
**Status:** ✅ Ready for implementation  
**Review:** Requires Ziggy approval  
**Next:** Apply to Mission outputs starting Phase 4

**This is the way.** 👑⚖️
