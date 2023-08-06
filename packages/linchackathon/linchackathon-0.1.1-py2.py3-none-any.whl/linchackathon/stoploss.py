# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 21:21:56 2021

@author: yasse
"""

# =============================================================================
#  Imports
# =============================================================================
import requests
from . import ipaddr as u

# =============================================================================
# Buy one stock
# =============================================================================

def getStoplosses():
	
    url_g = u.url+ '/private/' + u.token + '/stoploss'
    with requests.Session() as session:
        get = session.get(url_g)
		
    return get.json()


# =============================================================================
# Buy one stock
# =============================================================================

def placeStoploss(symbol, trigger, amount):

    try:
        int(amount)
        int(trigger)
    except:
        raise ValueError("""The amount and price must be integers""")


    amount = int(amount)
    trigger = int(trigger)
	
    url_s = u.url+ '/private/' + u.token + '/stoploss'
    body ={'symbol': symbol, 'trigger': trigger, 'amount' : amount}
    with requests.Session() as session:
        post = session.post(url_s, json= body)

    return post.content.decode("utf-8")




# =============================================================================
# Buy one stock
# =============================================================================

def deleteStoploss(symbol):

    url_s = u.url+ '/private/' + u.token + '/stoploss'
    body ={'symbol': symbol}
    with requests.Session() as session:
        post = session.delete(url_s, json= body)

    return post.content.decode("utf-8")