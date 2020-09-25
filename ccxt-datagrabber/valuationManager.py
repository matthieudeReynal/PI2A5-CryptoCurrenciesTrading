import psycopg2
import time
import datagrabber as grab
import ccxt

referenceCurrenciesSupply = {
	'BNT': 70 * 1000000,
	'LEND': 1300 * 1000000,
	'KNC': 180 * 1000000,
	'SNX': 90 * 1000000 ,
	'LRC': 1070 * 1000000,
	'REN': 1000 * 1000000,
	'ENJ': 1000 * 1000000,
	'BAND': 21 * 1000000,
	'AST': 500 * 1000000
}


class valuationManager:
	def __init__(self, connect_str, exchange, baseCurrency):

		self.connect_str = connect_str
		self.exchange = exchange
		self.baseCurrency = baseCurrency

	def getAssetPrices(self, quote_currency, timeStamp, duration = '5m'):

		trading_pair = quote_currency + "/" + self.baseCurrency
		##### Connect to db
		conn = psycopg2.connect(self.connect_str)
		cursor = conn.cursor()
		tableName = grab.getCandleTableName(self.exchange, trading_pair, duration)

		statement = "select high, low from %s where date < %s order by date desc limit 2" % (tableName, timeStamp)
		cursor.execute(statement)
		priceTuple = cursor.fetchone()
		conn.close()
		# print(priceTuple)
		if priceTuple == None:
			print("No data for this date %s " % timeStamp)
			return False, False
		buyPrice = priceTuple[0]
		sellPrice = priceTuple[1]

		return buyPrice, sellPrice

	def getPortfolioTotalValue (self, balancesList, timeOfExecution):
		totalValue = 0
		# print(balancesList)
		for currency in balancesList:
			# print(currency)
			optimisticPrice, pessimisticPrice = self.getAssetPrices(currency, timeOfExecution)
			totalValue += pessimisticPrice * balancesList[currency]

		return totalValue

	def getFullMcapValueForPortfolio(self, balancesList, timeOfExecution):
		portfolioComposition = {}
		for currency in balancesList:
			portfolioComposition[currency] = referenceCurrenciesSupply[currency]

		return self.getPortfolioTotalValue(portfolioComposition, timeOfExecution)

	def getPortfolioValues (self, balancesList, timeOfExecution):
		portfolioValues = {}
		# print(balancesList)
		for currency in balancesList:
			# print(currency)
			optimisticPrice, pessimisticPrice = self.getAssetPrices(currency, timeOfExecution)
			portfolioValues[currency] = pessimisticPrice * balancesList[currency]

		return portfolioValues

	def getPortfolioMcaps(self, balancesList, timeOfExecution):
		portfolioComposition = {}
		for currency in balancesList:
			portfolioComposition[currency] = referenceCurrenciesSupply[currency]

		return self.getPortfolioValues(portfolioComposition, timeOfExecution)

	def getNetworksMillionthOwned(self, balancesList, timeOfExecution):
		totalValue = self.getPortfolioTotalValue(balancesList, timeOfExecution)
		# print(totalValue)

		# - Calculer le tantieme de réseau agrégé possédé 
		mcapForPortfolio = self.getFullMcapValueForPortfolio(balancesList, timeOfExecution)
		# print(mcapForPortfolio)
		millionthOwned = 1000000*totalValue/mcapForPortfolio

		return millionthOwned

	def getMillionthOwnedPerCurrency(self, balancesList, timeOfExecution):

		allValues = self.getPortfolioValues(balancesList, timeOfExecution)
		# print(allValues)
		# - Calculer le tantieme de réseau agrégé possédé
		mcapsForPortfolio = self.getPortfolioMcaps(balancesList, timeOfExecution)
		# print(mcapsForPortfolio)
		millionthOwnedPortfolio = {}
		for currency in balancesList:
			millionthOwnedPortfolio[currency] = 1000000 * allValues[currency]/mcapsForPortfolio[currency]
		return millionthOwnedPortfolio








		

	def getEvenDistribution(self, baseBalance, currencies, timeOfExecution):

		fullMcap = self.getFullMcapValueForPortfolio(currencies, timeOfExecution)
		millionthOwned = baseBalance/fullMcap

		quote_balances = {}

		for currency in currencies:
			quote_balances[currency] = millionthOwned * referenceCurrenciesSupply[currency]

		return quote_balances



