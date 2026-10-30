"""Synthetic questionnaire evidence; never a real user answer."""
from copy import deepcopy


def records():
    answer = {'choice': 'needs_correction', 'note': 'Fixture only: D:/Documents/CFA/exact-source.png',
              'reference': {'assetID': 'A', 'sha256': 'a' * 64}, 'updatedAt': '2026-10-30T10:00:00.123456Z'}
    direction = {'choice': 'bounded_corrections', 'note': 'Synthetic feedback, never dispatch.'}
    reply = {'id': 'fixture-reply', 'preparedAt': '2026-10-30T10:00:01Z',
             'questionnaireVersion': 'synthetic-persistence-fixture-v1', 'answers': {'fixture-question': answer},
             'direction': direction, 'futureEvidence': {'href': '../original.json', 'sourceURL': 'D:/Documents/CFA/evidence.json'}}
    ready = {'format': 'cfa-collaborator-review-v1', 'taskID': 'grok-proof-package',
             'questionnaireVersion': 'synthetic-persistence-fixture-v1', 'state': 'ready',
             'answers': deepcopy(reply['answers']), 'direction': deepcopy(direction),
             'updatedAt': '2026-10-30T10:00:01Z', 'replies': [deepcopy(reply)], 'readyReplyID': reply['id']}
    unknown = {'format': 'cfa-collaborator-review-v1', 'taskID': 'future-task',
               'questionnaireVersion': 'future-questionnaire-v2', 'state': 'draft', 'answers': {},
               'direction': {'choice': '', 'note': ''}, 'updatedAt': '2026-10-30T10:00:00Z',
               'replies': [], 'readyReplyID': None, 'futureMetadata': {'sourceURL': 'D:/Documents/CFA/future.txt'}}
    return {ready['taskID']: ready, unknown['taskID']: unknown}


def backups():
    return [{'origin': 'synthetic future client', 'reason': 'Unsupported fixture format',
             'data': {'format': 'future-unsupported', 'sourceURL': 'D:/Documents/CFA/unread.json',
                      'href': '../unread.json', 'answers': {'fixture': 'Retain verbatim'}}}]
