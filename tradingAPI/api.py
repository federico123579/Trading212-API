from .low_level import LowLevelAPI

# logging
import logging
logger = logging.getLogger('tradingAPI')

class API(LowLevelAPI):
    """Interface object"""
    def __init__(self, brow='firefox'):
        super().__init__(brow)

    def addMov(self, product, quantity=None, mode="buy", stop_limit=None,
               auto_margin=None, name_counter=None):
        """main function for placing movements"""
        # ~ ARGS ~
        if (not isinstance(product, type('')) and
                not isinstance(name_counter, type(''))):
            raise ValueError(str())
        # exclusive args
        if quantity is not None and auto_margin is not None:
            logger.error("quantity and auto_margin are exclusive")
            raise ValueError()
        elif quantity is None and auto_margin is None:
            logger.error("need at least one quantity")
            raise ValueError()
        # ~ MAIN ~
        # open new window
        mov = self.new_mov(product)
        mov.open()
        # set quantity
        if quantity is not None:
            mov.set_quantity(quantity)
        # auto_margin calculate quantity
        # FROM HERE -----~~~

#         self.movements = []
#         self.stocks = []

#         # auto_quantity calculate quantity
#         if auto_quantity is not None:
#             # set the maximum quantity
#             right_arrow = self._css("span.quantity-slider-right-arrow")[0]
#             left_arrow = self._css("span.quantity-slider-left-arrow")[0]
#             last_margin = None
#             while last_margin != self.get_mov_margin():
#                 time.sleep(0.8)
#                 last_margin = self.get_mov_margin()
#                 right_arrow.click()
#                 if self._css('div.widget_message'):
#                     widget = self._decode(self._css('div.widget_message'))
#                     # in case of errors
#                     if widget == 'INSFU':
#                         logger.warning(
#                             f"Insufficient funds to " +
#                             f"buy {name} or reached limit")
#                         self.close_mov()
#                         return 'INSFU'
#             # and descend
#             while self.get_mov_margin() > auto_quantity:
#                 left_arrow.click()
#                 # check if margin is too high
#                 quantity = self._css(path['quantity'])[0].value
#                 if not quantity:
#                     logger.warning(
#                         f"Failed to add movement of {name} " +
#                         "cause of margin too high")
#                     self.close_mov()
#                     return False
#         # check margin and quantity used
#         margin = self.get_mov_margin()
#         quantity = self._css(path['quantity'])[0].value
#         # set stop_limit
#         if stop_limit is not None:
#             try:
#                 self._set_limit(stop_limit['mode'], stop_limit['value'])
#                 self._css(path['confirm-btn'])[0].click()
#                 if self._elCss('div.widget_message'):
#                     while self._elCss('div.widget_message'):
#                         num = self._decode_n_update(
#                             self._css('div.widget_message'),
#                             stop_limit['value'])
#                         self._set_limit('unit', num)
#                         self._css(path['confirm-btn'])[0].click()
#             except Exception as e:
#                 logger.error(e)
#                 self.close_mov()
#                 raise
#                 return False
#         else:
#             stop_limit['value'] = None
#             self._css(path['confirm-btn'])[0].click()
#         while self._elCss(path['confirm-btn']):
#             time.sleep(0.1)
#         logger.info(
#             f"Added movement of {bold(quantity)} {bold(name)} with " +
#             f"limit {round(stop_limit['value'][0], 8)}, " +
#             f"{round(stop_limit['value'][1], 8)} " +
#             f" and margin of {margin}")
#         return {'margin': margin, 'name': name}
#
#     def closeMov(self, mov_id):
#         """close a position"""
#         self._css("#" + mov_id + " div.close-icon")[0].click()
#         self.browser.find_by_text("OK")[0].click()
#         time.sleep(1.5)
#         if self._elCss("#" + mov_id + " div.close-icon"):
#             logger.error(f"failed to close mov {mov_id}")
#             return False
#         else:
#             logger.info(f"closed mov {mov_id}")
#             return True
#
#     def checkPos(self):
#         """check all current positions"""
#         soup = BeautifulSoup(
#             self._css(path['movs-table'])[0].html,
#             "html.parser")
#         movs = []
#         for x in soup.find_all("tr"):
#             try:
#                 prod_id = x['id']
#                 product = x.select("td.name")[0].text
#                 quant = self._num(x.select("td.quantity")[0].text)
#                 if ("direction-label-buy" in soup.find_all("tr")[0]
#                         .select("td.direction")[0].span['class']):
#                     mode = "long"
#                 else:
#                     mode = "short"
#                 price = self._num(x.select("td.averagePrice")[0].text)
#                 curr = self._num(x.select("td.currentPrice")[0]
#                                  .select("span.price-info")[0].text)
#                 earn = self._num(x.select("td.ppl")[0].text)
#                 mov = Movement(prod_id, product, quant, mode,
#                                price, curr, earn)
#                 movs.append(mov)
#             except Exception as e:
#                 logger.error(e)
#         logger.debug(f"{len(movs)} positions updated")
#         self.movements.clear()
#         self.movements.extend(movs)
#         return self.movements
#
#     def checkStocks(self, stocks):
#         """check specified stocks (list)"""
#
#         soup = BeautifulSoup(
#             self._xpath('//*[@id="tradePanel"]/div[5]/div[3]/div')[0].html,
#             "html.parser")
#         count = 0
#         for product in soup.select("div.tradebox"):
#             fullname = product.select("span.instrument-name")[0].text.lower()
#             name = [x for x in stocks
#                     if fullname.lower().find(x.lower()) != -1]
#             if name:
#                 name = name[0]
#                 if not [x for x in self.stocks if x.name == name]:
#                     self.stocks.append(Stock(name))
#                 stock = [x for x in self.stocks if x.name == name][0]
#                 mark_closed_list = [x for x in product.select(
#                     "div.quantity-list-input-wrapper") if x.select(
#                     "div.placeholder")[0].text.lower().find("close") != -1]
#                 if len(mark_closed_list) != 0:
#                     market = False
#                 else:
#                     market = True
#                 stock.market = market
#                 if market is True:
#                     sell_price = product.select("div.tradebox-price-sell")[0]\
#                         .text
#                     raw_sent = product.select(
#                         "span.tradebox-buyers-container.number-box")[0].text
#                     try:
#                         sent = (int(raw_sent.strip('%')) / 100)
#                     except Exception as e:
#                         logger.warning(e)
#                         sent = None
#                     stock.addVar([float(sell_price), sent])
#                     count += 1
#         logger.debug(f"added {bold(count)} stocks")
#         return True
#
#     def addPrefs(self, prefs):
#         """add prefered stocks"""
#         try:
#             for pref in prefs:
#                 self._css(path['search-btn'])[0].click()
#                 self._css(path['all-tools'])[0].click()
#                 self._css(path['search-pref'])[0].fill(pref)
#                 if self._elCss(path['plus-icon']):
#                     self._css(path['add-btn'])[0].click()
#                 if self._elCss('span.btn-primary'):
#                     self._css('span.btn-primary')[0].click()
#             self._css(path['close-prefs'])[0].click()
#             logger.info("added {prefs} to preferencies".format(
#                 prefs=', '.join([bold(x) for x in prefs])))
#             self._css("span.prefs-icon-node")[0].click()
#             self._css(
#                 "div.item-tradebox-prefs-menu-list-sentiment_mode")[0].click()
#             self._css("span.equity-menu-btn-icon")[0].click()
#             self._css("div.equity-menu-items-list ")[0].click()
#             self._css("span.prefs-icon-node")[0].click()
#             logger.debug("set sentiment mode")
#             self._css("span.equity-menu-btn-icon")[0].click()
#             info_list = self._css("div.equity-menu-items-list")[0]
#             prefs_info_list = ['Free funds', 'Used margin']
#             for pref_info in prefs_info_list:
#                 checkbox = info_list.find_by_text(pref_info)[-1]
#                 if 'selected' not in checkbox['class'].split(' '):
#                     checkbox.find_by_css("svg")[0].click()
#             self._css("span.equity-menu-btn-icon")[0].click()
#             logger.debug("set bottom info")
#             return True
#         except Exception:
#             logger.error("addPrefs failed")
#             raise
#
#     def clearPrefs(self):
#         """clear all stock preferencies"""
#         try:
#             self._css(path['search-btn'])[0].click()
#             self._css(path['all-tools'])[0].click()
#             for res in self._css("div.search-results-list-item"):
#                 if not res.find_by_css(path['plus-icon']):
#                     res.find_by_css(path['add-btn'])[0].click()
#             self._css('div.widget_message span.btn')[0].click()
#             # fix errors
#             self._css(path['close-prefs'])[0].click()
#             while not self._elCss(path['search-btn']):
#                 time.sleep(0.5)
#             logger.debug("cleared preferencies")
#             return True
#         except Exception:
#             logger.error("clearPrefs failed")
#             raise
#
#
# class Movement(object):
#     def __init__(self, prod_id, product, quantity, mode, price, curr, earn):
#         self.id = prod_id
#         self.product = product
#         self.quantity = quantity
#         self.mode = mode
#         self.price = price
#         self.curr = curr
#         self.earn = earn
#
#
# class Stock(object):
#     def __init__(self, name):
#         self.name = name
#         self.market = False
#         self.vars = []
#
#     def addVar(self, var):
#         """add a variation (list)"""
#         self.vars.append(var)
