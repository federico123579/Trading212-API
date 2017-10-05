# logging
import logging
logger = logging.getLogger('tradingAPI.exceptions')


class BaseExc(BaseException):
    """for all other exceptions"""
    def __init__(self, exc):
        logger.error(f"Caught exception: {exc}")
        raise exc


class VBroException(Exception):
    """virtual display exception"""
    def __init__(self):
        err = "virtual display failed to launch"
        logger.error(err)
        super().__init__(err)


class BrowserException(Exception):
    """selenium browser exception"""
    def __init__(self, brow, msg):
        err = f"browser {brow} {msg}"
        logger.error(err)
        super().__init__(err)


class CredentialsException(Exception):
    """credential exception"""
    def __init__(self, username):
        err = "wrong credentials for {username}"
        logger.error(err)
        super().__init__(err)
