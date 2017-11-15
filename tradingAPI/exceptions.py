from bs4 import BeautifulSoup

# logging
import logging
logger = logging.getLogger('tradingAPI.exceptions')


class BasicExc(Exception):
    """for all exceptions in this module"""
    def __init__(self, err):
        super().__init__(err)


class BaseExc(BaseException):
    """for all other exceptions"""
    def __init__(self, exc):
        logger.error(f"Caught exception: {exc}")
        raise exc


class VBroException(BasicExc):
    """virtual display exception"""
    def __init__(self):
        self.err = "virtual display failed to launch"
        super().__init__(self.err)


class BrowserException(BasicExc):
    """selenium browser exception"""
    def __init__(self, brow, msg):
        self.err = f"browser {brow} {msg}"
        super().__init__(self.err)


class WindowException(BasicExc):
    """exception for not opened windows"""
    def __init__(self):
        self.err = "window hasn't been opened yet"
        super().__init__(self.err)


class CredentialsException(BasicExc):
    """credential exception"""
    def __init__(self, username):
        self.err = "wrong credentials for %s" % username
        super().__init__(self.err)


class WidgetException(BasicExc):
    """in case of pop-up"""
    def __init__(self, message):
        soup = BeautifulSoup(message.html, 'html.parser')
        self.err = soup.select("div.text")[0].text
        super().__init__(self.err)


class MaxQuantLimit(BasicExc):
    """in case of maximum quantity exceeding"""
    def __init__(self, quant):
        if quant == 0:
            raise MaxProduct()
        self.quant = quant
        self.err = "max quantity reached, need to be below %d" % quant
        super().__init__(self.err)


class MinQuantLimit(BasicExc):
    """in case of minimum quantity exceeding"""
    def __init__(self, quant):
        self.quant = quant
        self.err = "min quantity reached, need to be above %d" % quant
        super().__init__(self.err)


class StopLimit(BasicExc):
    """in case of limit too high or too low"""
    def __init__(self, text, val):
        text = text.lower()
        if 'stop loss' in text:
            self.cat = 'loss'
        elif 'take profit' in text:
            self.cat = 'gain'
        elif all(x in text for x in ['higher', 'spread']):
            raise HigherSpread()
        else:
            raise ValueError("category not found in %s" % text)
        self.err = "%s limit too close, need to be above %f" % (self.cat, val)
        self.val = val
        super().__init__(self.err)


class HigherSpread(BasicExc):
    """in case of spread too low"""
    def __init__(self):
        self.err = "limit too low, need to be over spread"
        super().__init__(self.err)


class PriceChange(BasicExc):
    """in case of price change"""
    def __init__(self, price):
        self.err = "price changed to %f" % price
        super().__init__(self.err)


class MarketClosed(Exception):
    """base exception for closed market"""
    def __init__(self):
        super().__init__()


class ProductNotFound(BasicExc):
    def __init__(self, product_name):
        self.err = "%s not found" % product_name
        super().__init__(self.err)


class MaxProduct(BasicExc):
    def __init__(self):
        self.err = "can't buy more of this product"
        super().__init__(self.err)
