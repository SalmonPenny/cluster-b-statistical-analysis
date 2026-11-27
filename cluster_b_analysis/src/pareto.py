"""Exact point-estimate Pareto comparisons of complete objective vectors."""
from collections.abc import Mapping
from itertools import combinations
from math import comb

from .data_loading import read_score


def orient(scores, directions):
    if set(scores) != set(directions) or not directions:
        raise ValueError("An objective vector must match the declared objectives")
    if any(d not in {"higher", "lower"} for d in directions.values()):
        raise ValueError("Unknown objective direction")
    result = []
    for name, direction in directions.items():
        value = read_score(scores[name])
        if value is None:
            raise ValueError(f"Missing objective {name}")
        result.append(value if direction == "higher" else -value)
    return tuple(result)


def relation(left, right, directions):
    """Weak includes equality. Standard requires one gain. Strict requires all gains."""
    a, b = orient(left, directions), orient(right, directions)
    weak = all(x >= y for x, y in zip(a, b))
    return weak, weak and a != b, all(x > y for x, y in zip(a, b))


def fronts(vectors, directions):
    """Successive point-estimate fronts in a single compatible panel."""
    remaining = {name: orient(scores, directions) for name, scores in vectors.items()}
    result = []
    while remaining:
        front = tuple(sorted(
            name for name, a in remaining.items()
            if not any(a != b and all(x <= y for x, y in zip(a, b)) for b in remaining.values())
        ))
        result.append(front)
        for name in front:
            del remaining[name]
    return result


def complete_panel(candidates: Mapping, directions, compatible):
    """Return complete vectors and evidence-based exclusions for a reviewed panel.

    Missing objectives exclude the candidate. The remaining candidates must form
    a fully compatible comparison set; callers must specify narrower panels if
    the remaining pair graph is incomplete.
    """
    vectors, excluded = {}, {}
    for name, scores in candidates.items():
        missing = sorted(k for k in directions if scores.get(k) in ("", None))
        if missing:
            excluded[name] = "Missing objectives: " + ", ".join(missing)
            continue
        orient(scores, directions)
        vectors[name] = scores
    for a, b in combinations(sorted(vectors), 2):
        if not compatible(a, b):
            raise ValueError(f"Incompatible candidates in panel: {a}, {b}")
    return vectors, excluded


def comparison_coverage(candidates, vectors):
    """Count possible unordered pairs and those admitted by complete_panel."""
    n_total, n_eligible = len(candidates), len(vectors)
    if not set(vectors) <= set(candidates):
        raise ValueError("Eligible systems must be drawn from the candidate panel")
    return {"candidate_systems": n_total, "eligible_systems": n_eligible,
            "candidate_pairs": comb(n_total, 2), "eligible_pairs": comb(n_eligible, 2)}
