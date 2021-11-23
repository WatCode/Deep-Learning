from decimal import *

filew = open("MULTIPLICATION.txt", "w")

to_write = ""

for i in range(1000):
    base = 2.0
    power = 1.0+i/200.0
    calc = base*power

    to_write += str(base)+","+str(power)+":"+str(calc)+"\n"

filew.write(to_write[:-1])
filew.close()