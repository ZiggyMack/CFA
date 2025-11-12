# Workshop - Active Brainstorming & Development Sessions

**Purpose:** Dedicated space for multi-Claude brainstorming sessions (B-STORM), design discussions, and collaborative development
**Location:** `auditors/relay/workshop/`
**Archive:** Completed sessions move to `.Archive/workshop/`
**Status:** Active workspace

---

## 🎯 What This Directory Is For

**Workshop is the CFA brainstorming lab.**

This is where:
- **B-STORM sessions** happen (multi-Claude collaborative problem-solving)
- **Design specifications** get drafted (before moving to docs/)
- **Architecture debates** occur (exploring multiple approaches)
- **Proof-of-concepts** are sketched (before implementation)
- **Knowledge gaps** get identified and resolved

**Philosophy:** "Messy thinking → Clean documentation. Workshop explores, docs/ explains."

---

## 📋 Workshop Workflow

### **1. Active Sessions (Here)**
```
auditors/relay/workshop/
├── README.md              ← You are here
├── ARCHIVE_INDEX.md       ← Index of all archived sessions
├── B-STORM_8.md           ← Current active session (example)
├── DESIGN_SPEC_XYZ.md     ← Draft specifications
└── [other active work]    ← In-progress documents
```

**Rules for active sessions:**
- ✅ Keep files here while actively working
- ✅ Use descriptive names (B-STORM_N.md, DESIGN_SPEC_NAME.md)
- ✅ Iterate freely - workshop files can be messy
- ✅ Document decisions/outcomes at end of session

### **2. Archival (When Complete)**
```bash
# When session/design is complete:
mv auditors/relay/workshop/B-STORM_8.md auditors/.Archive/workshop/

# Update archive index:
# Edit workshop/ARCHIVE_INDEX.md to add new entry
```

**Archive when:**
- ✅ Session concluded (decisions made, no further discussion needed)
- ✅ Design spec finalized and moved to docs/ (keep workshop version as historical)
- ✅ POC completed or abandoned
- ✅ File exceeds ~50KB (large transcripts should be archived)

### **3. Retrieval (When Needed)**
```bash
# Search archived sessions:
grep -r "search term" auditors/.Archive/workshop/

# Read specific archived session:
cat auditors/.Archive/workshop/B-STORM_6.md

# Check archive index for summaries:
cat auditors/relay/workshop/ARCHIVE_INDEX.md
```

---

## 📚 Session Types

### **B-STORM Sessions (Brainstorming)**
**Format:** B-STORM_N.md where N = session number
**Purpose:** Multi-Claude collaborative problem-solving
**Typical length:** 15KB - 100KB (can get lengthy!)
**Example topics:**
- Architecture decisions (Crux vs. alternative approaches)
- Process refinements (VUDU protocol improvements)
- Repository optimization (directory structure debates)
- Mission planning (CT↔MdN pilot preparation)

**When to archive:** Session concluded, major decisions documented

---

### **Design Specifications (Drafts)**
**Format:** DESIGN_SPEC_[NAME].md
**Purpose:** Technical specifications before formal docs/
**Typical length:** 5KB - 20KB
**Example topics:**
- SMV visualization schema
- Calibration YAML format
- Hyperlink architecture
- Data pipeline structure

**When to archive:** Spec finalized and copied to docs/ (keep workshop version)

---

### **Knowledge Gap Resolution (KG/KD)**
**Format:** KG_[TOPIC].md or KD_[DECISION].md
**Purpose:** Document unresolved questions and their resolutions
**Typical length:** 2KB - 10KB
**Example topics:**
- KG: "How to handle circular profile dependencies?"
- KD: "Decision: Use calibration hashes instead of version numbers"

**When to archive:** Question resolved, decision documented

---

### **Proof-of-Concepts**
**Format:** POC_[NAME].md or PROTOTYPE_[NAME].md
**Purpose:** Experimental approaches before full implementation
**Typical length:** 5KB - 30KB
**Example topics:**
- Alternative scoring algorithms
- UI mockup proposals
- Data structure experiments

**When to archive:** POC validated/rejected, lessons learned documented

---

## 🔥 Current Active Sessions

**As of 2025-11-12:**
- *No active sessions* (B-STORM_7 completed and archived)

**Next likely session:**
- B-STORM_8: SMV Phase 2 planning (Nova co-design)
- Or: CT↔MdN pilot debrief session

---

## 📊 Archive Statistics

**Total archived sessions:** 21 files (616KB)
- B-STORM series: 7 sessions (446KB)
- Design specs: 5 files (89KB)
- Mockups/data: 9 files (81KB)

**Largest archived session:** B-STORM_6.md (109KB, ~20,000 words)

**See full archive index:** [ARCHIVE_INDEX.md](ARCHIVE_INDEX.md)

---

## ⚠️ Workshop Etiquette

### **DO:**
✅ **Iterate freely** - Workshop is for exploration, not perfection
✅ **Document outcomes** - End sessions with "Decisions Made" section
✅ **Use descriptive names** - Future you will thank present you
✅ **Archive when done** - Keep workshop/ focused on active work
✅ **Reference archived sessions** - Link to archive when relevant

### **DON'T:**
❌ **Leave sessions open forever** - Archive or delete stale work
❌ **Duplicate into docs/** without archiving - Creates sync issues
❌ **Delete without archiving** - History matters for context
❌ **Work directly in .Archive/** - Archive is read-only reference
❌ **Mix operational docs here** - Workshop ≠ relay coordination

---

## 🔗 Relationship to Other Directories

**Workshop vs. relay/ (parent):**
- **relay/:** Active coordination (MISSION_CURRENT.md, Claude_Incoming/)
- **workshop/:** Development/brainstorming (B-STORM, design specs)
- **Philosophy:** Coordination = current tasks, Workshop = future exploration

**Workshop vs. docs/:**
- **workshop/:** Draft specifications, messy thinking, experimental
- **docs/:** Final documentation, polished, canonical
- **Flow:** workshop/ → docs/ (finalize then publish)

**Workshop vs. .Archive/workshop/:**
- **.Archive/workshop/:** Completed sessions (read-only historical)
- **workshop/:** Active sessions (read-write work-in-progress)
- **Flow:** workshop/ → .Archive/workshop/ (when complete)

---

## 📋 Archive Index Location

**Full archive index:** [ARCHIVE_INDEX.md](ARCHIVE_INDEX.md)

**What's in the index:**
- List of all archived sessions with dates
- Brief summaries (what was decided)
- Key decisions from each B-STORM
- Quick reference without reading full transcripts

**Keep index updated** when archiving new sessions!

---

## 🎯 Success Metrics

**Workshop is working when:**
- ✅ Active sessions < 5 files (focused work-in-progress)
- ✅ Archive grows steadily (sessions being completed)
- ✅ Design specs graduate to docs/ (workshop → production)
- ✅ No files >100KB in active workshop (archive large transcripts)
- ✅ ARCHIVE_INDEX.md stays current (index updated with each archive)

**Workshop needs cleanup when:**
- ⚠️ Active sessions > 10 files (too much WIP)
- ⚠️ Files older than 30 days (stale work)
- ⚠️ Multiple files >50KB (should be archived)
- ⚠️ Duplicate files across workshop/ and docs/ (sync issues)

---

## 💡 Tips for Effective B-STORM Sessions

**Starting a new B-STORM:**
1. **Check last session number** in ARCHIVE_INDEX.md
2. **Create B-STORM_[N+1].md** (increment number)
3. **Start with context** (what problem are we solving?)
4. **Involve relevant Claudes** (Process, Doc, Review, Shaman, Nova, Grok as needed)

**During session:**
- **Capture raw dialogue** (don't over-edit)
- **Flag key decisions** with "🎯 DECISION:" markers
- **Note action items** with "⏭️ TODO:" markers
- **Link to relevant docs** (profiles, protocols, previous sessions)

**Concluding session:**
- **Add "Decisions Made" section** at end
- **List action items** (what needs to happen next)
- **Update related docs** if decisions impact them
- **Archive session** when complete
- **Update ARCHIVE_INDEX.md** with summary

---

## 🔄 Maintenance Protocol

### **Weekly Check (Every Monday):**
- [ ] Archive completed sessions from last week
- [ ] Update ARCHIVE_INDEX.md with new entries
- [ ] Review active sessions (any stale work?)
- [ ] Check for files >50KB (candidates for archival)

### **Monthly Review (First of Month):**
- [ ] Audit workshop/ for files older than 30 days
- [ ] Verify archive index is current
- [ ] Check if any design specs should graduate to docs/
- [ ] Clean up abandoned POCs

---

## 📖 Example B-STORM Session Structure

```markdown
# B-STORM_8 - SMV Phase 2 Planning

**Date:** 2025-11-XX
**Participants:** Process Claude (C4), Nova
**Topic:** SMV visualization Phase 2 design
**Status:** Active

---

## Context

[What problem are we solving? Why now?]

## Discussion

[Raw dialogue, exploration, alternatives considered]

### Key Points
- Point 1
- Point 2

### Alternatives Considered
- Option A: [description]
- Option B: [description]

## Decisions Made

🎯 **DECISION 1:** [What was decided]
- Rationale: [Why]
- Impact: [What changes]

🎯 **DECISION 2:** [Next decision]

## Action Items

⏭️ **TODO:** [Action item 1]
⏭️ **TODO:** [Action item 2]

## Next Steps

[What happens after this session?]

---

**Session closed:** 2025-11-XX
**Archived to:** .Archive/workshop/B-STORM_8.md
**Related docs:** [links to updated files]
```

---

## 🗂️ File Organization Best Practices

**Naming conventions:**
- B-STORM sessions: `B-STORM_N.md` (sequential numbers)
- Design specs: `DESIGN_SPEC_[NAME].md` (descriptive name)
- Knowledge gaps: `KG_[TOPIC].md` or `KD_[DECISION].md`
- POCs: `POC_[NAME].md` or `PROTOTYPE_[NAME].md`
- Supporting data: `[NAME]_DATA.json` or `[NAME]_MOCKUP.svg`

**When to create subdirectories:**
- ✅ Multiple related files (e.g., smv_mockups/ for SVG files)
- ✅ Data sets for specific topic (e.g., test_scenarios/)
- ❌ Single-file categories (creates unnecessary hierarchy)

---

## 🔗 Quick Links

**Active coordination:**
- [MISSION_CURRENT.md](../MISSION_CURRENT.md) - Current mission status
- [Claude_Incoming/](../Claude_Incoming/) - Active messages

**Related archives:**
- [.Archive/workshop/](../../.Archive/workshop/) - Archived sessions
- [ARCHIVE_INDEX.md](ARCHIVE_INDEX.md) - Session summaries

**Documentation:**
- [docs/](../../../docs/) - Finalized documentation
- [REPO_LOG.md](../../../REPO_LOG.md) - Repository changelog

---

**Established:** 2025-11-12
**Maintainer:** Any Claude conducting brainstorming sessions
**Philosophy:** "Workshop explores messy possibilities. Archive preserves decisions. Docs/ publishes truth."

**This is the way.** 🛠️
