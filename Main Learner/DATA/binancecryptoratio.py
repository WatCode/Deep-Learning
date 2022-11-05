from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from decimal import *
from math import *

api_key = "xtJNJ5ye25ze6DbFrX9zlMrcl16IyDeSUdAKVBOTou5vEb7RDWlFRTzK2EvurcJD"
secret_key = "YU3boe3opckvNEwVvFpSEVm4JPjMheFOHIbtUDSEmQdlPn9OMhou2WWNPyQOg1yA"

client = Client(api_key, secret_key)

ticker = "BTCUSDT"

klines = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "60 days ago UTC")

average_size = 10

shift_count = 1

close_prices = [Decimal(entry[4]) for entry in klines]

moving_average_close = [sum(close_prices[i:i+average_size])/Decimal(average_size) for i in range(len(close_prices)-average_size+1)]

moving_average_ratio = [str(moving_average_close[i+1]/moving_average_close[i]) for i in range(len(moving_average_close)-1)]

halfway_point = int(len(moving_average_ratio)/2)-int(len(moving_average_ratio)/2)%shift_count

to_write_train = ",".join(moving_average_ratio[:halfway_point])
to_write_validate = ",".join(moving_average_ratio[halfway_point:])
to_write_test = to_write_train+","+to_write_validate

filew_train = open("STREAM" + ticker + "RATIOTRAIN.txt", "a")
filew_train.write(str(shift_count) + "\n" + to_write_train)
filew_train.close()

filew_validate = open("STREAM" + ticker + "RATIOVALIDATE.txt", "a")
filew_validate.write(str(shift_count) + "\n" + to_write_validate)
filew_validate.close()

filew_test = open("STREAM" + ticker + "RATIOTEST.txt", "a")
filew_test.write(str(shift_count) + "\n" + to_write_test)
filew_test.close()