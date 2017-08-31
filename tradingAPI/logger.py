from os import path
import sys
import re
import logging
import logging.config
from datetime import datetime

from .color import *

conv = {'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL}


class logger(object):
    def __init__(self, level='DEBUG'):
        logging.config.fileConfig(path.join(path.dirname(__file__), 'logging.conf'))
        logging.getLogger('tradingapi').setLevel(conv[level])

    def debug(self, s):
        logging.info(printer.process('- ' + re.match(r'\d+:\d+:\d+',
            str(datetime.now().time())).group(0) + ' - ' + s))
    
    def info(self, s):
        logging.info(printer.info('- ' + re.match(r'\d+:\d+:\d+',
            str(datetime.now().time())).group(0) + ' - ' + s))
    
    def warning(self, s):
        logging.info(printer.warning('- ' + re.match(r'\d+:\d+:\d+',
            str(datetime.now().time())).group(0) + ' - ' + yellow(s)))
    
    def error(self, s):
        logging.info(printer.error('- ' + re.match(r'\d+:\d+:\d+',
            str(datetime.now().time())).group(0) + ' - ' + red(s)))
    
    def critical(self, s):
        logging.info(printer.critical('- ' + re.match(r'\d+:\d+:\d+',
            str(datetime.now().time())).group(0) + ' - ' + bold(red(s))))
        sys.exit()