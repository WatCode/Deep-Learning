from random import *

filer = open("LONGCOVRAW.txt", "r").read().split("\n")

lines = []

duplicate_count = {}
input_output = {}

for line in filer[1:]:
    line_split = line.split(",")
    
    input_vector = ",".join(line_split[1:25])
    output_vector = [float(i) for i in line_split[25:]]
    
    if input_vector in input_output:
        duplicate_count[input_vector] += 1
        
        input_output[input_vector] = [input_output[input_vector][i]+output_vector[i] for i in range(len(output_vector))]
    else:
        input_output[input_vector] = output_vector
        duplicate_count[input_vector] = 1

for input_vector in input_output:
    lines.append(input_vector + ":" + ",".join([str(input_output[input_vector][i]/duplicate_count[input_vector]) for i in range(len(input_output[input_vector]))]))

shuffle(lines)

to_write_train = ""
to_write_validate = ""
to_write_test = ""    

for i in range(len(lines)):
    if i%2 == 0:
        to_write_train += lines[i] + "\n"
    else:
        to_write_validate += lines[i] + "\n"
    to_write_test += lines[i] + "\n"

filew = open("LONGCOVTRAIN.txt", "w")
filew.write(to_write_train[:-1])
filew.close()

filew = open("LONGCOVVALIDATE.txt", "w")
filew.write(to_write_validate[:-1])
filew.close()

filew = open("LONGCOVTEST.txt", "w")
filew.write(to_write_test[:-1])
filew.close()