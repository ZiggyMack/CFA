"""Add the pinned r003 winner originals and evidence without changing r002.

The provider's scoped verdict, reported human choices and site decisions remain
separate. Family links require an exact version hash or the supplied ROOT hash;
filenames alone never create lineage. This module writes no files or reviews.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import os
from pathlib import Path
import re
from urllib.parse import quote, unquote

from cfa_review_metadata_intake import DROP, LIBRARY, IntakeError, SHA, _under, verify_manifest

PACKAGE = 'CFA-SUPP-WINNERS-20261021_r003'
PARENT = 'CFA-SUPP-WINNERS-20261021_r002'
PINS = {
    'SHA256SUMS.txt': '96dcb643803458ed3318b8b596ae60cc022b7d0b1bbeb912ddafc2e67571fc0f',
    'WINNERS_list_r002_carryover.csv': '80d36b230ada1b7f6f496c8921208ef4b10c870ba1418ffbedb18593ac6d639a',
    'WINNERS_lineage.csv': '6b438e55d0c9e4b5c663393d91fa5b667092cad454a4094b36ffb8ee3ab7086f',
    'WINNERS_v_reports.csv': '3de544f6b4793b20a3c7323f51fe2feb357201edefae14723a87d1d1606c226e',
    'WINNERS_index_full.html': 'ca5ab701418ab48d33897f0f95658fa3a4f0714145fe04e31d695d211b09edf7',
    'RECEIPT_WINNERS_r003.txt': '2b78b9120a248e5b3192b338747db09c1d04d33397029e90883703cf86eaff48',
}
ALBUMS = {
    'mouth': ('hon:winners-mouth-v004-20261021', 'working', 'Mouth v004 · preliminary picks'),
    'chest_reference': ('hon:winners-chest-references-20261021', 'working', 'Chest rebuilds · reference candidates'),
    'chest_scene': ('hon:winners-chest-scenes-20261021', 'storyboard', 'Chest rebuilds · scene candidates'),
}


def _digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def _rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def _verified_package(root):
    folder = root / DROP / PACKAGE
    verified = verify_manifest(root, folder, 'SHA256SUMS.txt', PINS['SHA256SUMS.txt'])
    if len(verified) != 319:
        raise IntakeError('Winners r003 requires its 319 pinned manifest entries')
    for name, sha in PINS.items():
        if _digest(folder / name) != sha:
            raise IntakeError('Winners r003 pinned file changed: ' + name)
    parent = root / DROP / PARENT / 'WINNERS_list.csv'
    if (folder / 'WINNERS_list_r002_carryover.csv').read_bytes() != parent.read_bytes():
        raise IntakeError('Winners r003 carryover is not byte-identical to frozen r002')
    return folder, verified


def _classification(row):
    if row['category'].startswith('C.'):
        return 'mouth'
    remote = row['image_box']
    if remote.startswith('/workspace/falcon1000/') or '/hon-dolo-storyboard-' in remote:
        return 'chest_scene'
    return 'chest_reference'


def _hash_matches(text, target, possible):
    """Return only an unambiguous full or short hash explicitly in the report."""
    tokens = set(re.findall(r'(?<![A-Za-z0-9])[a-f0-9]{8,64}(?![A-Za-z0-9])', text))
    matches = [token for token in tokens if target.startswith(token)
               and sum(sha.startswith(token) for sha in possible) == 1]
    return sorted(matches, key=lambda token: (-len(token), token))


def load_winners_media(catalog, repo_root):
    """Return normalized metadata plus ``newAssets``; leave the catalog intact."""
    root = Path(repo_root).resolve()
    folder, verified = _verified_package(root)
    library = root / LIBRARY
    url = lambda path: quote(os.path.relpath(path, library).replace('\\', '/'), safe='/')
    source_path = lambda name: (folder / name).relative_to(root).as_posix()
    winners = _rows(folder / 'WINNERS_list_r002_carryover.csv')
    lineage_rows = _rows(folder / 'WINNERS_lineage.csv')
    report_rows = _rows(folder / 'WINNERS_v_reports.csv')
    if len(winners) != 52 or len({row['sha256'] for row in winners}) != 52:
        raise IntakeError('Expected 52 distinct frozen winner records')
    for row in winners:
        if not SHA.fullmatch(row['sha256']) or row['sha8'] != row['sha256'][:8]:
            raise IntakeError('Malformed winner hash: ' + row['id'])
    winner_names = {row['id']: row for row in winners}
    if len(winner_names) != 52 or len(lineage_rows) != 210 or len(report_rows) != 254:
        raise IntakeError('Unexpected winner/evidence index shape')

    # Rebuilds generate the same IDs; pre-existing exact bytes retain their IDs.
    original_assets = [a for a in catalog['assets'] if a.get('sourceIntake') != PACKAGE]
    assets_by_hash = defaultdict(list)
    for asset in original_assets:
        if SHA.fullmatch(asset.get('sha256', '')):
            assets_by_hash[asset['sha256']].append(asset)
    existing_ids = {a['id']: a for a in catalog['assets']}
    path_cache = {}

    def local_asset(sha):
        if sha not in path_cache:
            found = (None, None)
            for asset in assets_by_hash.get(sha, []):
                if asset.get('repoPath'):
                    path = _under(root, asset['repoPath'])
                elif asset.get('src') and not re.match(r'^[a-zA-Z]+:', asset['src']):
                    path = _under(root, (library / unquote(asset['src'])).resolve().relative_to(root))
                else:
                    continue
                if path.is_file() and _digest(path) == sha:
                    found = (asset, path)
                    break
            path_cache[sha] = found
        return path_cache[sha]

    media = {}
    for relative, sha in verified.items():
        path = root / relative
        if path.parent == folder / 'media':
            if sha in media:
                raise IntakeError('Repeated full image bytes in the bounded media folder')
            media[sha] = path
    expected_media = {r['sha256'] for r in winners if r['category'][0] in 'BC'}
    if set(media) != expected_media or len(media) != 41:
        raise IntakeError('r003 media must match exactly the 28 V passes and 13 preliminary picks')

    family_versions, family_roots = defaultdict(set), defaultdict(set)
    for family in catalog.get('reviewIntake', {}).get('families', []):
        for version in family.get('versions', []):
            if version.get('sha256'):
                family_versions[version['sha256']].add(family['id'])
        if (family.get('original') or {}).get('sha256'):
            family_roots[family['original']['sha256']].add(family['id'])
    lineage = defaultdict(list)
    for row in lineage_rows:
        winner = winner_names.get(row['winner'])
        if (not winner or row['winner_version'] != winner['version']
                or row['winner_sha8'] != winner['sha8'] or not SHA.fullmatch(row['sha256'])):
            raise IntakeError('Lineage row does not identify the exact frozen winning version')
        if row['kind'] not in ('ROOT', 'OTHER VERSION'):
            raise IntakeError('Unknown lineage relationship')
        lineage[row['winner']].append(row)
    reports = defaultdict(list)
    for row in report_rows:
        if row['winner'] not in winner_names:
            raise IntakeError('Report map names an unknown winner')
        path = _under(root, str(folder.relative_to(root)) + '/' + row['v_report_file'])
        if not path.is_relative_to(folder / 'v_reports') or verified.get(path.relative_to(root).as_posix()) != row['sha256']:
            raise IntakeError('Report map path/hash is not in the pinned r003 package')
        reports[row['winner']].append((row, path))

    possible_hashes = set(assets_by_hash) | set(media) | {r['sha256'] for r in winners + lineage_rows}
    new_assets, records, matched_existing = [], [], []
    text_cache = {}
    for row in winners:
        sha = row['sha256']
        group = {'A': 'approved', 'B': 'validated', 'C': 'preliminary'}[row['category'][0]]
        asset, old_path = local_asset(sha)
        full = media.get(sha) or old_path
        if not full and row['d_link']:
            supplied = _under(root, f'{DROP}/{PARENT}/' + row['d_link'])
            if not supplied.is_file() or _digest(supplied) != sha:
                raise IntakeError('Supplied original does not match winner hash: ' + row['id'])
            full = supplied
        thumb = _under(root, str(folder.relative_to(root)) + '/' + row['thumb'])
        thumb_sha = verified.get(thumb.relative_to(root).as_posix())
        if not thumb_sha or thumb_sha == sha:
            raise IntakeError('Thumbnail identity is missing or confused with the full image')
        classification = _classification(row) if sha in media else None
        if sha in media:
            if asset:
                matched_existing.append(asset['id'])
            else:
                asset_id = 'HD-WINNERS-' + sha[:20]
                if asset_id in existing_ids and existing_ids[asset_id].get('sha256') != sha:
                    raise IntakeError('Hash-stable asset ID collides with existing bytes')
                album_id, category, _ = ALBUMS[classification]
                asset = {'id': asset_id, 'project': 'hon', 'kind': 'image',
                         'title': row['id'] + ' · ' + row['version'], 'filename': full.name,
                         'sha256': sha, 'bytes': full.stat().st_size,
                         'repoPath': full.relative_to(root).as_posix(), 'src': url(full), 'thumb': url(thumb),
                         'category': category, 'album': album_id, 'sourceIntake': PACKAGE,
                         'sourceStatus': 'received_candidate',
                         'tags': ['winners supplement', 'mouth shapes' if classification == 'mouth' else 'chest rebuild'],
                         'note': 'Preliminary maker pick; no V-Team validation or human approval is recorded here.' if group == 'preliminary'
                                 else 'Scoped V-Team chest-rebuild evidence. Review this version separately from its original.'}
                new_assets.append(asset)
        roots = [r for r in lineage[row['id']] if r['kind'] == 'ROOT']
        family_links = [{'familyID': fid, 'matchBasis': 'exact_version_hash', 'matchedSHA256': sha}
                        for fid in sorted(family_versions.get(sha, []))]
        for ancestor in roots:
            for fid in sorted(family_roots.get(ancestor['sha256'], [])):
                if not any(link['familyID'] == fid for link in family_links):
                    family_links.append({'familyID': fid, 'matchBasis': 'explicit_lineage_root_hash',
                                         'matchedSHA256': ancestor['sha256'],
                                         'sourceURL': url(folder / 'WINNERS_lineage.csv')})
        version_links, supporting = [], []
        for mapped, path in reports[row['id']]:
            link = {'label': 'V-Team review' if path.suffix == '.tsv' else 'Review evidence',
                    'filename': path.name, 'url': url(path), 'sha256': mapped['sha256'],
                    'repoPath': path.relative_to(root).as_posix(), 'targetSHA256': sha,
                    'matchBasis': 'provider_winner_report_map', 'versionVerified': False}
            if path.suffix in ('.tsv', '.txt', '.md'):
                if path not in text_cache:
                    text_cache[path] = path.read_text(encoding='utf-8-sig')
                text = text_cache[path]
                tokens = _hash_matches(text, sha, possible_hashes)
                if tokens:
                    token = tokens[0]
                    link.update(matchBasis='exact_version_hash' if len(token) == 64 else 'unique_version_hash_prefix',
                                matchedHash=token, versionVerified=True,
                                matchedLines=[{'line': number, 'text': line} for number, line in enumerate(text.splitlines(), 1)
                                              if re.search(r'(?<![A-Za-z0-9])' + re.escape(token) + r'(?![A-Za-z0-9])', line)])
                    version_links.append(link)
                    continue
            supporting.append(link)
        if group == 'validated' and not version_links:
            raise IntakeError('No report explicitly identifies this V-passed version: ' + row['id'])
        if group == 'preliminary' and (version_links or row['v_verdict']):
            raise IntakeError('Preliminary mouth pick unexpectedly carries V validation')
        normalized_lineage = []
        for ancestor in lineage[row['id']]:
            old_asset, old_file = local_asset(ancestor['sha256'])
            old_file = media.get(ancestor['sha256']) or old_file
            normalized_lineage.append({'kind': ancestor['kind'], 'versionID': ancestor['version_id'],
                'sha256': ancestor['sha256'], 'status': ancestor['status'], 'loggedStatus': ancestor['logged_status'],
                'statusBasis': 'provider_inferred' if 'inferred' in ancestor['source'].lower() else 'provider_recorded',
                'sourceEvidence': ancestor['source'], 'exactAssetID': old_asset['id'] if old_asset else None,
                'fullImageURL': url(old_file) if old_file else None,
                'availability': 'local_original_verified' if old_file else 'not_delivered',
                'isImmediateParent': False})
        records.append({'id': PACKAGE + ':' + sha, 'title': row['id'], 'version': row['version'],
            'sha256': sha, 'sha8': row['sha8'], 'project': 'lisan' if row['id'].startswith('Lisan Al Gaib') else 'hon',
            'group': group, 'label': row['label'], 'deliveredInR003': sha in media,
            'exactAssetID': asset['id'] if asset else None, 'classification': classification,
            'fullImageURL': url(full) if full else None, 'repoPath': full.relative_to(root).as_posix() if full else None,
            'availability': 'local_original_verified' if full else 'preview_only',
            'thumbURL': url(thumb), 'thumbnailSHA256': thumb_sha,
            'familyIDs': [link['familyID'] for link in family_links], 'familyLinks': family_links,
            'familyLinkBasis': 'explicit_lineage_root_hash' if any(link['matchBasis'] == 'explicit_lineage_root_hash' for link in family_links)
                               else 'exact_version_hash' if family_links else '',
            'lineage': normalized_lineage, 'lineageURL': url(folder / 'WINNERS_lineage.csv'),
            'lineageNote': 'Root and other versions are provider-recorded relationships; other versions are not asserted to be the direct edit parent.',
            'vVerdict': row['v_verdict'], 'reviewScope': row['scope'], 'advisories': row['advisories'],
            'goldReferences': row['goldrefs'], 'sourceEvidence': row['source'], 'notes': row['note'],
            'reportLinks': version_links, 'supportingEvidence': supporting,
            'sourceReportsStatus': 'full_reports_available' if version_links else 'no_v_validation_recorded',
            'humanAcceptance': None, 'siteValidation': 'not_performed'})
    counts = Counter(r['group'] for r in records)
    missing = [{'title': r['title'], 'sha256': r['sha256'], 'version': r['version']}
               for r in records if not r['fullImageURL']]
    return {'id': PACKAGE, 'schemaVersion': 1, 'sourcePins': dict(PINS),
            'indexURL': url(folder / 'WINNERS_index_full.html'),
            'receiptURL': url(folder / 'RECEIPT_WINNERS_r003.txt'),
            'reportsURL': url(folder / 'WINNERS_v_reports.csv'),
            'lineageURL': url(folder / 'WINNERS_lineage.csv'),
            'carryoverURL': url(folder / 'WINNERS_list_r002_carryover.csv'),
            'summary': {'manifestEntriesVerified': len(verified), 'winnerRecords': len(records),
                        'deliveredFullImages': len(media), 'newAssets': len(new_assets),
                        'matchedExistingAssets': len(matched_existing), 'localOriginals': len(records)-len(missing),
                        'previewOnly': len(missing), 'lineageRows': len(lineage_rows),
                        'versionMatchedReportLinks': sum(len(r['reportLinks']) for r in records), **counts},
            'authorityNote': 'Available files, scoped V-Team evidence and human choices remain distinct. No site approval, score or reference default is changed.',
            'records': records, 'mediaRecords': [r for r in records if r['deliveredInR003']],
            'missingFullOriginals': missing, 'newAssets': new_assets}


def apply_winners_media(catalog, repo_root):
    """Append verified assets/albums and attach additive evidence; return metadata.

    Call before ``apply_winners_supplement`` so that the existing supplement can
    resolve the delivered originals by exact hash. Enrich its rows from this
    result's ``records`` without replacing the frozen reviewIntake families.
    """
    metadata = load_winners_media(catalog, repo_root)
    new_assets = metadata.pop('newAssets')
    existing = {a['id']: a for a in catalog['assets']}
    albums = {a['id']: a for a in catalog.get('albums', [])}
    # Validate collisions before any mutation, including a prior generated album.
    for asset in new_assets:
        if asset['id'] in existing and existing[asset['id']]['sha256'] != asset['sha256']:
            raise IntakeError('Winner asset identity changed')
    for classification in {r['classification'] for r in metadata['mediaRecords']}:
        album_id, category, _ = ALBUMS[classification]
        if album_id in albums and (albums[album_id].get('sourceIntake') != PACKAGE
                                   or albums[album_id].get('category') != category):
            raise IntakeError('Winner album ID collides with an existing collection')
    catalog['assets'].extend(a for a in new_assets if a['id'] not in existing)
    for classification, (album_id, category, title) in ALBUMS.items():
        ids = list(dict.fromkeys(r['exactAssetID'] for r in metadata['mediaRecords'] if r['classification'] == classification))
        if not ids:
            continue
        if album_id not in albums:
            album = {'id': album_id, 'project': 'hon', 'category': category, 'title': title,
                     'sourceIntake': PACKAGE, 'assetIDs': [],
                     'description': 'Returned versions for comparison. Existing decisions and reference defaults stay separate.'}
            catalog.setdefault('albums', []).append(album)
            albums[album_id] = album
        for asset_id in ids:
            if asset_id not in albums[album_id]['assetIDs']:
                albums[album_id]['assetIDs'].append(asset_id)
    catalog['winnersMediaIntake'] = metadata
    return metadata
