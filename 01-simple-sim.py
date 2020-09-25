import simEngine as se
import robotEngine as re
import copy

simConf = {}
simConf["simStartTime"] = 1592179200000
simConf["simStopTime"] = 1594771200000
simConf["simTimeIncrement"] = 43200000

robotClass = "exampleRobot"
robotConf = {}
robotConf["connect_str"] = "dbname='tradebotv4' user='tradebotv4' host='localhost' password='a-password'"
robotConf["parameters"] = {}
robotConf["exchange"] = "binance"
robotConf["base_currency"] = "USDT"
robotConf["candle_duration"] = "1d"
robotConf["isSim"] = True
robotConf["params"] = {}
robotConf["params"]["millionthOverBought"]= 1.1
robotConf["params"]["millionthUnderBought"]= 0.9
robotConf["params"]["sellSignal"]= 1.01
robotConf["params"]["buySignal"]= 0.99
robotConf["params"]["sellSellPct"]= 0.03
robotConf["params"]["availableSellPct"]= 0.02

initialBalances = {}
initialBalances["BNT"] = 10
initialBalances["LEND"] = 1000
initialBaseBalance = 0

simRobotConf = copy.deepcopy(robotConf)
baselineRobotConf = copy.deepcopy(robotConf)

# Running baseline simulation
baseSim = se.simulation(simConf,robotClass,baselineRobotConf, initialBalances, initialBaseBalance)
baseSim.runBaseline()

# Running actual simulation
firstSim = se.simulation(simConf,robotClass,simRobotConf, initialBalances, initialBaseBalance)
firstSim.run()


print(firstSim.compareToBaseline(baseSim.robotObject.results))





