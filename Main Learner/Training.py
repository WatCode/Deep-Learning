from DeepLearner import *

data_name = input("Data name: ")
model_name = input("Model name: ")

Model = Model_Class()
Model.load(model_name, min_diff=0.00001, learning_rate=0.000001, cycles=20, hidden_shaped=False, normaliser_depth=0)

Data_train = Data_Class()
Data_validate = Data_Class()

Data_train.extract(data_name + "TRAIN")
Data_validate.extract(data_name + "VALIDATE")

Model.train(Data_train, Data_validate)
Model.save()