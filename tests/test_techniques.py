import random

import pytest

from algorithms.techniques.sliding_window import (
    longest_unique_substring,
    max_sum_subarray,
    min_subarray_len,
    sliding_window_max,
)


def test_max_sum_subarray():
    assert max_sum_subarray([1, -2, 3, 4], 2) == 7
    assert max_sum_subarray([5], 1) == 5
    with pytest.raises(ValueError):
        max_sum_subarray([1, 2], 3)


@pytest.mark.parametrize(
    ("s", "expected"),
    [("", ""), ("bbbb", "b"), ("abba", "ab"), ("dvdf", "vdf"), ("abcdef", "abcdef")],
)
def test_longest_unique_substring(s, expected):
    assert longest_unique_substring(s) == expected


def test_min_subarray_len():
    assert min_subarray_len(4, [1, 4, 4]) == 1
    assert min_subarray_len(100, [1, 2, 3]) == 0
    assert min_subarray_len(6, [1, 2, 3]) == 3
    with pytest.raises(ValueError):
        min_subarray_len(1, [-1, 2])


def test_sliding_window_max_against_brute_force():
    rng = random.Random(5)
    for _ in range(100):
        nums = [rng.randint(-20, 20) for _ in range(rng.randint(1, 30))]
        k = rng.randint(1, len(nums))
        brute = [max(nums[i : i + k]) for i in range(len(nums) - k + 1)]
        assert sliding_window_max(nums, k) == brute
