"""Levenshtein edit distance: minimum insertions, deletions and substitutions.

``dp[i][j]`` = distance between ``a[:i]`` and ``b[:j]``; only the previous row is kept.

Complexity (m = len(a), n = len(b)):
    Time:  O(m * n)
    Space: O(min(m, n)) for the distance; O(m * n) for the alignment script
"""

from __future__ import annotations


def edit_distance(a: str, b: str) -> int:
    """
    >>> edit_distance("kitten", "sitting")
    3
    """
    if len(a) < len(b):
        a, b = b, a  # keep the row as short as possible
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(
                prev[j] + 1,  # delete ca
                cur[j - 1] + 1,  # insert cb
                prev[j - 1] + (ca != cb),  # substitute (or match)
            )
        prev = cur
    return prev[-1]


def edit_script(a: str, b: str) -> list[str]:
    """One optimal sequence of operations turning ``a`` into ``b``.

    >>> edit_script("kitten", "sitting")
    ['sub k->s', 'keep i', 'keep t', 'keep t', 'sub e->i', 'keep n', 'insert g']
    """
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = min(
                dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + (a[i - 1] != b[j - 1])
            )
    ops: list[str] = []
    i, j = m, n
    while i or j:
        if i and j and dp[i][j] == dp[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            ops.append(
                f"keep {a[i - 1]}" if a[i - 1] == b[j - 1] else f"sub {a[i - 1]}->{b[j - 1]}"
            )
            i, j = i - 1, j - 1
        elif i and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f"delete {a[i - 1]}")
            i -= 1
        else:
            ops.append(f"insert {b[j - 1]}")
            j -= 1
    return ops[::-1]
