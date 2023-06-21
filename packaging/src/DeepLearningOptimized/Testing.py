import Model_DL
import Data_DL

data_name = input("Data name: ")
model_name = input("Model name: ")

Model = Model_DL.model()
Model.load(model_name)

Data = Data_DL.data()
Data.extract(data_name + "TEST")

Model.test(Data)

print(Model.output_values)