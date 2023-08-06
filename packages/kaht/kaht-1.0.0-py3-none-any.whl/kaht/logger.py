import logging
from rich.logging import RichHandler
from rich.console import Console
from typing import Callable
from logging import Logger as pylogger
import threading

NELL_FILE = '/dev/null'

inner_logger = Console().log


def logger(filename: str = NELL_FILE):
    FORMAT = "[line %(lineno)d] %(asctime)s %(levelname)s: %(message)s"
    inner_logger(f"Will Log in {filename}")
    logging.basicConfig(
            level="NOTSET",
            format=FORMAT,
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=filename
    )
    log = logging.getLogger("rich")
    log.addHandler(RichHandler())
    return log


class LoggerMixIn:
    info: Callable
    warning: Callable
    warn: Callable
    debug: Callable
    critical: Callable

    def register_logger(self, _logger: pylogger):
        self.info = _logger.info
        self.warn = _logger.warning
        self.warning = _logger.warning
        self.debug = _logger.debug
        self.critical = _logger.critical


class Logger:
    _shared_lock_ = threading.Lock()

    def __init__(self, filename: str = NELL_FILE):
        FORMAT = "[%(filename)s line %(lineno)d] %(asctime)s %(levelname)s: %(message)s"
        inner_logger(f"Will Log in {filename}")
        logging.basicConfig(
                level="NOTSET",
                format=FORMAT,
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=filename
        )
        log = logging.getLogger("rich")
        log.addHandler(RichHandler())
        self.logger = log

    @classmethod
    def shared(cls, *args, **kwargs):
        if not hasattr(Logger, "__shared__"):
            with Logger._shared_lock_:
                if not hasattr(Logger, "__shared__"):
                    Logger.__shared__ = Logger(*args, **kwargs)
        return Logger.__shared__.logger
