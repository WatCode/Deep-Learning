from decimal import *

for k in range(10):
    filer = open("BTCRAW"+str(k+1)+".txt", "r").read().split("\n")

    raw_prices = []

    for line in filer:
        line_split = line.split(",")

        raw_prices.append(Decimal(line_split[4]))

    multiplier_prices = []

    for i in range(len(raw_prices)-1):
        multiplier_prices.append(str(raw_prices[i+1]/raw_prices[i]))

    input_size = 200
    output_size = 10
    
    line_count = len(multiplier_prices)-input_size-output_size

    to_write_train = ""
    to_write_test = ""

    for i in range(line_count):
        if i < line_count/3:
            to_write_test += ",".join(multiplier_prices[i:i+input_size]) + ":" + ",".join(multiplier_prices[i+input_size:i+input_size+output_size]) + "\n"
        else:
            to_write_train += ",".join(multiplier_prices[i:i+input_size]) + ":" + ",".join(multiplier_prices[i+input_size:i+input_size+output_size]) + "\n"

    filew_train = open("BTC"+str(k+1)+".txt", "w")
    filew_train.write(to_write_train[:-1])
    filew_train.close()

    filew_test = open("BTC"+str(k+1)+"VALIDATION.txt", "w")
    filew_test.write(to_write_test[:-1])
    filew_test.close()