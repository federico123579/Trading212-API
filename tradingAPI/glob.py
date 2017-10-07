# -*- coding: utf-8 -*-

"""
tradingAPI.glob
~~~~~~~~~~~~~~

This module provides the globals.
"""

import os.path
from .links import file_path
from .patterns import Singleton
from .saver import Saver, Collector

# logging
import logging
logger = logging.getLogger('tradingAPI.globals')


class Glob(object, metaclass=Singleton):
    def __init__(self):

        def conf_new(name):
            """configure new handler"""
            hand_name = (name + 'Handler')
            logger.debug("initialized %s" % hand_name)
            setattr(self, hand_name, Saver(file_path[name], name))
            configured = getattr(self, hand_name)
            configured.register_observer(self.theCollector)
            configured.read()

        # init Observer
        self.theCollector = Collector()
        logger.debug("initialized observer")
        # init Observables
        conf_new('pip')
        conf_new('unit_value')
        logger.debug("initialized observables")
