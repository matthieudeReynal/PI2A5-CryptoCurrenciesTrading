import simEngine as se
import robotEngine as re
import copy
import chromosomeEngine as chrEng
import valuationManager as val
import generationEngine 

simConf = {}
simConf["simStartTime"] = 1592179200000
simConf["simStopTime"] = 1594771200000
simConf["simTimeIncrement"] = 43200000

myGeneration = generationEngine.generationEngine()
robotClass = "exampleRobot"

# Loading main robot configuration (base currency, connect str etc)
robotConf = myGeneration.getRobotConf()

# Loading chromosomes configuration (bounds for parameters, etc)
chrDescription = myGeneration.getChrConf()

# Loading chromosome generation engine
chrInstance = chrEng.chromosomeEngine(chrDescription)

# Loading initial balances
valuationObject = val.valuationManager(robotConf["connect_str"], robotConf["exchange"], robotConf["base_currency"])
initialBalances = valuationObject.getEvenDistribution( 1000, ["BNT", "LEND"],1592179200000)
initialBaseBalance = 0

# Running baseline simulation
baseSim = se.simulation(simConf,robotClass,robotConf, initialBalances, initialBaseBalance)
baseSim.runBaseline()

# Launching a single simulation
robotConf["params"] = chrInstance.getRandChromosome()

# Running actual simulation
firstSim = se.simulation(simConf,robotClass,robotConf, initialBalances, initialBaseBalance)
firstSim.run()


print(firstSim.compareToBaseline(baseSim.robotObject.results))





