# Performance Benchmarks

This document records baseline execution times for selected utility functions.
Run `python scripts/performance_profile.py` to reproduce these numbers.

```
$ python scripts/performance_profile.py
portfolio_summary: 0.00xxs
correlation_matrix: 0.00xxs
```

These numbers provide a rough baseline for the analysis helpers. Large
deviations may indicate a regression after refactoring.
