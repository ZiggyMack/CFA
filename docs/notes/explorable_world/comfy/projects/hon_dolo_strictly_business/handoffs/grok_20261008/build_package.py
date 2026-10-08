"""Rebuild the integrated Grok handoff from exact sources; never edit or generate media.

Default: ZIP, manifest and receipt beside this script.
--output PATH: isolated output directory inside the repo.
--check-existing [PATH]: verify all current member bytes without writing anything.
ZIP timestamps are fixed; old container metadata may differ while members match.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file() and (p / 'apps').is_dir())
PROJECTS = HERE.parents[2]
HON = HERE.parents[1]
PACKAGE = 'GROK-HD-20261008'
ARMOR_SHA = '19593c0144edd9ed86c21fe74fc66ee475e62c9a7a7c22bfd5efba58afc331ab'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    # Preserve finalized manifest CRLF bytes across Windows and other hosts.
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').replace('\n', '\r\n').encode('utf-8')


def collect():
    sources, entries = {}, {}

    def add(name, source):
        path, source = PurePosixPath(name), source.resolve()
        if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name or not source.is_relative_to(ROOT):
            raise ValueError('Package path is out of bounds: ' + name)
        if name in entries or 'superseded' in name:
            raise ValueError('Repeated or superseded package destination: ' + name)
        sources[name], entries[name] = source, source.read_bytes()

    for name in ['START_HERE.txt', 'requests.json', 'asset_map.json', 'panel_plan.txt',
                 'return_manifest.template.json', 'GROK_DESIGN_INSTRUCTIONS.txt', 'boss_discovery_20261008.txt']:
        add(name, HERE / name)
    for name in ['review_sweep_20261008.json', 'review_sweep_20261008.txt',
                 'grok_favorite_prop_sweep_20261008.json', 'grok_favorite_prop_sweep_20261008.txt',
                 'boss_discovery_20261008.json']:
        add('review_context/' + name, HON / 'feedback' / name)
    add('review_context/detail_profiles.json', PROJECTS / 'collaborators/detail_profiles.json')
    audit_hashes = {}
    for name in ['tattoo_audit_20261008.json', 'tattoo_audit_20261008.txt']:
        add('audit/' + name, PROJECTS / 'visual_library' / name)
        audit_hashes[name] = sha(entries['audit/' + name])
    json.loads(entries['audit/tattoo_audit_20261008.json'])

    request = json.loads(entries['requests.json'])
    boss = next(item for item in request['items'] if item['request_id'] == 'SC-BOSS-001')
    if request['generation_boundary']['initial_max_new_stills'] != 7 or boss['max_initial_images'] != 0 or boss['status'] != 'hold_until_boss_discovery_selection':
        raise ValueError('Generation boundary or boss hold changed; review package scope before rebuilding')
    images = [a for a in json.loads(entries['asset_map.json'])['assets'] if a.get('include_in_package')]
    if len(images) != 13:
        raise ValueError('Expected exactly 13 mapped input images')
    for asset in images:
        name = asset['bundle_path']
        if not name.startswith('references/'):
            raise ValueError('Input image must be in references/: ' + name)
        add(name, ROOT / asset['source_repo_path'])
        data = entries[name]
        if sha(data) != asset['sha256'] or len(data) != asset['bytes'] or sha(data) == ARMOR_SHA:
            raise ValueError('Changed source or excluded Multiverse armor: ' + asset['source_asset_id'])

    records = [{'path': n, 'source_repo_path': sources[n].relative_to(ROOT).as_posix(),
                'sha256': sha(data), 'bytes': len(data),
                'role': 'input_image' if n.startswith('references/') else 'instructions_or_audit'}
               for n, data in entries.items()]
    contents = {
        'schema_version': 1, 'package_id': PACKAGE, 'updated': '2026-10-08', 'state': 'prepared_not_sent',
        'image_count': 13, 'document_count_excluding_this_manifest': len(entries) - 13, 'files': records,
        'scope': {
            'initial_main_stills': 7, 'boss_meeting': 'held_until_discovery_winner_selected',
            'boss_discovery': 'Use separate GROK-BOSS-DISCOVERY-20261008.zip; only one of its three reference images is in this correction package.',
            'creative_rule': 'Invented new-character tattoos require same-delivery four-option standalone art; 10-12 only on explicit further exploration. Prime preservation tasks retain their current details.',
            'audit_limit': 'Wider audit metadata does not mean all audited images are attached. Request exact referenced files needed for unresolved regions. No Multiverse armor image is in this Prime package.',
            'new_generations': 0, 'originals_modified': False},
        'audit_source_hashes': audit_hashes}
    entries['PACKAGE_CONTENTS.json'] = json_bytes(contents)
    return entries, contents


def verify(path, entries):
    expected = {PACKAGE + '/' + name: data for name, data in entries.items()}
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None or len(archive.namelist()) != len(expected) or set(archive.namelist()) != set(expected):
            raise ValueError('ZIP integrity or member-set mismatch')
        for name, data in expected.items():
            if archive.read(name) != data:
                raise ValueError('ZIP member differs from current exact source: ' + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument('--output', type=Path, default=HERE / (PACKAGE + '.zip'))
    actions.add_argument('--check-existing', nargs='?', const=HERE / (PACKAGE + '.zip'), type=Path)
    args = parser.parse_args()
    entries, contents = collect()
    if args.check_existing is not None:
        verify(args.check_existing, entries)
        print(json.dumps({'checked': str(args.check_existing), 'members': len(entries), 'all_member_bytes_match': True, 'writes': 0}))
        return
    target = args.output.resolve()
    if not target.is_relative_to(ROOT) or target.suffix.lower() != '.zip':
        raise ValueError('Output must be a .zip inside this repository')
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix('.rebuild.zip')
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in entries.items():
            info = zipfile.ZipInfo(PACKAGE + '/' + name, date_time=(2026, 10, 8, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    verify(temporary, entries)
    temporary.replace(target)
    receipt = {'package_id': PACKAGE, 'zip_path': target.relative_to(ROOT).as_posix(),
               'sha256': sha(target.read_bytes()), 'bytes': target.stat().st_size, 'entries': len(entries),
               'image_count': 13, 'all_member_hashes_match': True, 'multiverse_armor_present': False,
               'main_still_limit': 7, 'boss_interaction_on_hold': True,
               'audit_source_hashes': contents['audit_source_hashes'], 'state': 'prepared_not_sent'}
    (target.parent / 'PACKAGE_CONTENTS.json').write_bytes(entries['PACKAGE_CONTENTS.json'])
    (target.parent / 'package_build_receipt.json').write_bytes(json_bytes(receipt))
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
