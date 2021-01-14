import sqlite3
import psycopg2
import smtplib
import time
import sys
sys.path.append('ccxt-datagrabber')
import datagrabber as api
from email.mime.text import MIMEText
import ccxt
import pandas as pd

import numpy as np

connect_str = "dbname='tradebotv4' user='tradebotv4' host='localhost' password='a-password'"

exchanges = ['binance']
pairs = ['LEND/USDT', 'LRC/USDT', 'SNX/USDT', 'KNC/USDT', 'BNT/USDT', 'REN/USDT', 'ENJ/USDT', 'ETH/USDT']
durations = ['3m']
#pairs=['LEND/USDT']
def dataToDico(pairs=pairs, durations=durations, exchanges=exchanges):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    dico = {}

    for pair in pairs:
        dbName = api.getCandleTableName('binance',pair ,'3m')
        statement = "SELECT high FROM " + dbName
        cursor.execute(statement)
        highs = cursor.fetchall()
        highs = [item[0] for item in highs]
        statement = "SELECT low FROM " + dbName
        cursor.execute(statement)
        lows = cursor.fetchall()
        lows = [item[0] for item in lows]
        print(type(highs))
        statement = "SELECT close, date FROM " + dbName+ " ORDER BY date ASC"
        cursor.execute(statement)
        rows = cursor.fetchall()
        #print(closes[0][1])
        times = []
        closes = []
        for row in rows:
            closes.append(row[0])
            times.append(row[1])
        #closes = [item[0] for item in closes]
        dico['time'] = [    ]
        dico[pair] = []
        
        #times = [time[1] for time in closes]
        for i in range(len(closes)):
            dico[pair].append(closes[i])
        for i in range(len(times)):
            dico['time'].append(times[i])
        #print('****************************************')
        #print(dico)
        for key in dico.keys():
            for key2 in dico.keys():
                while len(dico[key])<len(dico[key2]) and key!='time':
                    dico[key].insert(0,0)
    conn.close()
    return dico

def oneAssetToDF(pairs=pairs, durations=durations, exchanges=exchanges):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    dbName = api.getCandleTableName('binance',pairs,'3m')
    statement = "SELECT high, low, close, date FROM " + dbName+ " ORDER BY date ASC"
    cursor.execute(statement)
    data = cursor.fetchall()
    highs =[]
    lows = []
    closes = []
    dates = []
    for row in data:
        highs.append(row[0])
        lows.append(row[1])
        closes.append(row[2])
        dates.append(row[3])
    d = {'date': dates, 'high': highs, 'low':lows, 'close': closes}
    df = pd.DataFrame(data = d)
    #df = pd.DataFrame(np.array([dates, highs, lows, closes]), columns = ['dates', 'highs', 'lows', 'closes'])
    return df
def oneAssetToDFalex(pairs=pairs, durations=durations, exchanges=exchanges):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    dbName = api.getCandleTableName('binance',pairs,'3m')
    statement = "SELECT high, low, close, date FROM " + dbName+ " ORDER BY date ASC"
    cursor.execute(statement)
    data = cursor.fetchall()
    index=0
    highs =[]
    lows = []
    closes = []
    dates = []
    for row in data:
        highs.append(row[0])
        lows.append(row[1])
        closes.append(row[2])
        dates.append(row[3])
    result = []
    for row in data: 
        tmp=False
        if (index-1<len(close) ):
            if (close[index]<close[index+1]):
                tmp=True
        else :
             tmp=False
        result.append(tmp)
        index=index +1
      
    d = {'date': dates, 'high': highs, 'low':lows, 'close': closes, 'result': result}
    df = pd.DataFrame(data = d)
    #df = pd.DataFrame(np.array([dates, highs, lows, closes]), columns = ['dates', 'highs', 'lows', 'closes'])
    return df

#dataToDico()
'''
def dataToDf(pairs=pairs, durations=durations,exchanges=exchanges):
    df = pd.DataFrame.from_dict(dataToDico(pairs, durations, exchanges)
    return df
'''
