"""Build local catalog records from the verified intake and scoped review."""
from pathlib import Path
from datetime import datetime, timezone
import json

HERE = Path(__file__).resolve().parent
ROOT = Path('D:/Documents/CFA')
receipt = json.loads((HERE/'intake_receipt.json').read_text(encoding='utf-8'))
crops = {c['file']:c for c in receipt['cropChecks']}
def rel(p): return p.relative_to(ROOT).as_posix()
def save(p,v): p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
notes = {
 'HD-TATTOO-PLACEMENT-GUIDE_v001.png': ('Tattoo placement guide v001 · revision needed', 'Verified derived placement proof only. Correct eye/know orientation and mismatch warning. Legacy face includes long fangs/jewelry, so scope remains placement-only. Optional dice is mislabeled center; partial chest extent unverified. Local TG key crosswalk differs from delivered numbering, which was not instructed. Not a current head, dental or complete-look master.'),
 'flat_1_STENCIL-ONLY.png': ('Tattoo art cleanup v001 · mask and placement sketches remain', 'Derived mixed-source sheet. Wolf/character photos removed, but mask tile 44 and body-placement sketches remain; not stencil-only. Hon/Lisan ownership and default/optional/history still need per-tile labels.'),
 'flat_0_LABELED.png': ('Tattoo sheet index v001 · source map incomplete', 'Derived 25-cell mixed-source sheet. Local crosswalk maps delivered 00–24 to F0-01–25; provider numbering was not constrained in the sent message. Labels cover image areas. Seven supplied full filename/hash references verify locally; one full claim and 17 caption-prefix-only rows remain unresolved. Index transcription is not approval.'),
}
crop_titles = {
 'CA01':'eye · character-right cheek crop', 'CA02':'know · character-left cheek crop',
 'CA03':'eye · flat comparison crop', 'CA04':'eye · skin comparison crop',
 'CA05':'know · cursive flat mismatch', 'CA06':'know · serif skin comparison',
 'CA07':'Legacy neck blaster · body crop', 'CA08':'Legacy chest ship · partial body crop',
 'CA09':'Scoundrel · gold N and flourish crop', 'CA10':'Optional dice · low-resolution forehead crop',
 'CA11':'Scoundrel · forearm placement context', 'CA12':'Dice pair · unplaced mixed-sheet crop',
 'CA13':'eye · mixed-sheet artwork crop', 'CA14':'know · mixed-sheet cursive mismatch',
 'CA15':'Chewie lettering · history/unplaced crop', 'CA16':'Bird · optional/unplaced artwork crop'
}
inspected = {'CA01','CA02','CA05','CA07','CA08','CA09','CA10','CA11','CA14'}
assets=[]
for row in receipt['files']:
    if not row.get('decoded'): continue
    fn=row['filename']; crop=crops.get(fn); code=Path(fn).name[:4]
    if fn in notes:
        title,note=notes[fn]; album='hon:tattoo-placement-guide-20261009'; role='Annotated guide/index candidate; requires revision'
    else:
        title=crop_titles[code]
        note='Independently verified exact pixel crop of the recorded source; opaque RGB derived evidence, not an original or transparent stencil. '
        if code in {'CA05','CA14'}: note+='Cursive know conflicts with the selected serif on-body know; retain mismatch evidence only.'
        elif code in {'CA07','CA08'}: note+='Legacy body-detail context only; source face/grill/jewelry and the partial chest extent are not approved.'
        elif code=='CA09': note+='Gold N and underline flourish retained. Exact forearm side/scale and transfer equivalence remain unresolved.'
        elif code=='CA10': note+='Optional forehead dice context only; low resolution, exact placement/art equivalence unverified.'
        elif code=='CA11': note+='Simpler black Scoundrel lettering and wrist context; anatomical arm side/scale unverified.'
        elif code in {'CA12','CA15','CA16'}: note+='Historical/optional mixed-sheet motif remains unplaced; do not add to default character.'
        else: note+='Use only the named lettering/comparison scope, not full-face identity or dental authority.'
        album='hon:tattoo-placement-derived-crops-20261009'; role='Exact derived crop; source-specific detail scope only'
    a={'id':'HD-TATGUIDE-'+row['sha256'][:12], 'project':'hon', 'path':row['path'], 'title':title, 'category':'details', 'album':album, 'sha256':row['sha256'], 'bytes':row['bytes'], 'width':row['width'], 'height':row['height'], 'sourceStatus':'Received and verified · candidate, not accepted', 'note':note, 'referenceRole':role, 'reviewStatus':'needs_revision' if not crop else 'derived_reference_not_new_approval', 'accepted':False, 'wholeCharacterApproved':False, 'artworkLineage':'exact_pixel_crop' if crop else 'annotated_sheet_or_guide_derivative', 'tags':['Hon Dolo','tattoo guide','derived','review candidate'], 'sourceAliases':[row['archiveMember']], 'visualReview':'individually_inspected' if fn in notes or code in inspected else 'decode_and_exact_pixel_crop_verification_only'}
    if crop:
        a.update(sourceAssetIDs=[crop['sourceAssetID']],sourceSHA256=crop['sourceSHA256'],cropBounds=crop['cropBounds'],pixelEqualityVerified=True)
    assets.append(a)
albums=[
 {'id':'hon:tattoo-placement-guide-20261009','project':'hon','category':'details','title':'Tattoo placement guide · first proof','description':'One guide and two derived sheets. Exact files are verified; layout, key mapping and stencil-only cleanup need revision. No new reference acceptance.','related':[]},
 {'id':'hon:tattoo-placement-derived-crops-20261009','project':'hon','category':'details','title':'Tattoo guide · exact derived crops','description':'16 pixel-verified opaque RGB crops. Skin-placement evidence, comparison art, optional motifs and mismatches remain separately scoped; none is a recovered original transparent stencil.','related':[]}
]
documents=[]
for f,t in [('REVIEW.txt','Tattoo placement guide · independent review'),('intake_receipt.json','Tattoo placement guide · verified file/crop receipt'),('asset_ledger.json','Tattoo placement guide · exact media ledger'),('received/README.md','Tattoo placement guide · provider claims'),('received/MANIFEST.csv','Tattoo placement guide · provider manifest'),('received/flat_0_INDEX.csv','Tattoo placement guide · provider index (unverified caption mappings)')]:
    documents.append({'project':'hon','path':rel(HERE/f),'title':t,'album':'Tattoo placement guide · intake and review'})
registry={'schema_version':1,'intakeID':receipt['intakeID'],'status':'received_verified_needs_revision_not_accepted','albums':albums,'assets':assets,'documents':documents}
save(HERE/'registry.json',registry)
ledger=json.loads((HERE/'asset_ledger.json').read_text(encoding='utf-8'))
ids={a['sha256']:a['id'] for a in assets}
for row in ledger['assets']:
    row['catalogAssetID']=ids.get(row['sha256'])
ledger['reviewPath']=rel(HERE/'REVIEW.txt')
ledger['registryPath']=rel(HERE/'registry.json')
save(HERE/'asset_ledger.json',ledger)
receipt.update(status='received_verified_needs_revision_not_accepted',reviewPath=rel(HERE/'REVIEW.txt'),registryPath=rel(HERE/'registry.json'),all16CropsPixelVerified=True,visualReviewScope={'wholeDerivatives':3,'individualCrops':sorted(inspected),'remainingCrops':'Decode/pixel comparison only'},reviewDecision='Request bounded repair of the same one guide and two sheets; no expansion or new acceptance')
receipt['legendCrosswalk']=[{'providerKey':'1','localKey':'TG-01','motif':'eye'},{'providerKey':'2','localKey':'TG-02','motif':'know'},{'providerKey':'3','localKey':None,'motif':'legacy neck blaster'},{'providerKey':'4','localKey':None,'motif':'partial chest ship'},{'providerKey':'5','localKey':'TG-04','motif':'optional dice'},{'providerKey':'6','localKey':'TG-03','motif':'Scoundrel'},{'providerKey':'U1','localKey':'TG-06','motif':'unplaced bird'},{'providerKey':'U2','localKey':'TG-05','motif':'historical Chewie lettering'}]
receipt['deliveryScopeCalibration']='Parent verified CHIEF_MESSAGE_001 did not transmit local TG/F0 numbering or require a blank mannequin; differences are local-schema reconciliation and visual scope risks, not failed delivered numbering requirements.'
save(HERE/'intake_receipt.json',receipt)
# Read the latest brief, preserving the parent's dispatch update.
brief=json.loads((HERE/'brief.json').read_text(encoding='utf-8'))
brief['status']='received_verified_needs_revision_not_accepted'
if 'dispatch' in brief: brief['dispatch']['actualProofValidation']='verified_locally_needs_revision_not_accepted'
brief['receivedIntake']={'receiptPath':rel(HERE/'intake_receipt.json'),'reviewPath':rel(HERE/'REVIEW.txt'),'registryPath':rel(HERE/'registry.json'),'archiveSHA256':receipt['archive']['sha256'],'newApprovals':[],'remoteCorrectionSent':False}
brief['updatedAtUTC']=datetime.now(timezone.utc).isoformat()
save(HERE/'brief.json',brief)
start=HERE/'START_HERE.txt'
old=start.read_text(encoding='utf-8')
prefix='RECEIVED PROOF v001 — INDEPENDENT REVIEW COMPLETE\n22 unique files / 19 images; all output/source hashes and 16 exact crops verified.\nGuide and both sheets need revision; no new approval. See REVIEW.txt,\nintake_receipt.json and registry.json. No correction message sent by this intake.\n\n'
if not old.startswith('RECEIVED PROOF v001'): start.write_text(prefix+old,encoding='utf-8')
print(json.dumps({'guideAssetID':next(a['id'] for a in assets if a['title'].startswith('Tattoo placement guide v001')),'assets':len(assets),'albums':len(albums),'documents':len(documents),'registry':rel(HERE/'registry.json')},indent=2))
