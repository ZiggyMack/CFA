FULL VISUAL LIBRARY — SEPARATE STREAMLIT PAGE

This mirrors the complete local HTML dashboard inside Streamlit, using the same
library.js, library.css and catalog data. The original abbreviated Creative Studio
app and its portable library are unchanged. Streamlit's normal multipage sidebar
adds Full Visual Library; that page also links back to Creative Studio.

PREPARE AND RUN LOCALLY
From D:\Documents\CFA:
  python apps/creative_studio/build_full_dashboard.py
  python -m streamlit run apps/creative_studio/app.py

Run the existing visual_library/build_catalog.py first whenever the source catalog
needs rebuilding. The mirror builder packages the current generated catalog; it
does not rebuild or change it. After UI/catalog changes, rerun the mirror builder.

The default output is apps/creative_studio/full_dashboard_bundle. Each snapshot is
identified by the source code/catalog hashes. current.json points to the completed
snapshot only after successful preparation. The builder never deletes old files,
executes document source code, converts imagery, uploads assets, or launches a server.

LOCAL STORAGE AND ORIGINALS
All packaged media are content-addressed and allowlisted by the catalog or prepared
Mission Control links. The default creates NTFS hardlinks on D:, using no additional
media bytes. They are serving references to the original bytes: do not edit files
inside a generated snapshot. Editing a hardlinked media file would edit its master.
Generated code/catalog files are separate files and replaced atomically.

This page uses a declared Streamlit v1 component; it does not expose the whole
repository, use a separate file server, or rely on local Windows file URLs.
Component documentation: https://docs.streamlit.io/develop/api-reference/custom-components

REVIEWS ON A PHONE
The same dashboard code provides browser backup, notes, scope selection, favorites,
import, export and review-sweep behavior. Originals and ID/hash identity remain the
same. The hosted origin has separate browser storage from the local file dashboard
and from the compact Streamlit app's session state. Export a complete review JSON
and import it on the other device/page to transfer it. There is no automatic cloud
sync or notification to Nova. File-picker autosave depends on browser support;
the existing Export review fallback remains available on mobile browsers.

The source dashboard already has phone CSS. The page offers Workspace height to
fit the inner image viewer to a phone. No visual browser QA was performed while
the local browser security restriction is in effect; packaging and source tests
are separate from an actual deployed phone check.

HOSTING / DEPLOYMENT HANDOFF
Nothing has been deployed or uploaded by this implementation. The existing hosted
app will keep its abbreviated page. A host needs the new page, builder support
files, and a complete chosen snapshot plus current.json. A separate app can point
to the page only after adjusting its back-to-Studio link for that deployment.

For an independent portable bundle, explicitly use:
  python apps/creative_studio/build_full_dashboard.py --copy-media

Copy mode duplicates the exact original bytes once per unique packaged file; it
does not silently substitute the older abbreviated library or recompress masters.
Check bundle_manifest.json for total bytes, asset count, hashes and missing prepared
links before choosing upload/storage. Images are lazy-loaded and video is opened
on demand, but this is the full collection, so host storage and phone bandwidth
cost more than the existing reduced preview library. Review derivative generation
could be a later explicit choice; it is not performed by this mirror.

The installed Streamlit 1.52.1 component handler reads a requested file in full and
does not implement media byte-range responses. Large video playback/seeking may
therefore wait for the file download and use more server memory than the compact
app's native media handler. Verify this on the intended phone/host before relying
on long clips; a reviewed media-hosting or proxy strategy can be chosen separately.

The generated bundle is git-ignored. Do not assume a commit alone deploys it. Its
contents include the catalog's full documents and media, so keep the intended
hosting audience/access restrictions when coordinating deployment. Streamlit
component assets are reachable through that deployment's component URLs. Do not
publish the bundle as a side effect of fixing navigation.

OFFLINE CHECKS
  python -m unittest discover -s apps/creative_studio/tests -p test_full_dashboard.py -v

Tests verify hardlink deduplication, original byte preservation, unchanged UI source,
ID/review preservation, explicit portable copies, inert helper documents, path
isolation and failure behavior before current.json is promoted.
