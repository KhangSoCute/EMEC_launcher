# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

class RotateLogger():
    def __init__(self, name, fpath, fsize, count, level=logging.ERROR):
        self.log = logging.getLogger(name)
        self.log.setLevel(level)
        handler = RotatingFileHandler(fpath, maxBytes=fsize, backupCount=count)
        handler.setFormatter(\
                logging.Formatter(\
                        '%(asctime)s - %(levelname)-8s - -%(threadName)s - %(message)s',
                        '%Y-%m-%d %H:%M:%S'))
        self.log.addHandler(handler)

    def debug(self, msg, *args, **kwargs):
        self.log.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.log.exception(msg, *args, exc_info=True, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log.critical(msg, *args, **kwargs)

    def shutdown(self):
        logging.shutdown()
