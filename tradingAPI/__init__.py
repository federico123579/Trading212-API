from tradingAPI.api import API
from tradingAPI.low_level import LowLevelAPI
import os.path
import logging
import logging.config


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'deafult': {
            'format':
                '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'mov_form': {
            'format': '%(asctime)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'deafult',
        },
        'rotating': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'deafult',
            'filename': os.path.join(
                os.path.dirname(__file__), 'logs/logfile.log'),
            'when': 'midnight',
            'backupCount': 3
        },
        'movs_handler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'mov_form',
            'filename': os.path.join(
                os.path.dirname(__file__), 'logs/movlist.log'),
            'mode': 'w'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'CRITICAL',
            'propagate': True
        },
        'tradingAPI': {
            'handlers': ['rotating'],
            'level': 'DEBUG'
        },
        'mover': {
            'handlers': ['movs_handler'],
            'level': 'INFO'
        }
    }
})

__VERSION__ = "v0.2rc1"
