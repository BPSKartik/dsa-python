"""
Tests that prove each structure and algorithm works. Run with:  pytest -v

These double as usage examples — read them to see how each piece is meant
to be called.
"""

import os
import random
import sys

# make the parent folder importable when running `pytest` from the repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from algorithms import binary_search, bfs, bubble_sort, dfs, merge_sort, quick_sort
from structures import BinarySearchTree, LinkedList, Queue, Stack


# ------------------------------- structures --------------------------------

def test_stack_is_lifo():
    s = Stack()
    for x in (1, 2, 3):
        s.push(x)
    assert len(s) == 3
    assert s.peek() == 3
    assert s.pop() == 3
    assert s.pop() == 2
    assert len(s) == 1


def test_stack_empty_errors():
    with pytest.raises(IndexError):
        Stack().pop()


def test_queue_is_fifo():
    q = Queue()
    for x in ("a", "b", "c"):
        q.enqueue(x)
    assert q.peek() == "a"
    assert q.dequeue() == "a"
    assert q.dequeue() == "b"
    assert len(q) == 1


def test_linked_list_operations():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.prepend(0)
    assert ll.to_list() == [0, 1, 2]
    assert len(ll) == 3
    assert ll.find(2) is True
    assert ll.find(9) is False
    assert ll.delete(0) is True          # delete the head
    assert ll.to_list() == [1, 2]
    assert ll.delete(9) is False         # not present


def test_bst_search_and_sorted_order():
    tree = BinarySearchTree()
    for k in (5, 3, 8, 1, 4, 7, 9):
        tree.insert(k)
    assert tree.search(7) is True
    assert tree.search(6) is False
    # inorder traversal of a BST is always sorted
    assert tree.inorder() == [1, 3, 4, 5, 7, 8, 9]


# ------------------------------- algorithms --------------------------------

SORTERS = [bubble_sort, merge_sort, quick_sort]


@pytest.mark.parametrize("sort", SORTERS)
def test_sorters_match_builtin(sort):
    cases = [
        [],
        [1],
        [3, 1, 2],
        [5, 5, 3, 3, 1],
        [9, -2, 0, 7, -5, 4],
    ]
    for case in cases:
        assert sort(case) == sorted(case)


@pytest.mark.parametrize("sort", SORTERS)
def test_sorters_do_not_mutate_input(sort):
    original = [4, 2, 7, 1]
    _ = sort(original)
    assert original == [4, 2, 7, 1]


@pytest.mark.parametrize("sort", SORTERS)
def test_sorters_on_random_lists(sort):
    rng = random.Random(0)
    for _ in range(20):
        data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 30))]
        assert sort(data) == sorted(data)


def test_binary_search():
    data = [1, 3, 5, 7, 9, 11]
    assert binary_search(data, 7) == 3
    assert binary_search(data, 1) == 0
    assert binary_search(data, 11) == 5
    assert binary_search(data, 4) == -1     # not present
    assert binary_search([], 1) == -1


def test_graph_traversals():
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": [],
        "E": ["F"],
        "F": [],
    }
    assert bfs(graph, "A") == ["A", "B", "C", "D", "E", "F"]
    assert dfs(graph, "A") == ["A", "B", "D", "E", "F", "C"]
