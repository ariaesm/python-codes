"""Union-find (disjoint set union) with path compression and union by size.

Complexity:
    find / union / connected: O(α(n)) amortised - inverse Ackermann, effectively constant
    Space: O(n)
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable


class UnionFind:
    """
    >>> uf = UnionFind(range(5))
    >>> uf.union(0, 1); uf.union(3, 4)
    True
    True
    >>> uf.connected(0, 1), uf.connected(1, 3), uf.count
    (True, False, 3)
    """

    def __init__(self, items: Iterable[Hashable] = ()) -> None:
        self._parent: dict[Hashable, Hashable] = {}
        self._size: dict[Hashable, int] = {}
        self.count = 0  # number of disjoint sets
        for x in items:
            self.add(x)

    def add(self, x: Hashable) -> None:
        if x not in self._parent:
            self._parent[x] = x
            self._size[x] = 1
            self.count += 1

    def find(self, x: Hashable) -> Hashable:
        """Representative of ``x``'s set. Unknown items are added as singletons."""
        self.add(x)
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != root:  # path compression
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a: Hashable, b: Hashable) -> bool:
        """Merge the sets of ``a`` and ``b``. Returns False if they were already joined."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self._size[ra] < self._size[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        self._size[ra] += self._size[rb]
        self.count -= 1
        return True

    def connected(self, a: Hashable, b: Hashable) -> bool:
        return self.find(a) == self.find(b)

    def set_size(self, x: Hashable) -> int:
        return self._size[self.find(x)]


def kruskal(n: int, edges: Iterable[tuple[int, int, float]]) -> tuple[float, list[tuple]]:
    """Minimum spanning tree/forest of nodes ``0..n-1`` - a classic union-find application.

    O(E log E) for sorting the edges.

    >>> kruskal(4, [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 1)])
    (4, [(0, 1, 1), (2, 3, 1), (1, 2, 2)])
    """
    uf = UnionFind(range(n))
    total, tree = 0, []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if uf.union(u, v):
            total += w
            tree.append((u, v, w))
    return total, tree
