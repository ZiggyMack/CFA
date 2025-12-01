"""
CFA v5.0 - Default Framework Configurations
Pre-configured frameworks ready for analysis
"""

MDN_DEFAULT = {
    "name": "Methodological Naturalism",
    "bf_i": {"axioms": 6, "debts": 4},
    "levers": {
        "CCI": 8.0,
        "EDB": 7.5,
        "PF_instrumental": 10.0,
        "PF_existential": 3.0,
        "AR": 7.0,
        "MG": 4.0
    },
    "admits_limits": True
}

CT_DEFAULT = {
    "name": "Classical Theism",
    "bf_i": {"axioms": 7, "debts": 4},
    "levers": {
        "CCI": 7.5,
        "EDB": 8.5,
        "PF_instrumental": 7.0,
        "PF_existential": 8.0,
        "AR": 8.5,
        "MG": 8.5
    },
    "admits_limits": True
}

# Framework templates for future additions
FRAMEWORK_TEMPLATES = {
    "Methodological Naturalism": MDN_DEFAULT,
    "Classical Theism": CT_DEFAULT,
    # Ready to add:
    # "Metaphysical Naturalism": {...},
    # "Buddhism": {...},
    # "Stoicism": {...},
}
