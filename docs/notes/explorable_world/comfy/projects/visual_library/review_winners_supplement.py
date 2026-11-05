"""Read the separately pinned winners supplement without changing r002 or reviews.

Thumbnails have their own hashes; they never stand in for delivered originals.
Frame-name associations are navigation only, not version lineage or acceptance.
"""
from collections import Counter, defaultdict
import csv
import hashlib
import os
from pathlib import Path
import re
from urllib.parse import quote, unquote

from cfa_review_metadata_intake import DROP, LIBRARY, IntakeError, _under, verify_manifest

PACKAGE = 'CFA-SUPP-WINNERS-20261021_r002'
PINS = {
    'WINNERS_index.html': 'e697dbd96c43660f1b03a08db28da04677fd05e8070b2c99ef4a93961ee5fd6e',
    'WINNERS_list.csv': '80d36b230ada1b7f6f496c8921208ef4b10c870ba1418ffbedb18593ac6d639a',
    'RECEIPT_WINNERS_r002.txt': 'e815a2e9b62b92f2648c93294412ea73ef3263e4f45f714725c32ee88362efab',
    'THUMBS_SHA256SUMS.txt': '6df2a2484c2377eb2f623bec68f790794fc9f1fd83281fce7ee070fa5f794415',
}
# These evidence files already exist locally. Do not link a same-name revision
# unless its cited digest matches. The remaining reports are not yet delivered.
LOCAL_EVIDENCE = {
    'cd202e09': 'HD-CHAIN_winners_v002/NOTES.md',
    '156489f3': 'GROK-HD-SB-GRILLUP-v001/NOTES_FOR_NOVA_AND_CODEX.md',
    '85dc35f0': 'LAG-GOLDCAND_drop01_worms_v001/ZIGGY_DECISION_build_20261021_v001.md',
    'db98b366': 'LAG-GOLDCAND_drop01_worms_v001/ZIGGY_DECISION_worm_style_20261021_v002.md',
}


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load_winners_supplement(catalog, repo_root):
    root = Path(repo_root).resolve()
    folder, library = root / DROP / PACKAGE, root / LIBRARY
    for filename, expected in PINS.items():
        if digest(folder / filename) != expected:
            raise IntakeError('Winners supplement changed: ' + filename)
    verified = verify_manifest(root, folder, 'THUMBS_SHA256SUMS.txt', PINS['THUMBS_SHA256SUMS.txt'])
    with (folder / 'WINNERS_list.csv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 52 and len({r['sha256'] for r in rows}) == 52
    assert len(verified) == 52
    url = lambda p: quote(os.path.relpath(p, library).replace('\\', '/'), safe='/')
    assets = defaultdict(list)
    for asset in catalog['assets']:
        if re.fullmatch('[0-9a-f]{64}', asset.get('sha256', '')):
            assets[asset['sha256']].append(asset)
    families = catalog.get('reviewIntake', {}).get('families', [])
    family_ids = {f['id'] for f in families}
    exact_versions = defaultdict(list)
    for family in families:
        for version in family['versions']:
            if version.get('sha256'):
                exact_versions[version['sha256']].append(family['id'])
    local_cache = {}

    def local_asset(sha):
        if sha in local_cache:
            return local_cache[sha]
        for asset in assets.get(sha, []):
            if asset.get('repoPath'):
                path = _under(root, asset['repoPath'])
            elif asset.get('src') and not re.match(r'^[a-zA-Z]+:', asset['src']):
                path = _under(root, (library / unquote(asset['src'])).resolve().relative_to(root))
            else:
                continue
            if path.is_file() and digest(path) == sha:
                local_cache[sha] = (asset, path)
                return asset, path
        local_cache[sha] = (None, None)
        return None, None

    items = []
    for row in rows:
        sha = row['sha256']
        assert re.fullmatch('[0-9a-f]{64}', sha) and row['sha8'] == sha[:8]
        thumb = _under(root, str(folder.relative_to(root)) + '/' + row['thumb'])
        thumbnail_sha = verified[thumb.relative_to(root).as_posix()]
        assert thumbnail_sha != sha, 'Preview must not impersonate the original bytes'
        asset, asset_path = local_asset(sha)
        full = asset_path
        if row['d_link']:
            supplied = _under(root, str(folder.relative_to(root)) + '/' + row['d_link'])
            if not supplied.is_file() or digest(supplied) != sha:
                raise IntakeError('Winner original mismatch: ' + row['id'])
            full = full or supplied
        related = sorted(set(exact_versions.get(sha, [])))
        basis = 'exact_version_hash' if related else ''
        if not related and row['image_box'].startswith('/workspace/falcon1000/'):
            # The provider's exact frame name supplies a related-family link,
            # not a same-image join, promotion, or inferred parent relation.
            frame = re.sub(r'-v\d+[a-z]*$', '', Path(row['image_box']).stem)
            candidate = 'GROK-HD-FALCON-1000:' + frame
            if candidate in family_ids:
                related, basis = [candidate], 'provider_frame_name_only'
        group = {'A': 'approved', 'B': 'validated', 'C': 'preliminary'}[row['category'][0]]
        evidence_links = []
        for prefix, relative in LOCAL_EVIDENCE.items():
            if prefix in row['source']:
                path = root / DROP / relative
                evidence_sha = digest(path)
                if evidence_sha.startswith(prefix):
                    evidence_links.append({'label': path.name, 'url': url(path), 'sha256': evidence_sha,
                                           'matchBasis': 'cited_hash_prefix'})
        items.append({
            'id': PACKAGE + ':' + sha, 'title': row['id'], 'version': row['version'],
            'project': 'lisan' if row['id'].startswith('Lisan Al Gaib') else 'hon',
            'label': row['label'], 'group': group, 'sha256': sha, 'sha8': sha[:8],
            'thumbURL': url(thumb), 'thumbnailSHA256': thumbnail_sha,
            'fullImageURL': url(full) if full else None,
            'availability': 'local_original_verified' if full else 'preview_only',
            'exactAssetID': asset['id'] if asset else None,
            'familyIDs': related, 'familyLinkBasis': basis,
            'sourceEvidence': row['source'], 'sourceLinks': evidence_links,
            'notes': row['note'], 'remoteImagePath': row['image_box'],
            'vVerdict': row['v_verdict'], 'reviewScope': row['scope'],
            'goldReferences': row['goldrefs'], 'advisories': row['advisories'],
            'sourceReportsStatus': 'partly_available' if evidence_links else 'not_delivered',
        })
    # Gold-reference assignments remain the provider's named/inferred claims.
    # Resolve a short hash only when it has a unique full-hash match locally.
    item_by_sha = {i['sha256']: i for i in items}
    possible = set(assets) | set(item_by_sha)
    for item in items:
        links = []
        for clause in item['goldReferences'].split(' ; '):
            for prefix in dict.fromkeys(re.findall(r'\b[0-9a-f]{8}\b', clause)):
                matches = [sha for sha in possible if sha.startswith(prefix)]
                if len(matches) != 1:
                    continue
                sha = matches[0]
                target = item_by_sha.get(sha)
                _, path = local_asset(sha)
                if not target and not path:
                    continue
                available = bool(path or target and target['fullImageURL'])
                links.append({'label': clause, 'sha256': sha,
                              'url': url(path) if path else target['fullImageURL'] or target['thumbURL'],
                              'availability': 'local_original_verified' if available else 'preview_only',
                              'matchBasis': 'unique_hash_prefix_from_provider'})
        item['referenceLinks'] = links
    delivery = catalog.get('winnersMediaIntake')
    if delivery:
        delivered = {record['sha256']: record for record in delivery['records']}
        decisions = {record['id']: record for record in catalog.get('reviewDecisions', [])}
        for item in items:
            record = delivered.get(item['sha256'])
            if not record:
                raise IntakeError('Winner missing from verified media intake: ' + item['title'])
            for key in ('fullImageURL', 'exactAssetID', 'availability', 'familyIDs',
                        'familyLinkBasis', 'familyLinks', 'lineage', 'lineageURL',
                        'lineageNote', 'reportLinks', 'supportingEvidence'):
                item[key] = record[key]
            if record['deliveredInR003']:
                item['sourceReportsStatus'] = record['sourceReportsStatus']
            item['sourceLinks'].extend(record['reportLinks'])
            decision = decisions.get(item['exactAssetID'], {})
            acceptance = decision.get('acceptedScope')
            item['humanAcceptance'] = acceptance if acceptance and acceptance.get('sha256') == item['sha256'] else None
    counts = Counter(i['group'] for i in items)
    local = sum(bool(i['fullImageURL']) for i in items)
    result = {
        'id': PACKAGE, 'title': 'Winners supplement', 'revision': 'r002',
        'sourceURL': url(folder / 'WINNERS_index.html'), 'indexURL': url(folder / 'WINNERS_index.html'),
        'csvURL': url(folder / 'WINNERS_list.csv'), 'receiptURL': url(folder / 'RECEIPT_WINNERS_r002.txt'),
        'goldReferenceStatus': 'provider_links_with_inferences',
        'summary': {'items': len(items), 'localOriginals': local, 'previewOnly': len(items)-local,
                    'exactAssetMatches': sum(bool(i['exactAssetID']) for i in items),
                    'relatedFamilies': sum(bool(i['familyIDs']) for i in items), **counts},
        'sourcePins': PINS, 'items': items,
        'authorityNote': 'Separate provider supplement. Recorded user choices, scoped V verdicts and preliminary picks stay distinct. No site review state is written.',
    }
    if delivery:
        result.update(indexURL=delivery['indexURL'], csvURL=delivery['carryoverURL'],
                      receiptURL=delivery['receiptURL'], mediaRevision=delivery['id'],
                      mediaDelivery={'fullImages': delivery['summary']['deliveredFullImages'],
                                     'versionMatchedReports': delivery['summary']['versionMatchedReportLinks'],
                                     'lineageRows': delivery['summary']['lineageRows']})
    return result


def apply_winners_supplement(catalog, repo_root):
    supplement = load_winners_supplement(catalog, repo_root)
    others = [s for s in catalog.get('reviewSupplements', [])
              if not s['id'].startswith('CFA-SUPP-WINNERS-20261021_')]
    catalog['reviewSupplements'] = others + [supplement]
    return supplement
