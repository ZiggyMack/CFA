# CFA Creative Studio

A standalone Streamlit review room for Hon Dolo, Lisan Al Gaib, and clips that still need a project. The layout borrows the Pan Handlers Help app's grouped sidebar, restrained color palette, and progressive detail. It has no Pan Handlers runtime dependency.

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

- **Library:** filter by category, album, and words; open an item for its larger picture or video and review details.
- **Storyboard:** illustrated panels grouped by story sequence, with lyric connections and review notes when supplied. Planning order does not imply measured song timings.
- **Collaborator kits:** Gemini instructions and maps, Flow briefs, collaborator roles, and Grok instructions when included in the catalog.
- **Favorites & notes:** stars and notes are held in the current Streamlit session. Export them before leaving; another browser or a restarted session does not automatically retain them.
- **Documents:** grouped supporting notes stay behind expanders.

Favorites retain the `cfa-visual-favorites-v1` interchange format used by the local gallery. Import merges known IDs and rejects supplied hash mismatches. The optional `notes` and `note_refs` fields carry review notes and their source hashes; older gallery exports work without them. Exports contain references and notes, not media. A star is a review shortlist choice and never changes an asset's production approval.

## Checks

From the repository root:

```powershell
python -m unittest discover -s apps/creative_studio/tests -v
```

The checks cover bundle path isolation, supplied collection order, favorite/hash compatibility, pagination, project navigation, storyboard rendering, and collaborator text. The app uses native Streamlit widgets and keeps the sidebar toggle accessible for narrow screens.
