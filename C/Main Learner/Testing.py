from DeepLearner import *
import matplotlib.pyplot as plt

data_name = input("Data name: ")
model_name = input("Model name: ")

Model0 = Model()
Model0.load(model_name)

Data0 = Data(Model0.input_count)
Data0.extractall(data_name)

Model0.test(Data0)

y1 = [abs(i) for i in Data0.target_values_test]

sum_ratio1 = 0

for i in range(len(Data0.target_values_test)):
    sum_ratio1 += abs(Data0.target_values_test[i])

sum_ratio2 = 0

for i in range(len(Model0.output_values)):
    sum_ratio2 += abs(Model0.output_values[i])

print(sum_ratio1/sum_ratio2)