filer = open("TTTCLASS.txt", "r").read().split("\n")
filew = open("TTTCLASS2.txt", "w")

for i in filer:
    line = i[:-11].replace("b", "0").replace("x", "0.5").replace("o", "-0.5")

    if i[-8:] == "positive":
        line += ":1"
    else:
        line += ":0"
    
    filew.write(line+"\n")

filew.close()