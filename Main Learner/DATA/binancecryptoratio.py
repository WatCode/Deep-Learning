from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from decimal import *
from math import *

api_key = "xtJNJ5ye25ze6DbFrX9zlMrcl16IyDeSUdAKVBOTou5vEb7RDWlFRTzK2EvurcJD"
secret_key = "YU3boe3opckvNEwVvFpSEVm4JPjMheFOHIbtUDSEmQdlPn9OMhou2WWNPyQOg1yA"

client = Client(api_key, secret_key)

ticker = "BTCUSDT"

klines = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "6 days ago UTC")

average_size = 10

close_prices = [Decimal(entry[4]) for entry in klines]

moving_average_close = [sum(close_prices[i:i+average_size])/Decimal(average_size) for i in range(len(close_prices)-average_size+1)]

moving_average_ratio = [str(moving_average_close[i+1]/moving_average_close[i]) for i in range(len(moving_average_close)-1)]

input_size = 300
output_size = 10

model_count = 1

line_count = len(moving_average_ratio)-input_size-output_size

for i in range(line_count):
    print(i)
    model_num = floor(i/(line_count/model_count))
    
    to_write = ",".join(moving_average_ratio[i:i+input_size]) + ":" + ",".join(moving_average_ratio[i+input_size:i+input_size+output_size]) + "\n"

    if i%2 == 0:
        filew = open(ticker + "RATIO" + str(model_num) + "TRAIN.txt", "a")
    else:
        filew = open(ticker + "RATIO" + str(model_num) + "VALIDATE.txt", "a")
    filew.write(to_write)
    filew.close()
    
    filew = open(ticker + "RATIO" + str(model_num) + "TEST.txt", "a")
    filew.write(to_write)
    filew.close()