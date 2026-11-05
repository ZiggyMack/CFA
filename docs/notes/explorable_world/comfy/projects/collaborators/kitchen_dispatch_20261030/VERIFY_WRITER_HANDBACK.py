"""Verify the addressed writer handback; receipt is acknowledgement only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import uuid

ROOT = Path(r'D:\Documents\CFA')
DESK = ROOT / 'docs/notes/explorable_world/comfy/projects/collaborators'
message = json.loads((DESK / 'mailbox/messages/be9438e8-a9c0-48a4-8bcf-873b11dc1b40.json').read_text(encoding='utf-8-sig'))
assert message['recipient'] == 'nova'
checked = []
for item in message['attachments']:
    path = (ROOT / item['path']).resolve()
    assert path.is_relative_to(ROOT)
    raw = path.read_bytes()
    checked.append({'path': item['path'], 'sha256': hashlib.sha256(raw).hexdigest(),
                    'bytes': len(raw), 'matches': hashlib.sha256(raw).hexdigest() == item['sha256'] and len(raw) == item['bytes']})
now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
report = {'checkedAtUTC': now, 'messageID': message['id'], 'attachments': checked,
          'allMatched': all(item['matches'] for item in checked),
          'scope': 'Receipt and byte verification; proposals await reconciliation against the October 30 author interview.'}
(Path(__file__).parent / 'WRITER_HANDBACK_VERIFICATION.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
assert report['allMatched'], 'Attachment changed; see verification report before acknowledging.'
receipt_id = str(uuid.uuid4())
receipt = {'schemaVersion': 1, 'id': receipt_id, 'messageId': message['id'], 'createdAtUTC': now,
           'actor': 'nova', 'event': 'acknowledged',
           'evidence': 'Read the full addressed handback and verified all five attachment hashes and byte counts on D:. Evidence: collaborators/kitchen_dispatch_20261030/WRITER_HANDBACK_VERIFICATION.json. This acknowledges receipt, not full creative acceptance, site intake, selected starting inputs or dispatch. The October 30 interview supersedes the older pacing target and standalone benchmark proposal; Claude and Site Nova are reconciling current decisions. Beat grids and the still-preparation route remain operator work at the relevant dispatch.',
           'replyMessageId': None, 'replacementMessageId': None}
with (DESK / 'mailbox/receipts' / (receipt_id + '.json')).open('x', encoding='utf-8') as out:
    out.write(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'allMatched': True, 'verifiedAttachments': len(checked), 'receiptID': receipt_id}))
