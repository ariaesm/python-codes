import bisect
import random

import pytest

from algorithms.searching.binary_search import (
    binary_search,
    count_occurrences,
    lower_bound,
    upper_bound,
)


def test_empty():
    assert binary_search([], 1) == -1
    assert count_occurrences([], 1) == 0


@pytest.mark.parametrize("target", [-1, 0, 1, 2, 3, 4, 5, 6])
def test_matches_bisect(target):
    items = [0, 1, 1, 3, 3, 3, 5]
    assert lower_bound(items, target) == bisect.bisect_left(items, target)
    assert upper_bound(items, target) == bisect.bisect_right(items, target)


def test_leftmost_match_and_random():
    rng = random.Random(0)
    for _ in range(200):
        items = sorted(rng.randint(0, 30) for _ in range(rng.randint(0, 40)))
        t = rng.randint(-2, 32)
        i = binary_search(items, t)
        if t in items:
            assert i == items.index(t)
        else:
            assert i == -1
        assert count_occurrences(items, t) == items.count(t)


def test_works_with_strings():
    assert binary_search(["ant", "bee", "cat"], "cat") == 2
