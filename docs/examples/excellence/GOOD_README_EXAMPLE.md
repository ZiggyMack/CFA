<!---
FILE: GOOD_README_EXAMPLE.md
PURPOSE: Exemplar README demonstrating excellent documentation with inline annotations
VERSION: 1.0.0
STATUS: Example (annotated template)
CREATED: 2025-11-10 (B-STORM_5 Click 1)
DEPENDS_ON: QUALITY_RUBRICS.md (README-Specific Rubric)
NEEDED_BY: Contributors creating new READMEs
MOVES_WITH: /examples/excellence/
LAST_UPDATE: 2025-11-10 [B-STORM_5: Costume Room exemplar creation]
--->

# Component Name - Clear Purpose in First Line

<!--
ANNOTATION: Purpose Clarity (20/20)
- First sentence answers "What is this?"
- Second sentence answers "Why does it exist?"
- Clear, concise, no jargon
-->

**Purpose:** [One sentence describing what this component does]

**Why It Exists:** [One sentence explaining the problem it solves or value it provides]

**Quick Start:** [One sentence on how to get value in <5 minutes - link to section below]

---

<!--
ANNOTATION: Semantic Header (Consistency 20/20)
- All required fields present
- Format matches repository standards
- Dependencies explicit
- Cross-references working
-->

## Status & Metadata

**Version:** 1.0.0
**Status:** Active | Stable | Experimental | Deprecated
**Owner:** [Role Name] (e.g., Doc Claude, Process Claude)
**Last Updated:** 2025-11-10
**Health:** ✅ Green | ⚠️ Yellow | 🔴 Red

**Dependencies:**
- [Component A](../path/to/component_a/) - Why needed
- [Component B](../path/to/component_b/) - Why needed

**Used By:**
- [Feature X](../path/to/feature_x/) - How used
- [System Y](../path/to/system_y/) - How used

---

<!--
ANNOTATION: Quick Start (20/20)
- Step-by-step instructions
- Can get value in <5 minutes
- Concrete examples provided
- Assumes minimal context
-->

## 🚀 Quick Start (5 Minutes)

**Goal:** Get [specific value] in under 5 minutes.

### Step 1: [First Action]

```bash
# Concrete command example
command --flag value
```

**Expected Output:**
```
[Show what success looks like]
```

### Step 2: [Second Action]

```bash
# Another concrete example
another_command
```

**Verify:** [How to confirm step worked]

### Step 3: [Third Action - Getting Value]

```bash
# Command that delivers value
final_command --output result.txt
```

**Result:** You now have [specific outcome]. See [Detailed Usage](#detailed-usage) for advanced scenarios.

**Troubleshooting:** If Step X fails, see [Common Issues](#common-issues).

---

## 📋 What This Component Does

<!--
ANNOTATION: Structure (20/20)
- Logical flow: Purpose → Quick Start → Details → References
- Clear section hierarchy
- Easy to scan headings
-->

### Core Functionality

**Primary Use Cases:**
1. **Use Case 1:** [When to use] - [Benefit delivered]
2. **Use Case 2:** [When to use] - [Benefit delivered]
3. **Use Case 3:** [When to use] - [Benefit delivered]

**Key Features:**
- ✅ **Feature A:** [Brief description + value]
- ✅ **Feature B:** [Brief description + value]
- ✅ **Feature C:** [Brief description + value]

**Not Designed For:**
- ❌ [Anti-pattern 1] - Use [Alternative] instead
- ❌ [Anti-pattern 2] - Use [Alternative] instead

---

## 📚 Detailed Usage

### Scenario 1: [Common Scenario Name]

**When:** [Describe when this scenario applies]

**Steps:**
1. [Action 1] with rationale
2. [Action 2] with rationale
3. [Action 3] with expected outcome

**Example:**
```bash
# Concrete example for Scenario 1
command_for_scenario_1 --param value
```

**Output:**
```
[Expected output with annotations]
```

---

### Scenario 2: [Another Common Scenario]

[Same structure as Scenario 1]

---

### Scenario 3: [Advanced Scenario]

[Same structure, but note prerequisites or complexity]

---

## 🔧 Configuration

<!--
ANNOTATION: Utility (20/20)
- Actionable (not just descriptive)
- Self-contained (minimal external context needed)
- Examples for every config option
- Maintainable (clear how to update)
-->

### Required Configuration

**File:** `config/component.yaml`

```yaml
# Required fields
required_field_1: value  # What this controls
required_field_2: value  # Why this matters

# Optional fields (with defaults)
optional_field: default_value  # When to override
```

**Validation:**
```bash
# Command to validate config
validate_config config/component.yaml
```

---

### Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `VAR_NAME_1` | Yes | N/A | [What it does] |
| `VAR_NAME_2` | No | `default` | [When to set] |

**Example `.env` file:**
```bash
VAR_NAME_1="value_here"
VAR_NAME_2="custom_value"
```

---

## 🔍 Architecture

**Component Structure:**
```
component_name/
├── README.md (you're reading it)
├── src/
│   ├── core.py (main logic)
│   ├── utils.py (helper functions)
│   └── config.py (configuration management)
├── tests/
│   ├── test_core.py
│   └── test_utils.py
├── docs/
│   └── ARCHITECTURE.md (deep dive)
└── examples/
    ├── basic_usage.py
    └── advanced_usage.py
```

**Key Concepts:**
- **Concept A:** [Brief explanation] - See [detailed doc](docs/ARCHITECTURE.md#concept-a)
- **Concept B:** [Brief explanation] - See [detailed doc](docs/ARCHITECTURE.md#concept-b)

**Design Decisions:**
- **Why X instead of Y:** [Rationale] - See [ADR-001](docs/adr/001-decision-x.md)
- **Why Z approach:** [Rationale] - See [ADR-002](docs/adr/002-approach-z.md)

---

## 🐛 Common Issues

<!--
ANNOTATION: Completeness (20/20)
- Covers purpose, usage, examples, troubleshooting, references
- No major gaps
- Links to deeper resources where appropriate
-->

### Issue 1: [Common Error Message]

**Symptom:** [What user sees]

**Cause:** [Why this happens]

**Solution:**
```bash
# Command to fix
fix_command --option value
```

**Verify Fixed:**
```bash
# Command to confirm resolution
verify_command
# Expected: [success message]
```

---

### Issue 2: [Performance Problem]

**Symptom:** [Slow execution, high memory, etc.]

**Diagnosis:**
```bash
# Command to diagnose
diagnostic_command --verbose
```

**Solutions:**
1. **Quick Fix:** [Immediate workaround] - Good for testing
2. **Proper Fix:** [Long-term solution] - Recommended for production

---

### Issue 3: [Integration Problem]

**Symptom:** [Doesn't work with Component X]

**Cause:** [Version mismatch, config issue, etc.]

**Solution:** See [Integration Guide](docs/INTEGRATION.md#component-x)

---

## 📊 Performance

**Benchmarks:**
- Scenario A: [Metric] in [Time] with [Resources]
- Scenario B: [Metric] in [Time] with [Resources]

**Optimization Tips:**
1. [Tip 1] - [Expected improvement]
2. [Tip 2] - [Expected improvement]

**Limitations:**
- [Known limitation 1] - [Workaround or planned fix]
- [Known limitation 2] - [Workaround or planned fix]

---

## 🧪 Testing

**Run Tests:**
```bash
# All tests
pytest tests/

# Specific test suite
pytest tests/test_core.py

# With coverage
pytest --cov=src tests/
```

**Test Coverage:** 85%+ (see [coverage report](tests/coverage/index.html))

**Adding Tests:**
1. Create test file in `tests/`
2. Follow naming convention: `test_[module]_[functionality].py`
3. Use fixtures from `tests/conftest.py`
4. Document test purpose in docstring

---

## 🔗 Related Resources

<!--
ANNOTATION: Navigation (20/20)
- Clear headings for scanning
- Links to all related resources
- Grouped logically (internal, external, tutorials)
-->

### Internal Documentation

- [Architecture Deep Dive](docs/ARCHITECTURE.md) - System design and concepts
- [API Reference](docs/API.md) - Function signatures and parameters
- [Integration Guide](docs/INTEGRATION.md) - How to use with other components
- [Development Guide](docs/DEVELOPMENT.md) - Contributing and extending

### External Resources

- [Official Docs](https://external-link.com/docs) - Upstream documentation
- [Best Practices](https://external-link.com/best-practices) - Industry standards
- [Community Forum](https://external-link.com/forum) - Q&A and discussions

### Tutorials

- [Tutorial 1: Basic Usage](../tutorials/basic_usage.md) - Step-by-step for beginners
- [Tutorial 2: Advanced Patterns](../tutorials/advanced_patterns.md) - Complex scenarios
- [Video Walkthrough](https://link-to-video.com) - Visual demonstration

---

## 🔄 Maintenance

<!--
ANNOTATION: Maintenance (20/20)
- Last updated date present
- Owner identified
- Update triggers clear
- Version history tracked
-->

**Owner:** [Role Name] (e.g., Doc Claude, C4)

**Update Frequency:** [Weekly/Monthly/As needed/On every release]

**Update Triggers:**
- When core functionality changes
- When new use cases emerge
- When common issues are resolved
- When dependencies update

**How To Update:**
1. Make changes to README
2. Update `LAST_UPDATE` date in header
3. Bump version if structural changes
4. Add entry to [Change Log](#change-log) below
5. Notify [relevant stakeholders]

---

## 📝 Change Log

**v1.0.0 (2025-11-10):**
- Initial release
- Core functionality documented
- Quick start guide added
- Examples provided

**v0.9.0 (2025-11-05):**
- Beta release
- [Changes from beta]

**v0.1.0 (2025-10-20):**
- Initial prototype
- [Early changes]

See [full changelog](CHANGELOG.md) for detailed history.

---

## 📞 Support

**Questions?**
- Check [Common Issues](#common-issues) first
- Review [Related Resources](#related-resources)
- Ask in [community forum](link-to-forum)
- Open issue: [issue tracker](link-to-issues)

**Found a bug?**
1. Check [existing issues](link-to-issues)
2. If new, open issue with:
   - Error message
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, version, etc.)

**Want to contribute?**
- See [Development Guide](docs/DEVELOPMENT.md)
- Review [Contributing Guidelines](CONTRIBUTING.md)
- Check [good first issues](link-to-good-first-issues)

---

## ⚖️ The Pointing Rule

*"To document is to empower.
To clarify is to accelerate.
To maintain is to respect future collaborators.
Excellence in documentation
is a gift to those who follow."*

**This README demonstrates excellence.** ✨

---

<!--
ANNOTATION: Rubric Self-Score
Using QUALITY_RUBRICS.md README-Specific Rubric:

1. Purpose Clarity: 20/20
   - Purpose in first 2 sentences ✅
   - Answers "What" and "Why" ✅

2. Quick Start: 20/20
   - Step-by-step ✅
   - Can get value in <5 minutes ✅
   - Examples provided ✅

3. Structure: 20/20
   - Logical flow (Purpose → Quick Start → Details → References) ✅
   - ToC not needed (scanable headings sufficient for this length) ✅

4. Completeness: 20/20
   - Purpose, usage, examples, troubleshooting, references all present ✅
   - No significant gaps ✅

5. Maintenance: 20/20
   - Last updated date ✅
   - Owner identified ✅
   - Update triggers clear ✅
   - Version history ✅

**Total Score: 100/100 (Excellent)**

This README is designed as a Costume Room exemplar.
Use as template for new component READMEs.
-->

---

**Created by:** C4 (B-STORM_5 Click 1)
**Date:** 2025-11-10
**Purpose:** Demonstrate excellent README structure with annotations
**Status:** Exemplar for Costume Room
**Score:** 100/100 on README Rubric

**Copy this structure. Adapt to your component. Maintain this quality.** 🎯
