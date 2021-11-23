from decimal import *

filer = open("COVRAW.txt", "r").read().split("\n")

new_cases = []

for i in filer:
    line = i.split(",")

    if line[0] == "ZAF":
        try:
            new_cases.append(Decimal(line[6]))
        except:
            continue

smoothed_new_cases = []

chunk_length = 1

for i in range(len(new_cases)-chunk_length+1):
    smoothed_new_cases.append(sum(new_cases[i:i+chunk_length])/Decimal(chunk_length))

maximum_smoothed_new_cases = max(smoothed_new_cases)

print(maximum_smoothed_new_cases)

normalised_smoothed_new_cases = [smoothed_new_cases[i]/maximum_smoothed_new_cases for i in range(len(smoothed_new_cases))]

input_size = 70
output_size = 1

filew_train = open("COV.txt", "w")
filew_test = open("COVVALIDATION.txt", "w")

to_write_train = ""
to_write_test = ""

half_point = int(len(normalised_smoothed_new_cases)/2)

for i in range(len(normalised_smoothed_new_cases)-input_size-1):
    if i < half_point-input_size:
        for value in normalised_smoothed_new_cases[i:i+input_size]:
            to_write_test += str(value) + ","
        to_write_test = to_write_test[:-1] + ":"
        for value in normalised_smoothed_new_cases[i+input_size:i+input_size+output_size]:
            to_write_test += str(value) + ","
        to_write_test = to_write_test[:-1] + "\n"
    else:
        for value in normalised_smoothed_new_cases[i:i+input_size]:
            to_write_train += str(value) + ","
        to_write_train = to_write_train[:-1] + ":"
        for value in normalised_smoothed_new_cases[i+input_size:i+input_size+output_size]:
            to_write_train += str(value) + ","
        to_write_train = to_write_train[:-1] + "\n"


filew_train.write(to_write_train[:-1])
filew_train.close()

filew_test.write(to_write_test[:-1])
filew_test.close()