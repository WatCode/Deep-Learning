from decimal import *

filer = open("BTCRAW07.txt", "r").read().split("\n")
filew = open("BTCVALIDATION005.txt", "w")

highvals = [Decimal(line.split(",")[2]) for line in filer]
minimum = Decimal(min(highvals))
maximum = Decimal(max(highvals))
interval = maximum-minimum
average = sum(highvals)/Decimal(len(highvals))

normvals = [price/average for price in highvals]
normvals = normvals[int(len(normvals)*0.5):]
leadlen = 10
laglen = 1
strw = ""

for i in range(0,len(normvals)-leadlen-laglen,1):
    for j in range(leadlen):
        strw += str(normvals[j+i])+","
    
    strw = strw[:-1] + ":"

    for k in range(laglen):
        strw += str(normvals[leadlen+k+i])+","

    strw = strw[:-1] + "\n"

filew.write(strw[:-1])
filew.close()