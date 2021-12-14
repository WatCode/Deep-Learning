from random import *

filer = open("LONGCOVRAW.txt", "r").read().split("\n")

lines = []

for line in filer[1:]:
    line_split = line.split(",")
    
    lines.append(",".join(line_split[1:25]) + ":" + ",".join(line_split[25:]))

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