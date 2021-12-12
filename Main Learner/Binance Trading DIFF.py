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

USDT_principal = Decimal(100)

C1_balance = Decimal(0)
C2_balance = Decimal(0)

fees_paid = Decimal(0)

predicted_count = 45

average_size = 10

x_values = [i for i in range(Trade_Models[0].input_count+predicted_count)]

i = 0

while True:
    C1C2_klines = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "24 hours ago UTC")
    C1USDT_klines = client.get_historical_klines(ticker[:3] + "USDT", Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
    C2USDT_klines = client.get_historical_klines(ticker[-3:] + "USDT", Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
    
    C1USDT_rate = Decimal(C1USDT_klines[0][4])
    C2USDT_rate = Decimal(C2USDT_klines[0][4])
    
    if i == 0:
        C1_balance += USDT_principal/C1USDT_rate
    
    previous_rates = [Decimal(element[4]) for element in C1C2_klines[-Trade_Models[0].input_count-average_size:]]
    
    change_rates = [previous_rates[i+1]-previous_rates[i] for i in range(len(previous_rates)-1)]
    
    moving_average_previous_rates = [sum(previous_rates[i:i+average_size])/Decimal(average_size) for i in range(len(change_rates)-average_size+1)]
    
    moving_average_change_rates = [sum(change_rates[i:i+average_size])/Decimal(average_size) for i in range(len(change_rates)-average_size+1)]
    
    y_values = moving_average_previous_rates
    
    Trade_Data.load([], [], [], [], moving_average_change_rates, [])
    
    recursive_output_values = [Decimal(0) for i in range(predicted_count)]
    
    for i in range(model_count):
        Trade_Models[i].recursive_test(Trade_Data, predicted_count, 1)
        
        for j in range(predicted_count):
            recursive_output_values[j] += Trade_Models[i].recursive_output_values[-predicted_count+j]
    
    for i in range(predicted_count):
        recursive_output_values[i] /= Decimal(model_count)
    
    compounded_change = []
    
    for change in recursive_output_values:
        compounded_change.append(Decimal(1)-(previous_rates[-1]/y_values[-1]))
        y_values.append(y_values[-1]+change)
    
    C1C2_rate = previous_rates[-1]
        
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

    proportion = (abs(compounded_change[index-1])-trade_fees)/trade_fees
    
    if proportion > 1:
        proportion = Decimal(1)
    
    if all_positive:
        fees_paid += trade_fees*((proportion*C2_balance)*C2USDT_rate)
        
        C1_balance += (Decimal(1)-trade_fees)*((proportion*C2_balance)/C1C2_rate)
        C2_balance *= (Decimal(1)-proportion)
    if all_negative:
        fees_paid += trade_fees*((proportion*C1_balance)*C1USDT_rate)
        
        C2_balance += (Decimal(1)-trade_fees)*((proportion*C1_balance)*C1C2_rate)
        C1_balance *= (Decimal(1)-proportion)
        
    USDT_value = C1_balance*C1USDT_rate+C2_balance*C2USDT_rate
    
    print("Minutes: " + str(index))
    print("Price change: " + str(float(compounded_change[index-1])))
    print(ticker[:3] + " value in USDT: " + str(float(C1_balance*C1USDT_rate)))
    print(ticker[-3:] + " value in USDT: " + str(float(C2_balance*C2USDT_rate)))
    print("Total value in USDT: " + str(float(USDT_value)))
    print("Total fees paid in USDT: " + str(float(fees_paid)))
    print("Total value generated in USDT: " + str(float(USDT_value+fees_paid)))
    print("\n")
    
    plt.clf()
    plt.plot(x_values, y_values)
    plt.plot(x_values[:-predicted_count], previous_rates[average_size:])
    plt.pause(0.01)

    i += 1
    
plt.show()