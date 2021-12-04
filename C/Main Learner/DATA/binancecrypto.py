from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from decimal import *
from math import *

api_key = "xtJNJ5ye25ze6DbFrX9zlMrcl16IyDeSUdAKVBOTou5vEb7RDWlFRTzK2EvurcJD"
secret_key = "YU3boe3opckvNEwVvFpSEVm4JPjMheFOHIbtUDSEmQdlPn9OMhou2WWNPyQOg1yA"

client = Client(api_key, secret_key)

klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "28 days ago UTC")

close_prices = [Decimal(entry[4]) for entry in klines]

close_ratio = [str(close_prices[i+1]/close_prices[i]) for i in range(len(close_prices)-1)]

input_size = 300
output_size = 10

model_count = 4

line_count = len(close_ratio)-input_size-output_size

for i in range(line_count):
    print(i)
    model_num = floor(i/(line_count/model_count))
    
    to_write = ",".join(close_ratio[i:i+input_size]) + ":" + ",".join(close_ratio[i+input_size:i+input_size+output_size]) + "\n"

    if i%2 == 0:
        filew = open("BTC" + str(model_num) + "TRAIN.txt", "a")
    else:
        filew = open("BTC" + str(model_num) + "VALIDATE.txt", "a")
    filew.write(to_write)
    filew.close()
    
    filew = open("BTC" + str(model_num) + "TEST.txt", "a")
    filew.write(to_write)
    filew.close()