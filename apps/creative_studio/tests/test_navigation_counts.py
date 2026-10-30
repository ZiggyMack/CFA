"""Navigation counts describe media, documents and authored shots separately."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from library_helpers import navigation_reference_count, navigation_storyboard_shot_count


class NavigationCountsTest(unittest.TestCase):
    def test_storyboard_counts_authored_parent_shots_not_images_or_takes(self):
        main = dict(id='main', project='hon', kind='song')
        data = dict(storyboardStories=[main, deepcopy(main),
            dict(id='grill', project='hon', kind='sequence', sequenceID='grill-sequence'),
            dict(id='other-story', project='hon', kind='sequence', sequenceID='other-sequence'),
            dict(id='empty', project='hon', kind='sequence', sequenceID='empty-sequence'),
            dict(id='seed', project='hon', kind='prose'), dict(id='wrong-project', project='lisan')],
            storyboardStructure=dict(stories=[dict(storyID='main', project='hon', shots=[
                dict(shotID='A'), dict(shotID='A'), dict(shotID='A1B'),
                dict(shotID='child', parentShotID='A'), dict(shotID='child2', parent_shot_id='A'),
                dict(shotID='child3', parent=dict(shotID='A')), dict(shotID='orphan', parentShotID='missing'),
                dict(shotID='ordinary', parentID='A')])]),
            storyboardSequences=[dict(id='grill-sequence', project='hon'),
                dict(id='other-sequence', project='hon', shots=[dict(shotID='A')]),
                dict(id='empty-sequence', project='hon', shots=[])],
            shotMaterials=dict(shots=[dict(shotID='Q', project='hon', independentSequenceID='grill-sequence'),
                dict(shotID='Q', project='hon', independentSequenceID='grill-sequence'),
                dict(shotID='not-an-authored-shot', project='hon'),
                dict(shotID='no-empty-fallback', project='hon', independentSequenceID='empty-sequence'),
                dict(shotID='cross-project', project='lisan', independentSequenceID='grill-sequence')]),
            storyboardTakes=dict(takes=[dict(storyID='main', shotID='A', number=number) for number in range(8)]),
            assets=[dict(id=str(number), kind='image') for number in range(100)])
        before = deepcopy(data)
        self.assertEqual(navigation_storyboard_shot_count(data, 'hon'), 6)
        self.assertEqual(navigation_storyboard_shot_count(data, 'lisan'), 0)
        self.assertEqual(data, before)

    def test_navigation_counts_separate_documents_and_preserve_selections(self):
        assets = [dict(id='image',kind='image'), dict(id='video',kind='video'),
                  dict(id='note',kind='document'), dict(id='pdf',kind='pdf')]
        selected = {'image','note','pdf','not-in-current-catalog'}
        before = deepcopy((assets,selected))
        self.assertEqual(navigation_reference_count(assets), 2)
        self.assertEqual(navigation_reference_count(assets, documents=True), 2)
        self.assertEqual(navigation_reference_count(assets, selected), 1)
        self.assertEqual(navigation_reference_count(assets, selected, documents=True), 2)
        self.assertEqual((assets,selected), before)

    def test_native_sidebar_keeps_documents_selected_without_counting_them_as_media(self):
        app = AppTest.from_file(str(APP/'app.py'), default_timeout=60).run()
        self.assertFalse(app.exception)
        assets = app.session_state.studio_export_assets
        image = next(a for a in assets if a.get('kind')=='image')
        document = next(a for a in assets if a.get('kind') in {'document','pdf'})
        app.session_state.studio_basket = {image['id'], document['id']}
        app.run()
        self.assertFalse(app.exception)
        self.assertEqual(app.button(key='nav:Export basket').label, 'Export basket · 1')
        self.assertEqual(app.session_state.studio_basket, {image['id'], document['id']})
        count = navigation_reference_count([a for a in assets if a.get('project')==app.session_state.studio_project], documents=True)
        self.assertEqual(app.button(key='nav:Documents').label, 'Documents · '+str(count))
        catalog = json.loads((APP/'library/design_catalog.json').read_text(encoding='utf-8'))
        shots = navigation_storyboard_shot_count(catalog, app.session_state.studio_project)
        self.assertEqual(app.button(key='nav:Storyboard').label, f'Storyboard · {shots}')

    def test_writings_heading_counts_documents_and_keeps_every_document(self):
        docs = [dict(id='note', project='hon', kind='document', title='Written scene', filename='scene.md'),
                dict(id='pdf', project='hon', kind='pdf', title='Coverage map', filename='coverage.pdf')]
        data = dict(assets=docs, albums=[], storyboardStories=[dict(id='story',project='hon',title='A small story',
                    kind='prose',documentIDs=['note','pdf'])])
        script = f"""
import sys
sys.path.insert(0, {str(APP)!r})
import streamlit as st
from pathlib import Path
from story_view import render_stories
st.session_state.seen_documents = []
render_stories({data!r}, 'hon', Path({str(APP)!r}), lambda *args: None, lambda *args: None,
               lambda asset, **kwargs: st.session_state.seen_documents.append(asset['id']), reviews={{}})
"""
        with tempfile.TemporaryDirectory(prefix='navigation-counts-') as temporary:
            source = Path(temporary)/'story_writings_app.py'
            source.write_text(script, encoding='utf-8')
            app = AppTest.from_file(str(source), default_timeout=60).run()
            self.assertFalse(app.exception)
            self.assertTrue(any(h.value=='Series and seeds · 1 writing collections' for h in app.subheader))
            self.assertTrue(any(h.value=='Writings · A small story · 2 documents' for h in app.subheader))
            self.assertEqual(app.session_state.seen_documents, ['note','pdf'])


if __name__ == '__main__': unittest.main()
