import sys
sys.path.append('ccxt-datagrabber')
import datagrabber as grab
import genstats as stat
import ccxt

connect_str = "dbname='tradebotv4' user='tradebotv4' host='localhost' password='a-password'"

# api.cleanDb(connect_str)
exchange = 'binance'
trading_pair = 'LEND/USDT'
duration = '5m'

tableName = grab.getCandleTableName(exchange, trading_pair, duration)

# Check if column exists in db
# print(stat.checkIfColumnExistsInTable(connect_str, tableName, 'sma_wfwfwf7'))
# print(stat.checkIfColumnExistsInTable(connect_str, tableName, 'close'))

# Add column to db
# print(stat.createColumnInTable(connect_str, tableName, 'sma_71', 'REAL

# Generating SMA in db
# stat.calculateSMAPeriod(connect_str, tableName, 7 )
# stat.calculateEMAPeriod(connect_str, tableName, 7 )
stat.calculatePercentChange(connect_str, tableName)
period = grab.getTimeframeInMilliSeconds(duration)
# print(period)
stat.getPercentChange(connect_str, tableName, 1594771200000, period, 1 )
stat.getPercentChange(connect_str, tableName, 1594771200000, period, 2 )
stat.getPercentChange(connect_str, tableName, 1594771200000, period, 3 )
stat.getPercentChange(connect_str, tableName, 1594771200000, period, 20 )