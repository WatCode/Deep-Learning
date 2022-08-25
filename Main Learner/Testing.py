from DeepLearner import *
import matplotlib.pyplot as plt

data_name = input("Data name: ")
model_name = input("Model name: ")

Model0 = Model_Class()
Model0.load(model_name)

Data0 = Data_Class(Model0.input_count)
Data0.extractall(data_name)

Model0.test(Data0)

Model0.output_values = [round(float(Model0.output_values[i])) for i in range(len(Model0.output_values))]

mean_error = 0

for i in range(len(Data0.target_values_test)):
    mean_error += abs((Model0.output_values[i]-Data0.target_values_test[i]))
    
mean_error /= len(Data0.target_values_test)

print(mean_error)

filew = open(model_name + "results.txt", "w")
filew.write(",".join([str(i) for i in range(len(Data0.target_values_test))]) + "\n")
filew.write(",".join([str(i) for i in Data0.target_values_test]) + "\n")
filew.write(",".join([str(i) for i in Model0.output_values]))
filew.close()