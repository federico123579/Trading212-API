import time
import selenium.common.exceptions
import re
from datetime import datetime
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from splinter import Browser
from tradingAPI import exceptions
from .links import path

# logging
import logging
logger = logging.getLogger('tradingAPI')


def expect(func, args, times=7, sleep_t=0.5):
    """try many times as in times with sleep time"""
    while times > 0:
        try:
            return func(*args)
        except Exception as e:
            times -= 1
            time.sleep(sleep_t)
            if times == 0:
                raise exceptions.BaseExc(e)


def num(string):
    """convert a string to float"""
    try:
        string = re.sub('[^a-zA-Z0-9\n\.]', '', string)
        number = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", string)
        return float(number[0])
    except Exception as e:
        logger = logging.getLogger('tradingAPI.num')
        logger.debug("number not found in %s" % string)
        return None


class AbstractAPI(object):
    def __init__(self, brow="firefox"):
        self.brow_name = brow
        # init virtual Display
        self.vbro = Display()

    def launch(self):
        """launch browser and virtual display"""
        try:
            self.vbro.start()
            logger.debug("virtual display launched")
        except Exception:
            raise exceptions.VBroException()
        try:
            self.browser = Browser(self.brow_name)
            logger.debug(f"browser {self.brow_name} launched")
        except Exception:
            raise exceptions.BrowserException(
                self.brow_name, "failed to launch")
        return True

    def css(self, css_path, dom=None):
        """css find function abbreviation"""
        if dom is None:
            dom = self.browser
        return expect(dom.find_by_css, args=[css_path])

    def css1(self, css_path, dom=None):
        """return the first value of self.css"""
        if dom is None:
            dom = self.browser
        return self.css(css_path, dom)[0]

    def search_name(self, name, dom=None):
        """name find function abbreviation"""
        if dom is None:
            dom = self.browser
        return expect(dom.find_by_name, args=[name])

    def xpath(self, xpath, dom=None):
        """xpath find function abbreviation"""
        if dom is None:
            dom = self.browser
        return expect(dom.find_by_xpath, args=[xpath])

    def elCss(self, css_path, dom=None):
        """check if element is present by css"""
        if dom is None:
            dom = self.browser
        return expect(dom.is_element_present_by_css, args=[css_path])

    def elXpath(self, xpath, dom=None):
        """check if element is present by css"""
        if dom is None:
            dom = self.browser
        return expect(dom.is_element_present_by_xpath, args=[xpath])

    def login(self, username, password, mode="demo"):
        """login function"""
        url = "https://trading212.com/it/login"
        try:
            logger.debug(f"visiting %s" % url)
            self.browser.visit(url)
            logger.debug(f"connected to %s" % url)
        except selenium.common.exceptions.WebDriverException:
            logger.critical("connection timed out")
            raise
        try:
            self.search_name("login[username]").fill(username)
            self.search_name("login[password]").fill(password)
            self.css1(path['log']).click()
            # define a timeout for logging in
            timeout = time.time() + 30
            while not self.elCss(path['logo']):
                if time.time() > timeout:
                    logger.critical("login failed")
                    raise CredentialsException(username)
            time.sleep(1)
            logger.info(f"logged in as {username}")
            # check if it's a weekend
            if mode == "demo" and datetime.now().isoweekday() in range(6, 8):
                timeout = time.time() + 10
                while not self.elCss(path['alert-box']):
                    if time.time() > timeout:
                        logger.warning(
                            "weekend trading alert" +
                            "box not closed")
                        break
                if self.elCss(path['alert-box']):
                    self.css1(path['alert-box']).click()
        except Exception as e:
            logger.critical("login failed")
            raise exceptions.BaseExc(e)
        return True

    def logout(self):
        """logout func (quit browser)"""
        try:
            self.browser.quit()
        except Exception:
            raise exceptions.BrowserException(self.brow_name, "not started")
            return False
        self.vbro.stop()
        logger.info("logged out")
        return True

    def get_bottom_info(self, info):
        accepted_values = {
            'free_funds': 'equity-free',
            'account_value': 'equity-total',
            'live_result': 'equity-ppl',
            'used_margin': 'equity-margin'}
        try:
            info_label = accepted_values[info]
            val = self.css1("div#%s span.equity-item-value" % info_label).text
            return num(val)
        except KeyError as e:
            raise exceptions.BaseExc(e)

    def get_price(self, name):
        soup = BeautifulSoup(
            self.css("div.scrollable-area-content")[1].html, "html.parser")
        for product in soup.select("div.tradebox"):
            fullname = product.select("span.instrument-name")[0].text.lower()
            if fullname.find(name.lower()) != -1:
                mark_closed_list = [x for x in product.select(
                    "div.quantity-list-input-wrapper") if x.select(
                    "div.placeholder")[0].text.lower().find("close") != -1]
                if mark_closed_list:
                    sell_price = product.select("div.tradebox-price-sell")[0]\
                        .text
                    return float(sell_price)
                else:
                    return False

    class MovementWindow(object):
        """add movement window"""
        def __init__(self, api, name):
            self.api = api
            self.name = name
            self.insfu = False

        def open(self, name_counter=None):
            """open the window"""
            if self.api.css1(path['add-mov']).visible:
                self.api.css1(path['add-mov']).click()
            else:
                self.api.css1('span.dataTable-no-data-action').click()
            self.api.css1(path['search-box']).fill(self.name)
            if self.get_result(0) is None:
                logger.error("%s not found" % self.name)
                self.close_mov()
                raise ValueError('%s not found in mov list' % self.name)
            result, name = self.search_res(self.name, name_counter)
            result.click()
            if self.elCss("div.widget_message"):
                self.decode(self.api.css1("div.widget_message"))
            self.name = name

        def close(self):
            """close a movement"""
            self.api.css1(path['close']).click()

        def search_res(self, res, check_counter=None):
            """search for a res"""
            result = self.get_result(0)
            name = self.get_research_name(result)
            x = 0
            while not self.check_name(res, name, counter=check_counter):
                name = self.get_research_name(self.get_result(x))
                logger.debug(name)
                if self.check_name(res, name, counter=check_counter):
                    return self.get_result(x)
                x += 1
            return result, name

        def check_name(self, name, string, counter=None):
            """if both in string return False"""
            name = name.lower()
            string = string.lower()
            if counter is None:
                if name in string:
                    return True
                else:
                    return False
            counter = counter.lower()
            if name in string and counter in string:
                logger.debug("check_name: counter found in string")
                return False
            elif name in string and counter not in string:
                return True
            else:
                return False

        def get_research_name(self, res):
            """return result name"""
            return self.api.css1("span.instrument-name", res).text

        def get_result(self, pos):
            """get pos result, where 0 is first"""
            evalxpath = path['res'] + f"[{pos + 1}]"
            try:
                return self.api.xpath(evalxpath)[0]
            except Exception:
                return None

        def set_limit(self, mode, value):
            """set limit in movement window"""
            if not isinstance((), type(value)):
                value = (value, value)
            if mode not in ["buy", "sell"]:
                raise ValueError()
            self.xpath(path['limit-gain-' + mode])[0].fill(str(value[0]))
            self.xpath(path['limit-loss-' + mode])[0].fill(str(value[1]))

        def decode(self, message):
            """decode text pop-up"""
            title = self.api.css1("div.title", message).text
            text = self.api.css1("div.text", message).text
            if title == "Insufficient Funds":
                self.insfu = True

        def decode_update(self, message, value, mult=0.1):
            """decode and update the value"""
            try:
                msg_text = self.api.css1("div.text", message).text
                return num(msg_text)
            except Exception:
                if msg_text.lower().find("higher") != -1:
                    value += value * mult
                    return value
                else:
                    self.decode(message)
                    return None

        def get_mov_margin(self):
            """get the margin of the movement"""
            return num(self.css1("span.cfd-order-info-item-value").text)

        def set_quantity(self, quant):
            """set quantity"""
            self.css(path['quantity'])[0].fill(str(quant))
            self.quantity = quant

    def new_mov(self, name):
        return self.MovementWindow(self, name)
