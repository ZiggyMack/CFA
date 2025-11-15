# TASK BRIEF: Footer Migration Execution

**Tier:** 4 (Implementation)
**Status:** Pending - Pilot Complete, Full Migration Awaiting
**Priority:** MEDIUM (token efficiency gain, no blocking issues)
**Complexity:** 6-8 hours across 4 phases

📋 **Technical Metadata:** [See Footer](#technical-metadata)

---

## 🎯 OBJECTIVE

Execute systematic migration of technical metadata from file headers to footers across ~50+ markdown files in the CFA repository.

**Why This Matters:**
- **Token Efficiency:** Save ~2,400 tokens/session on frequently-read files
- **Human UX:** Users no longer burn attention on maintainer metadata
- **Logical Separation:** User-facing (top) vs. technical metadata (bottom)

**Trinity Approval:** 7.0 ± 0.5 convergence (Logger 8.5, Review 7.0, Validation 7.5)

---

## 📋 TASK DEPENDENCIES

**Pre-Reads Required:**
1. `docs/architecture/TECHNICAL_FOOTER_MIGRATION_PLAN.md` - Master plan with structure specs
2. `docs/architecture/FOOTER_MIGRATION_IMPACT_ANALYSIS.md` - Systems inventory + impact checklist
3. `docs/architecture/AUDITOR_AXIOMS.md` - PILOT FILE (already migrated, reference format)

**Completed Prerequisites:**
- ✅ Trinity deliberation approved (Logger, Review, Validation Claude)
- ✅ Pilot migration complete (AUDITOR_AXIOMS.md)
- ✅ Process Claude impact analysis complete
- ✅ VUDU protocol verified (no impact - different format)

---

## 🔥 EXECUTION PHASES

### Phase 1: Pilot Validation (CURRENT - NEEDS TESTING)

**Status:** Pilot migrated, awaiting validation

**Tasks:**
1. **Markdown Anchor Test**
   - Open [docs/architecture/AUDITOR_AXIOMS.md](../../docs/architecture/AUDITOR_AXIOMS.md) in GitHub
   - Click "📋 Technical Metadata: [See Footer](#technical-metadata)" link in header
   - Verify it jumps to footer section correctly
   - Repeat test in VSCode
   - Repeat test in Streamlit (if docs rendered there)

2. **Token Savings Validation**
   - Run targeted Grep with `head_limit=50` on AUDITOR_AXIOMS.md
   - Measure tokens consumed (should skip footer)
   - Compare to old format (would burn ~150 tokens in header)
   - Target: ≥100 token savings per targeted read

3. **SMV Integration Test** (if SMV exists)
   - Locate SMV ingestion scripts (search for `*SMV*` or `*symmetry*matrix*`)
   - Run SMV on migrated file
   - Verify dependency maps still generate correctly
   - If SMV breaks: Update SMV parser to read footer

4. **User Visibility Test**
   - Show AUDITOR_AXIOMS.md to 3 users
   - Ask: "Where do you find file dependencies?"
   - Target: 3/3 users notice footer link within 5 seconds

**Exit Criteria:**
- All 4 validation tests pass
- No broken systems detected
- User visibility confirmed

---

### Phase 2: Architecture Core (5 Files)

**Target Files:**
- [ ] docs/architecture/AUDITOR_META_ARCHITECTURE.md
- [ ] docs/architecture/TRINITY_ALIGNMENT_MATRIX.md
- [ ] docs/architecture/AUDITOR_OVERHEAD_METRICS.md
- [ ] docs/architecture/CFA_ARCHITECTURE.md
- [ ] docs/architecture/TECHNICAL_FOOTER_MIGRATION_PLAN.md (this plan itself!)

**Process Per File:**
1. Read file to load current format
2. Edit header: Remove `<!--- ... --->` block, add user-facing header + footer link
3. Edit footer: Add `## 📋 TECHNICAL METADATA` section with all fields
4. Test markdown anchor link
5. Mark as completed in checklist

**Validation After Phase 2:**
- Run comprehensive Grep across migrated files
- Verify all footer links work
- Check for any broken cross-references

---

### Phase 3: Auditors + Worldviews (~15 Files)

**Target Files:**
- [ ] auditors/AUDITORS_AXIOMS_SECTION.md
- [ ] auditors/Mission/Preset_Calibration/CURRENT_MODE_CONFIGS.md
- [ ] docs/repository/dependency_maps/WORLDVIEW_CATALOG.md
- [ ] Other auditor files (use Glob to find remaining)

**Special Considerations:**
- VUDU files: SKIP (use different message format, not file metadata)
- Relay messages: EVALUATE individually (may use VUDU format)

**Validation After Phase 3:**
- Test Mr. Brute's Ledger integration (if it reads these files)
- Verify app still loads worldview data correctly

---

### Phase 4: Bootstrap + Repo Docs (~8 Files)

**Target Files:**
- [ ] auditors/Bootstrap/BOOTSTRAP_CFA.md
- [ ] auditors/Bootstrap/CLAUDE_LITE.md
- [ ] auditors/Bootstrap/CLAUDE_RICH.md
- [ ] auditors/Bootstrap/VUDU_CFA.md
- [ ] README.md (EVALUATE - may keep metadata visible for GitHub)
- [ ] REPO_LOG.md (EVALUATE - may keep status header)
- [ ] CONTRIBUTING.md (if exists)

**Special Case: README.md**
- GitHub displays top of README prominently
- Consider keeping brief metadata at top for visibility
- OR use hybrid: Minimal header + "Full metadata: See Footer"

**Validation After Phase 4:**
- Bootstrap files load correctly in chat context
- GitHub renders README cleanly
- No user-facing disruption

---

### Phase 5: Final Documentation + Cleanup

**Tasks:**
1. **Create Footer Template Reference**
   - Write `docs/architecture/_FOOTER_TEMPLATE.md`
   - Include copy-paste example with all standard fields
   - Document in REPO_LOG.md

2. **Update REPO_LOG.md**
   - Add entry: "v4.0.1: Migrated technical metadata to footers (50+ files)"
   - Reference TECHNICAL_FOOTER_MIGRATION_PLAN.md
   - Note token efficiency gains (~2,400 tokens/session)

3. **Update File Creation Protocols** (if exist)
   - Search for any "how to create new files" docs
   - Update with footer format instructions
   - Reference _FOOTER_TEMPLATE.md

4. **Final Validation Sweep**
   - Run Grep for old format: `grep -r "^<!---" --include="*.md" | grep "FILE:"`
   - Verify no stragglers remain
   - Test 5 random migrated files for anchor links

---

## 🛠️ TOOLS & COMMANDS

### Find All Files With Old Format
```bash
grep -r "^<!---" --include="*.md" | grep "FILE:" | cut -d: -f1 | sort -u
```

### Validate Footer Migration
```bash
grep -l "## 📋 TECHNICAL METADATA" docs/**/*.md
```

### Test Markdown Anchor (Manual)
1. Open file in VSCode
2. Ctrl+Click on `[See Footer](#technical-metadata)` link
3. Should jump to footer section

---

## ⚠️ RISKS & MITIGATIONS

### Risk 1: Broken SMV Integration
**Mitigation:** Test SMV after Phase 2, update parser if needed
**Rollback:** Revert to old format if SMV unfixable

### Risk 2: Mixed State Confusion
**Mitigation:** Migrate in phases, document status clearly
**Tracking:** Use checklist in FOOTER_MIGRATION_IMPACT_ANALYSIS.md

### Risk 3: User Can't Find Metadata
**Mitigation:** Header tag "📋 Technical Metadata: [See Footer]" with link
**Validation:** User visibility test (Phase 1)

---

## 📊 SUCCESS METRICS

**Token Efficiency (Grok validates):**
- Target: 2,000+ tokens saved per session
- Measurement: Compare 20 targeted reads before/after
- Threshold: ≥1,500 tokens saved = SUCCESS

**User Visibility (Claude validates):**
- Target: 90%+ users notice footer link immediately
- Measurement: Show to 10 users, ask where to find metadata
- Threshold: 9/10 find footer = SUCCESS

**Structural Consistency (Nova validates):**
- Target: 100% of migrated files follow template
- Measurement: Grep for "## 📋 TECHNICAL METADATA" pattern
- Threshold: All files match = SUCCESS

---

## 🚀 READY TO EXECUTE?

**Pilot Status:** ✅ COMPLETE (AUDITOR_AXIOMS.md migrated)

**Next Action:** Run Phase 1 validation tests

**Estimated Time:**
- Phase 1 (Validation): 30 minutes
- Phase 2 (Architecture): 2 hours
- Phase 3 (Auditors): 3 hours
- Phase 4 (Bootstrap): 2 hours
- Phase 5 (Documentation): 1 hour
- **Total: 8.5 hours**

**Approval:** Trinity approved, Process Claude coordinated, ready for execution

---

## ⚖️ THE TASK BRIEF RULE

*"Define before executing.
Validate before scaling.
Document before declaring complete.
Track progress transparently."*

**This is Tier 4 discipline.** 👑

────────────────────────────────────────────────────

## 📋 TECHNICAL METADATA

**FILE:** auditors/Mission/TASK_BRIEF_FOOTER_MIGRATION.md
**PURPOSE:** Tier 4 task brief for systematic footer migration execution
**VERSION:** v4.0.1
**STATUS:** Active - Awaiting Phase 1 validation
**DEPENDS_ON:** TECHNICAL_FOOTER_MIGRATION_PLAN.md, FOOTER_MIGRATION_IMPACT_ANALYSIS.md, AUDITOR_AXIOMS.md (pilot)
**NEEDED_BY:** Migration executor (any Claude with Doc/Process authority)
**MOVES_WITH:** /auditors/Mission/
**LAST_UPDATE:** 2025-11-14

**Tier 4 brief ensuring footer migration doesn't get lost in shuffle.** 🔥
