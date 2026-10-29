"""Exercise both structure views without modifying a saved review."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP))
from library_helpers import effective_reviews

class StructureAppTest(unittest.TestCase):
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
        self.assertFalse(any(s.key == 'structure-foundation:hon' for s in app.selectbox))
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

if __name__=='__main__': unittest.main()
