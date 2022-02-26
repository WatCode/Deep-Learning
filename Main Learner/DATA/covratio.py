from decimal import *

getcontext().prec = 64

filer = open("COVRAW.txt", "r").read().split("\n")

heading_list = filer[0].split(",")

iso_list = ["OWID_WRL"]
iso_data = {iso:{heading:[] for heading in heading_list} for iso in iso_list}

iso_lengths = {iso:0 for iso in iso_list}

for line in filer[1:]:
    line_split = line.split(",")
    
    if line_split[0] in iso_list:
        iso_lengths[line_split[0]] += 1
        
        for i in range(len(line_split)):
            value = line_split[i]
            
            if len(value) == 0:
                value = 0
            
            try:
                value = Decimal(value)
            except:
                continue
            finally:
                iso_data[line_split[0]][heading_list[i]].append(value)

target_headings = ["new_cases_smoothed_per_million", "new_deaths_smoothed_per_million", "people_fully_vaccinated_per_hundred", "total_boosters_per_hundred"]

normalised_iso_data = {iso:{heading:[] for heading in target_headings} for iso in iso_list}

for iso in iso_list:
    for heading in target_headings:
        for i in range(len(iso_data[iso][heading])-1):
            if iso_data[iso][heading][i] == 0 or iso_data[iso][heading][i+1] == 0:
                normalised_iso_data[iso][heading].append(Decimal(1))
            else:
                normalised_iso_data[iso][heading].append(iso_data[iso][heading][i+1]/iso_data[iso][heading][i])
            
input_size = 200
output_size = 7

to_write_train = ""
to_write_validate = ""
to_write_test = ""

for iso in iso_list:
    for i in range(iso_lengths[iso]-input_size-output_size-1):
        for j in range(input_size):
            for heading in target_headings:
                if i%2 == 0:
                    to_write_train += str(normalised_iso_data[iso][heading][i+j]) + ","
                else:
                    to_write_validate += str(normalised_iso_data[iso][heading][i+j]) + ","
                if iso == iso_list[0]:
                    to_write_test += str(normalised_iso_data[iso][heading][i+j]) + ","

        if i%2 == 0:
            to_write_train = to_write_train[:-1] + ":"
        else:
            to_write_validate = to_write_validate[:-1] + ":"
        if iso == iso_list[0]:
            to_write_test = to_write_test[:-1] + ":"

        for j in range(output_size):
            for heading in target_headings:
                if i%2 == 0:
                    to_write_train += str(normalised_iso_data[iso][heading][i+input_size+j]) + ","
                else:
                    to_write_validate += str(normalised_iso_data[iso][heading][i+input_size+j]) + ","
                
                to_write_test += str(normalised_iso_data[iso][heading][i+input_size+j]) + ","
        
        if i%2 == 0:
            to_write_train = to_write_train[:-1] + "\n"
        else:
            to_write_validate = to_write_validate[:-1] + "\n"
        if iso == iso_list[0]:
            to_write_test = to_write_test[:-1] + "\n"
    
filew = open("COVRATIOTRAIN.txt", "w")
filew.write(to_write_train[:-1])
filew.close()

filew = open("COVRATIOVALIDATE.txt", "w")
filew.write(to_write_validate[:-1])
filew.close()

filew = open("COVRATIOTEST.txt", "w")
filew.write(to_write_test[:-1])
filew.close()