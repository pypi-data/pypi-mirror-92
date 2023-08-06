from datetime import datetime
import time
import logging
import sys


class Timer(object):
    def __init__(self, func):
        self._func_ = func

    def __call__(self, *args, **kwargs):
        start = datetime.now()
        self._func_(*args, **kwargs)
        end = datetime.now()
        print(f"{self._func_.__name__} Time Cost {(end - start).seconds} s")


class KeyInterruptHandler(object):
    def __init__(self, func):
        self._func_ = func

    def __call__(self, *args, **kwargs):
        try:
            self._func_(*args, **kwargs)
        except KeyboardInterrupt:
            logging.critical("Detect Keyboard Interrupt. Exit.")
            sys.exit(1)

