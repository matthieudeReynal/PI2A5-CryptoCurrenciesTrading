import sys
sys.path.append('ccxt-datagrabber')
import datagrabber as api
import ccxt

connect_str = "dbname='tradebotv4' user='tradebotv4' host='localhost' password='a-password'"

# api.cleanDb(connect_str)

exchanges = ['binance']
pairs = ['LEND/USDT', 'LRC/USDT', 'SNX/USDT', 'KNC/USDT', 'BNT/USDT', 'REN/USDT', 'ENJ/USDT', 'ETH/USDT']
durations = ['1d']

for exchange in exchanges:
	for pair in pairs:
		for duration in durations:
			api.refreshDataCandle(connect_str, exchange, pair, duration)
