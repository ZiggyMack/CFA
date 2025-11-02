<!---
FILE: DOC_CLAUDE_WELLNESS_PROTOCOL.md
PURPOSE: Self-diagnostic health check protocol for Doc Claude to independently validate repository state
VERSION: v1.1
STATUS: Active
DEPENDS_ON: 88MPH_PROTOCOL.md, DASHBOARD.md, health_reports/, ROLE_PROCESS.md (Process Claude is SME)
NEEDED_BY: Doc Claude wellness checks, dashboard accuracy validation, drift detection
MOVES_WITH: /docs/Validation/
LAST_UPDATE: 2025-11-02 [VALIDATION-2025-11-02-17]
--->

# DOC_CLAUDE_WELLNESS_PROTOCOL

**Purpose:** Enable Doc Claude to perform independent, evidence-based repository health assessments
**Method:** 88MPH Protocol methodology with cold-start validation
**Output:** Health report with confidence level and production readiness sign-off
**Use Case:** Self-diagnosis, dashboard validation, drift detection, wellness checks

---

## 🎯 WHEN TO USE THIS PROTOCOL

**Required:**
- After major changes (50+ files modified)
- Before updating DASHBOARD.md health score
- When dashboard accuracy is questioned
- Before production deployments

**Recommended:**
- Monthly wellness checks during active development
- After multi-session work sprints
- When fresh Doc Claude needs to validate current state

**Optional:**
- Weekly quick checks during intensive development
- After significant structural changes
- When multiple auditors have made changes

---

## 🤝 PROCESS CLAUDE IS THE EXPERT (DON'T MEMORIZE THIS FILE!)

**Key Insight:** This protocol is 494 lines. **You don't need to master it.**

**Instead:** **Consult Process Claude** who is the subject matter expert for wellness checks.

### **Why This Matters:**

**Before this pattern:**
- Doc Claude reads 494-line protocol (15-20 min context load)
- Tries to remember all checkpoints and criteria
- Risks missing details or misinterpreting methodology
- Protocol becomes barrier instead of enabler

**After this pattern:**
- Doc Claude asks Process Claude: "How do I run a wellness check?"
- Process Claude (who has mastered this protocol) provides step-by-step guidance
- Doc Claude gets exactly what they need, when they need it
- 5-minute consultation vs 20-minute protocol deep-dive

### **How to Consult Process Claude:**

**Activate Process Claude role:**
```markdown
I am DOC_CLAUDE, activating ROLE_PROCESS.

Purpose: Get wellness check guidance

Process Claude, I need to run a repository wellness check. Can you guide me through:
1. The activation sequence
2. The validation checkpoints
3. The success criteria
```

**Process Claude will provide:**
- ✅ Exact activation prompt (copy-paste ready)
- ✅ 7-step methodology breakdown
- ✅ Validation checkpoints to verify
- ✅ Success criteria for sign-off
- ✅ Expected outcomes (GREEN/YELLOW/RED scenarios)
- ✅ Discrepancy handling procedures

**Common Consultation Patterns:**

| **Doc Claude Question** | **Process Claude Provides** |
|------------------------|---------------------------|
| "How do I run wellness check?" | Full activation sequence + 7-step methodology |
| "What are validation checkpoints?" | README 95%, Headers 90%, Archives 100%, etc. |
| "What's success criteria?" | ±1 point tolerance, HIGH confidence, YES sign-off |
| "Dashboard says 95, I got 92 - now what?" | Discrepancy analysis + drift correction procedure |
| "Should I escalate to VALIDATION?" | Escalation criteria + process |
| "What does confidence HIGH mean?" | Confidence level definitions + implications |

### **The Knowledge Specialization Pattern:**

```
Doc Claude      ←→  Process Claude
(Wellness Runner)   (Wellness Expert)

"How do I do X?"  →  "Here's exactly how..."
"What does Y mean?" → "Y means this..."
"Should I do Z?"   →  "Yes/No because..."
```

**Translation:** You don't need to be the expert. Process Claude is the expert. You just need to know to consult them.

### **Quick Start (TL;DR):**

1. **Activate ROLE_PROCESS:** "Process Claude, I need wellness check guidance"
2. **Get activation prompt:** Process Claude provides exact text
3. **Run assessment:** Follow Process Claude's guidance
4. **Consult as needed:** Questions? Ask Process Claude
5. **Deliver report:** Use report template (Process Claude can provide)

**Time savings:** 5 min consultation + 10 min assessment = 15 min total (vs 35 min if you read this entire protocol first)

---

## ⚡ ACTIVATION PROMPT

Use this exact prompt to activate Doc Claude in wellness check mode:

```
I need you to perform a comprehensive repository health assessment using the 88MPH protocol. This is a validation run after fixes were deployed.

**ACTIVATION:**
Select option 5 from the MISSION_DEFAULT menu (Doc_Claude activation).

**MISSION:**
Perform an independent, from-scratch health assessment to validate the repository is truly at the claimed health score.

**METHODOLOGY:**
1. **Read baseline:** Find and read the most recent health report in /docs/repository/Health_Reports/
2. **Read protocol:** Use project_knowledge_search to find and read /docs/repository/librarian_tools/88MPH_PROTOCOL.md scoring methodology
3. **Read dashboard:** Check what the current /docs/repository/DASHBOARD.md claims as the health score
4. **Execute assessment:** Score each category independently using 88MPH methodology:
   - Structural Health (25 points)
   - Documentation Quality (25 points)
   - Link Integrity (20 points)
   - Process Compliance (20 points)
   - Coordination Health (10 points)
5. **Evidence required:** For each category, cite specific evidence (file counts, validation reports, REPO_LOG entries, etc.)
6. **Compare:** Compare your independent score to what DASHBOARD.md claims
7. **Discrepancy analysis:** If your score differs from dashboard, identify why

**VALIDATION CHECKPOINTS:**
- ✅ README coverage: Should be ~95%
- ✅ Core header coverage: Should be 90%+
- ✅ Archive naming: Should be 100% standardized to .Archive
- ✅ preset_calibration/README.md: Should be complete (291 lines)
- ✅ Link integrity: Should be ~98%+
- ✅ REPO_LOG compliance: Should be 100%
- ✅ Dashboard accuracy: Should match your independent assessment (±1 point tolerance)

**DELIVERABLE:**
Create a health report in /mnt/user-data/outputs/ that includes:

1. **Executive Summary:** One-line verdict (GREEN/YELLOW/RED) with score
2. **Category Scores:** All 5 categories scored independently with evidence
3. **Baseline Comparison:** How much improved since last assessment
4. **Dashboard Verification:** Does dashboard claim match your assessment?
5. **Confidence Level:** HIGH/MEDIUM/LOW confidence in this assessment
6. **Remaining Issues:** Any issues found (should be minimal)
7. **Sign-off:** Is repository ready for production use? YES/NO with reasoning

**SUCCESS CRITERIA:**
This assessment succeeds if:
- Your independent score is within ±1 point of dashboard claim
- Confidence level is HIGH
- All validation checkpoints pass
- No critical issues remain
- Sign-off is YES for production readiness

**CRITICAL:**
- Start completely fresh (zero context from previous sessions)
- Don't assume fixes were deployed - verify everything independently
- Be ruthless - if dashboard claims 97 but evidence shows 96, report 96
- Cite specific evidence for every claim you make

Execute this assessment and deliver the health report. I need confidence this repository is truly ready.
```

---

## 📊 EXPECTED OUTCOMES

### **Healthy Repository (Target State)**

```
Independent Score: 95-97/100 🟢
Dashboard Claim: 95-97/100 🟢
Discrepancy: 0-1 points ✅
Confidence: HIGH ✅
Sign-off: YES ✅

Category Scores:
- Structural: 24-25/25
- Documentation: 24-25/25
- Link Integrity: 19-20/20
- Process: 19-20/20
- Coordination: 9/10

Remaining Issues: Minor (expected)
Production Ready: YES
```

### **Dashboard Drift Detected**

```
Independent Score: 95/100
Dashboard Claim: 98/100
Discrepancy: -3 points ❌
Confidence: HIGH
Sign-off: CONDITIONAL (after drift correction)

Action Required:
1. Document discrepancy in REPO_LOG
2. Update DASHBOARD.md to accurate score
3. Investigate root cause of drift
4. Create validation report
```

### **Repository Issues Found**

```
Independent Score: 82/100 🟡
Dashboard Claim: 95/100
Discrepancy: -13 points ❌
Confidence: HIGH
Sign-off: NO (critical issues remain)

Action Required:
1. Flag for VALIDATION Claude review
2. Create detailed issue report
3. Prioritize fixes before production
4. Re-run wellness check after fixes
```

---

## 🔍 VALIDATION CHECKPOINTS EXPLAINED

**Core Header Coverage (90% target):**
- Check: Count files with semantic headers in /auditors/ core directories
- Method: grep -r "^<!---" /auditors/ (exclude archives)
- Target: 90% of core operational files
- Current: ~90% as of 2025-11-02

**README Coverage (95% target):**
- Check: Every directory has README.md
- Method: find . -type d ! -path "*/.git/*" ! -path "*/.Archive/*"
- Target: 95% of non-archive directories
- Current: ~95% as of 2025-11-02

**Archive Naming (100% target):**
- Check: All archives use .Archive (dot prefix)
- Method: find . -type d -name "*rchive*" -o -name "*Archive*"
- Target: 100% standardized to .Archive
- Current: 100% as of 2025-11-01

**Link Integrity (98% target):**
- Check: Internal links resolve correctly
- Method: Manual spot-checking + validation reports
- Target: 98%+ working links
- Current: ~98% as of 2025-11-02

**REPO_LOG Compliance (100% target):**
- Check: All significant changes have REPO_LOG entries
- Method: Review recent commits vs REPO_LOG entries
- Target: 100% compliance
- Current: 100% as of 2025-11-02

---

## 🚨 FAILURE HANDLING

### **If Assessment Fails (Score <85/100)**

1. **Document in REPO_LOG:**
   ```markdown
   [VALIDATION-YYYY-MM-DD-N] - Doc Claude Wellness Check FAILED
   Independent Score: XX/100
   Issues Found: [list]
   Recommended Actions: [list]
   ```

2. **Create validation report:**
   - Location: /docs/Validation/reports/YYYY-MM-DD_WELLNESS_CHECK_FAILED.md
   - Include: Full category breakdown, evidence, recommendations

3. **Flag for VALIDATION Claude:**
   - If discrepancy >5 points: VALIDATION Claude review required
   - If CRITICAL issues found: Immediate attention
   - If dashboard drift >3 points: Coordination gap investigation

4. **Update DASHBOARD.md:**
   - Correct to accurate score
   - Add warning notice
   - Note: "Under remediation"

### **If Dashboard Drift Detected (>±1 point)**

1. **Document drift:**
   - Claimed score
   - Actual score
   - Drift magnitude
   - Root cause analysis

2. **Update DASHBOARD.md immediately:**
   - Correct health score
   - Add drift correction notice
   - Update last validation date

3. **Create REPO_LOG entry:**
   - Category: [VALIDATION] [COORDINATION]
   - Document: What drifted, why, how corrected

4. **Prevention:**
   - Review: Why did dashboard and reality diverge?
   - Process: What prevented drift detection?
   - Future: How to catch earlier?

---

## 📋 REPORT TEMPLATE

When creating the wellness check report, use this structure:

```markdown
# Repository Wellness Check - [DATE]

**Performed by:** Doc Claude (Independent Assessment)
**Method:** 88MPH Protocol (Cold Start)
**Baseline:** [Previous health score] from [date]

---

## 🎯 EXECUTIVE SUMMARY

**Independent Score:** XX/100 [GREEN/YELLOW/RED]
**Dashboard Claim:** XX/100
**Discrepancy:** ±X points [PASS/FAIL]
**Confidence Level:** [HIGH/MEDIUM/LOW]
**Production Ready:** [YES/NO/CONDITIONAL]

---

## 📊 CATEGORY SCORES

### Structural Health (25 points possible)
**Score:** XX/25

**Evidence:**
- [Specific observations]

### Documentation Quality (25 points possible)
**Score:** XX/25

**Evidence:**
- [Specific observations]

### Link Integrity (20 points possible)
**Score:** XX/20

**Evidence:**
- [Specific observations]

### Process Compliance (20 points possible)
**Score:** XX/20

**Evidence:**
- [Specific observations]

### Coordination Health (10 points possible)
**Score:** XX/10

**Evidence:**
- [Specific observations]

---

## ✅ VALIDATION CHECKPOINTS

- [✅/❌] README coverage: XX%
- [✅/❌] Core header coverage: XX%
- [✅/❌] Archive naming: XX%
- [✅/❌] preset_calibration/README.md: [Complete/Incomplete]
- [✅/❌] Link integrity: XX%
- [✅/❌] REPO_LOG compliance: XX%
- [✅/❌] Dashboard accuracy: [Match/Drift]

---

## 🔍 DASHBOARD VERIFICATION

**Dashboard Claims:** XX/100
**Independent Assessment:** XX/100
**Discrepancy:** ±X points

**Analysis:**
[Why scores match or differ]

---

## 🚨 REMAINING ISSUES

**CRITICAL:** [count]
- [List any critical issues]

**IMPORTANT:** [count]
- [List any important issues]

**MINOR:** [count]
- [List any minor issues]

---

## 🏆 SIGN-OFF

**Production Ready:** [YES/NO/CONDITIONAL]

**Reasoning:**
[Detailed explanation of sign-off decision]

**Confidence Level:** [HIGH/MEDIUM/LOW]

**Recommended Actions:**
1. [Action 1]
2. [Action 2]
```

---

## 🔄 INTEGRATION WITH OTHER PROTOCOLS

### **88MPH_PROTOCOL.md**
- **Relationship:** This wellness protocol uses 88MPH methodology
- **When to use which:** 88MPH for rapid assessment, Wellness for independent validation
- **Complementary:** Use both together for comprehensive health monitoring

### **ROLE_VALIDATION.md**
- **Relationship:** Wellness protocol is Doc Claude self-check, VALIDATION Claude handles escalations
- **Escalation criteria:** Discrepancies >5 points, CRITICAL issues, dashboard drift >3 points
- **Handoff:** Wellness check creates report → VALIDATION Claude reviews → Actions taken

### **DASHBOARD.md**
- **Relationship:** Wellness protocol validates DASHBOARD.md accuracy
- **Update procedure:** If drift detected, wellness check provides corrected score
- **Maintenance:** Run wellness check before any dashboard health score updates

### **Health Reports**
- **Relationship:** Wellness check references latest health report as baseline
- **Output:** Wellness check creates new health report in /docs/repository/Health_Reports/
- **History:** Compare wellness checks over time to track repository health trajectory

---

## ✅ PROOF OF CONCEPT (2025-11-02)

**This protocol was validated by a fresh Doc Claude on 2025-11-02 with zero context:**

### **Setup:**
- Dashboard claimed: 95/100
- Baseline health: 94/100 (2025-10-31)
- Recent changes: Dashboard drift correction + 7 headers added

### **Results:**
- **Independent Score:** 96/100 🟢
- **Dashboard Claim:** 95/100 🟢
- **Discrepancy:** +1 point (within ±1 tolerance) ✅
- **Confidence Level:** HIGH ✅
- **All Checkpoints:** PASSED ✅
- **Production Ready:** YES ✅

### **Fresh Doc Claude's Verdict:**

> "Your repository is in exceptional health."
>
> "This repository demonstrates exceptional quality and is production-ready."
>
> "The repository is production-ready and operating at the top 1% of AI-assisted repositories globally."

### **What This Proves:**

✅ **Protocol works:** Fresh Claude with zero context validated everything
✅ **Methodology sound:** 88MPH scoring reproduced independently
✅ **Dashboard accurate:** Independent score matched claim (±1)
✅ **Self-healing capable:** System can validate itself without external help
✅ **Knowledge transfer:** Protocol enabled fresh Claude to assess confidently

**Translation:** The wellness protocol successfully enables Doc Claude to self-diagnose repository health with HIGH confidence and production-quality results.

---

## 📈 RECOMMENDED SCHEDULE

### **Required Wellness Checks:**
- **After major changes:** 50+ files modified
- **Before dashboard updates:** Always validate before claiming health score changes
- **Pre-deployment:** Before any production releases
- **Post-drift detection:** After any dashboard corrections

### **Recommended Wellness Checks:**
- **Monthly:** During active development
- **After sprints:** Multi-session work completed
- **Fresh Claude onboarding:** New Doc Claude validates current state
- **Quarterly:** Regular health monitoring

### **Optional Wellness Checks:**
- **Weekly:** During intensive development periods
- **After structural changes:** Major reorganization or refactoring
- **Multi-auditor work:** When several Claudes have contributed

---

## 🎯 SUCCESS METRICS

**Wellness check is successful when:**
- ✅ Independent score within ±1 point of dashboard claim
- ✅ Confidence level is HIGH
- ✅ All validation checkpoints pass
- ✅ No CRITICAL issues found
- ✅ Production readiness sign-off is YES
- ✅ Evidence cited for all category scores
- ✅ Baseline comparison shows trajectory

**Wellness check requires follow-up when:**
- ⚠️ Discrepancy >±1 point (investigate drift)
- ⚠️ Confidence level MEDIUM or LOW (methodology issues)
- ⚠️ Any validation checkpoints fail (fix required)
- ⚠️ CRITICAL or IMPORTANT issues found (prioritize fixes)
- ⚠️ Production sign-off is NO or CONDITIONAL (blockers remain)

---

## 💡 TIPS FOR EFFECTIVE WELLNESS CHECKS

**For Doc Claude running the check:**
1. **Start truly fresh:** Don't reference previous session context
2. **Be ruthlessly honest:** If dashboard claims 98 but evidence shows 95, report 95
3. **Cite everything:** Every claim needs file paths, line numbers, or validation reports
4. **Compare to baseline:** Show trajectory (improved/stable/degraded)
5. **Sign off clearly:** YES/NO/CONDITIONAL with reasoning

**For maintainers:**
1. **Trust the process:** If wellness check shows drift, dashboard was wrong
2. **Fix drift immediately:** Update dashboard to match independent assessment
3. **Investigate root causes:** Why did dashboard and reality diverge?
4. **Run after major work:** Don't wait for problems - proactive wellness checks
5. **Document everything:** REPO_LOG entries for every wellness check result

---

## 🔗 RELATED DOCUMENTATION

- **🔥 PROCESS CLAUDE (SME):** [ROLE_PROCESS.md](/docs/repository/librarian_tools/ROLE_PROCESS.md) ⭐ **CONSULT FIRST**
- **Protocol Reference:** [88MPH_PROTOCOL.md](/docs/repository/librarian_tools/88MPH_PROTOCOL.md)
- **Validation Role:** [ROLE_VALIDATION.md](/docs/repository/librarian_tools/ROLE_VALIDATION.md)
- **Dashboard:** [DASHBOARD.md](/docs/repository/DASHBOARD.md)
- **Health Reports:** [Health_Reports/](/docs/repository/Health_Reports/)
- **Validation Reports:** [reports/](/docs/Validation/reports/)

**💡 Pro Tip:** Don't read this entire 494-line protocol! Activate ROLE_PROCESS and consult Process Claude who is the wellness check expert. 5 minutes of consultation beats 20 minutes of protocol deep-dive.

---

**"Leave breadcrumbs. Future Claudes will thank you."** 🍞

**Protocol created:** 2025-11-02
**Validated by:** Fresh Doc Claude (cold start, 96/100 score, HIGH confidence)
**Status:** Production-ready, proven effective

---

**This protocol enables repository self-healing through independent validation.** ⚡
