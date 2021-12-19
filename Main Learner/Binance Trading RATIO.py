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

proportionality_constant = Decimal(0.001)

USDT_principal = Decimal(100)

C1_balance = Decimal(0)
C2_balance = Decimal(0)

fees_paid = Decimal(0)

predicted_count = 90

average_size = 10

start_flag = True

x_values = [i for i in range(Trade_Models[0].input_count+predicted_count)]

while True:
    C1C2_klines = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "12 hours ago UTC")
    C1USDT_klines = client.get_historical_klines(ticker[:3] + "USDT", Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
    C2USDT_klines = client.get_historical_klines(ticker[-3:] + "USDT", Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
    
    previous_rates = [Decimal(element[4]) for element in C1C2_klines]
    change_rates = [previous_rates[i+1]/previous_rates[i] for i in range(len(previous_rates)-1)]

    moving_average_previous_rates = [sum(previous_rates[i:i+average_size])/Decimal(average_size) for i in range(len(previous_rates)-average_size+1)]
    moving_average_change_rates = [sum(change_rates[i:i+average_size])/Decimal(average_size) for i in range(len(change_rates)-average_size+1)]
    
    input_values = []
    target_values = []
    
    for i in range(len(moving_average_change_rates)-Trade_Models[0].input_count+1):
        input_values += moving_average_change_rates[i:i+Trade_Models[0].input_count]
    
    for i in range(len(moving_average_change_rates)-Trade_Models[0].input_count-Trade_Models[0].output_count+1):
        target_values += moving_average_change_rates[i+Trade_Models[0].input_count:i+Trade_Models[0].input_count+Trade_Models[0].output_count]

    y_values = moving_average_previous_rates[-Trade_Models[0].input_count:]
    
    C1C2_rate = previous_rates[-1]

    try:
        C1USDT_rate = Decimal(C1USDT_klines[0][4])
        C2USDT_rate = Decimal(C2USDT_klines[0][4])
    except:
        continue
    
    if start_flag:
        C1_balance += USDT_principal/C1USDT_rate
        
        start_flag = False
    
    Trade_Data.load([], [], [], [], input_values, target_values)
    
    recursive_output_values = [Decimal(0) for i in range(predicted_count)]
    
    for i in range(model_count):
        Trade_Models[i].recursive_test(Trade_Data, predicted_count, 1)
        
        for j in range(predicted_count):
            recursive_output_values[j] += Trade_Models[i].recursive_output_values[-predicted_count+j]
    
    for i in range(predicted_count):
        recursive_output_values[i] /= Decimal(model_count)
    
    compounded_moving_change = []
    compounded_multiplier = Decimal(1)
    
    for multiplier in recursive_output_values:
        compounded_multiplier *= multiplier
        
        y_values.append(y_values[-1]*multiplier)
        compounded_moving_change.append(compounded_multiplier-Decimal(1))
        
    compounded_actual_change = []

    for change in compounded_moving_change:
        compounded_actual_change.append((moving_average_previous_rates[-1]*(change+Decimal(1)))/C1C2_rate-Decimal(1))

    moving_index = 0
    
    for change in compounded_moving_change:
        if change > trade_fees:
            break
        if change < -trade_fees:
            break
            
        moving_index += 1
    
    all_positive = False
    all_negative = False
    
    actual_index = 0
    
    for change in compounded_actual_change:
        if change > trade_fees:
            all_positive = True
            break
        if change < -trade_fees:
            all_negative = True
            break
            
        actual_index += 1
        
    if moving_index == len(compounded_moving_change):
        moving_index -= 1
    if actual_index == len(compounded_actual_change):
        actual_index -= 1
    
    for change in compounded_moving_change[:actual_index]:
        if all_positive:
            if change < 0:
                all_positive = False
                break
        if all_negative:
            if change > 0:
                all_negative = False
                break
        
    proportion = (abs(compounded_actual_change[actual_index])-proportionality_constant)/proportionality_constant
    
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
    
    print("Moving minutes: " + str(moving_index))
    print("Moving price change: " + str(float(compounded_moving_change[moving_index])))
    print("Actual minutes: " + str(actual_index))
    print("Actual price change: " + str(float(compounded_actual_change[actual_index])))
    print(ticker[:3] + " value in USDT: " + str(float(C1_balance*C1USDT_rate)))
    print(ticker[-3:] + " value in USDT: " + str(float(C2_balance*C2USDT_rate)))
    print("Total value in USDT: " + str(float(USDT_value)))
    print("Total fees paid in USDT: " + str(float(fees_paid)))
    print("Total value generated in USDT: " + str(float(USDT_value+fees_paid)))
    print("\n")
    
    plt.clf()
    plt.plot(x_values, y_values)
    plt.plot(x_values[:-predicted_count], previous_rates[-Trade_Models[0].input_count:])
    plt.pause(0.01)
    
plt.show()