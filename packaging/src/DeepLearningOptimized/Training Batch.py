from DeepLearningOptimized import Model_DL
from DeepLearningOptimized import Data_DL

data_name = input("Data name: ")
model_name = input("Model name: ")

model_count = int(input("Model count: "))

for i in range(model_count):
    Model = Model_DL.model()
    Model.load(model_name + str(i), min_diff=0.00001, learning_rate=0.0000001, cycles=10, hidden_shaped=False, normaliser_depth=0)

    Data_train = Data_DL.data()
    Data_validate = Data_DL.data()

    Data_train.extract(data_name + "TRAIN")
    Data_validate.extract(data_name + "VALIDATE")

    Model.train(Data_train, Data_validate)
    Model.save()