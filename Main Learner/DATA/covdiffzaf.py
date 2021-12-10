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

normalised_data = {heading:[] for heading in target_headings}

for heading in target_headings:
    for i in range(len(heading_data[heading])-1):
        normalised_data[heading].append((heading_data[heading][i+1]-heading_data[heading][i])/Decimal(heading_size[heading]))
            
moving_average_data = {heading:[] for heading in target_headings}

for heading in target_headings:
    length = 0
    
    for i in range(len(normalised_data[heading])-6):
        moving_average_data[heading].append(sum(normalised_data[heading][i:i+7])/Decimal(7))
        
        length += 1

input_size = 200
output_size = 7

to_write_train = ""
to_write_validate = ""
to_write_test = ""

for i in range(length-input_size-output_size):
    for j in range(input_size):
        for heading in target_headings:
            if i%2 == 0:
                to_write_train += str(moving_average_data[heading][i+j]) + ","
            else:
                to_write_validate += str(moving_average_data[heading][i+j]) + ","
            to_write_test += str(moving_average_data[heading][i+j]) + ","

    if i%2 == 0:
        to_write_train = to_write_train[:-1] + ":"
    else:
        to_write_validate = to_write_validate[:-1] + ":"
    to_write_test = to_write_test[:-1] + ":"

    for j in range(output_size):
        for heading in target_headings:
            if i%2 == 0:
                to_write_train += str(moving_average_data[heading][i+input_size+j]) + ","
            else:
                to_write_validate += str(moving_average_data[heading][i+input_size+j]) + ","
            to_write_test += str(moving_average_data[heading][i+input_size+j]) + ","
    
    if i%2 == 0:
        to_write_train = to_write_train[:-1] + "\n"
    else:
        to_write_validate = to_write_validate[:-1] + "\n"
    to_write_test = to_write_test[:-1] + "\n"
    
filew = open("COVDIFFZAFTRAIN.txt", "w")
filew.write(to_write_train[:-1])
filew.close()

filew = open("COVDIFFZAFVALIDATE.txt", "w")
filew.write(to_write_validate[:-1])
filew.close()

filew = open("COVDIFFZAFTEST.txt", "w")
filew.write(to_write_test[:-1])
filew.close()