import time
import re
import selenium.common.exceptions
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from splinter import Browser
from datetime import datetime
from .exceptions import *
from .logger import logger
from .color import *
from .data import *


class API(object):
    '''Interface object'''

    def __init__(self, level="debug"):
        self.movements = []
        self.stocks = []
        self.logger = logger(level)
        self.vbro = Display()

    def __find(self, func, arg, fails=3, sleep_t=0.5):
        n = 0
        while n <= fails:
            try:
                if func == 'css':
                    result = self.browser.find_by_css(arg)
                elif func == 'name':
                    result = self.browser.find_by_name(arg)
                return result
            except Exception as e:
                exc = e
                fails += 1
                time.sleep(sleep_t)
        self.logger.error(exc)
        return 0

    def _css(self, css_path):
        '''css find function abbreviation'''
        return self.__find('css', css_path)

    def _name(self, name):
        '''name find function abbreviation'''
        return self.__find('name', name)

    def _elCss(self, css_path):
        '''check if element is present by css'''
        return self.browser.is_element_present_by_css(css_path)

    def _num(self, string):
        '''convert a string to float'''
        number = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+",
                            string.replace(' ', ''))[0]
        return float(number)

    def launch(self, brow="firefox"):
        '''launch browser and virtual display'''
        try:
            self.vbro.start()
            self.logger.debug("virtual display launched")
        except Exception:
            self.logger.critical("virtual display failed to launch")
            return 0
        try:
            self.browser = Browser(brow)
            self.logger.debug("browser {brow} launched".format(brow=brow))
        except Exception as e:
            self.logger.critical("browser {brow} failed to launch"
                                 .format(brow=brow))
            self.logger.critical(e)
            return 0
        return 1

    def login(self, username, password, mode="demo"):
        '''Login function'''
        url = "https://trading212.com/it/login"
        try:
            self.browser.visit(url)
            self.logger.debug("visiting {url}".format(url=url))
        except selenium.common.exceptions.WebDriverException:
            self.logger.critical("connection timed out")
            return 0
        try:
            self._name("login[username]").fill(username)
            self._name("login[password]").fill(password)
            self._css(path['log']).click()
            timeout = time.time() + 30
            while not self._elCss(path['logo']):
                if time.time() > timeout:
                    self.logger.critical("login failed")
                    return 0
            time.sleep(1)
            self.logger.info("logged in as {}".format(bold(username)))
            # check if it's a weekend
            if mode == "demo" and datetime.now().isoweekday() in range(6, 8):
                timeout = time.time() + 10
                while not self._elCss(path['alert-box']):
                    if time.time() > timeout:
                        self.logger.warning("weekend trading alert" +
                                            "box not closed")
                        break
                if self._elCss(path['alert-box']):
                    self._css(path['alert-box'])[0].click()
            return 1
        except Exception:
            self.logger.critical("login failed")
            return 0

    def logout(self):
        '''logout func (to quit browser)'''
        try:
            self.browser.quit()
        except Exception:
            raise BrowserException("browser not started")
            return 0
        self.vbro.stop()
        self.logger.info("Logged out")
        return 1

    def __get_mov_margin(self):
        time.sleep(0.5)
        return self._num(self._css("span.cfd-order-info-item-value")[0].text)

    def __set_limit(self, mode, value=()):
        if not isinstance((), type(value)):
            value = (value, value)
        self._css(path['limit-gain-' + mode]
                  )[0].fill(str(value[0]))
        self._css(path['limit-loss-' + mode]
                  )[0].fill(str(value[1]))

    def __decode(self, message):
        title = message.find_by_css("div.title")[0].text
        text = message.find_by_css("div.text")[0].text
        if title == "Insufficient Funds":
            return 'INSFU'
        else:
            return 0

    def _decode_n_update(self, message, value, mult=0.1):
        try:
            msg_text = message.find_by_css("div.text")[0].text
            return self._num(msg_text)
        except Exception:
            if msg_text.lower().find("higher") != -1:
                value += value * mult
                return value
            else:
                return self.__decode(message)

    def addMov(self, product, quantity=None, mode="buy", stop_limit=None,
               auto_quantity=None):
        '''Add movement function'''
        if self._css(path['add-mov'])[0].visible:
            self._css(path['add-mov'])[0].click()
        else:
            self._css('span.dataTable-no-data-action')[0].click()
        self._css(path['search-box'])[0].fill(product)
        if not self._elCss(path['first-res']):
            self.logger.error("{product} not found".format(
                product=underline(product)))
            self._css('span.orderdialog-close')[0].click()
            return 0
        self._css(path['first-res'])[0].click()
        self._css(path[mode + '-btn'])[0].click()
        # override quantity
        if quantity is not None and auto_quantity is not None:
            self.logger.warning("quantity and auto_quantity are exclusive, " +
                                "overriding quantity")
            quantity = None
        # set quantity
        if quantity is not None:
            self._css(path['quantity'])[0].fill(str(quantity))
        # auto_quantity calculate quantity
        if auto_quantity is not None:
            # set the maximum quantity
            right_arrow = self._css("span.quantity-slider-right-arrow")[0]
            left_arrow = self._css("span.quantity-slider-left-arrow")[0]
            last_margin = None
            while last_margin != self.__get_mov_margin():
                last_margin = self.__get_mov_margin()
                right_arrow.click()
                if self._css('div.widget_message'):
                    widget = self.__decode(self._css('div.widget_message'))
                    # in case of errors
                    if widget == 'INSFU':
                        self.logger.warning("Insufficient funds to buy {}"
                                            .format(product))
                        self._css("span.orderdialog-close")[0].click()
                        return 0
            # and descend
            while self.__get_mov_margin() > auto_quantity:
                left_arrow.click()
                # check if margin is too high
                quantity = self._css(path['quantity'])[0].value
                if not quantity:
                    self.logger.warning(
                        "Failed to add movement of {} ".format(product) +
                        "cause of margin too high")
                    self._css("span.orderdialog-close")[0].click()
                    return 0
        # check margin and quantity used
        margin = self.__get_mov_margin()
        quantity = self._css(path['quantity'])[0].value
        # set stop_limit
        if stop_limit is not None:
            try:
                self.__set_limit(stop_limit['mode'], stop_limit['value'])
                self._css(path['confirm-btn'])[0].click()
                if self._elCss('div.widget_message'):
                    while self._elCss('div.widget_message'):
                        num = self._decode_n_update(
                            self._css('div.widget_message'),
                            stop_limit['value'])
                        self.__set_limit('unit', num)
                        self._css(path['confirm-btn'])[0].click()
            except Exception as e:
                self.logger.error(e)
                self._css("span.orderdialog-close")[0].click()
        else:
            self._css(path['confirm-btn'])[0].click()
        self.logger.info("Added movement of {} {} "
                         .format(bold(quantity), bold(product)) +
                         "with limit {} and margin of {}"
                         .format(bold(stop_limit['value']), margin))
        time.sleep(1)
        return 1

    def closeMov(self, mov_id):
        '''close a position'''
        self._css("#" + mov_id + " div.close-icon")[0].click()
        self.browser.find_by_text("OK")[0].click()
        time.sleep(1.5)
        if self._elCss("#" + mov_id + " div.close-icon"):
            self.logger.error("failed to close mov {id}".format(id=mov_id))
            return 0
        else:
            self.logger.info("closed mov {id}".format(id=bold(mov_id)))
            return 1

    def checkPos(self):
        '''check all current positions'''
        soup = BeautifulSoup(
            self._css("tbody.dataTable-show-currentprice-arrows").html,
            "html.parser")
        movs = []
        count = 0
        for x in soup.find_all("tr"):
            try:
                prod_id = x['id']
                product = x.select("td.name")[0].text
                quant = x.select("td.quantity")[0].text
                if "direction-label-buy" in soup.find_all("tr")[0] \
                        .select("td.direction")[0].span['class']:
                    mode = "long"
                else:
                    mode = "short"
                price = self._num(x.select("td.averagePrice")[0].text)
                earn = self._num(x.select("td.ppl")[0].text)
                mov = Movement(prod_id, product, quant, mode, price, earn)
                movs.append(mov)
                count += 1
            except Exception as e:
                self.logger.error(e)
        self.logger.debug(
            "{count} positions updated".format(count=bold(count)))
        self.movements = movs
        return 1

    def checkStocks(self, stocks):
        '''check specified stocks (list)'''
        soup = BeautifulSoup(
            self._css("div.scrollable-area-content").html, "html.parser")
        count = 0
        for product in soup.select("div.tradebox"):
            name = product.select("span.instrument-name")[0].text.lower()
            if [x for x in stocks if name.find(x) != -1]:  # to tidy up
                if not [x for x in self.stocks if x.name == name]:
                    self.stocks.append(Stock(name))
                stock = [x for x in self.stocks if x.name == name][0]
                mark_closed_list = [x for x in product.select(
                    "div.quantity-list-input-wrapper") if x.select(
                    "div.placeholder")[0].text.lower().find("close") != -1]
                if len(mark_closed_list) != 0:
                    market = False
                else:
                    market = True
                stock.market = market
                if market is True:
                    sell_price = product.select("div.tradebox-price-sell")[0]\
                        .text
                    raw_sent = product.select(
                        "span.tradebox-buyers-container.number-box")[0].text
                    try:
                        sent = (int(raw_sent.strip('%')) / 100)
                    except Exception as e:
                        self.logger.warning(e)
                        sent = None
                    stock.addVar([sell_price, sent])
                    count += 1
        self.logger.debug("added {count} stocks".format(count=bold(count)))
        return 1

    def addPrefs(self, prefs):
        '''add prefered stocks'''
        try:
            for pref in prefs:
                self._css(path['search-btn'])[0].click()
                self._css(path['all-tools'])[0].click()
                self._css(path['search-pref'])[0].fill(pref)
                if self._elCss(path['plus-icon']):
                    self._css(path['add-btn'])[0].click()
                if self._elCss('span.btn-primary'):
                    self._css('span.btn-primary')[0].click()
            self._css(path['close-prefs'])[0].click()
            self.logger.info("added {prefs} to preferencies".format(
                prefs=', '.join([bold(x) for x in prefs])))
            self._css("span.prefs-icon-node")[0].click()
            self._css(
                "div.item-tradebox-prefs-menu-list-sentiment_mode")[0].click()
            self._css("span.equity-menu-btn-icon")[0].click()
            self._css("div.equity-menu-items-list ")[0].click()
            self._css("span.prefs-icon-node")[0].click()
            self.logger.debug("set sentiment mode")
            self._css("span.equity-menu-btn-icon")[0].click()
            info_list = self._css("div.equity-menu-items-list")[0]
            prefs_info_list = ['Free funds', 'Used margin']
            for pref_info in prefs_info_list:
                checkbox = info_list.find_by_text(pref_info)[-1]
                if 'selected' not in checkbox['class'].split(' '):
                    checkbox.find_by_css("svg")[0].click()
            self._css("span.equity-menu-btn-icon")[0].click()
            self.logger.debug("set bottom info")
            return 1
        except Exception as e:
            self.logger.error(e)
            return 0

    def clearPrefs(self):
        '''clear all stock preferencies'''
        try:
            self._css(path['search-btn'])[0].click()
            self._css(path['all-tools'])[0].click()
            for res in self._css("div.search-results-list-item"):
                if not res.find_by_css(path['plus-icon']):
                    res.find_by_css(path['add-btn'])[0].click()
            self._css('div.widget_message span.btn')[0].click()
            # fix errors
            self._css(path['close-prefs'])[0].click()
            while not self._elCss(path['search-btn']):
                time.sleep(0.5)
            self.logger.debug("cleared preferencies")
            return 1
        except Exception as e:
            self.logger.error(e)
            return 0

    def get_bottom_info(self, info):
        accepted_values = {
            'free_funds': 'equity-free',
            'account_value': 'equity-total',
            'live_result': 'equity-ppl',
            'used_margin': 'equity-margin'}
        if accepted_values.get(info):
            val = self._css("div#" + accepted_values[info] +
                            " span.equity-item-value")[0].text
            return self._num(val)
        else:
            return 0


class Movement(object):
    def __init__(self, prod_id, product, quantity, mode, price, earn):
        self.id = prod_id
        self.product = product
        self.quantity = quantity
        self.mode = mode
        self.price = price
        self.earn = earn


class Stock(object):
    def __init__(self, name):
        self.name = name
        self.market = False
        self.vars = []

    def addVar(self, var):
        '''add a variation (list)'''
        self.vars.append(var)
