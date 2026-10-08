# Creative Studio review previews

This package supports browsing, comparing and shortlisting Hon Dolo and Lisan Al Gaib assets. Its images and videos are review previews; the unchanged local source files remain the production masters.

- `catalog.json` retains the visual library's project, album and asset IDs. Every `src` and `thumb` is relative to this directory.
- `images/` contains JPEG previews up to 1280 pixels; `thumbs/` contains lightweight previews up to 480 pixels.
- `videos/` contains H.264 proxies with the complete source picture duration and soundtrack. The existing 16:9 clips become 832 × 468, preserving their exact aspect ratio. Audio is re-encoded to AAC at 96 kb/s; this is not an audio-quality master.
- `animations/` retains the supplied GIF. `docs/` contains the PDF and inert text previews; supplied helper scripts are distributed only as `.txt` and are never executed by the builder.
- `manifest.json` records original and generated SHA-256 hashes, encoding settings, decode checks and source-preservation checks. Favoriting an item does not approve it for production.

Rebuild offline with `python apps/creative_studio/build_library.py` from a checkout containing the local source assets. Pillow and FFmpeg are required; use `--ffmpeg PATH` if needed. The builder performs no downloads and does not modify the masters. It reuses verified outputs when their source hashes and settings match.

Machine-specific absolute paths are removed from hosted text previews. Repository-relative provenance fields remain available for tracing a selection back to its master.
