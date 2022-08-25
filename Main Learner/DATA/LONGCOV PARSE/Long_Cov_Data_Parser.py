filer = [values.split(",") for values in open("Data_long_Cov.csv", "r").read().split("\n\n")]
filew = open("LONGCOVRAW.txt", "w")

target_attributes = ["Gender", "Weight_kg", "Length_cm", "CancerRemission", "CancerChemo", "CancerRadiation", "HospitalisedCovid19", "CovidAsymptomatic", "CovidMild", "CovidModerate", "CovidNoSymptoms", "CovidSevOxygen", "CovidSevVentilator", "Age", "CoMorbidity0", "CoMorbidity1", "CoMorbidity2", "CoMorbidity3", "CoMorbidity4", "CoMorbidity5", "CoMorbidity6", "CoMorbidity7", "CoMorbidity8", "CoMorbidity9", "CoMorbidity10", "CoMorbidity11", "CoMorbidity12", "CoMorbidity13", "Symptoms0", "Symptoms1", "Symptoms2", "Symptoms3", "Symptoms4", "Symptoms5", "Symptoms6", "Symptoms7", "Symptoms8", "Symptoms9", "Symptoms10", "Symptoms11"]

list_values = []
count = 0

to_write = ""

for values in filer[1:]:
    current = []
    
    for i in range(len(values)):
        if filer[0][i] in target_attributes:
            if filer[0][i] == "Gender":
                if values[i] == "1":
                    current += ["1", "0"]
                else:
                    current += ["0", "1"]
            else:
                current += [values[i]]
    
    line = ",".join(current) + "\n"
    
    #if line not in list_values:
    list_values.append(line)
    to_write += str(count)+","+line
    
    count += 1
    
filew.write(to_write[:-1])
filew.close()