from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import matplotlib.pyplot as plt
from DeepLearner import *
from decimal import *
from time import *

getcontext().prec = 64

model_name = input("Model name: ")
model_count = int(input("Model count: "))

Trade_Models = []

for i in range(model_count):
    Trade_Models.append(Model())
    Trade_Models[i].load(model_name+str(i))

Trade_Data = Data(Trade_Models[0].input_count)

api_key = "xtJNJ5ye25ze6DbFrX9zlMrcl16IyDeSUdAKVBOTou5vEb7RDWlFRTzK2EvurcJD"
secret_key = "YU3boe3opckvNEwVvFpSEVm4JPjMheFOHIbtUDSEmQdlPn9OMhou2WWNPyQOg1yA"

client = Client(api_key, secret_key)

ticker = "ETHBTC"

trade_fees = Decimal(0.00075)

USDT_balance = Decimal(1000)
BTC_balance = Decimal(0)

USDT_invested = Decimal(0)
fees_paid = Decimal(0)

predicted_count = 60

average_size = 10

x_values = [i for i in range(Trade_Models[0].input_count+predicted_count)]

while True:
    klines = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "6 hours ago UTC")
    
    previous_prices = [Decimal(element[4]) for element in klines[-Trade_Models[0].input_count-average_size:]]
    
    change_prices = [previous_prices[i+1]-previous_prices[i] for i in range(len(previous_prices)-1)]
    
    moving_average_change = [sum(change_prices[i:i+average_size])/Decimal(average_size) for i in range(len(change_prices)-average_size+1)]
    
    y_values = previous_prices[average_size:]
    
    Trade_Data.load([], [], [], [], moving_average_change, [])
    
    recursive_output_values = [Decimal(0) for i in range(predicted_count)]
    
    for i in range(model_count):
        Trade_Models[i].recursive_test(Trade_Data, predicted_count, 1)
        
        for j in range(predicted_count):
            recursive_output_values[j] += Trade_Models[i].recursive_output_values[-predicted_count+j]
    
    for i in range(predicted_count):
        recursive_output_values[i] /= Decimal(model_count)
    
    net_change = Decimal(0)
    compounded_change = []
    
    for change in recursive_output_values:
        net_change += change
        
        compounded_change.append(net_change/previous_prices[-1])
        y_values.append(y_values[-1]+change)
    
    proportion = Decimal(1)
    
    if proportion > 1:
        proportion = Decimal(1)
    
    BTCUSDT_rate = previous_prices[-1]
        
    all_positive = False
    all_negative = False
    
    index = 0
    
    for change in compounded_change:
        index += 1
        
        if change < -trade_fees:
            all_negative = True
            break
        if change > trade_fees:
            all_positive = True
            break
    
    for change in compounded_change[:index]:
        if all_negative:
            if change > 0:
                all_negative = False
                break
        if all_positive:
            if change < 0:
                all_positive = False
                break
    
    if all_positive:
        fees_paid += trade_fees*(proportion*USDT_balance)
        
        BTC_balance += (Decimal(1)-trade_fees)*((proportion*USDT_balance)/BTCUSDT_rate)
        USDT_invested += proportion*USDT_balance
        USDT_balance *= (Decimal(1)-proportion)
    if all_negative:
        if BTC_balance > 0 and (Decimal(1)-trade_fees)*BTCUSDT_rate >= USDT_invested/BTC_balance:
            fees_paid += trade_fees*((proportion*BTC_balance)*BTCUSDT_rate)
            
            USDT_balance += (Decimal(1)-trade_fees)*((proportion*BTC_balance)*BTCUSDT_rate)
            USDT_invested -= (Decimal(1)-trade_fees)*((proportion*BTC_balance)*BTCUSDT_rate)
            BTC_balance *= (Decimal(1)-proportion)
    
    print(index)
    print(compounded_change[-1])
    print(USDT_balance)
    print(BTC_balance*BTCUSDT_rate)
    print(USDT_balance+BTC_balance*BTCUSDT_rate)
    print(fees_paid)
    print("\n")
    
    #sleep(1)
    
    plt.clf()
    plt.plot(x_values, y_values)
    plt.pause(0.01)

plt.show()