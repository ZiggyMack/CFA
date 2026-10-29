# CFA Creative Studio

A standalone Streamlit review room for Hon Dolo, Lisan Al Gaib, and clips that still need a project. The layout borrows the Pan Handlers Help app's grouped sidebar, restrained color palette, and progressive detail. It has no Pan Handlers runtime dependency.

Hosted entry: [algaib.streamlit.app](https://algaib.streamlit.app/).

## Current local-index mirror and mobile reviews

[Full Visual Library](https://algaib.streamlit.app/Full_Visual_Library) serves the current local index's exact JavaScript and CSS with verified, browser-sized media. It starts at Intake, including Still to review / Reviewed / All families, batch gallery and detailed evidence views, the winners visual map, cast filters, note presets and the current local review layout. Reviews remain in that browser across Streamlit reruns. Export review and import the JSON on the desktop to transfer decisions; this is not automatic cross-device synchronization.

The compact Creative Studio shares the published catalog and offers quick triage, notes, note presets, optional scores and previous/next Intake navigation. Its changes remain in the Streamlit session, so Export review is available in the sidebar and beside the review controls. The two views have separate review storage. Use the Full Visual Library for longer sessions and use JSON export/import when switching views or devices.

The October 28 publication reconciles the latest exact-hash local review export field by field. Newer canonical decisions and equal-time conflicts remain canonical. Provider findings never become user acceptance through this reconciliation. Image identities and source hashes are retained while the hosted images are review copies.

Prepare both current publication snapshots:

```powershell
python apps/creative_studio/build_design_library.py --expected-source-sha <catalog-sha256> --review-export <latest-review.json> --expected-review-sha <review-sha256> --review-mode latest
python apps/creative_studio/build_portable_dashboard.py
```

Publish the changed application modules, all `design_manifest.json` publication files, and the portable dashboard receipt's publication files together. These are explicit allowlists; the older original-master dashboard builder is not needed for this deployment. The full mirror keeps original media outside the publication and supplies an honest hosted-copy label. Registered text-document changes must be reconciled before packaging; an image/hash mismatch fails verification.

## Run locally

From the CFA repository root:

```powershell
python -m streamlit run apps/creative_studio/app.py
```

The tested requirement is `streamlit==1.52.1`. Install `apps/creative_studio/requirements.txt` in the deployment environment. The app otherwise uses Python's standard library.

For a new Streamlit Community Cloud deployment, choose the **CFA repository**, the branch containing this app, and main file **`apps/creative_studio/app.py`**. This is a separate app from Pan Handlers. Committing files alone does not configure a new deployment.

## Portable library

The app expects `library/catalog.json` beside `app.py`, with `projects`, `assets`, `albums`, and `categories` arrays. It follows the same catalog contract as the CFA local visual library. Preserve the supplied album order and each album's `assetIDs` order; Lisan's placement portraits precede stencil options.

Media `src` and `thumb` values must resolve to files inside `library/`. The app rejects remote URLs, drive paths, and paths escaping that directory. The portable bundle should contain browser-sized review images, thumbnails, selected clips, and supporting documents. It does not need the original Windows download folders. Document `text` is displayed as inert text; technical source files are never executed by the review UI.

Native `st.image` and `st.video` serve packaged files through Streamlit. No static HTML hosting, iframe file access, local web server, or authenticated media endpoint is required. Videos load on the expanded review view; collection pages use still previews. Large collections paginate at 24 items.

## Review behavior

- **Ziggy’s Corner / Mission Control:** the first view in a new session. Current index tasks appear as collapsed status/title/project cards, with summary counts first, a closed Top priority section and collaborator handoffs. A compact Image review area offers Review images only when unanswered requests remain. The Shot plans count opens visible saved plans across all projects; review sweep stays in a closed disclosure. Before sending lists prerequisites; Deliverables lists expected returns; later review stays separate. Shortlist counts respect saved Keep/Fix/Remove decisions. References open within the Corner, and reviewed history remains accessible. The page does not monitor third-party accounts or imply a draft was sent.
- **Library:** filter by category, album, and words; open an item for its larger picture or video and review details. Videos have independent Layout (Grouped or All clips) and Sort (Longest first, Shortest, or Alphabetical A–Z) controls. The default is Grouped with Longest first within each scene category, alphabetical ties, unknown durations last, and turnarounds at the bottom. All clips sorts across the current collection/search.
- **Storyboard:** filter by planning stage, source-panel position, and story themes. Narrowing the position range also narrows the available themes. Stages are Preliminary, Detailed design, Verification, and Production; changing a stage does not claim a technical check passed. Planning order does not imply measured song timings.
- **Collaborators:** a global production workspace with ComfyUI first, then Flow, Gemini, Grok, and Panhandler Nova. ComfyUI shows concrete saved workflow records and their actual inputs, outputs/previews, documents, and execution status. Cloud links are restricted to `https://cloud.comfy.org/` and do not run the graph. Other providers show their saved tasks and current briefs across projects. A local FFmpeg result must not be described as a Cloud execution.
- **Collaborator briefs:** separate Gemini, Flow, Grok, and Shared roles sections. Current Grok care-package files are included; earlier exploration briefs remain in Documents as history. Flow's recommended first steps sit beside its starter download, with the canonical Start here · Flow guide in its own expander.
- **Needs review / Review queue:** Needs review groups active references needing attention, including saved Needs fixes decisions. Review queue keeps the complete decision history. Marking removal never deletes a file; it hides the reference from ordinary design browsing. Clear removes the decision while preserving the note and shot plan.
- **Shot plans:** quick Flow / Grok / Gemini toggles appear next to the star and export basket in an open reference. One click queues a local draft and shows that it has not been sent. Expand Plan a shot to refine the idea, prompt, and destinations. Turning off the final provider retains the idea/prompt under undecided; Remove shot plan clears the draft explicitly. Export TXT or JSON handoffs filtered by project, destination, and search. Attach the source images and current character/reference kit separately: a handoff is a reference manifest, not an image ZIP.
- **Export basket:** a separate selection across both projects, independent of stars and review flags. Export its `cfa-visual-export-v1` JSON selection list, or prepare an in-memory ZIP of hosted review copies plus a manifest. The ZIP retains original-reference hashes alongside actual packaged-copy hashes, includes duplicate content only once, and is limited to 100 MB of selected files. It does not contain original masters. Clearing the basket leaves favorites, reviews, and source files alone.
- **Favorites & notes:** export the complete review to retain decisions, notes, shot plans, and stars from every project. All changes are held in the current Streamlit session; another browser or a restarted session does not automatically retain them.
- **Details:** character profiles open individual tattoo or piercing objects, with placement examples and stencils kept distinct. All references remains available as a mixed view when needed.
- **Documents:** six parent groups collect related notes, including one Design & outfit notes parent. Parent and child counts include their documents; both levels start collapsed and matching search results expand.

Mission Control and Collaborators include a Back to library button that returns to the previous project view. Mission Control's Prepare review sweep downloads the current decisions, favorites, and eligible working-reference requests for a manual Nova handoff; it does not invoke an agent or alter any source file.

Open a reference to choose its Prime or Multiverse lane and request a working-reference scope (complete look, identity, outfit, scene, or detail). Requests remain pending until reviewed; they never move an item into the working-reference category automatically. Multiverse, removed, and archived entries cannot request promotion into Prime. Provider handoffs and basket exports default to Prime, excluding Multiverse and removals; the explicit Multiverse creative ingredients export intent permits alternate-lane ingredients while still excluding removals. Canonically archived entries stay in review bookkeeping but disappear from ordinary browsing, favorites, and exports. A session removal flag alone does not archive an item.

Complete reviews use `cfa-visual-review-v1`: `items` carry `id`, the original source `sha256`, `status` (`keep`, `needs_fixes`, `remove`, or explicit `null`), `note`, and optional `shotPlan`; `favorites` carries reference objects. A plan is `{status: "planned", destinations: [...], idea: "...", prompt: "..."}`; `shotPlan: null` explicitly clears it. Provider handoffs use `cfa-shot-handoff-v1` and are not session restore files.

Optional review fields are `variant` (`prime` or `multiverse`), `workingReference` (`{status, scope}` or `null`), and `storyboardStage` (`preliminary`, `detailed_design`, `verification`, `production`, or `null` to use the source stage). `variantSource` distinguishes a user lane choice from a catalog-derived snapshot: importing a stale catalog lane cannot overwrite a fresh seed. Fields merge independently, so an older note-only export cannot erase new canonical lane decisions. Full review backups retain archived/removal/Multiverse records even when production exports exclude them.

Supplied `catalog.reviewDecisions` seed the initial review. Session choices override matching seed fields, so an explicit Clear or removed shot plan stays cleared on reruns and after export/import. Import merges matching IDs, requires exact original hashes for new review exports, and skips unmatched or invalid entries. Legacy `cfa-visual-favorites-v1` files still import; their supplied hashes are checked, and optional `notes`/`note_refs` remain supported. Legacy note imports do not erase seeded decisions. Complete review files also carry optional `exportBasket` references; omitting that field leaves the current basket alone. Imports merge selections instead of removing existing favorites or basket entries absent from a file.

Mission Control reads `catalog.missionControl.tasks` as saved data. Task links may name a packaged `assetID` or a `downloadPath` resolving to a `.zip` inside `library/`. Local `href` fields are ignored by the hosted app. Care-package downloads are separate prepared files; creating a session shot plan does not rewrite them or send them anywhere.

The production workspace reads `catalog.productionWorkflows`: each record has `id`, `provider`, `project`, `title`, a human-readable `status`, `summary`, `nextAction`, source/output/document asset ID lists, and an optional bounded `cloudURL`. These are workflow bookkeeping records, not executable instructions. Linked media opens in the same gallery viewer.

JSON/TXT handoffs contain references and notes; the separately prepared basket ZIP contains review media. A star is a shortlist choice, and Keep only records the stated review scope; neither changes the source catalog's production approval. The application never writes review changes to the packaged catalog or original source files.

## Synchronizing Ziggy’s Corner only

Run python apps/creative_studio/build_mission_control.py after the local index catalog is updated. It prepares library/mission_control.json, library/mission_manifest.json and content-addressed files under library/mission_media/. It packages task references, collection links and saved review identities from the same generated catalog used by the index. It verifies original hashes, reuses verified existing previews, and reports missing references. The base library/catalog.json and general browsing collections stay unchanged.

The app uses this snapshot for the Corner when present, otherwise it uses its existing catalog. Reviews merge current snapshot seeds with session overrides; explicit clears remain authoritative. Full review exports and review sweeps retain Corner-only and base-library references, likeness and scene ratings, scoped component notes and review provenance. Mutable document contents can refresh under their existing IDs; reviewed image/video hashes cannot.

Deploy the changed Python files, the two snapshot JSON files, and **every path listed in mission_manifest.json outputs** to the existing app. Some outputs reuse base-library files. Running the builder only prepares local files; it does not commit, upload or update Streamlit. This is a publication snapshot, not live monitoring or automatic two-way browser storage sync. Export/import remains the review-transfer mechanism.

## Complete local-design publication

When `library/design_catalog.json` exists, the native app uses that complete snapshot for every view, including Ziggy’s Corner. It takes precedence over both the smaller original catalog and the older Corner-only snapshot. The Full Visual Library page opens the native Library so both entry points share the same session review.

The sidebar provides Working references, Outfits, Tattoos & piercings, Supporting cast, Storyboard, Videos, Comfy swap targets, Needs review, and Archive. Hon’s retired Inspiration collections move to Archive; Lisan retains Inspiration. No second Needs fixes list is added to Ziggy’s Corner.

- Working references opens one character BOM gallery. Dolo appears alongside the supporting characters. His nested sections keep one dental standard, Body art, Bling bling before Wardrobe, explicit Approved Multiverse choices, Video production candidates, one WIP disclosure, and the Verbose BOM. Reference-purpose previews are visible when the character opens.
- Hon outfits use Formal attire, Casual, and Scoundrel gear tags and expandable collections. Tattoo subjects pair artwork, mannequin placement, and applicable revision-needed proofs before their remaining examples. Creature boss ideas appear once under Supporting cast. Comfy keeps its ancillary swap references.
- Archive and Restore use `collectionState: archived|working`, separately from review status. Restore overrides default historical membership but does not clear a removal decision. Full review exports retain historical decisions, exact-hash validation evidence, and scene reviews.
- `multiverseSelection: candidate|approved` records an explicit choice. Approved Multiverse requires a character score of at least two and a visible Multiverse reference; neither stars nor the lane alone selects it.
- Retired visual-duplicate IDs resolve through the verified `assetAliases` family for navigation and review transfer. Only matching original hashes may redirect review records; validation evidence stays attached to its original ID/hash. Timestamped clear receipts prevent older exports from reviving cleared shot plans.
- Storyboard starts with the project’s song and offers separate independent sequences and writings. Shot material roles and pending references stay visible without converting availability into acceptance.

Prepare the complete publication with:

```powershell
python apps/creative_studio/build_design_library.py --expected-source-sha <catalog-sha256> --review-export <verified-review.json> --expected-review-sha <review-sha256>
```

The builder preserves all current asset identities and configuration, verifies source hashes, reuses verified existing packaged media, and writes missing browser-sized copies under `library/design_media/`. Safe self-contained SVG placement diagrams retain their original bytes. Text comes only from catalog source paths, including publication-safe writer excerpts. Existing verified Corner supplemental downloads are retained without discovering unrelated local files. The supplied review export only contributes the two newer, exact-hash explicit plan clears; it is not bundled or imported wholesale.

Publish `design_catalog.json`, `design_manifest.json`, every manifest `publicationFiles` entry (including reused files), and the changed native Python modules together. The builder is offline and does not publish. Review changes still require export/import between sessions or devices; the snapshot is not automatic two-way synchronization.

## Checks

From the repository root:

```powershell
python -m unittest discover -s apps/creative_studio/tests -v
```

The checks cover bundle path isolation, collection order, legacy and current hash compatibility, seed restoration, explicit clears, provider-filtered handoffs, draft-only plan state, and unchanged source bytes. Streamlit interaction checks exercise pagination, project navigation, storyboard rendering, collaborator text, review decisions, and plan save/removal. Native widgets keep the sidebar toggle accessible on narrow screens.

## Legacy full dashboard mirror

Without a complete design snapshot, the separate **Full Visual Library** page can reuse the older HTML dashboard. Prepare that fallback with `python apps/creative_studio/build_full_dashboard.py`, then use Streamlit's page sidebar. When a design snapshot is present, this entry opens the native Library instead. Local fallback bundles use hardlinks on D: and preserve all original bytes and review IDs; nothing is uploaded by the builder.

See [full dashboard preparation and deployment notes](FULL_DASHBOARD_README.txt) for phone review transfers, an explicit portable-copy option, media size and hosting constraints. The hosted page needs its complete bundle before deployment; preparation is not publication or cross-device autosync.
