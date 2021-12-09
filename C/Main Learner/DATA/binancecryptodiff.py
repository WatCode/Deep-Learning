from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from decimal import *
from math import *

api_key = "xtJNJ5ye25ze6DbFrX9zlMrcl16IyDeSUdAKVBOTou5vEb7RDWlFRTzK2EvurcJD"
secret_key = "YU3boe3opckvNEwVvFpSEVm4JPjMheFOHIbtUDSEmQdlPn9OMhou2WWNPyQOg1yA"

client = Client(api_key, secret_key)

klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "50 days ago UTC")

close_prices = [Decimal(entry[4]) for entry in klines]

close_diff = [close_prices[i+1]-close_prices[i] for i in range(len(close_prices)-1)]
moving_average_diff = [str(sum(close_diff[i:i+10])/Decimal(10)) for i in range(len(close_diff)-9)]

input_size = 300
output_size = 10

model_count = 50

line_count = len(moving_average_diff)-input_size-output_size

for i in range(line_count):
    print(i)
    model_num = floor(i/(line_count/model_count))
    
    to_write = ",".join(moving_average_diff[i:i+input_size]) + ":" + ",".join(moving_average_diff[i+input_size:i+input_size+output_size]) + "\n"

    if i%2 == 0:
        filew = open("BTCDIFF" + str(model_num) + "TRAIN.txt", "a")
    else:
        filew = open("BTCDIFF" + str(model_num) + "VALIDATE.txt", "a")
    filew.write(to_write)
    filew.close()
    
    filew = open("BTCDIFF" + str(model_num) + "TEST.txt", "a")
    filew.write(to_write)
    filew.close()