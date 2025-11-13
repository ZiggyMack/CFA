<!-- deps: file_structure, documentation -->
# UNIVERSAL FILE HEADER STANDARD v1.0

**Purpose:** Enable instant file understanding and dependency mapping  
**Benefit:** 90% comprehension from 5% of file content  
**Implementation:** Gradual rollout as files are touched  
**Created:** 2025-10-30 by DOC_CLAUDE (formerly README_Claude)  

---

## 🎯 **THE PROBLEM**

Currently, to understand a file's role and dependencies, I must:
- Read the entire file (expensive in tokens)
- Search for import statements scattered throughout
- Guess at relationships from context
- Hunt for version information
- Wonder about maintenance status

**This wastes ~80% of scanning effort.**

---

## ⚡ **THE SOLUTION: SEMANTIC HEADERS**

Every file gets a lightweight semantic header that answers:
1. **What is this?** (identity)
2. **What does it need?** (dependencies)
3. **Who needs it?** (dependents)
4. **Where does it live?** (location)
5. **What's its status?** (lifecycle)

**Result:** Instant comprehension, automatic dependency graphs, trivial maintenance tracking.

---

## 📝 **THE STANDARD**

### For Markdown Files (.md)

```markdown
<!---
FILE: BOOTSTRAP_DOC_CLAUDE.md
PURPOSE: DOC_CLAUDE's identity and teleological lens definition
VERSION: v4.0.0
STATUS: Active
DEPENDS_ON: BOOTSTRAP_FRAMEWORK.md, BOOTSTRAP_VUDU.md
NEEDED_BY: README_C.md, MISSION_CURRENT.md, Any Claude instance
MOVES_WITH: /auditors/Bootstrap/
LAST_UPDATE: 2025-10-31 [DOCUMENTATION-2025-10-31-11]
--->

# Regular document content starts here...
```

### For Python Files (.py)

```python
"""
FILE: calculations.py
PURPOSE: YPA calculation engine and framework scoring
VERSION: v4.0
STATUS: Active
DEPENDS_ON: config.py, numpy, pandas
NEEDED_BY: app.py, console.py, all framework analysis
MOVES_WITH: /utils/
LAST_UPDATE: 2025-10-25 [CODE-2025-10-25-3]
"""

# Regular code starts here...
import numpy as np
```

## 🚀 **BENEFITS FOR DOC_CLAUDE**

### Instant Dependency Mapping
```python
# I can now build a complete dependency graph with:
for file in all_files:
    header = read_first_10_lines(file)
    parse_dependencies(header)
```

### Token Efficiency
- **Before:** Read 500 lines to understand file = 2000 tokens
- **After:** Read 8-line header = 50 tokens
- **Savings:** 97.5% token reduction!

---

**Maintained by:** DOC_CLAUDE (Documentation Orchestration Claude)  
**This standard transforms repo maintenance.** 🚀
