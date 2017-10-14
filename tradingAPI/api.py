from bs4 import BeautifulSoup
from .links import path
# exceptions
from tradingAPI import exceptions
from .low_level import LowLevelAPI, Stock

# logging
import logging
logger = logging.getLogger('tradingAPI')
mov_logger = logging.getLogger('mover')


class API(LowLevelAPI):
    """Interface object"""
    def __init__(self, brow='firefox'):
        super().__init__(brow)
        self.preferences = []
        self.stocks = []

    def addMov(self, product, quantity=None, mode="buy", stop_limit=None,
               auto_margin=None, name_counter=None):
        """main function for placing movements
        stop_limit = {'gain': [mode, value], 'loss': [mode, value]}"""
        # ~ ARGS ~
        if (not isinstance(product, type('')) or
                (not isinstance(name_counter, type('')) and
                 name_counter is not None)):
            raise ValueError('product and name_counter have to be a string')
        if not isinstance(stop_limit, type({})) and stop_limit is not None:
            raise ValueError('it has to be a dictionary')
        # exclusive args
        if quantity is not None and auto_margin is not None:
            raise ValueError("quantity and auto_margin are exclusive")
        elif quantity is None and auto_margin is None:
            raise ValueError("need at least one quantity")
        # ~ MAIN ~
        # open new window
        mov = self.new_mov(product)
        mov.open()
        mov.set_mode(mode)
        # set quantity
        if quantity is not None:
            mov.set_quantity(quantity)
            # for best performance in long times
            try:
                margin = mov.get_unit_value() * quantity
            except TimeoutError:
                mov.close()
                logger.warning("market closed for %s" % mov.product)
                return False
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
        except (exceptions.MaxQuantLimit, exceptions.MinQuantLimit) as e:
            logger.warning(e.err)
            # resolve immediately
            mov.set_quantity(e.quant)
            mov.confirm()
        except Exception:
            logger.exception('undefined error in movement confirmation')
        mov_logger.info(f"added {mov.product} movement of {mov.quantity} " +
                        f"with margin of {margin}")
        mov_logger.debug(f"stop_limit: {stop_limit}")

#         return {'margin': margin, 'name': name}

    def checkPos(self):
        """check all positions"""
        soup = BeautifulSoup(self.css1(path['movs-table']).html, 'html.parser')
        poss = []
        for label in soup.find_all("tr"):
            pos_id = label['id']
            # init an empty list
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

    def checkStock(self):
        """check stocks in preference"""
        if not self.preferences:
            logger.debug("no preferences")
            return None
        soup = BeautifulSoup(
            self.xpath(path['stock-table'])[0].html, "html.parser")
        count = 0
        # iterate through product in left panel
        for product in soup.select("div.tradebox"):
            prod_name = product.select("span.instrument-name")[0].text
            stk_name = [x for x in self.preferences
                        if x.lower() in prod_name.lower()]
            if not stk_name:
                continue
            name = prod_name
            if not [x for x in self.stocks if x.product == name]:
                self.stocks.append(Stock(name))
            stock = [x for x in self.stocks if x.product == name][0]
            if 'tradebox-market-closed' in product['class']:
                stock.market = False
            if not stock.market:
                logger.debug("market closed for %s" % stock.product)
                continue
            sell_price = product.select("div.tradebox-price-sell")[0].text
            buy_price = product.select("div.tradebox-price-buy")[0].text
            sent = int(product.select(path['sent'])[0].text.strip('%')) / 100
            stock.new_rec([sell_price, buy_price, sent])
            count += 1
        logger.debug(f"added %d stocks" % count)
        return self.stocks

    def addPrefs(self, prefs=[]):
        self.preferences.extend(prefs)

    def clearPrefs(self):
        """clear the left panel and preferences"""
        self.preferences.clear()
        tradebox_num = len(self.css('div.tradebox'))
        for i in range(tradebox_num):
            self.xpath(path['trade-box'])[0].right_click()
            self.css1('div.item-trade-contextmenu-list-remove').click()
        logger.info("cleared preferences")

    def addPrefs(self, prefs=[]):
        """add preference in self.preferences"""
        if len(prefs) == len(self.preferences) == 0:
            logger.debug("no preferences")
            return None
        self.preferences.extend(prefs)
        self.css1(path['search-btn']).click()
        count = 0
        for pref in self.preferences:
            self.css1(path['search-pref']).fill(pref)
            self.css1(path['pref-icon']).click()
            btn = self.css1('div.add-to-watchlist-popup-item .icon-wrapper')
            if not self.css1('svg', btn)['class'] is None:
                btn.click()
                count += 1
            # remove window
            self.css1(path['pref-icon']).click()
        # close finally
        self.css1(path['back-btn']).click()
        self.css1(path['back-btn']).click()
        logger.debug("updated %d preferences" % count)
        return self.preferences
