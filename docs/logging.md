# Logging

`modules.logging_utils` provides a single helper `setup_logging()` for
configuring the root logger. It writes messages to both the console and a
log file using the format:

```
YYYY-MM-DD HH:MM:SS [LEVEL] logger: message
```

Example log entries:
```
2025-06-05 12:47:50 [INFO] numexpr.utils: NumExpr defaulting to 16 threads.
2025-06-05 12:47:51 [DEBUG] matplotlib: interactive is False
```

## Usage
```python
from modules.logging_utils import setup_logging

# Creates logs/fundalyze.log and sets the root level to DEBUG
setup_logging("logs/fundalyze.log", level=logging.DEBUG)
```
The directory is created automatically if it does not exist. After calling
`setup_logging` you can use the standard `logging` API throughout the project.
