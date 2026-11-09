import pytest

from algorithms.data_structures.lru_cache import LRUCache
from algorithms.data_structures.trie import Trie
from algorithms.data_structures.union_find import UnionFind, kruskal


class TestLRU:
    def test_eviction_order(self):
        c = LRUCache(3)
        for k in "abc":
            c.put(k, k.upper())
        c.get("a")  # a becomes most recent
        c.put("d", "D")  # evicts b
        assert "b" not in c
        assert c.keys() == ["d", "a", "c"]

    def test_update_moves_to_front(self):
        c = LRUCache(2)
        c.put(1, 1)
        c.put(2, 2)
        c.put(1, 10)
        c.put(3, 3)  # evicts 2
        assert c.get(1) == 10
        assert c.get(2, "missing") == "missing"
        assert len(c) == 2

    def test_matches_reference_model(self):
        import random
        from collections import OrderedDict

        rng = random.Random(1)
        c, ref = LRUCache(5), OrderedDict()
        for _ in range(2000):
            k = rng.randint(0, 9)
            if rng.random() < 0.5:
                c.put(k, k)
                ref[k] = k
                ref.move_to_end(k)
                if len(ref) > 5:
                    ref.popitem(last=False)
            else:
                assert c.get(k) == ref.get(k)
                if k in ref:
                    ref.move_to_end(k)
        assert c.keys() == list(reversed(ref))

    def test_invalid_capacity(self):
        with pytest.raises(ValueError):
            LRUCache(0)


class TestTrie:
    def test_basic(self):
        t = Trie(["apple", "app", "apt", "bat"])
        assert "app" in t and "ap" not in t
        assert t.starts_with("ap") and not t.starts_with("c")
        assert t.words_with_prefix("ap") == ["app", "apple", "apt"]
        assert t.words_with_prefix("z") == []
        assert len(t) == 4

    def test_duplicates_and_empty_string(self):
        t = Trie(["a", "a", ""])
        assert len(t) == 2
        assert "" in t

    def test_delete_prunes(self):
        t = Trie(["app", "apple"])
        assert t.delete("apple")
        assert t.words_with_prefix() == ["app"]
        assert not t.starts_with("appl")
        assert not t.delete("apple")
        assert not t.delete("ap")
        assert t.delete("app")
        assert len(t) == 0 and not t.starts_with("a")


class TestUnionFind:
    def test_union_and_count(self):
        uf = UnionFind(range(6))
        assert uf.union(0, 1) and uf.union(1, 2)
        assert not uf.union(0, 2)
        assert uf.connected(0, 2) and not uf.connected(0, 3)
        assert uf.count == 4
        assert uf.set_size(2) == 3

    def test_lazy_add(self):
        uf = UnionFind()
        uf.union("x", "y")
        assert uf.connected("x", "y")
        assert uf.count == 1

    def test_kruskal(self):
        edges = [
            (0, 1, 7),
            (0, 3, 5),
            (1, 2, 8),
            (1, 3, 9),
            (1, 4, 7),
            (2, 4, 5),
            (3, 4, 15),
            (3, 5, 6),
            (4, 5, 8),
            (4, 6, 9),
            (5, 6, 11),
        ]
        total, tree = kruskal(7, edges)
        assert total == 39
        assert len(tree) == 6
