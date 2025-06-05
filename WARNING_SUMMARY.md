# Warning Summary

This file lists unique warnings observed when running `pytest -q -W once`.

- **DeprecationWarning** at `pytest_freezegun.py:17`: uses deprecated `distutils` `LooseVersion` for comparing pytest versions. This warning originates from the third-party package `pytest-freezegun` and does not affect repository code.

All other tests run without warnings.

The warning is filtered in `pytest.ini`.
