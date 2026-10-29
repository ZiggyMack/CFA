"""Exercise both structure views without modifying a saved review."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP))

class StructureAppTest(unittest.TestCase):
    def test_structure_and_empty_template_preserve_reviews(self):
        app=AppTest.from_file(str(APP/'app.py'),default_timeout=60).run()
        self.assertFalse(app.exception)
        before=deepcopy(app.session_state['studio_reviews'])
        app.button(key='nav:Storyboard').click().run()
        app.radio(key='story-view:hon').set_value('Structure & gaps').run()
        self.assertFalse(app.exception)
        self.assertTrue(any('70 planned shots' in c.value and '14 sequences' in c.value for c in app.caption))
        app.selectbox(key='structure-sequence:hon').select('S02').run()
        self.assertTrue(any(e.label.startswith('S02-9 ·') for e in app.expander))
        app.selectbox(key='structure-focus:hon').select('Camera missing / not assessed').run()
        self.assertFalse(app.exception)
        self.assertFalse(any(e.label.startswith('S02-9 ·') for e in app.expander))
        app.radio(key='structure-mode:hon').set_value('Blank storyboard / shot template').run()
        self.assertFalse(app.exception)
        self.assertEqual(sum('Empty template' in e.label for e in app.expander),28)
        self.assertFalse(any(e.label.startswith('S02-') for e in app.expander))
        self.assertEqual(app.session_state['studio_reviews'],before)

if __name__=='__main__': unittest.main()
