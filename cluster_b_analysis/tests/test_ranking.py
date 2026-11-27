import unittest

from cluster_b_analysis.src.ranking import pair_outcomes, rank_reversals, rankings


class RankingTests(unittest.TestCase):
    def test_ties_and_rank_reversals(self):
        directions = {"quality": "higher", "cost": "lower"}
        panel = {"a": {"quality": 80, "cost": 5}, "b": {"quality": 80, "cost": 7},
                 "c": {"quality": 70, "cost": 4}}
        self.assertEqual(rankings(panel, directions), {
            "quality": {"a": 1, "b": 1, "c": 3}, "cost": {"a": 2, "b": 3, "c": 1}})
        self.assertEqual(pair_outcomes(panel["a"], panel["b"], directions), (("cost",), ("quality",), ()))
        self.assertEqual(list(rank_reversals(panel, directions)), [
            ("a", "c", "quality", "cost"), ("b", "c", "quality", "cost")])
