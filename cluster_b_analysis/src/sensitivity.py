"""Stage 2D descriptive stress tests. Run as a module from the repository root."""
from collections import defaultdict
from decimal import Decimal
from itertools import combinations
import json
from math import isfinite

import numpy as np

from .data_loading import ROOT, read_score
from .failure_mode_analysis import write_rows
from .pareto import fronts, orient
from .stage2c_analysis import PANELS, read

TOLERANCES = ("0", "0.5", "1", "2", "5")


def tolerance_outcomes(left, right, directions, tolerance):
    a, b = orient(left, directions), orient(right, directions)
    t = read_score(tolerance)
    if t is None or t < 0:
        raise ValueError("Tolerance must be nonnegative")
    diffs = [x - y for x, y in zip(a, b)]
    wins = sum(d > t for d in diffs)
    losses = sum(d < -t for d in diffs)
    return wins, len(diffs) - wins - losses, losses


def tolerance_edges(vectors, directions, tolerance):
    edges = set()
    for a, b in combinations(sorted(vectors), 2):
        wins, _, losses = tolerance_outcomes(vectors[a], vectors[b], directions, tolerance)
        if wins and not losses:
            edges.add((a, b))
        if losses and not wins:
            edges.add((b, a))
    return edges


def cycle_members(edges):
    """Return vertices with a directed path back to themselves."""
    outbound = defaultdict(set)
    for a, b in edges:
        outbound[a].add(b)
    cyclic = set()
    for start in list(outbound):
        visited = set()
        pending = list(outbound[start])
        while pending:
            point = pending.pop()
            if point == start:
                cyclic.add(start)
                break
            if point not in visited:
                visited.add(point)
                pending.extend(outbound[point])
    return tuple(sorted(cyclic))


def omit_objective(vectors, directions, objective):
    if objective not in directions or len(directions) < 3:
        raise ValueError("Objective removal requires at least two remaining objectives")
    remaining = {k: v for k, v in directions.items() if k != objective}
    return {name: {k: scores[k] for k in remaining} for name, scores in vectors.items()}, remaining


def normalize_weights(weights):
    values = np.asarray(weights, dtype=float)
    if values.ndim != 1 or not values.size or not all(isfinite(v) and v >= 0 for v in values):
        raise ValueError("Weights must be a finite nonnegative vector")
    total = values.sum()
    if not isfinite(total) or total <= 0:
        raise ValueError("Weights need positive finite mass")
    return values / total


def percentage_utilities(vectors, directions):
    """Fixed natural-scale utilities, in [0,1], for declared 0–100 objectives."""
    result = {}
    for name, scores in vectors.items():
        adjusted = orient(scores, directions)
        if any(not 0 <= read_score(v) <= 100 for v in scores.values()):
            raise ValueError("Preference analysis requires bounded percentage scores")
        result[name] = tuple(float((x if d == "higher" else 100+x)/100)
                             for x,d in zip(adjusted, directions.values()))
    return result


def analytical_weights(utilities):
    """Uniform first-objective weight on [0,1], split weight of exact ties."""
    lines = {k: (Decimal(str(x))-Decimal(str(y)), Decimal(str(y))) for k,(x,y) in utilities.items()}
    breaks = {Decimal(0), Decimal(1)}
    for (a,b),(c,d) in combinations(lines.values(),2):
        if a != c:
            z = (d-b)/(a-c)
            if 0 < z < 1:
                breaks.add(z)
    shares = dict.fromkeys(lines, Decimal(0))
    intervals = []
    ordered = sorted(breaks)
    for lo, hi in zip(ordered, ordered[1:]):
        mid = (lo+hi)/2
        scores = {k: a*mid+b for k,(a,b) in lines.items()}
        winners = tuple(sorted(k for k in scores if scores[k] == max(scores.values())))
        for winner in winners:
            shares[winner] += (hi-lo)/len(winners)
        if intervals and intervals[-1][2] == winners:
            intervals[-1] = (intervals[-1][0], hi, winners)
        else:
            intervals.append((lo,hi,winners))
    return {k: float(v) for k,v in shares.items()}, intervals


def sampled_weights(utilities, samples=4000, seed=27):
    """Uniform simplex preference sample (Dirichlet unit concentrations)."""
    names = sorted(utilities)
    data = np.asarray([utilities[k] for k in names])
    weights = np.random.default_rng(seed).dirichlet(np.ones(data.shape[1]), size=samples)
    scores = weights @ data.T
    ties = np.isclose(scores, scores.max(axis=1, keepdims=True), atol=1e-12, rtol=0)
    return dict(zip(names, (ties/ties.sum(axis=1, keepdims=True)).mean(axis=0)))


def served_event_frequency(abstain_percent, conditional_percent):
    a, u = map(read_score, (abstain_percent, conditional_percent))
    if a is None or u is None:
        return None
    if not 0 <= a <= 100 or not 0 <= u <= 100:
        raise ValueError("Rates must be percentages")
    # Conditional rate is defined in the table; an entirely unserved cohort has
    # no verifiable conditional denominator.
    return (100-a)*u/100 if a < 100 else None


def load_panels(rows):
    """Verify Stage 2C coverage and keep benchmark/reader/split boundaries intact."""
    panels = defaultdict(dict)
    metadata = {}
    specifications = {p.id: p for p in PANELS}
    from .stage2c_analysis import objective
    directions = {p.id: {objective(t,m):d for t,m,d in p.objectives} for p in PANELS}
    for row in rows:
        panel, name = row["panel"], row["configuration_id"]
        spec = specifications[panel]
        if (row["paper_id"], row["source_table"], row["protocol_block"]) != (spec.paper, spec.table, spec.block):
            raise ValueError(f"Unmatched panel source {panel}")
        if name in panels[panel] or set(json.loads(row["units"]).values()) != {"percent"}:
            raise ValueError(f"Duplicate vector or incompatible units {panel}")
        scores = json.loads(row["scores_in_original_units"])
        orient(scores, directions[panel])
        panels[panel][name] = scores
        metadata[panel,name] = row
    for panel, vectors in panels.items():
        conditions = {(metadata[panel,n]["benchmark"], metadata[panel,n]["benchmark_version"],
                       metadata[panel,n]["split"], metadata[panel,n]["backbone"]) for n in vectors}
        if len(conditions) != 1:
            raise ValueError(f"Incompatible conditions in {panel}")
        for index, group in enumerate(fronts(vectors, directions[panel]), 1):
            if any(int(metadata[panel,n]["front"]) != index for n in group):
                raise ValueError(f"Saved fronts do not reproduce for {panel}")
    if panels.keys() != specifications.keys():
        raise ValueError("Missing reviewed panel")
    return panels, directions, metadata


def compare_effects(a, b, field, scope):
    sign = lambda x: (x > 0) - (x < 0)
    raw = sign(read_score(a["absolute_difference"]) - read_score(b["absolute_difference"]))
    adjusted = sign(read_score(a[field]) - read_score(b[field]))
    return {**{k:a[k] for k in ("paper_id","protocol_block","benchmark","task","metric","unit",
                              "target_architecture","reference_architecture","comparison_type")},
            "scope": scope, "transformation":field, "raw_order":raw, "transformed_order":adjusted,
            "status":"reversal" if raw*adjusted < 0 else "tie changed" if raw != adjusted else "preserved",
            **{f"{side}_{k}":r[k] for side,r in (("first",a),("second",b)) for k in (
                "target_observation_id","reference_observation_id","target_source_row","reference_source_row",
                "absolute_difference","reference_score","protocol_block")},
            "first_transformed": a[field], "second_transformed": b[field]}


def effect_sensitivity(rows):
    groups = defaultdict(list)
    for r in rows:
        if r["contrast_kind"] != "baseline_relative":
            continue
        key = tuple(r[k] for k in ("paper_id", "table_id", "protocol_block", "benchmark", "benchmark_version",
                                   "split", "task", "metric", "unit", "reference_architecture",
                                   "target_architecture", "reference_backbone", "target_backbone",
                                   "reference_judge", "target_judge", "reference_metric_definition",
                                   "target_metric_definition", "comparison_type"))
        groups[key].append(r)
    for group in groups.values():
        for field in ("difference_pp", "relative_performance_improvement_pct",
                      "relative_error_reduction_pct", "relative_undesirable_event_reduction_pct"):
            common = [r for r in group if r[field] and r["absolute_difference"]]
            for a,b in combinations(common,2):
                yield compare_effects(a,b,field,"within compatible contrast stratum")


def run(root=ROOT):
    result = root/"results"
    panels, directions, meta = load_panels(read(result/"pareto_fronts.csv"))
    observations = {r["observation_id"]:r for r in read(root/"data"/"validated_results.csv")}
    tolerance_rows, objective_rows, weights_rows, events, evidence, claims = [], [], [], [], [], []

    def claim(panel, title, ids, tests, outcome, limit):
        claims.append({"panel":panel, "claim":title, "supporting_observations":ids,
                       "checks":tests, "outcome":outcome, "limitation":limit})

    for panel, vectors in panels.items():
        ds = directions[panel]
        name = lambda n: meta[panel,n]["system"]
        ids = lambda n: json.loads(meta[panel,n]["source_observation_ids"])
        base = tolerance_edges(vectors,ds,0)
        stable = set(base)
        for t in TOLERANCES:
            edges = tolerance_edges(vectors,ds,t)
            stable.intersection_update(edges)
            cyclic = cycle_members(edges)
            nontransitive = sorted((a,b,c) for a,b in edges for d,c in edges
                                   if b == d and a != c and (a,c) not in edges)
            for a,b in combinations(sorted(vectors),2):
                w,k,l = tolerance_outcomes(vectors[a],vectors[b],ds,t)
                tolerance_rows.append({"panel":panel,"tolerance_pp":t,"left":name(a),"right":name(b),
                                       "left_config":a,"right_config":b,"wins":w,"ties":k,"losses":l,
                                       "dominance":"left" if (a,b) in edges else "right" if (b,a) in edges else "none",
                                       "edge_count":len(edges),"cycle_members":cyclic,"nontransitive_chain_count":len(nontransitive),
                                       "example_nontransitive_chain":nontransitive[0] if nontransitive else ()})
        for a,b in sorted(base):
            claim(panel, f"{name(a)} dominates {name(b)} at printed values", [ids(a),ids(b)],
                  "0, 0.5, 1, 2 and 5 pp", "robust across tolerances" if (a,b) in stable else "tolerance-sensitive",
                  "Within-panel point estimates; no sampling claim")

        baseline_front = fronts(vectors,ds)[0]
        for drop in ds:
            info = {"panel":panel,"removed_objective":drop,"full_first_front":[name(n) for n in baseline_front]}
            if len(ds) == 2:
                objective_rows.append({**info,"status":"omitted: one objective would remain"})
                continue
            reduced, reduced_ds = omit_objective(vectors,ds,drop)
            front = fronts(reduced,reduced_ds)[0]
            reduced_edges = tolerance_edges(reduced,reduced_ds,0)
            objective_rows.append({**info,"status":"evaluated","first_front":[name(n) for n in front],
                                   "new_front_members":[name(n) for n in sorted(set(front)-set(baseline_front))],
                                   "lost_front_members":[name(n) for n in sorted(set(baseline_front)-set(front))],
                                   "dominance_added":len(reduced_edges-base),"dominance_lost":len(base-reduced_edges)})
        utilities = percentage_utilities(vectors,ds)
        intervals = []
        if len(ds) == 2:
            shares, intervals = analytical_weights(utilities)
        else:
            shares = sampled_weights(utilities)
        for n, share in sorted(shares.items()):
            weights_rows.append({"panel":panel,"system":name(n),"configuration_id":n,"share":share,
                                 "method":"analytic uniform weight" if intervals else "Dirichlet(1,...,1)",
                                 "objectives":list(ds),"normalized_utilities":utilities[n],
                                 "draws":"" if intervals else 4000,"seed":"" if intervals else 27,
                                 "winning_weight_intervals":[[str(lo),str(hi),list(w)] for lo,hi,w in intervals if n in w]})
        source = meta[panel, next(iter(vectors))]
        evidence += [
            {"panel":panel,"scenario":"strict","status":"evaluated","systems":len(vectors),
             "first_front":[name(n) for n in baseline_front]},
            {"panel":panel,"scenario":"remove contributing study, benchmark or cohort",
             "status":"panel loses all support", "removed_study":source["paper_id"],
             "removed_benchmark":source["benchmark"],"removed_cohort":source["cohort"],
             "reason":"No aligned replacement or valid pooled estimate"},
        ]
        if panel.startswith(("sirin","halumem")):
            evidence.append({"panel":panel,"scenario":"direct rubric endpoint only",
                             "status":"single endpoint, no multiobjective frontier",
                             "reason":"Retains conditional strict unfaithfulness or benchmark-labeled hallucination only"})
        else:
            evidence.append({"panel":panel,"scenario":"direct rubric endpoint only","status":"no eligible objective",
                             "reason":("IMLogic fabrication traps are forced-choice diagnostics, not open-generation hallucination rates"
                                       if panel == "imlogic-conversation" else "Selected BioMem QA scores are memory-performance proxies")})
        if panel.startswith("sirin"):
            for n,v in vectors.items():
                source_ids = ids(n)
                selected = [observations[source_ids[k]] for k in ds]
                sizes = {r["sample_size"] for r in selected}
                compatible = (len(sizes) == 1 and "" not in sizes and
                              "among served answers" in selected[1]["metric_definition"] and
                              "Share of evaluation queries abstained on" == selected[2]["metric_definition"])
                if not compatible:
                    raise ValueError("Unverified SIRIN event-rate denominator")
                vals = [v[k] for k in ds]
                events.append({"panel":panel,"configuration_id":n,"system":name(n),
                               "cohort_size":selected[0]["sample_size"],"served_accuracy_pct":vals[0],
                               "conditional_unfaithful_pct":vals[1],"abstain_pct":vals[2],
                               "coverage_pct":100-read_score(vals[2]),
                               "assumption_conditional_unfaithful_answer_pct_all_queries":served_event_frequency(vals[2],vals[1]),
                               "denominator_status":"Shared cohort verified; identical scorer inclusion and weighting unverified",
                               "verified_empirical_all_query_rate":"",
                               "source_observation_ids":source_ids,
                               "limitation":"Scenario assumes the conditional rate weights all served queries consistently with coverage. Rounded rates; no joint uncertainty."})
    panel = "halumem-long"
    extra = {f"{r['task']} / {r['metric']}":r["score"] for r in observations.values()
             if r["paper_id"]=="halumem" and r["table_id"]=="Table 3" and r["block_id"]=="halumem-long-original"
             and r["architecture"]=="Memobase" and f"{r['task']} / {r['metric']}" in directions[panel]}
    relaxed = {**panels[panel], "Memobase (conditional)":extra}
    evidence.append({"panel":panel,"scenario":"relaxed: include conditionally comparable Memobase",
                     "status":"exploratory","systems":len(relaxed),
                     "first_front":[meta[panel,n]["system"] if n in panels[panel] else n
                                    for n in fronts(relaxed,directions[panel])[0]],
                     "reason":"Source category nonclosure and method-specific 500-token retrieval cap; no eligibility upgrade"})
    claim(panel, "MemOS remains first-front when Memobase is added", [
          [r["observation_id"] for r in observations.values()
           if r["paper_id"]=="halumem" and r["table_id"]=="Table 3" and r["block_id"]=="halumem-long-original"
           and r["architecture"] in {"MemOS","Memobase"} and f"{r['task']} / {r['metric']}" in directions[panel]]],
          "strict and exploratory conditional Memobase", "robust to this inclusion scenario",
          "Conditional source nonclosure remains; no generalization across splits")
    evidence.append({"panel":"all","scenario":"pooled leave-one-study/benchmark-out",
                     "status":"unsupported","reason":"Stage 2B has no compatible pooled comparison"})
    evidence.append({"panel":"all","scenario":"other relaxed cross-protocol candidates",
                     "status":"not combined","reason":"Different systems, backbones, benchmarks, scoring or cohorts; missing vectors or unresolved compatibility"})

    matched = read(result/"matched_effect_sizes.csv")
    effects = list(effect_sensitivity(matched))
    both = sorted((r for r in matched if r["paper_id"] == "sirin" and r["table_id"] == "Table 8"
                   and r["task"] == "Overall" and r["metric"] == "Served accuracy"
                   and r["contrast_kind"] == "baseline_relative"
                   and "SIRIN Judge | + Both gates" in r["target_source_row"]),
                  key=lambda r:r["target_architecture"])
    if len(both) != 2:
        raise ValueError("Expected two separately matched SIRIN accuracy contrasts")
    scope = "Cross-framework normalization illustration only; separate within-framework effects"
    for field in ("difference_pp","relative_performance_improvement_pct","relative_error_reduction_pct"):
        effects.append(compare_effects(*both,field,scope))
    claim("sirin-mem0 and sirin-lightmem","Relative performance reverses the order of the two gain magnitudes",
          [{k:r[k] for k in ("target_observation_id","reference_observation_id")} for r in both],
          "Percentage points, relative performance and relative error",
          "normalization-sensitive", "Different baselines and served subsets; no architecture ranking")
    for panel in panels:
        rows = [r for r in weights_rows if r["panel"] == panel and r["share"] > 0]
        source_ids = [json.loads(meta[panel,r["configuration_id"]]["source_observation_ids"]) for r in rows]
        claim(panel, "Preferred configurations under the tested weights", source_ids,
              rows[0]["method"], "preference-sensitive" if len(rows) > 1 else "one positive-share winner",
              "Fixed percentage utilities and hypothetical preferences; not a superiority probability")
    claim("sirin-mem0 and sirin-lightmem", "An empirical all-query unfaithful-answer frequency is unverified",
          [r["source_observation_ids"] for r in events], "Common source cohort and scored denominator audit",
          "unsupported without shared scorer inclusion and weighting",
          "The rounded-rate products are illustrative scenarios. Abstentions are not counted as correct.")

    for filename, rows in (
        ("tolerance_sensitivity",tolerance_rows),("objective_selection_sensitivity",objective_rows),
        ("objective_weight_sensitivity",weights_rows),("effect_size_sensitivity",effects),
        ("evidence_selection_sensitivity",evidence),("sirin_denominator_sensitivity",events),
        ("robust_findings",claims),
    ):
        write_rows(result/f"{filename}.csv",rows)
    from .stage2d_figures import render
    render(root/"figures",tolerance_rows,weights_rows,events)
    print(f"{len(tolerance_rows)} tolerance comparisons, {len(objective_rows)} objective omissions, "
          f"{len(weights_rows)} preference rows, {len(effects)} transformation checks, {len(events)} SIRIN products")


if __name__ == "__main__":
    run()
