filew = open("FUNC.txt", "w")

for i in range(300):
    filew.write(str(i/10.0) + ":" + str(3.0*(i/10.0)+4.0) + "\n")

filew.close()