import robotEngine as re




connect_str = "dbname='tradebotv4' user='tradebotv4' host='localhost' password='a-password'"

robotConf = {}
robotConf["connect_str"] = "dbname='tradebotv4' user='tradebotv4' host='localhost' password='a-password'"

robotConf["parameters"] = {}
robotConf["exchange"] = "binance"
robotConf["base_currency"] = "USDT"
robotConf["candle_duration"] = "1d"
robotConf["isSim"] = True

initialBalances = {}
initialBalances["BNT"] = 10
initialBalances["LEND"] = 1000
initialBaseBalance = 0

robotInstance = re.exampleRobot(robotConf,initialBalances, initialBaseBalance)
robotInstance.run(1592492241000)