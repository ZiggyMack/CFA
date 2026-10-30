"""Hosted deep links stay scoped to the published project and survive refresh."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from full_dashboard_component import query_route, route_config, route_query_update, valid_route


class DashboardRouteTest(unittest.TestCase):
    def setUp(self):
        cache = APP.parents[1] / '.cache'
        cache.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='dashboard-routes-', dir=cache)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.snapshot = self.root / 'full_dashboard_bundle/snapshots/test'
        self.snapshot.mkdir(parents=True)
        self.catalog = {'projects': [{'id': 'hon'}, {'id': 'lisan'}, {'id': 'criminal_mind'}],
                        'categories': [['storyboard', 'Storyboard']], 'assets': [], 'albums': []}
        (self.snapshot / 'catalog.js').write_text('window.REVIEW_CATALOG=' + json.dumps(self.catalog) + ';', encoding='utf-8')
        (self.snapshot / 'index.html').write_text('<html>Fixture</html>', encoding='utf-8')
        self.config = route_config(self.snapshot)

    def test_project_and_casa_direct_links_have_distinct_routes(self):
        self.assertEqual(query_route({'project': 'criminal_mind'}, self.config), '#criminal_mind/all')
        self.assertEqual(query_route({'project': 'criminal_mind', 'view': 'casa_baldadoon'}, self.config), '#criminal_mind/casa_baldadoon')
        self.assertEqual(query_route({'project': 'hon', 'view': 'storyboard'}, self.config), '#hon/storyboard')
        self.assertEqual(query_route({'project': 'lisan'}, self.config), '#lisan/all')

    def test_native_library_and_legacy_overview_aliases_normalize_only_at_query_boundary(self):
        for project in ('hon', 'lisan', 'criminal_mind'):
            for label in ('Library', 'All files'):
                self.assertEqual(query_route({'project': project, 'view': label}, self.config), f'#{project}/all')
                self.assertIsNone(valid_route(f'#{project}/{label}', self.config))
        self.assertEqual(query_route({'project': 'criminal_mind', 'view': 'project_home'}, self.config), '#criminal_mind/all')
        self.assertEqual(query_route({'project': 'hon', 'view': 'project_home'}, self.config), '#hon/project_home')
        self.assertEqual(query_route({'project': 'criminal_mind', 'view': 'Library', 'album': 'source block'}, self.config),
                         '#criminal_mind/all/source%20block')
        for label in ('library', 'All Files', 'Library/asset', ['Library']):
            self.assertIsNone(query_route({'project': 'criminal_mind', 'view': label}, self.config))

    def test_unknown_projects_external_urls_and_path_tricks_are_rejected(self):
        for value in ('https://example.com', '#missing/all', '#criminal_mind/missing',
                      '#criminal_mind/asset/a%2Fb', '#criminal_mind/asset/a%5Cb',
                      '#criminal_mind/asset/a%0Ab', '#criminal_mind/project_home/extra/more'):
            self.assertIsNone(valid_route(value, self.config), value)
        self.assertIsNone(query_route({'project': 'missing'}, self.config))
        self.assertIsNone(query_route({'project': 'criminal_mind', 'view': 'https://example.com'}, self.config))

    def test_reported_navigation_round_trips_without_accepting_stale_request(self):
        value = {'route': '#criminal_mind/documents/source%20block', 'requestedRoute': '#criminal_mind/project_home'}
        self.assertEqual(route_query_update(value, value['requestedRoute'], self.config),
                         {'project': 'criminal_mind', 'view': 'documents', 'album': 'source block'})
        self.assertIsNone(route_query_update(value, '#hon/all', self.config))
        self.assertIsNone(route_query_update({'route': '#missing/all', 'requestedRoute': None}, None, self.config))
        self.assertIsNone(route_query_update(None, None, self.config))

    def test_alias_request_uses_canonical_acknowledgement_without_accepting_old_route(self):
        initial = query_route({'project': 'criminal_mind', 'view': 'Library'}, self.config)
        self.assertEqual(route_query_update({'route': initial, 'requestedRoute': initial}, initial, self.config),
                         {'project': 'criminal_mind', 'view': 'all', 'album': None})
        self.assertIsNone(route_query_update({'route': '#hon/all', 'requestedRoute': '#criminal_mind/project_home'},
                                            initial, self.config))
        self.assertIsNone(route_query_update({'route': '#criminal_mind/Library', 'requestedRoute': initial},
                                            initial, self.config))

    def test_full_page_passes_route_and_keeps_native_state_on_rerun(self):
        from streamlit.testing.v1 import AppTest
        from streamlit.runtime.pages_manager import PagesManager
        shutil.copyfile(APP / 'full_dashboard_component.py', self.root / 'full_dashboard_component.py')
        page = self.root / '01_Full_Visual_Library.py'
        # This page's APP_DIR is its parent.parent, so retain its normal folder.
        pages = self.root / 'pages'
        pages.mkdir()
        page = pages / page.name
        shutil.copyfile(APP / 'pages/01_Full_Visual_Library.py', page)
        (self.root / 'full_dashboard_bundle/current.json').write_text(json.dumps({
            'snapshot': 'snapshots/test', 'assetCount': 0, 'buildID': 'test'}), encoding='utf-8')
        (self.root / 'app.py').write_text("import streamlit as st\nst.title('Studio')\n", encoding='utf-8')
        with patch.object(PagesManager, 'uses_pages_directory', None):
            app = AppTest.from_file(str(self.root / 'app.py'), default_timeout=30).run()
            app.switch_page('pages/01_Full_Visual_Library.py')
            app.query_params['project'] = 'criminal_mind'
            app.query_params['view'] = 'casa_baldadoon'
            app.session_state.studio_project = 'hon'
            app.session_state.studio_reviews = {'existing': {'status': 'keep'}}
            app.run()
            self.assertFalse(app.exception)
            args = json.loads(app.get('component_instance')[0].proto.json_args)
            self.assertEqual(args['initialRoute'], '#criminal_mind/casa_baldadoon')
            self.assertIn('criminal_mind', args['routeConfig']['projects'])
            app.run()
            self.assertFalse(app.exception)
            self.assertEqual(app.query_params['project'], ['criminal_mind'])
            self.assertEqual(app.session_state.studio_project, 'hon')
            self.assertEqual(app.session_state.studio_reviews, {'existing': {'status': 'keep'}})
            for label in ('Library', 'project_home'):
                app.query_params['view'] = label
                app.run()
                self.assertFalse(app.exception)
                args = json.loads(app.get('component_instance')[0].proto.json_args)
                self.assertEqual(args['initialRoute'], '#criminal_mind/all')
                self.assertEqual(app.session_state.studio_project, 'hon')
                self.assertEqual(app.session_state.studio_reviews, {'existing': {'status': 'keep'}})


if __name__ == '__main__':
    unittest.main()
