from DeepLearner import *
import matplotlib.pyplot as plt

data_name = input("Data name: ")
model_name = input("Model name: ")

Model = Model_Class()
Model.load(model_name)

Data = Data_Class()
Data.extract(data_name + "TEST")

header_count = 4

Model.recursive_test(Data, 300, header_count)

header_values = [[Model.recursive_output_values[j*header_count+i] for j in range(int(len(Model.recursive_output_values)/header_count))] for i in range(header_count)]

x_values = [i for i in range(int(len(Model.recursive_output_values)/header_count))]

fig, axs = plt.subplots(header_count)

for i in range(header_count):
    y_values = []
    multiplier = Decimal(1)
    
    for value in header_values[i]:
        multiplier *= value
        
        y_values.append(multiplier)
    
    axs[i].plot(x_values, y_values)

plt.show()