"""Verify exact current or explicitly archived, dated textual evidence."""
import hashlib
import json
from pathlib import Path

def verify_evidence_source(root, source, snapshots=()):
    root = Path(root).resolve()
    def raw_at(pin):
        path = (root / pin['path']).resolve()
        assert path.is_relative_to(root), 'Evidence path leaves repository'
        return path.read_bytes()
    def matches(raw, pin):
        return len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256']
    live = raw_at(source)
    if matches(live, source):
        return 'current'
    key = {k: source[k] for k in ('path', 'bytes', 'sha256')}
    candidates = [row for row in snapshots if row['source'] == key]
    assert len(candidates) == 1, 'Changed evidence needs one registered historical snapshot: ' + source['path']
    row = candidates[0]
    assert row['currentSource']['path'] == source['path'] and matches(live, row['currentSource']), 'Current evidence revision changed'
    archived = raw_at(row['snapshot'])
    assert matches(archived, row['snapshot']) and matches(archived, source), 'Historical evidence bytes changed'
    assert live[:source['bytes']] == archived, 'Historical evidence prefix was not preserved'
    report_raw = raw_at(row['reconciliation'])
    assert matches(report_raw, row['reconciliation']), 'Owner reconciliation record changed'
    report = json.loads(report_raw)
    confirmations = [f for f in report['files'] if f['path'] == source['path']
        and f['beforeBytes'] == source['bytes'] and f['beforeSHA256'] == source['sha256']
        and f['afterBytes'] == row['currentSource']['bytes'] and f['afterSHA256'] == row['currentSource']['sha256']
        and f.get('originalPrefixRetained') is True]
    assert len(confirmations) == 1, 'Owner reconciliation does not establish this exact historical source'
    return 'historical_snapshot'
