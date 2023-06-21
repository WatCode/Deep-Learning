import Model_DL
import Data_DL

data_name = input("Data name: ")
model_name = input("Model name: ")

Model = Model_DL.model()
Model.load(model_name, min_diff=0.001, learning_rate=0.0000001, cycles=30, ignore_minimum=0, activation_values=[4,4,4,100], hidden_shaped=False, normaliser_depth=0)

Data_train = Data_DL.data()
Data_validate = Data_DL.data()

Data_train.extract(data_name + "TRAIN")
Data_validate.extract(data_name + "VALIDATE")

Model.train(Data_train, Data_validate)
Model.save()