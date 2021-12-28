from DeepLearner import *

data_name = input("Data name: ")
model_name = input("Model name: ")

Model0 = Model_Class()
Model0.load(model_name, min_diff=0.00001, learning_rate=0.0000001, cycles=5, hidden_shaped=False, normaliser_depth=0)

Data0 = Data_Class(Model0.input_count)
Data0.extractall(data_name)

Model0.train(Data0)
Model0.save()