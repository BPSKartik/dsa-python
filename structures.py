"""
Core data structures, implemented from scratch and kept deliberately small.
Each class notes the complexity of its main operations.
"""

from collections import deque
from typing import Any, Optional


class Stack:
    """LIFO — last in, first out. Think: a stack of plates."""

    def __init__(self) -> None:
        self._items: list[Any] = []

    def push(self, item: Any) -> None:      # O(1)
        self._items.append(item)

    def pop(self) -> Any:                    # O(1)
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:                   # O(1) — look without removing
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


class Queue:
    """FIFO — first in, first out. Think: a line at a counter."""

    def __init__(self) -> None:
        # deque pops from the left in O(1); a plain list would be O(n).
        self._items: deque[Any] = deque()

    def enqueue(self, item: Any) -> None:    # O(1)
        self._items.append(item)

    def dequeue(self) -> Any:                # O(1)
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def peek(self) -> Any:                   # O(1)
        if self.is_empty():
            raise IndexError("peek at empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


class _Node:
    """One link in a singly linked list."""

    def __init__(self, value: Any) -> None:
        self.value = value
        self.next: Optional["_Node"] = None


class LinkedList:
    """A singly linked list — a chain of nodes, each pointing to the next."""

    def __init__(self) -> None:
        self.head: Optional[_Node] = None
        self._size = 0

    def append(self, value: Any) -> None:    # O(n) — walk to the tail
        node = _Node(value)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = node
        self._size += 1

    def prepend(self, value: Any) -> None:   # O(1) — new head
        node = _Node(value)
        node.next = self.head
        self.head = node
        self._size += 1

    def find(self, value: Any) -> bool:      # O(n)
        cur = self.head
        while cur is not None:
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def delete(self, value: Any) -> bool:    # O(n)
        """Remove the first node holding `value`. Returns True if removed."""
        prev, cur = None, self.head
        while cur is not None:
            if cur.value == value:
                if prev is None:             # deleting the head
                    self.head = cur.next
                else:
                    prev.next = cur.next
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def to_list(self) -> list[Any]:
        out, cur = [], self.head
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out

    def __len__(self) -> int:
        return self._size


class _BSTNode:
    def __init__(self, key: Any) -> None:
        self.key = key
        self.left: Optional["_BSTNode"] = None
        self.right: Optional["_BSTNode"] = None


class BinarySearchTree:
    """
    Binary search tree: for every node, everything on the left is smaller and
    everything on the right is larger. That invariant makes search O(h), where
    h is the height (O(log n) when balanced, O(n) in the worst case).
    """

    def __init__(self) -> None:
        self.root: Optional[_BSTNode] = None

    def insert(self, key: Any) -> None:
        self.root = self._insert(self.root, key)

    def _insert(self, node: Optional[_BSTNode], key: Any) -> _BSTNode:
        if node is None:
            return _BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        # equal keys are ignored (a set-like tree)
        return node

    def search(self, key: Any) -> bool:
        node = self.root
        while node is not None:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def inorder(self) -> list[Any]:
        """Left -> node -> right yields the keys in sorted order."""
        out: list[Any] = []
        self._inorder(self.root, out)
        return out

    def _inorder(self, node: Optional[_BSTNode], out: list[Any]) -> None:
        if node is None:
            return
        self._inorder(node.left, out)
        out.append(node.key)
        self._inorder(node.right, out)
