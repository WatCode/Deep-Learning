from DeepLearner import *

data_name = input("Data name: ")
model_name = input("Model name: ")

Model = Model_Class()
Model.load(model_name, min_diff=0.00001, learning_rate=0.0001, cycles=1000, hidden_shaped=False, normaliser_depth=0)

Data_train = Data_Class(Model.input_count, Model.output_count)
Data_validate = Data_Class(Model.input_count, Model.output_count)

Data_train.extract(data_name + "TRAIN")
Data_validate.extract(data_name + "VALIDATE")

Model.train(Data_train, Data_validate)
Model.save()