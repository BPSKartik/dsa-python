# dsa-python

Clean, tested implementations of the data structures and algorithms that come
up in coursework and placement interviews. Every implementation carries a note
on its **time complexity**, and every public operation is covered by a test.

The goal isn't to collect code — it's to be able to whiteboard each of these
from memory and explain *why* it's O(what it is).

Everything here is written from scratch on the standard library only. The one
import that does real work is `collections.deque`, used for the `Queue` and for
the BFS frontier.

## What's inside

**`structures.py`** — 4 structures

| Structure | Operation | Complexity | Notes |
| :-- | :-- | :-- | :-- |
| `Stack` | `push` / `pop` / `peek` | O(1) | LIFO, backed by a Python list |
| `Queue` | `enqueue` / `dequeue` / `peek` | O(1) | FIFO, backed by `collections.deque` |
| `LinkedList` | `prepend` | O(1) | new head |
| | `append` | O(n) | no tail pointer — walks to the end |
| | `find` / `delete` / `to_list` | O(n) | `delete` removes the first match only |
| `BinarySearchTree` | `insert` / `search` | O(h) | h = height: O(log n) balanced, O(n) worst |
| | `inorder` | O(n) | returns keys in sorted order |

**`algorithms.py`** — 6 algorithms

| Algorithm | Complexity | Notes |
| :-- | :-- | :-- |
| `bubble_sort` | O(n²), O(n) best | early-exit flag; teaching baseline |
| `merge_sort` | O(n log n) | stable, divide & conquer |
| `quick_sort` | O(n log n) avg, O(n²) worst | middle pivot, three-way partition |
| `binary_search` | O(log n) | needs a **sorted** list; returns index or `-1` |
| `bfs` | O(V + E) | queue-based, returns visit order |
| `dfs` | O(V + E) | stack-based, matches recursive DFS order |

All three sorts return a **new** list and leave the caller's list untouched.

The complexity column isn't decoration — it was measured. Doubling the input
size makes `LinkedList.append` take ~3.8x longer (the ~4x an O(n²) build
predicts), while `Queue.dequeue` draining takes ~2x (linear, so O(1) per op),
and `binary_search` needs 24 steps on a 10-million-element list (log₂ 10M ≈ 23).

## Run the tests

The tests need `pytest` — the suite is **16 tests** (8 test functions, three of
them parametrized across the three sorts) and finishes in about 0.01s.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python3 -m pytest tests/ -q        # or: pytest -v
```

Last verified: 16 passed on Python 3.14.7 / pytest 9.1.1.

> **Don't run the test file directly.** `python3 tests/test_dsa.py` exits 0 but
> runs **nothing** — the file only defines test functions, it never invokes a
> runner. (Without pytest installed it doesn't even do that: it dies on
> `import pytest` with `ModuleNotFoundError`.) Always go through pytest, or
> you'll get a green light that means nothing.

## Known limits

These are deliberate — small teaching implementations, not production
containers. Worth knowing before you reuse any of it.

- **`BinarySearchTree` is unbalanced.** Inserting already-sorted keys degrades
  it into a linked list. Because `insert` and `inorder` both recurse, roughly
  1000 sorted keys is enough to hit Python's default recursion limit. The exact
  cut-off is not a fixed number — it shifts with how deep the call stack already
  is when you call it (in my runs it landed between 996 and 998 keys), and
  `inorder()` gives out slightly before `insert` does, so a tree you built
  successfully can still fail to traverse. `search` is iterative and survives.
  A real BST would self-balance — AVL or red-black.
- **`BinarySearchTree` ignores duplicate keys** — it behaves like a set, so
  inserting `5, 3, 5` gives an inorder of `[3, 5]`.
- **`merge_sort` needs `<=`, not just `<`.** The stable-merge comparison is
  `left[i] <= right[j]`, so sorting objects that define only `__lt__` raises
  `TypeError: '<=' not supported between instances of ...`. Python's built-in
  `sorted()` requires only `__lt__`, and `bubble_sort` and `quick_sort` happen
  to work on such objects — `merge_sort` is the odd one out.
- **`quick_sort` recurses.** Ordinary input is fine (sorted, reversed, and
  random 50k-element lists all sort without trouble, because a middle pivot on
  sorted data is the median). An adversarial list built so the middle element is
  always extreme hits `RecursionError` at about n = 2000 — n = 1950 still works.
- **`binary_search` with duplicates** returns *some* matching index, not
  necessarily the first: on `[1, 2, 2, 2, 2, 3]` it returns `2`, not `1`.
- **`binary_search` does not verify its input is sorted.** On unsorted input it
  returns a silently wrong answer — `binary_search([5, 4, 3, 2, 1], 4)` gives
  `-1` even though `4` is at index 1.
- **`bfs` / `dfs` treat a missing start node as an isolated node** rather than
  raising: `bfs({"A": ["B"]}, "Q")` returns `["Q"]`.

## Studying this repo

Read the code, then try re-writing one file from a blank page. If you can't,
you don't know it yet — that's the whole point.
