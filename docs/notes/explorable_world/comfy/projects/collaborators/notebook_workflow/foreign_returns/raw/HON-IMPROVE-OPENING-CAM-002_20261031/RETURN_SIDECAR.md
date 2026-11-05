# RETURN_SIDECAR — HON-IMPROVE-OPENING-CAM-002 (raw return, 2026-10-31)

Round ID: HON-IMPROVE-OPENING-CAM-002
Project: hon_dolo
Owner: PanHandlers Claude (CFA lead writer); driver: Nyquist repo Claude (Q1 + readback by the driving session; Q2, Q3, Q4 and second pass by an Opus 5.5 worker it spawned)
Destination notebook ID: 586b3ee6-5c57-45b3-a59d-a2e21c18a852 ("Notebook 1 — Hon Dolo · Strictly Business")
Status: RAW. Every claim below is a provider claim, unreviewed. Nothing sent, executed or accepted.

## Two runs

**Run B is the return that satisfies the round's "v2 only" contract. Run A is kept as dated history.**

**Run A, 2026-10-31 09:25–09:50 EDT. Source selection uncertain.** It probably used v2 plus the three Gemini chat sources, with the import off. Evidence: the composer chip read "docs (4)" in every turn, and the "Chats from Gemini (3)" group was drawn checked with class `mdc-checkbox--selected` while its native `.checked` read false. The Drive switch was ON for the readback and Q1, and OFF from Q2 on. The "Notebook 0" mention in the run A closing lines was first listed as evidence, but run B (v2 only) produced it too, so it is not evidence.

| Run A file | Bytes | SHA-256 |
|---|---|---|
| READBACK_RESPONSE.txt | 2,114 | 00201369f80cad1a9eb02b479300917efe63f005ca9704a1c0a399ae4191a706 |
| GEMINI_RESPONSE_Q1.txt | 16,548 | 941a79ccef900b63c75123d3e88975d9018204908cbcd815fc3a618df9577d08 |
| GEMINI_RESPONSE_Q2.txt | 15,931 | 3460ab0bfd198b2a40570e5a8df224b623184b270e42882ea7189299ea367ef7 |
| GEMINI_RESPONSE_Q3.txt | 9,584 | b8ffb89ac1772f0486a9a2d635557dfa1764d709d8acf2b80ac90dc302000264 |
| GEMINI_RESPONSE_Q4.txt | 4,305 | 257888bc36e51ff65ebec51c79136829f8de1e6c90f15376a7a8a9568c52a1cf |
| GEMINI_RESPONSE_SECONDPASS.txt | 1,286 | 577f7d01953e4ff8fdf45949e4f2c346c5be4d534ff8c8b2f865786482fde1ea |

**Run B, 2026-10-31 09:58–10:15 EDT. v2 only, verified three ways.** The selection was set by real clicks on the Sources tab. Before every send the driver checked:
- (a) the drawn state: only the v2 input carries `mdc-checkbox--selected` and `.checked`, and a zoomed screenshot showed only v2 ticked;
- (b) the composer chip read "docs (1)";
- (c) once, at 09:59:29, a retrieval probe listed only "HON-OPENING-SOURCE v2 | HON-IMPROVE-OPENING-CAM-0…" (`PROBE_V2ONLY.txt`).

The Drive switch was OFF throughout. Every prompt was hash-matched in the page before sending.

| Run B file | Sent (EDT) | Bytes | SHA-256 |
|---|---|---|---|
| PROBE_V2ONLY.txt | 09:59:29 | see MANIFEST.csv | see MANIFEST.csv |
| READBACK_RESPONSE_v2only.txt | 10:00:41 | 838 | 2073b4736b9850afae3e75d7636cd917dd842f8c1b438d3ee7b2962e4bfa443a |
| GEMINI_RESPONSE_Q1_v2only.txt | 10:02:25 | 16,584 | cdb80d8ed86c2e1656aa00cf588cc889b39b33b974bc95d167e3ea546f442196 |
| GEMINI_RESPONSE_Q2_v2only.txt | 10:05:42 | 15,939 | fdb762fa982b3aca6c2b23dd7449fd9f4c12f6be553a404785d1174c8259b888 |
| GEMINI_RESPONSE_Q3_v2only.txt | 10:08:05 | 10,524 | 190cb8829d59ab3d3a17f73fc8c3a26cf5d5366adc6fbe95244a1410ae548116 |
| GEMINI_RESPONSE_Q4_v2only.txt | 10:11:08 | 4,326 | 3587aab522bd7003b51038979c4176153d72789ec1ad750a8adf8280960cccf7 |
| GEMINI_RESPONSE_SECONDPASS_v2only.txt | 10:13:17 | 833 | 9a72ffa22c324315cb66b6cd98962e3071df834ca20207c3a4e3f70509abb7ce |

The run B readback prompt is `PROMPT_READBACK.txt`, the same text as in READBACK_RESPONSE.txt. Run B used the same PROMPT_Q1..Q4 and PROMPT_SECONDPASS files as run A.

Caveats for run B:
- Run B was asked in the same chat thread after run A, so run A's answers were visible to the model as history. Run B's answers are near-identical to run A's. They confirm that the run A content holds under v2 only, but run B is not a fresh blind run.
- Citation chips rendered in run B Q1 only. They are kept inline as "[n]", and the chip overflow icon is kept as "[more]". With only v2 selected, every chip points into v2.
- Run B Q3 contains markdown beat tables written with literal "\n" characters, kept verbatim.
- The run B files were checked against an in-page SHA-256 of the cleaned text. Q1, Q2 and Q3 were written by applying the in-page token diff (run A to run B) to the run A files, then checked against that hash.

The sections below describe run A as first filed. They apply to run B too, except for the selection.

## Capture after actual execution (fields from source_packet/ROUND_REQUEST.template.txt)

**Prompt exactly as sent:** the PROMPT files in this folder, byte for byte.
- `PROMPT_Q1.txt` (Q1), `PROMPT_Q2.txt`, `PROMPT_Q3.txt`, `PROMPT_Q4.txt`, `PROMPT_SECONDPASS.txt` (the second-pass text from the Nyquist README "HOW TO CONTINUE" step 4; no trailing newline).
- For Q2, Q3, Q4 and the second pass the query box content was hashed in the page (SHA-256 of the textarea value) before sending and matched the file's SHA-256 exactly (see MANIFEST.csv).
- The readback prompt is quoted at the top of `READBACK_RESPONSE.txt`.

**Chat/response URL:** https://notebook.google.com/notebook/586b3ee6-5c57-45b3-a59d-a2e21c18a852 (NotebookLM has no per-message URL or response ID; each answer is located in the notebook's chat by its marker line `HON-IMPROVE-OPENING-CAM-002 Qn` / `HON-IMPROVE-OPENING-CAM-002 SECOND-PASS` / `HON-IMPROVE-OPENING-CAM-002 READBACK`).

**Provider and visible model/mode:** Gemini Notebook (NotebookLM), model not displayed. Each answer had a collapsed "Thoughts" toggle (not expanded, not captured).

**Selected sources actually used (per question):**

| Question | Local time sent (2026-10-31) | Source checkboxes ticked (DOM) | Chat filter "Google Drive" switch |
|---|---|---|---|
| READBACK | ~09:25 | "HON-OPENING-SOURCE v2 \| HON-IMPROVE-OPENING-CAM-0…" only | ON (default; not yet found) |
| Q1 | ~09:28 | v2 only | ON (default; turned OFF at ~09:40 after Q1) |
| Q2 | 09:40:35 | v2 only | OFF (aria-checked=false, checked before send) |
| Q3 | 09:44:28 | v2 only | OFF (checked before send) |
| Q4 | 09:47:19 | v2 only | OFF (checked before send) |
| SECOND-PASS | 09:50:08 | v2 only | OFF (checked before send) |

Unticked throughout the questions by the native checkbox property: "Chats from Gemini (3)" group ("Select all Gemini chat sources") and "01_HON_DOLO_IMPORT.txt".

**CAVEAT — source selection is uncertain (found after the second pass, 09:52–09:55).** Three observations disagree with "v2 only":
1. The composer's source chip read "docs (4)" in every turn (readback, Q1–Q4, second pass). The notebook has 5 sources (3 Gemini chats + import + v2); with everything ticked the chip read "docs (5)". So "4" fits "3 chats + v2", not "v2 only".
2. On the Sources tab, the "Chats from Gemini (3)" group checkbox was drawn checked, and its input carried the class `mdc-checkbox--selected`, while its native `checked` property read false (the property the per-question check used).
3. (Withdrawn after run B.) The Q4 and second-pass closing lines mention "Notebook 0", which does not occur in the v2 Source text file. Run B Q4, with only v2 selected, also mentions it, so this is not evidence of extra sources.
Treat Q1–Q4, the readback and the second pass as possibly drawing on the three Gemini chat sources as well as v2. "01_HON_DOLO_IMPORT.txt" appears to have been off throughout (no selected class, not drawn checked). Not resolved: which internal state NotebookLM actually used.

**Tools/web use observed:** none available in NotebookLM chat; no web search. The chat filter's Google Drive search switch was ON for the readback and Q1 (no Drive file was cited in either) and OFF from Q2 onward.

**Raw response filenames and SHA-256:**

| File | Bytes | SHA-256 |
|---|---|---|
| READBACK_RESPONSE.txt | 2,114 | 00201369f80cad1a9eb02b479300917efe63f005ca9704a1c0a399ae4191a706 |
| GEMINI_RESPONSE_Q1.txt | 16,548 | 941a79ccef900b63c75123d3e88975d9018204908cbcd815fc3a618df9577d08 |
| GEMINI_RESPONSE_Q2.txt | 15,931 | 3460ab0bfd198b2a40570e5a8df224b623184b270e42882ea7189299ea367ef7 |
| GEMINI_RESPONSE_Q3.txt | 9,584 | b8ffb89ac1772f0486a9a2d635557dfa1764d709d8acf2b80ac90dc302000264 |
| GEMINI_RESPONSE_Q4.txt | 4,305 | 257888bc36e51ff65ebec51c79136829f8de1e6c90f15376a7a8a9568c52a1cf |
| GEMINI_RESPONSE_SECONDPASS.txt | 1,286 | 577f7d01953e4ff8fdf45949e4f2c346c5be4d534ff8c8b2f865786482fde1ea |

Capture method (Q2 onward): the chat panel's innerText was sliced from the last marker line; the echoed prompt, the "Thoughts / expand_more" toggle and the UI chrome after the answer (keep_pin, Save to note, copy, thumb_up/thumb_down, suggestion chips, Drive banner, tune, docs (4), arrow_upward, the "can make mistakes" footer) were removed; line breaks were restored before each shot id ("P-n (parent:", "S01-n (parent:", and in Q4 the "shot | section |" lines) and before each "UNTESTED | ". No words changed. The same cleaning was hashed in the page and matched the saved file's SHA-256 for Q2, Q3, Q4 and the second pass.

**Citations captured:** the answers cite inline by source title and section heading, always the v2 Source (rendered UI-truncated as "HON-OPENING-SOURCE v2 | HON-IMPROVE-OPENING-CAM-0…"), e.g. "Section 3: The shots", "SUMMARY FOR A COLD READER", "WORDS USED IN THE CARDS", "Section 2: Order of shots, cues and cuts", "Section 4: What exists, what is missing, and the order of work", "### P-1 Waiting above the city". In the readback the notebook's citation chip "[2]" = the v2 Source (index 2 in its panel). No other source, Drive file or chip was cited in any answer. The second pass marks one item "from the answers only".

**Observed limitation:**
- Source selection: see the CAVEAT above; "v2 only" is not established.
- Q1: all eleven lines "no change"-equivalent (before = after) with every label "deferred"; Q1 ran with the Drive switch ON.
- Q2: 5 "no change" (P-1, P-2, P-3, P-4, P-6) and 6 changed lines (P-5, P-6b, P-7, S01-2, S01-1, S01-3) whose "after" mostly adds dual-side tags and collar/tee bounce; labels carry "(deferred: … missing)".
- Q3: 4 lines; holds are given as ladder numbers (4.0/6.5, 2.5/1.5, 1.5/1.0, bar grid 4 bars or 10.5) which are the Source's Fibonacci half-second values, so "no seconds" is met in wording only; beat rows are packed into one field rather than separate rows. Conditionality on EVT-HON-01 is stated in the notes block and in each open field.
- Q4: 3 claimed axis/body-side errors (P-6b, S01-2, P-5), all asserted by geometric reasoning not quoted evidence; checks proposed are diagrams/floorplans. 3 UNTESTED lines.
- Name use: Q3 and the second pass name "CFA Nova" as the operator for the listening pass; the closing lines of Q4 and the second pass offer packets "for Ziggy or Notebook 0". "Nova" and "Ziggy" occur in the v2 Source text file; "Notebook 0" does not (it recurs in run B).
- Proposal lines came out of the page run together (separated only by spaces); restored as described above. Tables were flattened to text by innerText.
- Each answer ended with an unrequested emoji closing line (kept verbatim).
