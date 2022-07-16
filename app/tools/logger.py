"""Logger definitions."""
import logging
import logging.handlers
import queue

from logging.handlers import QueueHandler, QueueListener, TimedRotatingFileHandler
from typing import Any

from ansi2html import Ansi2HTMLConverter

logger = logging.getLogger()


def log_to_html(log_file: str):
    """Convert ANSI log to HTML."""
    with open(log_file, mode="r", encoding="UTF-8") as log:
        content = log.read()

    conv = Ansi2HTMLConverter()
    return conv.convert(content)


def init_logger(
    log_file: str, rotate_days: int | None = None, loglevel: Any = logging.INFO
) -> None:
    """Initialize the logger."""
    fmt = "%(asctime)s | %(levelname)8s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    # logging.basicConfig(format=fmt, level=logging.INFO, datefmt=datefmt)
    global logger
    logger.setLevel(loglevel)

    # stdout logger
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(loglevel)
    stdout_handler.setFormatter(ColorLogger(fmt=fmt, datefmt=datefmt))

    # File logger
    file_handler: logging.handlers.RotatingFileHandler | logging.handlers.TimedRotatingFileHandler
    if rotate_days:
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_file, when="midnight", backupCount=rotate_days
        )
    else:
        file_handler = logging.handlers.RotatingFileHandler(log_file, backupCount=1)

    file_handler.doRollover()

    file_handler.setLevel(loglevel)
    file_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))

    # Queue handler
    que = queue.Queue(-1)  # no limit on size
    queue_handler = QueueHandler(que)
    listener = QueueListener(que, file_handler, stdout_handler)

    logger.addHandler(queue_handler)

    listener.start()


class ColorLogger(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    cyan = "\x1b[96m"
    green = "\x1b[92m"

    def __init__(self, fmt, datefmt):
        super().__init__()
        self.fmt = fmt
        self.datefmt = datefmt
        self.FORMATS = {
            logging.DEBUG: self.cyan + self.fmt + self.reset,
            logging.INFO: self.green + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
