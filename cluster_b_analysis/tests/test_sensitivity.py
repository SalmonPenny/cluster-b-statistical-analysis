import unittest

from cluster_b_analysis.src.pareto import fronts
from cluster_b_analysis.src.sensitivity import (
    analytical_weights, cycle_members, effect_sensitivity, normalize_weights, omit_objective,
    sampled_weights, served_event_frequency, tolerance_edges, tolerance_outcomes,
)


class SensitivityTests(unittest.TestCase):
    def test_tolerance_and_direction(self):
        ds={"quality":"higher","cost":"lower"}
        a,b={"quality":15,"cost":21},{"quality":10,"cost":20}
        self.assertEqual(tolerance_outcomes(a,b,ds,0),(1,0,1))
        self.assertEqual(tolerance_outcomes(a,b,ds,1),(1,1,0))
        self.assertEqual(tolerance_outcomes(a,b,ds,5),(0,2,0))

    def test_nontransitive_cycle(self):
        ds=dict.fromkeys("xyz","higher")
        rows={k:dict(zip(ds,v)) for k,v in {"A":(2,1,0),"B":(0,2,1),"C":(1,0,2)}.items()}
        self.assertEqual(tolerance_edges(rows,ds,1),{("A","B"),("B","C"),("C","A")})
        self.assertEqual(cycle_members(tolerance_edges(rows,ds,1)),("A","B","C"))

    def test_missing_and_too_few_objectives(self):
        with self.assertRaisesRegex(ValueError,"Missing"):
            tolerance_outcomes({"x":None},{"x":1},{"x":"higher"},0)
        with self.assertRaisesRegex(ValueError,"at least two"):
            omit_objective({},{"x":"higher","z":"higher"},"z")
        rows,ds=omit_objective({"a":{"x":3,"y":2,"z":4}},
                               {"x":"higher","y":"higher","z":"lower"},"z")
        self.assertEqual(rows,{"a":{"x":3,"y":2}})
        self.assertEqual(len(ds),2)

    def test_preference_normalization_and_known_crossing(self):
        self.assertEqual(list(normalize_weights([1,3])),[.25,.75])
        for invalid in ([0,0],[1,-1]):
            with self.assertRaises(ValueError):
                normalize_weights(invalid)
        shares, _ = analytical_weights({"a":(1,0),"b":(0,.5)})
        self.assertAlmostEqual(shares["a"],2/3)
        self.assertAlmostEqual(shares["b"],1/3)
        self.assertEqual(analytical_weights({"a":(1,0),"b":(1,0)})[0],{"a":.5,"b":.5})

    def test_seed_and_monotone_front(self):
        u={"a":(.8,.3,.6),"b":(.5,.6,.7)}
        self.assertEqual(sampled_weights(u,100,4),sampled_weights(dict(reversed(list(u.items()))),100,4))
        ds={"one":"higher","two":"lower"}
        rows={"a":{"one":3,"two":2},"b":{"one":5,"two":3}}
        self.assertEqual(fronts(rows,ds),fronts({n:{k:s**3 for k,s in v.items()} for n,v in rows.items()},ds))

    def test_effect_transformations_keep_incompatible_designs_separate(self):
        fields = ("paper_id table_id protocol_block benchmark benchmark_version split task metric unit "
                  "reference_architecture target_architecture reference_backbone target_backbone "
                  "reference_judge target_judge reference_metric_definition target_metric_definition "
                  "comparison_type target_observation_id reference_observation_id target_source_row "
                  "reference_source_row reference_score").split()
        first = dict.fromkeys(fields, "example")
        first.update(contrast_kind="baseline_relative", absolute_difference="2", difference_pp="2",
                     relative_performance_improvement_pct="4", relative_error_reduction_pct="",
                     relative_undesirable_event_reduction_pct="")
        second = {**first, "absolute_difference":"1", "difference_pp":"1"}
        self.assertEqual(len(list(effect_sensitivity([first,second]))),2)
        for field in ("comparison_type","benchmark","reference_metric_definition"):
            self.assertEqual(list(effect_sensitivity([first,{**second,field:"different"}])),[])

    def test_denominator_product(self):
        self.assertEqual(served_event_frequency(20,25),20)
        self.assertIsNone(served_event_frequency(100,None))
        self.assertIsNone(served_event_frequency(20,None))
