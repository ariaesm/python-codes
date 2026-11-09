"""Trie (prefix tree) for strings.

Each node maps a character to a child node; a flag marks the end of a stored word.

Complexity (L = length of the word / prefix):
    insert / contains / starts_with / delete: O(L)
    words_with_prefix: O(L + size of the output subtree)
    Space: O(total characters stored) in the worst case
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator


class _Node:
    __slots__ = ("children", "terminal")

    def __init__(self) -> None:
        self.children: dict[str, _Node] = {}
        self.terminal = False


class Trie:
    """
    >>> t = Trie(["car", "cart", "care", "dog"])
    >>> t.words_with_prefix("car")
    ['car', 'care', 'cart']
    >>> "ca" in t, t.starts_with("ca")
    (False, True)
    """

    def __init__(self, words: Iterable[str] = ()) -> None:
        self._root = _Node()
        self._size = 0
        for w in words:
            self.insert(w)

    def __len__(self) -> int:
        return self._size

    def insert(self, word: str) -> None:
        node = self._root
        for ch in word:
            node = node.children.setdefault(ch, _Node())
        if not node.terminal:
            node.terminal = True
            self._size += 1

    def _find(self, prefix: str) -> _Node | None:
        node = self._root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def __contains__(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.terminal

    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def words_with_prefix(self, prefix: str = "") -> list[str]:
        """All stored words starting with ``prefix``, in lexicographic order."""
        node = self._find(prefix)
        return [] if node is None else list(self._walk(node, prefix))

    def _walk(self, node: _Node, prefix: str) -> Iterator[str]:
        if node.terminal:
            yield prefix
        for ch in sorted(node.children):
            yield from self._walk(node.children[ch], prefix + ch)

    def delete(self, word: str) -> bool:
        """Remove ``word``; prune nodes that no longer lead to any word. Returns success."""
        path = [self._root]
        for ch in word:
            nxt = path[-1].children.get(ch)
            if nxt is None:
                return False
            path.append(nxt)
        if not path[-1].terminal:
            return False
        path[-1].terminal = False
        self._size -= 1
        for i in range(len(word), 0, -1):
            node = path[i]
            if node.terminal or node.children:
                break
            del path[i - 1].children[word[i - 1]]
        return True
