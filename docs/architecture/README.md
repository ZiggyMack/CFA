<!-- deps: file_structure, documentation -->
# Architecture Documentation

## Core Architecture Documents

### [Trinity Architecture](TRINITY_ARCHITECTURE.md)
**Status:** CANONICAL | **Version:** v1.0 | **Date:** 2025-11-03

Defines the three foundational roles for repository coherence:
- **Keeper** (lock) - State integrity and coherence guardian
- **Logger** (ledger) - Narrative preservation and traceability curator
- **Shaman** (bridge) - Mythology-to-mechanism bridge

**Key Concepts:**
- Role matrix with clear invocation criteria
- Lifecycle hooks (Bootstrap, Audit, Incident, Release)
- Mythology -> Mechanism mapping
- Discovery Arc narrative

**When to consult:**
- Understanding role boundaries and responsibilities
- Determining which Claude to invoke for specific tasks
- Resolving "who owns what" questions
- Tracing mythological origins of architectural decisions
