from decimal import *
from random import *

k1 = Decimal(1.3949867209205726765)

filew = open("WATCRYPTTRAIN.txt", "w")

to_write = ""

for i in range(500):
    k0 = Decimal(random()+0.5)
    
    for i in range(10):
        p1 = Decimal(random()+0.5)
        o1 = (p1*k0)**k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"
    
    p1 = Decimal(random()+0.5)
    
    for i in range(10):
        k0 = Decimal(random()+0.5)
        o1 = (p1*k0)**k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"

filew.write(to_write[:-1])
filew.close()

filew = open("WATCRYPTVALIDATE.txt", "w")

to_write = ""

for i in range(500):
    k0 = Decimal(random()+0.5)
    
    for i in range(10):
        p1 = Decimal(random()+0.5)
        o1 = (p1*k0)**k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"
    
    p1 = Decimal(random()+0.5)
    
    for i in range(10):
        k0 = Decimal(random()+0.5)
        o1 = (p1*k0)**k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"

filew.write(to_write[:-1])
filew.close()

filew = open("WATCRYPTTEST.txt", "w")

to_write = ""

for i in range(500):
    k0 = Decimal(random()+0.5)
    
    for i in range(10):
        p1 = Decimal(random()+0.5)
        o1 = (p1*k0)**k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"
    
    p1 = Decimal(random()+0.5)
    
    for i in range(10):
        k0 = Decimal(random()+0.5)
        o1 = (p1*k0)**k1

        to_write += str(p1) + "," + str(k0) + ":" + str(o1) + "\n"

filew.write(to_write[:-1])
filew.close()