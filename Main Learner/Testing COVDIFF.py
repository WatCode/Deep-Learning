from DeepLearner import *
import matplotlib.pyplot as plt

data_name = input("Data name: ")
model_name = input("Model name: ")

Model = Model_Class()
Model.load(model_name)

Data = Data_Class()
Data.extract(data_name + "TEST")

header_count = 2

Model.recursive_test(Data, 300, header_count)

header_values = [[Model.recursive_output_values[j*header_count+i] for j in range(int(len(Model.recursive_output_values)/header_count))] for i in range(header_count)]

x_values = [i for i in range(int(len(Model.recursive_output_values)/header_count))]

fig, axs = plt.subplots(header_count)

for i in range(header_count):
    y_values = []
    cumulative_change = Decimal(0)
    
    for value in header_values[i]:
        y_values.append(value)
        cumulative_change += value
    
    axs[i].plot(x_values, y_values)

plt.show()