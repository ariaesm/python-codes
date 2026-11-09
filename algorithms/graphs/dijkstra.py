"""Dijkstra's single-source shortest paths (non-negative edge weights).

Uses a binary heap with "lazy deletion": stale heap entries are skipped when popped
instead of being decreased in place.

Graph format: ``{node: {neighbour: weight, ...}}``.

Complexity (V vertices, E edges):
    Time:  O((V + E) log V)
    Space: O(V + E) for the heap in the worst case
"""

from __future__ import annotations

import heapq
import itertools
import math
from collections.abc import Hashable, Mapping

WeightedGraph = Mapping[Hashable, Mapping[Hashable, float]]


def dijkstra(
    graph: WeightedGraph, source: Hashable
) -> tuple[dict[Hashable, float], dict[Hashable, Hashable]]:
    """Return ``(dist, prev)``: shortest distance to every reachable node and predecessors.

    >>> g = {"A": {"B": 1, "C": 4}, "B": {"C": 2, "D": 5}, "C": {"D": 1}}
    >>> dijkstra(g, "A")[0]
    {'A': 0, 'B': 1, 'C': 3, 'D': 4}
    """
    dist: dict[Hashable, float] = {source: 0}
    prev: dict[Hashable, Hashable] = {}
    counter = itertools.count()  # tie-breaker so nodes never need to be comparable
    heap = [(0, next(counter), source)]
    done: set[Hashable] = set()
    while heap:
        d, _, node = heapq.heappop(heap)
        if node in done:
            continue
        done.add(node)
        for nxt, w in graph.get(node, {}).items():
            if w < 0:
                raise ValueError(f"negative edge weight {node!r}->{nxt!r}: {w}")
            nd = d + w
            if nd < dist.get(nxt, math.inf):
                dist[nxt] = nd
                prev[nxt] = node
                heapq.heappush(heap, (nd, next(counter), nxt))
    return dist, prev


def shortest_path(
    graph: WeightedGraph, source: Hashable, target: Hashable
) -> tuple[float, list[Hashable]]:
    """Return ``(distance, path)``; ``(inf, [])`` if ``target`` is unreachable.

    >>> shortest_path({"A": {"B": 1, "C": 4}, "B": {"C": 2}}, "A", "C")
    (3, ['A', 'B', 'C'])
    """
    dist, prev = dijkstra(graph, source)
    if target not in dist:
        return math.inf, []
    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    return dist[target], path[::-1]
