from os import path
import sys
import re
import logging
import logging.config
from datetime import datetime
from .color import *


class logger(object):
    logging.config.fileConfig(
        path.join(path.dirname(__file__), 'logging.conf'))
    logging.getLogger().setLevel(getattr(logging, 'DEBUG'))

    def setlevel(level):
        logging.getLogger().setLevel(getattr(logging, level.upper()))

    def debug(s):
        logging.debug(
            printer.process(
                '- ' + re.match(
                    r'\d+:\d+:\d+',
                    str(datetime.now().time())).group(0) + ' - ' + s))

    def info(s):
        logging.info(
            printer.info(
                    '- ' + re.match(
                        r'\d+:\d+:\d+',
                        str(datetime.now().time())).group(0) + ' - ' + s))

    def warning(s):
        logging.warning(
            printer.warning(
                '- ' + re.match(
                    r'\d+:\d+:\d+',
                    str(datetime.now().time())).group(0) + ' - ' + yellow(s)))

    def error(s):
        logging.error(
            printer.error(
                '- ' + re.match(
                    r'\d+:\d+:\d+',
                    str(datetime.now().time())).group(0) + ' - ' + red(s)))

    def critical(s):
        logging.critical(
            printer.critical(
                '- ' + re.match(
                    r'\d+:\d+:\d+',
                    str(datetime.now().time())).group(0) +
                ' - ' + bold(red(s))))
