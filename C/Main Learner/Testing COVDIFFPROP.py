from DeepLearner import *
import matplotlib.pyplot as plt

data_name = input("Data name: ")
model_name = input("Model name: ")

Model0 = Model()
Model0.load(model_name)

Data0 = Data(Model0.input_count)
Data0.extractall(data_name)

header_count = 1

Model0.recursive_test(Data0, 200, header_count)

header_values = [[Model0.recursive_output_values[j*header_count+i] for j in range(int(len(Model0.recursive_output_values)/header_count))] for i in range(header_count)]

x_values = [i for i in range(int(len(Model0.recursive_output_values)/header_count))]

for i in range(header_count):
    y_values = []
    cumulative_change = Decimal(0)
    
    for value in header_values[i]:
        y_values.append(value)
        cumulative_change += value
    
    plt.plot(x_values, y_values)

plt.show()