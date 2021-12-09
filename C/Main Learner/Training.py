from DeepLearner import *

data_name = input("Data name: ")
model_name = input("Model name: ")

model_count = 50

for i in range(model_count):
    Model0 = Model()
    Model0.load(model_name+str(i), bias_count=1, input_count=300, hidden_count=64, output_count=10, layer_count=5, activation_values=[4 for i in range(6)], min_diff=0.001, learning_rate=0.00000001, cycles=5, hidden_shaped=False, normaliser_depth=0)

    Data0 = Data(Model0.input_count)
    Data0.extractall(data_name+str(i))

    Model0.train(Data0)
    Model0.save()