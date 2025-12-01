"""
CFA Profile Loader - Load worldview profiles from canonical YAML files

This module provides utilities to load worldview profiles from the profiles/worldviews/
directory. YPA scores are loaded from canonical .yaml files (Gospel Problem
protection - single source of truth), while .md files provide human-readable documentation.

Architecture (Dual-File System):
- .yaml files: Canonical machine-readable scores (axioms, debts, levers, YPA)
- .md files: Human-readable documentation (hyperlinks, sources, philosophy)
- Console reads .yaml for calculations, .md for context/display

Data Flow:
    get_ypa_data() → CLASSICAL_THEISM.yaml (primary)
                  ↓ (fallback if no .yaml)
                  → CLASSICAL_THEISM.md (legacy YAML blocks)

Usage:
    from utils.profile_loader import load_profile, get_ypa_data

    # Get YPA data for Console calculations (reads .yaml file)
    ypa_data = get_ypa_data("Classical Theism")
    # Returns: {"name": "...", "bf_i": {...}, "levers": {...}, "admits_limits": bool}

    # Load complete profile metadata (reads .md file)
    profile = load_profile("Classical Theism")
    # Returns: {"metadata": {...}, "ypa_data": {...}, "raw_content": "..."}
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Optional, List, Any

# Profile directory path (relative to project root)
PROFILES_DIR = Path(__file__).parent.parent / "profiles" / "worldviews"


class ProfileLoadError(Exception):
    """Raised when profile loading fails"""
    pass


def _extract_yaml_blocks(content: str) -> Dict[str, Any]:
    """
    Extract all YAML blocks from markdown content

    Returns dict with keys matching markdown headings before each yaml block
    """
    yaml_blocks = {}

    # Pattern: ## Heading followed by yaml code block
    # More flexible pattern that allows text between heading and yaml block
    # Captures: heading name and yaml content
    pattern = r'##\s+([^\n]+)\n+(.*?)```yaml\n(.*?)\n```'

    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        heading = match.group(1).strip()
        yaml_content = match.group(3)  # yaml content is group 3 now

        try:
            parsed = yaml.safe_load(yaml_content)
            yaml_blocks[heading] = parsed
        except yaml.YAMLError as e:
            print(f"Warning: Failed to parse YAML block under '{heading}': {e}")
            continue

    return yaml_blocks


def _normalize_worldview_name(name: str) -> str:
    """
    Normalize worldview name to filename format

    Examples:
        "Classical Theism" -> "CLASSICAL_THEISM"
        "classical theism" -> "CLASSICAL_THEISM"
        "ct" -> "CLASSICAL_THEISM" (via alias mapping)
    """
    # Alias mapping for common abbreviations
    aliases = {
        "ct": "CLASSICAL_THEISM",
        "mdn": "METHODOLOGICAL_NATURALISM",
        "oj": "ORTHODOX_JUDAISM",
        "lds": "MORMONISM",
    }

    name_lower = name.lower().strip()

    if name_lower in aliases:
        return aliases[name_lower]

    # Convert to SCREAMING_SNAKE_CASE
    return name.upper().replace(" ", "_").replace("-", "_")


def load_profile(worldview_name: str) -> Dict[str, Any]:
    """
    Load complete profile for a worldview

    Args:
        worldview_name: Name of worldview (e.g., "Classical Theism", "ct", "CLASSICAL_THEISM")

    Returns:
        Dict containing:
        - metadata: Profile metadata block
        - ypa_data: YPA application data (if present)
        - metrics: Philosophical metrics (when implemented)
        - raw_content: Full markdown content

    Raises:
        ProfileLoadError: If profile file not found or parsing fails
    """
    filename = f"{_normalize_worldview_name(worldview_name)}.md"
    filepath = PROFILES_DIR / filename

    if not filepath.exists():
        raise ProfileLoadError(
            f"Profile not found: {filepath}\n"
            f"Available profiles: {list_available_profiles()}"
        )

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        raise ProfileLoadError(f"Failed to read profile {filepath}: {e}")

    # Extract all YAML blocks
    yaml_blocks = _extract_yaml_blocks(content)

    return {
        "metadata": yaml_blocks.get("Metadata", {}),
        "ypa_data": yaml_blocks.get("YPA Application Data (CFA v4.0)", {}),
        "metrics": {},  # TODO: Phase 2 - extract philosophical metrics
        "raw_content": content,
        "filepath": str(filepath),
    }


def get_ypa_data(worldview_name: str) -> Dict[str, Any]:
    """
    Get YPA data from canonical .yaml file (Gospel Problem protection)

    Architecture: Reads from canonical .yaml files instead of .md YAML blocks.
    This ensures single source of truth for scores - .yaml files are the master,
    .md files are documentation only.

    Args:
        worldview_name: Name of worldview (e.g., "Classical Theism", "ct")

    Returns:
        Dict with keys: "name", "bf_i", "levers", "admits_limits"
        Matches format expected by utils/calculations.py::ypa_scenario_scores()

    Example:
        >>> ypa = get_ypa_data("Classical Theism")
        >>> ypa["levers"]["CCI"]
        7.5
        >>> ypa["bf_i"]["axioms"]
        7

    Raises:
        ProfileLoadError: If .yaml file not found or invalid
    """
    # Normalize name and construct .yaml filepath
    yaml_filename = f"{_normalize_worldview_name(worldview_name)}.yaml"
    yaml_filepath = PROFILES_DIR / yaml_filename

    # PRIMARY: Load from canonical .yaml file
    if yaml_filepath.exists():
        try:
            with open(yaml_filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # Convert canonical YAML structure to Console format
            return {
                "name": data["profile"]["name"],
                "bf_i": {
                    "axioms": data["calculated"]["axiom_count"],
                    "debts": data["calculated"]["debt_count"],
                },
                "levers": {
                    "CCI": data["levers"]["collective_coherence_impact"],
                    "EDB": data["levers"]["epistemic_debt_burden"],
                    "PF_instrumental": data["levers"]["paternalistic_force_interventionist"],
                    "PF_existential": data["levers"]["paternalistic_force_epistemic"],
                    "AR": data["levers"]["asymmetry_risk"],
                    "MG": data["levers"]["meta_governance"],
                },
                "admits_limits": data["behavioral_flags"]["admits_limits"],
            }

        except (KeyError, TypeError, yaml.YAMLError) as e:
            raise ProfileLoadError(
                f"Invalid YAML structure in {yaml_filepath}: {e}\n"
                f"Expected canonical format with profile/calculated/levers/behavioral_flags blocks."
            )

    # FALLBACK: Try old .md YAML block method (backward compatibility)
    # This ensures profiles without .yaml files yet (scaffolded profiles) still work
    else:
        profile = load_profile(worldview_name)

        if not profile["ypa_data"]:
            raise ProfileLoadError(
                f"Profile '{worldview_name}' has no canonical .yaml file AND no YPA data in .md file. "
                f"This profile may not be ready for CFA calculations yet.\n"
                f"Expected: {yaml_filepath}"
            )

        ypa = profile["ypa_data"]
        metadata = profile["metadata"].get("profile", {})

        # Extract data in frameworks.py format (legacy .md YAML blocks)
        return {
            "name": metadata.get("name", worldview_name),
            "bf_i": {
                "axioms": ypa.get("brute_fact_index", {}).get("axioms", 0),
                "debts": ypa.get("brute_fact_index", {}).get("debts", 0),
            },
            "levers": {
                "CCI": ypa.get("ypa_levers", {}).get("CCI", 0.0),
                "EDB": ypa.get("ypa_levers", {}).get("EDB", 0.0),
                "PF_instrumental": ypa.get("ypa_levers", {}).get("PF_instrumental", 0.0),
                "PF_existential": ypa.get("ypa_levers", {}).get("PF_existential", 0.0),
                "AR": ypa.get("ypa_levers", {}).get("AR", 0.0),
                "MG": ypa.get("ypa_levers", {}).get("MG", 0.0),
            },
            "admits_limits": ypa.get("behavioral_flags", {}).get("admits_limits", True),
        }


def list_available_profiles() -> List[str]:
    """
    List all available worldview profiles

    Returns:
        List of profile names (display format, e.g., "Classical Theism")
    """
    if not PROFILES_DIR.exists():
        return []

    profiles = []
    for filepath in PROFILES_DIR.glob("*.md"):
        # Convert filename to display name
        name = filepath.stem.replace("_", " ").title()
        profiles.append(name)

    return sorted(profiles)


def get_profile_metadata(worldview_name: str) -> Dict[str, Any]:
    """
    Get just the metadata block from a profile

    Useful for displaying profile info without loading full content
    """
    profile = load_profile(worldview_name)
    return profile["metadata"].get("profile", {})


def get_brute_ledger(worldview_name: str) -> Dict[str, Any]:
    """
    Get Mr. Brute's Ledger data (axioms and debts) for a worldview

    Returns dict with:
    - axioms: List of unprovable assumptions
    - debts: List of unresolved questions
    - audit_notes: Commentary on axioms/debts

    Used by pages/brute_ledger.py to dynamically generate ledger content
    """
    profile = load_profile(worldview_name)

    yaml_blocks = _extract_yaml_blocks(profile["raw_content"])
    ledger_data = yaml_blocks.get("Mr. Brute's Ledger", {}).get("brute_ledger", {})

    if not ledger_data:
        # Profile doesn't have brute ledger section yet
        return {
            "axioms": {"count": 0, "list": []},
            "debts": {"count": 0, "list": []},
            "audit_notes": "Brute ledger not yet documented for this profile.",
        }

    return ledger_data


# Backward compatibility: Provide frameworks.py-style constants
def get_framework_templates() -> Dict[str, Dict]:
    """
    Get all available frameworks in frameworks.py format

    This provides backward compatibility with code expecting
    utils/frameworks.py::FRAMEWORK_TEMPLATES
    """
    templates = {}

    for profile_name in list_available_profiles():
        try:
            ypa_data = get_ypa_data(profile_name)
            templates[ypa_data["name"]] = ypa_data
        except ProfileLoadError:
            # Skip profiles without YPA data (scaffolded profiles)
            continue

    return templates


# Legacy aliases for frameworks.py compatibility
def get_ct_default() -> Dict:
    """Backward compatibility: CT_DEFAULT from frameworks.py"""
    return get_ypa_data("Classical Theism")


def get_mdn_default() -> Dict:
    """Backward compatibility: MDN_DEFAULT from frameworks.py"""
    return get_ypa_data("Methodological Naturalism")


# Module-level exports for convenience
CT_DEFAULT = None  # Lazy-loaded on first access
MDN_DEFAULT = None  # Lazy-loaded on first access
FRAMEWORK_TEMPLATES = None  # Lazy-loaded on first access


def __getattr__(name):
    """
    Lazy-load module-level constants on first access

    This allows:
        from utils.profile_loader import CT_DEFAULT, MDN_DEFAULT

    To work as drop-in replacement for:
        from utils.frameworks import CT_DEFAULT, MDN_DEFAULT
    """
    global CT_DEFAULT, MDN_DEFAULT, FRAMEWORK_TEMPLATES

    if name == "CT_DEFAULT":
        if CT_DEFAULT is None:
            CT_DEFAULT = get_ct_default()
        return CT_DEFAULT

    elif name == "MDN_DEFAULT":
        if MDN_DEFAULT is None:
            MDN_DEFAULT = get_mdn_default()
        return MDN_DEFAULT

    elif name == "FRAMEWORK_TEMPLATES":
        if FRAMEWORK_TEMPLATES is None:
            FRAMEWORK_TEMPLATES = get_framework_templates()
        return FRAMEWORK_TEMPLATES

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if __name__ == "__main__":
    # Test/demo usage
    print("=== CFA Profile Loader Test ===\n")

    print(f"Available profiles: {list_available_profiles()}\n")

    for worldview in ["Classical Theism", "Methodological Naturalism"]:
        print(f"--- {worldview} ---")
        try:
            ypa = get_ypa_data(worldview)
            print(f"  Name: {ypa['name']}")
            print(f"  BFI: {ypa['bf_i']['axioms']} axioms, {ypa['bf_i']['debts']} debts")
            print(f"  CCI: {ypa['levers']['CCI']}")
            print(f"  EDB: {ypa['levers']['EDB']}")
            print(f"  PF_inst: {ypa['levers']['PF_instrumental']}")
            print(f"  PF_exist: {ypa['levers']['PF_existential']}")
            print(f"  AR: {ypa['levers']['AR']}")
            print(f"  MG: {ypa['levers']['MG']}")
            print(f"  Admits Limits: {ypa['admits_limits']}")
        except ProfileLoadError as e:
            print(f"  ERROR: {e}")
        print()
