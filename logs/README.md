# Log Files

The `logs/` directory stores runtime output from the application. By default all
utilities log to `logs/fundalyze.log` when `modules.logging_utils.setup_logging`
is called.

The log format follows:

```
YYYY-MM-DD HH:MM:SS [LEVEL] logger_name: message
```

Example line:

```
2025-06-05 12:48:24 [DEBUG] urllib3.connectionpool: Starting new HTTPS connection (1): finviz.com:443
```

## Rotation

There is currently **no automatic rotation** built into the logging
configuration. The log file grows indefinitely until removed. If long term
logging is required, consider using an external tool such as `logrotate` or
extending `setup_logging()` to use `RotatingFileHandler` from `logging.handlers`.

## Logging Levels

`setup_logging()` configures the root logger to the desired level (default:
`DEBUG`). Modules request loggers via `logging.getLogger(__name__)` and inherit
this level. Typical usage is `DEBUG` during development and `INFO` or higher for
production. Messages are written both to the log file and to the console.

## Flushing

Python's `logging` module handles flushing internally. When the program exits or
when handlers are closed, log buffers are flushed automatically. The library
does not call `flush()` explicitly.
