from decimal import *

getcontext().prec = 64

filer = open("COVDIFFZAFRAW.txt", "r").read().split("\n")

heading_list = filer[0].split(",")

heading_data = {heading:[] for heading in heading_list}

for line in filer[1:]:
    line_split = line.split(",")
    
    for i in range(len(line_split)):
        value = line_split[i]
        
        try:
            value = Decimal(value)
        except:
            continue
        finally:
            heading_data[heading_list[i]].append(value)

target_headings = ["EC","FS","GP","KZN","LP","MP","NC","NW","WC"]

heading_size = {"EC":6.712276,"FS":2.887465,"GP":15.176115,"KZN":11.289086,"LP":5.982584,"MP":4.592187,"NC":1.263875,"NW":4.027160,"WC":6.844272}

average_size = 7

diff_data = {heading:[] for heading in target_headings}

for heading in target_headings:
    for i in range(len(heading_data[heading])-1):
        diff_data[heading].append(heading_data[heading][i+1]-heading_data[heading][i])

normalised_data = {heading:[] for heading in target_headings}

for heading in target_headings:
    for i in range(len(diff_data[heading])-average_size+1):
        normalised_data[heading].append(sum(diff_data[heading][i:i+average_size])/Decimal(average_size))

input_size = 180
output_size = 7

for heading in target_headings:
    to_write_train = ""
    to_write_validate = ""
    to_write_test = ""
    
    for i in range(len(normalised_data[heading])-input_size-output_size):
        for j in range(input_size):
            if i%2 == 0:
                to_write_train += str(normalised_data[heading][i+j]) + ","
            else:
                to_write_validate += str(normalised_data[heading][i+j]) + ","
            to_write_test += str(normalised_data[heading][i+j]) + ","

        if i%2 == 0:
            to_write_train = to_write_train[:-1] + ":"
        else:
            to_write_validate = to_write_validate[:-1] + ":"
        to_write_test = to_write_test[:-1] + ":"

        for j in range(output_size):
            if i%2 == 0:
                to_write_train += str(normalised_data[heading][i+input_size+j]) + ","
            else:
                to_write_validate += str(normalised_data[heading][i+input_size+j]) + ","
            to_write_test += str(normalised_data[heading][i+input_size+j]) + ","
        
        if i%2 == 0:
            to_write_train = to_write_train[:-1] + "\n"
        else:
            to_write_validate = to_write_validate[:-1] + "\n"
        to_write_test = to_write_test[:-1] + "\n"
    
    filew = open("COVDIFFPROP" + heading.upper() + "TRAIN.txt", "w")
    filew.write(to_write_train[:-1])
    filew.close()

    filew = open("COVDIFFPROP" + heading.upper() + "VALIDATE.txt", "w")
    filew.write(to_write_validate[:-1])
    filew.close()

    filew = open("COVDIFFPROP" + heading.upper() + "TEST.txt", "w")
    filew.write(to_write_test[:-1])
    filew.close()