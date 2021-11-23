from decimal import *
from random import *

k01 = Decimal(0.915748218298252858382)
k02 = Decimal(0.834851291182879872217)

k1 = Decimal(1.3949867209205726765)
k2 = Decimal(1.2834739513647389458)
k3 = Decimal(2.3829249028428461492)
k4 = Decimal(1.4856829189385472123)

filew = open("WATCRYPT.txt", "w")

to_write = ""

for i in range(200):
    p1 = Decimal(random())
    p11 = (k01*p1+k02**(p1))

    for j in range(200):
        k1 = Decimal(1.0+random())
        o1 = k01*(k1*(k1-Decimal(1)))*p11
        to_write += str(p1) + "," +  str(k1) + ":" + str(o1) + "\n"

filew.write(to_write[:-1])
filew.close()

filew = open("WATCRYPTVALIDATION.txt", "w")

to_write = ""

for i in range(200):
    p1 = Decimal(random())
    p11 = (k01*p1+k02**(p1))

    for j in range(200):
        k1 = Decimal(1.0+random())
        o1 = k01*(k1*(k1-Decimal(1)))*p11
        to_write += str(p1) + "," +  str(k1) + ":" + str(o1) + "\n"

filew.write(to_write[:-1])
filew.close()