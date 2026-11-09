# python-codes - classic algorithms & data structures in Python

A small, curated collection of classic algorithms and data structures, each implemented
from scratch as a short, readable module with:

- a docstring explaining the idea,
- time/space complexity notes,
- runnable doctest examples,
- pytest tests, most of them checking against a brute-force or standard-library
  reference on randomised inputs.

Pure Python 3.11+, no dependencies besides `pytest` for the tests.

## Table of contents

| Topic | Module | Contents | Time | Space |
| --- | --- | --- | --- | --- |
| Searching | [`binary_search.py`](algorithms/searching/binary_search.py) | `binary_search`, `lower_bound`, `upper_bound`, `count_occurrences` | O(log n) | O(1) |
| Sorting | [`merge_sort.py`](algorithms/sorting/merge_sort.py) | stable top-down merge sort with `key` | O(n log n) | O(n) |
| Sorting | [`quick_sort.py`](algorithms/sorting/quick_sort.py) | in-place, random pivot, Hoare partition, no recursion | O(n log n) expected, O(n²) worst | O(log n) |
| Graphs | [`bfs_dfs.py`](algorithms/graphs/bfs_dfs.py) | BFS, iterative + recursive DFS, unweighted shortest path, connected components | O(V + E) | O(V) |
| Graphs | [`dijkstra.py`](algorithms/graphs/dijkstra.py) | Dijkstra with a binary heap, path reconstruction | O((V + E) log V) | O(V + E) |
| Data structures | [`lru_cache.py`](algorithms/data_structures/lru_cache.py) | LRU cache: hash map + doubly linked list | O(1) get/put | O(capacity) |
| Data structures | [`trie.py`](algorithms/data_structures/trie.py) | prefix tree: insert, lookup, prefix search, delete with pruning | O(L) per op | O(total chars) |
| Data structures | [`union_find.py`](algorithms/data_structures/union_find.py) | disjoint sets (path compression + union by size), Kruskal's MST | O(α(n)) amortised | O(n) |
| Techniques | [`sliding_window.py`](algorithms/techniques/sliding_window.py) | max-sum window, longest unique substring, min subarray ≥ target, window max (monotonic deque) | O(n) | O(1) - O(k) |
| Dynamic programming | [`knapsack.py`](algorithms/dynamic_programming/knapsack.py) | 0/1 knapsack value (1-D table) and chosen items | O(n·W) | O(W) / O(n·W) |
| Dynamic programming | [`lis.py`](algorithms/dynamic_programming/lis.py) | longest increasing subsequence: O(n²) DP and O(n log n) patience sorting | O(n log n) | O(n) |
| Dynamic programming | [`edit_distance.py`](algorithms/dynamic_programming/edit_distance.py) | Levenshtein distance (two rows) and an optimal edit script | O(m·n) | O(min(m, n)) |

## Usage

```bash
git clone https://github.com/ariaesm/python-codes.git
cd python-codes
pip install -r requirements.txt
```

Everything is importable from the `algorithms` package. Real output:

```python
>>> from algorithms.graphs.dijkstra import shortest_path
>>> g = {"Tehran": {"Qom": 140, "Karaj": 45}, "Karaj": {"Qazvin": 105},
...      "Qom": {"Kashan": 105}, "Qazvin": {"Zanjan": 175}}   # toy weights
>>> shortest_path(g, "Tehran", "Zanjan")
(325, ['Tehran', 'Karaj', 'Qazvin', 'Zanjan'])

>>> from algorithms.dynamic_programming.edit_distance import edit_distance, edit_script
>>> edit_distance("kitten", "sitting")
3
>>> edit_script("kitten", "sitting")
['sub k->s', 'keep i', 'keep t', 'keep t', 'sub e->i', 'keep n', 'insert g']

>>> from algorithms.data_structures.trie import Trie
>>> Trie(["car", "cart", "care", "dog"]).words_with_prefix("car")
['car', 'care', 'cart']
```

## Tests

```bash
python -m pytest
```

`pyproject.toml` enables `--doctest-modules`, so the examples in every docstring are
executed as tests too (84 tests in total at the time of writing). CI (GitHub Actions)
runs `ruff` and `pytest` on Python 3.12.

## Layout

```
algorithms/
  searching/            binary_search.py
  sorting/              merge_sort.py, quick_sort.py
  graphs/               bfs_dfs.py, dijkstra.py
  data_structures/      lru_cache.py, trie.py, union_find.py
  techniques/           sliding_window.py
  dynamic_programming/  knapsack.py, lis.py, edit_distance.py
tests/                  one test file per topic
```

## License

MIT - see [LICENSE](LICENSE).
