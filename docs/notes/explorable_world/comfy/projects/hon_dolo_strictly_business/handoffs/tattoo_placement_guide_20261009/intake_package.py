"""Local, bounded archive verification. No provider code is executed."""
from pathlib import Path
from datetime import datetime, timezone
from io import BytesIO, StringIO
import csv
import hashlib
import importlib.util
import json
import re
import zipfile
from PIL import Image, ImageChops

ROOT = Path('D:/Documents/CFA')
HERE = Path(__file__).resolve().parent
ZIP = ROOT / 'docs/notes/downloads/GROK-HD-TATTOO-GUIDE-v001.zip'
CAT = ROOT / 'docs/notes/explorable_world/comfy/projects/visual_library/catalog.js'
HELPER = HERE.parents[1] / 'grok_return_20261009/intake_return.py'
spec = importlib.util.spec_from_file_location('reviewed_intake_helpers', HELPER)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def rel(path):
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT.resolve()):
        raise ValueError('Path outside CFA')
    return resolved.relative_to(ROOT.resolve()).as_posix()

def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

cat = json.loads(CAT.read_text(encoding='utf-8-sig').split('=',1)[1].strip().rstrip(';'))
by_sha = {}
for asset in cat['assets']:
    path = asset.get('repoPath') or asset.get('path')
    if asset.get('sha256') and path:
        by_sha.setdefault(asset['sha256'], []).append(dict(asset, path=path))
brief = json.loads((HERE/'brief.json').read_text(encoding='utf-8'))
source_checks = []
for source in brief['sources']:
    p = ROOT/source['repoPath']
    actual = sha(p.read_bytes())
    source_checks.append({'assetID': source['assetID'], 'path': source['repoPath'], 'expectedSHA256': source['sha256'], 'actualSHA256': actual, 'matches': actual == source['sha256']})
    if actual != source['sha256']:
        raise ValueError('Brief source hash mismatch: '+source['assetID'])
    by_sha.setdefault(actual, []).append({'id': source['assetID'], 'path': source['repoPath']})

raw_zip = ZIP.read_bytes()
rows, local = [], {}
with zipfile.ZipFile(BytesIO(raw_zip)) as z:
    helpers.safe_members(z.infolist())
    if sum(i.file_size for i in z.infolist()) > 128*1024*1024:
        raise ValueError('Archive expansion exceeds bounded intake')
    bad = z.testzip()
    if bad:
        raise ValueError('CRC failed: '+bad)
    for info in z.infolist():
        if info.is_dir():
            continue
        archive_name = info.filename
        member_name = archive_name.split('/',1)[1]
        data = z.read(info)
        digest = sha(data)
        known = by_sha.get(digest, [])
        reused = next((a for a in known if (ROOT/a['path']).is_file() and sha((ROOT/a['path']).read_bytes()) == digest), None)
        if reused:
            path = ROOT/reused['path']
        else:
            path = HERE/'received'/member_name
            rel(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists() and path.read_bytes() != data:
                raise ValueError('Refusing to overwrite different bytes: '+str(path))
            path.write_bytes(data)
        row = {'archiveMember': archive_name, 'filename': member_name, 'sha256': digest, 'bytes': len(data), 'path': rel(path), 'existingCanonicalAssetID': reused['id'] if reused else None, 'storage': 'reused_exact_bytes' if reused else 'new_canonical_file'}
        if Path(member_name).suffix.lower() in helpers.IMAGE_EXTS:
            row.update(helpers.decode_image(data, member_name))
        rows.append(row)
        local[member_name] = (row, data)

manifest_rows = list(csv.DictReader(StringIO(local['MANIFEST.csv'][1].decode('utf-8-sig'))))
manifest_checks = []
for mr in manifest_rows:
    fn = mr['file']
    if fn.startswith('SOURCE:'):
        expected = mr['source_sha256']
        known = by_sha.get(expected, [])
        confirmed = next((a for a in known if (ROOT/a['path']).is_file() and sha((ROOT/a['path']).read_bytes()) == expected), None)
        manifest_checks.append({'file': fn, 'kind': 'provider_source_claim', 'sha256': expected, 'verifiedLocalAssetID': confirmed['id'] if confirmed else None, 'path': confirmed['path'] if confirmed else None, 'status': 'source_hash_verified' if confirmed else 'source_bytes_not_locally_resolved'})
    else:
        lr = local.get(fn)
        actual = lr[0]['sha256'] if lr else None
        match = actual == mr['output_sha256'] if lr else False
        manifest_checks.append({'file': fn, 'kind': 'provider_output_claim', 'expectedSHA256': mr['output_sha256'], 'actualSHA256': actual, 'matches': match})

crop_checks = []
for mr in manifest_rows:
    if not mr['file'].startswith('clean_art/'):
        continue
    match = re.search(r'box=\((\d+), (\d+), (\d+), (\d+)\)', mr['transformation'])
    bounds = list(map(int, match.groups())) if match else None
    known = by_sha.get(mr['source_sha256'], [])
    source = next((a for a in known if (ROOT/a['path']).is_file() and sha((ROOT/a['path']).read_bytes()) == mr['source_sha256']), None)
    check = {'file': mr['file'], 'sourceSHA256': mr['source_sha256'], 'sourceAssetID': source['id'] if source else None, 'sourcePath': source['path'] if source else None, 'cropBounds': bounds, 'providerTransformation': mr['transformation'], 'pixelEqualityVerified': None, 'status': 'source_bytes_not_locally_resolved'}
    if source and bounds:
        with Image.open(ROOT/source['path']) as src, Image.open(BytesIO(local[mr['file']][1])) as dst:
            expected = src.convert('RGB').crop(tuple(bounds))
            actual = dst.convert('RGB')
            same = expected.size == actual.size and ImageChops.difference(expected, actual).getbbox() is None
            check.update({'pixelEqualityVerified': same, 'status': 'exact_pixel_crop_verified' if same else 'pixel_crop_mismatch'})
    crop_checks.append(check)

index = list(csv.DictReader(StringIO(local['flat_0_INDEX.csv'][1].decode('utf-8-sig'))))
for ir in index:
    fn = ir['original_filename_match']
    if fn.endswith('.jpg') and re.fullmatch('[a-f0-9]{64}\\.jpg', fn):
        known = by_sha.get(fn[:-4], [])
        verified = next((a for a in known if (ROOT/a['path']).is_file() and sha((ROOT/a['path']).read_bytes()) == fn[:-4]), None)
        ir['localSourceAssetID'] = verified['id'] if verified else None
        ir['sourceHashVerified'] = bool(verified)
    else:
        ir['sourceHashVerified'] = False
        ir['localSourceAssetID'] = None
    ir['requestedIndex'] = f"F0-{int(ir['index'])+1:02d}"
    ir['providerIndex'] = ir['index']
    ir['providerCaptionMappingIsUnverified'] = True

receipt = {
 'schema_version': 1, 'intakeID': 'HON-TATTOO-PLACEMENT-GUIDE-20261009-V001',
 'recordedAtUTC': datetime.now(timezone.utc).isoformat(),
 'status': 'received_verified_candidate_not_accepted',
 'archive': {'path': rel(ZIP), 'bytes': len(raw_zip), 'sha256': sha(raw_zip), 'crcPassed': True, 'safeMemberValidationPassed': True, 'retainedUnchanged': True},
 'summary': {'files': len(rows), 'uniqueSHA256': len({r['sha256'] for r in rows}), 'images': sum(r.get('decoded',False) for r in rows), 'newCanonicalFiles': sum(r['storage']=='new_canonical_file' for r in rows), 'reusedCanonicalFiles': sum(r['storage']=='reused_exact_bytes' for r in rows), 'newCanonicalBytes': sum(r['bytes'] for r in rows if r['storage']=='new_canonical_file'), 'exactCropsVerified': sum(c['pixelEqualityVerified'] is True for c in crop_checks), 'unresolvedCropSources': sum(c['pixelEqualityVerified'] is None for c in crop_checks)},
 'briefSourceChecks': source_checks, 'providerManifestChecks': manifest_checks,
 'cropChecks': crop_checks, 'indexChecks': index, 'files': rows,
 'noProviderCodeExecuted': True, 'originalsModified': False, 'artAccepted': False,
 'method': {'helperSource': rel(HELPER), 'functionsReused': ['safe_members','decode_image'], 'lesson': brief['method']['lesson'], 'baseline': brief['method']['baseline'], 'deliberateChange': brief['method']['deliberateChange'], 'cloudRun': False, 'limits': 'Byte/decode verification does not establish placement or character acceptance. Visual review is recorded separately.'}
}
save('intake_receipt.json', receipt)
save('asset_ledger.json', {'schema_version': 1, 'intakeID': receipt['intakeID'], 'assets': rows, 'cropChecks': crop_checks, 'indexChecks': index})
print(json.dumps(receipt['summary'], indent=2))
print('OUTPUT HASH MISMATCHES', [c for c in manifest_checks if c.get('matches') is False])
print('CROP MISMATCHES', [c['file'] for c in crop_checks if c['pixelEqualityVerified'] is False])
