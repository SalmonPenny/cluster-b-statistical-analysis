import collections
import unittest

from cluster_b_analysis.src.candidate_selection import (
    DIAGNOSTIC, HALLUCINATION, HEAD_TO_HEAD, OTHER, PROXY, UNFAITHFULNESS,
    coverage_cell, evidence_class, head_to_head, inventory, matched_entry, shortlist, system_key,
)
from cluster_b_analysis.src.data_loading import ROOT
from cluster_b_analysis.src.stage2c_analysis import read


class CandidateSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data, results = ROOT / "data", ROOT / "results"
        cls.observations = {row["observation_id"]: row for row in read(data / "validated_results.csv")}
        cls.matrix = [matched_entry(row, cls.observations) for row in read(results / "matched_effect_sizes.csv")]
        cls.head = head_to_head(cls.matrix, cls.observations, *(read(results / f"{name}.csv") for name in (
            "pareto_fronts", "within_panel_rankings", "dominance_relations", "pareto_reported_uncertainty")))

    def test_direct_markers_are_reinterpreted_by_outcome(self):
        cases = [
            ("halumem", "Hallucination rate", HALLUCINATION),
            ("trustmem", "Hallucination rate", HALLUCINATION),
            ("sirin", "Strict unfaithfulness", UNFAITHFULNESS),
            ("synthius_mem", "LLM-Judge", DIAGNOSTIC),
            ("locomo_plus", "Constraint-consistency judge score", DIAGNOSTIC),
            ("es_memeval", "LLM-Judge", DIAGNOSTIC),
        ]
        for paper, metric, expected in cases:
            with self.subTest(paper=paper):
                row = next(r for r in self.observations.values() if
                           (r["paper_id"], r["metric"], r["hallucination_measurement"]) == (paper, metric, "direct"))
                self.assertEqual(evidence_class(row), expected)
        for paper, metric, expected in (("rmm", "Accuracy", PROXY), ("sirin", "Abstain rate", OTHER)):
            row = next(r for r in self.observations.values() if (r["paper_id"], r["metric"]) == (paper, metric))
            self.assertEqual(evidence_class(row), expected)
        resources = [row for row in self.observations.values()
                     if row["failure_mode"] and row["unit"] in {"seconds", "tokens", "thousands of tokens"}]
        self.assertTrue(resources)
        self.assertTrue(all(evidence_class(row) == OTHER for row in resources))

    def test_configuration_key_preserves_cross_judge_context(self):
        groups = collections.defaultdict(set)
        for row in self.observations.values():
            if row["paper_id"] == "root_memory" and row["table_id"] == "Table 7":
                groups[row["configuration_id"]].add(system_key(row))
        self.assertTrue(any(len(keys) > 1 for keys in groups.values()))

    def test_missing_class_has_no_numeric_effect(self):
        row = next(r for r in self.observations.values() if r["paper_id"] == "memoryrewardbench")
        _, profiles, matrix = inventory({row["observation_id"]: row}, [])
        gaps = [r for r in matrix if r["status"] == "no verified observation"]
        self.assertEqual(len(gaps), 4)
        self.assertTrue(all("score" not in r["target"] and "absolute_difference" not in r for r in gaps))
        self.assertTrue(any(r["status"] == "excluded or imported only" for r in profiles))

    def test_head_to_head_completeness_and_coverage_orientation(self):
        expected = [21, 30, 45, 30, 63, 63]
        counts = collections.Counter(r["panel"] for r in self.head)
        self.assertEqual(counts, dict(zip(HEAD_TO_HEAD, expected)))
        for row in self.head:
            if row["metric"] != "Answer coverage":
                continue
            self.assertEqual(row["denominator_scope"], "all queries (coverage)")
            self.assertNotIn("reported_paired_statistics", row)
            for side in ("target", "reference"):
                cell = row[side]
                source = self.observations[cell["source"]["observation_id"]]
                self.assertEqual(coverage_cell(source), cell)
                self.assertEqual(cell["source_abstention_score_as_printed"], source["score_as_printed"])
                self.assertEqual(cell["score_as_printed"], "")
                self.assertAlmostEqual(float(cell["score"]) + float(source["score"]), 100)
        interval_rows = [item for row in self.head for item in row.get("reported_paired_statistics", [])]
        self.assertEqual(len({item["observation_id"] for item in interval_rows}), 8)
        for item in interval_rows:
            if item["metric"].startswith("Probe minus Judge"):
                self.assertIn("SIRIN Probing:", item["reported_target_configuration_id"])
                self.assertIn("SIRIN Judge:", item["reported_reference_configuration_id"])

    def test_shortlist_preserves_variant_specific_scope_and_cohorts(self):
        selected = {row["candidate_id"]: row for row in shortlist(
            self.matrix, read(ROOT / "results/pareto_fronts.csv"),
            read(ROOT / "results/pareto_reported_uncertainty.csv"), self.observations)}
        self.assertEqual(selected["halumem-memos"]["n_anchor_panels"], 2)
        self.assertEqual(selected["halumem-memos"]["n_cohort_labels"], 1)
        self.assertEqual(selected["memgpt-retrieval"]["n_anchor_panels"], 3)
        for system in ("memos", "evermemos", "lightmem"):
            self.assertEqual(len(selected[f"{system}-rootmem"]["configuration_ids"]), 1)
        self.assertEqual(len(selected["sirin-mem0-both"]["reported_paired_statistics_source_ids"]), 2)

    def test_known_memguard_result_preserves_lower_is_better(self):
        entry = next(r for r in self.matrix if r["paper_id"] == "memguard" and
                     r["metric"] == "Hallucination rate" and r["task"] == "Question answering")
        self.assertEqual(entry["evidence_class"], HALLUCINATION)
        self.assertEqual(entry["difference_pp"], "-0.29")
        self.assertEqual(entry["directional_result"], "favors reference")
