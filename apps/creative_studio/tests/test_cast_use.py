"""Exact-version cast choices, character counts and portable review controls."""
import ast
from copy import deepcopy
from pathlib import Path
import json
import sys
import unittest

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from design_view import build_design_model, cast_browse_groups
from library_helpers import cast_story_targets, cast_use_state, effective_reviews, normalize_decision, read_review, review_payload


def fixture():
    assets = [dict(id=aid, project='hon', kind='image', title=aid, filename=aid+'.jpg', sha256=letter*64, category='cast')
              for aid, letter in [('boss','a'), ('wife','b'), ('wife-v2','c')]]
    assets[0].update(roleDecision='user_assigned', characterRole='Boss')
    return dict(assets=assets, albums=[], castCollections=[
        dict(id='boss-group', project='hon', title='Boss', role='Boss', coverID='boss', currentIDs=['boss'], assetIDs=['boss']),
        dict(id='wife-group', project='hon', title='Wife', role="Dolo's wife", coverID='wife', currentIDs=['wife'],
             assetIDs=['wife','wife-v2'], sceneAssetIDs=['wife-v2'])],
        storyboardStories=[dict(id='hon:story', project='hon', title='Hon story'),
                           dict(id='hon:sequence', project='hon', title='Separate sequence', sequenceID='sequence'),
                           dict(id='hon:no-sequence', project='hon', title='Writing only'),
                           dict(id='lisan:story', project='lisan', title='Other project')],
        storyboardStructure=dict(stories=[dict(storyID='hon:story', shots=[dict(shotID='S01-1', title='Arrival')]),
                                         dict(storyID='lisan:story', shots=[dict(shotID='L01-1', title='Elsewhere')])]),
        storyboardSequences=[dict(id='sequence', project='hon', shots=[dict(id='sequence-shot', title='Separate shot')])],
        shotMaterials=dict(shots=[dict(id='source-plan', project='hon', characterCollectionID='boss-group', panelAssetIDs=[])]))


class CastUseTest(unittest.TestCase):
    def test_defaults_union_manual_links_and_roundtrip(self):
        data = fixture()
        before = deepcopy(data)
        boss, wife, alternate = data['assets']
        boss_use = cast_use_state(data, boss, {})['value']
        self.assertTrue(boss_use['roleSelected'])
        self.assertEqual(boss_use['role'], 'Boss')
        boss_use['storyboardPlanned'] = True
        wife_use = cast_use_state(data, alternate, {})['value']
        wife_use.update(storyboardPlanned=True, roleSelected=True)
        reviews = {'boss': dict(castUse=boss_use, status='keep', note='Keep prior note', likenessRating=4),
                   'wife-v2': dict(castUse=wife_use)}
        groups = build_design_model(data, 'hon', 'cast', reviews)['sections'][0]['groups']
        self.assertEqual(len(cast_browse_groups(groups, connection='planned')), 2)
        self.assertEqual(len(cast_browse_groups(groups, connection='roles')), 2)
        # Two selected versions of one character count once, including non-cover versions.
        reviews['wife'] = {'castUse': deepcopy(wife_use)}
        groups = build_design_model(data, 'hon', 'cast', reviews)['sections'][0]['groups']
        self.assertEqual(len(cast_browse_groups(groups, connection='planned')), 2)
        reviews['boss']['castUse'].update(storyboardPlanned=False, roleSelected=False)
        groups = build_design_model(data, 'hon', 'cast', reviews)['sections'][0]['groups']
        boss_facts = next(g for g in groups if g['id']=='boss-group')['browseFacts']
        self.assertEqual([row['id'] for row in boss_facts['planned']], ['source-plan'])
        self.assertFalse(boss_facts['roles'])
        self.assertEqual(boss['roleDecision'], 'user_assigned')
        links = [dict(storyID='hon:story', shotID='S01-1'), dict(storyID='lisan:story', shotID='L01-1'),
                 dict(storyID='hon:story', shotID='gone')]
        reviews['wife-v2']['castUse'].update(storyboardPlanned=False, storyboardLinks=links, customContext='Preserve this')
        state = cast_use_state(data, alternate, reviews)
        self.assertEqual(state['validLinks'], links[:1])
        self.assertEqual(state['unresolvedLinks'], links[1:])
        groups = build_design_model(data, 'hon', 'cast', reviews)['sections'][0]['groups']
        self.assertEqual(len(cast_browse_groups(groups, connection='linked')), 1)
        self.assertEqual(len(next(g for g in groups if g['id']=='wife-group')['browseFacts']['unresolved']), 2)
        payload = review_payload(data['assets'], reviews, set())
        restored, _, skipped = read_review(payload, data['assets'])
        self.assertEqual(skipped, 0)
        self.assertEqual(restored['wife-v2']['castUse'], reviews['wife-v2']['castUse'])
        self.assertEqual(restored['boss']['note'], 'Keep prior note')
        self.assertEqual(restored['boss']['likenessRating'], 4)
        self.assertEqual(data, before)
        self.assertTrue(cast_use_state(data, boss, {'boss': {'castUse': None}})['roleSelected'])
        self.assertTrue(cast_use_state(data, boss, {'boss': {'castUse': {'storyboardPlanned': True}}})['roleSelected'])

    def test_targets_are_real_and_invalid_inputs_do_not_disappear(self):
        data = fixture()
        self.assertEqual({(row['storyID'],row['shotID']) for row in cast_story_targets(data, 'hon')},
                         {('hon:story','S01-1'), ('hon:sequence','sequence-shot')})
        link = dict(storyID='unknown-story', shotID='unknown-shot', source='Preserve imported provenance')
        normalized = normalize_decision({'castUse': {'roleSelected': False, 'storyboardLinks': [link,dict(link)], 'future': {'raw':1}}})
        self.assertEqual(normalized['castUse']['storyboardLinks'], [link])
        self.assertEqual(normalized['castUse']['future'], {'raw':1})
        for raw in ({'roleSelected':1}, {'storyboardPlanned':'yes'}, {'role':'x'*301},
                    {'storyboardLinks':[{'storyID':'hon:story','shotID':''}]}):
            with self.assertRaises(ValueError): normalize_decision({'castUse': raw})

    def test_real_wife_plan_increases_character_count_once(self):
        catalog = APP/'library/design_catalog.json'
        if catalog.exists():
            data = json.loads(catalog.read_text(encoding='utf-8'))
        else:
            catalog = APP.parents[1]/'docs/notes/explorable_world/comfy/projects/visual_library/catalog.js'
            data = json.loads(catalog.read_text(encoding='utf-8').split('=',1)[1].strip().rstrip(';'))
        reviews = effective_reviews(data['assets'], data.get('reviewDecisions', []), {})
        groups = build_design_model(data, 'hon', 'cast', reviews)['sections'][0]['groups']
        self.assertEqual(len(cast_browse_groups(groups, connection='planned')), 2)
        group = next(g for g in data['castCollections'] if g['id']=='hon:cast-ivory')
        by_id = {a['id']:a for a in data['assets']}
        for aid in group['assetIDs'][:2]:
            value = cast_use_state(data, by_id[aid], reviews)['value']
            value['storyboardPlanned'] = True
            reviews[aid] = {**reviews.get(aid, {}), 'castUse': value}
            groups = build_design_model(data, 'hon', 'cast', reviews)['sections'][0]['groups']
            self.assertEqual(len(cast_browse_groups(groups, connection='planned')), 3)

    def test_native_controls_preserve_source_role_and_link_exact_version(self):
        names = {'set_review_field','cast_control_state','save_cast_field','add_cast_link','remove_cast_link','render_cast_controls'}
        tree = ast.parse((APP/'app.py').read_text(encoding='utf-8'))
        code = ast.unparse(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]))
        data = fixture()
        script = f"""
import sys
sys.path.insert(0, {str(APP)!r})
import streamlit as st
from datetime import datetime, timezone
from library_helpers import effective_reviews, review_payload
REVIEW_EDITABLE_FIELDS = ('status','note','castUse')
{code}
data = {data!r}
if 'studio_review_overrides' not in st.session_state: st.session_state.studio_review_overrides = {{}}
st.session_state.studio_reviews = effective_reviews(data['assets'], [dict(id='boss',sha256='a'*64,status='keep',note='Existing note')], st.session_state.studio_review_overrides)
render_cast_controls(data['assets'][0], data)
st.session_state.fixture_export = review_payload(data['assets'], st.session_state.studio_reviews, set())
"""
        # AppTest's temporary script writer follows the Windows locale; keep
        # its source ASCII while preserving Unicode string literal contents.
        app = AppTest.from_string(script.encode('ascii', 'backslashreplace').decode('ascii'), default_timeout=60).run()
        self.assertFalse(app.exception)
        self.assertTrue(app.checkbox(key='cast-role-selected:boss').value)
        app.checkbox(key='cast-planned:boss').check().run()
        self.assertFalse(app.exception)
        decision = app.session_state.studio_reviews['boss']
        self.assertTrue(decision['castUse']['roleSelected'])
        self.assertEqual(decision['castUse']['role'], 'Boss')
        self.assertEqual(decision['note'], 'Existing note')
        self.assertEqual(decision['status'], 'keep')
        self.assertIn('castUse', decision['fieldUpdatedAt'])
        app.selectbox(key='cast-link-story:boss').select('hon:story').run()
        app.selectbox(key='cast-link-shot:boss').select('S01-1').run()
        app.button(key='cast-link-add:boss').click().run()
        self.assertFalse(app.exception)
        links = app.session_state.studio_reviews['boss']['castUse']['storyboardLinks']
        self.assertEqual(links, [dict(storyID='hon:story',shotID='S01-1')])
        restored, _, _ = read_review(app.session_state.fixture_export, data['assets'])
        self.assertEqual(restored['boss']['castUse']['storyboardLinks'], links)
        app.button(key='cast-unlink:boss:0').click().run()
        app.checkbox(key='cast-planned:boss').uncheck().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.studio_reviews['boss']['castUse']['storyboardLinks'], [])
        self.assertTrue(app.session_state.studio_reviews['boss']['castUse']['roleSelected'])
        self.assertNotIn('shotPlan', app.session_state.studio_review_overrides['boss'])


if __name__ == '__main__': unittest.main()
