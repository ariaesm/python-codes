"""Breadth-first and depth-first search.

Graphs are adjacency mappings ``{node: [neighbours, ...]}``; nodes only reachable as
neighbours (with no entry of their own) are treated as having no outgoing edges.

Complexity (V vertices, E edges):
    Time:  O(V + E) for every function here
    Space: O(V) for the visited set and the queue/stack
"""

from __future__ import annotations

from collections import deque
from collections.abc import Hashable, Iterable, Mapping

Graph = Mapping[Hashable, Iterable[Hashable]]


def bfs(graph: Graph, start: Hashable) -> list[Hashable]:
    """Nodes in breadth-first order (neighbours visited in the order listed).

    >>> bfs({"a": ["b", "c"], "b": ["d"], "c": ["d"]}, "a")
    ['a', 'b', 'c', 'd']
    """
    seen = {start}
    order = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph.get(node, ()):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return order


def dfs(graph: Graph, start: Hashable) -> list[Hashable]:
    """Nodes in depth-first preorder, iterative (no recursion limit issues).

    Produces the same order as the textbook recursive version.

    >>> dfs({"a": ["b", "c"], "b": ["d"], "c": ["d"]}, "a")
    ['a', 'b', 'd', 'c']
    """
    seen: set[Hashable] = set()
    order = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        # Push in reverse so the first-listed neighbour is explored first.
        stack.extend(n for n in reversed(list(graph.get(node, ()))) if n not in seen)
    return order


def dfs_recursive(graph: Graph, start: Hashable) -> list[Hashable]:
    """Recursive depth-first preorder (clear, but limited by Python's recursion depth)."""
    order: list[Hashable] = []
    seen: set[Hashable] = set()

    def visit(node: Hashable) -> None:
        seen.add(node)
        order.append(node)
        for nxt in graph.get(node, ()):
            if nxt not in seen:
                visit(nxt)

    visit(start)
    return order


def shortest_path(graph: Graph, start: Hashable, goal: Hashable) -> list[Hashable] | None:
    """Fewest-edges path from ``start`` to ``goal`` using BFS, or ``None``.

    >>> shortest_path({"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": ["e"]}, "a", "e")
    ['a', 'b', 'd', 'e']
    """
    parent: dict[Hashable, Hashable] = {start: start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            path = [node]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return path[::-1]
        for nxt in graph.get(node, ()):
            if nxt not in parent:
                parent[nxt] = node
                queue.append(nxt)
    return None


def connected_components(graph: Graph) -> list[list[Hashable]]:
    """Components of an *undirected* graph (each edge listed in both directions)."""
    seen: set[Hashable] = set()
    comps = []
    for node in graph:
        if node not in seen:
            comp = bfs(graph, node)
            seen.update(comp)
            comps.append(comp)
    return comps
