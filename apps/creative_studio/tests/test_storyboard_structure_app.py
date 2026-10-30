"""Exercise both structure views without modifying a saved review."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP))
from library_helpers import effective_reviews, review_payload, review_provenance
import storyboard_takes

class StructureAppTest(unittest.TestCase):
    def test_story_without_sequence_never_displays_unbound_work(self):
        data = dict(assets=[], storyboardStructure=dict(fields=[], kitchenFields=[], stories=[]),
                    shotMaterials=dict(shots=[dict(id=f'work-{number}', project='lisan',
                        title=f'Unbound work {number}', fields=[], materials=[]) for number in range(7)]))
        script = f"""
import sys
sys.path.insert(0, {str(APP)!r})
from story_view import render_structure
render_structure({data!r}, {{'id':'lisan:meta-mirror','project':'lisan','kind':'song'}},
                 'lisan', lambda *args: None, reviews={{}})
"""
        with tempfile.TemporaryDirectory(prefix='story-unbound-') as temporary:
            source = Path(temporary)/'unbound_story_app.py'
            source.write_text(script, encoding='utf-8')
            app = AppTest.from_file(str(source), default_timeout=60).run()
            self.assertFalse(app.exception)
            self.assertTrue(any('0 planned shots' in caption.value for caption in app.caption))
            self.assertFalse(any('Unbound work' in expander.label for expander in app.expander))
            self.assertTrue(any('No canonical shot structure' in info.value for info in app.info))

    def test_structure_and_empty_template_preserve_reviews(self):
        app=AppTest.from_file(str(APP/'app.py'),default_timeout=60).run()
        self.assertFalse(app.exception)
        before=deepcopy(app.session_state['studio_reviews'])
        app.button(key='nav:Storyboard').click().run()
        app.radio(key='story-view:hon').set_value('Structure & gaps').run()
        self.assertFalse(app.exception)
        self.assertTrue(any('70 planned shots' in c.value and '14 sequences' in c.value for c in app.caption))
        self.assertTrue(any('No starting frame selected: 70' in c.value for c in app.caption))
        app.selectbox(key='structure-foundation:hon').select('detailed').run()
        self.assertFalse(any(e.label.startswith('P-') for e in app.expander))
        app.selectbox(key='structure-foundation:hon').select('no_frame').run()
        app.selectbox(key='structure-sequence:hon').select('S02').run()
        self.assertTrue(any(e.label.startswith('S02-9 ·') for e in app.expander))
        app.selectbox(key='structure-focus:hon').select('Camera missing / not assessed').run()
        self.assertFalse(app.exception)
        self.assertFalse(any(e.label.startswith('S02-9 ·') for e in app.expander))
        app.radio(key='structure-mode:hon').set_value('Blank storyboard / shot template').run()
        self.assertFalse(app.exception)
        self.assertEqual(sum('Empty template' in e.label for e in app.expander),28)
        self.assertTrue(any(h.value == 'Kitchen / handoff structure' for h in app.subheader))
        self.assertFalse(any(e.label == 'Context & references · A–D' for e in app.expander))
        self.assertFalse(any(s.key == 'structure-foundation:hon' for s in app.selectbox))
        self.assertFalse(any(s.key == 'structure-status:hon' for s in app.selectbox))
        self.assertFalse(any(e.label.startswith('S02-') for e in app.expander))
        self.assertEqual(app.session_state['studio_reviews'],before)

    def test_foundation_filter_uses_current_reviews_without_promoting_storyboard(self):
        asset = dict(id='scene-frame', project='hon', kind='image', title='Exact scene frame',
                     sha256='a'*64, bytes=100, storyboardStage='preliminary', workingReferenceScope='scene')
        component = dict(id='mouth', project='hon', kind='image', title='Mouth component',
                         sha256='b'*64, bytes=50, storyboardStage='production', workingReferenceScope='detail')
        def shot(sid, materials):
            return dict(shotID=sid, sectionID='S01', title=sid, stage='preliminary', revision='take 1',
                        authoringStatus='Writer draft', fields=[], kitchen=[], materials=materials,
                        kitchenWritten=False, source={}, revisions=[])
        data = dict(assets=[asset, component], storyboardStructure=dict(fields=[], kitchenFields=[], stories=[dict(
            storyID='hon:fixture', sections=[dict(id='S01', title='Opening', shotIDs=['selected','linked-only'])],
            shots=[shot('selected', []), shot('linked-only', [dict(assetID='mouth',role='named_reference')])])]),
            storyboardSourceFoundation=dict(bindings=[dict(project='hon', storyID='hon:fixture', shotID='selected',
                mode='first_frame', evidence=dict(source='Explicit fixture selection',recordedAtUTC='2026-10-29T00:00:00Z'),
                inputs=[dict(assetID='scene-frame',sha256='a'*64,bytes=100,role='start_frame',required=True)])]))
        reviews = effective_reviews(data['assets'], [dict(id='scene-frame',sha256='a'*64,
            storyboardStage='production',workingReferenceScope='scene',status='keep',
            note='Missing nose jewelry remains recorded.')], {})
        self.assertNotIn('sha256', reviews['scene-frame'])
        script = f"""
import sys
sys.path.insert(0, {str(APP)!r})
import streamlit as st
from story_view import render_structure
if 'fixture_data' not in st.session_state: st.session_state.fixture_data = {data!r}
if 'fixture_reviews' not in st.session_state: st.session_state.fixture_reviews = {reviews!r}
render_structure(st.session_state.fixture_data, {{'id':'hon:fixture'}}, 'hon', lambda *args: None,
                 reviews=st.session_state.fixture_reviews)
"""
        app = AppTest.from_string(script,default_timeout=60).run()
        self.assertFalse(app.exception)
        self.assertTrue(any('Detailed foundation: 1' in c.value and 'No starting frame selected: 1' in c.value for c in app.caption))
        self.assertTrue(any('Source stage: Production' in c.value and 'Scope: scene' in c.value for c in app.caption))
        self.assertTrue(any('Storyboard maturity: Preliminary' == c.value for c in app.caption))
        self.assertTrue(any('Missing nose jewelry' in m.value for m in app.markdown))
        self.assertTrue(any('Explicit fixture selection' in t.value for t in app.text))
        self.assertTrue(any('Selected SHA-256: '+('a'*64) in t.value for t in app.text))
        app.selectbox(key='structure-foundation:hon').select('detailed').run()
        self.assertTrue(any(e.label.startswith('selected ·') for e in app.expander))
        self.assertFalse(any(e.label.startswith('linked-only ·') for e in app.expander))
        app.selectbox(key='structure-foundation:hon').select('no_frame').run()
        self.assertFalse(any(e.label.startswith('selected ·') for e in app.expander))
        self.assertTrue(any(e.label.startswith('linked-only ·') for e in app.expander))
        self.assertEqual(app.session_state.fixture_data, data)
        self.assertEqual(app.session_state.fixture_reviews, reviews)
        app.session_state.fixture_reviews['scene-frame']['storyboardStage']='preliminary'
        app.selectbox(key='structure-foundation:hon').select('preliminary').run()
        self.assertFalse(app.exception)
        self.assertTrue(any('Source stage: Preliminary' in c.value for c in app.caption))
        self.assertTrue(any(e.label.startswith('selected ·') for e in app.expander))
        self.assertEqual(app.session_state.fixture_data, data)

    def test_field_status_matches_any_main_field_and_scopes_counts(self):
        keys = ['purpose', 'context', 'lineage', 'references', 'start_frame', 'lighting', 'camera', 'character',
                'background', 'beats', 'cue', 'prompt_still', 'prompt_clip', 'settings', 'results', 'acceptance']
        sections = ['A', 'B', 'C', 'D', *map(str, range(12))]
        definitions = [dict(key=key, section=section, label=key, hint='Fixture field')
                       for key, section in zip(keys, sections)]
        def shot(sid, overrides=None, sequence='S01'):
            values = [dict(key=key, status=(overrides or {}).get(key, 'present'), text=key) for key in keys]
            return dict(shotID=sid, sectionID=sequence, title=sid, stage='preliminary', revision='take 1',
                        authoringStatus='Writer draft', fields=values, kitchen=[dict(key='delivery', status='missing')],
                        materials=[], kitchenWritten=False, source={}, revisions=[])
        shots = [shot('missing', dict(camera='unknown', prompt_clip='missing', cue='missing')),
                 shot('draft', dict(prompt_clip='draft')), shot('kitchen-only'),
                 shot('verified', dict(purpose='verified')), shot('accepted', dict(acceptance='accepted')),
                 shot('unknown', dict(camera='unknown', prompt_clip='unsupported')),
                 shot('not-needed', dict(prompt_clip='not_needed')), shot('selected', dict(start_frame='draft')),
                 shot('other-sequence', dict(prompt_clip='draft'), 'S02')]
        # Absent main fields are also not assessed. Extra fields never enter the main-field filter.
        shots[5]['fields'] = [value for value in shots[5]['fields'] if value['key'] != 'cue']
        shots[5]['fields'][0]['text'] = ''
        shots[2]['fields'].append(dict(key='non-main-field', status='missing'))
        provenance = dict(assetID='coverage-map', line=12, sha256='c'*64)
        shots[0].update(coverageUpdate='The earlier hold is superseded; the named scene remains a proposal.',
                        coverageAsOf='2026-10-28', coverageEvidence=provenance, parent=provenance,
                        priorDependencyEvidence=[dict(provenance, line=4)],
                        revisions=[dict(id='take-2', note='Revision proposal remains pending.', source=provenance)])
        asset = dict(id='frame', project='hon', kind='image', title='Frame', sha256='a'*64, bytes=100,
                     storyboardStage='detailed_design', workingReferenceScope='scene')
        document = dict(id='coverage-map', project='hon', kind='document', title='Coverage map', filename='coverage.md')
        data = dict(assets=[asset, document], storyboardStructure=dict(fields=definitions,
            kitchenFields=[dict(key='delivery', section='1', label='Delivery', hint='Fixture kitchen')], stories=[dict(
                storyID='hon:fixture', source=provenance, sections=[dict(id=section, title=section,
                    shotIDs=[s['shotID'] for s in shots if s['sectionID'] == section]) for section in ['S01', 'S02']],
                shots=shots)]), storyboardSourceFoundation=dict(bindings=[dict(project='hon', storyID='hon:fixture',
                    shotID='selected', mode='first_frame', inputs=[dict(assetID='frame', sha256='a'*64,
                    bytes=100, role='start_frame', required=True)])]))
        reviews = dict(frame=dict(status='keep', note='Keep existing review unchanged.'))
        script = f"""
import sys
sys.path.insert(0, {str(APP)!r})
import streamlit as st
from story_view import render_structure
if 'fixture_data' not in st.session_state: st.session_state.fixture_data = {data!r}
if 'fixture_reviews' not in st.session_state: st.session_state.fixture_reviews = {reviews!r}
render_structure(st.session_state.fixture_data, {{'id':'hon:fixture'}}, 'hon', lambda *args: None,
                 reviews=st.session_state.fixture_reviews)
"""
        app = AppTest.from_string(script, default_timeout=60).run()
        self.assertFalse(app.exception)
        self.assertTrue(any(h.value == 'Story plan & coverage' for h in app.subheader))
        self.assertTrue(any('Written coverage does not mean every shot has an image' in c.value for c in app.caption))
        self.assertTrue(any('Coverage notes · 2026-10-28' in m.value for m in app.markdown))
        self.assertTrue(any(t.value == shots[0]['coverageUpdate'] for t in app.text))
        self.assertTrue(any(c.value == 'Planning context · no field-specific material recorded' for c in app.caption))
        self.assertIsNotNone(app.button(key='structure-map:hon:hon:fixture:source:0'))
        self.assertIsNotNone(app.button(key='structure-coverage:hon:missing:source:0'))
        group_labels = ['Context & references · A–D', 'Creative direction · 0–7', 'Generation handoff · 8–9',
                        'Takes, results & review · 10–11', 'Kitchen / handoff structure · 0/1 sections written']
        groups = [e for e in app.expander if e.label in group_labels]
        self.assertEqual([e.label for e in groups], group_labels * 8)
        self.assertFalse(any(e.proto.expanded for e in groups))
        self.assertFalse(any(e.label == 'Prior takes, revisions & dependency evidence' for e in app.expander))
        first_groups = groups[:5]
        for group, expected_keys in zip([first_groups[0], first_groups[1], first_groups[2], first_groups[3]],
                                       [keys[:4], keys[4:12], keys[12:14], keys[14:]]):
            self.assertEqual([e.label.split(' · ', 1)[1].split(' — ', 1)[0]
                              for e in group.expander if ' — ' in e.label], expected_keys)
        self.assertEqual(len(first_groups[3].button), 4)
        self.assertTrue(any(m.value == 'Revision proposal remains pending.' for m in first_groups[3].markdown))
        self.assertTrue(first_groups[3].warning)
        expected = dict(missing=['missing'], draft=['draft', 'selected'], present=[s['shotID'] for s in shots[:8]],
                        verified=['verified'], accepted=['accepted'], unknown=['missing', 'unknown'], not_needed=['not-needed'])
        def shown():
            return [s['shotID'] for s in shots if any(e.label.startswith(s['shotID']+' · ') for e in app.expander)]
        self.assertIn('Missing · 1', app.selectbox(key='structure-status:hon').options)
        self.assertIn('Draft · 2', app.selectbox(key='structure-status:hon').options)
        for status, ids in expected.items():
            app.selectbox(key='structure-status:hon').select(status).run()
            self.assertFalse(app.exception)
            self.assertEqual(shown(), ids)
            if status == 'draft':
                self.assertEqual([e.proto.expanded for e in app.expander if e.label == 'Context & references · A–D'],
                                 [False, False])
                self.assertEqual([e.proto.expanded for e in app.expander if e.label == 'Creative direction · 0–7'],
                                 [False, True])
                self.assertEqual([e.proto.expanded for e in app.expander if e.label == 'Generation handoff · 8–9'],
                                 [True, False])
            if status == 'verified':
                self.assertTrue(next(e for e in app.expander if e.label == 'Context & references · A–D').proto.expanded)
            if status == 'accepted':
                self.assertTrue(next(e for e in app.expander if e.label == 'Takes, results & review · 10–11').proto.expanded)
        app.selectbox(key='structure-status:hon').select('all').run()
        self.assertEqual(shown(), [s['shotID'] for s in shots[:8]])
        app.selectbox(key='structure-foundation:hon').select('no_frame').run()
        self.assertIn('All field statuses · 7', app.selectbox(key='structure-status:hon').options)
        self.assertIn('Draft · 1', app.selectbox(key='structure-status:hon').options)
        app.selectbox(key='structure-status:hon').select('draft').run()
        self.assertEqual(shown(), ['draft'])
        app.selectbox(key='structure-focus:hon').select('Camera missing / not assessed').run()
        self.assertIn('Draft · 0', app.selectbox(key='structure-status:hon').options)
        self.assertIn('Not assessed · 2', app.selectbox(key='structure-status:hon').options)
        self.assertEqual(shown(), [])
        app.selectbox(key='structure-status:hon').select('all').run()
        self.assertEqual(shown(), ['missing', 'unknown'])
        app.selectbox(key='structure-focus:hon').select('All planned shots').run()
        app.selectbox(key='structure-sequence:hon').select('S02').run()
        self.assertIn('All field statuses · 1', app.selectbox(key='structure-status:hon').options)
        self.assertIn('Missing · 0', app.selectbox(key='structure-status:hon').options)
        self.assertEqual(shown(), ['other-sequence'])
        self.assertEqual(app.session_state.fixture_data, data)
        self.assertEqual(app.session_state.fixture_reviews, reviews)

    def test_explicit_next_take_preserves_history_and_blocks_conflicting_branches(self):
        definitions = [dict(key=key, section=section, label=key, hint='Fixture field') for key, section in
                       [('purpose','A'), ('camera','2'), ('prompt_clip','8'), ('settings','9'), ('results','10'), ('acceptance','11')]]
        shot = dict(shotID='S01-1', sectionID='S01', title='Original scene', stage='production', revision='take 1',
                    authoringStatus='Written source', kitchenWritten=True, source={}, materials=[], revisions=[],
                    fields=[dict(key=d['key'], text='Original '+d['key'], status='accepted', evidence=[]) for d in definitions],
                    kitchen=[dict(key='delivery', text='Original handoff', status='accepted', evidence=[]),
                             dict(key='k1', text='None intentionally needed', status='not_needed'),
                             dict(key='k2', text='Placeholder only', status='unknown'),
                             dict(key='k3', text='Not supplied', status='missing'),
                             dict(key='k4', text='  ', status='draft')],
                    coverageUpdate='Dated coverage context', sourceShotPlanIDs=['legacy-source'])
        data = dict(assets=[], storyboardStructure=dict(fields=definitions,
            kitchenFields=[dict(key=key, section=str(index+1), label=key, hint='Fixture kitchen')
                           for index, key in enumerate(['delivery', *['k'+str(i) for i in range(1,12)]])],
            stories=[dict(storyID='hon:fixture', sections=[dict(id='S01', title='Opening', shotIDs=['S01-1'],
                spineBeat='Shared sequence purpose')], shots=[shot])]))
        reviews = {'untouched': {'status': 'keep', 'note': 'Earlier review'}}
        script = f"""
import sys
sys.path.insert(0, {str(APP)!r})
import streamlit as st
from story_view import render_structure
from library_helpers import review_payload
if 'fixture_data' not in st.session_state: st.session_state.fixture_data = {data!r}
if 'fixture_reviews' not in st.session_state: st.session_state.fixture_reviews = {reviews!r}
render_structure(st.session_state.fixture_data, {{'id':'hon:fixture'}}, 'hon', lambda *args: None,
                 reviews=st.session_state.fixture_reviews)
st.session_state.fixture_export = review_payload([], {{}}, set(), provenance=st.session_state.get('studio_review_provenance', {{}}))
"""
        app = AppTest.from_string(script, default_timeout=60).run()
        self.assertFalse(app.exception)
        self.assertTrue(any('Take 1 · written plan' in e.label for e in app.expander))
        self.assertTrue(app.button(key='take-plan:hon:hon:fixture:S01-1').disabled)
        self.assertEqual(app.session_state.fixture_export['storyboardTakes'], storyboard_takes.empty())
        self.assertTrue(any(e.label == 'Kitchen / handoff structure · 2/12 sections written' for e in app.expander))
        linked = next(e for e in app.expander if e.label == 'Linked references')
        self.assertFalse(linked.proto.expanded)
        self.assertTrue(any(t.value == 'Dated coverage context' for t in linked.text))
        context = next(e for e in app.expander if e.label == 'Context & references · A–D')
        self.assertTrue(any(t.value == 'Shared sequence purpose' for t in context.text))
        app.text_area(key='take-change:hon:hon:fixture:S01-1').input('Move the camera closer; retain the story beat.').run()
        app.button(key='take-plan:hon:hon:fixture:S01-1').click().run()
        self.assertFalse(app.exception)
        ledger = app.session_state.fixture_export['storyboardTakes']
        self.assertEqual(len(ledger['takes']), 2)
        current = storyboard_takes.current(ledger, 'hon', 'hon:fixture', 'S01-1')
        original = next(row for row in ledger['takes'] if row['state'] == 'written')
        self.assertEqual(original['snapshot']['shot'], shot)
        self.assertEqual(current['number'], 2)
        self.assertEqual(current['state'], 'planned')
        self.assertEqual(current['snapshot']['shot']['stage'], 'preliminary')
        self.assertTrue(any('Take 2 · planned' in e.label for e in app.expander))
        self.assertTrue(any(e.label == 'Kitchen / handoff structure · 2/12 sections written' for e in app.expander))
        self.assertFalse(any('The live source foundation differs' in m.value for m in app.markdown))
        self.assertEqual({v['key']:v['status'] for v in current['snapshot']['shot']['fields'] if v['key'] in ('results','acceptance')},
                         dict(results='unknown', acceptance='unknown'))
        self.assertEqual(app.text_area(key='take-change:hon:hon:fixture:S01-1').value, '')
        self.assertEqual(app.session_state.fixture_reviews, reviews)
        self.assertEqual(app.session_state.fixture_data, data)
        self.assertEqual(review_provenance(app.session_state.fixture_export)['storyboardTakes'], ledger)
        # A later source catalog edit cannot overwrite the saved current plan.
        app.session_state.fixture_data['storyboardStructure']['stories'][0]['shots'][0]['title'] = 'Changed live source'
        app.run()
        self.assertFalse(app.exception)
        self.assertTrue(any(e.label.startswith('S01-1 · Original scene · Take 2') for e in app.expander))
        self.assertTrue(any('Source writing changed after this take was saved' in info.value for info in app.info))
        self.assertEqual(app.session_state.fixture_export['storyboardTakes'], ledger)
        # A second device can create a branch; both survive, neither becomes current.
        other = storyboard_takes.plan(storyboard_takes.empty(), dict(project='hon', storyID='hon:fixture', shot=shot,
            foundation=original['snapshot']['foundation'], changeNote='Alternate camera direction', id='other-device-take',
            recordedAt='2026-10-29T13:00:00Z'))
        union = storyboard_takes.merge(ledger, other)
        app.session_state.studio_review_provenance = review_provenance({'storyboardTakes': union})
        app.run()
        self.assertFalse(app.exception)
        self.assertIsNone(storyboard_takes.current(union, 'hon', 'hon:fixture', 'S01-1'))
        self.assertTrue(app.button(key='take-plan:hon:hon:fixture:S01-1').disabled)
        self.assertTrue(any('More than one take branch' in w.value for w in app.warning))
        self.assertEqual(app.session_state.fixture_export['storyboardTakes'], union)
        self.assertEqual(app.session_state.fixture_reviews, reviews)
        app.session_state.fixture_data['storyboardStructure']['stories'][0]['shots'][0]['kitchen'] = []
        app.run()
        self.assertFalse(app.exception)
        self.assertTrue(any(e.label == 'Kitchen / handoff structure · 0/12 sections written' for e in app.expander))

    def test_review_take_union_is_atomic_and_source_failures_keep_backups(self):
        shot = dict(shotID='S01-1', revision='take 1', fields=[], kitchen=[])
        first = storyboard_takes.plan(storyboard_takes.empty(), dict(project='hon', storyID='fixture', shot=shot,
            foundation=None, changeNote='Camera change', id='take-two', recordedAt='2026-10-29T12:00:00Z'))
        second = storyboard_takes.plan(first, dict(project='hon', storyID='fixture', shot=shot,
            foundation=None, changeNote='Lighting change', id='take-three', recordedAt='2026-10-29T13:00:00Z'))
        old_backup = dict(origin='Older import', reason='Unsupported record', data={'raw':'preserve'})
        provenance = review_provenance({'storyboardTakes': first, 'storyboardTakeBackups': [old_backup]})
        before = deepcopy(provenance)
        merged = review_provenance({'storyboardTakes': second}, provenance)
        self.assertEqual(len(merged['storyboardTakes']['takes']), 3)
        self.assertEqual(merged['storyboardTakeBackups'], [old_backup])
        self.assertEqual(review_provenance({'storyboardTakes': first}, merged), merged)
        exported = review_payload([], {}, set(), provenance=merged)
        self.assertEqual(exported['storyboardTakes'], second)
        conflict = deepcopy(first)
        next(t for t in conflict['takes'] if t['id']=='take-two')['changeNote'] = 'Overwrite immutable history'
        with self.assertRaisesRegex(ValueError, 'immutable record conflict'):
            review_provenance({'storyboardTakes': conflict}, provenance)
        self.assertEqual(provenance, before)
        unknown = {'format':'future-format','takes':['unread']}
        safe = review_provenance({'storyboardTakes': unknown}, provenance, strict_takes=False)
        self.assertEqual(safe['storyboardTakes'], first)
        self.assertEqual(safe['storyboardTakeBackups'][1]['data'], unknown)
        self.assertEqual(review_provenance({}, safe)['storyboardTakeBackups'], safe['storyboardTakeBackups'])

if __name__=='__main__': unittest.main()
