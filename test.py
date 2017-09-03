from tradingAPI.api import *

api = API("CRITICAL")

def test_launch():
    assert api.launch()

def test_login():
    assert api.login("james.lumper@gmail.com", "TestTest1.")

def test_movs():
    api.addMov("ethereum", 1, "buy")
    api.checkPos()
    stock = [x.id for x in api.movements if x.name == "ethereum" and x.quantity == 1][0]
    api.closeMov(stock)
    api.checkPos()
    assert len([x.id for x in api.movements if x.name == "ethereum" and x.quantity == 1][0]) == 0

def test_clearPrefs():
    assert api.clearPrefs()

def test_addPrefs():
    assert api.addPrefs(["bitcoin", "ethereum"])

def test_logout():
    assert api.logout()
