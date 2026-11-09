import math

import pytest

from algorithms.graphs import bfs_dfs, dijkstra

G = {"a": ["b", "c"], "b": ["d"], "c": ["d", "e"], "d": ["f"], "e": ["f"], "f": []}


def test_bfs_order():
    assert bfs_dfs.bfs(G, "a") == ["a", "b", "c", "d", "e", "f"]


def test_dfs_iterative_matches_recursive():
    assert bfs_dfs.dfs(G, "a") == ["a", "b", "d", "f", "c", "e"]
    assert bfs_dfs.dfs(G, "a") == bfs_dfs.dfs_recursive(G, "a")


def test_dfs_handles_deep_graph_without_recursion_error():
    chain = {i: [i + 1] for i in range(10_000)}
    assert len(bfs_dfs.dfs(chain, 0)) == 10_001


def test_cycles():
    cyc = {1: [2], 2: [3], 3: [1]}
    assert bfs_dfs.bfs(cyc, 1) == [1, 2, 3]
    assert bfs_dfs.dfs(cyc, 1) == [1, 2, 3]


def test_unweighted_shortest_path():
    assert bfs_dfs.shortest_path(G, "a", "f") == ["a", "b", "d", "f"]
    assert bfs_dfs.shortest_path(G, "a", "a") == ["a"]
    assert bfs_dfs.shortest_path(G, "f", "a") is None


def test_connected_components():
    und = {1: [2], 2: [1], 3: [4], 4: [3], 5: []}
    assert sorted(map(sorted, bfs_dfs.connected_components(und))) == [[1, 2], [3, 4], [5]]


W = {
    "A": {"B": 4, "C": 2},
    "B": {"C": 5, "D": 10},
    "C": {"E": 3},
    "E": {"D": 4},
    "D": {"F": 11},
}


def test_dijkstra_distances():
    dist, _ = dijkstra.dijkstra(W, "A")
    assert dist == {"A": 0, "B": 4, "C": 2, "E": 5, "D": 9, "F": 20}


def test_dijkstra_path_and_unreachable():
    assert dijkstra.shortest_path(W, "A", "D") == (9, ["A", "C", "E", "D"])
    assert dijkstra.shortest_path(W, "D", "A") == (math.inf, [])


def test_dijkstra_rejects_negative_weights():
    with pytest.raises(ValueError):
        dijkstra.dijkstra({"A": {"B": -1}}, "A")


def test_dijkstra_matches_bellman_ford_on_random_graphs():
    import random

    rng = random.Random(7)
    for _ in range(30):
        n = 8
        g = {
            u: {v: rng.randint(0, 9) for v in range(n) if v != u and rng.random() < 0.3}
            for u in range(n)
        }
        dist = {0: 0}
        for _ in range(n - 1):  # Bellman-Ford relaxation as a reference
            for u, edges in g.items():
                for v, w in edges.items():
                    if u in dist and dist[u] + w < dist.get(v, math.inf):
                        dist[v] = dist[u] + w
        assert dijkstra.dijkstra(g, 0)[0] == dist
