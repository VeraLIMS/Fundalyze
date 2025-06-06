# Utility Modules

This page describes the small helper modules under `modules/utils`. They are
used across the codebase for data loading, Excel formatting and simple
calculations.

```text
modules/
├── config_utils.py
├── logging_utils.py
└── utils/
    ├── data_utils.py
    ├── math_utils.py
    └── progress_utils.py
```

## `data_utils`
Safe wrappers around common pandas operations.

### Example
```python
from pathlib import Path
from modules.utils import read_csv_if_exists, strip_timezones

df = read_csv_if_exists(Path("prices.csv"))
if df is not None:
    df = strip_timezones(df)
```


## `math_utils`
Small mathematical helpers used in analytics modules.

### Example
```python
from modules.utils import moving_average
ma = moving_average(prices["Close"], window=20)
```

## `progress_utils`
Wraps an iterable with an optional `tqdm` progress bar. If `tqdm` is not
installed the function simply yields the values without a bar.

### Example
```python
for item in progress_iter(items, description="Processing"):
    handle(item)
```

See [logging.md](logging.md) for details on setting up application logging.
