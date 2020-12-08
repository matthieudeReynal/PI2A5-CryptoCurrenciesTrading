from dataToDictionnary import *
import sqlite3
import psycopg2
connect_str = "dbname='tradebotv4' user='tradebotv4' host='localhost' password='a-password'"
import requests
import json


API_KEY_NOMICS = "320b5a9ca6e199de978f670dce2d295b"
import urllib.request
url = "https://api.nomics.com/v1/market-cap/history?key="+API_KEY_NOMICS+"&start=2019-09-14T00%3A00%3A00Z"
#print(urllib.request.urlopen(url).read())

exchanges = ['binance']
pairs = ['LEND/USDT', 'LRC/USDT', 'SNX/USDT', 'KNC/USDT', 'BNT/USDT', 'REN/USDT', 'ENJ/USDT', 'ETH/USDT']
durations = ['1d']



def getFactor():
    assetsData = dataToDico(pairs, durations, exchanges)
    for asset in assetsData:
        length = len(assetsData[asset])

    dataCaps = requests.get(url)
    r_json = json.loads(dataCaps.text)

    marketCaps = []
    for i in r_json:
        marketCaps.append(i['market_cap'])
    
    for i in range (0,len(marketCaps)-length):
        del marketCaps[i]
    marketCapsFactor = []
    for i in range(len(marketCaps)):
        marketCaps[i] = float(marketCaps[i])
        marketCapsFactor.append(marketCaps[i]/marketCaps[0])
    print(marketCaps)
    print(marketCapsFactor)
    return marketCapsFactor

