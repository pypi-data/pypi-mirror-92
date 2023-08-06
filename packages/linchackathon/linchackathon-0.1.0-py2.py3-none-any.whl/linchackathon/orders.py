# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 19:50:58 2021

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

def getOrders():
	
    url_g = u.url+ '/private/' + u.token + '/order'
    with requests.Session() as session:
        get = session.get(url_g)
		
    return get.json()


# =============================================================================
# Buy one stock
# =============================================================================

def placeOrder(symbol, amount, price):

    try:
        int(amount)
        int(price)
    except:
        raise ValueError("""The amount and price must be integers""")


    amount = int(amount)
    price = int(price)
	
    url_s = u.url+ '/private/' + u.token + '/order'
    body ={'symbol': symbol, 'amount': amount, 'price' : price}
    with requests.Session() as session:
        post = session.post(url_s, json= body)

    return post.content.decode("utf-8")




# =============================================================================
# Buy one stock
# =============================================================================

def deleteOrder(symbol):

    url_s = u.url+ '/private/' + u.token + '/order'
    body ={'symbol': symbol}
    with requests.Session() as session:
        post = session.delete(url_s, json= body)

    return post.content.decode("utf-8")
