GROK 500 INTAKE — RECEIVED AND INTEGRITY-VERIFIED

CURRENT FOLLOW-UP: verified ZIP cleanup is complete. All 58 downloaded
ZIP copies were removed after verification; all 555 extracted originals
remain verified. The eight outer ZIPs were discovered and checked later.
See receipt_summary.txt and intake_status.json for both cleanup receipts
and the preserved earlier phase history. No creative approval was added.

Completed 2026-10-09T02:16:53.192404+00:00 (October 8, 2026 local time).
Start with receipt_summary.txt for measured delivery and caveats.
asset_ledger.json maps all 500 sources, 50 contact sheets and the index to
portable repository-relative paths, exact provider CSV fields and SHA-256.
No new design or production approval is created by receiving this pack.

CURRENT DELIVERY
The user supplied eight already-unpacked outer folders plus a loose guide:
docs/notes/explorable_world/comfy/references/From Grok/
  LAG-500-MASTER-part01/ through LAG-500-MASTER-part08/
  NOVA-GUIDE-500.md
These contain all 50 per-look ZIPs. Part01 also contains the exact CSV, raw
QA, guide and contact index. Outer ZIP bytes were not received, so their
CRC is unavailable. All 50 nested ZIPs passed CRC verification.

RECEIVED COPY
received/content/LAG-500-MASTER-part##/<look>.zip.contents/<look>/
  preserves the exact source JPEG and contact-sheet filenames.
received/content/LAG-500-MASTER-part01/ retains the CSV, QA, guide and index.
received/guides/NOVA-GUIDE-500.md retains the identical loose guide.
received/intake_receipt.json is the complete integrity and source-chain record.

The result contains 500 unique source JPEGs (250 V reference views and
250 S story scenes), 50 contact sheets, one index and four document copies.
All 555 saved files match the receipt; all 551 images decoded.
received/ is intentionally ignored bulk storage. The portable ledger, status
and summary stay outside it so the map can be versioned without the masters.

IDS AND REVIEW
Source IDs are LAG500-L##-V# or LAG500-L##-S#; contacts use
LAG500-L##-CONTACT; the index uses LAG500-CONTACT-INDEX.
Grok's QA, hero and requested-feature fields are provider data. They are
separate from user triage, favorites, approved references and production stage.
The status file preserves the earlier pending observation in prior_observations.

ACTUAL FOLDER INTAKE TOOL
Requires Python 3.10+ and Pillow. From this directory, the initial read-only
inspection command is:
  python intake_grok500_folders.py --input-dir "../../../references/From Grok"
This relative input resolves from this intake directory. An absolute D: path
is also supported.
The actual completed run used an absolute input path with:
  python intake_grok500_folders.py --input-dir <From Grok directory> --extract --resume-verified
Do not rerun extraction over the completed received/ receipt. Resume was
needed only for six verified partial files after the first long-path failure.
The wrapper rejects unexpected partials and hash/size/decode mismatches.
It uses long-path-capable Windows I/O; original member names remain intact.
The longest current saved path is 274 characters.

The folder wrapper does not delete anything. ZIP cleanup is a separate
root-coordinated operation after the verified receipt and completeness review.
At this receipt snapshot all original nested ZIP inputs remain unchanged.

ORIGINAL ZIP-INPUT TOOL (RETAINED FOR FUTURE DELIVERIES)
intake_grok500.py expects eight actual independent ZIP files named
LAG-500-MASTER-part01.zip through part08.zip plus a loose NOVA-GUIDE-500.md.
That input layout was not what the user supplied in this delivery.
Its incoming/ directory remains available for a future complete ZIP-based
intake in a new output root. Do not apply that cleanup branch to this
folder-based receipt or treat the absent outer ZIP bytes as verified.

VALIDATION
The original ZIP-input tool's 15 synthetic tests were recorded during setup.
The folder intake's 15 safety tests passed in 66.017s before the completed
production extraction, including long paths, changed partials and safe resume.
Actual integrity evidence is received/intake_receipt.json, not the test count.
