from audioop import rms
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