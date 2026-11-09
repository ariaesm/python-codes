"""Quick sort (in place, randomised pivot, Hoare partition).

Pick a random pivot, partition the slice so that everything left of the split is
``<= pivot`` and everything right is ``>= pivot``, then repeat on both sides.
An explicit stack replaces recursion: the larger side is pushed and work continues
on the smaller one, which bounds the stack to O(log n) entries.

Complexity:
    Time:  O(n log n) expected, O(n^2) worst case (vanishingly unlikely with random pivots)
    Space: O(log n) stack
    Stable: no
"""

from __future__ import annotations

import random
from typing import Any


def _partition(a: list[Any], lo: int, hi: int, rng: random.Random) -> int:
    pivot = a[rng.randint(lo, hi)]
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < pivot:
            i += 1
        j -= 1
        while pivot < a[j]:
            j -= 1
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]


def quick_sort(a: list[Any], seed: int | None = None) -> list[Any]:
    """Sort list ``a`` in place and return it.

    >>> quick_sort([3, 6, 1, 8, 2, 9, 2])
    [1, 2, 2, 3, 6, 8, 9]
    """
    rng = random.Random(seed)
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        while lo < hi:
            p = _partition(a, lo, hi, rng)
            # Defer the larger part, keep working on the smaller one.
            if p - lo < hi - p:
                stack.append((p + 1, hi))
                hi = p
            else:
                stack.append((lo, p))
                lo = p + 1
    return a
