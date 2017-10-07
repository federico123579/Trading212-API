# -*- coding: utf-8 -*-

"""
tradingAPI.saver
~~~~~~~~~~~~~~

This module is used for saving valueble data.
"""

import os
import os.path
import yaml
from .patterns import Observer, Observable, Singleton

# logging
import logging
logger = logging.getLogger('tradingAPI.saver')


class Saver(Observable):
    """save data"""
    def __init__(self, path, name):
        self._observers = []
        self.name = name
        self.config_file = path
        self.config = {}

    def read(self):
        self.checkFile()
        with open(self.config_file, 'r') as f:
            yaml_dict = yaml.load(f)
            logger.debug('yaml: ' + str(yaml_dict))
            if yaml_dict is not None:
                self.config = yaml_dict
        self.notify_observers(event='update', data=self.config)
        return self.config

    def save(self):
        self.checkFile()
        if not self.config:
            logger.error("nothing to save (config not exists)")
            raise NotImplemented()
        with open(self.config_file, 'w') as f:
            f.write(yaml.dump(self.config))
        logger.debug("saved data")

    def checkFile(self):
        if not os.path.isfile(self.config_file):
            directory = os.path.dirname(self.config_file)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(self.config_file, 'w') as f:
                pass

    def add_val(self, val):
        """add value in form of dict"""
        if not isinstance(val, type({})):
            raise ValueError(type({}))
        self.read()
        self.config.update(val)
        self.save()


class Collector(Observer, metaclass=Singleton):
    """collect all data"""
    def __init__(self):
        self.collection = {}

    def notify(self, observable, event, data):
        if event == 'update' and isinstance(data, type({})):
            logger.debug("observer notified")
            self.collection[observable.name] = data
