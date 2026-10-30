"""Native app routes against the actual portable publication snapshot, read-only."""
import json
from pathlib import Path
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from library_helpers import effective_design_data, mission_visible
from streamlit.testing.v1 import AppTest


@unittest.skipUnless((APP / "library/design_catalog.json").is_file(), "Build the portable design snapshot first")
class DesignAppTest(unittest.TestCase):
    def launch(self):
        app = AppTest.from_file(str(APP / "app.py"), default_timeout=45).run()
        self.assertFalse(app.exception)
        return app

    def test_storyboard_review_lane_opens_exact_authored_package(self):
        app = self.launch()
        before = json.dumps(app.session_state.studio_reviews, sort_keys=True)
        self.assertTrue(any('1 writing package awaits your choices.' == caption.value for caption in app.caption))
        button = app.button(key='mission-storyboard-review:hon-coverage-review-queue-20261028')
        self.assertEqual(button.label, 'Review storyboard')
        button.click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.studio_view, 'Storyboard')
        self.assertEqual(app.selectbox(key='story-select:hon').value, 'hon:strictly-business')
        self.assertEqual(app.radio(key='story-view:hon').value, 'Structure & gaps')
        app.button(key='author-shot:hon-coverage-review-queue-20261028:1:P-6b').click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox(key='structure-sequence:hon').value, 'PROLOGUE')
        self.assertTrue(next(expander for expander in app.expander if expander.label.startswith('P-6b ·')).proto.expanded)
        self.assertFalse(any(area.label == 'Your answer' for area in app.text_area))
        self.assertNotIn('authorResponses', app.session_state.studio_review_provenance)
        app.button(key='nav:Ziggy’s Corner').click().run()
        self.assertTrue(all(not expander.proto.expanded for expander in app.expander if expander.label == 'Briefs and records'))
        app.button(key='mission-writing-workspace:hon-coverage-review-queue-20261028').click().run()
        self.assertEqual(app.session_state.studio_view, 'Storyboard')
        self.assertEqual(app.radio(key='story-view:hon').value, 'Structure & gaps')
        self.assertEqual(json.dumps(app.session_state.studio_reviews, sort_keys=True), before)

    def test_all_design_destinations_and_archive_restore_without_review_loss(self):
        app = self.launch()
        snapshot = json.loads((APP / "library/design_catalog.json").read_text(encoding="utf-8"))
        reviews = app.session_state["studio_reviews"]
        visible = effective_design_data(snapshot, reviews)
        plans = [asset for asset in visible["assets"] if reviews.get(asset["id"], {}).get("shotPlan") and mission_visible(asset, reviews)]
        self.assertGreater(len(plans), 0)
        self.assertEqual(app.button(key="mission-shot-plans").label, f"Shot plans · {len(plans)} →")
        app.button(key="mission-shot-plans").click().run()
        self.assertFalse(app.exception)
        self.assertIn(f"{len(plans)} saved shot plans across all projects.", [c.value for c in app.caption])
        app.button(key="corner-collection-back").click().run()
        nav = [b.label for b in app.sidebar.button]
        self.assertFalse(any(label == 'Needs review' for label in nav))
        self.assertEqual(nav[next(i for i, label in enumerate(nav) if label.startswith('Review queue ·')) + 1], "Archive")
        for view in ("Working references", "Outfits", "Tattoos & piercings", "Supporting cast", "Comfy swap targets", "Review queue", "Archive", "Videos", "Storyboard"):
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
