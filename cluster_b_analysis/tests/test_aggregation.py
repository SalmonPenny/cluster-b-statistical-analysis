import unittest

from cluster_b_analysis.src.aggregation import aggregate, contrast_availability


def contrast(effect, *, study="a", cohort="one", protocol="p", endpoint="x",
             stratum="LongMemEval|Accuracy|pp", target=None, reference=None):
    source_key = f"{study}/{protocol}/{endpoint}"
    return {
        "stratum": stratum,
        "study": study,
        "cohort": cohort,
        "protocol": protocol,
        "endpoint": endpoint,
        "target_observation_id": target or f"{source_key}/target",
        "reference_observation_id": reference or f"{source_key}/reference",
        "effect": effect,
    }


class AggregationTests(unittest.TestCase):
    def test_unequal_observations_protocols_studies_and_cohorts(self):
        rows = [
            contrast(0),
            contrast(2, endpoint="y"),
            contrast(8, protocol="q"),
            contrast(12, study="b"),
            contrast(20, study="c", cohort="two"),
        ]
        protocols, cohorts, (profile,) = aggregate(rows)
        self.assertEqual([row["effect"] for row in protocols], [1, 8, 12, 20])
        self.assertEqual([row["effect"] for row in cohorts], [7, 20])
        self.assertEqual(cohorts[0]["studies"], ("a", "b"))
        self.assertEqual(cohorts[0]["protocols"], (("a", "p"), ("a", "q"), ("b", "p")))
        self.assertEqual(profile["observation_weighted_mean"], 42 / 5)
        self.assertEqual(profile["protocol_weighted_mean"], 41 / 4)
        self.assertEqual(profile["study_balanced_mean"], (4.5 + 12 + 20) / 3)
        self.assertEqual(profile["cohort_balanced_mean"], 27 / 2)
        self.assertEqual(tuple(profile[key] for key in (
            "n_observations", "n_protocols", "n_studies", "n_cohorts", "n_source_observations",
        )), (5, 4, 3, 2, 10))
        self.assertEqual(aggregate(rows), aggregate(reversed(rows)))

    def test_duplicate_pair_and_endpoint_preserve_source_ids(self):
        first = contrast(8, target="same-a", reference="shared")
        exact = dict(first)
        same_endpoint = contrast("8.00", target="same-b", reference="shared")
        other_endpoint = contrast(-2, endpoint="y", target="other", reference="shared")
        results = aggregate([first, exact, same_endpoint, other_endpoint])
        for (summary,) in results:
            self.assertEqual(summary["n_observations"], 2)
            self.assertEqual(summary["n_source_pairs"], 3)
            self.assertEqual(summary["n_source_observations"], 4)
            self.assertEqual(summary["observation_pairs"], (
                ("other", "shared"), ("same-a", "shared"), ("same-b", "shared"),
            ))
        protocol, cohort, profile = (rows[0] for rows in results)
        self.assertEqual(protocol["effect"], 3)
        self.assertEqual(cohort["effect"], 3)
        self.assertEqual(profile["cohort_balanced_mean"], 3)

    def test_reversed_source_pair_is_rejected(self):
        forward = contrast(8, target="a", reference="b")
        reversed_pair = contrast(-8, target="b", reference="a")
        with self.assertRaisesRegex(ValueError, "reversed source pair"):
            aggregate([forward, reversed_pair])

    def test_conflicting_endpoint_and_cohort_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Conflicting effects for endpoint"):
            aggregate([contrast(5), contrast(7, target="different")])
        with self.assertRaisesRegex(ValueError, "conflicting cohort assignments"):
            aggregate([contrast(5), contrast(7, cohort="two", endpoint="y")])

    def test_missing_effect_is_excluded_and_zero_is_retained(self):
        rows = [contrast(None, protocol="q"), contrast("", study="b"), contrast(0)]
        protocols, cohorts, profiles = aggregate(rows)
        self.assertEqual(len(protocols), 1)
        self.assertEqual(cohorts[0]["n_studies"], 1)
        self.assertEqual(profiles[0]["observation_weighted_mean"], 0)
        self.assertEqual(profiles[0]["n_observations"], 1)
        self.assertEqual(aggregate(rows[:2]), ([], [], []))
        with self.assertRaisesRegex(ValueError, "Non-finite"):
            aggregate([contrast(float("nan"))])

    def test_strata_keep_benchmarks_and_incompatible_metrics_separate(self):
        rows = [
            contrast(1),
            contrast(99, stratum="LoCoMo|Accuracy|pp", target="locomo-accuracy"),
            contrast(100, stratum="LoCoMo|Latency|seconds", target="locomo-latency"),
        ]
        _, _, profiles = aggregate(rows)
        self.assertEqual({row["stratum"]: row["cohort_balanced_mean"] for row in profiles}, {
            "LongMemEval|Accuracy|pp": 1, "LoCoMo|Accuracy|pp": 99, "LoCoMo|Latency|seconds": 100,
        })

    def test_available_improvement_with_zero_ceiling_and_negative_change(self):
        self.assertAlmostEqual(contrast_availability("70.4", "63.6", 100), 6.8 / 36.4)
        self.assertEqual(contrast_availability(100, 0, 100), 1)
        self.assertEqual(contrast_availability(0, 0, 100), 0)
        self.assertEqual(contrast_availability(40, 60, 100), -0.5)
        self.assertIsNone(contrast_availability(90, 100, 100))
        self.assertIsNone(contrast_availability(None, 60, 100))
        with self.assertRaisesRegex(ValueError, "ceiling"):
            contrast_availability(105, 60, 100)
