"""0/1 knapsack: choose items (each at most once) to maximise value within a weight limit.

``dp[w]`` = best value achievable with capacity ``w`` using the items seen so far.
Iterating ``w`` downwards ensures each item is used at most once.

Complexity (n items, capacity W):
    Time:  O(n * W)  - pseudo-polynomial
    Space: O(W) for the value; O(n * W) when reconstructing the chosen items
"""

from __future__ import annotations

from collections.abc import Sequence


def knapsack(weights: Sequence[int], values: Sequence[float], capacity: int) -> float:
    """Best total value.

    >>> knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7)
    9
    """
    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values, strict=True):
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def knapsack_items(
    weights: Sequence[int], values: Sequence[float], capacity: int
) -> tuple[float, list[int]]:
    """Best total value and the indices of the chosen items.

    >>> knapsack_items([1, 3, 4, 5], [1, 4, 5, 7], 7)
    (9, [1, 2])
    """
    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")
    n = len(weights)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for c in range(capacity + 1):
            table[i][c] = table[i - 1][c]
            if w <= c and table[i - 1][c - w] + v > table[i][c]:
                table[i][c] = table[i - 1][c - w] + v
    chosen, c = [], capacity
    for i in range(n, 0, -1):
        if table[i][c] != table[i - 1][c]:
            chosen.append(i - 1)
            c -= weights[i - 1]
    return table[n][capacity], sorted(chosen)
