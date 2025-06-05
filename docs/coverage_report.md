# Test Coverage Summary

The automated suite was executed with `pytest --cov=modules` using
`pytest-cov`. The run on the reference environment yielded roughly **11%**
statement coverage.

```
modules/__init__.py                   0      0   100%
modules/analytics/__init__.py        24     17    29%
...
TOTAL                               2422   2165    11%
```

Coverage is expected to remain low until more modules gain dedicated tests, but
the report helps track progress over time. To generate the report locally run:

```bash
pytest --cov=modules --cov-report=term
```
