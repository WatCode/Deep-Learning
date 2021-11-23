from decimal import *

filer = open("COVRAW.txt", "r").read().split("\n")

countries = ["ZAF"]

country_new_cases_per_mill = {country:[] for country in countries}
country_new_deaths_per_mill = {country:[] for country in countries}
country_reproduction_rate = {country:[] for country in countries}
country_new_icu_per_mill = {country:[] for country in countries}
country_new_hosp_per_mill = {country:[] for country in countries}
country_new_tests_per_mill = {country:[] for country in countries}
country_positivity_rate = {country:[] for country in countries}
country_vacc_percent = {country:[] for country in countries}
country_stringency_index = {country:[] for country in countries}
country_population_density = {country:[] for country in countries}
country_median_age = {country:[] for country in countries}
country_life_expectancy = {country:[] for country in countries}
country_develop_index = {country:[] for country in countries}

for i in filer:
    line = i.split(",")

    if line[0] in countries and len(line[0]) > 0:
        for j in range(len(line)):
            if line[j] == "":
                try:
                    line[j] = last_line[j]
                except:
                    line[j] = "0"
                    continue

        country_new_cases_per_mill[line[0]].append(Decimal(line[12]))
        country_new_deaths_per_mill[line[0]].append(Decimal(line[15]))
        country_reproduction_rate[line[0]].append(Decimal(line[16])*Decimal(100))
        country_new_icu_per_mill[line[0]].append(Decimal(line[22]))
        country_new_hosp_per_mill[line[0]].append(Decimal(line[24]))
        country_new_tests_per_mill[line[0]].append(Decimal(line[30]))
        country_positivity_rate[line[0]].append(Decimal(line[31]))
        country_vacc_percent[line[0]].append(Decimal(line[41]))
        country_stringency_index[line[0]].append(Decimal(line[43]))
        country_population_density[line[0]].append(Decimal(line[45]))
        country_median_age[line[0]].append(Decimal(line[46]))
        country_life_expectancy[line[0]].append(Decimal(line[57]))
        country_develop_index[line[0]].append(Decimal(line[58])*Decimal(100))
    
        last_line = line[::-1][::-1]

input_size = 200
output_size = 1

filew_train = open("COV.txt", "w")
filew_test = open("COVVALIDATION.txt", "w")

to_write_train = ""
to_write_test = ""

for country in countries:
    new_cases_per_mill = country_new_cases_per_mill[country]
    new_deaths_per_mill = country_new_deaths_per_mill[country]
    reproduction_rate = country_reproduction_rate[country]
    new_icu_per_mill = country_new_icu_per_mill[country]
    new_hosp_per_mill = country_new_hosp_per_mill[country]
    new_tests_per_mill = country_new_tests_per_mill[country]
    positivity_rate = country_positivity_rate[country]
    vacc_percent = country_vacc_percent[country]
    stringency_index = country_stringency_index[country]
    population_density = country_population_density[country]
    median_age = country_median_age[country]
    life_expectancy = country_life_expectancy[country]
    develop_index = country_develop_index[country]

    half_point = int(len(new_cases_per_mill)/2)

    for i in range(len(new_cases_per_mill)-input_size-output_size):
        if i <= half_point:
            for j in range(input_size):
                value1 = new_cases_per_mill[i+j]
                value2 = new_deaths_per_mill[i+j]
                value3 = reproduction_rate[i+j]
                value4 = new_icu_per_mill[i+j]
                value5 = new_hosp_per_mill[i+j]
                value6 = new_tests_per_mill[i+j]
                value7 = positivity_rate[i+j]
                value8 = vacc_percent[i+j]
                value9 = stringency_index[i+j]
                value10 = population_density[i+j]
                value11 = median_age[i+j]
                value12 = life_expectancy[i+j]
                value13 = develop_index[i+j]
                to_write_test += str(value1) + "," + str(value2) + "," + str(value3) + "," + str(value4) + "," + str(value5) + "," + str(value6) + "," + str(value7) + "," + str(value8) + "," + str(value9) + "," + str(value10) + "," + str(value11) + "," + str(value12) + "," + str(value13) + ","

            to_write_test = to_write_test[:-1] + ":"

            for j in range(output_size):
                value1 = new_cases_per_mill[i+input_size+j]
                value2 = new_deaths_per_mill[i+input_size+j]
                value3 = reproduction_rate[i+input_size+j]
                value4 = new_icu_per_mill[i+input_size+j]
                value5 = new_hosp_per_mill[i+input_size+j]
                value6 = new_tests_per_mill[i+input_size+j]
                value7 = positivity_rate[i+input_size+j]
                value8 = vacc_percent[i+input_size+j]
                value9 = stringency_index[i+input_size+j]
                value10 = population_density[i+input_size+j]
                value11 = median_age[i+input_size+j]
                value12 = life_expectancy[i+input_size+j]
                value13 = develop_index[i+input_size+j]
                to_write_test += str(value1) + "," + str(value2) + "," + str(value3) + "," + str(value4) + "," + str(value5) + "," + str(value6) + "," + str(value7) + "," + str(value8) + "," + str(value9) + ","

            to_write_test = to_write_test[:-1] + "\n"

        for j in range(input_size):
            value1 = new_cases_per_mill[i+j]
            value2 = new_deaths_per_mill[i+j]
            value3 = reproduction_rate[i+j]
            value4 = new_icu_per_mill[i+j]
            value5 = new_hosp_per_mill[i+j]
            value6 = new_tests_per_mill[i+j]
            value7 = positivity_rate[i+j]
            value8 = vacc_percent[i+j]
            value9 = stringency_index[i+j]
            value10 = population_density[i+j]
            value11 = median_age[i+j]
            value12 = life_expectancy[i+j]
            value13 = develop_index[i+j]
            to_write_train += str(value1) + "," + str(value2) + "," + str(value3) + "," + str(value4) + "," + str(value5) + "," + str(value6) + "," + str(value7) + "," + str(value8) + "," + str(value9) + "," + str(value10) + "," + str(value11) + "," + str(value12) + "," + str(value13) + ","

        to_write_train = to_write_train[:-1] + ":"

        for j in range(output_size):
            value1 = new_cases_per_mill[i+input_size+j]
            value2 = new_deaths_per_mill[i+input_size+j]
            value3 = reproduction_rate[i+input_size+j]
            value4 = new_icu_per_mill[i+input_size+j]
            value5 = new_hosp_per_mill[i+input_size+j]
            value6 = new_tests_per_mill[i+input_size+j]
            value7 = positivity_rate[i+input_size+j]
            value8 = vacc_percent[i+input_size+j]
            value9 = stringency_index[i+input_size+j]
            value10 = population_density[i+input_size+j]
            value11 = median_age[i+input_size+j]
            value12 = life_expectancy[i+input_size+j]
            value13 = develop_index[i+input_size+j]
            to_write_train += str(value1) + "," + str(value2) + "," + str(value3) + "," + str(value4) + "," + str(value5) + "," + str(value6) + "," + str(value7) + "," + str(value8) + "," + str(value9) + ","
            
        to_write_train = to_write_train[:-1] + "\n"


filew_train.write(to_write_train[:-1])
filew_train.close()

filew_test.write(to_write_test[:-1])
filew_test.close()