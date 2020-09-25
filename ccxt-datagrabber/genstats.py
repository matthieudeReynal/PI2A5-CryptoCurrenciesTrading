import sqlite3
import psycopg2
import time

def checkIfColumnExistsInTable(connect_str, tableName, columnName):
	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()

	statement = "SELECT * FROM information_schema.tables WHERE  table_name = 'last_checks'" 
	# statement = "SELECT column_name FROM information_schema.columns WHERE table_name='%s' and column_name='%s'" % (tableName, columnName) 
	# statement = "SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='%s' AND column_name='%s')" %(tableName, columnName) 
	statement = "SELECT TRUE FROM pg_attribute WHERE  attrelid = '%s'::regclass AND attname = '%s' AND    NOT attisdropped" % (tableName, columnName) 
	# print(statement)

	cursor.execute(statement)
	result = cursor.fetchone()
	conn.close()
	# print(result)
	if result == None:
		return False
	else:
		return True

def createColumnInTable(connect_str, tableName, columnName, dataType):
	if checkIfColumnExistsInTable(connect_str, tableName, columnName):
		return False

	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()

	statement = "ALTER TABLE %s ADD COLUMN %s %s" % (tableName, columnName, dataType) 

	try:
		cursor.execute(statement)
		# result = cursor.fetchone()
		conn.commit()
		# print(result)
		conn.close()
		return True
	except:
		conn.close()
		return False

def calculateSMAPeriod(connect_str, tableName, smaPeriod):
	##### Connect to db
	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()

	columnName = "sma_%s" % smaPeriod
	##### Verifying if SMA period column exists
	if not checkIfColumnExistsInTable(connect_str, tableName, columnName):
		createColumnInTable(connect_str, tableName, columnName, 'REAL')

	##### Retrieving data in database
	selectStatement = """SELECT id, close FROM """  + tableName + """ order by date"""
	cursor.execute(selectStatement)

	allValues = cursor.fetchall()

	print(len(allValues))
	# print allValues[1][2]

	smaVector = []

	for i in range(0,len(allValues)):
		
		## Initializing smaVector
		if i < smaPeriod:
			smaVector.append(allValues[i][1])
			# print(smaVector)
			continue

		# else:
		# 	break

		## Calculating sma
		smaValue = sum(smaVector) / smaPeriod
		# print smaValue
		# print smaVector
		updateStatement = "UPDATE %s SET %s = %s where id = %s" % (tableName, columnName, smaValue, str(allValues[i][0]))
		# print(updateStatement)
		cursor.execute(updateStatement)
		# print i
		## Shifting previous period value
		for j in range(0,smaPeriod-1):
			# print smaVector
			smaVector[j] = smaVector[j+1]

		## Including new value
		smaVector[smaPeriod-1] = allValues[i][1]

		# print smaVector


	conn.commit()
	conn.close()
		
		
def calculateEMAPeriod(connect_str, tableName, emaPeriod):

	##### Connect to db
	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()

	columnName = "ema_%s" % emaPeriod

	##### Verifying if SMA period column exists
	if not checkIfColumnExistsInTable(connect_str, tableName, columnName):
		createColumnInTable(connect_str, tableName, columnName, 'REAL')

	selectStatement = """SELECT id, close, sma_"""+ str(emaPeriod)+ """ FROM """  + tableName + """ order by date"""
	cursor.execute(selectStatement)

	allValues = cursor.fetchall()

	print(len(allValues))
	# print allValues[1][2]

	emaValue = 0
	emaFactor = 2.0 / (emaPeriod + 1)

	for i in range(emaPeriod,len(allValues)):
		if i == emaPeriod:
			### Initialiazing EMA with SMA
			emaValue = allValues[i][2]
		else:
			## Calculating ema
			emaValue = emaValue + emaFactor*(allValues[i][1] - emaValue)

		updateStatement = "UPDATE %s SET %s = %s where id = %s" % (tableName, columnName, str(emaValue), str(allValues[i][0]) )

		print(updateStatement)
		cursor.execute(updateStatement)

	conn.commit()
	conn.close()
		
def calculatePercentChange(connect_str, tableName):
	##### Connect to db
	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()

	columnName = "percentchange"

	##### Verifying if SMA period column exists
	if not checkIfColumnExistsInTable(connect_str, tableName, columnName):
		createColumnInTable(connect_str, tableName, columnName, 'REAL')

	# Getting data from db
	selectStatement = """SELECT id, close FROM """  + tableName + """ order by date"""
	cursor.execute(selectStatement)

	allValues = cursor.fetchall()
	print(len(allValues))


	smaVector = []

	for i in range(0,len(allValues)):
		
		## Initializing smaVector
		if i == 0 :
			percentChangeValue = 0

		else:
			percentChangeValue = allValues[i][1]/allValues[i-1][1]

		updateStatement = "UPDATE %s SET %s = %s where id = %s" % (tableName, columnName, percentChangeValue, str(allValues[i][0]))
		print(updateStatement)
		cursor.execute(updateStatement)

	conn.commit()
	conn.close()

def getPercentChange(connect_str, tableName, timeStamp, period, average = 1):
	##### Connect to db
	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()

	columnName = "percentchange"

	##### Verifying if SMA period column exists
	if not checkIfColumnExistsInTable(connect_str, tableName, columnName):
		return False
	upperBound = timeStamp
	lowerBound = timeStamp- period * average
	selectStatement = """SELECT avg(%s) FROM %s where date <=%s and date >= %s""" % (columnName, tableName, upperBound, lowerBound)
	# selectStatement = """SELECT * FROM %s where date <=%s and date >= %s""" % ( tableName, upperBound, lowerBound)

	# print(selectStatement)
	cursor.execute(selectStatement)

	allValues = cursor.fetchone()
	# print(allValues)
	return allValues[0]


# def updateSMAPeriod(tableName, smaPeriod, timeDelay = False):
	
# 	if not timeDelay:
# 		limitDate = int(time.time()) - smaPeriod * 300 * 2
# 	else:
# 		limitDate = int(time.time()) - timeDelay

# 	# print limitDate
# 	conn = sqlite3.connect(db_name)

# 	cursor = conn.cursor()

# 	selectStatement = """SELECT id, close, sma_"""+ str(smaPeriod) +""" FROM """  + tableName + """ where date > """ + str(limitDate) + """ order by date""" 
# 	# print selectStatement
# 	cursor.execute(selectStatement)

# 	allValues = cursor.fetchall()

# 	# print len(allValues)
# 	# print allValues[1][2]

# 	smaVector = []

# 	for i in range(0,len(allValues)):
		
# 		## Initializing smaVector
# 		if i < smaPeriod:
# 			smaVector.append(allValues[i][1])
# 			# print(smaVector)
# 			continue

# 		if allValues[i][2] != None:
# 			for j in range(0,smaPeriod-1):
# 				# print smaVector
# 				smaVector[j] = smaVector[j+1]

# 			## Including new value
# 			smaVector[smaPeriod-1] = allValues[i][1]
# 			continue

# 		# else:
# 		# 	break

# 		## Calculating sma
# 		smaValue = sum(smaVector) / smaPeriod
# 		# print smaValue
# 		# print smaVector
# 		updateStatement = """UPDATE """  + tableName + """ SET  sma_""" + str(smaPeriod)+ "=" + str(smaValue) + """ where id = """ + str(allValues[i][0])
# 		cursor.execute(updateStatement)
# 		# print i
# 		## Shifting previous period value
# 		for j in range(0,smaPeriod-1):
# 			# print smaVector
# 			smaVector[j] = smaVector[j+1]

# 		## Including new value
# 		smaVector[smaPeriod-1] = allValues[i][1]

# 		# print smaVector


# 	conn.commit()
# 	conn.close()


# def updateEMAPeriod(tableName, emaPeriod, timeDelay = False):

# 	if not timeDelay:
# 		limitDate = int(time.time()) - emaPeriod * 300 * 2
# 	else:
# 		limitDate = int(time.time()) - timeDelay

# 	# print limitDate
# 	##### Retrieving data to process
# 	conn = sqlite3.connect(db_name)

# 	cursor = conn.cursor()



# 	selectStatement = """SELECT id, close, sma_"""+ str(emaPeriod)+ """, ema_""" + str(emaPeriod) + """ FROM """  + tableName + """ where date > """ + str(limitDate) + """ order by date """
# 	# print selectStatement
# 	cursor.execute(selectStatement)

# 	allValues = cursor.fetchall()

# 	# print len(allValues)
# 	# print allValues[1][2]

# 	emaValue = 0
# 	emaFactor = 2.0 / (emaPeriod + 1)

# 	for i in range(emaPeriod,len(allValues)):
# 		if allValues[i][3] != None:
# 			### EMA was already calculated, we pass
# 			# print "Hey I am here " + str(allValues[i][0])
# 			emaValue = allValues[i][3]
# 			continue
# 		else:
# 			## Calculating ema
# 			emaValue = emaValue + emaFactor*(allValues[i][1] - emaValue)
# 		# print "Plop"

# 		updateStatement = """UPDATE """  + tableName + """ SET  ema_""" + str(emaPeriod)+ "=" + str(emaValue) + """ where id = """ + str(allValues[i][0])
# 		cursor.execute(updateStatement)

# 	conn.commit()
# 	conn.close()
		







