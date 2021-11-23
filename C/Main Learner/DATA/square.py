filew = open("SQUARETESTING.txt", "w")

for i in range(30):
    filew.write(str(i/10.0) + ",2:" + str((i/10.0)**2) + "\n")

filew.close()