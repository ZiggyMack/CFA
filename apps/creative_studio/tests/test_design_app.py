"""Native app routes against the actual portable publication snapshot, read-only."""
import json
from pathlib import Path
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from streamlit.testing.v1 import AppTest


@unittest.skipUnless((APP / "library/design_catalog.json").is_file(), "Build the portable design snapshot first")
class DesignAppTest(unittest.TestCase):
    def launch(self):
        app = AppTest.from_file(str(APP / "app.py"), default_timeout=45).run()
        self.assertFalse(app.exception)
        return app

    def test_all_design_destinations_and_archive_restore_without_review_loss(self):
        app = self.launch()
        self.assertEqual(app.button(key="mission-shot-plans").label, "Shot plans · 18 →")
        nav = [b.label for b in app.sidebar.button]
        self.assertEqual(nav[nav.index("Needs review") + 1], "Archive")
        for view in ("Working references", "Outfits", "Tattoos & piercings", "Supporting cast", "Comfy swap targets", "Needs review", "Archive", "Videos", "Storyboard"):
            app.button(key="nav:" + view).click().run()
            self.assertFalse(app.exception, view)
        app.button(key="nav:Working references").click().run()
        toggle = next(b for b in app.button if b.label == "Show references")
        toggle.click().run()
        self.assertFalse(app.exception)
        headings = [h.value for h in app.subheader]
        self.assertIn("Body art", headings)
        self.assertIn("Bling bling", headings)
        self.assertIn("Wardrobe", headings)
        self.assertLess(headings.index("Body art"), headings.index("Bling bling"))
        self.assertLess(headings.index("Bling bling"), headings.index("Wardrobe"))
        dental = "HD-B-91ef00348229"
        next(b for b in app.button if (b.key or "").startswith("open:design:") and b.key.endswith(":" + dental)).click().run()
        self.assertFalse(app.exception)
        before = dict(app.session_state["studio_reviews"][dental])
        app.button(key="archive:" + dental).click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.button(key="archive:" + dental).label, "Restore from Archive")
        app.button(key="archive:" + dental).click().run()
        self.assertEqual(app.button(key="archive:" + dental).label, "Archive")
        after = app.session_state["studio_reviews"][dental]
        self.assertEqual(after.get("status"), before.get("status"))
        self.assertEqual(after.get("note"), before.get("note"))
        self.assertEqual(after.get("likenessRating"), before.get("likenessRating"))
        self.assertEqual(after.get("shotPlan"), before.get("shotPlan"))

    def test_story_selection_and_lisan_references(self):
        app = self.launch()
        app.selectbox(key="studio_project").select("lisan").run()
        app.button(key="nav:Storyboard").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox(key="story-select:lisan").value, "lisan:meta-mirror")
        app.selectbox(key="story-select:lisan").select("lisan:story-01").run()
        self.assertFalse(app.exception)
        self.assertTrue(any("38 shots" in c.value and "9 scenes" in c.value for c in app.caption))
        app.button(key="nav:Working references").click().run()
        next(b for b in app.button if b.label == "Show references").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Natural face and neck marks" in m.value for m in app.markdown))


if __name__ == '__main__':
    unittest.main()
