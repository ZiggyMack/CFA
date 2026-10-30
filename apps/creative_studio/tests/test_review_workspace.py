"""Pending requests, legacy collections and saved removals stay distinct."""
import ast
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import unittest

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from design_view import build_design_model, model_asset_ids
from library_helpers import effective_design_data, navigation_reference_count, mission_pending_requests, mission_storyboard_requests, mission_tasks


def fixture():
    assets = [dict(id=aid, project='hon', kind='document' if aid.endswith('doc') else 'image',
                   title=aid, filename=aid+'.txt', sha256=aid+'-hash', category='review', album='batch',
                   archived=aid.startswith('archived'))
              for aid in ('pending', 'kept', 'removed', 'removed-doc', 'archived-remove', 'archived', 'legacy')]
    reviews = {'kept': dict(status='keep', note='Keep this choice'),
               'removed': dict(status='remove', note='Remove this version', likenessRating=2),
               'removed-doc': dict(status='remove', note='Superseded document'),
               'archived-remove': dict(status='remove', note='Already archived')}
    data = dict(assets=assets, albums=[dict(id='batch', project='hon', category='review', title='Original batch',
        assetIDs=[a['id'] for a in assets])], reviewRequests=[dict(id=aid, sha256=aid+'-hash', type='missing_decision')
        for aid in ('pending', 'kept', 'removed', 'archived-remove')])
    return data, reviews


class ReviewWorkspaceTest(unittest.TestCase):
    def test_storyboard_lane_counts_only_explicit_current_packages(self):
        source = dict(id='writing', project='hon', provider='Writer', title='Author choices',
            status='needs_input', summary='A written package', nextAction='Review', missing=['Choice']*17,
            userAction=dict(links=[dict(project='hon',view='storyboard',album='structure:hon:story')]))
        data = dict(storyboardStories=[dict(id='hon:story', project='hon')],
            storyboardStructure=dict(stories=[dict(storyID='hon:story', shots=[dict(shotID=str(i)) for i in range(70)])]),
            missionControl=dict(tasks=[source, {**source, 'id':'done', 'status':'done'},
                {**source, 'id':'no-request', 'userAction':{}},
                {**source, 'id':'cross-project', 'userAction':dict(links=[dict(project='lisan',view='storyboard',album='structure:hon:story')])},
                {**source, 'id':'missing-story', 'userAction':dict(links=[dict(project='hon',view='storyboard',album='structure:hon:missing')])}]))
        before = deepcopy(data)
        requests = mission_storyboard_requests(data, mission_tasks(data['missionControl']), 'hon')
        self.assertEqual(requests, [dict(id='writing', title='Author choices', project='hon', storyID='hon:story', structure=True)])
        self.assertEqual(mission_storyboard_requests(data, mission_tasks(data['missionControl']), 'lisan'), [])
        self.assertEqual(data, before)

    def test_archive_separates_nonarchived_removals_without_duplicate_or_state_change(self):
        data, reviews = fixture()
        before = deepcopy((data, reviews))
        model = build_design_model(data, 'hon', 'Archive', reviews)
        removal = model['sections'][0]
        self.assertEqual(removal['kind'], 'disclosure')
        self.assertEqual(removal['assetIDs'], ['removed', 'removed-doc'])
        self.assertEqual(removal['title'], 'Saved removal decisions and archive · 2')
        archived = [aid for section in model['sections'][1:] for aid in model_asset_ids(section)]
        self.assertCountEqual(archived, ['archived-remove', 'archived'])
        self.assertFalse(set(removal['assetIDs']) & set(archived))
        self.assertEqual((data, reviews), before)

    def test_pending_and_collections_views_and_legacy_navigation_preserve_reviews(self):
        data, reviews = fixture()
        effective = effective_design_data(data, reviews)
        pending = mission_pending_requests(effective, reviews, 'hon')
        self.assertEqual(pending, ['pending'])
        self.assertEqual(navigation_reference_count(effective['assets'], pending), 1)
        tree = ast.parse((APP/'app.py').read_text(encoding='utf-8'))
        names = {'init_state', 'navigate', 'render_needs_review', 'render_review_queue'}
        functions = '\n\n'.join(ast.unparse(node) for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names)
        script = f"""
import sys, json
sys.path.insert(0, {str(APP)!r})
import streamlit as st
from library_helpers import ordered_assets, mission_pending_requests
CORNER = 'Corner'
{functions}
init_state()
if 'fixture_reviews' not in st.session_state:
    st.session_state.fixture_reviews = {reviews!r}
st.session_state.studio_reviews = st.session_state.fixture_reviews
st.session_state.seen = {{}}
def render_grid(rows, signature):
    st.session_state.seen[signature] = [asset['id'] for asset, album in rows]
st.button('Old Needs review route', key='legacy', on_click=navigate, args=('Needs review',))
st.button('Review queue', key='queue', on_click=navigate, args=('Review queue',))
render_review_queue({effective!r}, 'hon')
"""
        with tempfile.TemporaryDirectory(prefix='review-workspace-') as temporary:
            source = Path(temporary)/'review_workspace_app.py'
            source.write_text(script, encoding='utf-8')
            app = AppTest.from_file(str(source), default_timeout=60).run()
            self.assertFalse(app.exception)
            self.assertEqual(app.radio(key='review-queue-view').value, 'Awaiting your decision')
            self.assertEqual(app.session_state.seen['review-awaiting:hon:'], ['pending'])
            self.assertEqual(app.session_state.seen['review-saved:hon:'], ['kept'])
            self.assertFalse(any('removal' in item.label.casefold() for item in app.expander))
            app.button(key='legacy').click().run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state.studio_view, 'Review queue')
            self.assertEqual(app.radio(key='review-queue-view').value, 'Review collections')
            self.assertEqual(app.session_state.seen['needs-review:hon:all:'], ['pending', 'kept', 'legacy'])
            self.assertTrue(any('1 collections' in caption.value for caption in app.caption))
            app.button(key='queue').click().run()
            self.assertEqual(app.radio(key='review-queue-view').value, 'Awaiting your decision')
            self.assertEqual(app.session_state.fixture_reviews, reviews)


if __name__ == '__main__': unittest.main()
