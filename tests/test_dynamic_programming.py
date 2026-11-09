import itertools
import random

from algorithms.dynamic_programming.edit_distance import edit_distance, edit_script
from algorithms.dynamic_programming.knapsack import knapsack, knapsack_items
from algorithms.dynamic_programming.lis import lis_length_quadratic, longest_increasing_subsequence


def brute_knapsack(weights, values, cap):
    best = 0
    for r in range(len(weights) + 1):
        for combo in itertools.combinations(range(len(weights)), r):
            if sum(weights[i] for i in combo) <= cap:
                best = max(best, sum(values[i] for i in combo))
    return best


def test_knapsack_against_brute_force():
    rng = random.Random(11)
    for _ in range(50):
        n = rng.randint(0, 8)
        w = [rng.randint(1, 10) for _ in range(n)]
        v = [rng.randint(0, 20) for _ in range(n)]
        cap = rng.randint(0, 25)
        expected = brute_knapsack(w, v, cap)
        assert knapsack(w, v, cap) == expected
        value, items = knapsack_items(w, v, cap)
        assert value == expected
        assert sum(w[i] for i in items) <= cap
        assert sum(v[i] for i in items) == value


def is_strictly_increasing_subsequence(sub, seq):
    it = iter(seq)
    return all(x in it for x in sub) and all(a < b for a, b in itertools.pairwise(sub))


def test_lis_random():
    rng = random.Random(3)
    for _ in range(200):
        nums = [rng.randint(0, 15) for _ in range(rng.randint(0, 20))]
        sub = longest_increasing_subsequence(nums)
        assert len(sub) == lis_length_quadratic(nums)
        assert is_strictly_increasing_subsequence(sub, nums)


def test_lis_edge_cases():
    assert longest_increasing_subsequence([]) == []
    assert longest_increasing_subsequence([2, 2, 2]) == [2]
    assert longest_increasing_subsequence([1, 2, 3]) == [1, 2, 3]


def apply_script(a, ops):
    out, i = [], 0
    for op in ops:
        kind = op.split()[0]
        if kind == "keep":
            out.append(a[i])
            i += 1
        elif kind == "sub":
            out.append(op[-1])
            i += 1
        elif kind == "delete":
            i += 1
        else:
            out.append(op[-1])
    return "".join(out)


def test_edit_distance_known():
    assert edit_distance("", "abc") == 3
    assert edit_distance("flaw", "lawn") == 2
    assert edit_distance("intention", "execution") == 5
    assert edit_distance("same", "same") == 0


def test_edit_script_is_optimal_and_correct():
    rng = random.Random(9)
    for _ in range(100):
        a = "".join(rng.choice("abc") for _ in range(rng.randint(0, 7)))
        b = "".join(rng.choice("abc") for _ in range(rng.randint(0, 7)))
        ops = edit_script(a, b)
        assert apply_script(a, ops) == b
        assert sum(not op.startswith("keep") for op in ops) == edit_distance(a, b)
        assert edit_distance(a, b) == edit_distance(b, a)
