"""Least-recently-used (LRU) cache.

A hash map gives O(1) lookup and a doubly linked list keeps recency order: the most
recently used node sits right after the head sentinel, the least recently used one right
before the tail sentinel, so eviction is O(1) too. (In production code
:class:`collections.OrderedDict` or :func:`functools.lru_cache` do the same job; this is the
from-scratch version.)

Complexity:
    get / put: O(1) time
    Space:     O(capacity)
"""

from __future__ import annotations

from collections.abc import Hashable
from typing import Any


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: Hashable = None, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.prev: _Node = self
        self.next: _Node = self


class LRUCache:
    """Fixed-capacity mapping that evicts the least recently used key.

    >>> c = LRUCache(2)
    >>> c.put("a", 1); c.put("b", 2); c.get("a")
    1
    >>> c.put("c", 3)  # evicts "b", the least recently used
    >>> c.get("b") is None
    True
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._map: dict[Hashable, _Node] = {}
        self._head = _Node()  # sentinel: head.next is most recent
        self._tail = _Node()  # sentinel: tail.prev is least recent
        self._head.next, self._tail.prev = self._tail, self._head

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, key: Hashable) -> bool:
        return key in self._map

    def _unlink(self, node: _Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node: _Node) -> None:
        node.prev, node.next = self._head, self._head.next
        self._head.next.prev = node
        self._head.next = node

    def get(self, key: Hashable, default: Any = None) -> Any:
        node = self._map.get(key)
        if node is None:
            return default
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key: Hashable, value: Any) -> None:
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self._map) == self.capacity:
            lru = self._tail.prev
            self._unlink(lru)
            del self._map[lru.key]
        node = _Node(key, value)
        self._map[key] = node
        self._push_front(node)

    def keys(self) -> list[Hashable]:
        """Keys from most to least recently used."""
        out = []
        node = self._head.next
        while node is not self._tail:
            out.append(node.key)
            node = node.next
        return out
