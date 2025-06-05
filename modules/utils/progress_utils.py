from __future__ import annotations

"""Utilities for optional progress indicators.

Example::

    for item in progress_iter(values, description="Processing"):
        handle(item)
"""

from typing import Iterable, Iterator, TypeVar, Optional

try:
    from tqdm import tqdm
except Exception:  # pragma: no cover - fallback if tqdm missing
    tqdm = None  # type: ignore

T = TypeVar("T")


def progress_iter(iterable: Iterable[T], *, description: Optional[str] = None) -> Iterator[T]:
    """Yield items from ``iterable`` while displaying a progress bar if possible.

    Parameters
    ----------
    iterable:
        Any iterable sequence of values.
    description:
        Optional label shown alongside the progress bar.

    Returns
    -------
    Iterator[T]
        Iterator over the original values.
    """
    if tqdm is None:
        for item in iterable:
            yield item
    else:  # pragma: no cover - UI behavior not tested
        for item in tqdm(iterable, desc=description):
            yield item
