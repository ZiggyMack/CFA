# Falcon-1000 roll-up
Updated: Wed Oct 21, 2026 11:30 AM ET (31 new fix JPGs since the 10:27 AM ET roll-up, all from the full-scale chest rebuild to Ziggy's approved C04-010 v011 pilot; qa*.tsv unchanged)

**Falcon: 1460 JPG image files on disk** across 67 category folders: 1224 originals plus 236 fix versions. Every category is at 15 or more originals; none under 15. Mask/zoom PNGs and sidecars beside the fixes are not counted as images.
Per Chief REBALANCE 08:28: no more new Falcon categories. Remaining Falcon work is top-ups and fixes only (other agents).

## Counts per category (JPG images on disk)
- C01-pilot-hover: 15
- C02-captain-portrait: 15 originals + 22 other versions (37 files)
- C03-look-back-softened: 15 originals + 23 other versions (38 files)
- C04-battle-light: 15 originals + 42 other versions (57 files)
- C05-lurch-grin: 15 originals + 60 other versions (75 files)
- C06-lurch-no-grin: 15 originals + 32 other versions (47 files)
- C07-throttle-insert: 22
- C08-overhead-lever: 15
- C09-overhead-switches: 15
- C10-harness-buckle: 15
- C11-nav-display: 15
- C12-chewy-switches: 15
- C13-chewy-levers: 15
- C14-chewy-look: 15
- C15-cockpit-twoshot: 15 originals + 6 other versions (21 files)
- C16-leia-doorway: 22
- C17-lounge-empty: 15
- C18-dj-station: 15
- C19-chewy-decks: 15
- C20-fader-push: 15
- C21-chewy-holds-room: 20 originals + 4 other versions (24 files)
- C22-reverse-dj-to-pilot: 21 originals + 2 other versions (23 files)
- C23-hold-hatch: 22
- C24-leia-surveys: 20 originals + 4 other versions (24 files)
- C25-corridors-arches: 22
- C26-quarters: 22 originals + 12 other versions (34 files)
- C27-bureau: 22 originals + 2 other versions (24 files)
- C28-bathroom: 22
- C29-galley: 22
- C30-cargo: 22
- C31-comms: 22
- C32-engine: 22
- C33-ramp-inside: 22
- C34-silhouette: 22
- C35-hangar-exit: 22
- C36-warship-pass: 22
- C37-bank: 22
- C38-turn: 22
- C39-accel: 22
- C40-maw: 22
- C41-cockpit-ext: 22 originals + 5 other versions (27 files)
- C42-ramp-landing: 22 originals + 12 other versions (34 files)
- C43-dolo-ramp: 22
- C44-chewy-boarding: 22
- C45-leia-boarding: 22
- C46-gunner-well: 22
- C47-holochess: 15
- C60-nebula-drift: 15
- C61-ice-moon-landing: 15
- C62-docking-clamps: 22
- C63-repair-spacewalk: 22
- C64-rain-hangar: 15
- C65-asteroid-hide: 15
- C66-sunrise-orbit: 22
- C67-cargo-hold-dolo-chewy: 15 originals + 4 other versions (19 files)
- C68-escape-pod-bay: 15
- C69-hyperspace-exit: 15 originals + 1 other versions (16 files)
- C70-dune-landing: 15
- C71-gas-giant-storm: 15
- C72-salvage-yard: 15
- C73-ice-field-chase: 15
- C74-moonlit-ocean-skim: 15
- C75-meteor-shower: 15
- C76-city-rooftop-landing: 22 originals + 5 other versions (27 files)
- C77-galley-breakfast-dolo-chewy: 15
- C78-cockpit-night-watch: 15
- C79-tractor-beam-pull: 15

## STRONG / defect / FAIL tallies
- qa*.tsv files unchanged since Oct 17, so no new STRONG/defect/FAIL rows in them.
- New since 10:27 AM ET: the **full-scale chest rebuild** (to Ziggy-approved C04-010 v011, d68287f1; Falcon metadata v004 is frozen on D:, these go in a later revision). Every new version is **PRELIMINARY** (Z-bot self-checks; no V-Team pass logged yet):
  - C02 (Z_7, `Z7_CHEST_FULL_v002.tsv`): 006, 008, 009, 012 at v005.
  - C03 (Z_8, `Z8_CHEST_v001.tsv`): 001-v004, 007-v006 (superseded by v007, kept), 007-v007, 008-v005, 010-v006. Z_8 notes 001-v004's top-rim gap is 0.151 DW, outside the 0.25-0.58 band. **Blocked for a Chief ruling:** C03-006 (top rim under the flap) and C03-009; no file written for either.
  - C04 (Z_9, `Z9_CHEST_v003.tsv`): 005-v004 (superseded) and 005-v005 (V_4 round-1 fix, moved down the sternum); 010-v009, v010, v011 (the approved pilot) and v012 (Chief disc-rule variant).
  - C05 (Z_10, `Z10_CHEST_FULLSCALE_v001.tsv`): 001, 003, 005, 006, 008, 011, 013, 015 at v003 and 001, 003, 006, 010 at v004 (v004s fix spire/pistol clearance under 10 px in the v003s, which are kept).
  - C06 (Z_11, `Z11_FULLSCALE_STENCIL_v001.tsv`): 001-v006 superseded by v007 (clearance 6 px); 003-v005 has a script mark 7.6 px under the pistol.
  - C42-022-v005 (Z_8).
- V-Team returns posted since 10:27 (`/workspace/v1_refinv/returns/`): V_2 chest-fix z4_285k v001 and z5armor v005; V_4 crops for C04-010 v008 ink/erase, 285 v002k neck/grill and armorswap01 v004 grill.
- Still unresolved: C02-014-v007 V_5 re-measure; no QA rows for the Z_3 v003-v006 fixes, C41-002-v002 or the C04-008-v003 `_test` file. Chief needs to say which version goes forward per frame (C04-010 now has v006-v012; C04-005 v005 passed V_4 per the 11:23 READY note).
- New tips: none in TIPS-TEAM.md.
- Ziggy decisions still open: C15-001 Chewy-drift hold; soft notes on C06-005 and C06-008; REF-05; ZIGGY_CHEST_VARIANTS_v003.tsv (28 rows); challenge-list vs multiverse for unfixable chests; 20 duplicate groups (`_dedup_pass_v001/`).
- Generation: nothing generated this run; every category is at 15 or more originals and Chief's REBALANCE says no new categories.
- Nothing deleted or moved. Housekeeping is Chief's.
