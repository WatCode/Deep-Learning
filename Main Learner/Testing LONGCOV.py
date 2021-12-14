from numpy import maximum
from DeepLearner import *
import matplotlib.pyplot as plt

data_name = input("Data name: ")
model_name = input("Model name: ")

Model0 = Model()
Model0.load(model_name)

Data0 = Data(Model0.input_count)
Data0.extractall(data_name)

Model0.test(Data0)

symptom_count = 12

symptom_names = ['Shortness of Breath', 'Recurring Chest Pain', 'Low Oxygen Levels', 'Heart Rate Dysfunction', 'Constant Fatigue', 'Joint and Muscle Pain', 'Brain Fog', 'Loss of Smell/Taste', 'Sleep Disturbances', 'Depression/Anxiety', 'Digestive Problems', 'Kidney Problems']

symptom_target_values = [[Data0.target_values_test[j*symptom_count+i] for j in range(int(len(Data0.target_values_test)/symptom_count))] for i in range(symptom_count)]

symptom_output_values = [[Model0.output_values[j*symptom_count+i] for j in range(int(len(Model0.output_values)/symptom_count))] for i in range(symptom_count)]

symptom_minimum_threshold_vector = []
symptom_maximum_threshold_vector = []
symptom_average_threshold_vector = []

for i in range(symptom_count):
    minimum = max(symptom_output_values[i])
    maximum = min(symptom_output_values[i])
    
    for j in range(len(symptom_output_values[i])):
        if symptom_target_values[i][j] == Decimal(1) and symptom_output_values[i][j] < minimum:
            minimum = symptom_output_values[i][j]
        if symptom_target_values[i][j] == Decimal(0) and symptom_output_values[i][j] > maximum:
            maximum = symptom_output_values[i][j]
    
    symptom_minimum_threshold_vector.append(minimum)
    symptom_maximum_threshold_vector.append(maximum)
    symptom_average_threshold_vector.append(sum(symptom_output_values[i])/len(symptom_output_values[i]))
    
print(symptom_minimum_threshold_vector)
print(symptom_maximum_threshold_vector)

proportion = sum(Model0.output_values)/len(Model0.output_values)

new_output_values = []

count_positive = 0
total_positive = 0

count_negative = 0
total_negative = 0

for i in range(len(Model0.output_values)):
    symptom_num = i%symptom_count
    
    if symptom_minimum_threshold_vector[symptom_num] >= symptom_maximum_threshold_vector[symptom_num]:
        if Model0.output_values[i] >= symptom_minimum_threshold_vector[symptom_num]:
            new_output_values.append(Decimal(1))
        else:
            new_output_values.append(Decimal(0))
    else:
        if Model0.output_values[i] <= symptom_minimum_threshold_vector[symptom_num]+(symptom_maximum_threshold_vector[symptom_num]-symptom_minimum_threshold_vector[symptom_num])*proportion:
            new_output_values.append(Decimal(1))
        else:
            new_output_values.append(Decimal(0))
    
    if Data0.target_values_test[i] == Decimal(1):
        if new_output_values[i] == Data0.target_values_test[i]:
            count_positive += 1
        
        total_positive += 1
    else:
        if new_output_values[i] == Data0.target_values_test[i]:
            count_negative += 1
        
        total_negative += 1
    
print(count_positive/total_positive)
print(count_negative/total_negative)