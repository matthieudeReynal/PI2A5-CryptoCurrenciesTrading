import psycopg2
import time
import datagrabber as grab
import valuationManager as val
import ccxt

class orderManager:
	def __init__(self, connect_str, exchange, isSim, valuationObject):
		# if isSim:
		# 	print("this is a simulation")
		self.isSim = isSim
		self.connect_str = connect_str
		self.exchange = exchange
		# Getting exchange class
		exchange_class = getattr(ccxt, exchange)
		self.exchangeObject = exchange_class()
		self.valuationObject = valuationObject

	def swapCurrencies(self, quote_currency, direction, volume, timestamp):
		if self.isSim:
			# print("This is a simulation")
			return self.simSwapCurrencies(quote_currency, direction, volume, timestamp)
		else:
			print("This is a real order")
			return self.actualSwapCurrencies()

	def simSwapCurrencies(self, quote_currency, direction, originVolume, timestamp):
		buyPrice, sellPrice = self.valuationObject.getAssetPrices(quote_currency, timestamp)
		if buyPrice == False:
			return 0, 0

		binanceFeeMultiplier = 1-0.001
		### Converting
		if direction == 'buy':
			baseVolume = originVolume
			quoteVolume = baseVolume/buyPrice*binanceFeeMultiplier
		elif direction == 'sell':
			quoteVolume = originVolume
			baseVolume = quoteVolume*sellPrice*binanceFeeMultiplier

		return quoteVolume, baseVolume



	def actualSwapCurrencies(self):
		print("Not implemented yet")