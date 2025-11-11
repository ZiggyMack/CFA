<!---
FILE: MATRIX_PROTOTYPE_NOTES.md
PURPOSE: Running notes for SMV prototype work (mock data tests, UI behaviors)
STATUS: Draft (workshop)
OWNER: Nova
CREATED: 2025-11-11
LAST_UPDATE: 2025-11-11 [Scaffold created]
--->

# SMV Prototype Notes (Workshop)

Use this file to track experiments, rendering issues, and open questions while Phase 1 is underway. Once the prototype stabilizes we can migrate the relevant content into `ui/smv/README.md`.

## Initial TODOs

- [ ] Set up local viewer (React D3 or static HTML) for triangle + timeline demos
- [ ] Import `MATRIX_MOCK_DATA.json` and confirm schema validation
- [ ] Implement color scale utility (green ? amber ? red)
- [ ] Prototype tension sparkline component
- [ ] Prototype ethics badge overlay (examined/deferred/missing)

## Open Questions

1. Should we animate edge-width transitions or keep them discrete per tick?
2. Do we need a fourth auditor placeholder for future sessions (e.g., Shaman involvement), or keep schema locked to 3 nodes for now?
3. How do we display simultaneous Crux IDs if multiple metrics trigger at the same tick?

Add notes below as we test pieces of the UI.
