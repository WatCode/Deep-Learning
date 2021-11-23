from decimal import *
from random import *

k1 = Decimal(1.3949867209205726765)
k2 = Decimal(0.2834739513647389458)
k3 = Decimal(0.3829249028428461492)
k4 = Decimal(0.4856829189385472123)

filew = open("WATCRYPTTRAIN.txt", "w")

to_write = ""

for i in range(1000):
    p1 = Decimal(random())
    o1 = k1*((p1+k1)**k1)+k1

    p2 = Decimal(random())
    o2 = k2*((o1+p2+k2)**k2)+k2

    p3 = Decimal(random())
    o3 = k3*((o2+p3+k3)**k3)+k3

    p4 = Decimal(random())
    o4 = k4*((o3+p4+k4)**k4)+k4
    
    k0 = Decimal(random())

    to_write += str(p1) + "," + str(k0) + ":" + str(o1*k0) + "\n"

filew.write(to_write[:-1])
filew.close()

filew = open("WATCRYPTVALIDATE.txt", "w")

to_write = ""

for i in range(1000):
    p1 = Decimal(random())
    o1 = k1*((p1+k1)**k1)+k1

    p2 = Decimal(random())
    o2 = k2*((o1+p2+k2)**k2)+k2

    p3 = Decimal(random())
    o3 = k3*((o2+p3+k3)**k3)+k3

    p4 = Decimal(random())
    o4 = k4*((o3+p4+k4)**k4)+k4
    
    k0 = Decimal(random())

    to_write += str(p1) + "," + str(k0) + ":" + str(o1*k0) + "\n"

filew.write(to_write[:-1])
filew.close()

filew = open("WATCRYPTTEST.txt", "w")

to_write = ""

for i in range(1000):
    p1 = Decimal(random())
    o1 = k1*((p1+k1)**k1)+k1

    p2 = Decimal(random())
    o2 = k2*((o1+p2+k2)**k2)+k2

    p3 = Decimal(random())
    o3 = k3*((o2+p3+k3)**k3)+k3

    p4 = Decimal(random())
    o4 = k4*((o3+p4+k4)**k4)+k4
    
    k0 = Decimal(random())

    to_write += str(p1) + "," + str(k0) + ":" + str(o1*k0) + "\n"

filew.write(to_write[:-1])
filew.close()