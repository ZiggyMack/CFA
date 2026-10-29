"""Grok video is an explicit draft destination, separate from legacy still routing."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library_helpers import destination_label, handoff_payload, handoff_text, normalize_plan, read_review, review_payload


class GrokVideoRouteTest(unittest.TestCase):
    def test_route_roundtrip_does_not_change_source_or_existing_decision(self):
        assets = [{"id": "clip", "project": "hon", "sha256": "a" * 64, "kind": "video",
                   "filename": "clip.mp4", "repoPath": "references/clip.mp4", "provider": "Gemini"}]
        reviews = {"clip": {"status": "keep", "note": "My exact note", "likenessRating": 4, "sceneQualityRating": 5,
                            "shotPlan": {"status": "planned", "destinations": ["Grok", "grok_video"], "idea": "Exact idea", "prompt": "Exact prompt"}}}
        before = deepcopy((assets, reviews))
        exported = review_payload(assets, reviews, set())
        restored, _, skipped = read_review(exported, assets)
        self.assertEqual(skipped, 0)
        self.assertEqual(restored["clip"]["shotPlan"], reviews["clip"]["shotPlan"])
        for field in ("status", "note", "likenessRating", "sceneQualityRating"):
            self.assertEqual(restored["clip"][field], reviews["clip"][field])
        self.assertEqual((assets, reviews), before)

    def test_exact_route_exports_do_not_reinterpret_still_plans(self):
        assets = [{"id": key, "project": "hon", "sha256": key, "filename": key + ".jpg"} for key in ("still", "video")]
        reviews = {key: {"shotPlan": {"destinations": [route], "idea": "A scene", "prompt": "Keep its look"}}
                   for key, route in (("still", "Grok"), ("video", "grok_video"))}
        video = handoff_payload(assets, reviews, "hon", "grok_video")
        still = handoff_payload(assets, reviews, "hon", "Grok")
        self.assertEqual([row["id"] for row in video["items"]], ["video"])
        self.assertEqual([row["id"] for row in still["items"]], ["still"])
        self.assertEqual(video["status"], "planned; not sent or generated")
        self.assertIn("Grok video", handoff_text(video))
        self.assertIn("Grok stills", handoff_text(still))
        self.assertEqual(destination_label("Flow"), "Flow")
        self.assertEqual(normalize_plan({"status": "sent", "destinations": ["grok_video", "grok_video"]})["status"], "planned")
        self.assertEqual(normalize_plan({"destinations": ["Grok"]})["destinations"], ["Grok"])


if __name__ == "__main__":
    unittest.main()
