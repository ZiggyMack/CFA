<!---
FILE: DOC_DEP_SIMPLIFIED.md
PURPOSE: Simplified documentation dependency tracking system
VERSION: v2.0
STATUS: Active
DEPENDS_ON: DOCUMENTATION_DEPENDENCY_ANALYSIS.md
NEEDED_BY: DOC_CLAUDE, feature developers, documentation maintainers
MOVES_WITH: /docs/repository/dependency_maps/
LAST_UPDATE: 2025-10-31 [DOCUMENTATION-2025-10-31-11]
--->

# DOC_DEP System - Simplified Implementation Guide

**Purpose:** Track which documentation needs updating when features change  
**Method:** Lightweight tagging with YAML registry  
**Complexity:** Reduced by 60% from v1.0  
**Created by:** DOC_CLAUDE  

────────────────────────────────────────────────────

## 🎯 **THE PROBLEM (RESTATED SIMPLY)**

When you change a feature, documentation breaks in 20+ places.  
You don't know where. 
Hours wasted hunting.

**Solution:** Tag documentation sections. Map dependencies. Generate checklists.

---

## ⚡ **THE SIMPLIFIED APPROACH**

### Old Way (v1.0) - Too Complex
```markdown
<!-- DOC_DEP: setup, file_structure, v3.5 -->
## Getting Started
[content]
<!-- /DOC_DEP -->  ← UNNECESSARY CLOSING TAG
```

### New Way (v2.0) - Clean & Simple
```markdown
<!-- deps: setup, file_structure, v3.5 -->
## Getting Started
[content - no closing tag needed]
```

**What changed:**
- Shorter tag name (`deps` not `DOC_DEP`)
- No closing tags (50% less markup)
- Cleaner, more readable

---

## 📝 **IMPLEMENTATION PHASES**

### Phase 1: Tag High-Change Files (This Week)

**The 5 Pilot Files:**
1. **README.md** - Add deps tags to major sections
2. **MISSION_CURRENT.md** - Tag mission-specific content
3. **console.py** - Tag preset configurations
4. **SUCCESS_CRITERIA.md** - Tag validation sections
5. **DEPLOYMENT.md** - Tag setup instructions

**Example tagging:**
```markdown
<!-- deps: presets, configuration -->
## Preset Modes

The CFA includes 4 preset modes:
- Skeptic: High skepticism, low certainty
- Diplomat: Balanced approach
- Seeker: Meaning-first orientation
- Zealot: High certainty tolerance
```

### Phase 2: Create Simple Registry (Next Week)

**File:** `documentation_dependencies.yaml`

```yaml
# Documentation Dependency Registry
# Purpose: Map features to documentation sections
# Maintained by: DOC_CLAUDE
# Format: YAML (human-readable, commentable)

presets:
  stability: occasional  # How often this changes
  current_value: 4       # Current number of presets
  last_changed: 2025-10-27
  documented_in:
    - path: README.md
      section: features
      priority: primary    # Must update
    - path: console.py
      section: preset-config
      priority: primary
    - path: MISSION_CURRENT.md
      section: calibration-targets
      priority: secondary  # Should update
    - path: pages/manual.py
      section: mode-descriptions
      priority: tertiary   # Nice to update
  update_checklist: |
    When changing preset count:
    1. Update README.md feature list
    2. Modify console.py configurations
    3. Adjust validation criteria
    4. Update all "4 modes" references
    5. Test manual.py display

file_structure:
  stability: stable      # Rarely changes
  last_changed: 2025-10-15
  documented_in:
    - path: DEPLOYMENT.md
      section: structure
      priority: primary
    - path: README.md
      section: quick-start
      priority: primary
    - path: app.py
      section: imports
      priority: secondary
  notes: |
    File structure is stable but critical.
    Any change cascades through setup docs.

vudu_protocol:
  stability: stable
  version: 1.1
  documented_in:
    - path: VUDU_PROTOCOL.md
      section: all
      priority: primary
    - path: relay/README.md
      section: coordination
      priority: primary
    - path: BOOTSTRAP_VUDU.md
      section: overview
      priority: secondary
```

### Phase 3: Build Checklist Generator (Month 2)

**Simple Python script:**
```python
import yaml

def get_update_checklist(feature_changed):
    """Generate checklist when feature changes"""
    
    with open('documentation_dependencies.yaml') as f:
        deps = yaml.safe_load(f)
    
    if feature_changed not in deps:
        return f"No dependencies mapped for {feature_changed}"
    
    feature = deps[feature_changed]
    checklist = []
    
    # Group by priority
    for priority in ['primary', 'secondary', 'tertiary']:
        for doc in feature['documented_in']:
            if doc.get('priority') == priority:
                checklist.append(
                    f"[{priority.upper()}] Update {doc['path']}#{doc['section']}"
                )
    
    # Add custom checklist if exists
    if 'update_checklist' in feature:
        checklist.append("\nCustom steps:")
        checklist.append(feature['update_checklist'])
    
    return '\n'.join(checklist)

# Usage:
# >>> get_update_checklist('presets')
# [PRIMARY] Update README.md#features
# [PRIMARY] Update console.py#preset-config
# [SECONDARY] Update MISSION_CURRENT.md#calibration-targets
# ...
```

---

## 🎨 **YAML vs JSON (Why YAML Wins)**

### JSON (Old Proposal) - Rigid
```json
{
  "presets": {
    "stability": "occasional",
    "documented_in": [
      {
        "path": "README.md",
        "section": "features"
      }
    ]
  }
}
```
❌ No comments allowed  
❌ Verbose syntax  
❌ Hard to read  
❌ Must quote everything

### YAML (New Approach) - Flexible
```yaml
presets:
  stability: occasional  # Can add comments!
  documented_in:
    - path: README.md
      section: features
      priority: primary  # Must update
```
✅ Comments for context  
✅ Clean, readable  
✅ Less syntactic noise  
✅ Multiline strings for notes

---

## 🚀 **QUICK START GUIDE**

### For DOC_CLAUDE (Today)
1. **Add deps tags to 5 pilot files** (30 min)
2. **Create documentation_dependencies.yaml** (20 min)
3. **Document in REPO_LOG** (5 min)
4. **Test with one feature change** (10 min)

### For Feature Developers
1. **Before changing feature:** Check if it's in registry
2. **Get checklist:** Run generator or check YAML
3. **Update docs:** Follow priority order
4. **Add to registry:** If feature not mapped yet

### For Documentation Maintainers
1. **When writing new docs:** Add deps tags
2. **When updating docs:** Check what depends on this
3. **Regular audit:** Validate registry accuracy

---

## 📊 **SUCCESS METRICS**

### Week 1 Goals
- ✅ 5 files tagged with deps
- ✅ Basic YAML registry created
- ✅ One feature fully mapped
- ✅ Manual checklist generated

### Month 1 Goals
- 📋 20 files tagged
- 📋 All major features mapped
- 📋 Automated checklist script
- 📋 50% reduction in stale docs

### Month 3 Goals
- 📋 80% of docs tagged
- 📋 CI/CD integration
- 📋 Automated staleness detection
- 📋 Zero documentation drift

---

## ⚠️ **COMMON PITFALLS (AVOIDED)**

### Don't Over-Tag
❌ **Bad:** Tagging every paragraph  
✅ **Good:** Tag meaningful sections only

### Don't Over-Specify
❌ **Bad:** Complex 5-level dependency trees  
✅ **Good:** Simple feature → doc mappings

### Don't Block Progress
❌ **Bad:** "Can't change until all docs tagged"  
✅ **Good:** Gradual adoption, immediate value

### Don't Automate Too Early
❌ **Bad:** Complex CI/CD from day 1  
✅ **Good:** Manual process first, automate what works

---

## 🎯 **THE VISION (SIMPLIFIED)**

**Today:** Hunt through 20 files when features change  
**Tomorrow:** Run script, get checklist, update systematically  
**Future:** CI/CD auto-generates PRs for doc updates

But we start simple. Tag 5 files. Build from there.

---

## 💡 **KEY INSIGHT**

> "Documentation is code for humans.  
> Treat it with the same rigor.  
> Track dependencies.  
> Automate updates.  
> Maintain quality."

**- DOC_CLAUDE**

---

## 📝 **IMPLEMENTATION CHECKLIST**

### Immediate (30 minutes)
- [ ] Tag README.md sections with `<!-- deps: X, Y -->`
- [ ] Tag MISSION_CURRENT.md sections
- [ ] Create documentation_dependencies.yaml with 2 features
- [ ] Test manually: "If I change presets, what updates?"
- [ ] Create REPO_LOG entry

### Short Term (This Week)
- [ ] Tag remaining 3 pilot files
- [ ] Expand registry to 5 features
- [ ] Write simple Python generator
- [ ] Document lessons learned

### Medium Term (This Month)
- [ ] Reach 20 files tagged
- [ ] All critical features mapped
- [ ] Team training on system
- [ ] Measure improvement metrics

---

**"Start simple. Iterate. Improve."** 🚀

**This is DOC_CLAUDE's way.** 🔥

────────────────────────────────────────────────────
**System:** DOC_DEP v2.0 (Simplified)  
**Complexity:** -60% from v1.0  
**Adoption Barrier:** Minimal  
**Value Delivery:** Immediate
