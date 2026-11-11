COMPARE_TEMPLATE - one page, four columns: REF (upload image 1) | GROK BOT baseline | NANO BANANA | CHATGPT

Option 1 (no install): open COMPARE/COMPARE.html in Chrome or Firefox (double-click, from inside the unzipped kit).
  It auto-loads RETURNS/A_NANOBANANA/<TEST-ID>_NANOBANANA_a<N>.png and RETURNS/B_CHATGPT/<TEST-ID>_CHATGPT_a<N>.png
  (also .jpg/.jpeg/.webp). 'latest' shows the highest attempt found; pick a1/a2/a3 to see a specific attempt.
  Empty tile = pending. A _REFUSAL screenshot is shown if that's all there is. Click to zoom.
Option 2 (shareable JPGs): python3 COMPARE/build_compare_sheets.py [--attempt latest|a1|a2|a3]
  -> COMPARE/sheets/<TEST-ID>_compare.jpg + ALL_compare.jpg. Reads LEDGER.csv to print REFUSED + the first 80 chars of the refusal text on empty tiles.
Files must follow the naming in PLAN.md section 6 or they won't show up. Nothing here scores or approves; everything is needs_user_review.
