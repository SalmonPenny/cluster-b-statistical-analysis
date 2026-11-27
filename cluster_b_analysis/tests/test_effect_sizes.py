from decimal import Decimal
import unittest

from cluster_b_analysis.src.effect_sizes import (
    Score, absolute_difference, percentage_point_difference, relative_error_reduction,
    relative_event_reduction, relative_improvement,
)


class EffectSizeTests(unittest.TestCase):
    def test_rmm_gte(self):
        method, baseline = Score(70.4, "percent"), Score(63.6, "percent")
        self.assertEqual(absolute_difference(method, baseline, "higher"), Decimal("6.8"))
        self.assertEqual(percentage_point_difference(method, baseline, "higher"), Decimal("6.8"))
        self.assertAlmostEqual(relative_improvement(method, baseline, "higher", ratio_scale=True),
                               Decimal("0.106918239"), places=8)
        self.assertAlmostEqual(relative_error_reduction(method, baseline, error_complement=True),
                               Decimal("0.186813187"), places=8)

    def test_lower_direction_and_direct_event_semantics(self):
        method, baseline = Score(.04, "proportion"), Score(.10, "proportion")
        self.assertEqual(absolute_difference(method, baseline, "lower"), Decimal(".06"))
        self.assertEqual(percentage_point_difference(method, baseline, "lower"), Decimal("6"))
        self.assertEqual(relative_event_reduction(method, baseline, direct_undesirable_rate=True),
                         Decimal(".6"))
        self.assertIsNone(relative_event_reduction(method, baseline, direct_undesirable_rate=False))
        self.assertEqual(absolute_difference(method, baseline, "higher"), Decimal("-.06"))

    def test_missing_and_unknown_direction(self):
        missing, known = Score(None, "percent"), Score(45, "percent")
        self.assertIsNone(absolute_difference(missing, known, "higher"))
        self.assertIsNone(relative_improvement(known, missing, "higher", ratio_scale=True))
        self.assertIsNone(relative_error_reduction(missing, known, error_complement=True))
        self.assertIsNone(relative_event_reduction(missing, known, direct_undesirable_rate=True))
        self.assertIsNone(percentage_point_difference(known, known, ""))

    def test_unit_validation(self):
        with self.assertRaisesRegex(ValueError, "same known unit"):
            absolute_difference(Score(80, "percent"), Score(.60, "proportion"), "higher")
        with self.assertRaisesRegex(ValueError, "unit bounds"):
            absolute_difference(Score(140, "percent"), Score(60, "percent"), "higher")
        self.assertIsNone(percentage_point_difference(Score(7, "seconds"), Score(10, "seconds"), "lower"))

    def test_zero_and_ceiling_denominators(self):
        zero, full = Score(0, "percent"), Score(100, "percent")
        self.assertIsNone(relative_improvement(full, zero, "higher", ratio_scale=True))
        self.assertIsNone(relative_event_reduction(full, zero, direct_undesirable_rate=True))
        self.assertIsNone(relative_error_reduction(zero, full, error_complement=True))
        self.assertEqual(relative_error_reduction(full, zero, error_complement=True), Decimal("1"))
        self.assertEqual(absolute_difference(full, full, "higher"), Decimal("0"))

    def test_scientific_applicability(self):
        baseline, method = Score(60, "percent"), Score(75, "percent")
        self.assertIsNone(relative_error_reduction(method, baseline, error_complement=False))
        self.assertIsNone(relative_improvement(method, baseline, "higher", ratio_scale=False))
        self.assertIsNone(relative_event_reduction(Score(5, "seconds"), Score(10, "seconds"),
                                                   direct_undesirable_rate=True))
