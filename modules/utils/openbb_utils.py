from __future__ import annotations

"""Utility functions for accessing the OpenBB Platform."""

import os


_obb = None
_logged_in = False


def get_openbb():
    """Return OpenBB module ensuring login via ``OPENBB_TOKEN`` if available."""
    global _obb, _logged_in
    if _obb is None:
        from openbb import obb as _module
        _obb = _module
    if not _logged_in:
        token = os.getenv("OPENBB_TOKEN")
        if token:
            try:
                _obb.account.login(pat=token)
                _logged_in = True
            except Exception as exc:  # pragma: no cover - network/login error
                print(f"Warning: OpenBB login failed: {exc}")
        else:
            print("OPENBB_TOKEN environment variable not set; skipping OpenBB login.")
    return _obb
