"""Append-only take planning. No dispatch, media selection or review writes."""
from copy import deepcopy
from datetime import datetime
from decimal import Decimal
import hashlib
import json
import math
import re

FORMAT = 'cfa-storyboard-takes-v1'
RESET_NOTE = 'Not recorded for this planned take. Earlier evidence remains with its original take.'
UPDATE_NOTE = "Copied direction: update against this take's change note before dispatch."
HANDOFF_NOTE = 'Copied handoff: reconcile inputs, prompts and settings for this planned take.'
REVIEW_NOTE = 'Previous-take assessment does not approve this planned take.'
KEYS = {'id', 'project', 'storyID', 'shotID', 'number', 'parentID', 'state', 'recordedAt', 'changeNote', 'snapshot'}
MAX_INT = 9007199254740991


def _fail(message):
    raise ValueError('Storyboard takes: ' + message)


def _canonical(value):
    """Sorted JSON compatible with browser serialization, including finite floats."""
    if value is None or isinstance(value, bool):
        return json.dumps(value)
    if isinstance(value, str):
        try:
            value.encode('utf-8')
        except UnicodeEncodeError:
            _fail('invalid Unicode string')
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, (int, float)):
        if not math.isfinite(value) or (value == int(value) and abs(value) > MAX_INT):
            _fail('numbers must be finite and safely representable')
        if value == int(value):
            return str(int(value))
        text = repr(value).lower()
        if 'e' in text:
            mantissa, exponent = text.split('e')
            exponent = int(exponent)
            if 1e-6 <= abs(value) < 1e21:
                return format(Decimal(text), 'f')
            return mantissa.removesuffix('.0') + 'e' + ('+' if exponent >= 0 else '-') + str(abs(exponent))
        return text
    if isinstance(value, list):
        return '[' + ','.join(_canonical(item) for item in value) + ']'
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        # Browser keys sort by UTF-16 code units.
        return '{' + ','.join(_canonical(key) + ':' + _canonical(value[key]) for key in sorted(value, key=lambda key: key.encode('utf-16-be'))) + '}'
    _fail('records must contain only plain JSON values')


def _copy(value):
    _canonical(value)
    return deepcopy(value)


def _token(value, name):
    if not isinstance(value, str) or not value.strip() or len(value) > 512:
        _fail(name + ' must be a nonempty identifier')
    return value


def _scope(row):
    return row['project'], row['storyID'], row['shotID']


def empty():
    return {'format': FORMAT, 'takes': []}


def _validate_snapshot(snapshot, shot_id):
    if (not isinstance(snapshot, dict) or set(snapshot) != {'shot', 'foundation'}
            or not isinstance(snapshot['shot'], dict) or snapshot['shot'].get('shotID') != shot_id
            or not isinstance(snapshot['shot'].get('fields'), list)
            or (snapshot['foundation'] is not None and not isinstance(snapshot['foundation'], dict))):
        _fail('invalid snapshot')
    for name in ('fields', 'kitchen'):
        if name == 'kitchen' and name not in snapshot['shot']:
            continue
        fields = snapshot['shot'][name]
        if not isinstance(fields, list):
            _fail('invalid snapshot fields')
        for field in fields:
            if (not isinstance(field, dict) or not isinstance(field.get('key'), str) or not field['key']
                    or not isinstance(field.get('text'), str) or ('evidence' in field and not isinstance(field['evidence'], list))):
                _fail('invalid snapshot field')
    if 'materials' in snapshot['shot'] and (not isinstance(snapshot['shot']['materials'], list) or any(not isinstance(row, dict) for row in snapshot['shot']['materials'])):
        _fail('invalid snapshot materials')
    if snapshot['foundation'] is not None and 'notes' in snapshot['foundation'] and not isinstance(snapshot['foundation']['notes'], list):
        _fail('invalid foundation notes')
    _canonical(snapshot)


def _validate_record(row):
    if not isinstance(row, dict) or set(row) != KEYS:
        _fail('invalid record fields')
    for key in ('id', 'project', 'storyID', 'shotID'):
        _token(row[key], key)
    if row['state'] not in ('written', 'planned'):
        _fail('unsupported take state')
    number = row['number']
    if number is not None and (type(number) is not int or not 1 <= number <= MAX_INT):
        _fail('invalid take number')
    if row['parentID'] is not None:
        _token(row['parentID'], 'parentID')
    if not isinstance(row['changeNote'], str):
        _fail('invalid change note')
    if row['state'] == 'written' and (row['parentID'] is not None or row['recordedAt'] is not None):
        _fail('written source must be a root with unknown recording time')
    if row['state'] == 'planned':
        if number is None or row['parentID'] is None or not row['changeNote'].strip():
            _fail('planned take needs a number, parent and change note')
        stamp = row['recordedAt']
        if not isinstance(stamp, str) or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,6})?(?:Z|[+-]\d\d:\d\d)', stamp):
            _fail('planned take needs an ISO recording time')
        try:
            datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        except ValueError:
            _fail('planned take needs an ISO recording time')
    _validate_snapshot(row['snapshot'], row['shotID'])
    _canonical(row)


def merge(*ledgers):
    rows = {}
    for ledger in ledgers:
        if not isinstance(ledger, dict) or ledger.get('format') != FORMAT or not isinstance(ledger.get('takes'), list):
            _fail('invalid ledger')
        for row in ledger['takes']:
            _validate_record(row)
            if row['id'] in rows and _canonical(rows[row['id']]) != _canonical(row):
                _fail('immutable record conflict: ' + row['id'])
            rows[row['id']] = _copy(row)
    for row in rows.values():
        if row['parentID'] is not None:
            parent = rows.get(row['parentID'])
            if parent is None or _scope(parent) != _scope(row):
                _fail('missing or cross-shot parent: ' + row['id'])
            if row['number'] != (1 if parent['number'] is None else parent['number'] + 1):
                _fail('take number does not follow parent')
        visited = {row['id']}
        parent_id = row['parentID']
        while parent_id is not None:
            if parent_id in visited:
                _fail('cyclic take history')
            visited.add(parent_id)
            parent_id = rows.get(parent_id, {}).get('parentID')
    return {'format': FORMAT, 'takes': [rows[key] for key in sorted(rows)]}


def for_shot(ledger, project, story_id, shot_id):
    return [row for row in merge(ledger)['takes'] if _scope(row) == (project, story_id, shot_id)]


forShot = for_shot


def current(ledger, project, story_id, shot_id):
    rows = for_shot(ledger, project, story_id, shot_id)
    parents = {row['parentID'] for row in rows}
    leaves = [row for row in rows if row['id'] not in parents]
    return leaves[0] if len(leaves) == 1 else None


def _copied_status(field):
    status = field.get('status')
    if status in ('missing', 'unknown', 'not_needed'):
        return status
    return 'draft' if status in ('draft', 'present', 'verified', 'accepted') and field['text'].strip() else 'unknown'


def _planned_snapshot(base, number):
    snapshot = _copy(base)
    shot = snapshot['shot']
    shot.update(stage='preliminary', revision='take ' + str(number),
                authoringStatus='Planned take · direction and handoff need reconciliation',
                kitchenWritten=False, handoffNeedsReconciliation=True, dependencyReviewNeeded=True)
    reset = ('settings', 'results', 'acceptance')
    shot['fields'] = [field for field in shot['fields'] if field['key'] not in reset]
    shot['fields'].extend({'key': key, 'text': '', 'status': 'unknown', 'evidence': [], 'note': RESET_NOTE} for key in reset)
    for field in shot['fields']:
        if field.get('status') in ('accepted', 'verified'):
            field.update(status=_copied_status(field), note=' '.join(filter(None, [field.get('note'), REVIEW_NOTE])))
        if field['key'] in ('prompt_still', 'prompt_clip'):
            field.update(status=_copied_status(field), note=UPDATE_NOTE)
    shot['kitchen'] = [{**field, 'status': _copied_status(field), 'note': HANDOFF_NOTE} for field in shot.get('kitchen', [])]
    if 'materials' in shot:
        shot['materials'] = [row for row in shot['materials'] if row.get('role') != 'result_on_disk']
    if snapshot['foundation'] is not None:
        snapshot['foundation']['dependencyReviewNeeded'] = True
        snapshot['foundation']['notes'] = [*snapshot['foundation'].get('notes', []), HANDOFF_NOTE]
    return snapshot


def plan(ledger, options):
    result = merge(ledger)
    if not isinstance(options, dict):
        _fail('planning options required')
    project = _token(options.get('project'), 'project')
    story_id = _token(options.get('storyID'), 'storyID')
    take_id = _token(options.get('id'), 'id')
    shot = options.get('shot')
    foundation = options.get('foundation')
    if not isinstance(shot, dict) or not isinstance(shot.get('fields'), list):
        _fail('shot fields required')
    shot_id = _token(shot.get('shotID'), 'shotID')
    note = options.get('changeNote')
    note = note.strip() if isinstance(note, str) else ''
    if not note:
        _fail('describe what changes in the next take')
    if any(row['id'] == take_id for row in result['takes']):
        _fail('take ID already exists')
    rows = for_shot(result, project, story_id, shot_id)
    parent = current(result, project, story_id, shot_id)
    if rows and parent is None:
        _fail('conflicting branches must be reconciled before planning')
    if parent is None:
        snapshot = _copy({'shot': shot, 'foundation': foundation})
        _validate_snapshot(snapshot, shot_id)
        match = re.match(r'^take (\d+)', shot.get('revision', ''), re.I)
        identity = {'project': project, 'storyID': story_id, 'shotID': shot_id, 'snapshot': snapshot}
        parent = {'id': 'source:' + hashlib.sha256(_canonical(identity).encode('utf-8')).hexdigest(),
                  'project': project, 'storyID': story_id, 'shotID': shot_id,
                  'number': int(match[1]) if match else None, 'parentID': None, 'state': 'written',
                  'recordedAt': None, 'changeNote': '', 'snapshot': snapshot}
        result['takes'].append(parent)
    number = 1 if parent['number'] is None else parent['number'] + 1
    result['takes'].append({'id': take_id, 'project': project, 'storyID': story_id, 'shotID': shot_id,
                            'number': number, 'parentID': parent['id'], 'state': 'planned',
                            'recordedAt': options.get('recordedAt'), 'changeNote': note,
                            'snapshot': _planned_snapshot(parent['snapshot'], number)})
    return merge(result)
