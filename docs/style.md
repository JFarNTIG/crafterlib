# crafterlib Code Style Guide

*Version 1.0 - June 2025*

> **Purpose**
> Establish a consistent, modern, and readable coding style for all contributors to the crafterlib project.

---

## 1  Repository Layout

| Item            | Convention                            | Example                             |
| --------------- | ------------------------------------- | ----------------------------------- |
| Source files    | `*.py`                                | `crafting_data.py`                  |
| Public modules  | live in `src/crafterlib`              | `src/crafterlib/loader.py`          |
| Private helpers | live under `src/crafterlib/_internal` | `src/crafterlib/_internal/cache.py` |
| Tests           | `tests/`                              | `tests/io/test_file_reader.py`      |
| Examples        | `examples/`                           | `examples/minecraft_recipes.py`     |
| Docs            | `docs/`                               | `docs/style.md`                     |

---

## 2  Formatting Rules

* **Indentation:** 4 spaces, never tabs.
* **Line length:** 100 chars max (except long URLs or deeply nested data).
* **Whitespace:**

  * No spaces immediately inside parentheses, brackets, or braces.
  * Exactly one space after a comma, colon, or semicolon.
* **Braces:** Python uses indentation blocks. Avoid unnecessary braces in dict comprehensions.
* **Trailing commas:**

  * Required in multi-line collections.
  * Forbidden in single-line collections.
* **Blank lines:**

  * Two blank lines between top-level definitions.
  * One blank line between methods within a class.
* **Shebang:** Only in executable scripts: `#!/usr/bin/env python3`.
* **Encoding:** UTF-8 (implicit, do not add `# -*- coding: utf-8 -*-`).

*Code formatter:* **black** (with default line length = 100).
*Linter:* **ruff** (or flake8 + mypy where applicable).

---

## 3  Naming Conventions

| Entity              | Style              | Example                |
| ------------------- | ------------------ | ---------------------- |
| Package / Module    | `lower_snake_case` | `item_graph`           |
| Class               | `UpperCamelCase`   | `ItemGraph`            |
| Function            | `lower_snake_case` | `load_data_for_game`   |
| Variable            | `lower_snake_case` | `file_size`            |
| Constant            | `ALL_CAPS_SNAKE`   | `MAX_COUNT`            |
| Private member      | `_lower_snake`     | `_cache`               |
| TypeVar / ParamSpec | `UpperCamelCase`   | `T_contra`             |
| CLI command         | kebab-case         | `mytool-generate-docs` |

---

## 4  Language Guidelines

* Always use **type hints** (PEP 484 / PEP 681).
* Prefer **dataclasses** over handwritten `__init__` when only storing data.
* Use `property` for observable attributes rather than exposing mutable public fields.
* Default to **immutability** where practical (namedtuple or `@dataclass(frozen=True)`).
* Prefer `enumeration.Enum` or `StrEnum` for discrete sets.
* Mark one-argument constructors/factory functions as `@classmethod def from_*`.
* Use `__all__` in each public module to declare exported symbols.
* Never shadow built-ins (`list`, `id`, `file`, ...).

---

## 5  Imports & Dependencies

1. **Order (black / ruff style):**

   1. Standard library
   2. Third-party
   3. Local package
2. Absolute imports only; never use implicit relative (`import mymodule`) inside package.
3. Import specific names. Use of `*` should be avoided.
4. Use **optional dependencies** guarded by `typing.TYPE_CHECKING` or runtime try/except.

```python
from __future__ import annotations  # top of file

import logging
from pathlib import Path

import numpy as np
from rich.console import Console

from myproject._internal.cache import LRUCache
```

---

## 6  Error Handling

* Prefer **exceptions**; do **not** return sentinel values (`None`, `-1`) for errors.
* Catch narrow exception classes (`except FileNotFoundError`) rather than bare `except`.
* Convert third-party exceptions into library-defined domain errors when crossing API boundaries.
* Use `raise from` to preserve traceback context.

```python
try:
    data = Path(path).read_bytes()
except OSError as exc:
    raise StreamReadError(path) from exc
```

---

## 7  Concurrency & Async

* Choose between **threading** and **asyncio**. Never mix without clear boundaries.
* Protect shared mutable state with `threading.Lock` or `contextvars` for async local state.
* Use **concurrent.futures** pools for CPU-bound tasks; prefer **asyncio.Semaphore** for limiting I/O concurrency.
* All public APIs must be either sync *or* async. Never return `awaitable` conditionally.

---

## 8  Documentation & Comments

* **Docstrings:** Use **Google style** or **reStructuredText** consistently across the codebase.
* **Public APIs** must have complete docstrings: summary line, Args, Returns, Raises, Examples.
* **Private helpers** need at least a summary if non-trivial.
* Inline comments should clarify *why*, not *what*:

```python
# Binary search here is O(log n), acceptable for buffers <= 32 KB.
```

* TODOs: `# TODO(username, YYYY-MM-DD): ...`

Example public function:

```python
def buffered_match(text: str, pattern: str, *, pos: int = 0) -> bool:
    """Return ``True`` if *pattern* matches *text* at *pos*.

    Args:
        text: The haystack string.
        pattern: A regular expression.
        pos: The starting offset within *text*.

    Returns:
        ``True`` if a match exists, else ``False``.

    Raises:
        regex.error: If *pattern* is invalid.
    """
```

---

## 9  Unit Testing

* Framework: **pytest** (plus **pytest-asyncio** for async code).
* Coverage target: **>= 90 %** for new code.
* Arrange-Act-Assert structure; fixture names should describe the role (`sample_pdf`, `tmp_repo`).
* Tests must be deterministic and independent; disable network unless explicitly needed.
* Average suite runtime <= 5 s; long-running cases behind `pytest.mark.slow`.

---

## 10  Git Workflow

1. **Branch names:** `feature/short-desc` · `bugfix/short-desc` · `docs/short-desc`.

2. **Commit messages:** Imperative, <= 72 chars subject line.

   ```
   Add streaming UTF-8 decoder
   ```

3. **Pull Requests:**

   * Title: `[feat]`, `[fix]`, `[docs]`, `[refactor]`, `[perf]`, `[test]`, `[ci]`, `[build]`, `[misc]`.
   * Follow the PR template and fill out the checklist when submitting a PR.
   * Require one approving review; use GitHub Suggestions for small fixes.

4. **Conventional Commits** optional but encouraged for automatic changelogs.

---

## 11  Deprecation Policy

* Decorate deprecated callables with

  ```python
  import warnings

  def old_api(*args, **kwargs):  # pragma: no cover
      warnings.warn(
          "old_api() is deprecated; use new_api() instead.",
          DeprecationWarning,
          stacklevel=2,
      )
      ...
  ```

* Maintain for **one minor release** before removal.

---

## 12  License Header

Add to every source file:

```python
# SPDX-License-Identifier: MIT
```

---

## 13  Acknowledgements

Inspired by **PEP 8**, **Google Python Style Guide**, **Black**, and **Python Core Guidelines**.
