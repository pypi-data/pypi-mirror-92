# -*- coding: utf-8 -*-

"""
LINC
======



LINC is short for I don't know actually


"""

from . import auth
from . import private
from . import public
from . import orders
from . import stoploss

#auth.py
init = auth.init

#public.py
getTickers = public.getTickers
getTickersNames = public.getTickersNames
getStock = public.getStock
getStockHistory = public.getStockHistory

#private.py
buyStock = private.buyStock
sellStock = private.sellStock
getPortfolio = private.getPortfolio
getSaldo = private.getSaldo
getHistory = private.getHistory

#orders.py
placeOrder= orders.placeOrder
getOrders= orders.getOrders
deleteOrder= orders.deleteOrder

#orders.py
getStoplosses= stoploss.getStoplosses
placeStoploss= stoploss.placeStoploss
deleteStoploss= stoploss.deleteStoploss
