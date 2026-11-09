"""Longest strictly increasing subsequence (LIS).

Two approaches:

* ``lis_length_quadratic`` - the textbook DP, ``dp[i]`` = LIS ending at ``i``. O(n^2).
* ``longest_increasing_subsequence`` - patience sorting with binary search:
  ``tails[k]`` is the smallest tail of any increasing subsequence of length ``k + 1``.
  O(n log n) time, O(n) space, and reconstructs an actual subsequence.
"""

from __future__ import annotations

from bisect import bisect_left
from collections.abc import Sequence
from typing import Any


def lis_length_quadratic(nums: Sequence[Any]) -> int:
    """Length of the LIS using the O(n^2) DP.

    >>> lis_length_quadratic([10, 9, 2, 5, 3, 7, 101, 18])
    4
    """
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp, default=0)


def longest_increasing_subsequence(nums: Sequence[Any]) -> list[Any]:
    """One longest strictly increasing subsequence, in O(n log n).

    >>> longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
    [2, 3, 7, 18]
    """
    tails: list[Any] = []  # tail values
    tail_idx: list[int] = []  # index in nums of each tail
    prev = [-1] * len(nums)
    for i, x in enumerate(nums):
        k = bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
            tail_idx.append(i)
        else:
            tails[k] = x
            tail_idx[k] = i
        prev[i] = tail_idx[k - 1] if k > 0 else -1
    out = []
    i = tail_idx[-1] if tail_idx else -1
    while i != -1:
        out.append(nums[i])
        i = prev[i]
    return out[::-1]
