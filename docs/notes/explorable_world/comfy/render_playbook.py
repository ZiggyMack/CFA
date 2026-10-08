"""Render the Comfy handbook as a self-contained offline reader.

Run from the repository root:
    python docs/notes/explorable_world/comfy/render_playbook.py

Uses the Markdown package already used by the parent research reader.
"""

from html import escape
from pathlib import Path
import re

import markdown


ROOT = Path(__file__).resolve().parent
SECTIONS = [
    ("video-first", "Video: choose the workflow"),
    ("start", "September checkpoint"),
    ("graph", "Read the graph"),
    ("resources", "GitHub and resource reviews"),
    ("sop-1", "1. Connect and discover"),
    ("sop-2", "2. Reuse a community workflow"),
    ("sop-3", "3. First pump image"),
    ("sop-4", "4. Controlled edits"),
    ("sop-5", "5. Static mesh and engine"),
    ("sop-6", "6. Preserve and reproduce"),
    ("sop-7", "7. Cost and recovery"),
    ("sop-8", "8. Simple creative controls"),
    ("learning", "Keep learning"),
    ("sources", "Sources"),
]

STYLE = """
:root { color-scheme: light; font-family: Georgia, 'Times New Roman', serif; }
* { box-sizing: border-box; }
body { margin: 0; background: #fff; color: #24272a; }
.layout { display: grid; grid-template-columns: 250px minmax(0, 1fr);
          max-width: 1360px; margin: auto; }
nav { border-right: 1px solid #ddd; padding: 32px 24px;
      font: 14px/1.5 Arial, sans-serif; }
nav .contents { position: sticky; top: 24px; max-height: calc(100vh - 48px);
                overflow-y: auto; }
nav strong, nav a { display: block; margin-bottom: 12px; }
nav .files { border-top: 1px solid #ddd; padding-top: 16px; margin-top: 20px; }
main { min-width: 0; padding: 38px 52px 80px; font-size: 18px; line-height: 1.65; }
h1 { margin: 0 0 28px; font-size: clamp(30px, 4vw, 44px); line-height: 1.15; }
p { margin: 0 0 20px; }
a { color: #254f65; text-underline-offset: 3px; overflow-wrap: anywhere; }
nav a { text-decoration: none; }
nav a:hover { text-decoration: underline; }
a:focus-visible { outline: 2px solid #254f65; outline-offset: 4px; }
a[id] { display: block; scroll-margin-top: 22px; }
a[id] + p { font-size: 23px; line-height: 1.3; margin-top: 40px; }
li { margin-bottom: 11px; }
table { width: 100%; border-collapse: collapse; margin: 24px 0;
        font: 14px/1.5 Arial, sans-serif; }
th, td { padding: 11px 9px; text-align: left; vertical-align: top;
         border-bottom: 1px solid #ddd; overflow-wrap: anywhere; }
th { background: #f2f3f4; border-top: 1px solid #bbb; }
sup { line-height: 0; }
.footnote { border-top: 1px solid #bbb; margin-top: 28px; padding-top: 20px;
            font: 14px/1.6 Arial, sans-serif; }
.footnote hr { display: none; }
.footnote p { margin-bottom: 0; }
.skip { position: absolute; left: -10000px; }
.skip:focus { left: 12px; top: 8px; padding: 10px; background: white; }
@media (max-width: 920px) {
  .layout { display: block; }
  nav { border-right: 0; border-bottom: 1px solid #ddd; padding: 24px; }
  nav .contents { position: static; max-height: none; }
  nav a { display: inline-block; margin: 0 15px 10px 0; }
  main { padding: 30px 24px 60px; font-size: 17px; }
  table { font-size: 12px; }
  th, td { padding: 9px 6px; }
}
@media print {
  @page { size: A4; margin: 17mm; }
  .layout { display: block; }
  nav, .skip { display: none; }
  main { padding: 0; font-size: 10pt; line-height: 1.45; }
  h1 { font-size: 25pt; }
  a { color: inherit; }
  a[id] + p { font-size: 13pt; margin-top: 18pt; break-after: avoid; }
  p { margin-bottom: 10pt; orphans: 3; widows: 3; }
  li { margin-bottom: 6pt; }
  table, .footnote { font-size: 8pt; line-height: 1.4; }
  th, td { padding: 6pt; }
  tr { break-inside: avoid; }
}
"""


def main():
    source = (ROOT / "PLAYBOOK.md").read_text(encoding="utf-8")
    anchors = set(re.findall(r'<a id="([^"]+)"></a>', source))
    missing = {key for key, _ in SECTIONS} - anchors
    if missing:
        raise ValueError(f"Missing navigation targets: {sorted(missing)}")
    body = markdown.markdown(source, extensions=["tables", "footnotes"])
    links = "\n".join(
        f'<a href="#{escape(key)}">{escape(label)}</a>' for key, label in SECTIONS
    )
    page = (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="description" content="Comfy video workflow selection, '
        'source-scene transformation, high-resolution finishing and production procedures.">'
        '<title>Comfy video workshop</title>'
        f'<style>{STYLE}</style></head><body>'
        '<a class="skip" href="#content">Skip to handbook</a><div class="layout">'
        '<nav aria-label="Handbook contents"><div class="contents">'
        f'<strong>Comfy handbook</strong>{links}'
        '<div class="files"><a href="PLAYBOOK.md">Markdown source</a>'
        '<a href="LESSONS.md">Learning record</a>'
        '<a href="templates/run_record.json">Run record template</a>'
        '<a href="pump_concept_prompt.txt">Pump concept prompt</a>'
        '<a href="../lobby_concept.html">Observatory lobby concept</a>'
        '</div></div></nav>'
        f'<main id="content">{body}</main></div></body></html>\n'
    )
    destination = ROOT / "index.html"
    destination.write_text(page, encoding="utf-8")
    print(f"Rendered {destination.name}; {len(SECTIONS)} navigation links.")


if __name__ == "__main__":
    main()
