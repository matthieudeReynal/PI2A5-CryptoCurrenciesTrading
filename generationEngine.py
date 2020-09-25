import robotEngine as re
import valuationManager as val
import simEngine as se
import valuationManager as val
import chromosomeEngine as chrEng
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import numpy as np
import copy

class generationEngine:
	def __init__(self):
		print("Initiating generationEngine, please wait")
		# Loading main robot configuration (base currency, connect str etc)
		self.setRobotConf()
		# Loading chromosomes configuration (bounds for parameters, etc)
		self.setChrConf()
		# Loading simulation configuration (time boundaries, etc)
		self.setSimConf()
		# Loading chromosome generation engine
		self.chrInstance = chrEng.chromosomeEngine(self.chrDescription)
		# Loading base balances
		self.setBaseBalance()
		# Running baseline simulation
		self.baseSim = se.simulation(self.simConf,self.robotClass,self.robotConf, self.initialBalances, self.initialBaseBalance)
		self.baseSim.runBaseline()
		self.generation = 0
		self.generationSize = 200

		# Generating gen 0 chromosomes
		self.generateFirstSimGeneration()
		print("generationEngine Initiated")

	def generateFirstSimGeneration(self):
		self.currentSimulations = []
		for i in range(0,self.generationSize):
			self.currentSimulations.append(self.getARandomSimulation())

	def getARandomSimulation(self):
		currentRobotConf = copy.deepcopy(self.robotConf)
		currentRobotConf["params"] = self.chrInstance.getRandChromosome()
		aSimulation = se.simulation(self.simConf,self.robotClass,currentRobotConf, self.initialBalances, self.initialBaseBalance)
		return aSimulation

	def mixTwoSims(self,sim1, sim2):
		currentRobotConf = copy.deepcopy(self.robotConf)
		currentRobotConf["params"] = self.chrInstance.mixChromosomes(sim1.robotObject.confJson["params"],sim2.robotObject.confJson["params"])
		aSimulation = se.simulation(self.simConf,self.robotClass,currentRobotConf, self.initialBalances, self.initialBaseBalance)
		return aSimulation

	def setRobotConf(self):
		self.robotClass = "exampleRobot"
		robotConf = {}
		robotConf["connect_str"] = "dbname='tradebotv4' user='tradebotv4' host='localhost' password='a-password'"
		robotConf["parameters"] = {}
		robotConf["exchange"] = "binance"
		robotConf["base_currency"] = "USDT"
		robotConf["candle_duration"] = "15m"
		robotConf["isSim"] = True
		self.robotConf = robotConf
		return robotConf

	def setChrConf(self):
		chrDescription = {}
		chrDescription["millionthOverBought"]= {}
		chrDescription["millionthUnderBought"]={}
		chrDescription["sellSignal"]= {}
		chrDescription["buySignal"]= {}
		chrDescription["sellSellPct"]= {}
		chrDescription["availableSellPct"]= {}
		chrDescription["averageLookback"]= {}
		

		chrDescription["millionthOverBought"]["lowerBound"]=1000
		chrDescription["millionthOverBought"]["upperBound"]=1200
		chrDescription["millionthOverBought"]["resolution"] = 1000
		chrDescription["millionthUnderBought"]["lowerBound"]=800
		chrDescription["millionthUnderBought"]["upperBound"]=1000
		chrDescription["millionthUnderBought"]["resolution"] = 1000
		chrDescription["sellSignal"]["lowerBound"]=800
		chrDescription["sellSignal"]["upperBound"]=1200
		chrDescription["sellSignal"]["resolution"] = 1000
		chrDescription["buySignal"]["lowerBound"]=800
		chrDescription["buySignal"]["upperBound"]=1200
		chrDescription["buySignal"]["resolution"] = 1000
		chrDescription["sellSellPct"]["lowerBound"]=0
		chrDescription["sellSellPct"]["upperBound"]=500
		chrDescription["sellSellPct"]["resolution"] = 100
		chrDescription["availableSellPct"]["lowerBound"]=0
		chrDescription["availableSellPct"]["upperBound"]=500
		chrDescription["availableSellPct"]["resolution"] = 100
		chrDescription["averageLookback"]["lowerBound"] = 1
		chrDescription["averageLookback"]["upperBound"] = 96
		chrDescription["averageLookback"]["resolution"] = 1
		
		self.chrDescription = chrDescription
		return chrDescription
	
	def setBaseBalance(self):
		valuationObject = val.valuationManager(self.robotConf["connect_str"], self.robotConf["exchange"], self.robotConf["base_currency"])
		self.initialBalances = valuationObject.getEvenDistribution( 1000, ["BNT", "LEND", "KNC", "BNT"],1592179200000)
		self.initialBaseBalance = 0

	def setSimConf(self):
		simConf = {}
		simConf["simStartTime"] = 1592179200000
		simConf["simStopTime"] = 1594771200000
		simConf["simTimeIncrement"] = 43200000
		self.simConf = simConf

	def createNewGeneration(self):
		self.currentSimulations = []
		for i in range (0, len(self.bestSims)):
			if self.bestSims[i][1].performance > 0:
				self.currentSimulations.append(self.bestSims[i][1])
				for j in range (i+1, len(self.bestSims)):
					self.currentSimulations.append(self.mixTwoSims(self.bestSims[i][1], self.bestSims[j][1]))
			else:
				self.currentSimulations.append(self.getARandomSimulation())
				for j in range (i+1, len(self.bestSims)):
					self.currentSimulations.append(self.getARandomSimulation())
		print(len(self.currentSimulations))
		while len(self.currentSimulations) < self.generationSize:
			self.currentSimulations.append(self.getARandomSimulation())
		print(len(self.currentSimulations))

	def runGeneration(self):
		startTime = time.time()
		# runASimulation(self.currentSimulations[0])
		# print(self.currentSimulations[0].hasRun)
		with ThreadPoolExecutor() as pool:
			simulations  = pool.map(runASimulation,self.currentSimulations)

		endTime = time.time()

		# Assess performance for all simulations
		allSim = []
		for element in simulations:
			simScore = element.compareToBaseline(self.baseSim.robotObject.results)
			if simScore >0 :
				print(simScore)
			allSim.append((simScore, copy.deepcopy(element)))

		# Select 20 best simulations
		def takeFirst(elem):
			return elem[0]
		# print(allSim)
		allSim.sort(key=takeFirst, reverse=True)
		# print([sim[0] for sim in allSim])
		self.bestSims = allSim[0:20]
		avgPerf = np.mean([perf[0] for perf in self.bestSims])
		print("Ran gen %s on %s chromosomes in %s seconds, average perf for top 20 is %s" % (self.generation, self.generationSize, endTime - startTime, avgPerf))
		
		print(self.bestSims[0][0], self.bestSims[0][1].robotObject.confJson["params"])
		# Generate next chromosome generation from best in class
		self.createNewGeneration()
		self.generation += 1


def runASimulation(aSimulation):
	# Launching a single simulation
	# robotConf["params"] = chrInstance.getRandChromosome()
	# Running actual simulation
	# print("Hello")
	if aSimulation.hasRun == False:
		aSimulation.run()

	return aSimulation


