import sys
sys.path.append('ccxt-datagrabber')
import datagrabber as grab
import genstats as stat
import ccxt
import orderManager as orde
import valuationManager as val


connect_str = "dbname='tradebotv4' user='tradebotv4' host='localhost' password='a-password'"

# api.cleanDb(connect_str)
exchange = 'binance'
quote_currency = 'BNT'
duration = '12h'
base_currency = "USDT"
valuationObject = val.valuationManager(connect_str, exchange, base_currency)
myOrders = orde.orderManager(connect_str, exchange, True, valuationObject)

print(myOrders.swapCurrencies(quote_currency, 'buy', 10, 1595049840000))
print(myOrders.swapCurrencies(quote_currency, 'sell', 10, 1595049840000))