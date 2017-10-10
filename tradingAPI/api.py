from bs4 import BeautifulSoup
from .links import path
from .low_level import LowLevelAPI

# logging
import logging
logger = logging.getLogger('tradingAPI')
mov_logger = logging.getLogger('mover')


class API(LowLevelAPI):
    """Interface object"""
    def __init__(self, brow='firefox'):
        super().__init__(brow)

    def addMov(self, product, quantity=None, mode="buy", stop_limit=None,
               auto_margin=None, name_counter=None):
        """main function for placing movements
        stop_limit = {'gain': [mode, value], 'loss': [mode, value]}"""
        # ~ ARGS ~
        if (not isinstance(product, type('')) and
                not isinstance(name_counter, type(''))):
            raise ValueError('product and name_counter have to be a string')
        if not isinstance(stop_limit, type({})):
            raise ValueError('has to be a dictionary')
        # exclusive args
        if quantity is not None and auto_margin is not None:
            raise ValueError("quantity and auto_margin are exclusive")
        elif quantity is None and auto_margin is None:
            raise ValueError("need at least one quantity")
        # ~ MAIN ~
        # open new window
        mov = self.new_mov(product)
        mov.open()
        # set quantity
        if quantity is not None:
            mov.set_quantity(quantity)
            # for best performance in long times
            margin = mov.get_unit_value() * quant
        # auto_margin calculate quantity (how simple!)
        elif auto_margin is not None:
            unit_value = mov.get_unit_value()
            mov.set_quantity(auto_margin * unit_value)
            margin = auto_margin
        # stop limit (how can be so simple!)
        if stop_limit is not None:
            mov.set_limit('gain', stop_limit['gain'][0], stop_limit['gain'][1])
            mov.set_limit('loss', stop_limit['loss'][0], stop_limit['loss'][1])
        # confirm
        try:
            mov.confirm()
        except MaxQuantLimit as e:
            logger.warning(e.err)
            # resolve immediately
            mov.set_quantity()
            mov.confirm()
        except Exception:
            logger.exception('undefined error in movement confirmation')
        mov_logger.info("added {mov.name} movement of {mov.quant} with " +
                        "margin of {margin}")
        mov_logger.debug(f"stop_limit: {stop_limit}")

#         self.movements = []
#         self.stocks = []


#         return {'margin': margin, 'name': name}

    def closePos(self):
        """close a mov given the position"""
        # -- FROM HERE ----~~~\
        # | need a position   |
        # | object in lower   |
        # \ level             |
        # \----------------~~~/
        pass

    def checkPos(self):
        """check all positions"""
        soup = BeautifulSoup(self.css1(path['movs-table']).html, 'html.parser')
        for label in soup.find_all("tr"):
            pos_id = label['id']
            # init an empty list
            poss = []
            # check if it already exist
            pos_list = [x for x in self.positions if x.id == pos_id]
            if pos_list:
                # and update it
                pos = pos_list[0]
                pos.update(label)
            else:
                pos = self.new_pos(label)
            pos.get_gain()
            poss.append(pos)
            # remove old positions
            self.positions.clear()
            self.positions.extend(poss)
        logger.debug("%d positions update" % len(poss))
        return self.positions


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
