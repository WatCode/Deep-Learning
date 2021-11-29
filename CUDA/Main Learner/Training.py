from DeepLearner import *
import matplotlib.pyplot as plt
from decimal import *

getcontext().prec = 64

data_name = input("Name of data: ")
model_name = input("Name of model: ")

Model1 = Model()
Model1.load(model_name, min_diff=0.01, learning_rate=0.00000001, cycles=-1, hidden_shaped=False, normaliser_depth=0)

Data1 = Data(Model1)
Data1.extractall(data_name)

Model1.train(Data1)
Model1.save()