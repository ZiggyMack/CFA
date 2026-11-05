# The Criminal Mind, set binding v002: the Grok set-round returns bound to the storyboard (2026-11-04)

Author: Claude (lite), the PH_Claude_Lite session, on the lead writer's review of 2026-11-05 | status: PRELIMINARY proposal, nothing selected | specialist review: none | adopted contributions: none

Written 2026-11-05 01:28 UTC. v001 stays as posted beside this file. Rests on TCM_SET_BINDING_v001_REVIEW_20261105.md (the lead writer's rulings, section 3 item 1), and on TASK_BRIEF_SET_BINDING_FOR_SONNET_20261104.md (sections 1 to 7), the set camera maps v001 with Addenda A to D, TCM_HELD_POSITIONS_RULINGS_20261102.md, the shot map delta v002 (TSV) and CFA Nova's storyboard structure v001. Nothing here selects an image; the director selects. No posted file, zip or storyboard card was edited.

## 1. What this binding is

Every still of the Grok set round is tied to the storyboard shots its camera position serves, as one row per shot and candidate still (TCM_SET_BINDING_v002.tsv). The same rows are arranged per shot in TCM_SET_BINDING_11_2_ROWS_PROPOSED_v002.json, which carries three levels of link for every shot: a cover (one placeholder still), the options (every candidate with a count) and the family (the family id, its ten-look sheet from the October 30 intake, and the contact sheets of its set-round packs), so that no card is bare. The JSON is a proposal for Nova, the card author, to apply; this file only reports.

How a still is tied to a shot (the binding rule, applied by script):

1. Family, position and light state come from the pack's own index columns, cross-checked against the filename; the position id is the maps' id (for example ALA-P01) found by the position token in the filename within the family.
2. A still binds to a shot when the maps' Serves list for that position names the shot and the still's light state is among the position's light states ("maps serves"), or when the delta's setPositions for the shot names the position with that light state ("delta setPositions"), or both ("both"). Two stills are bound by the rulings (the HEXT-P05 morning state to shot TCM-09-03, and the HOST-PX stills to TCM-40-04, which the maps list under dusk and the rulings relight to overcast day); their bindingSource names the rulings section.
3. The delta's BATH position ids occur in two families (the Henderson bathroom and the precinct washroom); each is resolved to the family whose maps row serves that shot, by script.
4. Priority (proof, needed, exploratory) is the maps' own. The four new families and the hostage-house exterior have no Priority column in v001, so their priority cells are blank.
5. An exploratory position gets rows only where the delta claims it for a shot; otherwise it is listed in section 6.
6. isTake1 is the lowest L-number among the stills of that position and light state in the packs before any ADDD, B3, LOT, HOSTPX, IDSHEET or EXTRAS pack. Where no earlier still exists (14 groups, section 12) the lowest-numbered still is take 1 by first delivery, and the row's notes say so.
7. isDefaultPlaceholder is true for exactly one row per shot, position and light state: the take 1 still if its screening tag is OK, else the lowest-numbered still tagged OK, else the take 1 still with its tag. It is a placeholder under the placeholder rule, not a selection.
8. The screening tag and note are copied verbatim from the pack's SCREENING_ROWS file, joined on the filename. They are the screeners' words, not mine, and no image was viewed or judged for this file.
9. variant is the letter in the filename or pack index (a, b, c). For the car windshield plates (position P06) the filename carries a P06 letter (a to f) and, in the rule-of-three packs, a second letter; the cell then reads the P06 letter, a hyphen and the rule-of-three letter (for example a-b). A first still that later stills name as their variantOf is marked a, and says so in notes. Otherwise the cell is blank.
10. (v002) Priority left blank in v001 is filled by review ruling 4: needed where the maps name a shot for the position, exploratory otherwise (23 positions).
11. (v002) An extra is bound only where its pack index or README says it is the reroll of a named still (review ruling 5): at the extra's own position and light state, isTake1 false, notes "reroll of Lnn". Every other extra stays listed in section 8, unbound. The identity sheet is never bound.
12. (v002) For a car group that has both identities, the default placeholder is the lowest-numbered SUV still tagged OK, else the lowest-numbered SUV still with its tag; the sedan stills stay options marked "earlier identity (Addendum B supersedes)" (review ruling 7). The SUV default sorts ahead of take 1 in the cover rule, after the OK test.
13. (v002) Option-only rows (review ruling 3 and the rooftop binding) are never the cover. TCM-09-04 and TCM-09-04-i1 take HEXT-P05 morning as an interim cover (review ruling 1). The pack's own screener name is kept beside the tag in a new last column, screener (review ruling 2).

## 1b. Changes from v001

v001 stays as posted (its report: sha256 83b58670239c1e4f6a942f652f6c877b381cdf79ae0c715d4858d74dea58ba47). v002 applies the lead writer review rulings 1, 3, 4, 5, 7 and 9 and the two rooftop and host bindings:

1. Rows: 2150 in v001, 2303 in v002; shots with at least one row: 208 in v001, 210 in v002.
2. Ruling 1: TCM-09-04 and TCM-09-04-i1 take the HEXT-P05 morning stills as an interim cover (10 rows), marked coverInterim in the JSON and INTERIM in notes.
3. Ruling 3: the five HEXT-L3 pre-dawn stills are also bound to TCM-08-01 as options only; with the rooftop bindings below, 14 option-only rows exist, never the cover.
4. Ruling 4: priority filled for 23 positions of the new families and the host exterior (needed where the maps name a shot, exploratory otherwise).
5. Ruling 5: 22 extras are bound as rerolls of a named still (132 rows), isTake1 false.
6. Ruling 7: 61 car-family rows are SUV defaults; 94 sedan take 1 rows are marked "earlier identity (Addendum B supersedes)".
7. Ruling 9: covers whose tag is not OK are flagged coverPendingCorrection (44 shots in v002, 43 in v001); no cover was withheld.
8. Rooftop and host bindings: TCM-39-08 and TCM-39-15 take ROOFTOP RT-P05 and RT-P08 as options only (RT-LS2 for both shots, RT-LS3 also for 39-15) and no longer name BARST-P01 or STREET-P05 (dropped); the dusk light cell of the maps for HOST-PX is noted as superseded in the notes of its rows.
9. Covers that changed against v001: 12 shots (8 car-family shots from the SUV rule, 4 others: TCM-09-04, TCM-09-04-i1, TCM-29-03, TCM-35-04).
10. New: the screener column (the pack own screener name beside the tag, ruling 2), and the small file TCM_SET_BINDING_SITE_DISPLAY_v002.json for Site Nova (per shot: cover, option count, family sheet paths).

## 2. Counts

| Item | Count |
| --- | --- |
| Set-round zips read | 65 |
| Original ten-look sources read (19 zips, plus the Henderson exterior folder) | 20 |
| Batch manifests read | 48 |
| Stills found in the set-round zips (the pack SHA256 sidecars list them) | 756 |
|   of which position stills (L-numbered) | 679 |
|   of which extras (X-numbered rerolls and singles; section 8) | 57 |
|   of which identity-sheet stills (ID01 to ID10, two frames; never bound, section 8) | 20 |
| Other images in the zips: contact sheets (jpg and png) | 232 |
| Other images in the zips: evidence crops (png) | 11 |
| Position stills bound to at least one shot | 617 |
| Position stills unbound (all exploratory positions that no shot claims; section 6) | 62 |
| Binding rows in the TSV (shot by candidate still, extras included) | 2303 |
| Extras bound as rerolls of a named still | 22 |
| Extras left unbound (not a named reroll, or the reroll is at a position no shot claims) | 35 |
| Shots with at least one row (of 210: Nova's 165 plus the delta's 45 sub-shots and inserts) | 210 |
| Shot, position and light groups (one default placeholder each) | 699 |

Screening tags on the 679 position stills: SCRIPT-DRIFT 263, OK 235, ADVISORY 138, QUALITY-FAIL 26, SCRIPT-MISS 16, MISS 1.

Checks run by script before hand-back:

| Check | Items tested | Failures |
| --- | --- | --- |
| file in named zip, sha256 and bytes equal the pack sidecar | 639 | 0 |
| shotId in Nova 165 or delta 210 | 2303 | 0 |
| positionId exists in v001 | 2303 | 0 |
| family of the row equals the filename family and the pack index family | 2303 | 0 |
| per-zip still counts equal the manifests | 65 | 0 |
| JSON loads; every JSON row sha256 is in the TSV | 2303 | 0 |
| exactly one default placeholder per shot, position and light | 699 | 0 |

Per-zip still counts equal the manifests' original_count, still_count or extra_count for all 65 zips named in the manifests, and the zip byte sizes equal the manifests' bytes column (0 zips differ). The sum of the manifests' counts, attributed to families, is 756, equal to the 756 stills found.

## 3. Per family

| Family | Positions in the maps | Positions delivered | Positions missing | Position stills | Bound | Extras and ID | Found (all) | Manifest count | Stills per position and light |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMPALA | 14 | 14 | none | 101 | 84 | 32 | 133 | 133 | 1 to 16 |
| HENDERSON-BATHROOM | 10 | 10 | none | 28 | 25 | 0 | 28 | 28 | 1 to 3 |
| HENDERSON-BEDROOM | 9 | 9 | none | 32 | 30 | 0 | 32 | 32 | 1 to 3 |
| PRECINCT-OFFICE | 10 | 10 | none | 36 | 36 | 2 | 38 | 38 | 3 |
| HENDERSON-LIVING | 9 | 8 | HLIV-P04 | 33 | 33 | 2 | 35 | 35 | 3 |
| CAPTAIN-OFFICE | 9 | 9 | none | 36 | 36 | 0 | 36 | 36 | 3 |
| ROOFTOP | 8 | 8 | none | 36 | 36 | 6 | 42 | 42 | 3 |
| ALLEY-A | 11 | 11 | none | 32 | 30 | 1 | 33 | 33 | 1 to 3 |
| BEAN-EATER-ALLEY | 9 | 9 | none | 32 | 30 | 4 | 36 | 36 | 1 to 3 |
| CAFE | 10 | 10 | none | 26 | 21 | 3 | 29 | 29 | 1 to 3 |
| LATE-BAR | 10 | 10 | none | 34 | 33 | 8 | 42 | 42 | 1 to 3 |
| HOSTAGE-HOUSE | 10 | 10 | none | 35 | 35 | 1 | 36 | 36 | 1 to 6 |
| HOSPITAL | 10 | 10 | none | 11 | 8 | 1 | 12 | 12 | 1 |
| HENDERSON-EXTERIOR | 6 | 6 | none | 37 | 34 | 0 | 37 | 37 | 3 to 5 |
| CHILD-HOME | 8 | 8 | none | 24 | 21 | 5 | 29 | 29 | 1 to 3 |
| PRECINCT-BATHROOM | 8 | 8 | none | 19 | 16 | 3 | 22 | 22 | 1 to 3 |
| INTERROGATION | 8 | 8 | none | 23 | 22 | 0 | 23 | 23 | 1 to 3 |
| MEETING | 8 | 8 | none | 19 | 15 | 0 | 19 | 19 | 1 to 3 |
| JUNKYARD | 8 | 8 | none | 19 | 16 | 0 | 19 | 19 | 1 to 3 |
| PRECINCT-EXTERIOR | 7 | 7 | none | 14 | 10 | 4 | 18 | 18 | 1 to 3 |
| STREET-RESIDENTIAL | 6 | 5 | STREET-P05 | 13 | 12 | 0 | 13 | 13 | 1 to 3 |
| HIGHWAY | 6 | 6 | none | 18 | 15 | 3 | 21 | 21 | 3 |
| BAR-STAIRWELL | 4 | 4 | none | 10 | 9 | 0 | 10 | 10 | 1 to 3 |
| BAR-STREET | 6 | 5 | BARST-P01 | 11 | 10 | 2 | 13 | 13 | 1 to 3 |

"Stills per position and light" is the smallest and largest number of position stills sharing one position and light state in that family (the rule of three gives three where the quality pass reached it; the car windshield plates, the Henderson exterior states and the two host exterior angles run higher because they carry lettered sub-variants or two angles at three variants).

## 4. Shots with zero candidates

None. Every shot now has at least one candidate: TCM-09-04 and TCM-09-04-i1, which had none in v001, carry HEXT-P05 morning as an interim cover (review ruling 1).

Shots with candidates for some but not all of the positions they name:

| Shot | Positions named but with no delivered still |
| --- | --- |
| TCM-09-03 | HLIV-P04 |
| TCM-09-04 | HLIV-P04 |
| TCM-09-04-i1 | HLIV-P04 |

Held or missing slots as the packs record them (verbatim from the screening rows):

| Pack | File or slot | Tag | Note (first 220 characters) |
| --- | --- | --- | --- |
| TCM-SET-BAR-STREET-L02-L06.zip | (held; not delivered) TCM-SET-BAR-STREET-L01__P01-rain-day.jpg | HELD | HELD: not screened per brief; slot S01 BARST-P01 rain-day. No file present in TCM-SET-BAR-STREET/ (consistent with the hold). |
| TCM-SET-HENDERSON-BATHROOM-L11-L23.zip | (no file) | MISSING-SLOT | L18 logged as a missing slot, NOT a defect and not counted: the L-number is unused (operator slip per BATCH_02_NAMING_NOTE; P06-LS2 saved as L19). All 12 card 6a slots are filled once. |
| TCM-SET-HOSTAGE-HOUSE-L11-L21.zip |  | HELD | PRELIMINARY; slot S12 HOST-PX house exterior, the door, light dusk (still 1 of 2) - HELD until Claude rules (V_1 batch 2 assignment); no __PX file on disk and nothing opened or screened. Card section 9 conflict: HOST-PX  |
| TCM-SET-HOSTAGE-HOUSE-L11-L21.zip |  | HELD | PRELIMINARY; slot S13 HOST-PX house exterior, the door, light dusk (still 2 of 2; variant unspecified) - HELD until Claude rules; no __PX file on disk, nothing screened. Ref ids: n/a (no still). |
| TCM-SET-STREET-RESIDENTIAL-L01-L06.zip | TCM-SET-STREET-RESIDENTIAL-L??__P05-dawn.jpg | HELD | PRELIMINARY; slot S05; position STREET-P05; light dawn; HELD by V_1 until Claude rules (card §9 conflict: dawn/front-step/kerb vs SS:L167, SS:L206, SS:L260, SS:L289); no file on disk for this slot; not screened; gap, not |

## 5. Dropped positions and the rulings

| Position | Ruling | Shots the maps still list for it | Stills delivered for it | Result |
| --- | --- | --- | --- | --- |
| BAR-STREET L01 (BARST-P01) | dropped (rulings section 1) | TCM-39-08, TCM-39-15 | 0 | none delivered |
| STREET-RESIDENTIAL P05 (STREET-P05) | dropped (rulings section 1) | TCM-09-03 | 0 | none delivered |

HEXT-P05 is delivered in two states: 5 stills at HEXT-L3 (pre-dawn) and 5 at the maker token MORNING. MORNING is bound to TCM-09-03 by the rulings file, and (v002) to TCM-09-04 and TCM-09-04-i1 as an interim cover by review ruling 1. The five HEXT-L3 pre-dawn stills stay bound to TCM-09-03 as the maps bind them and (v002) are also bound to TCM-08-01 as options only, never the cover, by review ruling 3.

HOST-PX: 6 stills (rulings: relit to overcast day, two angles) are bound to TCM-40-04, the shot the maps name for the position, by ruling; the maps' light cell for the position still reads dusk, and the delta names no HOST position for any shot.

HENDERSON-LIVING P04: the rulings file said it stands as delivered; the pack records it as held and no still exists. The review corrects that and asks the Chief for HLIV-P04 in HLIV-L2 at three variants; until it lands TCM-09-04 and TCM-09-04-i1 use the interim cover above. TCM-39-08 and TCM-39-15 lose BARST-P01 (dropped) and take ROOFTOP RT-P05 and RT-P08 as options only (39-08 in RT-LS2; 39-15 in RT-LS2 or RT-LS3). Dropped positions no longer count as positions a shot names, so TCM-09-03 shows only HLIV-P04 as named but missing.

## 6. Positions delivered that no shot claims

All 62 unbound stills are stills at positions the maps mark exploratory and that no delta shot claims. None is an orphan (an orphan would be a delivered position or light state the maps lack); the script found no orphan.

| Family | Position | Light | Priority | Maps Serves | Stills |
| --- | --- | --- | --- | --- | --- |
| IMPALA | IMPALA-P09 | IMPALA-LS04 | exploratory | exploratory (maps) | 1 |
| IMPALA | IMPALA-P11 | IMPALA-LS01 | exploratory | exploratory (maps) | 4 |
| IMPALA | IMPALA-P12 | IMPALA-LS01 | exploratory | exploratory (maps) | 4 |
| IMPALA | IMPALA-P12 | IMPALA-LS04 | exploratory | exploratory (maps) | 4 |
| IMPALA | IMPALA-P14 | IMPALA-LS04 | exploratory | exploratory (maps) | 4 |
| HENDERSON-BATHROOM | BATH-P08 | BATH-LS2 | exploratory | exploratory (maps) | 1 |
| HENDERSON-BATHROOM | BATH-P09 | BATH-LS2 | exploratory | exploratory (maps) | 1 |
| HENDERSON-BATHROOM | BATH-P10 | BATH-LS2 | exploratory | exploratory (maps) | 1 |
| HENDERSON-BEDROOM | BED-P08 | BED-LS3 | exploratory | exploratory (maps) | 1 |
| HENDERSON-BEDROOM | BED-P09 | BED-LS2 | exploratory | exploratory (maps) | 1 |
| ALLEY-A | ALA-P10 | ALA-LS1 | exploratory | exploratory (maps) | 1 |
| ALLEY-A | ALA-P11 | ALA-LS1 | exploratory | exploratory (maps) | 1 |
| BEAN-EATER-ALLEY | BEA-P08 | BEA-LS3 | exploratory | exploratory (maps) | 1 |
| BEAN-EATER-ALLEY | BEA-P09 | BEA-LS1 | exploratory | exploratory (maps) | 1 |
| CAFE | CAFE-P06 | CAFE-LS1 | exploratory | exploratory (maps) | 1 |
| CAFE | CAFE-P07 | CAFE-LS1 | exploratory | exploratory (maps) | 1 |
| CAFE | CAFE-P08 | CAFE-LS1 | exploratory | exploratory (maps) | 1 |
| CAFE | CAFE-P09 | CAFE-LS1 | exploratory | exploratory (maps) | 1 |
| CAFE | CAFE-P10 | CAFE-LS1 | exploratory | exploratory (maps) | 1 |
| LATE-BAR | LBAR-P10 | LBAR-LS1 | exploratory | exploratory (maps) | 1 |
| HOSPITAL | HOS-P08 | HOS-LS1 | exploratory | exploratory (maps) | 1 |
| HOSPITAL | HOS-P09 | HOS-LS1 | exploratory | exploratory (maps) | 1 |
| HOSPITAL | HOS-P10 | HOS-LS1 | exploratory | exploratory (maps) | 1 |
| HENDERSON-EXTERIOR | HEXT-P06 | HEXT-L2 | exploratory | exploratory (maps) | 3 |
| CHILD-HOME | CHOME-P06 | CHOME-L1 | exploratory | exploratory (maps) | 1 |
| CHILD-HOME | CHOME-P07 | CHOME-L2 | exploratory | exploratory (maps) | 1 |
| CHILD-HOME | CHOME-P08 | CHOME-L1 | exploratory | exploratory (maps) | 1 |
| PRECINCT-BATHROOM | BATH-P06 | BATH-LS1 | exploratory | exploratory (maps) | 1 |
| PRECINCT-BATHROOM | BATH-P07 | BATH-LS1 | exploratory | exploratory (maps) | 1 |
| PRECINCT-BATHROOM | BATH-P08 | BATH-LS1 | exploratory | exploratory (maps) | 1 |
| INTERROGATION | IN-P08 | IN-L1 | exploratory | exploratory (maps) | 1 |
| MEETING | ME-P07 | ME-L1 | exploratory | exploratory (maps) | 3 |
| MEETING | ME-P08 | ME-L1 | exploratory | exploratory (maps) | 1 |
| JUNKYARD | JY-P06 | JY-LS1 | exploratory | exploratory (maps) | 1 |
| JUNKYARD | JY-P07 | JY-LS1 | exploratory | exploratory (maps) | 1 |
| JUNKYARD | JY-P08 | JY-LS1 | exploratory | exploratory (maps) | 1 |
| PRECINCT-EXTERIOR | EXT-P04 | EXT-LS1 | exploratory | exploratory (maps) | 1 |
| PRECINCT-EXTERIOR | EXT-P05 | EXT-LS1 | exploratory | exploratory (maps) | 1 |
| PRECINCT-EXTERIOR | EXT-P06 | EXT-LS1 | exploratory | exploratory (maps) | 1 |
| PRECINCT-EXTERIOR | EXT-P07 | EXT-LS1 | exploratory | exploratory (maps) | 1 |
| STREET-RESIDENTIAL | STREET-P06 | night | exploratory | exploratory (maps) | 1 |
| HIGHWAY | HWY-P06 | dusk | exploratory | exploratory (maps) | 3 |
| BAR-STAIRWELL | STAIR-P04 | day | exploratory | exploratory (maps) | 1 |
| BAR-STREET | BARST-P06 | overcast-day | exploratory | exploratory (maps) | 1 |

## 7. Disagreements between the maps' Serves lists and the delta's setPositions column

Listed from both sides; nothing is decided here. A pair is a shot with a position. Counts: 22 pairs the maps name that the delta lacks; 115 pairs the delta names that the maps lack; 0 pairs on both sides whose light states differ (none).

### 7a. Named by the maps, absent from the delta

The delta carries no set positions at all for the families STREET-RESIDENTIAL, HIGHWAY, BAR-STAIRWELL and BAR-STREET, and none for HOST-PX (the maps' new families and the hostage-house exterior, written by the lead writer after the delta's audit). Their shots are bound from the maps alone ("maps serves").

| Shot | Positions the maps serve (delta lacks) |
| --- | --- |
| TCM-09-03 | STREET-P05 |
| TCM-29-03 | STREET-P01, STREET-P02, STREET-P03 |
| TCM-29-04 | STREET-P02, STREET-P04 |
| TCM-35-01 | HWY-P01 |
| TCM-35-03 | HWY-P02, HWY-P03 |
| TCM-35-04 | HWY-P04, HWY-P05 |
| TCM-39-08 | BARST-P01, STAIR-P02 |
| TCM-39-11 | STAIR-P01, STAIR-P02, STAIR-P03 |
| TCM-39-15 | BARST-P01, BARST-P02 |
| TCM-39-17 | BARST-P03, BARST-P04, BARST-P05 |
| TCM-40-04 | HOST-PX |

### 7b. Named by the delta, absent from the maps' Serves lists

All 115 are sub-shots (letter suffix) or inserts (-i suffix) whose parent shot the maps do serve at the same position; the maps' Serves lists carry parent shot ids only. The delta side is the more granular. None is a position the maps do not know.

| Shot | Parent | Positions the delta names (maps' Serves lacks the shot id) |
| --- | --- | --- |
| TCM-02-03b | TCM-02-03 | ALA-P05 |
| TCM-02-05-i1 | TCM-02-05 | ALA-P03, ALA-P04, ALA-P07 |
| TCM-02-06b | TCM-02-06 | ALA-P01, ALA-P03, ALA-P07 |
| TCM-02-06c | TCM-02-06 | ALA-P01, ALA-P03, ALA-P07 |
| TCM-03-01-i1 | TCM-03-01 | IMPALA-P01, IMPALA-P03 |
| TCM-09-02-i1 | TCM-09-02 | HLIV-P03 |
| TCM-09-04-i1 | TCM-09-04 | HLIV-P04 |
| TCM-11-01-i1 | TCM-11-01 | IMPALA-P01, IMPALA-P06 |
| TCM-11-03-i1 | TCM-11-03 | IMPALA-P03, IMPALA-P04, IMPALA-P06, IMPALA-P07 |
| TCM-15-01-i1 | TCM-15-01 | OFF-P03 |
| TCM-16-03-i1 | TCM-16-03 | JY-P02, JY-P03, JY-P04 |
| TCM-16-03b | TCM-16-03 | JY-P02, JY-P03, JY-P04 |
| TCM-16-03c | TCM-16-03 | JY-P02, JY-P03, JY-P04 |
| TCM-16-04-i1 | TCM-16-04 | JY-P01, JY-P04, JY-P05 |
| TCM-17-04b | TCM-17-04 | IN-P01, IN-P03, IN-P04, IN-P05 |
| TCM-21-02-i1 | TCM-21-02 | BEA-P03, BEA-P05 |
| TCM-22-01-i1 | TCM-22-01 | HEXT-P01, HEXT-P04, HLIV-P01, HLIV-P09 |
| TCM-23-01-i1 | TCM-23-01 | IMPALA-P01, IMPALA-P03 |
| TCM-24-01-i1 | TCM-24-01 | BEA-P01, BEA-P03, BEA-P05 |
| TCM-24-01-i2 | TCM-24-01 | BEA-P01, BEA-P03, BEA-P05 |
| TCM-24-01b | TCM-24-01 | BEA-P01, BEA-P03, BEA-P05 |
| TCM-24-01c | TCM-24-01 | BEA-P01, BEA-P03, BEA-P05 |
| TCM-24-02-i1 | TCM-24-02 | BEA-P03, BEA-P05, BEA-P07 |
| TCM-24-04-i1 | TCM-24-04 | BEA-P02, BEA-P03 |
| TCM-24-04-i2 | TCM-24-04 | BEA-P02, BEA-P03 |
| TCM-24-04-i3 | TCM-24-04 | BEA-P02, BEA-P03 |
| TCM-24-04b | TCM-24-04 | BEA-P02, BEA-P03 |
| TCM-25-01-i1 | TCM-25-01 | OFF-P01, OFF-P10 |
| TCM-27-01-i1 | TCM-27-01 | BATH-P01, BATH-P02, BATH-P03, BATH-P07, BED-P04 |
| TCM-27-02-i1 | TCM-27-02 | BATH-P02, BATH-P04 |
| TCM-27-04-i1 | TCM-27-04 | BATH-P04, BATH-P05, BATH-P06 |
| TCM-27-05-i1 | TCM-27-05 | BATH-P06, BATH-P07 |
| TCM-27-05-i2 | TCM-27-05 | BATH-P06, BATH-P07 |
| TCM-27-06b | TCM-27-06 | BATH-P04, BATH-P05, BATH-P07, BED-P01, BED-P04 |
| TCM-29-01-i1 | TCM-29-01 | IMPALA-P05, IMPALA-P08 |
| TCM-35-01-i1 | TCM-35-01 | IMPALA-P05, IMPALA-P06 |
| TCM-36-07-i1 | TCM-36-07 | HLIV-P05, HLIV-P07 |
| TCM-38-02-i1 | TCM-38-02 | LBAR-P01, LBAR-P03, LBAR-P04 |
| TCM-39-01-i1 | TCM-39-01 | RT-P01, RT-P03, RT-P07 |
| TCM-39-17-i1 | TCM-39-17 | RT-P08 |
| TCM-39-17b | TCM-39-17 | RT-P08 |
| TCM-39-17c | TCM-39-17 | RT-P08 |
| TCM-40-05-i1 | TCM-40-05 | HH-P02, HH-P03, HH-P04 |
| TCM-40-09-i1 | TCM-40-09 | HH-P06, HH-P07, HH-P08 |
| TCM-41-05-i1 | TCM-41-05 | HOS-P02, HOS-P03, HOS-P04, HOS-P06, HOS-P07 |

### 7c. Light states

For every pair named on both sides with a light list, the maps' light cell and the delta's list agree. One maps/ruling difference of light rather than shot: HOST-PX is dusk in the maps and overcast day by the rulings.

## 8. The identity sheet and the extras (listed here, not bound)

The identity sheet (TCM-SET-IMPALA-IDSHEET-01-ID01-ID10.zip, Addendum C): ten present-day unmarked SUVs, each in frame A (P08, LS05, day, at the driver door) and frame B (P12, LS04, day, from the rear corner). Twenty stills; never bound to shots; the director picks one car. Zip: TCM-SET-IMPALA-IDSHEET-01-ID01-ID10.zip.

| Car | Frame A file | Screening tag | Frame B file | Screening tag |
| --- | --- | --- | --- | --- |
| ID01 | TCM-SET-IMPALA-ID01__P08-LS05.jpg | ADVISORY | TCM-SET-IMPALA-ID01__P12-LS04.jpg | ADVISORY |
| ID02 | TCM-SET-IMPALA-ID02__P08-LS05.jpg | SCRIPT-DRIFT | TCM-SET-IMPALA-ID02__P12-LS04.jpg | SCRIPT-DRIFT |
| ID03 | TCM-SET-IMPALA-ID03__P08-LS05.jpg | ADVISORY | TCM-SET-IMPALA-ID03__P12-LS04.jpg | OK |
| ID04 | TCM-SET-IMPALA-ID04__P08-LS05.jpg | OK | TCM-SET-IMPALA-ID04__P12-LS04.jpg | ADVISORY |
| ID05 | TCM-SET-IMPALA-ID05__P08-LS05.jpg | ADVISORY | TCM-SET-IMPALA-ID05__P12-LS04.jpg | OK |
| ID06 | TCM-SET-IMPALA-ID06__P08-LS05.jpg | OK | TCM-SET-IMPALA-ID06__P12-LS04.jpg | ADVISORY |
| ID07 | TCM-SET-IMPALA-ID07__P08-LS05.jpg | ADVISORY | TCM-SET-IMPALA-ID07__P12-LS04.jpg | OK |
| ID08 | TCM-SET-IMPALA-ID08__P08-LS05.jpg | ADVISORY | TCM-SET-IMPALA-ID08__P12-LS04.jpg | OK |
| ID09 | TCM-SET-IMPALA-ID09__P08-LS05.jpg | ADVISORY | TCM-SET-IMPALA-ID09__P12-LS04.jpg | OK |
| ID10 | TCM-SET-IMPALA-ID10__P08-LS05.jpg | SCRIPT-DRIFT | TCM-SET-IMPALA-ID10__P12-LS04.jpg | SCRIPT-DRIFT |

The 57 extras (rerolls and single stills in the X packs and the TCM-SETROUND-EXTRAS packs). They are not binding rows under the brief; the position they sit at and the shots that position serves are visible in the maps. Review ruling 5 binds only the named rerolls (column Bound as); the rest stay listed.

| Family | File | Zip | Position | Light | Screening tag | Bound as |
| --- | --- | --- | --- | --- | --- | --- |
| ALLEY-A | TCM-SET-ALLEY-A-X01__P09-LS1.jpg | TCM-SETROUND-EXTRAS-01.zip | ALA-P09 | ALA-LS1 | ALA-LS1 | reroll of L20 (rows: 1) |
| BAR-STREET | TCM-SET-BAR-STREET-X01__P02-rain-day.jpg | TCM-SETROUND-EXTRAS-01.zip | BARST-P02 | rain-day | rain-day | reroll of L02 (rows: 1) |
| BAR-STREET | TCMSET_B3_TCM-SET-BAR-STREET-X02__P04-rain-day.jpg | TCM-SET-BAR-STREET-EXTRAS-X02.zip | BARST-P04 | rain-day | SCRIPT-DRIFT | reroll of L09 (rows: 1) |
| BEAN-EATER-ALLEY | TCMSET_B3_BEAN-EATER-ALLEY_X01__P03-LS2.jpg | TCM-SET-BEAN-EATER-ALLEY-EXTRAS-X01-X04.zip | BEA-P03 | BEA-LS2 | OK | not bound |
| BEAN-EATER-ALLEY | TCMSET_B3_BEAN-EATER-ALLEY_X02__P05-LS2.jpg | TCM-SET-BEAN-EATER-ALLEY-EXTRAS-X01-X04.zip | BEA-P05 | BEA-LS2 | OK | not bound |
| BEAN-EATER-ALLEY | TCMSET_B3_BEAN-EATER-ALLEY_X03__P07-LS1.jpg | TCM-SET-BEAN-EATER-ALLEY-EXTRAS-X01-X04.zip | BEA-P07 | BEA-LS1 | ADVISORY | not bound |
| BEAN-EATER-ALLEY | TCMSET_B3_BEAN-EATER-ALLEY_X04__P07-LS1.jpg | TCM-SET-BEAN-EATER-ALLEY-EXTRAS-X01-X04.zip | BEA-P07 | BEA-LS1 | SCRIPT-DRIFT | not bound |
| CAFE | TCM-SET-CAFE-X01__P09-LS1.jpg | TCM-SETROUND-EXTRAS-02.zip | CAFE-P09 | CAFE-LS1 | SCRIPT-DRIFT | not bound |
| CAFE | TCMSET_B3_CAFE_X02__P02-LS1.jpg | TCM-SET-CAFE-EXTRAS-X02-X03.zip | CAFE-P02 | CAFE-LS1 | OK | not bound |
| CAFE | TCMSET_B3_CAFE_X03__P05-LS1.jpg | TCM-SET-CAFE-EXTRAS-X02-X03.zip | CAFE-P05 | CAFE-LS1 | QUALITY-FAIL | not bound |
| CHILD-HOME | TCMSET_B3_CHILD-HOME_X01.jpg | TCM-SET-CHILD-HOME-ADDD-L21-L34-X01-X05.zip |  |  | OK | not bound |
| CHILD-HOME | TCMSET_B3_CHILD-HOME_X02.jpg | TCM-SET-CHILD-HOME-ADDD-L21-L34-X01-X05.zip |  |  | OK | not bound |
| CHILD-HOME | TCMSET_B3_CHILD-HOME_X03.jpg | TCM-SET-CHILD-HOME-ADDD-L21-L34-X01-X05.zip |  |  | OK | not bound |
| CHILD-HOME | TCMSET_B3_CHILD-HOME_X04.jpg | TCM-SET-CHILD-HOME-ADDD-L21-L34-X01-X05.zip |  |  | OK | not bound |
| CHILD-HOME | TCMSET_B3_CHILD-HOME_X05.jpg | TCM-SET-CHILD-HOME-ADDD-L21-L34-X01-X05.zip |  |  | OK | not bound |
| HENDERSON-LIVING | TCM-SET-HENDERSON-LIVING-X01__P09-L1.jpg | TCM-SETROUND-EXTRAS-01.zip | HLIV-P09 | HLIV-L1 | HLIV-L1 | reroll of L22 (rows: 3) |
| HENDERSON-LIVING | TCMSET_B3_HENDERSON-LIVING_X02__P01-L1.jpg | TCM-SET-Z8-EXTRAS-LIVING-X02-PBATH-X01-X03.zip | HLIV-P01 | HLIV-L1 | QUALITY-FAIL | reroll of L34 (rows: 4) |
| HIGHWAY | TCMSET_B3_HIGHWAY_X01__P03-day-c.jpg | TCM-SET-HIGHWAY-L01-L06-X01-X03.zip | HWY-P03 | day | ADVISORY | not bound |
| HIGHWAY | TCMSET_B3_HIGHWAY_X02__P04-day-c.jpg | TCM-SET-HIGHWAY-L01-L06-X01-X03.zip | HWY-P04 | day | SCRIPT-DRIFT | not bound |
| HIGHWAY | TCMSET_B3_HIGHWAY_X03__P02-day-c.jpg | TCM-SET-HIGHWAY-L01-L06-X01-X03.zip | HWY-P02 | day | ADVISORY | not bound |
| HOSPITAL | TCM-SET-HOSPITAL-X01__P10-LS1.jpg | TCM-SETROUND-EXTRAS-01.zip | HOS-P10 | HOS-LS1 | OK | not bound |
| HOSTAGE-HOUSE | TCMSET_B3_TCM-SET-HOSTAGE-HOUSE-X01__P03-LS1.jpg | TCM-SET-HOSTAGE-HOUSE-EXTRAS-X01.zip | HH-P03 | HH-LS1 | ADVISORY | not bound |
| IMPALA | TCM-SET-IMPALA-X01__P11-LS01.jpg | TCM-SETROUND-EXTRAS-01.zip | IMPALA-P11 | IMPALA-LS01 | SCRIPT-DRIFT | not bound |
| IMPALA | TCM-SET-IMPALA-X02__P03-LS04.jpg | TCM-SETROUND-EXTRAS-01.zip | IMPALA-P03 | IMPALA-LS04 | ADVISORY | reroll of L22 (rows: 7) |
| IMPALA | TCM-SET-IMPALA-X03__P06-LS04-c.jpg | TCM-SETROUND-EXTRAS-01.zip | IMPALA-P06 | IMPALA-LS04 | QUALITY-FAIL | reroll of L28 (rows: 11) |
| IMPALA | TCM-SET-IMPALA-X04__P06-LS04-c.jpg | TCM-SETROUND-EXTRAS-01.zip | IMPALA-P06 | IMPALA-LS04 | SCRIPT-DRIFT | reroll of L28 (rows: 11) |
| IMPALA | TCMSET_B3_IMPALA_X05__P03-LS01.jpg | TCM-SETROUND-EXTRAS-03.zip | IMPALA-P03 | IMPALA-LS01 | ADVISORY | reroll of L42 (rows: 7) |
| IMPALA | TCMSET_B3_IMPALA_X06__P06-LS04-c.jpg | TCM-SETROUND-EXTRAS-03.zip | IMPALA-P06 | IMPALA-LS04 | QUALITY-FAIL | reroll of L47 (rows: 11) |
| IMPALA | TCMSET_B3_IMPALA_X07__P06-LS04-d.jpg | TCM-SETROUND-EXTRAS-03.zip | IMPALA-P06 | IMPALA-LS04 | ADVISORY | reroll of L48 (rows: 11) |
| IMPALA | TCMSET_B3_IMPALA_X08__P06-LS04-c.jpg | TCM-SETROUND-EXTRAS-04.zip | IMPALA-P06 | IMPALA-LS04 | SCRIPT-DRIFT | reroll of L47 and X06 (rows: 11) |
| IMPALA | TCMSET_B3_IMPALA_X09__P06-LS04-c-c.jpg | TCM-SET-IMPALA-EXTRAS-X09-X11.zip | IMPALA-P06 | IMPALA-LS04 | ADVISORY | reroll of L47 (rows: 11) |
| IMPALA | TCMSET_B3_IMPALA_X10__P06-LS04-d-b.jpg | TCM-SET-IMPALA-EXTRAS-X09-X11.zip | IMPALA-P06 | IMPALA-LS04 | SCRIPT-DRIFT | reroll of L48 (rows: 11) |
| IMPALA | TCMSET_B3_IMPALA_X11__P13-LS01-b.jpg | TCM-SET-IMPALA-EXTRAS-X09-X11.zip | IMPALA-P13 | IMPALA-LS01 | ADVISORY | reroll of L56 (rows: 1) |
| IMPALA | TCMSET_B3_IMPALA_X15__P02-LS04.jpg | TCM-SET-IMPALA-EXTRAS-X15.zip | IMPALA-P02 | IMPALA-LS04 | QUALITY-FAIL | not bound |
| LATE-BAR | TCM-SET-LATE-BAR-X01.jpg | TCM-SETROUND-EXTRAS-01.zip |  |  | QUALITY-FAIL | not bound |
| LATE-BAR | TCM-SET-LATE-BAR-X02.jpg | TCM-SETROUND-EXTRAS-01.zip |  |  | OK | not bound |
| LATE-BAR | TCM-SET-LATE-BAR-X03.jpg | TCM-SETROUND-EXTRAS-01.zip |  |  | OK | not bound |
| LATE-BAR | TCM-SET-LATE-BAR-X04.jpg | TCM-SETROUND-EXTRAS-01.zip |  |  | OK | not bound |
| LATE-BAR | TCM-SET-LATE-BAR-X05.jpg | TCM-SETROUND-EXTRAS-01.zip |  |  | OK | not bound |
| LATE-BAR | TCM-SET-LATE-BAR-X06.jpg | TCM-SETROUND-EXTRAS-01.zip |  |  | OK | not bound |
| LATE-BAR | TCM-SET-LATE-BAR-X07.jpg | TCM-SETROUND-EXTRAS-01.zip |  |  | OK | not bound |
| LATE-BAR | TCM-SET-LATE-BAR-X08__P05-LS1.jpg | TCM-SETROUND-EXTRAS-01.zip | LBAR-P05 | LBAR-LS1 | LBAR-LS1 | reroll of L15 (rows: 1) |
| PRECINCT-BATHROOM | TCMSET_B3_PRECINCT-BATHROOM_X01__P01-LS2.jpg | TCM-SET-Z8-EXTRAS-LIVING-X02-PBATH-X01-X03.zip | BATH-P01 | BATH-LS2 | ADVISORY | not bound |
| PRECINCT-BATHROOM | TCMSET_B3_PRECINCT-BATHROOM_X02__P06-LS1.jpg | TCM-SET-Z8-EXTRAS-LIVING-X02-PBATH-X01-X03.zip | BATH-P06 | BATH-LS1 | SCRIPT-DRIFT | not bound |
| PRECINCT-BATHROOM | TCMSET_B3_PRECINCT-BATHROOM_X03__P08-LS1.jpg | TCM-SET-Z8-EXTRAS-LIVING-X02-PBATH-X01-X03.zip | BATH-P08 | BATH-LS1 | ADVISORY | not bound |
| PRECINCT-EXTERIOR | TCMSET_B3_PRECINCT-EXTERIOR_X01__P06-LS1.jpg | TCM-SET-PRECINCT-EXTERIOR-ADDD-L19-L24-X01-X04.zip | EXT-P06 | EXT-LS1 | OK | not bound |
| PRECINCT-EXTERIOR | TCMSET_B3_PRECINCT-EXTERIOR_X02__P07-LS1.jpg | TCM-SET-PRECINCT-EXTERIOR-ADDD-L19-L24-X01-X04.zip | EXT-P07 | EXT-LS1 | SCRIPT-DRIFT | not bound |
| PRECINCT-EXTERIOR | TCMSET_B3_PRECINCT-EXTERIOR_X03__P02-LS1.jpg | TCM-SET-PRECINCT-EXTERIOR-ADDD-L19-L24-X01-X04.zip | EXT-P02 | EXT-LS1 | OK | not bound |
| PRECINCT-EXTERIOR | TCMSET_B3_PRECINCT-EXTERIOR_X04__P03-LS1.jpg | TCM-SET-PRECINCT-EXTERIOR-ADDD-L19-L24-X01-X04.zip | EXT-P03 | EXT-LS1 | ADVISORY | not bound |
| PRECINCT-OFFICE | TCM-SET-PRECINCT-OFFICE-X01__P04-LS2.jpg | TCM-SET-PRECINCT-OFFICE-ADDD-L23-L46-X01-X02.zip | OFF-P04 | OFF-LS2 | ADVISORY | not bound |
| PRECINCT-OFFICE | TCM-SET-PRECINCT-OFFICE-X02__P06-LS1.jpg | TCM-SET-PRECINCT-OFFICE-ADDD-L23-L46-X01-X02.zip | OFF-P06 | OFF-LS1 | ADVISORY | not bound |
| ROOFTOP | TCM-SET-ROOFTOP-X01__P05-LS2.jpg | TCM-SETROUND-EXTRAS-01.zip | RT-P05 | RT-LS2 | RT-LS2 | reroll of L16 (rows: 3) |
| ROOFTOP | TCMSET_B3_TCM-SET-ROOFTOP-X02__P01-LS3.jpg | TCM-SET-ROOFTOP-EXTRAS-X02-X05.zip | RT-P01 | RT-LS3 | SCRIPT-DRIFT | reroll of L24 (rows: 5) |
| ROOFTOP | TCMSET_B3_TCM-SET-ROOFTOP-X03__P08-LS2.jpg | TCM-SET-ROOFTOP-EXTRAS-X02-X05.zip | RT-P08 | RT-LS2 | QUALITY-FAIL | reroll of L36 (rows: 6) |
| ROOFTOP | TCMSET_B3_TCM-SET-ROOFTOP-X04__P05-LS2.jpg | TCM-SET-ROOFTOP-EXTRAS-X02-X05.zip | RT-P05 | RT-LS2 | SCRIPT-DRIFT | reroll of L38 (rows: 3) |
| ROOFTOP | TCMSET_B3_TCM-SET-ROOFTOP-X05__P08-LS3.jpg | TCM-SET-ROOFTOP-EXTRAS-X02-X05.zip | RT-P08 | RT-LS3 | SCRIPT-DRIFT | reroll of L39 (rows: 6) |
| ROOFTOP | TCMSET_B3_TCM-SET-ROOFTOP-X06__P08-LS2.jpg | TCM-SET-ROOFTOP-EXTRAS2-X06.zip | RT-P08 | RT-LS2 | QUALITY-FAIL | reroll of L36 (rows: 6) |

## 9. Cover, options, family: the three levels of link (brief section 7)

| Level reached | Shots |
| --- | --- |
| Cover with a screening tag OK (take 1 where it is OK) | 166 |
| Options, but the default placeholder is not tagged OK (cover pending correction) | 44 |
| Family link only (no candidate still for any position the shot names) | 0 |
| Nothing (no still and no family image) | 0 |

Cover rule (mine, a placeholder rule and not a selection): among the shot's default placeholder rows, tag OK first, then take 1, then priority (proof, needed, other), then the order in which the delta (else the maps) lists the shot's positions, then the lowest L-number. Review ruling 8 accepts this rule; ruling 7 inserts the SUV default of the car family after the OK test. Covers whose tag is not OK are flagged coverPendingCorrection in the JSON, interim covers coverInterim; the distinct cover files behind the pending ones number 19.


Shots whose cover is not tagged OK:

| Cover tag | Cover file | Shots |
| --- | --- | --- |
| ADVISORY | TCM-SET-CAFE-L17__P05-LS1.jpg | TCM-18-04 |
| ADVISORY | TCM-SET-CAPTAIN-OFFICE-L13__P02-DAY.jpg | TCM-14-03, TCM-14-05, TCM-40-03 |
| ADVISORY | TCMSET_B3_IMPALA_L45__P06-LS01-a-b.jpg | TCM-23-03 |
| QUALITY-FAIL | TCM-SET-ROOFTOP-L16__P05-LS2.jpg | TCM-39-08, TCM-39-16 |
| SCRIPT-DRIFT | TCM-SET-ALLEY-A-L11__P01-LS1.jpg | TCM-02-01, TCM-02-06, TCM-02-06b, TCM-02-06c, TCM-04-03 |
| SCRIPT-DRIFT | TCM-SET-ALLEY-A-L13__P02-LS1.jpg | TCM-04-01 |
| SCRIPT-DRIFT | TCM-SET-CAPTAIN-OFFICE-L11__P01-DAY.jpg | TCM-33-01, TCM-33-03, TCM-40-01, TCM-40-10 |
| SCRIPT-DRIFT | TCM-SET-HENDERSON-BEDROOM-L11__P01-N1.jpg | TCM-07-01 |
| SCRIPT-DRIFT | TCM-SET-HENDERSON-LIVING-L16__P03-L2.jpg | TCM-09-01, TCM-09-02, TCM-09-02-i1 |
| SCRIPT-DRIFT | TCM-SET-HENDERSON-LIVING-L21__P08-L4.jpg | TCM-36-02, TCM-36-05, TCM-36-06 |
| SCRIPT-DRIFT | TCM-SET-IMPALA-L32__P07-LS04.jpg | TCM-35-03 |
| SCRIPT-DRIFT | TCM-SET-JUNKYARD-L11__P01-LS1.jpg | TCM-16-01 |
| SCRIPT-DRIFT | TCM-SET-PRECINCT-BATHROOM-L16__P05-LS1.jpg | TCM-31-04 |
| SCRIPT-DRIFT | TCM-SET-PRECINCT-OFFICE-L14__P03-LS1.jpg | TCM-15-01, TCM-15-01-i1, TCM-15-03, TCM-30-01, TCM-30-03, TCM-32-01, TCM-34-02 |
| SCRIPT-DRIFT | TCM-SET-PRECINCT-OFFICE-L15__P04-LS1.jpg | TCM-30-02, TCM-32-02, TCM-32-03 |
| SCRIPT-DRIFT | TCM-SET-PRECINCT-OFFICE-L18__P06-LS1.jpg | TCM-13-02, TCM-32-04 |
| SCRIPT-DRIFT | TCM-SET-PRECINCT-OFFICE-L20__P08-LS1.jpg | TCM-30-04 |
| SCRIPT-DRIFT | TCM-SET-ROOFTOP-L18__P06-LS2.jpg | TCM-39-09 |
| SCRIPT-DRIFT | TCM-SET-ROOFTOP-L21__P08-LS2.jpg | TCM-39-17-i1, TCM-39-17b, TCM-39-17c |

Shots with the family link only: .

Shots with nothing: none.

Family level in the JSON: every family has its set-round contact sheets (244 sheet images across the families, jpg and png, from the packs' own CONTACT_SHEET, MAKER and V-series sheet files, counted once per family they serve); 19 families have the ten-look sheet from the October 30 intake (the four new families have none); the author's recorded pick TCM-SET-HENDERSON-EXTERIOR-L03 is carried on the Henderson exterior family and its shots (authorPick).

## 10. Method and scripts

Every count above comes from a script run in this session, kept in the session scratchpad (C:\Users\Stephen\AppData\Local\Temp\claude\4ee6a18a9621c041\e584f9c0-4b3f-41aa-9fb2-92905ce74de2\scratchpad\) and run with python -I. Zips were read in place with the zipfile module (nothing was extracted, nothing written to C: or D: other than the three outputs); hashes were computed from the zip members. Scripts: load.py (sha256 df95812eb777), maps.py (sha256 1f137311fdf4), resolve.py (sha256 2854cdd6aba1), stills.py (sha256 c37d57734df3), build.py (sha256 5a05c6656ce1), data2.py (sha256 7f9f06c073d0), out1.py (sha256 d42e64dfe089), v2.py (sha256 69a0e8116449), stats2.py (sha256 c3a1213b632b), out2v2.py (sha256 068ce25c3c76).

## 11. Outputs

| File | sha256 | Bytes |
| --- | --- | --- |
| TCM_SET_BINDING_SITE_DISPLAY_v002.json | f9d6800aa773ff38897d881a9dadb43153ef281fb986969e330c1d7a893ace49 | 806994 |
| TCM_SET_BINDING_v002.tsv | 24db3c66544f0d28f60df5ea36aad9f8ff44c073423869e5d883024987e07943 | 2605124 |
| TCM_SET_BINDING_11_2_ROWS_PROPOSED_v002.json | ddda880cd7475a0d0a7bac35e737e322c238fe62d1d46a29b46078493b700333 | 6293058 |
| TCM_SET_BINDING_v002.md | printed in the hand-back message and in chat (a file cannot hold its own hash) | see the hand-back message |

If this file is revised before the writer posts it, my own three files are overwritten and the revision is stated here.

## 12. Open points for the writer (none guessed)

1. The review asks the Chief for HLIV-P04 in HLIV-L2 and for corrections of the cover files behind the covers whose tag is not OK; when they land, a later binding moves the covers. The interim covers of TCM-09-04 and TCM-09-04-i1 stay until then.
2. 35 extras and the 20 identity-sheet stills stay unbound.
3. 2 screening notes quote a real car make or model (files: TCMSET_B3_HIGHWAY_L03__P03-day-a.jpg, TCMSET_B3_HIGHWAY_L03__P03-day-c.jpg). Kept verbatim; Nova applies the tag, not the note.

Claude (lite)
