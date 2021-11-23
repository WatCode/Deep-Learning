from math import *

filew = open("SIN.txt", "w")
to_write = ""

for i in range(int(400*pi)):
    to_write += str(i/100) + ":" + str(sin(i/100)) + "\n"

filew.write(to_write[:-1])
filew.close()

filew = open("SINVALIDATION.txt", "w")
to_write = ""

for i in range(int(400*pi)):
    to_write += str(i/100+2.0*pi) + ":" + str(sin(i/100+2.0*pi)) + "\n"

filew.write(to_write[:-1])
filew.close()