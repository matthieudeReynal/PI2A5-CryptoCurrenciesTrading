import sqlite3
import psycopg2
import smtplib
import time
import sys
sys.path.append('ccxt-datagrabber')
import datagrabber as api
from email.mime.text import MIMEText
import ccxt


connect_str = "dbname='tradebotv4' user='tradebotv4' host='localhost' password='a-password'"

exchanges = ['binance']
pairs = ['LEND/USDT', 'LRC/USDT', 'SNX/USDT', 'KNC/USDT', 'BNT/USDT', 'REN/USDT', 'ENJ/USDT', 'ETH/USDT']
durations = ['1d']
#pairs=['LEND/USDT']
def dataToDico(pairs=pairs, durations=durations, exchanges=exchanges):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    dico = {}

    for pair in pairs:
        dbName = api.getCandleTableName('binance',pair,'1d')
        statement = "SELECT high FROM " + dbName
        cursor.execute(statement)
        highs = cursor.fetchall()
        dico[pair] = []
        for high in highs:
            dico[pair].append(high[0])
        print('****************************************')
        print(dico)
    conn.close()

dataToDico()