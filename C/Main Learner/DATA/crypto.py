from decimal import *
from random import *

k1 = Decimal(0.3949867209205726765)
k2 = Decimal(0.2834739513647389458)
k3 = Decimal(0.3829249028428461492)
k4 = Decimal(0.4856829189385472123)

filew = open("WATCRYPTTRAIN.txt", "w")

to_write = ""

for i in range(100):
    k0 = Decimal(random())
    
    for i in range(50):
        p1 = Decimal(random())
        o1 = k1*((p1*k0+k1)**k1)+k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"
    
    p1 = Decimal(random())
    
    for i in range(50):
        k0 = Decimal(random())
        o1 = k1*((p1*k0+k1)**k1)+k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"

filew.write(to_write[:-1])
filew.close()

filew = open("WATCRYPTVALIDATE.txt", "w")

to_write = ""

for i in range(100):
    k0 = Decimal(random())
    
    for i in range(50):
        p1 = Decimal(random())
        o1 = k1*((p1*k0+k1)**k1)+k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"
    
    p1 = Decimal(random())
    
    for i in range(50):
        k0 = Decimal(random())
        o1 = k1*((p1*k0+k1)**k1)+k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"

filew.write(to_write[:-1])
filew.close()

filew = open("WATCRYPTTEST.txt", "w")

to_write = ""

for i in range(100):
    k0 = Decimal(random())
    
    for i in range(50):
        p1 = Decimal(random())
        o1 = k1*((p1*k0+k1)**k1)+k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"
    
    p1 = Decimal(random())
    
    for i in range(50):
        k0 = Decimal(random())
        o1 = k1*((p1*k0+k1)**k1)+k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"

filew.write(to_write[:-1])
filew.close()