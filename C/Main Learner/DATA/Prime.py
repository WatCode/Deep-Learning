from math import *

def is_prime(n):
    prime = True

    for i in range(floor(n**0.5)-1):
        if n%(i+2) == 0:
            prime = False
            break
    
    return prime

primes = []
composites =  []

for i in range(98):
    if is_prime(i+2):
        primes.append(str(i+2))
    else:
        composites.append(str(i+2))

input_size = 10
output_size = 1

mix = []
to_write = ""

for i in range(len(primes)-input_size-output_size):
    mix.append(composites[i])
    mix.append(primes[i])

for i in range(int(len(mix)/2)-1):
    to_write += mix[i] + "," + mix[i+1] + ":1\n"
    to_write += mix[i] + "," + mix[i+2] + ":0\n"

filew = open("PRIMES.txt", "w")
filew.write(to_write[:-1])
filew.close()