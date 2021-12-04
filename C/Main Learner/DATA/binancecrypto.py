from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from decimal import *
from math import *

api_key = "xtJNJ5ye25ze6DbFrX9zlMrcl16IyDeSUdAKVBOTou5vEb7RDWlFRTzK2EvurcJD"
secret_key = "YU3boe3opckvNEwVvFpSEVm4JPjMheFOHIbtUDSEmQdlPn9OMhou2WWNPyQOg1yA"

client = Client(api_key, secret_key)

klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "4 days ago UTC")

close_prices = [Decimal(entry[4]) for entry in klines]

close_ratio = [close_prices[i+1]/close_prices[i] for i in range(len(close_prices)-1)]

input_size = 300
output_size = 30

model_count = 4

line_count = len(close_ratio)-input_size-output_size

to_write_train = ["" for i in range(model_count)]
to_write_validate = ["" for i in range(model_count)]
to_write_test = ["" for i in range(model_count)]

for i in range(line_count):
    model_num = floor(i/(line_count/model_count))
    
    for j in range(input_size):
        if i%2 == 0:
            to_write_train[model_num] += str(close_ratio[i+j]) + ","
        else:
            to_write_validate[model_num] += str(close_ratio[i+j]) + ","
        to_write_test[model_num] += str(close_ratio[i+j]) + ","
    
    if i%2 == 0:
        to_write_train[model_num] += to_write_train[model_num][:-1] + ":"
    else:
        to_write_validate[model_num] += to_write_validate[model_num][:-1] + ":"
    to_write_test[model_num] += to_write_test[model_num][:-1] + ":"

    for j in range(output_size):
        if i%2 == 0:
            to_write_train[model_num] += str(close_ratio[i+input_size+j]) + ","
        else:
            to_write_validate[model_num] += str(close_ratio[i+input_size+j]) + ","
        to_write_test[model_num] += str(close_ratio[i+input_size+j]) + ","

    if i%2 == 0:
        to_write_train[model_num] += to_write_train[model_num][:-1] + "\n"
    else:
        to_write_validate[model_num] += to_write_validate[model_num][:-1] + "\n"
    to_write_test[model_num] += to_write_test[model_num][:-1] + "\n"

for i in range(model_count):
    filew = open("BTC" + str(i) + "TRAIN.txt", "w")
    filew.write(to_write_train[i][:-1])
    filew.close()

    filew = open("BTC" + str(i) + "VALIDATE.txt", "w")
    filew.write(to_write_validate[i][:-1])
    filew.close()
    
    filew = open("BTC" + str(i) + "TEST.txt", "w")
    filew.write(to_write_test[i][:-1])
    filew.close()