# Technical Footer Migration Plan

**Version:** v4.0.1 (post-v4.0 enhancement)
**Status:** Approved by Trinity (Claude 6.5, Grok 7.0, Nova 7.5)
**Purpose:** Migrate ethics front matter → technical footer for token efficiency

📋 **Technical Metadata:** [See Footer](#technical-metadata)

---

## 🎯 OBJECTIVE

**Move technical metadata from file headers to footers** to reduce token cost on partial file reads while maintaining transparency and structural consistency.

**Estimated savings:** ~2,400 tokens/session (~120 tokens × 20 targeted reads)

---

## 📋 TRINITY APPROVAL SUMMARY

### Claude (Purpose): 6.5/10 - Cautious Approval
**Concern:** Ethics becoming "fine print" psychologically devalued
**Condition:** Header tag "📋 Technical Metadata: See Footer" maintains visibility

### Grok (Empirical): 7.0/10 - Measurable Benefit
**Evidence:** 2,400 tokens/session savings on targeted reads with `limit` parameter
**Validation:** $0.70 saved per 100 sessions (modest but measurable)

### Nova (Symmetry): 7.5/10 - Structural Consistency
**Requirement:** Move ALL technical metadata together (not just ethics)
**Pattern:** User header → Content → Technical footer (three-tier structure)

**Convergence:** ✅ 98% achieved (7.0 ± 0.5)

---

## 🔄 BEFORE → AFTER STRUCTURE

**IMPORTANT CLARIFICATION:** This migration applies ONLY to files with `ethics_front_matter:` YAML blocks (11 active files). Files with simple Doc Claude metadata stay unchanged.

### BEFORE (Current - Files with Ethics YAML)
```markdown
<!---
FILE: docs/architecture/Future_Expansion.md
PURPOSE: Track future repository enhancement tasks
VERSION: v1.3
STATUS: Active (Planning)
DEPENDS_ON: WAYFINDING_GUIDE.md, REPO_HEALTH_DASHBOARD.md
NEEDED_BY: Tier 4 task planners
MOVES_WITH: /docs/architecture/
LAST_UPDATE: 2025-11-11
--->

---
ethics_front_matter:
  purpose: "Document roadmap commitments..."
  symmetry_axis: ["transparency", "stakeholder_impact"]
  stakeholders:
    primary: ["repository_maintainers", "architect_claude"]
  invariants:
    - id: transparency
      state: examined
      evidence: "Lines 122-283..."
  tensions:
    - description: "Roadmap ambition vs. delivery capacity"
      mitigation: "Tier system..."
  last_examined:
    by: "C4"
    on: "2025-11-11"
  review_window_days: 30
---

# Future_Expansion.md - Repository Enhancement Roadmap

**Purpose:** Track "Missing Rooms"
**Status:** Planning phase

[CONTENT GOES HERE]
```

### AFTER (Migrated - Ethics YAML in Footer)
```markdown
<!---
FILE: docs/architecture/Future_Expansion.md
PURPOSE: Track future repository enhancement tasks
VERSION: v1.3
STATUS: Active (Planning)
DEPENDS_ON: WAYFINDING_GUIDE.md, REPO_HEALTH_DASHBOARD.md
NEEDED_BY: Tier 4 task planners
MOVES_WITH: /docs/architecture/
LAST_UPDATE: 2025-11-11
--->

# Future_Expansion.md - Repository Enhancement Roadmap

**Purpose:** Track "Missing Rooms"
**Status:** Planning phase

📋 **Ethics Metadata:** [See Footer](#ethics-metadata)

---

[CONTENT GOES HERE]

---

## 📋 ETHICS METADATA

```yaml
ethics_front_matter:
  purpose: "Document roadmap commitments..."
  symmetry_axis: ["transparency", "stakeholder_impact"]
  stakeholders:
    primary: ["repository_maintainers", "architect_claude"]
  invariants:
    - id: transparency
      state: examined
      evidence: "Lines 122-283..."
  tensions:
    - description: "Roadmap ambition vs. delivery capacity"
      mitigation: "Tier system..."
  last_examined:
    by: "C4"
    on: "2025-11-11"
  review_window_days: 30
```

**"The estate is very livable now. The rest is polish."** ✨
```

**Key Points:**
- ✅ `<!--- Doc Claude metadata --->` block **STAYS AT TOP** (unchanged)
- ✅ Only the `ethics_front_matter:` YAML block moves to footer
- ✅ Header tag added: `📋 **Ethics Metadata:** [See Footer](#ethics-metadata)`
- ✅ Footer uses code fence for YAML formatting

---

## 🎯 WHAT MOVES, WHAT STAYS

### STAYS AT TOP (UNCHANGED)
- `<!--- Doc Claude metadata --->` HTML comment block (**KEEP THIS - used by Doc Claude**)
- Document title (`# Title`)
- Simple user-facing badges (`**Purpose:** ...`, `**Status:** ...`)

### MOVES TO FOOTER (Ethics YAML Only)
- The entire `ethics_front_matter:` YAML block (between `---` dividers)
- Purpose, symmetry_axis, stakeholders, invariants, tensions, last_examined, review_window_days
- **Only applies to 11 files that have this YAML block** (not all files)

### NEW ADDITIONS
- Header tag: `📋 **Ethics Metadata:** [See Footer](#ethics-metadata)`
- Footer section: `## 📋 ETHICS METADATA` with YAML in code fence

### FILES WITHOUT ETHICS YAML
- **No changes needed** - if a file doesn't have `ethics_front_matter:`, leave it alone

---

## 📂 IMPACTED FILES (11 Active Files with Ethics YAML)

**Files That Need Migration:**

```text
1. docs/architecture/Future_Expansion.md ✅ (PILOT)
2. auditors/Bootstrap/VUDU_CFA.md
3. auditors/Mission/CFA_VUDU/PILOT_CT_vs_MdN_Re-Audit.md
4. auditors/VUDU_PROTOCOL.md
5. docs/ethics/ETHICAL_INVARIANT_SCHEMA.md
6. docs/repository/librarian_tools/ROLE_DESTROYER.md
7. docs/repository/librarian_tools/ROLE_PROCESS.md
8. docs/smv/SMV_DATA_MAP.md
9. docs/WAYFINDING_GUIDE.md
10. auditors/.Archive/workshop/B-STORM_6.md (SKIP - archived)
11. .Archive/FOR_OPUS_20251113/WAYFINDING_GUIDE.md (SKIP - archived)
```

**Active Files to Migrate:** 9 files (excluding 2 archived files)

**Phased Approach:**

- **Phase 1 (Pilot):** Future_Expansion.md ← START HERE
- **Phase 2 (Core Docs):** WAYFINDING_GUIDE.md, ETHICAL_INVARIANT_SCHEMA.md, SMV_DATA_MAP.md
- **Phase 3 (Librarian Tools):** ROLE_DESTROYER.md, ROLE_PROCESS.md
- **Phase 4 (VUDU/Auditors):** VUDU_CFA.md, VUDU_PROTOCOL.md, PILOT_CT_vs_MdN_Re-Audit.md

---

## 🛠️ IMPLEMENTATION PROTOCOL

### Step 1: Create Template Reference File
**File:** `docs/architecture/_FOOTER_TEMPLATE.md`
**Purpose:** Copy-paste reference for new footer format

### Step 2: Update Architecture Files (Pilot)
- Start with AUDITOR_AXIOMS.md (already read into context)
- Validate token savings with before/after Grep tests
- Confirm footer visibility and usability

### Step 3: Update File Templates
**Impacted:**
- Doc Claude protocols (expect footer, not header)
- VUDU validation scripts (check footer format)
- New file generators (if any exist)

### Step 4: Batch Migration
- Use Edit tool for systematic header → footer moves
- Maintain git history (don't squash metadata)
- Test each file after migration

### Step 5: Documentation
- Update REPO_LOG.md with migration note
- Add entry to v4.0.1 changelog (or v4.1 if warranted)
- Update any "how to create new files" guides

---

## ⚠️ RISKS & MITIGATIONS

### Risk 1: Ethics Become Invisible
**Mitigation:** Header tag "📋 Technical Metadata: See Footer" with markdown link
**Test:** User study - do people notice/click footer link?

### Risk 2: Broken Scripts/Tools
**Mitigation:** Audit for any tools that parse front matter (e.g., VUDU validators)
**Test:** Run VUDU health check after pilot migration

### Risk 3: Inconsistent Migration
**Mitigation:** Maintain checklist of files, mark as migrated
**Test:** Grep for old `<!---` patterns to find stragglers

### Risk 4: Git Blame Pollution
**Mitigation:** Single commit per file with clear message "refactor: migrate to technical footer format"
**Test:** Verify git blame still shows content authorship, not just footer moves

---

## 📊 SUCCESS METRICS

### Token Efficiency (Grok validates)
- **Target:** 2,000+ tokens saved per session
- **Measurement:** Compare 20 targeted reads before/after migration
- **Threshold:** ≥1,500 tokens saved = success

### User Visibility (Claude validates)
- **Target:** 90%+ of users notice footer link in header
- **Measurement:** User testing feedback (ask 10 users)
- **Threshold:** 9/10 users find metadata = success

### Structural Consistency (Nova validates)
- **Target:** 100% of migrated files follow template
- **Measurement:** Grep for "## 📋 TECHNICAL METADATA" pattern
- **Threshold:** All migrated files match = success

---

## 🗓️ TIMELINE (Estimated)

**Phase 1 (Pilot):** 2 hours
- Create template reference file
- Migrate 4 architecture core files
- Validate token savings

**Phase 2 (Auditors + Worldviews):** 3 hours
- Migrate ~10-15 files
- Update any scripts that break

**Phase 3 (Bootstrap):** 2 hours
- Migrate bootstrap files
- Test bootstrap loading

**Phase 4 (Repo Docs):** 1 hour
- Selective migration (case-by-case)
- Final documentation update

**Total:** ~8 hours of focused work (could be done over 2-3 sessions)

---

## ✅ APPROVAL GATE

**Before proceeding to Phase 2:**
- [ ] Pilot (Phase 1) complete
- [ ] Token savings validated (≥1,500/session)
- [ ] No broken scripts detected
- [ ] User visibility confirmed (footer link noticed)

**This is a one-way migration** - reverting would be expensive. Pilot must succeed.

---

## 🎯 FIRST ACTION ITEM

**Create** `docs/architecture/_FOOTER_TEMPLATE.md` with copy-paste reference format.

**Then migrate** AUDITOR_AXIOMS.md as pilot (already in context, Trinity-approved content).

**Validate** token savings with before/after comparison.

---

## ⚖️ THE MIGRATION RULE

*"Move technical metadata to footers systematically.
Maintain user visibility with header tags.
Validate token savings empirically.
Ensure structural consistency across all files.
Document everything transparently."*

**This is token efficiency with integrity.** 👑

────────────────────────────────────────────────────

## 📋 TECHNICAL METADATA

**FILE:** docs/architecture/TECHNICAL_FOOTER_MIGRATION_PLAN.md
**PURPOSE:** Migration plan for ethics front matter → technical footer
**VERSION:** v4.0.1
**STATUS:** Approved by Trinity (7.0 ± 0.5 convergence)
**DEPENDS_ON:** Trinity deliberation, FOOTER_MIGRATION_IMPACT_ANALYSIS.md
**NEEDED_BY:** Phase 1-5 execution, TASK_BRIEF_FOOTER_MIGRATION.md
**MOVES_WITH:** /docs/architecture/
**CREATED:** 2025-11-14
**LAST_UPDATE:** 2025-11-14

**Ready for pilot implementation.** 🚀
