from DeepLearner import *
import matplotlib.pyplot as plt
from decimal import *

getcontext().prec = 64

data_name = input("Name of data: ")
model_name = input("Name of model: ")

Model1 = Model()
Model1.load(model_name)

Data1 = Data(Model1)
Data1.extractall(data_name)

Model1.test(Data1)
print(Model1.output_values)