# Pan_Handlers guidance map audit, 2026-10-30

FILE: REPO-SYNC/GUIDANCE_MAP_AUDIT_20261030.md
PURPOSE: report-only audit of the parent repository's guidance (start pages, handbooks, maps, sync channel, archive front doors): what exists, who owns it, where it contradicts itself, and a proposed structure. Nothing is moved, renamed or edited by this report.
STATUS: report v001, filed for Ziggy's review and for Map Maker Nova's reuse. Uncommitted (commit = publish). Written by Claude as Pan_Handlers file steward, the parent-side half of the handbook audit Site Nova asked for on 2026-10-30.
LAST_UPDATE: 2026-10-30 at 17:32 UTC (working tree at commit a8ebc41, 2026-10-27, plus one untracked file)

## 0. Scope and method

Site Nova's ask (2026-10-30): "First report current sources, conflicts/gaps, ownership and a proposed structure; no document reorganization yet." CFA Nova added that this inventory follows its own schedule and is not a dependency of the S01-1 package. Both are honored: this file reports; the repository is untouched.

What was audited: every guidance document in D:\Documents\Pan_Handlers that a newcomer, a maintainer, a CFA agent or a cold-booted Claude could reasonably open first, in four areas: Help/ (Pathfinder, the learner app and its five maintainer documents); the root and REPO-SYNC/ (README.md, MANIFEST.md, PAN_HANDLERS_SPEC.md, projects.json, manifests/, docs/, dashboard/, tests/); circle/ and projects/ (the human-profile archive and the project concept files); and the links that reach into the CFA repository (the pathfinder_handoff map, the evidence vocabulary, the storyboard and notebook sources Pan cites).

How: a multi-agent pass on 2026-10-30. Four finders inventoried the four areas (121 source entries, 90 unique files) and listed candidate conflicts; one skeptic per candidate was told to refute it by reading the cited lines and git history. 71 candidates survived, 2 were refuted (Appendix B lists all 71 in one line each; section 3 groups them). Every claim below carries the file and line the skeptic confirmed against the working tree of 2026-10-30. Line numbers will drift as files change. I did not run a second verification round afterward; the credits were kept for the writing, as CFA Nova asked. No file under D:\Downloads was opened.

Vocabulary. "Stale pointer": a link or instruction whose target does not exist or no longer describes the thing. "Contradiction": two guidance statements that cannot both be followed. "Duplicate": the same guidance written in more than one place with no declared canonical copy. "Missing entry": a document or path a reader needs that no index names. "Ownership unclear": a document whose writer, reader or gate is not stated or is stated inconsistently. "Orphan": a file nothing links to.

## 1. The map as it stands

Three generations of guidance sit in the repository with no connector between them.

1. The 2025 federation layer (November and December 2025): README.md's identity sections, MANIFEST.md, PAN_HANDLERS_SPEC.md, projects.json, manifests/*.json, docs/THE_MATRIX_MANIFEST.md, dashboard/START_HERE.md, the root pages/ package. It describes Pan Handlers as the Hall of a repository federation with a Tri-Council (Nova as Chief Coherence Architect, Claude as repository steward of Nyquist), a Matrix landing page as canon, and a root app.py that was deleted on the day it was created.
2. The July 2026 layer: docs/I_AM/I_AM.md v2.0 (2026-07-21) and circle/ (the human-profile archive, 218 files, PUBLIC by the 2026-07-16 decision). I_AM.md is the only file that records the shift from "metadata, not core documents" to the repository being the long-term home of the archive.
3. The September to October 2026 layer: Help/ (Pathfinder, eight pages, five maintainer documents, 16 test modules), REPO-SYNC/ (the sync channel, Briefing #002 of 2026-10-10, the recovered index-site brief of 2026-10-27, the untracked rules-of-the-road draft), and .claude/launch.json. This is where the work with CFA actually happens.

Four reader paths, as they stand today:

| Reader | Path that works | Where it breaks |
| --- | --- | --- |
| Learner (wants Pathfinder) | README.md line 7 to Help/README.md "Run it" (line 47) to the Start here page (Help/pages/start_here.py) | README.md lines 175 to 182 tell the same reader to run a root app.py that does not exist; Help/README.md tells them to act inside the app (line 25) before it says how to launch it (line 47) |
| Maintainer (wants the handbook) | Help/FILE_MAP.md, linked from Help/README.md lines 5 and 191 | No document lists all five Help/ markdown files with roles; FILE_MAP.md covers four and omits CFA_TUTORIAL_LEDGER.md; the app itself has no handbook destination |
| CFA agent arriving | REPO-SYNC/README.md protocol (lines 24 to 36) and MASTER_REPO_SYNC_OUT.md's three reply routes (lines 191 to 193) | Help/ never mentions REPO-SYNC or the mailbox; REPO-SYNC never mentions Help or Pathfinder; CFA_HANDOFF.md still says "start with README.md and reply in CFA_FEEDBACK.md" from September |
| Claude cold boot | dashboard/START_HERE.md "Cold Boot Guide for Claude" (2025-11-30) | It predates Pathfinder, omits dashboard/pages/pathfinder.py, and mandates a theme the app no longer defaults to |

The circle/ archive is internally a handbook (ARCHIVE_PLAN.md, ETHICS_AND_CONSENT.md, PROFILE_SCHEMA.md, the protocol, the registries) but its front door is stale: INDEX.md's header and phase tracker stop at 2026-07-17 while its own registries run to 2026-07-21.

## 2. Inventory

The finders recorded 121 source entries; 90 are unique after removing the files two areas both claimed (Appendix A gives each with its git last-commit date, sha256 prefix, size, entry-point flag and the owner and purpose the finder inferred; a few entries group several sibling files and are marked as groups). Counts by area, first claim wins:

| Area | Entries | Entry points the finder marked | Last commits range (Pan files) |
| --- | --- | --- | --- |
| Help/ (Pathfinder) | 34 | Help/README.md, Help/CFA_TUTORIAL_LEDGER.md, Help/app.py, Help/pages/start_here.py, README.md, dashboard/START_HERE.md | 2025-11-30 to 2026-10-20 |
| Root and REPO-SYNC/ | 21 | README.md, MANIFEST.md, REPO-SYNC/README.md, docs/I_AM/I_AM.md, docs/THE_MATRIX_MANIFEST.md, docs/prompts/dashboard_claude.md | 2025-11-27 to 2026-10-27, plus two untracked (the rules draft; .claude/settings.local.json) |
| circle/ and projects/ | 24 | circle/README.md, circle/SYNC_OUT/README.md | 2025-11-27 to 2026-10-04 |
| CFA links (files Pan points into, and the Pan files that point) | 11 | CFA notebook_workflow/START_HERE.txt, CFA writer_pass_20261010/START_HERE.txt | 2026-10-09 to 2026-10-20 |

The one guidance document that is neither tracked nor linked: REPO-SYNC/RULES_OF_THE_ROAD_DRAFT_20261027.md (151 lines, untracked since 2026-10-27, zero inbound references by filename anywhere in the repository). It is the only Pan-side text that writes the parent methodology.

## 3. Confirmed conflicts and gaps, grouped

### 3.1 The root front door (2025 layer still presented as current)

- README.md lines 175 to 182: `cd Pan_Handlers`, `streamlit run app.py`, "Visit http://localhost:8501". Root app.py was removed in commit d8e4187 (2025-11-27, "Remove duplicate root app.py"); the lines were written in d14881f the same day and never revised. The real entry points are Help/app.py (port 8506, README.md line 15) and dashboard/app.py (port 8504, its own docstring).
- README.md line 171 points at `Pan_Handlers/manifest_schema.json`, which never existed (the schema is inline in PAN_HANDLERS_SPEC.md lines 15 to 64). PAN_HANDLERS_SPEC.md line 153 and pages/about.py line 140 point at a root config.py that does not exist (the only config.py is dashboard/config.py, with no manifest URL list).
- README.md line 144 "Initializing (2025-11-27)", lines 148 to 149 "Next steps: Build Pan Handlers Streamlit app", line 73 "Status: In Preparation"; PAN_HANDLERS_SPEC.md lines 201 to 202 "Production Ready / Implement full Streamlit app". The repository is 168 commits past that state.
- README.md lines 11 to 13 call "Rewrite a scene" Pathfinder's central mission. Help/README.md line 19 (October 2 redirection to lifelike video), Help/console.py lines 29 to 30 (Rewrite a scene under OTHER SCENE TOOLS) and every page header say otherwise. The root sentence is the single stale outlier.
- MANIFEST.md is frozen at its only commit (d14881f). Its repo tree (lines 39 to 77) lists app.py and assets/, which do not exist, omits pages/matrix.py, and omits six top-level directories that do: Help/, REPO-SYNC/, circle/, dashboard/, docs/, tests/. PAN_HANDLERS_SPEC.md lines 92 to 117 is a second whole-repo tree with the same defects plus config.py, utils.py and data/roadmap.json. No file indexes the repository as it stands.
- projects.json (last_updated 2025-11-27): four artifact paths that were never created (line 70 nursing/ROADMAP.md, line 100 voting/SPEC.md, line 101 voting/mockups/, line 192 ABI/ARCHITECTURE.md); placeholder `github.com/USER/...` URLs at lines 231 and 238 while manifests/nyquist_consciousness.json and manifests/cfa.json carry the real ones; line 232's local_manifest resolves to a missing file. The dashboard loads the file but never reads these fields.
- manifests/cfa.json names eight CFA docs paths (lines 84 to 154) that do not exist in the CFA tree, and is not a copy of CFA's own panhandlers_manifest.json (v5.0.0, no projects array) although PAN_HANDLERS_SPEC.md line 105 calls manifests/ "local manifest cache/copies".
- Hard-coded dates still shown as upcoming: pages/roadmap.py lines 119 to 120 (2026 Q1 arXiv submission), pages/matrix.py line 417 ("Publication 95%, Workshop Ready").

### 3.2 Names and vocabularies with no canonical form

- CFA is expanded three ways: "Continuous Framework Architecture" (docs/I_AM/I_AM.md line 80); "Collaborative Friction Architecture" (projects.json line 237, dashboard/pages/about.py line 51); "Coherence, Faith, Agency" (data/glossary.md line 13, MANIFEST.md line 210, manifests/cfa.json lines 3 and 92). The glossary declares itself the shared language of the network (line 3) and nothing reconciles the three.
- ABI: "American Bureau of Intelligence" in three files (manifests/abi.json, manifests/panhandlers-root.json, MANIFEST.md line 88) against "American Bureau of Investigation" in eight. NDO: "Neural Data Observatory" (MANIFEST.md line 87) against "Nyquist Data Observatory" (MANIFEST.md line 213 and the manifests). DCIA: "Decentralized Centralized" (manifests/dcia.json line 3) against "Decentralized Central" everywhere else.
- Three glossaries, unlinked: data/glossary.md; pages/glossary.py's GLOSSARY dict (lines 9 to 128, definitions differ, for example the S-stack described through S9 with a PFI threshold); circle/SYNC_OUT/GLOSSARY.md.
- The Nyquist S-stack is described four incompatible ways (pages/matrix.py S0 to S77 with S3 Temporal Stability; pages/roadmap.py S0 to S9 with S7 Temporal Stability; data/glossary.md S0 to S9 with different S0 to S2 names; the manifests). No Pan file marks itself canonical for it.
- Evidence-state vocabulary: the October 10 agreement made CFA's templates/workflow_intake.md "Evidence states" the single canonical source. Pan still carries three definitions: Help/content/collaborators.py lines 260 to 271 (a labelled, cited learner summary, acceptable), Help/CFA_TUTORIAL_LEDGER.md line 26 (uncited five-term list), and the restatements at Help/README.md line 45 and REPO-SYNC/MASTER_REPO_SYNC_OUT.md line 83.

### 3.3 Help/ maintainer side (five documents, no index, stale labels)

- No document lists all five Help/ markdown files with roles. Help/FILE_MAP.md lines 72 to 75 cover README.md, FILE_MAP.md, CFA_HANDOFF.md, CFA_FEEDBACK.md and never mention CFA_TUTORIAL_LEDGER.md. Help/README.md's tree (lines 193 to 203) lists no markdown at all. No Python file under Help/ or dashboard/ names any of the five; the console's sidebar groups (ORIENT, ACTIVE MISSION, OTHER SCENE TOOLS, MAKE, KEEP EXPLORING) offer no handbook destination. The ledger reaches the screen only as the pre-filled default of an editable text area.
- Help/README.md has no orientation block: line 3 is "Collaborator handoff - October 8, 2026" and 44 lines of dated production state precede "Run it" at line 47. Its dated state (October 8 at line 3, October 2 at line 19, October 4 at line 45, the scope list at line 233) is two adoption rounds behind the app it documents: Help/content/cfa_learning.py line 11 and Help/content/collaborators.py line 13 carry the October 10 and October 20 adoptions. README.md last changed 2026-10-09.
- Help/README.md line 35 labels CFA_FEEDBACK.md "historical September feedback" while lines 15 and 221 treat it as the live return channel, and the file's October returns occupy lines 3 to 159 (five "Pathfinder to CFA" sections dated October 4 to 20) with the September review last. Its title (line 1, "Nova to Pathfinder") names the opposite direction from five of its eleven sections.
- Help/README.md lines 35 and 221 and Help/FILE_MAP.md line 74 label CFA_HANDOFF.md the current direction or current coordination; its newest section is the October 8 debrief (line 3), it was last committed 2026-10-09, and the three later adoptions live only in CFA_FEEDBACK.md and the ledger. FILE_MAP.md was edited in that same October 10 commit without updating line 74.
- Seven pages versus eight: Help/README.md lines 68 to 93 and 205 to 213 and Help/pages/__init__.py line 1 ("The seven Pathfinder sidebar pages") omit Collaborators; Help/console.py line 18, Help/FILE_MAP.md line 20 and tests/test_help_console.py list eight.
- Superseded test counts in CFA_HANDOFF.md: 68 (line 11, October 4) and 27 (line 140, undated, September by position); the suite now has 70 test functions. CFA_FEEDBACK.md line 210 names scene_lab.py, renamed to pages/rewrite_scene.py on October 4 (covered by the location note at line 159, so historical rather than broken).
- Addressee drift: "Nova" and "Panhandler Nova" remain the addressee in text positioned as current (CFA_HANDOFF.md lines 1, 15, 23, 196; CFA_TUTORIAL_LEDGER.md lines 3, 27, 70, 101, 110, 173, 186) although the record since October 10 names Claude as Pan's steward and distinguishes CFA Nova, Site Nova, Map Maker Nova and the Nova Dot.
- The ledger is written by two parties with no per-section assignment: its own protocol (lines 22 to 30), CFA_HANDOFF.md line 15 and Help/README.md line 15 give CFA the ledger at intake and give Pan CFA_FEEDBACK.md, yet Pan writes adoption and status sections into the ledger (lines 5 to 20, 242 to 250, 252 to 274, 276 to 300, 310).
- Duplicates with no declared canonical copy: each adoption event is recorded two to four times (October 8 in four places: CFA_FEEDBACK.md 88 to 118, the ledger 242 to 250, Help/README.md 3 to 11, CFA_HANDOFF.md 3 to 7); the Pan-to-CFA loop procedure is stated in seven tracked places plus the untracked draft, each with a different subset of its steps; the Pathfinder run command is verbatim in four files (Help/README.md 55, Help/FILE_MAP.md 8, README.md 15, dashboard/README.md 18); four CFA return sections are byte-identical in CFA_HANDOFF.md lines 163 to 196 and the ledger lines 124 to 173; the ownership statement exists as a two-party form in six places and a three-party form (adding Nyquist's method ownership) in five.
- Agreed and undone: the October 10 Briefing #002 adoption recorded three de-duplication tasks (CFA_FEEDBACK.md line 55 and the ledger line 300: re-point the five other stale-widget mentions at Save & load; replace the connector version in guides/cloud_access.py with a dated CFA pointer; thin count prose in README.md and CFA_HANDOFF.md). No commit since October 10 touches those files.
- Help/.preview/ holds gitignored staging copies of CFA's handoff README (October 4 and October 8) that nothing references except their own receipts; their relative links resolve only from the CFA pathfinder_handoff directory.
- Help/content/collaborators.py line 116 records the Flow boundary as "no upload through October 9" with no forward pointer; the later state (Flow 002 returned 6.0 s with an audio track) is recorded only in the untracked rules draft (line 54).

### 3.4 dashboard/ (the Back Alley) and tests/

- dashboard/START_HERE.md (2025-11-30) is positioned as the first read for Claude and never mentions Pathfinder, Help/ or FIELD GUIDES; its tree (lines 44 to 50) omits dashboard/pages/pathfinder.py (added 2026-10-04). dashboard/README.md's navigation section (lines 98 to 119) omits FIELD GUIDES although its own lines 17 to 20 describe it.
- Theme contradiction: START_HERE.md lines 69 to 76 ("DO NOT CHANGE" the green-on-black Matrix identity) and dashboard/.streamlit/config.toml against dashboard/app.py lines 628 to 630 (matrix_mode defaults to False) and lines 659 to 667 (Enter/Exit The Matrix toggle); docs/prompts/dashboard_claude.md lines 22 to 27 documents two themes.
- docs/prompts/dashboard_claude.md line 48 instructs "use st.experimental_rerun() not st.rerun()"; requirements.txt line 5 pins streamlit>=1.36,<2 and dashboard/app.py lines 663 and 668 call st.rerun().
- Run instructions for the two apps are written in seven files at eleven locations with four ports (8501, 8504, 8506, 8510) and three working directories; the "add a new page" procedure is written three times (START_HERE.md 115 to 119, dashboard/README.md 123 to 147, dashboard_claude.md 29 to 33).
- tests/: all 16 modules target Help/. One test loads dashboard/app.py and asserts only that the embedded Pathfinder page renders. No test covers the root pages/ package, projects.json content, or whether any markdown link target exists.

### 3.5 REPO-SYNC/, the generations and the cross-repo links

- REPO-SYNC/README.md (LAST_UPDATE 2026-10-03) covers MASTER_REPO_SYNC_OUT.md, SYNC_IN/pending/ and SYNC_IN/processed/ only. Nothing says that standalone dated briefs live at the REPO-SYNC root, who maintains them, or whether they are trimmed or kept. Two such files exist: INDEX_SITE_BRIEF_RECOVERED_20261021.md (committed a8ebc41, lacking the channel's FILE/PURPOSE/STATUS/LAST_UPDATE header) and the untracked rules draft.
- RULES_OF_THE_ROAD_DRAFT_20261027.md: untracked, unlinked, one-way (it names the index brief; nothing names it). It carries the house style (G1 to G11), a preferred-not-rigid method for five collaborators including the DeepSeek entry Pathfinder lacks, the two promotion routes, proposed homes in both parent faces, and 14 open questions for Ziggy.
- MASTER_REPO_SYNC_OUT.md is written to be relayed outside the repository as-is, yet most of its file pointers are bare basenames (collaborators.py, video_routes.py, workflow_lessons.py, workflow_files.py, video_handoff.py, workflow_decision.py) that resolve only if the reader knows Help/content from Help/guides.
- Role labels: the 2025 layer (README.md lines 159 to 160; MANIFEST.md lines 150 to 154 and 237 to 238; manifests/panhandlers-root.json line 25 "ai_steward: Nova") still names Nova as Pan's architect and Claude as Nyquist's steward. The 2026 record (Briefing #002, the ledger, the rules draft) has Ziggy's October 10 decision: CFA owns production, Pan teaches, Nyquist owns the notebook method, Claude stewards the Pan files. The split is agreed; the 2025 text was never reconciled to it.
- No start page exists for a CFA agent. The fragments (CFA_HANDOFF.md lines 86 and 97; Help/README.md lines 5, 191, 221; FILE_MAP.md line 95; REPO-SYNC/README.md lines 24 to 36; MASTER_REPO_SYNC_OUT.md lines 191 to 193) do not link each other completely, and the only START_HERE-named file is scoped to dashboard development.
- Pan holds three unreconciled descriptions of CFA with no precedence rule: manifests/cfa.json's eight 2025 project statuses; Help/content/cfa_learning.py's STATUS_ROWS, which Briefing #002 (lines 35 to 38) declares the only place Pan restates CFA status; and CFA's own panhandlers_manifest.json.
- The cross-repo link map (CFA's pathfinder_handoff/README.md, 357 lines) has no stated owner. Pan names it four ways ("shared-methods map", "CFA's handoff map", "CFA's map between repositories", "CFA evidence index") and writes into it on every adoption under a sha256 guard.
- docs/THE_MATRIX_MANIFEST.md lines 76 to 77 and 182 ("Matrix.py becomes the first point of contact for ANY user or agent"; "THE MATRIX IS NOW CANON") and I_AM.md line 311 ("Portal Layer: The Matrix") against pages/matrix.py, which is static cards and metrics with no link, button or page switch to any repository, inside a root pages/ package that nothing mounts.
- Deploy source: three candidates on record and none authoritative in-repo. Help/README.md line 215 and Help/FILE_MAP.md line 11 say Streamlit Cloud's entry is Help/app.py (the index brief ties that to pan-studio.streamlit.app via a CFA receipt). dashboard/START_HERE.md line 13 and dashboard/README.md line 4 name panhandlers.streamlit.app as the Grand Hall. Ziggy's 2026-10-27 answer (index brief line 11, rules draft line 9) places the Hall at the root pages/ package on that host, but no tracked file records a launcher for it, and the root app.py that would be it does not exist.

### 3.6 circle/ (the archive's front door is stale; one canonical rule was replaced without a recorded revision)

- circle/INDEX.md: line 19 "14 candidates, 1 OPEN" against line 46 "131 candidates, 118 OPEN" (IDEA_TRAILS/README.md line 9 confirms 131 and 118, reviewed 2026-07-21); lines 56 to 57 "No source conversations are filed yet" against line 28 "FOUR G-DIRECT SOURCES FILED" and line 50 "Ziggy 4, Grant 8"; header line 6 "Last updated 2026-07-17" although rows and sweeps inside run to 2026-07-21 (last commit f50cd39).
- circle/README.md's Directory Map (lines 52 to 72, "you are here") omits five tracked items added after its 2026-07-16 commit: mirror/, SYNC_OUT/, DIG_MAP.md, CONSTITUTIONAL_BACKBONE.md, evidence/corpus_sweeps/.
- circle/SHARED_HISTORY/README.md line 10 "Status: empty" while TIMELINE.md holds a 59 KB populated chronology; LEXICON_INTERNAL.md and NORMS.md are suggested and unwritten. circle/evidence/chat_extractions/README.md line 12 "0 packets filed" against its own FILED marks (lines 87 to 92), 32 DIG workbooks and four synthesis packets. circle/RELATIONSHIP_MAP.md lines 4 and 8 still call the file a placeholder above a 27-row protocol-fed holding ledger.
- circle/ARCHIVE_PLAN.md lines 3 to 6 declare itself canonical and say README.md, PROFILE_SCHEMA.md and ETHICS_AND_CONSENT.md derive from it and "must not contradict it without a recorded revision". Its section IX (lines 313 to 324) prescribes private and public layers and "Nothing moves from private to public without explicit review". ETHICS_AND_CONSENT.md section 1 records "Publication Status: PUBLIC (decided 2026-07-16)" and section 2 "Content Boundary (replaces the old layer split)". The derived file replaced the canonical rule; the canonical file has no revision note.
- circle/mirror/README.md lines 63 to 79: "not yet consent-reviewed, not yet linked from any member's real profile", three unchecked prerequisites before it is final. All seven STRAWMAN files are committed (2026-07-21) in an archive where "the whole circle/ archive is published" and the gate is "what gets committed and pushed". The gate for this artifact type is undefined.
- circle/SYNC_OUT/ holds hand-maintained snapshots of three masters; two carry a re-copy banner and IDEA_TRAILS_INDEX.md (byte-identical to IDEA_TRAILS/README.md) carries none, so nothing in it says it is a copy. SYNC_OUT/README.md line 151: "Nothing in this folder auto-syncs."
- manifests/panhandlers-root.json line 36 and MANIFEST.md line 159 ("PanHandlers holds metadata, not core documents") were never revised after circle/ made the repository the long-term home of profiles, evidence and debate notes (ARCHIVE_PLAN.md line 25). Only I_AM.md lines 158 and 171 record the change.

### 3.7 Refuted (2)

- A claim about the storyboard workflow file tested the wrong path (the scope file names collaborators/storyboard_detail_20261009/shared/STORYBOARD_WORKFLOW.txt). Not a defect.
- A claimed contradiction between MANIFEST.md lines 159 to 160 and Briefing #002 lines 17 to 21: all passages exist as cited but do not conflict. Not a defect.

## 4. Ownership, as recorded and as practiced

| Guidance | Written by (practice) | Read by | Gate | Stated in-repo? |
| --- | --- | --- | --- | --- |
| Pan_Handlers repository files | Claude, as file steward since Ziggy's 2026-10-10 decision | Ziggy, collaborators, the public (repo is PUBLIC) | Ziggy's word to commit; commit = publish | Only in the 2026 sync record; 2025 files still say Nova |
| Help/ learner app and content modules | Claude (adoptions on Ziggy's go) | learners, CFA Nova | tests pass; dated adoption record | Yes (Help/README.md line 15), but labels stale |
| Help/CFA_TUTORIAL_LEDGER.md | CFA Nova (intake) and Claude (adoption), interleaved | both | none stated per section | Protocol says CFA; practice is both |
| Help/CFA_FEEDBACK.md | Claude (Pan's dated adoption returns); September section by CFA Nova | CFA Nova | dated sections, never rewritten | Title says the reverse direction |
| REPO-SYNC/MASTER_REPO_SYNC_OUT.md | Claude | Ziggy relays to CFA Nova; CFA Nova reads | one briefing per closed checkpoint | Yes (REPO-SYNC/README.md) |
| REPO-SYNC root briefs and drafts | Claude | Ziggy | Ziggy's review; untracked until he decides | No |
| circle/ archive | Claude under Ziggy's gate (2026-07 rules) | public | ETHICS_AND_CONSENT.md Do-Not list at commit time | Yes, but ARCHIVE_PLAN section IX contradicts it |
| CFA pathfinder_handoff/README.md (link map) | CFA Nova hosts; Claude inserts under sha256 guard | both | hash check before writing | No owner stated |
| Document-map proposals across repositories | Map Maker Nova (Site Nova's assignment of 2026-10-30) | Site Nova, Ziggy | Ziggy's review | In CFA collaborators/handbook_audit_20261030, not in Pan |
| The site, navigation, publication | Site Nova (CFA Site Codex) | all | her scoped reconciliations | CFA side only |
| Browser, provider cost, dispatch | CFA Nova | all | mode and cost are hers | CFA side only |
| Deploy sources (two Streamlit hosts) | unresolved | public | unresolved | Three candidates, no record |

Claude does not edit site files and does not answer approvals in Ziggy's name; this table reports practice, it does not assign anything.

## 5. Proposed structure (a proposal; nothing is moved by this report)

P1. One root connector. A short START_HERE.md at the repository root, or a block above README.md's line 1 if Ziggy prefers one file: three sentences on what Pan Handlers is in October 2026; the three generations each labelled current, historical (kept), or proposal; the four reader paths of section 1 with one link each. Every other front door points to it for orientation and keeps only its own area's content.

P2. A Help/ handbook index. One table in Help/FILE_MAP.md (which already has four of the five) naming each maintainer document with role, who writes it, who reads it, and cadence; a five-line orientation block above Help/README.md's line 3 with the "Run it" commands moved up; the labels at Help/README.md lines 35 and 221 and FILE_MAP.md line 74 corrected to what the files now are. CFA_FEEDBACK.md's title changed to name both directions. The ledger gets a per-section byline convention (CFA intake / Pan adoption) rather than a rewrite.

P3. One canonical home per repeated statement, the rest become pointers:
- run commands: Help/FILE_MAP.md lines 7 to 11 for Pathfinder, dashboard/README.md for the dashboard, one port each, every other copy a link;
- the Pan-to-CFA loop: Help/CFA_TUTORIAL_LEDGER.md lines 22 to 30 until the rules of the road are adopted, then the rules;
- the ownership statement: Briefing #002 (or the rules once adopted), three-party form;
- evidence vocabulary: CFA's workflow_intake.md by link only; the ledger's line 26 list and the two restatements become pointers;
- glossary and name expansions: data/glossary.md, which already declares itself the shared language; pages/glossary.py reads it or is retired with the orphaned root pages/;
- the S-stack: the Nyquist repository by link; Pan stops restating layer names.

P4. Dated banners on the 2025 layer rather than rewriting it: MANIFEST.md, PAN_HANDLERS_SPEC.md, dashboard/START_HERE.md, docs/THE_MATRIX_MANIFEST.md, projects.json's meta and manifests/*.json each get one line, "historical as of 2025-11-27 (or 12-01); the current map is START_HERE.md". The exceptions, corrected in place because a public newcomer hits them first: README.md lines 171 to 182 (the nonexistent app.py and schema file), README.md lines 11 to 13 (the mission sentence), dashboard_claude.md line 48 (the removed Streamlit API), and the four never-created paths in projects.json.

P5. REPO-SYNC/README.md gains a paragraph on standalone briefs and reports: they live at the channel root, carry the FILE/PURPOSE/STATUS/LAST_UPDATE header, are kept rather than trimmed, and are listed in a short index at the foot of the README. The index brief, the rules draft and this audit would be its first three entries once Ziggy decides which are tracked.

P6. A circle/ header refresh pass (INDEX.md's phase tracker, bottleneck and header; README.md's map; SHARED_HISTORY, chat_extractions and RELATIONSHIP_MAP status lines), a recorded revision in ARCHIVE_PLAN.md section IX acknowledging the 2026-07-16 PUBLIC decision, a banner and re-copy rule on SYNC_OUT/IDEA_TRAILS_INDEX.md, and a recorded gate decision for mirror/. Content untouched; headers only.

P7. A guidance entry template shared with Map Maker Nova's proposal: question or purpose; scope; owner; canonical source with revision or hash; why and when to read; predecessor and supersession; valid-for and invalid-for; unresolved issue; next action; reviewed or adopted evidence. Appendix A is already shaped toward it (path, hash prefix, git date, entry flag, owner) and can be lifted into her document map as-is.

P8. One test that resolves every relative markdown link and every path in a fenced command inside README.md, Help/*.md, REPO-SYNC/*.md and dashboard/*.md to an existing file. It would have caught the stale pointers in 3.1, 3.3 and 3.4 and will keep P1 to P5 honest.

## 6. Choices that need Ziggy

1. Deploy source of record for panhandlers.streamlit.app and pan-studio.streamlit.app: confirm the 2026-10-27 answer (Hall at root pages/) and let the launcher script be recorded, or name a different one.
2. The 2025 federation layer: retire it with banners (P4), or restore it (which would make the Matrix landing page and the Tri-Council current again).
3. Canonical expansions: CFA, ABI, NDO, DCIA, one form each.
4. REPO-SYNC/RULES_OF_THE_ROAD_DRAFT_20261027.md: track and link it, or keep it untracked until adopted (tracking publishes it).
5. circle/mirror/: public as-is, behind a stronger banner, or comparison-only; and whether ARCHIVE_PLAN.md section IX gets its revision note.
6. Root START_HERE.md as a new file, or the connector at the top of README.md.
7. Whether the circle/ headers are refreshed (P6) or the archive is declared a July 2026 snapshot and left as it stands.

Ordinary corrections (stale labels, nonexistent paths, duplicate pointers) do not need him and can be done on his word to proceed with P2 to P5.

## 7. Limits

Report-only; no file was edited, moved or renamed. Each of the 71 findings was confirmed by one skeptic agent reading the cited lines and git history on 2026-10-30; I did not run a second round, and line numbers are those of the working tree at commit a8ebc41. The CFA side of the handbook (Nova Dot's part) is not audited here except where Pan points into it. Help/.preview/ and the untracked draft were included because a newcomer on this machine sees them. No file under D:\Downloads was read or cited. Where this report paraphrases Ziggy's decisions it uses the record's wording (Briefing #002, the index brief, the rules draft); it records no decision in his name.

Companion files: a copy of this report sits under the CFA audit folder collaborators/handbook_audit_20261030/pan_handlers/ for Map Maker Nova's reuse; her own proposal and source manifest are in collaborators/handbook_audit_20261030/map_maker_nova/. The underlying finder and skeptic output (461 KB of JSON) stays in the session scratchpad and can be regenerated.

## Appendix A. Inventory (90 unique entries, some grouping several sibling files; git date = last commit touching the file; sha256 = first 12 hex of the file as of 2026-10-30)


### A.1 help (34 files)

| Path | Entry | Git last commit | sha256 (12) | Bytes | Owner as inferred by the finder | Purpose as inferred by the finder |
| --- | --- | --- | --- | --- | --- | --- |
| Help/README.md | yes | 2026-10-09 | 33185202ed89 | 37685 | Unsigned. FILE_MAP.md line 72 describes it as 'Running, coverage and maintenance instructions'. Since Oct 10 t | Pathfinder project README: newest-first dated production state (Oct 8 collaborator handoff, lines 3-11; tutorial loop, 13-17; Oct 2 active d |
| Help/FILE_MAP.md |  | 2026-10-10 | 62d01a17d941 | 12370 | Unsigned. Updated with each adoption (line 56 names the October 10 adoption). | Sidebar label to Python file map (15-24), nested ComfyUI lesson map (26-58), folder tree (60-83), 'How to request an update' as page to tab  |
| Help/CFA_HANDOFF.md |  | 2026-10-09 | dcce24e51908 | 28971 | Line 80: 'Drafted September 12, 2026 for the user to pass to Nova'. Later Pan sections unsigned; appendices 15 | Titled 'To Nova: connect CFA production work with Pathfinder' (1). Pan to CFA direction letter in dated layers: Oct 8 adoption pointer (3-7) |
| Help/CFA_FEEDBACK.md |  | 2026-10-20 | 7d541b5e60da | 41421 | Oct 10 and Oct 20 sections: 'Adopted by Claude, Pan_Handlers Master Repo steward' (5, 59). Oct 4 and Oct 8 sec | Titled '# Nova to Pathfinder' (1) but holds, newest first, five 'Pathfinder to CFA' adoption returns: Oct 20 clip-scope (3-27), Oct 10 Brief |
| Help/CFA_TUTORIAL_LEDGER.md | yes | 2026-10-20 | 635a2a5cc792 | 73219 | Dual-written. CFA Nova authored the frame and intake sections (3, 89, 91-240, 302-308); Pan adoption/status se | 'Comfy tutorial ledger and reusable workflow notes': PH TUT 01-06 dated result table (5-20), 'Standing process for future guides' (22-30), e |
| Help/app.py | yes | 2026-10-09 | 3505c5edbf81 | 935 | Unsigned; git ZiggyMack. | Standalone Streamlit launcher; docstring line 1 'Run from the repository root: python -m streamlit run Help/app.py.' Registers one hidden st |
| Help/console.py |  | 2026-10-09 | 8a8c2bc6242d | 3238 | Unsigned; FILE_MAP 78 'console.py owns the shared navigation shell'. | Navigation shell shared by standalone app and dashboard: SECTIONS tuple of eight (line 18); grouped sidebar ORIENT / ACTIVE MISSION / OTHER  |
| Help/pages/start_here.py | yes | 2026-10-10 | e49504d9e82a | 4376 | Unsigned; git ZiggyMack. CFA receipt pipeline_banner_20261009 requested the banner-first layout (per REPO-SYNC | The learner start-here (default section). Rendered text: path_cards() banner (14); hero 'VIDEO FIRST / THE NEXT EXPERIMENT' / 'Keep the perf |
| Help/pages/video_workshop.py |  | 2026-10-10 | 5199bfa35ced | 23948 | Unsigned. | 'Video-first routing and a review notebook; never submits Comfy jobs.' Five stages; route cards show kind + 'Official documentation checked' |
| Help/pages/collaborators.py |  | 2026-10-10 | 96ae8122b0b9 | 7802 | Unsigned. | 'Teach collaborator handoffs; production files and operations stay in CFA.' Three tabs (Role & handoff, Preserve or explore, Continue a less |
| Help/pages/sources_roadmap.py |  | 2026-10-09 | c2a88da835db | 3295 | Unsigned. | Sources and roadmap. Tab 'About this console' (42-44) is the only in-app statement of the Pan/CFA split: 'Pathfinder is the reusable guide i |
| Help/pages/{comfyui_guide,compare_paths,rewrite_scene,field_journal}.py |  | see members | group entry | 0 | Unsigned. | Remaining sidebar pages: ComfyUI guide (235 lines, outer tabs 00-07 assembling guides/*), Compare paths (45), Rewrite a scene (261, dialogue |
| Help/pages/__init__.py |  | 2026-10-09 | 82eeda851d5d | 42 | Unsigned. | Package docstring: 'The seven Pathfinder sidebar pages.' |
| Help/guides/tutorial_notes.py |  | 2026-10-09 | f2ea44b85a94 | 21943 | Unsigned. | Annotated transcript bookmarks selector (eleven entries) and exports. REVIEWED = 'September 12, 2026' (module constant). |
| Help/guides/node_atlas.py |  | 2026-10-09 | 5807b42b50c5 | 64284 | Unsigned. | Curated node atlas (24 node types, six recipes). Docstring: checked against upstream 2026-09-12, prompt-composition additions 2026-10-04; ca |
| Help/guides/model_library.py |  | 2026-10-09 | 2bd41d5603db | 31769 | Unsigned. | Model selection reference and receipt template. Docstring: 'Primary sources reviewed on 2026-09-12.' |
| Help/guides/cloud_access.py |  | 2026-10-09 | 2951f124ff12 | 14535 | Unsigned. | Shared Cloud access checklist; also carries Codex MCP OAuth reconnection instructions (CODEX_MCP_URL line 7; entries 23, 83-84, 104). The Oc |
| Help/guides/video_handoff.py |  | 2026-10-20 | 80b705651455 | 24401 | Unsigned; Oct 20 change adopted by Claude (CFA_FEEDBACK.md 13). | Video/audio handoff lesson shared by Workflow lab, Collaborators and Rewrite a scene; carries the dated soundtrack case, mouth-continuity ro |
| Help/guides/workflow_files.py |  | 2026-10-10 | 436b1dda7e2c | 11862 | Unsigned. | Save & load lesson; designated home (Oct 10) of the consolidated stale-widget / readback lesson (64, 105). |
| Help/guides/{generation_settings,image_edit_lab,model_filters,prompt_wiring,sampling_lab,shared_controls,vae_paths,worked_example,workflow_controls,workflow_decision,workflow_lab}.py |  | see members | group entry | 0 | Unsigned. | Remaining reusable lessons; each docstring states it performs no execution. image_edit_lab 192 and sampling_lab 138 cite 'Help/CFA_TUTORIAL_ |
| Help/content/cfa_learning.py |  | 2026-10-10 | 66ed2c9d6eb7 | 23595 | Unsigned; adopted by Claude Oct 10. | Dated CFA evidence snapshot driving Start here, Video workshop 'Where we actually stand', Sources & roadmap. REVIEWED = 'October 9, 2026 · d |
| Help/content/collaborators.py |  | 2026-10-20 | 00f0b6e258eb | 34859 | Unsigned; Oct 10 and Oct 20 entries adopted by Claude. | Teaching data for the Collaborators page: PROVIDERS (ComfyUI, Grok, Gemini, Flow) with purpose/how/boundaries/sources/evidence; COMMON_LESSO |
| Help/content/catalog.py |  | 2026-10-09 | d619129255ce | 33108 | Unsigned. | PATHS, COMFY_TRADEOFFS, STEPS, ENVIRONMENT_GUIDES, SOURCES, GLOSSARY, FUTURE_CHECKLIST. REVIEWED_ON = '2026-09-12'. |
| Help/content/{tutorial_register,creative_control_guide,video_routes,h3_candidate}.py |  | see members | group entry | 0 | Unsigned. | tutorial_register: eight source records with hashes, REVIEWED 'October 4, 2026'; creative_control_guide: Spanish NKD annotations, REVIEWED ' |
| Help/content/{episode_three,episode_four,additional_guide,scene_content,workflow_lessons,tutorial_followups}.py |  | see members | group entry | 0 | Unsigned. | Transcript annotations and curriculum data; episode_three/four, additional_guide, scene_content, workflow_lessons state Sep 12, 2026 review; |
| Help/state/{journey,scene_plan,session,video_plan}.py and Help/ui/{theme,components}.py |  | see members | group entry | 0 | FILE_MAP.md 78-80 assigns ownership by file; unsigned otherwise. | Journal schema v1, scene worksheet, session callbacks, video-plan v1; theme (Nyquist palette, Matrix mode) and shared components (path_cards |
| Help/examples/cfa_pump_v001/README.md |  | 2026-10-04 | 3731cc7e26b4 | 4155 | CFA-sourced, packaged by Nova Sep 12 (CFA_FEEDBACK.md 180-184). | Portable worked-example evidence: 'Field evidence from D:/Documents/CFA, branch main, September 12, 2026' (3); open/run the recipe (22-40);  |
| Help/.preview/ (cfa_handoff_return.README.md 2026-10-04, cfa_collaborators_return.README.md 2026-10-08, their .receipt.json and .section.md, screenshots, smoke scripts, streamlit logs, restore.json) |  | see members | group entry | 0 | Unsigned; gitignored (.gitignore:42 '/Help/.preview/'). | Local working artifacts: the two README.md files are staged copies of CFA's pathfinder_handoff README prepared for the SHA-guarded writes on |
| README.md (repo root) | yes | see members | group entry | 0 | Contributors list 156-162; unsigned otherwise. | Grand Hall README. Lines 5-18 'Pathfinder , follow the process' link Help/README.md (7), give the run command (15) and 'FIELD GUIDES to Path |
| dashboard/README.md |  | 2026-10-04 | ab23517a9d63 | 5535 | Unsigned. | Dashboard README; lines 17-19 'FIELD GUIDES to Pathfinder opens the new AI-assisted 3D/video learning console', run command, link to ../Help |
| dashboard/START_HERE.md | yes | 2025-11-30 | 504015b400bc | 5054 | Unsigned. | 'START HERE - Cold Boot Guide for Claude' for the Back Alley dashboard; first steps, critical files, directory tree. |
| dashboard/pages/pathfinder.py and D:/Documents/Pan_Handlers/.claude/launch.json |  | see members | group entry | 0 | Unsigned. | pathfinder.py: 'Embed the same Pathfinder console used by Help/app.py' (render(standalone=False)). launch.json: 'pathfinder' preview config  |
| tests/ (16 files, 70 test functions) |  | see members | group entry | 0 | Unsigned. | AppTest suite; test_help_console.py SECTIONS tuple lists all eight pages (20-22); test_collaborators.py asserts the Oct 20 lesson once with  |
| REPO-SYNC/{README.md, MASTER_REPO_SYNC_OUT.md, SYNC_IN/processed/2026-10-10_nova_cfa_teaching_delta.md, INDEX_SITE_BRIEF_RECOVERED_20261021.md, RULES_OF_THE_ROAD_DRAFT_20261027.md (untracked)} |  | see members | group entry | 0 | REPO-SYNC/README.md header: NEEDED_BY Ziggy, Master Repo Claude, Nova; briefings by Claude. | Sync channel. README (git 2026-10-04): protocol, no mention of Help docs. MASTER_REPO_SYNC_OUT Briefing #002 (git 2026-10-10): section 3 'Du |

### A.2 root-and-sync (21 files)

| Path | Entry | Git last commit | sha256 (12) | Bytes | Owner as inferred by the finder | Purpose as inferred by the finder |
| --- | --- | --- | --- | --- | --- | --- |
| README.md | yes | 2026-10-04 | c38a899b0995 | 6829 | Ziggy + Nova (2025 text); Claude, Master Repo steward (2026 Pathfinder section, commit 02f3ab9). | Root readme. Two layers: a 2026 Pathfinder section (lines 5-18) that sends readers to Help/README.md, `python -m streamlit run Help/app.py - |
| MANIFEST.md | yes | 2025-11-27 | c556742b6c8c | 7914 | Nova (Author line 5), commissioned by Ziggy (line 6). | 'PANHANDLERS ROOT MANIFEST v1.0 , Nova-Prime Edition' (line 1-7). The only root file that claims to describe the whole repo: purpose/identit |
| PAN_HANDLERS_SPEC.md |  | 2025-11-27 | b960245af1b9 | 6413 | Nova/Ziggy (unsigned; v1.0 2025-11-27 at line 197). | Manifest schema v1 (lines 15-87) and architecture/folder plan (lines 90-147), 'Adding a New Repo' (149-154: add URL to config.py), MANIFEST_ |
| projects.json |  | 2025-11-27 | a6c5b24b2548 | 14937 | Ziggy + Nova (2025); no steward line. | Flagship project definitions read by dashboard/app.py (via utils.load_projects); meta tagline/philosophy (lines 2-7), seven flagship_project |
| LICENSE |  | 2025-11-27 | c6a87d285d50 | 1087 | ZiggyMack. | MIT License, Copyright (c) 2025 ZiggyMack. Not guidance. |
| .gitignore |  | 2026-10-04 | 7c4c7c1c1bb4 | 384 | Claude (2026 addition, commit 02f3ab9). | Standard Python/IDE ignores; `.streamlit/secrets.toml` (line 39); `/Help/.preview/` 'Local Pathfinder browser checks and screenshots' (lines |
| requirements.txt |  | 2026-10-09 | 3b62b678759f | 543 | Claude (commit a1c4f65). | Single dependency `streamlit>=1.36,<2` annotated 'Dashboard and Pathfinder guide (explicit navigation, tabs, forms)' (line 5); optional futu |
| REPO-SYNC/README.md | yes | 2026-10-04 | a01baac38a0f | 2092 | Master Repo Claude (line 3, 13-14). | Protocol of the Master Repo <-> collaborators sync channel (v1.0, STATUS Live): outbound MASTER_REPO_SYNC_OUT.md (lines 26-29), inbound SYNC |
| REPO-SYNC/MASTER_REPO_SYNC_OUT.md |  | 2026-10-10 | 642f9759f22c | 15688 | Claude, Pan_Handlers Master Repo steward and repository lead (lines 14-15). | Standing outbound briefing. Briefing #002 (2026-10-10, lines 12-195) states the Pan/CFA operating model (lines 30-48: CFA owns production in |
| REPO-SYNC/INDEX_SITE_BRIEF_RECOVERED_20261021.md |  | 2026-10-27 | 658970e09398 | 22971 | Claude, Pan_Handlers Master Repo steward (line 3). | Read-only recovered brief on 'the Pan_Handlers index site' from six sweeps. Section 0 inferred Pathfinder; the 2026-10-27 paragraph at line  |
| REPO-SYNC/RULES_OF_THE_ROAD_DRAFT_20261027.md |  | untracked | 482f2e6d613f | 32053 | Claude, lead writer and Pan_Handlers steward (lines 3, 151). | Draft v001 'Rules of the road: how Pan Handlers works with its collaborators' for Ziggy's review (line 3): house-style global rules G1-G11 ( |
| REPO-SYNC/SYNC_IN/pending/README.md |  | 2026-10-04 | e8abec90f446 | 301 | Master Repo Claude. | Inbox rule: one verbatim file per collaborator reply, `YYYY-MM-DD_<who>_<topic>.md`; Claude reads at session start, appends disposition, mov |
| REPO-SYNC/SYNC_IN/processed/README.md |  | 2026-10-04 | 5be754f8702c | 206 | Master Repo Claude. | Outbox rule: ingested replies land here with a one-line dated disposition appended; verbatim content above the note is never edited. |
| REPO-SYNC/SYNC_IN/processed/2026-10-10_nova_cfa_teaching_delta.md |  | 2026-10-10 | a6d6cb606a5a | 7585 | CFA Codex Nova (author); disposition by Master Repo Claude. | CFA Codex Nova's verbatim packet (lines 1-31) plus Claude's disposition (line 34). Line 27 is the only place that lists all Pan/CFA communic |
| docs/I_AM/I_AM.md | yes | 2026-07-21 | cff1063c0993 | 12407 | Claude (Repo) with Ziggy; v1.0 Nova/Ziggy 2025-11-27. | 'The soul of Pan Handlers' v2.0 (header lines 1-11; NEEDED_BY 'Anyone asking What is Pan Handlers?' line 7). Federation hub (line 38), three |
| docs/THE_MATRIX_MANIFEST.md | yes | 2025-12-01 | 95621caf7811 | 6971 | Ziggy + Nova (line 201). | Mythic vision of 'The Matrix' liminal portal page: 'A Universal Landing Page: Matrix.py becomes the first point of contact for ANY user or a |
| docs/prompts/dashboard_claude.md | yes | 2025-12-01 | 5314e6d372c1 | 2240 | Unsigned; 'Status: Active, Last Updated: December 2025' (lines 71-72). | Cold-boot prompt for a 'Pan Handlers Dashboard Claude': bootstrap file dashboard/START_HERE.md 'Read it first' (lines 10-14), key files (16- |
| .claude/launch.json |  | 2026-10-27 | 0c974fc4621c | 266 | Claude steward. | Claude Code browser-preview launch configuration; one configuration named 'pathfinder' (keys: version, configurations). Tracked in git since |
| .claude/settings.local.json |  | untracked | 8d52a07d6a16 | 217 | Ziggy/Claude (local). | Project-local Claude Code settings; single top-level key `permissions`. Not tracked; ignored by the global rule `**/.claude/settings.local.j |
| tests/ (16 files: test_collaborators.py, test_help_console.py, test_help_journey.py, test_image_edit_lab.py, test_model_filters.py, test_prompt_wiring.py, test_sampling_lab.py, test_scene_plan.py, test_scene_rehearsal.py, test_tutorial_register.py, test_video_handoff.py, test_video_plan.py, test_video_workshop.py, test_worked_example.py, test_workflow_decision.py, test_workflow_lab.py) |  | see members | group entry | 0 | Claude steward. | unittest + streamlit.testing AppTest suites, all against Help/app.py or Help modules. Run command documented only in test_help_console.py li |
| manifests/panhandlers-root.json |  | 2025-11-27 | bda253680e79 | 4623 | Ziggy + Nova + The Collective (line 4). | The repo's own manifest (not listed in MANIFEST.md's module table): display_name 'Pan Handlers Civilization Engine', tagline 'The Living Mus |

### A.3 circle-and-projects (24 files)

| Path | Entry | Git last commit | sha256 (12) | Bytes | Owner as inferred by the finder | Purpose as inferred by the finder |
| --- | --- | --- | --- | --- | --- | --- |
| circle/README.md | yes | 2026-07-16 | 4cef838f25c6 | 5366 | Not stated in file; Phase 0 built by P.H. Claude on Ziggy's charter (SHARED_HISTORY/TIMELINE.md line 9) | Methodology: the circle's front door. States the Five Laws (lines 32-42), a directory map (lines 52-72), working rules for adding claims/dig |
| circle/INDEX.md |  | 2026-07-21 | 8591a2e8c3dd | 11745 | Not stated; maintained by P.H. Claude per TIMELINE filing convention | Content/status board for the circle only: phase tracker (lines 10-19), member profile table (lines 23-36), registries table with counts (lin |
| circle/ARCHIVE_PLAN.md |  | 2026-07-16 | ef7446237ea5 | 12150 | Ziggy (charter received 2026-07-16, TIMELINE.md line 8) | Methodology: founding charter, declared canonical (lines 3-6: operational docs 'must not contradict it without a recorded revision'). Design |
| circle/ETHICS_AND_CONSENT.md |  | 2026-07-17 | 61f0de03b5bd | 7145 | Ziggy (decision) + P.H. Claude (filing); Nova (register spec) per revision log lines 131-133 | Methodology: 'The Gate'. §1 publication status PUBLIC and the ingestion filter enforced before every commit (lines 11-31); §2 content bounda |
| circle/CONSENT_REGISTER.md |  | 2026-07-17 | 1313775fa0d5 | 3090 | Spec per Nova (line 8); filed by P.H. Claude | Methodology/record: consent basis for publication, one row per member with scope, status (DIRECT for Ziggy, REPORTED for all seven others),  |
| circle/PROFILE_SCHEMA.md |  | 2026-07-16 | c03b786adb87 | 7895 | Not stated; derived from ARCHIVE_PLAN (line 7) | Methodology: the profile contract (confidence labels table lines 13-22, claim format, sections A-L). Schema v1.0 2026-07-16. |
| circle/CHAT_EXTRACTION_PROTOCOL.md |  | 2026-07-17 | 3e862f5648c8 | 31599 | Nova (design, lines 3-12); filed by P.H. Claude | Methodology: the dig instrument v0.2.2, ACTIVE and DESIGN FROZEN (line 1-6). Four-stage execution, source-discipline labels, promotion rules |
| circle/DEBATES/README.md |  | 2026-07-16 | 7b9d0827ca8d | 1431 | Not stated (Phase 0, P.H. Claude) | Methodology: record format for debate files (lines 12-37), fidelity discipline (lines 39-42). Status '0 debates recorded' (line 8); folder h |
| circle/SHARED_HISTORY/README.md |  | 2026-07-16 | 0fc7759bcc94 | 900 | Not stated (Phase 0, P.H. Claude) | Methodology: what belongs in the chronology ('lore as infrastructure', lines 3-6); suggested files TIMELINE.md, LEXICON_INTERNAL.md, NORMS.m |
| circle/SHARED_HISTORY/TIMELINE.md |  | 2026-07-21 | 57aafab7190c | 59346 | Rows attribute Ziggy, Nova, P.H. Claude per entry | Content: dated chronology of the archive with observer attribution per row (lines 6-30+). The most complete narrative record of how every ci |
| circle/mirror/README.md |  | 2026-07-21 | 83d81f0914de | 5256 | Not stated; built 2026-07-21 from Ziggy's reads plus archive layer | Methodology for a deliberately ungated side-project: STRAWMAN_<MEMBER>.md files that skip every gate (lines 3-17); two-layer model (lines 40 |
| circle/SYNC_OUT/README.md | yes | 2026-10-04 | 61393d2d3d3a | 9388 | Filed by P.H. Claude; 'Beefed up 2026-07-22 by Repo (Nyquist) Claude' (lines 163-166) | Methodology for exporting circle work to outside AIs: what the packet is (lines 9-34), reading order with CONSTITUTIONAL_BACKBONE.md marked  |
| circle/SYNC_OUT/{CONSTITUTIONAL_BACKBONE.md,DIG_MAP.md,IDEA_TRAILS_INDEX.md,GLOSSARY.md} |  | see members | group entry | 0 | Snapshots: P.H. Claude; GLOSSARY: not stated | Content: snapshot copies. BACKBONE and DIG_MAP carry a snapshot banner naming the master copy (diff shows banner is the only difference); ID |
| circle/IDEA_TRAILS/README.md |  | 2026-07-22 | 1e3e418b16b8 | 36038 | Not stated; filed by P.H. Claude | Mixed: methodology (trail file format, lines 13-32) then content (registry table of 131 candidates, 118 OPEN, from line 36). Header line 9 g |
| circle/CONSTITUTIONAL_BACKBONE.md |  | 2026-07-22 | 9b9521785fe8 | 10040 | Nova (synthesis) then verified/sourced by P.H. Claude (lines 10-13) | Content/synthesis: 'the archive's philosophical spine' compressing 131 trails into six structural questions (lines 3-7); first draft 2026-07 |
| circle/DIG_MAP.md |  | 2026-07-21 | 99c377b7f927 | 12422 | Not attributed; built 2026-07-21 (line 11) | Content: one row per source conversation (31 digs), grouped by underlying question, with a highest-signal shortlist (lines 3-13). |
| circle/evidence/chat_extractions/README.md |  | 2026-07-21 | cc11c7493a41 | 51838 | Not stated | Methodology + process board: how workbooks, synthesis packets, profile recursion and field-desk reviews work (lines 16-40, head only read; f |
| circle/evidence/corpus_sweeps/README.md |  | 2026-07-17 | b2dec9775121 | 1777 | Not stated | Methodology: sweeps are ORIENTATION ONLY, never promotable (lines 12-23); naming and header conventions (lines 25-41). |
| circle/MEMBERS/ |  | 2026-07-21 | directory | 0 | Per PROFILE_SCHEMA observer attribution | Content: one folder per member plus _TEMPLATE (10 skeleton files). 00_ZIGGY has PROFILE/OPERATOR_MAP/POSITION_LEDGER/SOURCE_INDEX (no MEMBER |
| circle/{OPERATOR_LEXICON.md,RELATIONSHIP_MAP.md} |  | see members | group entry | 0 | Not stated | Content registries: 14 operators all RED (LEXICON line 9); RELATIONSHIP_MAP declares itself a Phase 4 placeholder BLOCKED 0/3 (lines 3, 8) t |
| projects/ |  | 2025-11-27 | directory | 0 | Per file header: Ziggy + community (ABI, DCIA, voting); Caelum + Ziggy + Nova (gene_therapy); Daniel + Nova +  | Content: six concept/vision documents, one per flagship folder (ABI/VISION.md 166 lines, DCIA/VISION.md 218, gene_therapy/CONCEPT.md 98, mod |
| pages/ |  | 2025-11-27 | directory | 0 | Not stated; git author ZiggyMack | Content embedded in UI code: home.py (gallery), about.py (how to add a repo, lines 95-150), matrix.py (portal page, S0-S77 stack), glossary. |
| manifests/ |  | 2025-11-27 | directory | 0 | Each file's owner field; root: 'Ziggy + Nova + The Collective' (line 4), MANIFEST.md names Nova as author | Content/registration data: ten JSON manifests (panhandlers-root, cfa, nyquist_consciousness, ndo, abi, dcia, voting-lab, justice-lab, gene-l |
| data/ |  | 2025-11-27 | directory | 0 | Not stated | Content: single file glossary.md (v1.0, 'Shared language for the whole network', 137 lines): core concepts, S-stack S0-S9, personas, systems |

### A.4 cfa-links (11 files)

| Path | Entry | Git last commit | sha256 (12) | Bytes | Owner as inferred by the finder | Purpose as inferred by the finder |
| --- | --- | --- | --- | --- | --- | --- |
| Help/content/tutorial_register.py |  | 2026-10-09 | b86e751b5598 | 7701 | Panhandler Nova / Claude (October 4 integration) | Portable source register for the eight CFA transcript archives; absolute D:/Documents/CFA paths as provenance labels only (docstring L4-5: n |
| Help/content/video_routes.py |  | 2026-10-10 | c82e588784d4 | 20711 | Claude (Pan steward) | Video route cards; SOURCES tuple links CFA's production plan as dated research (L179). |
| Help/guides/prompt_wiring.py |  | 2026-10-09 | a31dfa754214 | 12248 | Panhandler Nova / Claude | Prompt-composition lesson; L94 cites 'docs/notes/explorable_world/comfy/workflows/README.md' as a CFA-root-relative text citation (not resol |
| Help/examples/cfa_pump_v001/manifest.json (and README.md) |  | see members | group entry | 0 | CFA Nova (Sept 12 contribution) | Portable copy of the September 12 CFA pump still evidence; manifest records source_checkout D:/Documents/CFA (L5) and canonical_evidence pat |
| tests/test_collaborators.py |  | 2026-10-20 | c2fc8e12509c | 3053 | Claude (Pan steward) | Test asserting the Oct 20 lesson's evidence path is exactly CFA's GEMINI_CLIP_SOURCES.txt (L46-51); the only automated guard on a Pan-to-CFA |
| CFA: docs/notes/explorable_world/comfy/projects/collaborators/kitchen_dispatch_20261030/OPERATOR_METHOD.txt |  | n/a | ac5eecf965e4 | 10617 | CFA Nova | CFA Nova's Oct 30 Kitchen coordination note. The only one of the five named CFA files with a true path pointer into Pan: L101 'D:/Documents/ |
| CFA: docs/notes/explorable_world/comfy/projects/collaborators/PRODUCTION_METHOD_20261012.txt |  | n/a | 8b62319c9626 | 15477 | CFA Codex Nova (transcription of Ziggy) | CFA production method of Oct 12 (Ziggy's direction via Personal Nova). Mentions Pan only as a role: L20 'Claude's creative responsibilities  |
| CFA: docs/notes/explorable_world/comfy/projects/collaborators/notebook_workflow/START_HERE.txt | yes | n/a | 4c3960bd82fa | 14215 | CFA Nova | CFA notebook collaboration start-here (Oct 9). L6 'SHARED METHOD OWNERSHIP: Nyquist remains the home of HOLY_GRAIL, the round/routing method |
| CFA: docs/notes/explorable_world/comfy/projects/collaborators/notebook_workflow/README.txt |  | n/a | d4b04bb564d7 | 4350 | CFA Nova | 'METHOD HOME , REUSE NYQUIST' breadcrumbs (L3-12): HOLY_GRAIL.md, WORKFLOW_SPEC.md, report_template.md in Nyquist. Pan's collaborators.py L1 |
| CFA: docs/notes/explorable_world/comfy/projects/collaborators/shared/STORYBOARD_WORKFLOW.txt |  | missing | missing | 0 | n/a | Named in the task as a possible shared storyboard workflow. Does not exist; the collaborators/shared/ directory does not exist either. Pan_H |
| CFA: docs/notes/explorable_world/comfy/projects/hon_dolo_strictly_business/story/writer_pass_20261010/START_HERE.txt | yes | n/a | f969b3da3791 | 15998 | Claude, lead writer | Claude's Hon Dolo writer's pass start-here (Oct 10, proposal). Its only 'Panhandlers' hit (L151, 'the stage-mic and Panhandlers-card panels  |

## Appendix B. The 71 confirmed findings, one line each (area, kind, where; details in section 3)

| # | Area | Kind | Where |
| --- | --- | --- | --- |
| 1 | help | contradiction | D:/Documents/Pan_Handlers/Help/README.md line 35 vs Help/CFA_FEEDBACK.md lines 3-149 |
| 2 | help | stale_pointer | Help/README.md line 35 and Help/FILE_MAP.md line 74 to Help/CFA_HANDOFF.md |
| 3 | help | contradiction | Help/CFA_FEEDBACK.md line 1 vs lines 3, 29, 57, 88, 120 |
| 4 | help | contradiction | Help/README.md lines 68-93 and 205-213; Help/pages/__init__.py line 1; vs Help/console.py line 18, Help/FILE_MAP.md line 20, tests/test_help_console.py 20-22 |
| 5 | help | missing_entry | Help/FILE_MAP.md lines 62-76; Help/README.md lines 193-203 |
| 6 | help | missing_entry | Help/README.md lines 3-46 vs 47-58 |
| 7 | help | ownership_unclear | Help/CFA_HANDOFF.md lines 1, 23, 82, 142-146, 196; Help/CFA_TUTORIAL_LEDGER.md lines 3, 27, 70, 101, 110, 173, 186 vs CFA_TUTORIAL_LEDGER.md 254 and CFA_FEEDBACK.md 5, 59 |
| 8 | help | ownership_unclear | Help/CFA_TUTORIAL_LEDGER.md (whole file) |
| 9 | help | duplicate | Help/CFA_TUTORIAL_LEDGER.md 22-30 and 278; Help/CFA_HANDOFF.md 15; Help/README.md 15, 95, 221; Help/FILE_MAP.md 95; REPO-SYNC/SYNC_IN/processed/2026-10-10_nova_cfa_teaching_delta.md 27; REPO-SYNC/RULE |
| 10 | help | duplicate | Help/CFA_FEEDBACK.md 3-27 / 57-86 / 88-118 / 120-149 vs Help/CFA_TUTORIAL_LEDGER.md 302-310 / 252-274 / 242-250 / 5-20; plus Help/README.md 3-11 and Help/CFA_HANDOFF.md 3-7 |
| 11 | help | duplicate | Help/README.md 53-58 and 215; Help/FILE_MAP.md 7-11 and 83; D:/Documents/Pan_Handlers/README.md 15; dashboard/README.md 18 |
| 12 | help | stale_pointer | D:/Documents/Pan_Handlers/README.md lines 177-182 (hop 1 of the newcomer path) |
| 13 | help | missing_entry | D:/Documents/Pan_Handlers/dashboard/START_HERE.md (git 2025-11-30) |
| 14 | help | stale_pointer | Help/CFA_HANDOFF.md lines 11 and 140; Help/README.md (no count) |
| 15 | help | stale_pointer | Help/CFA_FEEDBACK.md line 210 |
| 16 | help | duplicate | Agreed-but-undone maintenance recorded in Help/CFA_FEEDBACK.md 55 and Help/CFA_TUTORIAL_LEDGER.md 300: (a) guides/shared_controls.py 37, workflow_decision.py 33, prompt_wiring.py 91, content/cfa_learn |
| 17 | help | duplicate | Help/CFA_TUTORIAL_LEDGER.md 26; Help/content/collaborators.py 32 and evidence-state table; Help/README.md 45; REPO-SYNC/MASTER_REPO_SYNC_OUT.md 83 |
| 18 | help | contradiction | Help/README.md lines 3, 19, 45, 233 vs Help/content/cfa_learning.py REVIEWED and Help/content/collaborators.py REVIEWED |
| 19 | help | orphan | D:/Documents/Pan_Handlers/Help/.preview/cfa_handoff_return.README.md (2026-10-04) and cfa_collaborators_return.README.md (2026-10-08), with .receipt.json and .section.md siblings |
| 20 | help | missing_entry | Help/pages/start_here.py and Help/pages/sources_roadmap.py vs the five markdown docs |
| 21 | root-and-sync | contradiction | D:/Documents/Pan_Handlers/README.md lines 28-44 vs MANIFEST.md lines 13-33 vs docs/I_AM/I_AM.md lines 38, 190-199 vs Help/README.md lines 19, 33 vs REPO-SYNC/MASTER_REPO_SYNC_OUT.md lines 17-19, 30-48 |
| 22 | root-and-sync | contradiction | D:/Documents/Pan_Handlers/README.md line 11 vs Help/README.md line 19 and Help/console.py lines 28-32 |
| 23 | root-and-sync | stale_pointer | D:/Documents/Pan_Handlers/README.md lines 175-182 |
| 24 | root-and-sync | stale_pointer | D:/Documents/Pan_Handlers/README.md lines 170-173; PAN_HANDLERS_SPEC.md lines 149-154; pages/about.py line 140 |
| 25 | root-and-sync | stale_pointer | D:/Documents/Pan_Handlers/MANIFEST.md lines 39-77; PAN_HANDLERS_SPEC.md lines 94-116 |
| 26 | root-and-sync | stale_pointer | D:/Documents/Pan_Handlers/projects.json lines 70, 100-101, 192, 228-243 |
| 27 | root-and-sync | contradiction | D:/Documents/Pan_Handlers/docs/I_AM/I_AM.md line 80; projects.json line 237; data/glossary.md line 13; MANIFEST.md line 210 |
| 28 | root-and-sync | missing_entry | D:/Documents/Pan_Handlers/ (root) and D:/Documents/Pan_Handlers/docs/ |
| 29 | root-and-sync | orphan | D:/Documents/Pan_Handlers/REPO-SYNC/RULES_OF_THE_ROAD_DRAFT_20261027.md |
| 30 | root-and-sync | ownership_unclear | D:/Documents/Pan_Handlers/REPO-SYNC/INDEX_SITE_BRIEF_RECOVERED_20261021.md and REPO-SYNC/README.md |
| 31 | root-and-sync | contradiction | D:/Documents/Pan_Handlers/dashboard/START_HERE.md lines 69-76 and dashboard/.streamlit/config.toml vs dashboard/app.py lines 628-630 and docs/prompts/dashboard_claude.md lines 22-27 |
| 32 | root-and-sync | stale_pointer | D:/Documents/Pan_Handlers/docs/prompts/dashboard_claude.md line 48 vs requirements.txt line 5 and dashboard/app.py lines 663, 668 |
| 33 | root-and-sync | stale_pointer | D:/Documents/Pan_Handlers/dashboard/START_HERE.md lines 40-65; dashboard/README.md lines 26-51 and 98-119 |
| 34 | root-and-sync | duplicate | D:/Documents/Pan_Handlers/README.md lines 15, 179-182; dashboard/README.md lines 11-18, 171; dashboard/START_HERE.md lines 22, 164-168; docs/prompts/dashboard_claude.md line 41; dashboard/app.py line  |
| 35 | root-and-sync | duplicate | D:/Documents/Pan_Handlers/dashboard/START_HERE.md lines 115-119; dashboard/README.md lines 123-147; docs/prompts/dashboard_claude.md lines 29-33 |
| 36 | root-and-sync | ownership_unclear | D:/Documents/Pan_Handlers/README.md lines 158-162; MANIFEST.md lines 150-160, 232-241; REPO-SYNC/README.md lines 3, 13-14; REPO-SYNC/MASTER_REPO_SYNC_OUT.md lines 14-16, 41-42; REPO-SYNC/RULES_OF_THE_ |
| 37 | root-and-sync | contradiction | D:/Documents/Pan_Handlers/dashboard/START_HERE.md lines 18-23 vs Help/pages/start_here.py lines 13-19 and Help/README.md lines 5, 15, 25, 191 |
| 38 | root-and-sync | contradiction | D:/Documents/Pan_Handlers/docs/THE_MATRIX_MANIFEST.md lines 76-77, 182 vs pages/matrix.py lines 1-3 and the 2026 landing surfaces |
| 39 | root-and-sync | missing_entry | D:/Documents/Pan_Handlers/REPO-SYNC/MASTER_REPO_SYNC_OUT.md lines 56, 65, 75, 77, 81, 84, 90, 96, 110, 129, 241 |
| 40 | root-and-sync | missing_entry | D:/Documents/Pan_Handlers/tests/ |
| 41 | circle-and-projects | contradiction | D:/Documents/Pan_Handlers/circle/INDEX.md lines 19, 46, 56 |
| 42 | circle-and-projects | stale_pointer | D:/Documents/Pan_Handlers/circle/INDEX.md line 6 |
| 43 | circle-and-projects | missing_entry | D:/Documents/Pan_Handlers/circle/README.md lines 52-72 (Directory Map) |
| 44 | circle-and-projects | stale_pointer | D:/Documents/Pan_Handlers/circle/SHARED_HISTORY/README.md lines 10, 14-16 |
| 45 | circle-and-projects | stale_pointer | D:/Documents/Pan_Handlers/circle/evidence/chat_extractions/README.md line 12 |
| 46 | circle-and-projects | contradiction | D:/Documents/Pan_Handlers/circle/ARCHIVE_PLAN.md §IX lines 313-324 vs circle/ETHICS_AND_CONSENT.md §1-2 lines 11-44 and circle/README.md lines 100-107 |
| 47 | circle-and-projects | ownership_unclear | D:/Documents/Pan_Handlers/circle/mirror/README.md lines 63-79 vs circle/ETHICS_AND_CONSENT.md lines 20-31, 80 |
| 48 | circle-and-projects | duplicate | D:/Documents/Pan_Handlers/data/glossary.md, pages/glossary.py lines 9-128, circle/SYNC_OUT/GLOSSARY.md |
| 49 | circle-and-projects | contradiction | D:/Documents/Pan_Handlers/pages/matrix.py lines 288-313 vs pages/roadmap.py lines 23-34 vs data/glossary.md lines 27-55 vs manifests |
| 50 | circle-and-projects | contradiction | D:/Documents/Pan_Handlers/projects.json line 237 vs manifests/cfa.json line 3 vs data/glossary.md line 13 |
| 51 | circle-and-projects | contradiction | D:/Documents/Pan_Handlers/manifests/abi.json line 3, manifests/panhandlers-root.json line 70, MANIFEST.md line 88 vs projects.json line 166, projects/ABI/VISION.md line 1, data/glossary.md line 158, R |
| 52 | circle-and-projects | stale_pointer | D:/Documents/Pan_Handlers/projects.json lines 70, 100, 101, 192, 232, 239 |
| 53 | circle-and-projects | stale_pointer | D:/Documents/Pan_Handlers/manifests/cfa.json lines 84, 94, 104, 114, 124, 134, 144, 154 |
| 54 | circle-and-projects | ownership_unclear | D:/Documents/Pan_Handlers/manifests/cfa.json lines 76-157 vs Help/README.md lines 29-35 and REPO-SYNC/MASTER_REPO_SYNC_OUT.md lines 32-38 |
| 55 | circle-and-projects | stale_pointer | D:/Documents/Pan_Handlers/README.md lines 171, 179; MANIFEST.md lines 46, 76; PAN_HANDLERS_SPEC.md lines 97, 115, 153; pages/about.py line 140 |
| 56 | circle-and-projects | orphan | D:/Documents/Pan_Handlers/pages/ (home.py, about.py, matrix.py, glossary.py, roadmap.py, project_view.py) |
| 57 | circle-and-projects | missing_entry | D:/Documents/Pan_Handlers/MANIFEST.md §II lines 37-77 |
| 58 | circle-and-projects | ownership_unclear | D:/Documents/Pan_Handlers/manifests/panhandlers-root.json line 36 vs circle/ and docs/I_AM/I_AM.md lines 170-178 |
| 59 | circle-and-projects | stale_pointer | D:/Documents/Pan_Handlers/circle/RELATIONSHIP_MAP.md lines 3, 8 and circle/INDEX.md line 18 |
| 60 | circle-and-projects | duplicate | D:/Documents/Pan_Handlers/circle/SYNC_OUT/{CONSTITUTIONAL_BACKBONE.md,DIG_MAP.md,IDEA_TRAILS_INDEX.md} |
| 61 | circle-and-projects | stale_pointer | D:/Documents/Pan_Handlers/pages/roadmap.py lines 113-122, pages/matrix.py lines 411-417, projects.json line 13, README.md lines 73, 144-146 |
| 62 | cfa-links | missing_entry | D:/Documents/Pan_Handlers (no collaborator start-here) |
| 63 | cfa-links | stale_pointer | D:/Documents/Pan_Handlers/README.md L178-179; MANIFEST.md L46; PAN_HANDLERS_SPEC.md L96; README.md L171 |
| 64 | cfa-links | stale_pointer | D:/Documents/Pan_Handlers/Help/README.md L3-7, L19; Help/CFA_HANDOFF.md L3-7 |
| 65 | cfa-links | duplicate | D:/Documents/Pan_Handlers/Help/CFA_HANDOFF.md L163-196 vs Help/CFA_TUTORIAL_LEDGER.md L124-173 |
| 66 | cfa-links | duplicate | Ownership statement (CFA production / Pan teaching / Nyquist notebook method) restated in eight Pan files |
| 67 | cfa-links | duplicate | Evidence-state vocabulary: Help/content/collaborators.py L260-271 vs Help/CFA_TUTORIAL_LEDGER.md L26 |
| 68 | cfa-links | orphan | D:/Documents/Pan_Handlers/REPO-SYNC/RULES_OF_THE_ROAD_DRAFT_20261027.md |
| 69 | cfa-links | ownership_unclear | D:/Documents/CFA/docs/notes/explorable_world/pathfinder_handoff/README.md (the cross-repo link map) |
| 70 | cfa-links | ownership_unclear | Deploy source of the parent app: Help/README.md L215, Help/FILE_MAP.md L11, dashboard/START_HERE.md L13, RULES draft L128 and L148 |
| 71 | cfa-links | stale_pointer | D:/Documents/Pan_Handlers/Help/content/collaborators.py L116 (Flow boundaries) |

