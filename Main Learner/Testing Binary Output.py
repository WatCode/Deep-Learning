from audioop import rms
from statistics import median
from DeepLearner import *
import matplotlib.pyplot as plt

data_name = input("Data name: ")
model_name = input("Model name: ")

Model0 = Model_Class()
Model0.load(model_name)

Data0 = Data_Class(Model0.input_count)
Data0.extractall(data_name, data_name, data_name)

Model0.test(Data0)

print(Model0.output_values)

median_index = len(Data0.target_values_test)-int(sum(Data0.target_values_test))-1
sorted_output_values = sorted(Model0.output_values)
print(median_index)
print(sorted_output_values)
output_value_threshold = (sorted_output_values[median_index]+sorted_output_values[median_index+1])/Decimal(2)

print(output_value_threshold)

for i in range(len(Model0.output_values)):
    if Model0.output_values[i] >= output_value_threshold:
        Model0.output_values[i] = 1
    else:
        Model0.output_values[i] = 0

mean_error = 0
rms_error = 0

for i in range(len(Data0.target_values_test)):
    mean_error += abs((Model0.output_values[i]-Data0.target_values_test[i]))
    rms_error += (Model0.output_values[i]-Data0.target_values_test[i])**2
    
mean_error /= len(Data0.target_values_test)
rms_error = (rms_error/Decimal(len(Data0.target_values_test)))**Decimal(0.5)

print(mean_error)
print(rms_error)

filew = open(model_name + "results.txt", "w")
filew.write(",".join([str(i) for i in range(len(Data0.target_values_test))]) + "\n")
filew.write(",".join([str(i) for i in Data0.target_values_test]) + "\n")
filew.write(",".join([str(i) for i in Model0.output_values]))
filew.close()