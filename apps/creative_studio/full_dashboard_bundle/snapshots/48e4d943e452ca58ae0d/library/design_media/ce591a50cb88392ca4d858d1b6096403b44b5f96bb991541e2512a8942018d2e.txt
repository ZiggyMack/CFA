#!/usr/bin/env python3
"""Build side-by-side compare sheets: REF | GROK BOT | NANO BANANA | CHATGPT.
Usage (from anywhere):  python3 COMPARE/build_compare_sheets.py [--attempt a1|a2|a3|latest]
Needs Pillow (pip install pillow). Output: COMPARE/sheets/<TEST-ID>_compare.jpg and COMPARE/sheets/ALL_compare.jpg
Reads COMPARE/tests.json; looks in RETURNS/A_NANOBANANA and RETURNS/B_CHATGPT for <TEST-ID>_<TOOL>_a<N>.(png|jpg|jpeg|webp)
(falls back to _REFUSAL screenshots). Optionally reads LEDGER.csv to print REFUSED on empty tiles. Nothing here scores or approves anything."""
import os, sys, json, csv
from PIL import Image, ImageDraw, ImageFont
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
att = sys.argv[sys.argv.index("--attempt") + 1] if "--attempt" in sys.argv else "latest"
tests = json.load(open(os.path.join(KIT, "COMPARE", "tests.json")))
EXT = ["png", "jpg", "jpeg", "webp"]
refused = {}
try:
    for r in csv.DictReader(open(os.path.join(KIT, "LEDGER.csv"))):
        if r.get("refused", "").upper() == "Y": refused.setdefault((r["test_id"], r["tool"]), r.get("refusal_text", "")[:80])
except Exception: pass
def find(dirn, tid, tool):
    atts = ["a3", "a2", "a1"] if att == "latest" else [att]
    for suf in ("", "_REFUSAL"):
        for a in atts:
            for e in EXT:
                p = os.path.join(KIT, "RETURNS", dirn, "%s_%s_%s%s.%s" % (tid, tool, a, suf, e))
                if os.path.exists(p): return p, a + suf
    return None, None
try: F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20); FB = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
except Exception: F = FB = ImageFont.load_default()
TW, TH, PAD, HEAD = 640, 360, 10, 70
def tile(path, label, empty):
    t = Image.new("RGB", (TW, TH + 34), (32, 32, 32)); d = ImageDraw.Draw(t)
    if path:
        im = Image.open(path).convert("RGB"); im.thumbnail((TW, TH)); t.paste(im, ((TW - im.width) // 2, 34 + (TH - im.height) // 2))
    else:
        d.text((20, 34 + TH // 2 - 10), empty, fill=(150, 150, 150), font=F)
    d.text((6, 6), label, fill=(255, 200, 90), font=F); return t
os.makedirs(os.path.join(KIT, "COMPARE", "sheets"), exist_ok=True)
rows = []
for t in tests:
    tiles = [tile(os.path.join(KIT, t["uploads"][0]), "REF (image 1)", "missing"),
             tile(os.path.join(KIT, t["baselines"][0]), "GROK BOT baseline", "missing")]
    for dirn, tool, lab, code in (("A_NANOBANANA", "NANOBANANA", "NANO BANANA", "A_NANOBANANA"), ("B_CHATGPT", "CHATGPT", "CHATGPT", "B_CHATGPT")):
        p, a = find(dirn, t["id"], tool)
        empty = ("REFUSED: " + refused[(t["id"], code)]) if (t["id"], code) in refused else "pending - no file"
        tiles.append(tile(p, lab + (" " + a if a else ""), empty))
    W = PAD + 4 * (TW + PAD); H = HEAD + TH + 34 + PAD
    s = Image.new("RGB", (W, H), (18, 18, 18)); d = ImageDraw.Draw(s)
    d.text((PAD, 10), "%s  %s" % (t["id"], t["subject"]), fill=(240, 240, 240), font=FB)
    d.text((PAD, 42), "needs_user_review" + ("  |  " + t["status_flag"] if t["status_flag"] else ""), fill=(255, 120, 120), font=F)
    for i, tl in enumerate(tiles): s.paste(tl, (PAD + i * (TW + PAD), HEAD))
    out = os.path.join(KIT, "COMPARE", "sheets", "%s_compare.jpg" % t["id"]); s.save(out, quality=88); rows.append(s); print(out)
W = max(r.width for r in rows); allim = Image.new("RGB", (W, sum(r.height for r in rows)), (18, 18, 18)); y = 0
for r in rows: allim.paste(r, (0, y)); y += r.height
allim = allim.resize((allim.width // 2, allim.height // 2)); allim.save(os.path.join(KIT, "COMPARE", "sheets", "ALL_compare.jpg"), quality=85)
print("done:", os.path.join(KIT, "COMPARE", "sheets", "ALL_compare.jpg"))
