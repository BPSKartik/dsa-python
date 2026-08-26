"""
Classic sorting, searching, and graph-traversal algorithms.
All sorts return a NEW list and leave the input untouched.
"""

from typing import Any


def bubble_sort(items: list[Any]) -> list[Any]:
    """
    O(n^2). Repeatedly walk the list swapping neighbours that are out of order;
    the largest element 'bubbles' to the end each pass. Slow, but the easiest
    sort to reason about. The early-exit flag makes an already-sorted list O(n).
    """
    a = items[:]                       # copy so we don't mutate the caller's list
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):     # last i items are already in place
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:                # nothing moved -> already sorted
            break
    return a


def merge_sort(items: list[Any]) -> list[Any]:
    """
    O(n log n), stable. Divide the list in half, sort each half, then merge the
    two sorted halves back together. The classic divide-and-conquer sort.
    """
    if len(items) <= 1:
        return items[:]
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    return _merge(left, right)


def _merge(left: list[Any], right: list[Any]) -> list[Any]:
    merged: list[Any] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:        # <= keeps equal items in order (stable)
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])            # one side is exhausted; append the rest
    merged.extend(right[j:])
    return merged


def quick_sort(items: list[Any]) -> list[Any]:
    """
    O(n log n) average, O(n^2) worst case. Pick a pivot, partition the rest into
    'smaller' and 'larger', then recurse. This readable version uses extra lists;
    an in-place version saves memory but is harder to read.
    """
    if len(items) <= 1:
        return items[:]
    pivot = items[len(items) // 2]
    smaller = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    larger = [x for x in items if x > pivot]
    return quick_sort(smaller) + equal + quick_sort(larger)


def binary_search(sorted_items: list[Any], target: Any) -> int:
    """
    O(log n). Halve the search range each step. Requires a SORTED list.
    Returns the index of `target`, or -1 if it isn't present.
    """
    low, high = 0, len(sorted_items) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_items[mid] == target:
            return mid
        if sorted_items[mid] < target:
            low = mid + 1              # target is in the right half
        else:
            high = mid - 1             # target is in the left half
    return -1


def bfs(graph: dict[Any, list[Any]], start: Any) -> list[Any]:
    """
    Breadth-first search. Explore level by level using a queue.
    Returns nodes in the order they were first visited. O(V + E).
    """
    from collections import deque

    visited: list[Any] = []
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        visited.append(node)
        for neighbour in graph.get(node, []):
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return visited


def dfs(graph: dict[Any, list[Any]], start: Any) -> list[Any]:
    """
    Depth-first search. Go as deep as possible before backtracking, using a
    stack. Returns visit order. O(V + E).
    """
    visited: list[Any] = []
    seen: set[Any] = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        visited.append(node)
        # reversed() so neighbours come out in their listed order
        for neighbour in reversed(graph.get(node, [])):
            if neighbour not in seen:
                stack.append(neighbour)
    return visited
