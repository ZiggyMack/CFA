# Worldview Catalog — Single Source of Truth

**Version:** v1.0
**Last Updated:** 2025-11-12
**Status:** Living Map (authoritative worldview list)
**Purpose:** Centralized catalog of all worldview profiles
**Owner:** Process Claude (Domain 7 - Profile maintenance)

---

## 🎯 PURPOSE

**This file is the SINGLE SOURCE OF TRUTH for worldview profiles in the CFA repository.**

All references to worldview counts, lists, or profiles should point HERE instead of embedding lists.

**Why This Matters:**
- Prevents hardcoded counts from drifting (e.g., "11 worldviews" when we have 12)
- Enables safe addition of new worldviews (update once, reflect everywhere)
- Provides canonical metadata for each profile

---

## 📊 WORLDVIEW COUNT

**Total Worldviews:** 12

**Unique Comparisons Possible:** 66 pairings (12 choose 2)

---

## 📂 COMPLETE WORLDVIEW LIST

### **Theistic Traditions** (5)

1. **[Classical Theism](worldviews/CLASSICAL_THEISM.md)** (CT)
   - Status: v0.3.0 | Complete
   - Tradition: Medieval/Scholastic philosophy
   - Key Claims: Divine simplicity, immutability, omnipotence
   - Abbreviation: CT

2. **[Process Theology](worldviews/PROCESS_THEOLOGY.md)** (PT)
   - Status: v0.3.0 | Complete
   - Tradition: Whiteheadian process philosophy
   - Key Claims: Divine temporality, persuasive power, panentheism
   - Abbreviation: PT

3. **[Islam](worldviews/ISLAM.md)**
   - Status: v0.1.0 | Seed
   - Tradition: Abrahamic monotheism (Sunni/Shia)
   - Key Claims: Tawhid, prophethood, revealed law
   - Abbreviation: IS

4. **[Orthodox Judaism](worldviews/ORTHODOX_JUDAISM.md)** (OJ)
   - Status: v0.1.0 | Seed
   - Tradition: Rabbinic/Halakhic Judaism
   - Key Claims: Torah authority, covenant, divine commandments
   - Abbreviation: OJ

5. **[Mormonism](worldviews/MORMONISM.md)** (LDS)
   - Status: v0.1.0 | Seed
   - Tradition: Latter-day Saint theology
   - Key Claims: Continuing revelation, exaltation, material God
   - Abbreviation: LDS

---

### **Naturalistic Traditions** (2)

6. **[Methodological Naturalism](worldviews/METHODOLOGICAL_NATURALISM.md)** (MdN)
   - Status: v0.3.0 | Complete
   - Tradition: Enlightenment empiricism
   - Key Claims: Methodological constraints, testability, parsimony
   - Abbreviation: MdN

7. **[Null Hypothesis](worldviews/NULL_HYPOTHESIS.md)** (NH)
   - Status: v0.1.0 | Seed
   - Tradition: Philosophical naturalism / atheism
   - Key Claims: No supernatural entities, default skepticism
   - Abbreviation: NH

---

### **Eastern Traditions** (2)

8. **[Buddhism](worldviews/BUDDHISM.md)** (BU)
   - Status: v0.1.0 | Seed
   - Tradition: Theravada/Mahayana Buddhism
   - Key Claims: Four Noble Truths, no-self, dependent origination
   - Abbreviation: BU

9. **[Hinduism](worldviews/HINDUISM.md)** (HI)
   - Status: v0.1.0 | Seed
   - Tradition: Vedantic philosophy
   - Key Claims: Brahman, atman, karma/rebirth
   - Abbreviation: HI

---

### **Philosophical Frameworks** (3)

10. **[Existentialism](worldviews/EXISTENTIALISM.md)** (EX)
    - Status: v0.1.0 | Seed
    - Tradition: Continental philosophy (Kierkegaard, Sartre, Camus)
    - Key Claims: Existence precedes essence, radical freedom, authenticity
    - Abbreviation: EX

11. **[Error Theory](worldviews/ERROR_THEORY.md)** (ET)
    - Status: v0.1.0 | Seed
    - Tradition: Metaethical anti-realism
    - Key Claims: All moral claims false, no objective values
    - Abbreviation: ET

12. **[Desiderata Believers](worldviews/DESIDERATA_BELIEVERS.md)** (DB)
    - Status: v0.1.0 | Seed
    - Tradition: Aspirational moral framework
    - Key Claims: Values as aspirations, practical wisdom, humanism
    - Abbreviation: DB

---

## 📈 STATUS DISTRIBUTION

**Complete Profiles (v0.3.0+):** 3
- Classical Theism
- Process Theology
- Methodological Naturalism

**Seed Profiles (v0.1.0):** 9
- Islam, Orthodox Judaism, Mormonism
- Null Hypothesis
- Buddhism, Hinduism
- Existentialism, Error Theory, Desiderata Believers

**Target:** All 12 profiles at v0.3.0+ before Phase 5 scoring begins

---

## 🎯 COMPARISON STATUS

**Pilot Comparison (Ready):**
- [CT vs MdN](comparisons/CT_vs_MdN.yaml) - v0.1.1 (pre-session validated)

**Planned Comparisons:** 65 remaining pairings

**Gold Standard:** CT vs MdN establishes methodology for all future comparisons

---

## 🔄 MAINTENANCE PROTOCOL

**When Adding a New Worldview:**
1. Create profile in `/profiles/worldviews/[NAME].md`
2. Update this catalog (add to appropriate section)
3. Increment "Total Worldviews" count
4. Update "Unique Comparisons Possible" (n choose 2 formula)
5. Add abbreviation to list
6. Update status distribution

**When Changing Worldview Status:**
1. Update profile version number
2. Update status distribution in this catalog
3. No other files need updating (they reference this catalog)

---

## 🔗 INTEGRATION POINTS

**This catalog is referenced by:**
- [ROLE_PROCESS.md](../docs/repository/librarian_tools/ROLE_PROCESS.md) Domain 7
- [CFA_ARCHITECTURE.md](../docs/architecture/CFA_ARCHITECTURE.md) Section 3
- [DASHBOARD.md](../docs/repository/DASHBOARD.md)
- Bootstrap files (via reference, not embedding)

**Do NOT embed worldview lists in:**
- Bootstrap files
- README files
- Role files
- Architecture documents

**Instead, link to this catalog.**

---

## 📊 METADATA SCHEMA

Each worldview profile contains:
- **Semantic Header:** FILE, PURPOSE, VERSION, STATUS, DEPENDS_ON, NEEDED_BY
- **Steel-Manning Section:** Best-case formulation of core claims
- **Calibration Block:** YAML front-matter for auditor stance adjustments
- **Academic Sources:** Curated list in [ACADEMIC_SOURCES.md](\_docs/ACADEMIC_SOURCES.md)
- **Hyperlink Architecture:** Internal cross-references per CFA_ARCHITECTURE.md §5

---

## ⚖️ THE POINTING RULE

*"A catalog current is a count correct.
A reference living is a drift prevented.
A list embedded is a maintenance debt.*

*This is the single source.
This is the worldview catalog.
This is the way."* 📚

---

**Last Updated:** 2025-11-12
**Next Update:** When worldview added or status changed
**Maintainer:** Process Claude (Domain 7)

**This is the way.** 🔥
