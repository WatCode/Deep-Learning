from decimal import *
from binance.client import Client
from binance.websockets import BinanceSocketManager

client = Client("eUBdIviMwPpuiP3SfeST4Y2SKsqqLA6pMUyyYG5UP6gkAqQ0z9RQyvdAyIogwCmf", "VhLxZQ0RKebDCiyZnkHCbE0XlAmOJhwSfIt9sH5PiZ6VDJl6d0wIWG8QgEzDq9Nt")

initial_input_count = 100
initial_output_count = 4

real_values_bid = []
real_values_ask = []

real_diff_values_bid = []
real_diff_values_ask = []

counter = 0

def simulate(data):
    global counter, initial_input_count, real_values_bid, real_values_ask, real_diff_values_bid, real_diff_values_ask

    filew_bid = open("BTC_bid.txt", "a")
    filew_ask = open("BTC_ask.txt", "a")

    filew_action = open("BTC_action.txt", "a")

    latest_bid = Decimal(data["b"])
    latest_ask = Decimal(data["a"])

    if counter > 0:
        real_diff_values_bid.append(latest_bid-real_values_bid[-1])
        real_diff_values_ask.append(latest_ask-real_values_ask[-1])
    
    real_values_bid.append(Decimal(latest_bid))
    real_values_ask.append(Decimal(latest_ask))

    if counter >= initial_input_count+initial_output_count:
        greatest_bid = min(real_diff_values_bid[:-1])
        if max(real_diff_values_bid[:-1]) > abs(min(real_diff_values_bid[:-1])):
            greatest_bid = max(real_diff_values_bid[:-1])
        greatest_ask = min(real_diff_values_ask[:-1])
        if max(real_diff_values_ask[:-1]) > abs(min(real_diff_values_ask[:-1])):
            greatest_ask = max(real_diff_values_ask[:-1])      
        greatest = abs(greatest_ask)
        if abs(greatest_bid) > abs(greatest_ask):
            greatest = abs(greatest_bid)

        choice = ""

        if real_values_bid[-1] > real_values_ask[-2] and real_values_bid[-2] < real_values_ask[-1]:
            choice = "B"
        if real_values_bid[-1] < real_values_ask[-2] and real_values_bid[-2] > real_values_ask[-1]:
            choice = "S"

        line_bid = ""
        line_ask = ""

        for i in range(initial_input_count):
            line_bid += str(real_diff_values_bid[i]/greatest) + ","
            line_ask += str(real_diff_values_ask[i]/greatest) + ","
        
        line_bid = line_bid[:-1] + ":"
        line_ask = line_ask[:-1] + ":"

        for i in range(initial_output_count):
            line_bid += str(real_diff_values_bid[initial_input_count+i]/greatest) + ","
            line_ask += str(real_diff_values_ask[initial_input_count+i]/greatest) + ","

        filew_bid.write(line_bid[:-1] + "\n")
        filew_ask.write(line_ask[:-1] + "\n")

        filew_bid.close()
        filew_ask.close()

        line_action = line_bid+line_ask[:-1]

        if choice == "B":
            line_action += ":1,0\n"
        if choice == "S":
            line_action += ":0,1\n"
        if choice == "":
            line_action += ":0,0\n"
        
        filew_action.write(line_action)
        filew_action.close()

        real_diff_values_bid.pop(0)
        real_diff_values_ask.pop(0)

        real_values_bid.pop(0)
        real_values_ask.pop(0)

    counter += 1

bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket("BTCUSDT", simulate)
bsm.start()