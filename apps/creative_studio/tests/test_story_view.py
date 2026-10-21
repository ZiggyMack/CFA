import json
from pathlib import Path
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from story_view import song_panels, sequence_coverage


class StoryViewsTest(unittest.TestCase):
    def test_song_does_not_mix_independent_sequence_or_unpositioned_references(self):
        data = {"albums": [{"id": "song", "project": "hon", "category": "storyboard", "assetIDs": ["a", "b", "reference"]},
                           {"id": "independent", "project": "hon", "category": "storyboard", "assetIDs": ["other"]}],
                "storyboardSequences": [{"project": "hon", "sourceAlbumIDs": ["independent"]}],
                "assets": [{"id": "a", "storyboardPosition": 20, "storyboardOrder": 2},
                           {"id": "b", "storyboardPosition": 10, "storyboardOrder": 1}, {"id": "reference"},
                           {"id": "other", "storyboardPosition": 0}]}
        self.assertEqual([a["id"] for a in song_panels(data, "hon", {})], ["b", "a"])
        self.assertEqual([a["id"] for a in song_panels(data, "hon", {"b": {"collectionState": "archived"}})], ["a"])

    def test_coverage_counts_shots_not_materials_and_respects_visibility(self):
        sequence = {"sections": [{"scene": 1}], "shots": [
            {"materials": [{"assetID": "frame", "role": "setting_stand_in"}, {"assetID": "frame2", "role": "source_frame"}], "pendingReferences": ["Character"]},
            {"materials": [{"assetID": "video", "role": "result_on_disk"}]}]}
        assets = {key: {"id": key} for key in ("frame", "frame2", "video")}
        self.assertEqual(sequence_coverage(sequence, assets, {}), {"shots": 2, "scenes": 1, "frames": 1, "results": 1, "pending": 1})
        self.assertEqual(sequence_coverage(sequence, assets, {"video": {"status": "remove"}})["results"], 0)

    def test_packaged_story_counts_when_bundle_available(self):
        path = APP / "library/design_catalog.json"
        if not path.exists():
            self.skipTest("Design snapshot not built yet")
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(len(song_panels(data, "hon", {})), 36)
        self.assertEqual(len(song_panels(data, "lisan", {})), 50)
        seq = next(s for s in data["storyboardSequences"] if s["id"] == "LAG-STORY-01-THE-GLOVED-HAND")
        self.assertEqual(sequence_coverage(seq, {a['id']: a for a in data['assets']}, {}),
                         {"shots": 38, "scenes": 9, "frames": 33, "results": 1, "pending": 21})


if __name__ == '__main__':
    unittest.main()
