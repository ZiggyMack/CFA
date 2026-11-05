"""Verify source inputs for the requested skeleton UI; no site/writer mutations."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

root = Path(r'D:\Documents\CFA')
projects = root / 'docs/notes/explorable_world/comfy/projects'
writer = projects / 'hon_dolo_strictly_business/story/writer_pass_20261010'
mail = projects / 'collaborators/mailbox/messages/e01c86af-d096-4e81-8b55-22b185055ec7.json'
message = json.loads(mail.read_text(encoding='utf-8-sig'))
attachments = []
for source in message['attachments']:
    path = root / source['path']
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    attachments.append({'path': source['path'], 'sha256': actual_hash, 'bytes': path.stat().st_size,
                        'hashMatches': actual_hash == source['sha256'],
                        'bytesMatch': path.stat().st_size == source['bytes']})
coverage_path = writer / 'HON_COVERAGE_MAP_20261028.json'
coverage = json.loads(coverage_path.read_text(encoding='utf-8-sig'))
packet_path = writer / 'kitchen_block_20261029/S02_PACKET_20261029.md'
packet = packet_path.read_text(encoding='utf-8-sig')
cards = {}
for match in re.finditer(r'^### (S02-\d+) (.+?)\n(.*?)(?=^### S02-|\Z)', packet, re.M | re.S):
    shot_id, title, text = match.groups()
    cards[shot_id] = {
        'title': title,
        'line': packet[:match.start()].count('\n') + 1,
        'creativeSectionHeadings': [n for n in range(8) if re.search(rf'^{n}\. \*\*', text, re.M)],
        'kitchenFieldLabels': [n for n in range(1, 13) if re.search(rf'\*\*11\.{n}(?:\D)', text)],
        'promptStatements': re.findall(r'^(?:7\. |\*\*7b\.).*', text, re.M),
        'warning': 'Field presence is structural evidence only; prompt text can explicitly be not yet.'
    }
report = {
    'checkedAtUTC': datetime.now(timezone.utc).isoformat(),
    'messageID': message['id'], 'attachments': attachments,
    'coverageSource': str(coverage_path.relative_to(root)),
    'coverageSHA256': hashlib.sha256(coverage_path.read_bytes()).hexdigest(),
    'authoredShotCount': len(coverage['shots']),
    'uniqueShotIDCount': len({shot['shotID'] for shot in coverage['shots']}),
    'sectionIDs': [section['id'] for section in coverage['sections']],
    'newPacketCards': cards,
    'sampleInterpretations': {
        'S02-9': 'Camera, lighting, background, beats and cue are written; character direction explicitly none; ship design and start frame absent; resulting prompt explicitly not yet. See packet lines363 onward.',
        'S02-6': 'Still prompt written; video prompt explicitly not yet because timing and the lip-sync lane are unproven; start frame absent. See packet lines242 onward.',
        'S01-1': 'Scoped identity/dental references exist; prepared starting frame absent; still and motion prompts written. Original example must be read with AddendumA.'
    },
    'limits': [
        'Dated map artState is not a search of the entire current media library.',
        'New source documents and structural presence do not grant creative acceptance, technical validation or execution.',
        'The blank demonstration is not an authored shot, asset or production task.',
        'Site implementation/publication is owned by CFA SITE INDEX and is not claimed here.'
    ],
    'siteFilesChanged': False, 'writerFilesChanged': False, 'newGeneration': False
}
output = Path(__file__).with_name('WRITER_INPUT_VERIFICATION.json')
output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'attachmentsVerified': all(a['hashMatches'] and a['bytesMatch'] for a in attachments),
                  'shots': report['authoredShotCount'], 'uniqueIDs': report['uniqueShotIDCount'],
                  'sections': len(report['sectionIDs']), 'newPacketCards': len(cards),
                  'receipt': str(output)}, indent=2))
