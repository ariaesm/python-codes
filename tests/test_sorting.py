import random

import pytest

from algorithms.sorting.merge_sort import merge_sort
from algorithms.sorting.quick_sort import quick_sort

CASES = [[], [1], [2, 1], [3, 3, 3], list(range(50)), list(range(50, 0, -1)), [5, -2, 0, 9, -2]]


@pytest.mark.parametrize("data", CASES)
def test_merge_sort_cases(data):
    original = list(data)
    assert merge_sort(data) == sorted(data)
    assert data == original  # does not mutate input


@pytest.mark.parametrize("data", CASES)
def test_quick_sort_cases(data):
    assert quick_sort(list(data), seed=1) == sorted(data)


def test_random_lists():
    rng = random.Random(42)
    for _ in range(200):
        data = [rng.randint(-100, 100) for _ in range(rng.randint(0, 100))]
        assert merge_sort(data) == sorted(data)
        assert quick_sort(list(data)) == sorted(data)


def test_merge_sort_is_stable():
    pairs = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]
    assert merge_sort(pairs, key=lambda p: p[0]) == [(1, "b"), (1, "d"), (2, "a"), (2, "c")]


def test_quick_sort_in_place_large_with_duplicates():
    data = [random.Random(3).randint(0, 3) for _ in range(5000)]
    expected = sorted(data)
    quick_sort(data)
    assert data == expected
