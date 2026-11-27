"""Descriptive competition ranks and objective disagreements within one panel."""
from itertools import combinations

from .pareto import orient


def rankings(vectors, directions):
    """Give exact ties the same rank, skipping the ranks they occupy (1,1,3)."""
    adjusted = {name: orient(vector, directions) for name, vector in vectors.items()}
    return {
        objective: {
            name: 1 + sum(another[index] > values[index] for another in adjusted.values())
            for name, values in sorted(adjusted.items())
        }
        for index, objective in enumerate(directions)
    }


def pair_outcomes(left, right, directions):
    a, b = orient(left, directions), orient(right, directions)
    wins = tuple(k for k, x, y in zip(directions, a, b) if x > y)
    ties = tuple(k for k, x, y in zip(directions, a, b) if x == y)
    losses = tuple(k for k, x, y in zip(directions, a, b) if x < y)
    return wins, ties, losses


def rank_reversals(vectors, directions):
    """List pairs with opposite preference on two objectives. Ties do not reverse."""
    for a, b in combinations(sorted(vectors), 2):
        wins, _, losses = pair_outcomes(vectors[a], vectors[b], directions)
        for win in wins:
            for loss in losses:
                yield a, b, win, loss
