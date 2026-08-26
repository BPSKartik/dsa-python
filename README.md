# dsa-python

Clean, tested implementations of the data structures and algorithms that come
up in coursework and placement interviews. Every implementation is commented
with its **time complexity** and has a test that proves it works.

The goal isn't to collect code — it's to be able to whiteboard each of these
from memory and explain *why* it's O(what it is).

## What's inside

**`structures.py`**
| Structure | Key operations | Notes |
| :-- | :-- | :-- |
| `Stack` | push / pop / peek — O(1) | LIFO, on a Python list |
| `Queue` | enqueue / dequeue — O(1) | FIFO, on `collections.deque` |
| `LinkedList` | append / prepend / find / delete | singly linked |
| `BinarySearchTree` | insert / search / inorder | inorder = sorted order |

**`algorithms.py`**
| Algorithm | Complexity | Notes |
| :-- | :-- | :-- |
| `bubble_sort` | O(n²) | simple, teaching baseline |
| `merge_sort` | O(n log n) | stable, divide & conquer |
| `quick_sort` | O(n log n) avg | in-practice fast |
| `binary_search` | O(log n) | needs a **sorted** list |
| `bfs` / `dfs` | O(V + E) | graph traversal on an adjacency map |

## Run the tests

```bash
pip install -r requirements.txt
pytest -v
```

## Studying this repo

Read the code, then try re-writing one file from a blank page. If you can't,
you don't know it yet — that's the whole point.
