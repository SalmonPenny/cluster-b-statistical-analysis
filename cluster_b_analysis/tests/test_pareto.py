import unittest

from cluster_b_analysis.src.pareto import comparison_coverage, complete_panel, fronts, relation


class ParetoTests(unittest.TestCase):
    directions = {"accuracy": "higher", "cost": "lower"}
    a = {"accuracy": 8, "cost": 2}
    b = {"accuracy": 8, "cost": 4}
    c = {"accuracy": 9, "cost": 8}

    def test_weak_standard_strict(self):
        self.assertEqual(relation(self.a, self.b, self.directions), (True, True, False))
        self.assertEqual(relation(self.a, self.a, self.directions), (True, False, False))
        self.assertEqual(relation(self.a, {"accuracy": 7, "cost": 4}, self.directions), (True, True, True))

    def test_fronts_equal_vectors_and_order(self):
        vectors = {"a": self.a, "b": self.b, "c": self.c, "identical": self.a}
        expected = [("a", "c", "identical"), ("b",)]
        self.assertEqual(fronts(vectors, self.directions), expected)
        self.assertEqual(fronts(dict(reversed(list(vectors.items()))), self.directions), expected)

    def test_missing_objective_and_incompatible_panel(self):
        candidates = {"a": self.a, "b": self.b, "incomplete": {"accuracy": 10}}
        vectors, excluded = complete_panel(candidates, self.directions, lambda a, b: True)
        self.assertEqual(set(vectors), {"a", "b"})
        self.assertIn("cost", excluded["incomplete"])
        self.assertEqual(comparison_coverage(candidates, vectors),
                         {"candidate_systems": 3, "eligible_systems": 2, "candidate_pairs": 3, "eligible_pairs": 1})
        with self.assertRaisesRegex(ValueError, "Incompatible"):
            complete_panel(candidates, self.directions, lambda a, b: False)
        with self.assertRaisesRegex(ValueError, "Missing"):
            relation({"accuracy": 10, "cost": None}, self.b, self.directions)

    def test_monotone_transformations_keep_fronts(self):
        vectors = {"a": self.a, "b": self.b, "c": self.c}
        transformed = {name: {"accuracy": v["accuracy"] ** 3, "cost": 13*v["cost"] + 2}
                       for name, v in vectors.items()}
        self.assertEqual(fronts(vectors, self.directions), fronts(transformed, self.directions))
