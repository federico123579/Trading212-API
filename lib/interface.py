#/usr/bin/env python3.6

from splinter import Browser
from data import path

class Interface(object):
    def __init__(self, brow="firefox"):
        self.browser = Browser(brow)

    def _css(self, css_path):
        return self.browser.find_by_css(css_path)

    def login(self, username, password, mode="demo"):
        self.browser.visit("https://trading212.com")
        self._css(path['login-btn']).click()
        browser.find_by_name("login[username]").fill(username)
        browser.find_by_name("login[password]").fill(password)
        self._css(path['log']).click()