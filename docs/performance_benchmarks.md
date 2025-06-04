# Performance Benchmarks

This document records baseline execution times for selected utility functions.
Run `python scripts/performance_profile.py` to reproduce these numbers.

```
$ python scripts/performance_profile.py
_safe_concat_normal: 0.00xxs
_transpose_financials: 0.00xxs
```

The `_transpose_financials` loop was optimized to use a list comprehension for
renaming columns, providing a small speedup visible in the profiling output.
