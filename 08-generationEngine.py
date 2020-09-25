import copy
import generationEngine 
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# def runASimulation(robotConf, chrInstance, robotClass, initialBalances, initialBaseBalance):
# 	# Launching a single simulation
# 	robotConf["params"] = chrInstance.getRandChromosome()
# 	# # Running actual simulation
# 	# aSimulation = se.simulation(simConf,robotClass,robotConf, initialBalances, initialBaseBalance)
# 	# aSimulation.run()

# 	return robotConf
# 	# return aSimulation

myGeneration = generationEngine.generationEngine()
while myGeneration.generation < 6:
	myGeneration.runGeneration()

# robotConfVector = [myGeneration.robotConf for i in range(0,10)]
# chrInstanceVector = [myGeneration.chrInstance for i in range(0,10)]
# initialBalancesVector = [myGeneration.initialBalances for i in range(0,10)]
# initialBaseBalanceVector = [myGeneration.initialBaseBalance for i in range(0,10)]
# with ThreadPoolExecutor() as pool:
# 	simulations  = pool.map(runASimulation, robotConfVector, chrInstanceVector, initialBalancesVector, initialBaseBalanceVector)



