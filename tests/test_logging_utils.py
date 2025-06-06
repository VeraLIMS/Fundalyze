import logging
from modules.logging_utils import setup_logging


def test_setup_logging_creates_file_and_logs(tmp_path):
    log_file = tmp_path / "test.log"
    logging.getLogger().handlers.clear()
    setup_logging(str(log_file))
    assert log_file.is_file()
    logging.getLogger().info("hello")
    for h in logging.getLogger().handlers:
        if hasattr(h, "flush"):
            h.flush()
    content = log_file.read_text()
    assert "hello" in content
    assert "INFO" in content
    logging.getLogger().handlers.clear()
