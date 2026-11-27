"""Descriptive aggregation of matched contrasts within declared estimands."""

from collections import defaultdict
from math import fsum
from statistics import fmean, mean

from .data_loading import read_score


def contrast_availability(score, baseline, ceiling):
    """Fraction of available gain for a bounded, higher-is-better outcome.

    The caller supplies the justified attainable ceiling for this metric. A
    missing score or a baseline at the ceiling leaves the fraction undefined.
    A deterioration yields a negative fraction.
    """
    score, baseline, ceiling = map(read_score, (score, baseline, ceiling))
    if None in (score, baseline, ceiling):
        return None
    if max(score, baseline) > ceiling:
        raise ValueError("Scores cannot exceed the attainable ceiling")
    if baseline == ceiling:
        return None
    return float((score - baseline) / (ceiling - baseline))


def _source_support(pairs):
    return {
        "n_source_pairs": len(pairs),
        "n_source_observations": len({observation for pair in pairs for observation in pair}),
        "observation_pairs": tuple(sorted(pairs)),
    }


def _support(protocol_rows):
    cohorts = tuple(sorted({row["cohort"] for row in protocol_rows}))
    studies = tuple(sorted({row["study"] for row in protocol_rows}))
    protocols = tuple(sorted((row["study"], row["protocol"]) for row in protocol_rows))
    pairs = {pair for row in protocol_rows for pair in row["observation_pairs"]}
    return {
        "n_cohorts": len(cohorts),
        "n_studies": len(studies),
        "n_protocols": len(protocols),
        "n_observations": sum(row["n_observations"] for row in protocol_rows),
        "cohorts": cohorts,
        "studies": studies,
        "protocols": protocols,
        **_source_support(pairs),
    }


def aggregate(rows):
    """Return protocol, cohort and profile summaries, respectively.

    A row supplies stratum, study, cohort, protocol, endpoint, effect,
    target_observation_id and reference_observation_id. The caller defines each
    stratum as a scientifically compatible estimand, including the benchmark,
    outcome, evidence type, effect scale and reference context. Endpoint is the
    hashable semantic contrast identity within that stratum and study protocol.

    Each protocol mean gives equal weight to its distinct endpoints. A cohort
    or study mean gives equal weight to its contributing protocols. Profile
    means give equal weight to the units named by the weighting scheme.
    n_observations counts retained matched endpoints. Source pairs and unique
    source observations have separate counts. Provenance lists are sorted, with
    pairs ordered target first and protocol keys ordered study first.
    """
    identifiers = ("stratum", "study", "cohort", "protocol", "target_observation_id",
                   "reference_observation_id")
    cohort_by_protocol = {}
    directed_edges = {}
    blocks = defaultdict(dict)
    for row in rows:
        effect = read_score(row["effect"])
        if effect is None:
            continue
        values = tuple(row[field] for field in identifiers)
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError("Each contributing contrast requires nonblank string identifiers")
        stratum, study, cohort, protocol, target, reference = values
        endpoint = row["endpoint"]
        if not endpoint or target == reference:
            raise ValueError("A contrast needs an endpoint and distinct target and reference IDs")

        study_protocol = (study, protocol)
        if cohort_by_protocol.setdefault(study_protocol, cohort) != cohort:
            raise ValueError(f"Protocol {study_protocol!r} has conflicting cohort assignments")

        pair = (target, reference)
        edge_key = (stratum, *sorted(pair))
        edge_signature = (pair, study_protocol, endpoint, effect)
        if directed_edges.setdefault(edge_key, edge_signature) != edge_signature:
            raise ValueError(f"Conflicting or reversed source pair {edge_key[1:]!r} in {stratum!r}")

        block_key = (stratum, *study_protocol)
        previous_effect, endpoint_pairs = blocks[block_key].setdefault(endpoint, (effect, set()))
        if effect != previous_effect:
            raise ValueError(f"Conflicting effects for endpoint {endpoint!r} in {block_key!r}")
        endpoint_pairs.add(pair)

    protocol_rows = []
    protocols_by_cohort = defaultdict(list)
    protocols_by_stratum = defaultdict(list)
    for (stratum, study, protocol), endpoints in sorted(blocks.items()):
        cohort = cohort_by_protocol[study, protocol]
        pairs = {pair for _, endpoint_pairs in endpoints.values() for pair in endpoint_pairs}
        summary = {
            "stratum": stratum,
            "study": study,
            "cohort": cohort,
            "protocol": protocol,
            "effect": float(mean(effect for effect, _ in endpoints.values())),
            "n_observations": len(endpoints),
            "n_protocols": 1,
            "n_studies": 1,
            "n_cohorts": 1,
            **_source_support(pairs),
        }
        protocol_rows.append(summary)
        protocols_by_cohort[stratum, cohort].append(summary)
        protocols_by_stratum[stratum].append(summary)

    cohort_rows = []
    cohorts_by_stratum = defaultdict(list)
    for (stratum, cohort), protocols in sorted(protocols_by_cohort.items()):
        summary = {
            "stratum": stratum,
            "cohort": cohort,
            "effect": fmean(row["effect"] for row in protocols),
            **_support(protocols),
        }
        cohort_rows.append(summary)
        cohorts_by_stratum[stratum].append(summary)

    profile_rows = []
    for stratum, protocols in sorted(protocols_by_stratum.items()):
        effects_by_study = defaultdict(list)
        for protocol in protocols:
            effects_by_study[protocol["study"]].append(protocol["effect"])
        protocol_effects = [protocol["effect"] for protocol in protocols]
        support = _support(protocols)
        observation_effect_sum = fsum(row["effect"] * row["n_observations"] for row in protocols)
        profile_rows.append({
            "stratum": stratum,
            "cohort_balanced_mean": fmean(row["effect"] for row in cohorts_by_stratum[stratum]),
            "protocol_weighted_mean": fmean(protocol_effects),
            "study_balanced_mean": fmean(fmean(effects) for effects in effects_by_study.values()),
            "observation_weighted_mean": observation_effect_sum / support["n_observations"],
            **support,
        })
    return protocol_rows, cohort_rows, profile_rows
