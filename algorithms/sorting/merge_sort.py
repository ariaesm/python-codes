"""Merge sort (top-down, stable).

Split the list in half, sort each half recursively, then merge the two sorted halves.

Complexity:
    Time:  O(n log n) in the best, average and worst case
    Space: O(n) auxiliary
    Stable: yes
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any


def merge(left: Sequence[Any], right: Sequence[Any], key: Callable[[Any], Any]) -> list[Any]:
    """Merge two sorted lists. Ties take from ``left`` first, which keeps the sort stable."""
    out: list[Any] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(right[j]) < key(left[i]):
            out.append(right[j])
            j += 1
        else:
            out.append(left[i])
            i += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def merge_sort(items: Sequence[Any], key: Callable[[Any], Any] | None = None) -> list[Any]:
    """Return a new sorted list.

    >>> merge_sort([5, 2, 9, 1, 5, 6])
    [1, 2, 5, 5, 6, 9]
    """
    k = key or (lambda x: x)
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    return merge(merge_sort(items[:mid], k), merge_sort(items[mid:], k), k)
