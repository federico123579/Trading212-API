import re
import time
import selenium.common.exceptions
from bs4 import BeautifulSoup
from splinter import Browser
from datetime import datetime
from pyvirtualdisplay import Display
from .base.logger import logger
from .base.color import *
from .exceptions import *


# class AbstractAPI(object):
#     def __init__(self, level):
#         logger.setlevel(level)
#         self.vbro = Display()
#
#     def __try(self, func, args, fails=7, sleep_t=0.5):
#         fn = 0
#         while fn <= fails:
#             try:
#                 return func(*args)
#             except Exception as e:
#                 exc = e
#                 fn += 1
#                 time.sleep(sleep_t)
#                 if fails < fn:
#                     logger.error(exc)
#                     raise
#
#     def _css(self, css_path):
#         """css find function abbreviation"""
#         return self.__try(self.browser.find_by_css, args=(css_path,))
#
#     def _name(self, name):
#         """name find function abbreviation"""
#         return self.__try(self.browser.find_by_name, args=(name,))
#
#     def _xpath(self, xpath):
#         """xpath find function abbreviation"""
#         return self.__try(self.browser.find_by_xpath, args=(xpath,))
#
#     def _elCss(self, css_path):
#         """check if element is present by css"""
#         return self.browser.is_element_present_by_css(css_path)
#
#     def _elXpath(self, xpath):
#         """check if element is present by css"""
#         return self.browser.is_element_present_by_xpath(xpath)
#
#     def _num(self, string):
#         """convert a string to float"""
#         try:
#             string = re.sub('[^a-zA-Z0-9\n\.]', '', string)
#             number = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", string)
#             return float(number[0])
#         except Exception as e:
#             return False
#
#     def launch(self, brow="firefox", exe=None):
#         """launch browser and virtual display"""
#         try:
#             self.vbro.start()
#             logger.debug("virtual display launched")
#         except Exception:
#             logger.critical("virtual display failed to launch")
#             return False
#         try:
#             if brow == "firefox" and exe is not None:
#                 self.browser = Browser(brow, executable_path=exe)
#             elif brow == "firefox":
#                 self.browser = Browser(brow)
#             elif exe is not None:
#                 self.browser = Browser(brow, headless=True,
#                                        executable_path=exe)
#             else:
#                 self.browser = Browser(brow, headless=True)
#             logger.debug(f"browser {brow} launched")
#         except Exception as e:
#             logger.critical(f"browser {brow} failed to launch")
#             logger.critical(e)
#             return False
#         return True
#
#     def login(self, username, password, mode="demo"):
#         """Login function"""
#         url = "https://trading212.com/it/login"
#         try:
#             self.browser.visit(url)
#             logger.debug(f"visiting {url}")
#         except selenium.common.exceptions.WebDriverException:
#             logger.critical("connection timed out")
#             return False
#         try:
#             self._name("login[username]").fill(username)
#             self._name("login[password]").fill(password)
#             self._css(path['log']).click()
#             timeout = time.time() + 30
#             while not self._elCss(path['logo']):
#                 if time.time() > timeout:
#                     logger.critical("login failed")
#                     return False
#             time.sleep(1)
#             logger.info(f"logged in as {bold(username)}")
#             # check if it's a weekend
#             if mode == "demo" and datetime.now().isoweekday() in range(6, 8):
#                 timeout = time.time() + 10
#                 while not self._elCss(path['alert-box']):
#                     if time.time() > timeout:
#                         logger.warning(
#                             "weekend trading alert" +
#                             "box not closed")
#                         break
#                 if self._elCss(path['alert-box']):
#                     self._css(path['alert-box'])[0].click()
#             return True
#         except Exception:
#             logger.critical("login failed")
#             raise
#
#     def logout(self):
#         """logout func (quit browser)"""
#         try:
#             self.browser.quit()
#         except Exception:
#             raise BrowserException("browser not started")
#             return False
#         self.vbro.stop()
#         logger.info("Logged out")
#         return True
#
#     def _set_limit(self, mode, value):
#         if not isinstance((), type(value)):
#             value = (value, value)
#         try:
#             self._xpath(path['limit-gain-' + mode]
#                         )[0].fill(str(value[0]))
#             self._xpath(path['limit-loss-' + mode]
#                         )[0].fill(str(value[1]))
#         except Exception:
#             logger.error("set_limit failed")
#             raise
#
#     def _decode(self, message):
#         title = message.find_by_css("div.title")[0].text
#         text = message.find_by_css("div.text")[0].text
#         if title == "Insufficient Funds":
#             return 'INSFU'
#         else:
#             return None
#
#     def _decode_n_update(self, message, value, mult=0.1):
#         try:
#             msg_text = message.find_by_css("div.text")[0].text
#             return self._num(msg_text)
#         except Exception:
#             if msg_text.lower().find("higher") != -1:
#                 value += value * mult
#                 return value
#             else:
#                 return self._decode(message)
#
#     def get_bottom_info(self, info):
#         accepted_values = {
#             'free_funds': 'equity-free',
#             'account_value': 'equity-total',
#             'live_result': 'equity-ppl',
#             'used_margin': 'equity-margin'}
#         if accepted_values.get(info):
#             val = self._css("div#" + accepted_values[info] +
#                             " span.equity-item-value")[0].text
#             return self._num(val)
#         else:
#             return False
#
#     def get_mov_margin(self):
#         time.sleep(0.8)
#         try:
#             num = self._num(
#                 self._css("span.cfd-order-info-item-value")[0].text)
#             return num
#         except Exception:
#             logger.error("get_mov_margin failed")
#             raise
#
#     def _check_name(self, name, string, counter=None):
#         """if both in string return False"""
#         name = name.lower()
#         string = string.lower()
#         if counter is None:
#             if name in string:
#                 return True
#             else:
#                 return False
#         counter = counter.lower()
#         if name in string and counter in string:
#             logger.debug("check_name: counter found in string")
#             return False
#         elif name in string and counter not in string:
#             return True
#         else:
#             return False
#
#     def _get_result(self, pos):
#         """get pos result, where 0 is first"""
#         eval_xpath = path['res'] + f"[{pos + 1}]"
#         if not self._elXpath(eval_xpath):
#             raise IndexError("pos not found")
#         else:
#             return self._xpath(eval_xpath)[0]
#
#     def _get_res_name(self, res):
#         """return result name"""
#         return res.find_by_css("span.instrument-name").text
#
#     def search_res(self, res, check_counter=None):
#         """search for a res"""
#         result = self._get_result(0)
#         name = self._get_res_name(self._get_result(0))
#         x = 0
#         while not self._check_name(res, self._get_res_name(result),
#                                    counter=check_counter):
#             name = self._get_res_name(self._get_result(x))
#             logger.debug(name)
#             if self._check_name(res, name, counter=check_counter):
#                 return self._get_result(x)
#             x += 1
#         return result, name
#
#     def open_mov(self, name, name_counter=None):
#         if self._css(path['add-mov'])[0].visible:
#             self._css(path['add-mov'])[0].click()
#         else:
#             self._css('span.dataTable-no-data-action')[0].click()
#         self._css(path['search-box'])[0].fill(name)
#         if not self._get_result(0):
#             logger.error("{underline(name)} not found")
#             return False
#             self.close_mov()
#         result, name = self.search_res(name, check_counter=name_counter)
#         result.click()
#         if self._elCss("div.widget_message"):
#             if (self._css("div.widget_message div.title")
#                     [0].text == "Insufficient Funds"):
#                 return "INSFU"
#             else:
#                 return False
#         return name
#
#     def close_mov(self):
#         try:
#             self._css(path['close'])[0].click()
#         except Exception:
#             raise
#
#     def set_quantity(self, quant):
#         try:
#             self._css(path['quantity'])[0].fill(str(quant))
#             return True
#         except Exception:
#             raise
#
#     def get_price(self, name):
#         soup = BeautifulSoup(
#             self._css("div.scrollable-area-content").html, "html.parser")
#         for product in soup.select("div.tradebox"):
#             fullname = product.select("span.instrument-name")[0].text.lower()
#             if fullname.find(name.lower()) != -1:
#                 mark_closed_list = [x for x in product.select(
#                     "div.quantity-list-input-wrapper") if x.select(
#                     "div.placeholder")[0].text.lower().find("close") != -1]
#                 if mark_closed_list:
#                     sell_price = product.select("div.tradebox-price-sell")[0]\
#                         .text
#                     return float(sell_price)
#                 else:
#                     return False
#
#
# path = {
#     'login-btn': "#login-button",
#     'log': "input.btn-head",
#     'logo': "div.nav_logo",
#     'alert-box': "span.weekend-trading-close",
#     'add-mov': "span.open-dialog-icon.svg-icon-holder",
#     'search-box': "div.searchbox input",
#     'res':
#         '//*[@id="list-results-instruments"]/div/div[3]/div/div/div',
#     'sell-btn': "div#orderdialog div.tradebox-button.tradebox-sell",
#     'buy-btn': "div#orderdialog div.tradebox-button.tradebox-buy",
#     'quantity': "div.quantity-slider-input-wrapper > input",
#     'limit-gain-unit':
#         '//*[@id="smartorder"]/div[1]/div[3]/div/div[3]/div[1]/div[5]/input',
#     'limit-gain-value':
#         '//*[@id="smartorder"]/div[1]/div[3]/div/div[3]/div[1]/div[6]/input',
#     'limit-loss-unit':
#         '//*[@id="smartorder"]/div[1]/div[3]/div/div[3]/div[3]/div[5]/input',
#     'limit-loss-value':
#         '//*[@id="smartorder"]/div[1]/div[3]/div/div[3]/div[3]/div[6]/input',
#     'confirm-btn': "div.orderdialog-confirm-button",
#     'data-table': "tbody.table-body.dataTable-show-currentprice-arrows",
#     'search-btn': "div.tradepanel-control-bar span",
#     'search-pref': "input.search-input",
#     'all-tools': "div.search-tab",
#     'add-btn': "div.search-results-column div.svg-icon-holder",
#     'plus-icon': "svg.search-plus-icon",
#     'close-prefs': "div.back-button",
#     'close': "span.orderdialog-close",
#     'movs-table': "div#accountPanel .table-body",
# }


class API(AbstractAPI):
    """Interface object"""

    def __init__(self, level="debug"):
        super().__init__(level)
        self.movements = []
        self.stocks = []

    def addMov(self, product, quantity=None, mode="buy", stop_limit=None,
               auto_quantity=None, name_counter=None):
        """Add movement function"""
        name = self.open_mov(product, name_counter=name_counter)
        if name == "INSFU":
            logger.warning(
                f"Insufficient funds to " +
                f"buy {name} or reached limit")
            self.close_mov()
            return 'INSFU'
        self._css(path[mode + '-btn'])[0].click()
        # override quantity
        if quantity is not None and auto_quantity is not None:
            logger.warning(
                "quantity and auto_quantity are exclusive, " +
                "overriding quantity")
            quantity = None
        # set quantity
        if quantity is not None:
            self.set_quantity(quantity)
        # auto_quantity calculate quantity
        if auto_quantity is not None:
            # set the maximum quantity
            right_arrow = self._css("span.quantity-slider-right-arrow")[0]
            left_arrow = self._css("span.quantity-slider-left-arrow")[0]
            last_margin = None
            while last_margin != self.get_mov_margin():
                time.sleep(0.8)
                last_margin = self.get_mov_margin()
                right_arrow.click()
                if self._css('div.widget_message'):
                    widget = self._decode(self._css('div.widget_message'))
                    # in case of errors
                    if widget == 'INSFU':
                        logger.warning(
                            f"Insufficient funds to " +
                            f"buy {name} or reached limit")
                        self.close_mov()
                        return 'INSFU'
            # and descend
            while self.get_mov_margin() > auto_quantity:
                left_arrow.click()
                # check if margin is too high
                quantity = self._css(path['quantity'])[0].value
                if not quantity:
                    logger.warning(
                        f"Failed to add movement of {name} " +
                        "cause of margin too high")
                    self.close_mov()
                    return False
        # check margin and quantity used
        margin = self.get_mov_margin()
        quantity = self._css(path['quantity'])[0].value
        # set stop_limit
        if stop_limit is not None:
            try:
                self._set_limit(stop_limit['mode'], stop_limit['value'])
                self._css(path['confirm-btn'])[0].click()
                if self._elCss('div.widget_message'):
                    while self._elCss('div.widget_message'):
                        num = self._decode_n_update(
                            self._css('div.widget_message'),
                            stop_limit['value'])
                        self._set_limit('unit', num)
                        self._css(path['confirm-btn'])[0].click()
            except Exception as e:
                logger.error(e)
                self.close_mov()
                raise
                return False
        else:
            stop_limit['value'] = None
            self._css(path['confirm-btn'])[0].click()
        while self._elCss(path['confirm-btn']):
            time.sleep(0.1)
        logger.info(
            f"Added movement of {bold(quantity)} {bold(name)} with " +
            f"limit {round(stop_limit['value'][0], 8)}, " +
            f"{round(stop_limit['value'][1], 8)} " +
            f" and margin of {margin}")
        return {'margin': margin, 'name': name}

    def closeMov(self, mov_id):
        """close a position"""
        self._css("#" + mov_id + " div.close-icon")[0].click()
        self.browser.find_by_text("OK")[0].click()
        time.sleep(1.5)
        if self._elCss("#" + mov_id + " div.close-icon"):
            logger.error(f"failed to close mov {mov_id}")
            return False
        else:
            logger.info(f"closed mov {mov_id}")
            return True

    def checkPos(self):
        """check all current positions"""
        soup = BeautifulSoup(
            self._css(path['movs-table'])[0].html,
            "html.parser")
        movs = []
        for x in soup.find_all("tr"):
            try:
                prod_id = x['id']
                product = x.select("td.name")[0].text
                quant = self._num(x.select("td.quantity")[0].text)
                if ("direction-label-buy" in soup.find_all("tr")[0]
                        .select("td.direction")[0].span['class']):
                    mode = "long"
                else:
                    mode = "short"
                price = self._num(x.select("td.averagePrice")[0].text)
                curr = self._num(x.select("td.currentPrice")[0]
                                 .select("span.price-info")[0].text)
                earn = self._num(x.select("td.ppl")[0].text)
                mov = Movement(prod_id, product, quant, mode,
                               price, curr, earn)
                movs.append(mov)
            except Exception as e:
                logger.error(e)
        logger.debug(f"{len(movs)} positions updated")
        self.movements.clear()
        self.movements.extend(movs)
        return self.movements

    def checkStocks(self, stocks):
        """check specified stocks (list)"""

        soup = BeautifulSoup(
            self._xpath('//*[@id="tradePanel"]/div[5]/div[3]/div')[0].html,
            "html.parser")
        count = 0
        for product in soup.select("div.tradebox"):
            fullname = product.select("span.instrument-name")[0].text.lower()
            name = [x for x in stocks
                    if fullname.lower().find(x.lower()) != -1]
            if name:
                name = name[0]
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
                        logger.warning(e)
                        sent = None
                    stock.addVar([float(sell_price), sent])
                    count += 1
        logger.debug(f"added {bold(count)} stocks")
        return True

    def addPrefs(self, prefs):
        """add prefered stocks"""
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
            logger.info("added {prefs} to preferencies".format(
                prefs=', '.join([bold(x) for x in prefs])))
            self._css("span.prefs-icon-node")[0].click()
            self._css(
                "div.item-tradebox-prefs-menu-list-sentiment_mode")[0].click()
            self._css("span.equity-menu-btn-icon")[0].click()
            self._css("div.equity-menu-items-list ")[0].click()
            self._css("span.prefs-icon-node")[0].click()
            logger.debug("set sentiment mode")
            self._css("span.equity-menu-btn-icon")[0].click()
            info_list = self._css("div.equity-menu-items-list")[0]
            prefs_info_list = ['Free funds', 'Used margin']
            for pref_info in prefs_info_list:
                checkbox = info_list.find_by_text(pref_info)[-1]
                if 'selected' not in checkbox['class'].split(' '):
                    checkbox.find_by_css("svg")[0].click()
            self._css("span.equity-menu-btn-icon")[0].click()
            logger.debug("set bottom info")
            return True
        except Exception:
            logger.error("addPrefs failed")
            raise

    def clearPrefs(self):
        """clear all stock preferencies"""
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
            logger.debug("cleared preferencies")
            return True
        except Exception:
            logger.error("clearPrefs failed")
            raise


class Movement(object):
    def __init__(self, prod_id, product, quantity, mode, price, curr, earn):
        self.id = prod_id
        self.product = product
        self.quantity = quantity
        self.mode = mode
        self.price = price
        self.curr = curr
        self.earn = earn


class Stock(object):
    def __init__(self, name):
        self.name = name
        self.market = False
        self.vars = []

    def addVar(self, var):
        """add a variation (list)"""
        self.vars.append(var)
