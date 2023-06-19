#Copyright (c) 2023 by Liam Roan Watson and Watcode. All rights reserved. For licensing, contact lrwatson@uwaterloo.ca or +1 437 688 3927

from decimal import *
from ctypes import *
import os

getcontext().prec = 64

c_type = c_double

if os.system("nvcc --version") == 0:
    c_type = c_float
elif os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

class data:
    def __init__(self):
        self.input_count = 0
        self.output_count = 0

        self.stream = False
        self.shift_count = 0
        self.line_count = 0
        self.batch_count = 0
        self.input_values = []
        self.target_values = []

        self.c_stream = c_type(self.stream)
        self.c_shift_count = c_type(self.shift_count)
        self.c_line_count = c_type(self.line_count)
        self.c_batch_count = c_type(self.batch_count)
        self.c_input_values = (c_type*len(self.input_values))(*self.input_values)
        self.c_target_values = (c_type*len(self.target_values))(*self.target_values)

    def load(self, input_values, target_values, stream, shift_count):
        self.stream = stream
        self.shift_count = shift_count

        self.input_values = input_values
        self.target_values = target_values

        self.c_stream = c_int(self.stream)
        self.c_shift_count = c_int(self.shift_count)

        c_input_values_seq = c_type*len(self.input_values)
        c_target_values_seq = c_type*len(self.target_values)

        self.c_input_values = c_input_values_seq(*self.input_values)
        self.c_target_values = c_target_values_seq(*self.target_values)
    
    def extract(self, data_name):
        stream = False
        shift_count = self.input_count
        data_input = []
        data_target = []

        try:
            data_file = open(os.getcwd() + "/DATA/" + data_name + ".txt", "r").read().split("\n")
            
            if data_name.startswith("STREAM"):
                stream = True
                shift_count = int(data_file[0])
                data_file = data_file[1:]
            
            for data_line in data_file:
                data_split = data_line.split(":")

                data_input += [Decimal(value) for value in data_split[0].split(",")]
                
                if not stream:
                    data_target += [Decimal(value) for value in data_split[1].split(",")]
        finally:
            self.load(data_input, data_target, stream, shift_count)
            
    def prepare(self, input_count, output_count, test_mode=True, batch_count=-1):
        self.input_count = input_count
        self.output_count = output_count
        
        if not self.stream:
            self.shift_count = self.input_count
            
            self.c_shift_count = c_int(self.shift_count)
        
        if test_mode or not self.stream:
            self.line_count = (len(self.input_values)-self.input_count)//self.shift_count + 1
        else:
            self.line_count = (len(self.input_values)-self.input_count-self.output_count)//self.shift_count + 1
        
        self.c_line_count = c_int(self.line_count)
        
        if batch_count == -1:
            self.batch_count = self.line_count
        
        self.c_batch_count = c_int(self.batch_count)