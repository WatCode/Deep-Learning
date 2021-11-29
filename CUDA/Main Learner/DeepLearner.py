from random import *
from time import *
from math import *
from ctypes import *
import numpy as np
import os

clib = CDLL("./deep.dll")

def findsize(hidden_sizes, bias_count):
    total_size = 0
    
    for i in range(len(hidden_sizes)-1):
        total_size += (hidden_sizes[i]+bias_count)*hidden_sizes[i+1]
    
    return total_size

def createsizes(hidden_count, layer_count):
    base = ceil(hidden_count/2.0)
    step = 0

    if layer_count > 2:
        step = int(base/(ceil(layer_count/2.0)-1))
    else:
        base = hidden_count

    hidden_sizes = []

    for i in range(layer_count):
        if i < layer_count/2.0:
            hidden_sizes.append(base+(step*i))
        else:
            hidden_sizes.append(base+(step*(layer_count-i-1)))

    return hidden_sizes

def findmean(values):
    mean = sum(values)/float(len(values))

    return mean

def finddeviation(values, mean):
    variance = 0

    for value in values:
        variance += (value-mean)**2
    
    variance /= float(len(values))
    deviation = variance**float(0.5)

    return deviation

def varyfind(output_values, target_values):
    diff = 0

    for i in range(len(output_values)):
        diff += abs(output_values[i]-target_values[i])

    return diff/float(len(output_values))

class Model:
    def __init__(self):
        self.model_name = ""
        self.hidden_shaped = False
        self.normaliser_depth = 0
        
        self.bias_count = 0
        self.weights_count = 0
        self.input_count = 0
        self.total_hidden_count = 0
        self.output_count = 0
        self.layer_count = 0
        self.activation_values = []
        self.hidden_sizes_values = []
        self.weights_values = []
        self.output_values = []
        self.recursive_output_values = []

        self.c_bias_count = 0
        self.c_weights_count = 0
        self.c_input_count = 0
        self.c_total_hidden_count = 0
        self.c_output_count = 0
        self.c_layer_count = 0
        self.c_activation_values = []
        self.c_hidden_sizes_values = []
        self.c_weights_values = []
        self.c_output_values = []

    def load(self, model_name="", bias_count=-1, input_count=-1, hidden_count=-1, output_count=-1, layer_count=-1, activation_values=[], min_diff=-1, learning_rate=-1, cycles=-1, hidden_shaped=False, normaliser_depth=-1, softmax=False):
        self.model_name = model_name
        self.hidden_shaped = hidden_shaped
        self.normaliser_depth = normaliser_depth

        new_model = False

        if not os.path.exists("./" + self.model_name):
            new_model = True
            os.mkdir("./" + self.model_name + "/")

            if layer_count == -1:
                self.bias_count = int(input("Number of bias neurons: "))
                self.input_count = int(input("Number of input neurons: "))
                self.hidden_count = int(input("Number of hidden neurons: "))
                self.output_count = int(input("Number of output neurons: "))
                self.activation_values = [4 for i in range(6)]

                if softmax:
                    self.activation_values += [100]
                    
                self.layer_count = len(self.activation_values)-1
            else:
                self.bias_count = bias_count
                self.input_count = input_count
                self.hidden_count = hidden_count
                self.output_count = output_count
                self.activation_values = activation_values
                self.layer_count = layer_count

            if self.hidden_shaped:
                self.hidden_sizes_values = createsizes(self.hidden_count, self.layer_count)
            else:
                self.hidden_sizes_values = [self.hidden_count for i in range(self.layer_count)]
            
            self.hidden_sizes_values = [self.input_count]+self.hidden_sizes_values+[self.output_count]

            self.total_hidden_count = sum(self.hidden_sizes_values[1:-1])

            self.weights_count = findsize(self.hidden_sizes_values, self.bias_count)

            self.randomiseweights()
        else:
            self.get()
        
        self.min_diff = min_diff
        self.c_min_diff = c_float(self.min_diff)
        self.learning_rate = learning_rate
        self.c_learning_rate = c_float(self.learning_rate)
        self.cycles = cycles
        self.c_cycles = c_int(self.cycles)
        
        self.c_bias_count = c_int(self.bias_count)
        self.c_weights_count = c_int(self.weights_count)
        self.c_input_count = c_int(self.input_count)
        self.c_total_hidden_count = c_int(self.total_hidden_count)
        self.c_output_count = c_int(self.output_count)
        self.c_layer_count = c_int(self.layer_count)

        activation_values_seq = c_int*len(self.activation_values)
        self.c_activation_values = activation_values_seq(*self.activation_values)

        hidden_sizes_values_seq = c_int*len(self.hidden_sizes_values)
        self.c_hidden_sizes_values = hidden_sizes_values_seq(*self.hidden_sizes_values)

        weights_values_seq = c_float*len(self.weights_values)
        self.c_weights_values = weights_values_seq(*self.weights_values)

        if self.normaliser_depth > 0:
            self.NModel = Model()
            self.NModel.load(self.model_name + "/NORMALISER", 1, self.output_count, 6, self.output_count, 3, [4,4,4], -1, -1, -1, False, self.normaliser_depth-1, softmax)

            self.NData = Data(self.NModel)
        
        if new_model:
            self.save()

    def save(self):
        if "nan" not in [str(value).lower() for value in self.weights_values]:
            config_file = open("./" + self.model_name + "/config.txt", "w")
            config_file.write(str(self.normaliser_depth) + "," + str(self.bias_count) + "," + str(self.weights_count) + "," + str(self.layer_count) + "\n" + ",".join([str(value) for value in self.hidden_sizes_values]) + "\n" + ",".join([str(value) for value in self.activation_values]))
            config_file.close()

            self.weights_values = [float(value) for value in self.c_weights_values]

            weight_index = 0

            for layer_num in range(self.layer_count+1):
                to_write = ""

                for i in range(self.hidden_sizes_values[layer_num+1]):
                    to_write += ",".join([str(value) for value in self.weights_values[weight_index:weight_index+(self.hidden_sizes_values[layer_num]+self.bias_count)]]) + "\n"
                    
                    weight_index += (self.hidden_sizes_values[layer_num]+self.bias_count)

                weight_file = open("./" + self.model_name + "/hidden" + str(layer_num) + ".txt", "w")
                weight_file.write(to_write[:-1])
                weight_file.close()
            
            if self.normaliser_depth > 0:
                self.NModel.save()
    
    def get(self):
        config_file = open("./" + self.model_name + "/config.txt", "r").read()
        config_split = config_file.split("\n")

        config_data = config_split[0].split(",")
        self.normaliser_depth = int(config_data[0])
        self.bias_count = int(config_data[1])
        self.weights_count = int(config_data[2])
        self.layer_count = int(config_data[3])

        self.hidden_sizes_values = [int(value) for value in config_split[1].split(",")]

        self.input_count = self.hidden_sizes_values[0]
        self.output_count = self.hidden_sizes_values[-1]

        self.total_hidden_count = sum(self.hidden_sizes_values[1:-1])

        self.activation_values = [int(value) for value in config_split[2].split(",")]

        self.weights_values = []
        
        for layer_num in range(self.layer_count+1):
            weights_file = open("./" + self.model_name + "/hidden" + str(layer_num) + ".txt", "r").read()
            weights_split = weights_file.split("\n")

            for i in range(self.hidden_sizes_values[layer_num+1]):
                self.weights_values += [float(value) for value in weights_split[i].split(",")]
    
    def randomiseweights(self):
        self.weights_values = []
        
        for layer_num in range(self.layer_count+1):
            current_weights = np.random.normal(float(1/self.hidden_sizes_values[layer_num]), float(self.hidden_sizes_values[layer_num+1]/(self.hidden_sizes_values[layer_num]**2)), (self.hidden_sizes_values[layer_num]+self.bias_count)*self.hidden_sizes_values[layer_num+1])
            shuffle(current_weights)

            self.weights_values += [float(values) for values in current_weights]
    
    def train(self, Data):
        if self.learning_rate == -1:
            temp_cycles = 16
            temp_c_cycles = c_int(temp_cycles)
            temp_min_diff = -1
            temp_c_min_diff = c_float(temp_min_diff)
            self.learning_rate = float(0)

            fault = False

            for i in range(64):
                if fault:
                    self.learning_rate -= float(1)/float(2)**(i+1)
                else:
                    self.learning_rate += float(1)/float(2)**(i+1)

                self.c_learning_rate = c_float(self.learning_rate)

                backup_weights_values = self.weights_values.copy()
                clib.train(self.c_min_diff, self.c_learning_rate, Data.c_line_count_train, Data.c_input_values_train, Data.c_target_values_train, Data.c_line_count_test, Data.c_input_values_test, Data.c_target_values_test, self.c_layer_count, self.c_activation_values, self.c_hidden_sizes_values, self.c_total_hidden_count, self.c_bias_count, self.c_weights_count, self.c_weights_values)
                self.weights_values = [float(value) for value in self.c_weights_values]

                if "nan" in [str(value).lower() for value in self.weights_values] or self.weights_values == backup_weights_values:
                    fault = True
                else:
                    fault = False

                self.weights_values = backup_weights_values.copy()
                weights_values_seq = c_float*len(self.weights_values)
                self.c_weights_values = weights_values_seq(*self.weights_values)
            
            self.learning_rate *= float("0." + 16*"9")
            self.c_learning_rate = c_float(self.learning_rate)
            
        clib.train(self.c_min_diff, self.c_learning_rate, Data.c_line_count_train, Data.c_input_values_train, Data.c_target_values_train, Data.c_line_count_test, Data.c_input_values_test, Data.c_target_values_test, self.c_layer_count, self.c_activation_values, self.c_hidden_sizes_values, self.c_total_hidden_count, self.c_bias_count, self.c_weights_count, self.c_weights_values)

        self.weights_values = [float(value) for value in self.c_weights_values]

        if self.normaliser_depth > 0:
            self.test(Data, False)

            midpoint_index = int((len(self.output_values)/self.output_count)/2)*self.output_count

            normaliser_input_values_train = self.output_values[:midpoint_index]
            normaliser_target_values_train = Data.target_values_test[:midpoint_index]
            normaliser_input_values_test = self.output_values
            normaliser_target_values_test = Data.target_values_test

            self.NData.load(normaliser_input_values_train, normaliser_target_values_train, normaliser_input_values_test, normaliser_target_values_test)

            self.NModel.train(self.NData)
    
    def genetic_train(self, Data, deviation_coefficient, loop_count, pool_size):
        for i in range(loop_count):
            weights_values_list = []
            weights_values_set = {}
            diff_values = []

            for j in range(pool_size-len(weights_values_list)):
                self.randomiseweights()

                weights_values_list.append(self.weights_values)
            
            for weights_values in weights_values_list:
                weights_values_seq = c_float*len(weights_values)
                self.c_weights_values = weights_values_seq(*weights_values)

                self.test(Data, False)

                diff = varyfind(self.output_values, Data.target_values_test)
                diff_values.append(diff)

                weights_values_set[diff] = weights_values
            
            mean = findmean(diff_values)
            deviation = finddeviation(diff_values, mean)

            weights_values_sum = [float(0) for j in range(self.weights_count)]
            weights_values_count = 0
            avg_diff = 0

            for diff in diff_values:
                if diff <= mean-deviation*float(deviation_coefficient):
                    weights_values_sum = [weights_values_sum[j]+weights_values_set[diff][j] for j in range(self.weights_count)]
                    weights_values_count += 1
                    avg_diff += diff

                weights_values_list.remove(weights_values_set[diff])
                weights_values_set.pop(diff)
            
            avg_diff /= float(weights_values_count)
            print(avg_diff)
            print(weights_values_count)
            
            for j in range(self.weights_count):
                weights_values_sum[j] /= float(weights_values_count)
            
            for j in range(pool_size):
                weights_values_list.append([value*float(1.0+random()/1000.0) for value in weights_values_sum])
        
        self.weights_values = weights_values_sum

    def test(self, Data, test_mode=True):
        self.output_values = []

        self.c_output_values_seq = c_float*(Data.line_count_test*self.output_count)
        self.c_output_values = self.c_output_values_seq(*self.output_values)

        clib.test(Data.c_line_count_test, Data.c_input_values_test, self.c_layer_count, self.c_activation_values, self.c_hidden_sizes_values, self.c_total_hidden_count, self.c_bias_count, self.c_weights_count, self.c_weights_values, self.c_output_values)

        self.output_values = [float(value) for value in self.c_output_values]

        if self.normaliser_depth > 0 and test_mode:
            self.NData.load([], [], self.output_values, [])

            self.NModel.test(self.NData)

            self.output_values = self.NModel.output_values

    def recursive_test(self, Data, feedback_count, loop_count):
        self.recursive_output_values = Data.input_values_test[:self.input_count]+Data.target_values_test

        for i in range(loop_count):
            Data.load([], [], self.recursive_output_values[-self.input_count:], [])

            self.test(Data)

            self.recursive_output_values += self.output_values

class Data:
    def __init__(self, parent_model):
        self.parent_model = parent_model

        self.line_count_train = 0
        self.line_count_test = 0
        self.input_values_train = []
        self.target_values_train = []
        self.input_values_test = []
        self.target_values_test = []

        self.c_line_count_train = 0
        self.c_line_count_test = 0
        self.c_input_values_train = []
        self.c_target_values_train = []
        self.c_input_values_test = []
        self.c_target_values_test = []

    def load(self, input_values_train, target_values_train, input_values_test, target_values_test):
        self.line_count_train = int(len(input_values_train)/self.parent_model.input_count)
        self.line_count_test = int(len(input_values_test)/self.parent_model.input_count)

        self.input_values_train = input_values_train
        self.target_values_train = target_values_train
        self.input_values_test = input_values_test
        self.target_values_test = target_values_test

        self.c_line_count_train = c_int(self.line_count_train)
        self.c_line_count_test = c_int(self.line_count_test)

        c_input_values_train_seq = c_float*len(input_values_train)
        c_target_values_train_seq = c_float*len(target_values_train)
        c_input_values_test_seq = c_float*len(input_values_test)
        c_target_values_test_seq = c_float*len(target_values_test)

        self.c_input_values_train = c_input_values_train_seq(*input_values_train)
        self.c_target_values_train = c_target_values_train_seq(*target_values_train)
        self.c_input_values_test = c_input_values_test_seq(*input_values_test)
        self.c_target_values_test = c_target_values_test_seq(*target_values_test)
    
    def extract(self, data_name):
        data_input = []
        data_target = []

        try:
            data_file = open("./DATA/" + data_name + ".txt", "r").read().split("\n")

            for data_line in data_file:
                data_split = data_line.split(":")

                data_input += [float(value) for value in data_split[0].split(",")]
                data_target += [float(value) for value in data_split[1].split(",")]
        finally:
            return data_input, data_target
        
    def extractall(self, data_name):
        data_train = self.extract(data_name)
        data_test = self.extract(data_name + "VALIDATION")

        self.load(data_train[0], data_train[1], data_test[0], data_test[1])