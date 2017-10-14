from bs4 import BeautifulSoup

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


class WindowException(Exception):
    """exception for not opened windows"""
    def __init__(self):
        err = "window hasn't been opened yet"
        logger.error(err)
        super().__init__(err)


class CredentialsException(Exception):
    """credential exception"""
    def __init__(self, username):
        err = "wrong credentials for %s" % username
        logger.error(err)
        super().__init__(err)


class WidgetException(Exception):
    """in case of pop-up"""
    def __init__(self, message):
        soup = BeautifulSoup(message.html, 'html.parser')
        err = soup.select("div.text")[0].text
        logger.error(err)
        super().__init__(err)


class MaxQuantLimit(Exception):
    """in case of maximum quantity exceeding"""
    def __init__(self, quant):
        self.quant = quant
        self.err = "max quantity reached, need to be below %d" % quant


class MinQuantLimit(Exception):
    """in case of minimum quantity exceeding"""
    def __init__(self, quant):
        self.quant = quant
        self.err = "min quantity reached, need to be above %d" % quant


class MarketClosed(Exception):
    """base exception for closed market"""
    def __init__(self):
        super().__init__()


class ProductNotFound(Exception):
    def __init__(self, product_name):
        err = "%s not found" % product_name
        logger.error(err)
        super().__init__(err)
