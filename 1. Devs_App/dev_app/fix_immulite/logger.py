# -*- coding: utf-8 -*-
# DEBUG > INFO > WARNING > ERROR > CRITICAL

import logging
import os
from logging.handlers import RotatingFileHandler

class RotateLogger():
    def __init__(self, name = "Minicap", fpath=os.path.join(os.getcwd(),"log.log"), fsize=100000000, bk_count=3, level=logging.DEBUG): 
        self.log = logging.getLogger(name)
        self.log.setLevel(level)
        handler = RotatingFileHandler(fpath, maxBytes=fsize, backupCount=bk_count)
        handler.setFormatter(\
                logging.Formatter(\
                        '%(asctime)s - %(levelname)-8s - %(threadName)s - %(message)s',
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

if __name__ == "__main__":
    t = RotateLogger(__name__,'log.log',10000000,9,level="DEBUG")
    t.info("ABC")
    t.info("CBA")

