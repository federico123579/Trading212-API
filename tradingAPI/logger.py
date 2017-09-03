from os import path
import re
import logging
import logging.config
from datetime import datetime

from .color import *


class logger(object):
    def __init__(self, level='DEBUG'):
        logging.config.fileConfig(path.join(path.dirname(__file__), 'logging.conf'))
        logging.getLogger().setLevel(getattr(logging, level))

    def debug(self, s):
        logging.debug(printer.process('- ' + re.match(r'\d+:\d+:\d+',
            str(datetime.now().time())).group(0) + ' - ' + s))

    def info(self, s):
        logging.info(printer.info('- ' + re.match(r'\d+:\d+:\d+',
            str(datetime.now().time())).group(0) + ' - ' + s))

    def warning(self, s):
        logging.warning(printer.warning('- ' + re.match(r'\d+:\d+:\d+',
            str(datetime.now().time())).group(0) + ' - ' + yellow(s)))

    def error(self, s):
        logging.error(printer.error('- ' + re.match(r'\d+:\d+:\d+',
            str(datetime.now().time())).group(0) + ' - ' + red(s)))

    def critical(self, s):
        logging.critical(printer.critical('- ' + re.match(r'\d+:\d+:\d+',
            str(datetime.now().time())).group(0) + ' - ' + bold(red(s))))
