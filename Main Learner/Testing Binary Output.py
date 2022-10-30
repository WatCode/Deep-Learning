from audioop import rms
from statistics import median
from DeepLearner import *
import matplotlib.pyplot as plt

data_name = input("Data name: ")
model_name = input("Model name: ")

Model = Model_Class()
Model.load(model_name)

Data = Data_Class(Model.input_count, Model.output_count)
Data.extract(data_name + "TEST")

Model.test(Data)

print(Model.output_values)

median_index = len(Data.target_values)-int(sum(Data.target_values))-1
sorted_output_values = sorted(Model.output_values)
output_value_threshold = (sorted_output_values[median_index]+sorted_output_values[median_index+1])/Decimal(2)

print(output_value_threshold)

for i in range(len(Model.output_values)):
    if Model.output_values[i] >= output_value_threshold:
        Model.output_values[i] = 1
    else:
        Model.output_values[i] = 0

mean_error = 0
rms_error = 0

for i in range(len(Data.target_values)):
    mean_error += abs((Model.output_values[i]-Data.target_values[i]))
    rms_error += (Model.output_values[i]-Data.target_values[i])**2
    
mean_error /= len(Data.target_values)
rms_error = (rms_error/Decimal(len(Data.target_values)))**Decimal(0.5)

print(mean_error)
print(rms_error)

filew = open("./" + model_name + "/RESULTS.txt", "w")
filew.write(",".join([str(i) for i in range(len(Data.target_values))]) + "\n")
filew.write(",".join([str(i) for i in Data.target_values]) + "\n")
filew.write(",".join([str(i) for i in Model.output_values]))
filew.close()