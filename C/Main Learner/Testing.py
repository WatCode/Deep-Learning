from DeepLearner import *
import matplotlib.pyplot as plt

data_name = input("Data name: ")
model_name = input("Model name: ")

Model0 = Model()
Model0.load(model_name)

Data0 = Data(Model0.input_count)
Data0.extractall(data_name)

Model0.test(Data0)

print(Model0.output_values)

new_output_values = []
avg_value = sum(Model0.output_values)/Decimal(len(Model0.output_values))

count = 0
total = 0

for i in range(len(Model0.output_values)):
    if Model0.output_values[i] >= avg_value:
        new_output_values.append(Decimal(1))
    else:
        new_output_values.append(Decimal(0))

    if Data0.target_values_test[i] == Decimal(1):
        total += 1
            
        if new_output_values[i] == Data0.target_values_test[i]:
            count += 1
    
print(count/total)