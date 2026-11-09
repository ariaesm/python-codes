"""Sliding-window technique.

Maintain a window ``[left, right]`` over a sequence and move both ends forward only,
so every element enters and leaves the window at most once.

Complexity: O(n) time for every function below.
Space: O(1), except where noted.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Sequence


def max_sum_subarray(nums: Sequence[float], k: int) -> float:
    """Maximum sum of any contiguous window of exactly ``k`` elements (fixed window).

    >>> max_sum_subarray([2, 1, 5, 1, 3, 2], 3)
    9
    """
    if not 0 < k <= len(nums):
        raise ValueError("k must be between 1 and len(nums)")
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best


def longest_unique_substring(s: str) -> str:
    """Longest substring without repeating characters (variable window).

    Space: O(alphabet) for the last-seen map.

    >>> longest_unique_substring("abcabcbb")
    'abc'
    >>> longest_unique_substring("pwwkew")
    'wke'
    """
    last: dict[str, int] = {}
    left = best_start = best_len = 0
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:
            left = last[ch] + 1
        last[ch] = right
        if right - left + 1 > best_len:
            best_start, best_len = left, right - left + 1
    return s[best_start : best_start + best_len]


def min_subarray_len(target: float, nums: Sequence[float]) -> int:
    """Length of the shortest contiguous subarray with sum >= ``target`` (0 if none).

    Requires non-negative numbers (shrinking the window must never increase the sum).

    >>> min_subarray_len(7, [2, 3, 1, 2, 4, 3])
    2
    """
    if any(x < 0 for x in nums):
        raise ValueError("nums must be non-negative")
    left = 0
    total = 0.0
    best = len(nums) + 1
    for right, x in enumerate(nums):
        total += x
        while total >= target and left <= right:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best > len(nums) else best


def sliding_window_max(nums: Sequence[float], k: int) -> list[float]:
    """Maximum of every window of size ``k`` using a monotonic deque.

    Space: O(k) for the deque.

    >>> sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
    [3, 3, 5, 5, 6, 7]
    """
    if not 0 < k <= len(nums):
        raise ValueError("k must be between 1 and len(nums)")
    dq: deque[int] = deque()  # indices, values strictly decreasing
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
