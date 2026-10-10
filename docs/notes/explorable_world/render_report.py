"""Render the local research brief as an offline HTML document."""

from pathlib import Path
import re

import markdown


ROOT = Path(__file__).resolve().parent
SECTIONS = [
    ("reference", "Design references"),
    ("curiosity", "Curiosity"),
    ("inherited-purpose", "Inheriting a purpose"),
    ("expeditions", "Upgrades and expeditions"),
    ("world", "A changing world"),
    ("care", "Care and consequences"),
    ("lobby", "Knobs of Care"),
    ("three-rooms", "Three-room journey"),
    ("chapter", "First chapter"),
    ("puzzle", "The relay puzzle"),
    ("conversation", "The conversation"),
    ("atmosphere", "Atmosphere"),
    ("inheritance", "Existing CFA material"),
    ("technology", "Engine choice"),
    ("pipeline", "Data and game state"),
    ("production", "Production passes"),
    ("evaluation", "Playtesting"),
    ("sources", "Sources"),
]

STYLE = """
:root { color-scheme: light; font-family: Georgia, 'Times New Roman', serif; }
* { box-sizing: border-box; }
body { margin: 0; color: #202326; background: #fff; }
.layout { max-width: 1340px; margin: auto; display: grid;
          grid-template-columns: 230px minmax(0, 1fr); }
nav { padding: 40px 24px; border-right: 1px solid #ddd;
      font: 14px/1.45 Arial, sans-serif; }
nav .contents { position: sticky; top: 28px; }
nav strong { display: block; margin-bottom: 16px; }
nav a { display: block; margin: 0 0 12px; text-decoration: none; }
nav a:hover { text-decoration: underline; }
nav .source { border-top: 1px solid #ddd; padding-top: 16px; margin-top: 22px; }
main { min-width: 0; padding: 40px 56px 80px; font-size: 18px; line-height: 1.7; }
h1 { font: 600 44px/1.14 Georgia, serif; letter-spacing: -.02em; margin: 0 0 30px; }
p { margin: 0 0 21px; }
a { color: #244f67; text-underline-offset: 3px; }
a[id] { display: block; scroll-margin-top: 24px; }
a[id] + p { margin-top: 45px; font-size: 22px; line-height: 1.4; }
table { width: 100%; border-collapse: collapse; margin: 26px 0;
        font: 14px/1.5 Arial, sans-serif; }
th, td { text-align: left; vertical-align: top; padding: 11px 10px;
         border-bottom: 1px solid #ddd; overflow-wrap: anywhere; }
th { background: #f1f2f3; color: #24282c; border-top: 1px solid #bbb; }
tr { break-inside: avoid; }
img { display: block; max-width: 100%; height: auto; margin: 26px 0 12px; }
code { font: .86em Consolas, monospace; overflow-wrap: anywhere; }
.footnote { margin-top: 32px; border-top: 1px solid #bbb;
            font: 14px/1.6 Arial, sans-serif; }
.footnote hr { display: none; }
.footnote li { margin-bottom: 15px; overflow-wrap: anywhere; }
.footnote p { margin: 0; }
sup { line-height: 0; }
::selection { background: #d8e6ed; }
@media (max-width: 900px) {
  .layout { display: block; }
  nav { padding: 24px; border-right: 0; border-bottom: 1px solid #ddd; }
  nav .contents { position: static; }
  nav a { display: inline-block; margin: 0 16px 12px 0; }
  nav .source { display: block; }
  main { padding: 30px 24px 60px; font-size: 17px; }
  h1 { font-size: 37px; }
  table { font-size: 12px; }
  th, td { padding: 9px 6px; }
}
@media print {
  @page { size: A4; margin: 17mm 16mm; }
  .layout { display: block; max-width: none; }
  nav { display: none; }
  main { padding: 0; font-size: 10pt; line-height: 1.45; }
  h1 { font-size: 27pt; margin-bottom: 18pt; }
  p { margin-bottom: 10pt; orphans: 3; widows: 3; }
  a[id] + p { font-size: 13pt; margin-top: 19pt; break-after: avoid; }
  a { color: inherit; }
  table { font-size: 8pt; line-height: 1.35; margin: 12pt 0; }
  th, td { padding: 6pt; }
  img { max-height: 100mm; object-fit: contain; }
  .footnote { font-size: 8pt; }
}
"""


def main():
    source = (ROOT / "RESEARCH.md").read_text(encoding="utf-8")
    source = re.sub(r"\A<!--.*?-->\s*", "", source, flags=re.S)
    body = markdown.markdown(source, extensions=["tables", "footnotes", "fenced_code"])
    links = "\n".join(f'<a href="#{key}">{label}</a>' for key, label in SECTIONS)
    html = (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="description" content="Research and original design for a '
        'contemplative CFA world with curiosity, expeditions, and an evolving history.">'
        '<title>The Observatory — CFA design research</title>'
        f'<style>{STYLE}</style></head><body><div class="layout">'
        '<nav aria-label="Document contents"><div class="contents"><strong>Contents</strong>'
        f'{links}<a class="source" href="RESEARCH.md">Read the Markdown source</a>'
        '</div></nav><main>'
        f'{body}</main></div></body></html>\n'
    )
    destination = ROOT / "index.html"
    destination.write_text(html, encoding="utf-8")
    print(f"Rendered {destination.name}; {len(SECTIONS)} navigation links.")


if __name__ == "__main__":
    main()
