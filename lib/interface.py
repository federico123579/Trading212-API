#/usr/bin/env python3.6

from splinter import Browser
from time import sleep

from .data import path


class API(object):
    '''Interface object'''
    def __init__(self, brow="firefox"):
        self.browser = Browser(brow)

    def _css(self, css_path):
        '''css find function abbreviation'''
        return self.browser.find_by_css(css_path)

    def _name(self, name):
        '''name find function abbreviation'''
        return self.browser.find_by_name(name)

    def _elCss(self, css_path):
        '''check if element is present by css'''
        return self.browser.is_element_present_by_css(css_path)

    def login(self, username, password, mode="demo"):
        '''Login function'''
        self.browser.visit("https://trading212.com/it/login")
        # self._css(path['login-btn']).click() obsolete
        self._name("login[username]").fill(username)
        self._name("login[password]").fill(password)
        self._css(path['log']).click()
        if "demo.trading212.com" not in self.browser.url:
            return 0
        while not self._elCss(path['logo']):
            sleep(1)
        if mode == "demo" and self._elCss(path['alert-box']):
            self._css(path['alert-box']).click()
        return 1

    def logout(self):
        '''logout func (to quit browser)'''
        self.browser.quit()

    def addMov(self, product, mode="buy", quantity=None, stop_limit=None):
        '''Add movement function'''
        self._css(path['add-mov']).click()
        self._css(path['search-box']).fill(product)
            if not self._elCss(path['first-res']):
                return 0
        self._css(path['first-res']).click()
        self._css(path[mode + '-btn']).click()
        if quantity != None:
            self._css(path['quantity']).fill(str(quantity))
        if stop_limit != None:
            self._css(path['limit-gain-' + stop_limit['gain'][0]]).fill(str(stop_limit['gain'][1]))
            self._css(path['limit-loss-' + stop_limit['loss'][0]]).fill(str(stop_limit['loss'][1]))
        self._css(path['confirm-btn']).click()
        return 1