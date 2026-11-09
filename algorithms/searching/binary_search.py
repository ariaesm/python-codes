"""Binary search on a sorted sequence.

Repeatedly halves the search interval ``[lo, hi)`` of a sorted sequence.

Complexity:
    Time:  O(log n)
    Space: O(1)

``lower_bound`` / ``upper_bound`` mirror :func:`bisect.bisect_left` /
:func:`bisect.bisect_right` and are the building blocks for the others.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def lower_bound(items: Sequence[Any], target: Any) -> int:
    """Index of the first element ``>= target`` (``len(items)`` if none)."""
    lo, hi = 0, len(items)
    while lo < hi:
        mid = (lo + hi) // 2
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(items: Sequence[Any], target: Any) -> int:
    """Index of the first element ``> target`` (``len(items)`` if none)."""
    lo, hi = 0, len(items)
    while lo < hi:
        mid = (lo + hi) // 2
        if target < items[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo


def binary_search(items: Sequence[Any], target: Any) -> int:
    """Return the index of ``target`` in sorted ``items`` (leftmost match), or -1.

    >>> binary_search([1, 3, 5, 7, 9], 7)
    3
    >>> binary_search([1, 3, 5, 7, 9], 4)
    -1
    """
    i = lower_bound(items, target)
    return i if i < len(items) and items[i] == target else -1


def count_occurrences(items: Sequence[Any], target: Any) -> int:
    """Number of elements equal to ``target`` in O(log n).

    >>> count_occurrences([1, 2, 2, 2, 3], 2)
    3
    """
    return upper_bound(items, target) - lower_bound(items, target)
