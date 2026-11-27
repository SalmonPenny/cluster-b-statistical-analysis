import unittest

from cluster_b_analysis.src.failure_mode_analysis import (
    FailureMode, compatibility_audit, context_for, effect_value, failure_mode, mapped_failure, measurement,
    scope, stratum_id,
)


def source(**kwargs):
    row = dict.fromkeys((
        "architecture", "configuration_id", "architecture_version", "rq2_category",
        "metric_definition", "backbone", "judge", "hallucination_measurement", "judging_protocol",
        "retrieval_budget", "memory_budget", "context_budget", "mechanisms", "source_row",
    ), "")
    row.update(benchmark="LoCoMo", task="Adversarial", metric="Accuracy", paper_id="memguard",
               architecture="MemGuard", configuration_id="configured", role="proposed",
               hallucination_measurement="proxy")
    row.update(kwargs)
    return row


class FailureModeTests(unittest.TestCase):
    def test_benchmark_specific_assignment_and_abstention(self):
        self.assertEqual(failure_mode("LoCoMo", "Adversarial", "LLM-Judge").label, "False-premise rejection")
        self.assertEqual(failure_mode("LoCoMo-Plus", "cognitive-awareness",
                                      "Constraint-consistency judge score").label, "Latent constraint application")
        self.assertIsNone(failure_mode("LoCoMo", "overall", "LLM-Judge"))
        self.assertIsNone(mapped_failure(source(task="overall", metric="Answer F1")))
        self.assertIsNotNone(mapped_failure(source(paper_id="memorybench", task="overall", metric="Answer F1")))
        self.assertIsNone(failure_mode("LongMemEval", "Overall", "Served accuracy"))

    def test_retrieval_and_source_measurement_are_distinct(self):
        recall = source(benchmark="RealMem", metric="Memory Recall", task="Temporal reasoning",
                        paper_id="biomem", hallucination_measurement="n/a")
        mapped = mapped_failure(recall)
        self.assertEqual(mapped.label, "Evidence retrieval")
        self.assertTrue(mapped.mapping_task.startswith("Medical subset"))
        self.assertEqual(measurement(recall, recall, mapped), "memory-performance proxy")
        bad_event = source(metric="Strict unfaithfulness", hallucination_measurement="direct")
        refusal = source(hallucination_measurement="direct")
        self.assertNotEqual(measurement(bad_event, bad_event, mapped), measurement(refusal, refusal, mapped))

    def test_compatibility_requires_exact_system_context_outcome_and_protocol(self):
        fields = ("paper_id", "table_id", "benchmark", "benchmark_version", "split", "task", "metric",
                  "unit", "direction", "comparison_type", "protocol_block")
        effect = dict.fromkeys(fields, "")
        effect.update(benchmark="LoCoMo", metric="Accuracy", unit="percent",
                      comparison_type="evaluated systems", protocol_block="P")
        target = source()
        ref = source(architecture="RAG", role="baseline", configuration_id="control")
        mode = FailureMode("False-premise rejection", "Adversarial")
        identify = lambda e, t, r: stratum_id(context_for(e, t, r, mode, "baseline_relative"))
        key = identify(effect, target, ref)
        for field, value in (("benchmark", "LongMemEval"), ("metric", "LLM-Judge"),
                             ("protocol_block", "Q"), ("unit", "proportion"),
                             ("comparison_type", "controlled variant")):
            self.assertNotEqual(key, identify({**effect, field: value}, target, ref))
        for field, value in (("configuration_id", "variant"), ("judge", "different judge"),
                             ("retrieval_budget", "top 10"), ("metric_definition", "different definition")):
            self.assertNotEqual(key, identify(effect, target, {**ref, field: value}))
        self.assertEqual(key, identify(dict(reversed(list(effect.items()))), target, ref))

    def test_locality_free_audit_checks_possible_cross_cohort_scopes(self):
        context = {"contrast_kind": "baseline_relative", "benchmark": "LoCoMo", "metric": "Accuracy"}
        rows = [{"stratum": key, "cohort": key, "study": key, "effect": 0} for key in ("a", "b")]
        by_stratum = {key: {**context, "paper_id": key, "protocol_block": key} for key in ("a", "b")}
        self.assertEqual(compatibility_audit(rows, by_stratum), {
            "candidate_scopes": 1, "multicontrast_scopes": 1,
            "cross_cohort_scopes": 1, "cross_study_scopes": 1})
        by_stratum["b"]["benchmark"] = "LongMemEval"
        self.assertEqual(compatibility_audit(rows, by_stratum)["cross_cohort_scopes"], 0)

    def test_halu_mem_operation_and_personalized_recall(self):
        self.assertEqual(failure_mode("HaluMem", "Memory extraction", "Weighted recall").label,
                         "Reference memory retention")
        self.assertEqual(failure_mode("HaluMem", "Memory updating", "Hallucination rate").label,
                         "Incorrect or hallucinated memory changes")
        self.assertEqual(failure_mode("PerLTQA", "Question answering", "Accuracy").label,
                         "Personalized memory recall")

    def test_pairwise_design_is_explicit_and_absence_is_not_zero(self):
        target = source(benchmark="HaluMem", task="Question answering", metric="Hallucination rate", role="baseline")
        ref = {**target, "architecture": "Zep"}
        self.assertEqual(scope(target, ref), "source_ordered_pair")
        self.assertEqual(scope({**target, "role": "ablation"}, ref), "baseline_relative")
        self.assertEqual(scope(target, target), "")
        self.assertEqual(effect_value({"difference_pp": "", "absolute_difference": "", "unit": "score"}),
                         ("score", None))
        self.assertEqual(effect_value({"difference_pp": "0.0", "absolute_difference": "0", "unit": "percent"}),
                         ("percentage points", 0.0))
