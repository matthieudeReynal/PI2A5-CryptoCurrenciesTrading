import sys
sys.path.append('ccxt-datagrabber')
import datagrabber as api
import ccxt

connect_str = "dbname='tradebotv4' user='tradebotv4' host='localhost' password='a-password'"

# api.cleanDb(connect_str)

exchanges = ['binance']
pairs = ['LEND/USDT', 'KNC/USDT', 'SNX/USDT', 'LRC/USDT', 'BNT/USDT']
durations = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d', '3d', '1w']

for exchange in exchanges:
	for pair in pairs:
		for duration in durations:
			api.refreshDataCandle(connect_str, exchange, pair, duration)
