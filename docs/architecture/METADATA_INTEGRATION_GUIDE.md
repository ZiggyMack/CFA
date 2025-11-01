# METADATA INTEGRATION GUIDE

**Version:** 1.0
**Date:** 2025-11-01
**Authority:** Nova Strategic Direction (Decision Record: `NOVA_STRATEGIC_DIRECTION_TASKS_4_5.md`)
**Status:** ACTIVE
**Scope:** All CFA repository files

---

## 🎯 PURPOSE

This guide documents the boundaries and integration strategy for CFA's three metadata systems:
1. **Semantic Headers** (FILE metadata)
2. **`<!-- deps: -->` Comments** (WHAT metadata - technical dependencies)
3. **YAML Front-matter** (WHY metadata - ethical invariants)

**Integration Approach:** **COMPLEMENTARY** (coexistence, not replacement or unification)

---

## 📊 METADATA SYSTEMS OVERVIEW

### **System 1: Semantic Headers**

**What It Captures:** FILE-level metadata
**Format:** HTML comment block at top of file
**Coverage:** Universal (all tracked files should have)
**Status:** Established standard (8-line format)

**Example:**
```markdown
<!---
FILE: example.md
PURPOSE: Demonstrate semantic header format
VERSION: 1.0
STATUS: Active
DEPENDS_ON: None
NEEDED_BY: Documentation readers
MOVES_WITH: /docs/examples/
LAST_UPDATE: 2025-11-01
--->
```

**Fields:**
- `FILE`: Filename
- `PURPOSE`: What this file does (single line)
- `VERSION`: Version number
- `STATUS`: Active/Archived/Deprecated
- `DEPENDS_ON`: Other files this file needs
- `NEEDED_BY`: Who/what needs this file
- `MOVES_WITH`: Directory affinity (where does this file belong)
- `LAST_UPDATE`: Last modification date

**Use Cases:**
- Quick file identification
- Dependency tracking at file level
- Version management
- Navigation (MOVES_WITH indicates logical grouping)

---

### **System 2: `<!-- deps: -->` Comments**

**What It Captures:** WHAT metadata - technical dependencies for code sections
**Format:** Inline HTML comment
**Coverage:** Partial (~40% of files, expanding organically)
**Status:** Recently deployed (VuDu v3.7.2)

**Example:**
```markdown
<!-- deps: authentication, database -->

## User Login Flow

This section describes how users authenticate...
```

**Fields:**
- Comma-separated list of technical dependencies
- Can appear multiple times in a file (section-level granularity)
- Lightweight (no schema required)

**Use Cases:**
- Technical dependency tracking (imports, modules, services)
- Section-level granularity (different parts of file may have different deps)
- Lightweight annotation (quick to add, easy to maintain)
- Enables automated dependency analysis

---

### **System 3: YAML Front-matter (NEW)**

**What It Captures:** WHY metadata - ethical invariants, purpose, stakeholders
**Format:** YAML block at top of file (after semantic header)
**Coverage:** Select Tier 1 files only (NOT repository-wide)
**Status:** Proposed (Nova approval, awaiting implementation)

**Example:**
```yaml
---
ethical_invariants:
  - never_allow_unexamined_purpose
  - transparency_and_accountability
purpose: |
  This file defines the bootstrap process for activating Claude instances.
  It ensures proper role understanding and mission alignment before work begins.
stakeholders:
  - Claude instances (activated via this protocol)
  - Ziggy (repository owner, coordination authority)
  - Future auditors (Grok, Nova - rely on proper Claude activation)
tensions:
  - Thoroughness vs Efficiency: Comprehensive bootstrap takes time, but prevents misalignment
  - Flexibility vs Structure: Templates guide but shouldn't constrain creative problem-solving
resolution: |
  Favor thoroughness over speed for bootstrap (one-time cost, long-term benefit).
  Provide templates as starting points, explicitly allow adaptation with reasoning.
---
```

**Fields:**
- `ethical_invariants`: Which AXIOMS.md principles apply to this file
- `purpose`: WHY this file exists (multi-line, detailed explanation)
- `stakeholders`: WHO is affected by this code/documentation
- `tensions`: Competing concerns or trade-offs present in this file
- `resolution`: HOW tensions are balanced or addressed

**Use Cases:**
- Ethical oversight (what principles guide this file's content)
- Purpose tracking (WHY not just WHAT)
- Stakeholder awareness (who cares about changes to this file)
- Tension documentation (what trade-offs were considered)
- Symmetry Matrix Visualizer input (feeds SMV for pattern analysis)

---

## 🧭 WHEN TO USE WHICH SYSTEM

### **Decision Tree:**

```
Is this about the FILE itself (name, version, location)?
├─ YES → Use Semantic Header
└─ NO ↓

Is this about WHAT this code/section depends on technically?
├─ YES → Use <!-- deps: --> comment
└─ NO ↓

Is this about WHY this file exists or what ethical principles apply?
├─ YES → Use YAML front-matter (Tier 1 files only)
└─ NO → Metadata may not be needed
```

---

### **Use Case Matrix:**

| Question | System to Use | Example |
|----------|---------------|---------|
| What is this file called? | Semantic Header (`FILE`) | `FILE: BOOTSTRAP_CLAUDE.md` |
| What version is this? | Semantic Header (`VERSION`) | `VERSION: 2.1` |
| Where does this file belong? | Semantic Header (`MOVES_WITH`) | `MOVES_WITH: /auditors/Bootstrap/` |
| What files does this depend on? | Semantic Header (`DEPENDS_ON`) | `DEPENDS_ON: BOOTSTRAP_CFA.md, AXIOMS.md` |
| What technical systems does this section use? | `<!-- deps: -->` | `<!-- deps: authentication, database -->` |
| What imports does this code need? | `<!-- deps: -->` | `<!-- deps: vudu_protocol, task_handler -->` |
| Why does this file exist? | YAML (`purpose`) | `purpose: Activate Claude with mission understanding` |
| What ethical principles apply? | YAML (`ethical_invariants`) | `ethical_invariants: [never_allow_unexamined_purpose]` |
| Who is affected by this code? | YAML (`stakeholders`) | `stakeholders: [Claude instances, Ziggy]` |
| What trade-offs are present? | YAML (`tensions`, `resolution`) | `tensions: Thoroughness vs Efficiency` |

---

## 🔄 SYSTEM RELATIONSHIPS

### **Complementary, Not Redundant:**

**Semantic Header ↔ deps Comments:**
- Header `DEPENDS_ON`: File-level dependencies (other files)
- deps comment: Section-level dependencies (technical systems, modules)
- **No overlap:** Different granularities, different purposes

**Semantic Header ↔ YAML Front-matter:**
- Header `PURPOSE`: Brief one-line WHAT (e.g., "Bootstrap protocol for Claude activation")
- YAML `purpose`: Detailed multi-line WHY (e.g., "This file exists to ensure proper role understanding and mission alignment before work begins, preventing misalignment that could compromise mission integrity...")
- **No overlap:** Brief vs detailed, WHAT vs WHY

**deps Comments ↔ YAML Front-matter:**
- deps: WHAT technical dependencies (authentication, database)
- YAML: WHY ethical dependencies (which AXIOMS.md principles)
- **No overlap:** Technical vs ethical, WHAT vs WHY

---

### **Integration Points:**

**Symmetry Matrix Visualizer (SMV) ← YAML Front-matter:**
- SMV reads YAML ethical invariant data
- Visualizes tensions and resolutions
- Patterns emerge from aggregated YAML metadata

**Dependency Mapping ← Semantic Headers + deps:**
- File-level map uses header `DEPENDS_ON` and `NEEDED_BY`
- Section-level map uses deps comments
- Combined view shows complete dependency graph

**Linter (Future) ← YAML Front-matter:**
- Pre-commit linter validates YAML schema
- Warns if ethical_invariants missing on Tier 1 files
- Warns if tensions unaddressed
- **NEVER blocks:** Warn-only mode (human authority preserved)

---

## 📋 SCOPE BOUNDARIES

### **Semantic Headers:**

**Scope:** ALL tracked files in repository

**Mandatory:** YES (established standard)

**Exceptions:**
- Generated files (build artifacts, temp files)
- External dependencies (vendor/, node_modules/)
- Binary files (images, zips - where applicable via companion .md file)

---

### **`<!-- deps: -->` Comments:**

**Scope:** Files with technical dependencies

**Mandatory:** NO (organic adoption, ~40% current coverage)

**When to Add:**
- File has technical dependencies (imports, services, modules)
- Section needs dependency annotation (different parts have different deps)
- Dependency tracking would aid understanding

**When to Skip:**
- File has no technical dependencies
- Dependencies are obvious from context
- File is simple standalone documentation

**Growth Strategy:** Organic (add when useful, not forced compliance)

---

### **YAML Front-matter:**

**Scope:** **SELECT TIER 1 FILES ONLY**

**Mandatory:** NO (select files, not repository-wide)

**When to Add:**
- File is Tier 1 (infrastructure, protocols, mission-critical)
- File involves ethical considerations or trade-offs
- File affects multiple stakeholders
- File would benefit from symmetry lens analysis

**Examples of Tier 1 Files:**
- `/docs/AXIOMS.md` (ethical invariants source)
- `/auditors/VUDU_PROTOCOL.md` (coordination protocol)
- `/auditors/Bootstrap/BOOTSTRAP_CLAUDE.md` (activation protocol)
- `/docs/repository/librarian_tools/88MPH_PROTOCOL.md` (role definitions)
- Files in `/docs/decisions/` (architectural decisions)

**When to Skip:**
- Tier 4 task-specific files (focused, single-purpose)
- Simple documentation or examples
- Generated or temporary files
- Files without ethical dimensions or stakeholder impact

**Growth Strategy:** Curated (thoughtful selection, not bulk deployment)

**Target Coverage:** ~10-20 files initially (core Tier 1), expand deliberately based on SMV insights

---

## 🚀 MIGRATION STRATEGY

### **Migration Approach: NONE**

**Rationale:**
- Systems are complementary, not replacement
- No need to migrate from one system to another
- Existing coverage preserved (semantic headers, deps comments)

---

### **Adoption Strategy: ADDITIVE**

**Phase 1: Establish YAML on Select Tier 1 Files (Manual)**
1. Identify 5-10 core Tier 1 files
2. Manually add YAML front-matter with ethical invariant data
3. Collect feedback (Nova, Claude, Ziggy)
4. Refine schema based on real-world usage
5. Duration: 2-3 days (part of Task #4 Phase 1)

**Phase 2: Build Warn-only Linter (Conditional)**
1. Build linter IF Phase 1 validates usefulness
2. Implement `--warn-only` mode as default
3. Linter checks: YAML schema validity, required fields present
4. Document override procedures (legitimate edge cases)
5. Duration: 2-3 days (part of Task #4 Phase 2)

**Phase 3: Organic Growth (Future)**
1. Add YAML to additional Tier 1 files as needed
2. Use SMV insights to guide selection (which files benefit most)
3. Periodic review: Is YAML coverage appropriate or excessive?
4. Defer enforcement mode (blocking) until data justifies

**No Mass Migration:** Never bulk-convert files. Thoughtful curation only.

---

## 🛠️ PRACTICAL EXAMPLES

### **Example 1: Simple Documentation File**

**File:** `/docs/examples/EXAMPLE_SIMPLE.md`

**Metadata Applied:**

```markdown
<!---
FILE: EXAMPLE_SIMPLE.md
PURPOSE: Demonstrate simple documentation structure
VERSION: 1.0
STATUS: Active
DEPENDS_ON: None
NEEDED_BY: Documentation readers
MOVES_WITH: /docs/examples/
LAST_UPDATE: 2025-11-01
--->

# Simple Example

This is a simple documentation file with no technical dependencies or ethical dimensions.
```

**Systems Used:**
- ✅ Semantic Header (file-level metadata)
- ❌ deps comments (no technical dependencies)
- ❌ YAML front-matter (not Tier 1, no ethical dimensions)

---

### **Example 2: Technical Documentation with Dependencies**

**File:** `/docs/architecture/AUTHENTICATION_FLOW.md`

**Metadata Applied:**

```markdown
<!---
FILE: AUTHENTICATION_FLOW.md
PURPOSE: Document user authentication architecture
VERSION: 2.0
STATUS: Active
DEPENDS_ON: DATABASE_SCHEMA.md, API_ENDPOINTS.md
NEEDED_BY: Backend developers, security auditors
MOVES_WITH: /docs/architecture/
LAST_UPDATE: 2025-11-01
--->

# Authentication Flow

<!-- deps: authentication_service, user_database, session_manager -->

## Overview

The authentication system uses JWT tokens for session management...

<!-- deps: jwt_library, crypto -->

## Token Generation

Tokens are generated using the crypto library...
```

**Systems Used:**
- ✅ Semantic Header (file-level metadata)
- ✅ deps comments (technical dependencies at section level)
- ❌ YAML front-matter (not Tier 1, technical not ethical)

---

### **Example 3: Tier 1 Infrastructure File with Ethical Dimensions**

**File:** `/auditors/Bootstrap/BOOTSTRAP_CLAUDE.md`

**Metadata Applied:**

```markdown
<!---
FILE: BOOTSTRAP_CLAUDE.md
PURPOSE: Bootstrap protocol for Claude instance activation
VERSION: 3.0
STATUS: Active
DEPENDS_ON: BOOTSTRAP_CFA.md, AXIOMS.md, VUDU_PROTOCOL.md
NEEDED_BY: All Claude instances, Ziggy, external auditors
MOVES_WITH: /auditors/Bootstrap/
LAST_UPDATE: 2025-11-01
--->

---
ethical_invariants:
  - never_allow_unexamined_purpose
  - transparency_and_accountability
  - preserve_institutional_memory
purpose: |
  This file defines the bootstrap process for activating Claude instances with proper
  mission understanding. It ensures Claude reads foundational documents (AXIOMS.md,
  CFA_README.md, VUDU_PROTOCOL.md) before beginning work, preventing misalignment that
  could compromise mission integrity.
stakeholders:
  - Claude instances: Rely on this for proper activation and role understanding
  - Ziggy: Needs confidence that Claude understands mission before delegating work
  - Future auditors (Grok, Nova): Depend on proper Claude activation for coordination
  - Repository integrity: Misaligned Claude could damage institutional memory
tensions:
  - Thoroughness vs Efficiency: Comprehensive bootstrap takes time but prevents costly misalignment
  - Flexibility vs Structure: Templates guide but shouldn't constrain creative problem-solving
  - Trust vs Verification: VuDu culture is trust-based, but bootstrap ensures baseline understanding
resolution: |
  Favor thoroughness over speed for bootstrap (one-time cost, long-term benefit).
  Provide templates as starting points, explicitly allow adaptation with documented reasoning.
  Trust-based culture preserved: Bootstrap establishes shared understanding, not rigid compliance.
---

<!-- deps: vudu_protocol, bootstrap_templates, axioms -->

# Bootstrap Protocol for Claude

## Purpose

This protocol ensures Claude instances begin work with proper mission understanding...
```

**Systems Used:**
- ✅ Semantic Header (file-level metadata)
- ✅ YAML front-matter (Tier 1, ethical dimensions, stakeholder impact)
- ✅ deps comments (technical dependencies for specific sections)

**Rationale for Full Metadata:**
- Tier 1 infrastructure file (bootstrap affects all future work)
- Ethical dimensions (proper activation prevents misalignment)
- Multiple stakeholders (Claude, Ziggy, auditors, repository)
- Tensions present (thoroughness vs efficiency, flexibility vs structure)
- Technical dependencies (vudu_protocol, templates, axioms)

---

## ⚠️ ANTI-PATTERNS TO AVOID

### **❌ Anti-Pattern #1: Redundant Information**

**Bad Example:**
```markdown
<!---
PURPOSE: Bootstrap protocol for Claude activation
--->

---
purpose: Bootstrap protocol for Claude activation
---
```

**Problem:** Exact duplication between semantic header and YAML

**Correct Approach:**
```markdown
<!---
PURPOSE: Bootstrap protocol for Claude activation
--->

---
purpose: |
  This file exists to ensure proper role understanding and mission alignment before work begins.
  It prevents misalignment by requiring Claude to read foundational documents (AXIOMS.md, CFA_README.md)
  before accepting task assignments. Without this protocol, Claude might execute tasks without
  understanding mission context, potentially damaging institutional memory or violating ethical principles.
---
```

**Fix:** Semantic header has brief WHAT, YAML has detailed WHY

---

### **❌ Anti-Pattern #2: YAML on Every File**

**Bad Example:**
```markdown
# TODO List

- [ ] Buy milk
- [ ] Review PR #15
```

**If someone adds:**
```yaml
---
ethical_invariants:
  - never_allow_unexamined_purpose
purpose: This is a todo list
stakeholders: [Ziggy]
---
```

**Problem:** YAML adds no value here (simple file, no ethical dimensions, obvious purpose)

**Correct Approach:** No YAML front-matter (use semantic header only if needed)

---

### **❌ Anti-Pattern #3: Mixing System Purposes**

**Bad Example:**
```markdown
<!-- deps: transparency, accountability -->

## Mission Statement

Our mission is to maintain transparency and accountability...
```

**Problem:** Using deps system for ethical concepts (not technical dependencies)

**Correct Approach:**
```yaml
---
ethical_invariants:
  - transparency_and_accountability
---

## Mission Statement

Our mission is to maintain transparency and accountability...
```

**Fix:** deps for WHAT (technical), YAML for WHY (ethical)

---

### **❌ Anti-Pattern #4: Incomplete YAML**

**Bad Example:**
```yaml
---
ethical_invariants:
  - never_allow_unexamined_purpose
---
```

**Problem:** Missing required fields (purpose, stakeholders, tensions)

**Correct Approach:** If file warrants YAML, complete the schema:
```yaml
---
ethical_invariants:
  - never_allow_unexamined_purpose
purpose: |
  [WHY this file exists and its mission importance]
stakeholders:
  - [Who is affected by this file]
tensions:
  - [What trade-offs are present]
resolution: |
  [How tensions are addressed]
---
```

**Fix:** Complete schema or don't use YAML (partial metadata is confusing)

---

## 🎯 VALIDATION & ENFORCEMENT

### **Semantic Headers:**

**Validation:** Manual review during REVIEW Claude assessments

**Enforcement:** Social norm (expected standard, not forced compliance)

**Tools:** None currently (could build linter if needed)

---

### **`<!-- deps: -->` Comments:**

**Validation:** Organic (users add when useful)

**Enforcement:** NONE (opt-in system, grows naturally)

**Tools:** Dependency mapping tools can read and visualize

---

### **YAML Front-matter:**

**Validation:**
- Phase 1: Manual review (Nova/Claude feedback on select files)
- Phase 2: Warn-only linter (if Phase 1 validates usefulness)

**Enforcement:**
- **NEVER blocking** (warn-only mode preserves human authority)
- Periodic adversarial audits (Nova/Claude review) remain final authority
- Developers can override for legitimate edge cases

**Tools:**
- Warn-only linter (Task #4 Phase 2, conditional on Phase 1 success)
- Symmetry Matrix Visualizer (Task #5, consumes YAML data)

---

## 📚 SCHEMA SPECIFICATIONS

### **Semantic Header Schema:**

**Format:** HTML comment block, 8 required fields

**Required Fields:**
```
FILE: [filename]
PURPOSE: [one-line description]
VERSION: [semantic version]
STATUS: [Active|Archived|Deprecated]
DEPENDS_ON: [comma-separated file list or "None"]
NEEDED_BY: [who/what needs this file]
MOVES_WITH: [directory path]
LAST_UPDATE: [YYYY-MM-DD]
```

**Optionaladditional fields allowed but not required**

---

### **deps Comment Schema:**

**Format:** HTML comment, comma-separated list

**Syntax:**
```markdown
<!-- deps: dependency1, dependency2, dependency3 -->
```

**Rules:**
- Can appear multiple times in file (section-level)
- Lowercase, underscore_separated naming preferred
- No strict schema (flexible by design)

---

### **YAML Front-matter Schema:**

**Format:** YAML block between `---` delimiters

**Required Fields:**
```yaml
---
ethical_invariants:
  - invariant1  # From AXIOMS.md
  - invariant2
purpose: |
  Multi-line string explaining WHY this file exists
stakeholders:
  - stakeholder1: Description of their interest
  - stakeholder2: Description of their interest
tensions:
  - Tension description (competing concerns)
resolution: |
  How tensions are balanced or addressed
---
```

**Optional Fields:**
```yaml
metadata_version: "1.0"  # Schema version (for future evolution)
last_reviewed_by: "Nova"  # Who last reviewed ethical dimensions
review_date: "2025-11-01"  # When last reviewed
```

**Validation Rules:**
- All required fields must be present
- `ethical_invariants` must reference AXIOMS.md principles
- `purpose` must be substantive (not just filename restatement)
- `stakeholders` must include at least one entry
- `tensions` and `resolution` can be "None identified" if truly absent

---

## 🔄 EVOLUTION & MAINTENANCE

### **When to Update This Guide:**

1. New metadata system introduced
2. Existing system scope changes (e.g., YAML expands beyond Tier 1)
3. Schema evolution (new required fields)
4. Integration patterns discovered (new use cases)
5. Anti-patterns identified (add to warnings)

**Maintainer:** DOC_CLAUDE (Repo Librarian)
**Review Frequency:** After major metadata-related changes
**Version Control:** Track updates in REPO_LOG.md

---

### **Future Considerations:**

**Potential Evolution:**
- Automated dependency visualization (combine semantic headers + deps)
- YAML coverage expansion (if SMV demonstrates value)
- Schema versioning (metadata_version field for backward compatibility)
- Enforcement mode for linter (only if data justifies, defer decision)

**Guiding Principles for Evolution:**
- Additive, not breaking (preserve existing work)
- Value-driven (only expand if proven useful)
- Human-centric (automation serves, doesn't replace)
- Complementary (avoid redundancy, maintain distinct purposes)

---

## ⚖️ PHILOSOPHICAL FOUNDATION

### **Nova's Anchor (Applied to Metadata):**

> "Symmetry thrives in dialogue, not dictation.
> The tools should reveal patterns, not police them.
> Automation serves reflection; reflection preserves meaning.
> Let understanding precede control."

**Application:**

**"Symmetry thrives in dialogue":**
- Three systems coexist (dialogue) rather than one unified system (dictation)
- Each serves distinct purpose (complementary dialogue)
- Users choose which system fits their need (collaborative, not mandated)

**"Tools should reveal patterns":**
- deps reveals technical dependency patterns
- YAML reveals ethical consideration patterns
- SMV reveals symmetry patterns from YAML data
- None police compliance (all inform understanding)

**"Automation serves reflection":**
- Linter warns (serves reflection) not blocks (replaces judgment)
- SMV visualizes (serves reflection) not enforces (dictates compliance)
- Metadata enables human reflection on dependencies, purpose, ethics

**"Let understanding precede control":**
- Phase 1 manual annotation (understand use case) before Phase 2 linter (control)
- Organic deps growth (understand value) before any enforcement
- Visualization (SMV understanding) before enforcement (linter control)

---

## 📋 QUICK REFERENCE

### **Which System When:**

| Scenario | Use This System |
|----------|----------------|
| "What is this file?" | Semantic Header |
| "What version is this?" | Semantic Header |
| "Where does this belong?" | Semantic Header (`MOVES_WITH`) |
| "What files does this need?" | Semantic Header (`DEPENDS_ON`) |
| "What modules does this section use?" | `<!-- deps: -->` |
| "What services does this call?" | `<!-- deps: -->` |
| "Why does this file exist?" | YAML (`purpose`) - Tier 1 only |
| "What ethical principles apply?" | YAML (`ethical_invariants`) - Tier 1 only |
| "Who cares about this file?" | YAML (`stakeholders`) - Tier 1 only |
| "What trade-offs are present?" | YAML (`tensions`, `resolution`) - Tier 1 only |

---

### **Coverage Quick Check:**

| System | Coverage | Mandatory? | Growth Strategy |
|--------|----------|------------|----------------|
| Semantic Headers | Universal | YES | Standard for all files |
| `<!-- deps: -->` | ~40%, growing | NO | Organic (add when useful) |
| YAML Front-matter | Select Tier 1 only | NO | Curated (10-20 files initially) |

---

**Guide Status:** ✅ ACTIVE
**Authority:** Nova Strategic Direction (2025-11-01)
**Next Review:** After Task #4 Phase 1 complete (manual YAML annotation feedback)

---

**This is the way.** 🔥
