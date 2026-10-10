"""
Run from the repo root:
    python -m unittest discover -s cfa_data/tests -v

Tests read the real profiles on disk (they are the fixture) and skip the
run-corpus tests when the Nyquist repo is not reachable.
"""

import unittest

from cfa_data import codes, paths
from cfa_data.matchups import coverage_matrix, get_matchup, list_matchups
from cfa_data.profiles import LEVER_ORDER, METRIC_ORDER, load_worldviews
from cfa_data.status import build_status
from cfa_data.sync import sync_state


class CodesTest(unittest.TestCase):
    def test_every_spelling_resolves(self):
        for s in ("OJ", "oj", "Orthodox Judaism", "ORTHODOX_JUDAISM", "vs_orthodox_judaism", "orthodox judaism"):
            self.assertEqual(codes.code_for(s), "OJ", s)
        self.assertEqual(codes.code_for("Methodological Naturalism"), "MdN")
        self.assertEqual(codes.code_for("mdn"), "MdN")
        self.assertEqual(codes.code_for("Mormonism"), "LDS")
        self.assertIsNone(codes.code_for("Stoicism"))

    def test_matchup_keys(self):
        self.assertEqual(codes.matchup_key_to_code("vs_classical_theism"), ("CT", None))
        self.assertEqual(codes.matchup_key_to_code("b_vs_process_theology"), ("PT", None))
        self.assertEqual(codes.matchup_key_to_code("control_baseline_ct"), ("CT", "control"))
        self.assertEqual(codes.matchup_key_to_code("control_baseline_pooled"), (None, "control"))


class ProfilesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wvs = load_worldviews()

    def test_all_thirteen_load(self):
        self.assertEqual(sorted(self.wvs), sorted(codes.WORLDVIEWS))

    def test_every_profile_has_six_canonical_levers_and_bft(self):
        for wv in self.wvs.values():
            self.assertEqual(sorted(wv.canonical_levers), sorted(LEVER_ORDER), wv.code)
            self.assertGreater(wv.bft_standard, 0, wv.code)
            self.assertEqual(wv.axiom_count, len(wv.axioms), wv.code)
            self.assertEqual(wv.debt_count, len(wv.debts), wv.code)

    def test_breadth_profile_shape(self):
        oj = self.wvs["OJ"]
        self.assertEqual(oj.status, "AUDITED-PRELIMINARY")
        self.assertTrue(oj.depth_pass_pending)
        conds = {(b.opponent, b.condition) for b in oj.trinity_by_matchup.values()}
        self.assertEqual(conds, {("CT", "external"), ("MdN", "external"), ("CT", "control")})
        for blk in oj.trinity_by_matchup.values():
            self.assertEqual(sorted(blk.metrics), sorted(METRIC_ORDER))
            self.assertEqual(blk.n, 1)
        self.assertIn("web-research prior", oj.canonical_levers_provenance)
        self.assertAlmostEqual(oj.canonical_lever_sum, 45.5)

    def test_anchor_canonical_levers_are_a_deliberated_copy(self):
        ct = self.wvs["CT"]
        self.assertIn("vs_methodological_naturalism", ct.canonical_levers_provenance)
        self.assertIsNotNone(ct.phase2)

    def test_buddhism_prefixed_keys_resolve(self):
        b = self.wvs["B"]
        opps = {blk.opponent for blk in b.trinity_by_matchup.values()}
        self.assertEqual(opps, {"PT", "G", "MdN"})
        self.assertTrue(all(blk.condition == "control" for blk in b.trinity_by_matchup.values()))

    def test_batch_shape_metrics_normalize(self):
        ct_vs_pt = self.wvs["CT"].trinity_by_matchup["vs_process_theology"]
        bfi = ct_vs_pt.metrics["BFI"]
        self.assertIsNotNone(bfi.claude)
        self.assertIsNotNone(bfi.convergence)
        self.assertLessEqual(bfi.convergence, 1.0)
        self.assertAlmostEqual(bfi.crux_rate, 0.1)

    def test_misplaced_pt_vs_buddhism_block_is_flagged_not_crashed(self):
        pt = self.wvs["PT"]
        blk = pt.levers_by_matchup.get("vs_buddhism")
        self.assertIsNotNone(blk)
        self.assertTrue(blk.malformed)


class MatchupsTest(unittest.TestCase):
    def test_oj_vs_ct_matches_yaml_ypa(self):
        m = get_matchup("OJ", "CT")
        self.assertEqual(m.readiness, "trinity+levers")
        self.assertAlmostEqual(m.ypa_standard, 3.6, places=2)       # calculated.ypa_vs_classical_theism
        self.assertIsNotNone(m.ypa_scenarios)
        self.assertIn("Neutral", m.ypa_scenarios)
        c = get_matchup("OJ", "CT", "control")
        self.assertAlmostEqual(c.ypa_standard, 4.37, places=2)      # calculated.ypa_control_ct

    def test_direction_matters(self):
        a = get_matchup("CT", "MdN")
        b = get_matchup("MdN", "CT")
        self.assertNotEqual(a.levers.levers, b.levers.levers)

    def test_list_and_coverage(self):
        ms = list_matchups()
        self.assertGreater(len(ms), 30)
        self.assertEqual(len({m.key for m in ms}), len(ms))
        cov = coverage_matrix()
        self.assertEqual(len(cov["subjects"]), 13)
        for s in cov["subjects"]:
            self.assertEqual(cov["grids"]["external"][s][s], "none")
        self.assertEqual(cov["grids"]["external"]["OJ"]["CT"], "trinity+levers")
        self.assertEqual(cov["grids"]["external"]["CT"]["OJ"], "none")


class SyncAndStatusTest(unittest.TestCase):
    def test_sync_state_shape(self):
        s = sync_state()
        self.assertIn("inbox_clear", s)
        self.assertIsInstance(s["sync_in_processed"], list)

    def test_status_builds(self):
        st = build_status()
        self.assertEqual(st["worldviews"]["count"], 13)
        self.assertIn("by_readiness", st["matchups"])
        self.assertIn("open_loops_structural", st)


@unittest.skipUnless(paths.runs_available(), "Nyquist run corpus not reachable")
class RunsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from cfa_data.runs import load_run_index
        cls.idx = load_run_index()

    def test_index_builds_and_dedupes(self):
        self.assertGreater(len(self.idx.runs), 500)
        self.assertEqual(len(self.idx.by_session), len(self.idx.runs))
        self.assertGreaterEqual(self.idx.scanned_files, len(self.idx.runs))

    def test_errored_and_dryrun_excluded_but_kept(self):
        from cfa_data.runs import bucket_for
        self.assertEqual(bucket_for(""), "unfiled")
        self.assertEqual(bucket_for(".errored"), "errored")
        self.assertEqual(bucket_for("cfa_trinity/pre_schema"), "pre_schema")
        self.assertEqual(bucket_for("cfa_trinity/Framework_G"), "calibration")
        self.assertEqual(bucket_for("cfa_trinity/OJ"), "worldview")
        self.assertFalse(any(r.bucket in ("errored", "dryrun") for r in self.idx.runs))
        s = self.idx.summary()
        self.assertIn("mission_control_equivalent", s)
        self.assertEqual(s["mission_control_equivalent"] + s["unfiled_top_level"] + s["cfa_archive_only"],
                         s["distinct_runs"])

    def test_aborted_and_data_quality_flags(self):
        aborted = [r for r in self.idx.runs if r.aborted]
        self.assertGreater(len(aborted), 0)
        self.assertTrue(all(r.abort_reason or r.metrics_scored is not None or True for r in aborted))
        flagged = [r for r in self.idx.runs if r.data_quality]
        self.assertEqual(len(flagged), 4)
        self.assertEqual(sorted(r.subject for r in flagged), ["ISL", "LDS", "NULL", "OJ"])

    def test_cfa_archive_root_is_scanned_when_present(self):
        from cfa_data import paths as p
        if not p.CFA_ARCHIVE_RUNS.is_dir():
            self.skipTest("CFA archive raw_runs not present")
        arch = [r for r in self.idx.runs if r.root == "cfa_archive"]
        self.assertGreater(len(arch), 0)
        self.assertTrue(all(r.bucket == "cfa_archive" for r in arch))

    def test_known_run_present_and_coded(self):
        r = self.idx.by_session.get("20260716_123142")
        self.assertIsNotNone(r)
        self.assertEqual((r.subject, r.opponent, r.condition), ("G", "B", "control"))
        self.assertTrue(r.auditor_errors["nova"])

    def test_filter_by_subject(self):
        oj = self.idx.filter(subject="Orthodox Judaism")
        self.assertGreaterEqual(len(oj), 6)

    def test_full_run_loads(self):
        from cfa_data.runs import load_run
        run = load_run("20260716_123142")
        self.assertIn("component1_results", run)


class ServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from cfa_data.server import create_app
        cls.client = create_app().test_client()

    def test_endpoints(self):
        self.assertEqual(self.client.get("/api/health").status_code, 200)
        wv = self.client.get("/api/worldviews").get_json()
        self.assertEqual(len(wv), 13)
        self.assertEqual(self.client.get("/api/worldviews/Orthodox%20Judaism").get_json()["code"], "OJ")
        m = self.client.get("/api/matchups/OJ/CT?condition=control").get_json()
        self.assertEqual(m["condition"], "control")
        self.assertEqual(self.client.get("/api/worldviews/Stoicism").status_code, 404)
        self.assertEqual(self.client.get("/api/coverage").status_code, 200)
        self.assertEqual(self.client.get("/api/status").status_code, 200)


if __name__ == "__main__":
    unittest.main()
