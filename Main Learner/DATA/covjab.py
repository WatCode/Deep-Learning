import math

filer = open("COVJABRAW.txt", "r").read().split("\n")[:-1]

to_write_train = ""
to_write_validate = ""
to_write_test = ""

for i in range(len(filer)):
    line_split = filer[i].split(",")
    line_split[5] = str(math.tan(float(line_split[5])/(180.0/math.pi)))
    
    if i%3 != 1:
        to_write_train += ",".join(line_split) + "\n"
    else:
        to_write_validate += ",".join(line_split) + "\n"
        
    to_write_test += ",".join(line_split) + "\n"
    
filew_train = open("COVJABTRAIN.txt", "w")
filew_train.write(to_write_train[:-1])
filew_train.close()

filew_validate = open("COVJABVALIDATE.txt", "w")
filew_validate.write(to_write_validate[:-1])
filew_validate.close()

filew_test = open("COVJABTEST.txt", "w")
filew_test.write(to_write_test[:-1])
filew_test.close()