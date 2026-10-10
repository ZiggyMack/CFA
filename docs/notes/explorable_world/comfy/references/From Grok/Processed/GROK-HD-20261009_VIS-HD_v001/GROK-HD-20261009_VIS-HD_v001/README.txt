README - GROK-HD-20261009_VIS-HD_v001
Built 2026-10-09 05:35 UTC by Grok Bot.
Everything status=needs_user_review; user_approved=false everywhere. Never write approved.

PURPOSE
  Hon Dolo mouth-lock viseme reference sheet — the standard ~9–12 mouth shapes animators
  cycle for dialogue lip-sync (Preston Blair ~10 shapes, Rhubarb Lip Sync 9, MPEG-4 / Oculus
  viseme sets up to ~15). This package locks Hon Dolo's face while varying only the mouth:
    - two gold upper canine fangs
    - natural white other upper teeth
    - silver lower grill
    - one hoop each nostril
    - two lip rings at bottom-lip corners
  Face lock ref: /workspace/hd-sb/work/lockface_face_neck_crop.png
  Rerolls also used 04 EE as a second reference.

CONTENTS
  01_VISEMES/   12 deliverables VIS-HD-NN_<SHAPE>.jpg (1280x720 JPEG)
  02_REJECTED/  5 rejected attempts (F/V r2 + r1s for S/T/K, CH/SH, GRIN, SHOUT)
  CONTACT.jpg   labelled 4x3 contact sheet (NN SHAPE + short QA tag)
  manifest.json full package manifest
  manifest.csv  flat table (id, shape, phonemes, file, sha256, source_asset_sha, attempt, qa_note, status)
  README.txt    this file

  Contact sheet also copied next to the ZIP as:
    /workspace/hd-sb/return/GROK-HD-20261009_VIS-HD_v001_CONTACT.jpg

VISEMES (01_VISEMES/)
  01 REST    VIS-HD-01_REST.jpg     a1  good
  02 MBP     VIS-HD-02_MBP.jpg      a1  good; only one nostril hoop visible
  03 AH      VIS-HD-03_AH.jpg       a1  good
  04 EE      VIS-HD-04_EE.jpg       a1  good
  05 OH      VIS-HD-05_OH.jpg       a1  lip rings drawn with ball ends
  06 OO-W    VIS-HD-06_OO-W.jpg     a1  good
  07 F-V     VIS-HD-07_F-V.jpg      a1  UNRESOLVED — best-available; lower lip not tucked under upper teeth; ball-end rings
  08 L-TH    VIS-HD-08_L-TH.jpg     a1  ball-end rings
  09 S-T-K   VIS-HD-09_S-T-K.jpg    a2  good (r1 rejected: gold cap on central incisor)
  10 CH-SH   VIS-HD-10_CH-SH.jpg    a2  grill correct; lip funnel weak (r1 rejected: 4 gold upper teeth)
  11 GRIN    VIS-HD-11_GRIN.jpg     a2  good (r1 rejected: gold lower canines)
  12 SHOUT   VIS-HD-12_SHOUT.jpg    a2  good (r1 rejected: tongue out, doubled lip rings, septum-looking nostril rings)

KNOWN DRIFT / QA
  - F/V (07): UNRESOLVED. r1 (9168d102) weak — lower lip not tucked under upper teeth; ball-end rings.
    r2 (1ae4a534) also failed (lips just parted) — in 02_REJECTED. Kept r1 as best-available.
  - Ball-end lip rings (should be plain rings at bottom-lip corners): noted on OH, F/V, L/TH.
  - MBP: only one nostril hoop visible (should be one each nostril).
  - CH/SH: lip funnel weaker than ideal; grill OK.
  - Rejected r1s mostly for teeth lock failures (extra gold teeth / gold lower canines / central gold cap)
    or SHOUT anatomy (tongue out, doubled lip rings, septum-looking rings).

REJECTED (02_REJECTED/)
  VIS-HD-07_F-V_r2_*     1ae4a534  lips just parted; failed F/V shape
  VIS-HD-09_S-T-K_r1_*   6e6e7ecc  gold cap on central incisor
  VIS-HD-10_CH-SH_r1_*   9d21b465  4 gold upper teeth
  VIS-HD-11_GRIN_r1_*    dcaf71bf  gold lower canines
  VIS-HD-12_SHOUT_r1_*   8b5fef5f  tongue out; doubled lip rings; septum-looking nostril rings

HASHES
  All sha256 values in manifest.* are computed from the exact bytes packaged.
  Asset filenames under assets/ are <sha256>.jpg and match file contents.
  Packaged copies are byte-identical to source assets (sha of copy == source asset sha).
