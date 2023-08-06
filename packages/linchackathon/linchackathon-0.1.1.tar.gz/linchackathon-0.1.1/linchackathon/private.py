# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 11:08:56 2021

@author: yasse
"""

# =============================================================================
#  Imports
# =============================================================================
import requests
import pandas as pd
from . import ipaddr as u

# =============================================================================
# Buy one stock
# =============================================================================

def buyStock(symbol, amount):

    try:
        int(amount)
    except:
        raise ValueError("""The amount must be an integer""")


    amount = int(amount)
    url_s = u.url+ '/private/' + u.token + '/buy'
    body ={'symbol': symbol, 'amount': amount}
    with requests.Session() as session:
        post = session.post(url_s, json= body)

    return post.content.decode("utf-8")



# =============================================================================
# sell one stock
# =============================================================================
	
def sellStock(symbol, amount):
 
    try:
        int(amount)
    except:
        raise ValueError("""The amount must be an integer""")


    amount = int(amount)
    url_s = u.url+ '/private/' + u.token + '/sell'
    body ={'symbol': symbol, 'amount': amount}
    with requests.Session() as session:
        post = session.post(url_s, json= body)

    return post.content.decode("utf-8")



# =============================================================================
# get portfolio
# =============================================================================

def getPortfolio():

    url_g = u.url + '/private/' + u.token + '/getPortfolio'
    response = requests.get(url_g)

    return response.json()


# =============================================================================
# get saldo
# =============================================================================

def getSaldo():

    url_g = u.url + '/private/' + u.token + '/getSaldo'
    response = requests.get(url_g)

    return response.json()


# =============================================================================
# get Hisory
# =============================================================================

def getHistory():

    url_g = u.url + '/private/' + u.token + '/getHistory'
    response = requests.get(url_g)
	
    history = pd.DataFrame(response.json())
    history.index += 1
	
    return history

