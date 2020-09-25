# import Paymium_api_sql as app
# import Bitfinex_api_sql as apb
# import Kraken_api_sql as apk
# import Poloniex_api_sql as apo
# import Bitstamp_api_sql as apbi
import sqlite3
import psycopg2
import smtplib
import time
from email.mime.text import MIMEText
import ccxt

################ Check db integrity
def checkDb(connect_str):
	# Check when the update was last done
	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()

	# # Checking if table last_checks exists
	statement = """SELECT EXISTS (SELECT FROM information_schema.tables WHERE  table_name = 'last_checks')"""
	cursor.execute(statement)
	myTable = cursor.fetchone()
	if myTable[0] == False:
		print("Table last_checks does not exist")
		cursor.execute("""CREATE TABLE last_checks(Id SERIAL PRIMARY KEY, exchange TEXT, trading_pair TEXT, duration TEXT, table_name TEXT, last_check BIGINT, startdate BIGINT, last_id INT);""")
		conn.commit()
		print("Table last_checks was created")

	conn.close()

	return

def refreshDataCandle(connect_str, exchange, trading_pair = 'BTCUSD', duration = '5m', delay=365*24*60*60, debug = False):
	
	# Checking if db was initialized
	checkDb(connect_str)

	# Checking if this (exchange, trading pair, duration) has already been recorded
	checkIfCandleTableExists(connect_str, exchange, trading_pair, duration, delay)

	# Getting exchange class
	exchange_class = getattr(ccxt, exchange)
	exchangeObject = exchange_class()

	# Test if exchange has OHLCV
	if not exchangeObject.has['fetchOHLCV']:
		return False

	# Check when the update was last done
	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()
	statement = """SELECT id, last_check FROM last_checks WHERE exchange='%s' and trading_pair='%s' and duration ='%s'""" % (exchange, trading_pair, duration)
	cursor.execute(statement)
	lastCheckTuple = cursor.fetchone()
	sinceWhen = lastCheckTuple[1] + 1
	# print(sinceWhen)

	# Defining what is the max candle we want. We do NOT want the current candle.
	maxCandle = int(time.time())*1000 - getTimeframeInMilliSeconds(duration)
	print(maxCandle)

	while sinceWhen < maxCandle:
		print("new call!")
		time.sleep (exchangeObject.rateLimit / 1000) # time.sleep wants seconds
		candleResults = exchangeObject.fetchOHLCV(trading_pair, duration, sinceWhen)
		for candle in candleResults:
			# Updating sinceWhen
			sinceWhen = candle[0] + 1

			# Checkinf if we deal with current candle
			if sinceWhen > maxCandle:
				continue

			# Insert candle in db
			insertStatement = """INSERT INTO %s (date, open, high, low, close, volume) VALUES(%s, %s, %s, %s, %s, %s)""" % (getCandleTableName(exchange, trading_pair, duration), candle[0], candle[1], candle[2], candle[3], candle[4], candle[5] )
			print(candle)
			print(insertStatement)
			cursor.execute(insertStatement)
	# Update Sincewhen
	cursor.execute("""UPDATE last_checks SET last_check=%s, last_id=%s WHERE id = %s""", (maxCandle, 0, lastCheckTuple[0]))
	conn.commit()
	conn.close()
	return True

def getCandleTableName(exchange, trading_pair, duration):
	expectedTableName = exchange + "_" + trading_pair.replace('/', '_') + "_" + str(duration)
	return expectedTableName

def getTimeframeInMilliSeconds(timeFrame):
	if timeFrame == "1m":
		return 60*1000
	elif timeFrame == "3m":
		return 180*1000
	elif timeFrame == "5m":
		return 300*1000
	elif timeFrame == "15m":
		return 900*1000
	elif timeFrame == "30m":
		return 1800*1000
	elif timeFrame == "1h":
		return 3600*1000
	elif timeFrame == "2h":
		return 7200*1000
	elif timeFrame == "4h":
		return 14400*1000
	elif timeFrame == "6h":
		return 21600*1000
	elif timeFrame == "8h":
		return 28800*1000
	elif timeFrame == "12h":
		return 43200*1000
	elif timeFrame == "1d":
		return 86400*1000
	elif timeFrame == "3d":
		return 259200*1000
	elif timeFrame == "1w":
		return 604800*1000
	elif timeFrame == "1M":
		return 2592000*1000

#### Common functions
def createApiKey(public_key, secret_key, exchange, user):
	# CREATE TABLE executions_tradebot1(Id INTEGER PRIMARY KEY, sell_past REAL, sell_next REAL, buy_past REAL, buy_next REAL, balance_btc REAL, balance_eur REAL, saved_btc REAL, saved_eur REAL, state_sell BIT, state_buy BIT, current_uuid TEXT, past_uuid TEXT, state_pending BIT, currency TEXT, chrm_id INT, exchange TEXT);

	#print "Je suis la"
	keysParam = {}
	keysParam["public"] = public_key
	keysParam["secret"] = secret_key
	keysParam["exchange"] = exchange
	keysParam["user"] = user

	conn = sqlite3.connect('../data/keys/keys_db.db')

	cursor = conn.cursor()
	
	# sell , buy , pastTradeNumber , sqrVarBuy , sqrVarSell , sampleSizeSqVar , buycancel , sellCancel );
	# Inserting record in record table
	cursor.execute("""
	INSERT INTO api_key(public, secret, exchange, user) VALUES(:public, :secret, :exchange, :user)""", keysParam)
	cursor.execute("""
	SELECT last_insert_rowid()""")
	newId = cursor.fetchone()
	# newId = cursor.fetchone()
	# print newId
	
	conn.commit()
	conn.close()

	return newId[0]

def retrieveApiKey(userId, exchange):
	conn = sqlite3.connect('../data/keys/keys_db.db')
	cursor = conn.cursor()
	# buyMachineId = 1
	cursor.execute("""
	SELECT * FROM api_key WHERE user=? and exchange=?""", (userId,exchange))
	keyValues = cursor.fetchone()

	conn.close()
	if keyValues == None:
		print("No key found")
		return "None", "None"
	keyParams = {}
	keyParams["id"] = keyValues[0]
	keyParams["public"] = keyValues[1]
	keyParams["secret"] = keyValues[2]
	keyParams["exchange"] = keyValues[3]
	keyParams["user_id"] = keyValues[4]
	

	return keyParams["public"] , keyParams["secret"]

def recordTransaction(connect_str, orderDetails):
	# Record db fields:
	# id
	# exchange
	# uuid
	# trading_pair
	# state: To log errors	
	# btc_fee: Fee in NOT base currency
	# currency_fee: Fee in base currency
	# timestamp
	# traded_btc: Traded amount in NOT base currecny, fees not deducted
	# direction
	# traded_currency: Traded amount in base currency, fees not deducted
	# path_id: For abitragebot
	# machine_id: for investobot
	# user_id
	acceptedFields = ['uuid' , 'trading_pair' , 'state' , 'quote_fee' , 'base_fee' , 'timestamp' , 'price' , 'traded_quote' , 'direction' , 'traded_base'  , 'machine_id' , 'user_id']

	fieldString = "INSERT INTO records("
	valuesString = " VALUES("
	isFirst = True
	for field in orderDetails:
		if not str(field) in acceptedFields:
			print("Field " + str(field) + " not recognized")
			continue
		fieldString	+= str(field) + ", "
		valuesString += "%(" + str(field) + ")s" + ", "
	fullString = fieldString[:-2] + ") " + valuesString[:-2] + ")"
	print(fullString)
	
	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()
	
	# Inserting record in record table
	cursor.execute(fullString, orderDetails)
	
	
	conn.commit()
	conn.close()

def checkIfCandleTableExists(connect_str, exchange, trading_pair, duration, delay = 365*24*60*60):

	expectedTableName = getCandleTableName(exchange, trading_pair, duration)

	##### Retrieving last checks in database
	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()

	cursor.execute("""
	SELECT * FROM last_checks WHERE exchange='%s' and trading_pair='%s' and duration ='%s'""" % (exchange, trading_pair, duration))
	lastCheckResultTuple = cursor.fetchone()
	if lastCheckResultTuple == None:
		setStartDate = int(time.time()-delay)*1000
		cursor.execute("""
		INSERT INTO last_checks(exchange, trading_pair, duration, table_name, startdate, last_check, last_id) VALUES('%s', '%s', '%s', '%s', %s, %s, %s)""" % (exchange, trading_pair, duration, expectedTableName, setStartDate, setStartDate, 1) )
		tableCreationStatement = """CREATE TABLE """ + expectedTableName + """(Id SERIAL PRIMARY KEY, date BIGINT, high REAL, low REAL, open REAL, close REAL, volume REAL)"""
		cursor.execute(tableCreationStatement)


		conn.commit()

		print("This (pair, exchange) was not existant. It has been created in last_check table. I also created table " + expectedTableName)

	conn.close()

def sendEmail(direction, stringAd = '', email = ''):
	


	fromaddr = 'raspberry@henril.eu'
	# toaddrs  = 'henri.lieutaud.tradebot@gmail.com,' + email
	recipients = ['henri.lieutaud.tradebot@gmail.com', email]
	#msg = 'There was a terrible error that occured and I wanted you to know!'
	# msg = """From: Tradebot <raspberry@henril.eu>
	# To: Master <henri.lieutaud@gmail.com>
	# Subject: A new """
	# msg = msg + str(direction)

	# msg = msg + """
	# I just made a new trade.
	# """
	# msg = msg + "A " + str(direction) + " at price " + str(price)
	# msg = msg + """
	# Aditionnal information: 
	# """
	# msg = msg + str(string)
	#msgTxt = """ I just made a new trade!""" 
	msgTxt = stringAd
	msg = MIMEText(msgTxt)
	# msg['Subject'] = 'A new '+ str(direction) + ' at ' + str(price)
	msg['Subject'] = str(direction) 
	msg['From'] = fromaddr
	msg['To'] = ", ".join(recipients)
	# msg['To'] = toaddrs
	# Credentials (if needed)
	username = 'raspberry@henril.eu'
	password = 'b0puyVih'

	# The actual mail send
	# server = smtplib.SMTP('smtp.gmail.com:587')
	# print "Opening..."
	server = smtplib.SMTP('smtp.online.net:587')
	# print "ehlo..."
	server.ehlo()
	# print "starttls..."
	server.starttls()
	# print "Loging...."
	server.login(username,password)
	# print "Sending..."
	server.sendmail(fromaddr, recipients, msg.as_string())
	#server.sendmail(fromaddr, toaddrs, msg)
	server.quit()

def cleanDb(connect_str):
	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()

	statement = "select * from last_checks"
	cursor.execute(statement)
	newList = cursor.fetchall()
	for element in newList:
		statement = "drop table %s" % element[4]
		cursor.execute(statement)

	statement = "drop table last_checks"
	cursor.execute(statement)
	conn.commit()
	conn.close()