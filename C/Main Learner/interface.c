#include "deeplearner.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int size_of_double_A = sizeof(double);
double zero_A = 0;
double one_A = 1.0;

void train(double min_diff, double learning_rate, int cycles, int line_count_train, double *input_values_train, double *target_values_train, int line_count_test, double *input_values_test, double *target_values_test, int layer_count, int *activation_values, int *hidden_sizes, int total_hidden_count, int bias_count, int weights_count, int input_count, int output_count, double *weights_values) {
  double* hidden_values_layers_train = (double*) malloc((line_count_train * input_count + total_hidden_count + output_count) * size_of_double_A);
  double* hidden_values_layers_test = (double*) malloc((line_count_test * input_count + total_hidden_count + output_count) * size_of_double_A);

  double* learning_rate_values = (double*) malloc(line_count_train * size_of_double_A);

  double* diff_values = (double*) malloc(line_count_train * size_of_double_A);
  double* prev_diff_values = (double*) malloc(line_count_train * size_of_double_A);

  double diff_train, avg_diff_train, prev_avg_diff_train;
  double diff_test, avg_diff_test, prev_avg_diff_test;
  double change_coefficient, cycles_remaining_current;
  
  double cycles_remaining_sum = zero_A;
  double cycles_remaining_average = zero_A;
  double total_cycles_sum = zero_A;

  int cycle = zero_A;
  
  int average_size = 10;

  double* prev_cycles_remaining = (double*) malloc(average_size * size_of_double_A);

  int minimum_reached = zero_A;

  memcpy(hidden_values_layers_train, input_values_train, line_count_train*input_count*size_of_double_A);
  memcpy(hidden_values_layers_test, input_values_test, line_count_test*input_count*size_of_double_A);

  for(int i = zero_A; i < line_count_train; i++) learning_rate_values[i] = learning_rate;

  avg_diff_train = min_diff;

  while (avg_diff_train >= min_diff && (minimum_reached == zero_A || (cycles == -1 || cycle < cycles))) {
    avg_diff_train = zero_A;
    avg_diff_test = zero_A;

    for (int line_num_train = zero_A; line_num_train < line_count_train; line_num_train++) {
      forward(line_count_train, line_num_train, activation_values, hidden_sizes, layer_count, bias_count, input_count, output_count, hidden_values_layers_train, weights_values);
      backward(line_count_train, line_num_train, activation_values, hidden_sizes, total_hidden_count, bias_count, weights_count, learning_rate_values[line_num_train], layer_count, input_count, output_count, hidden_values_layers_train, target_values_train, weights_values);
      
      diff_train = varyfind(line_count_train, line_num_train, input_count, total_hidden_count, output_count, target_values_train, hidden_values_layers_train);
      avg_diff_train += diff_train;

      change_coefficient = fabs((diff_values[line_num_train]-prev_diff_values[line_num_train])/(diff_train-diff_values[line_num_train]));

      if(cycle > one_A && diff_train != diff_values[line_num_train] && diff_values[line_num_train] != prev_diff_values[line_num_train] && change_coefficient < 2.0){
        learning_rate_values[line_num_train] *= change_coefficient;
      }
      else{
        learning_rate_values[line_num_train] = learning_rate;
      }

      prev_diff_values[line_num_train] = diff_values[line_num_train];
      diff_values[line_num_train] = diff_train;
    }

    for(int line_num_test = zero_A; line_num_test < line_count_test; line_num_test++){
      forward(line_count_test, line_num_test, activation_values, hidden_sizes, layer_count, bias_count, input_count, output_count, hidden_values_layers_test, weights_values);
      diff_test = varyfind(line_count_test, line_num_test, input_count, total_hidden_count, output_count, target_values_test, hidden_values_layers_test);

      avg_diff_test += diff_test;
    }

    avg_diff_train /= (double) line_count_train;
    avg_diff_test /= (double) line_count_test;

    if(cycle > average_size){
      cycles_remaining_average = cycles_remaining_sum/average_size;

      if(cycles_remaining_average < total_cycles_sum/cycle){
        minimum_reached = one_A;
      }

      cycles_remaining_sum -= prev_cycles_remaining[0];
    }

    if(cycle > zero_A){
      cycles_remaining_current = (prev_avg_diff_train+prev_avg_diff_test)/(avg_diff_train+avg_diff_test);
      cycles_remaining_sum += cycles_remaining_current;
      total_cycles_sum += cycles_remaining_current;

      for(int i = zero_A; i < average_size-1; i++) prev_cycles_remaining[i] = prev_cycles_remaining[i+1];

      prev_cycles_remaining[average_size-1] = cycles_remaining_current;
    }

    prev_avg_diff_train = avg_diff_train;
    prev_avg_diff_test = avg_diff_test;

    printf("%.16f : %.16f : %.16f\n", avg_diff_train, avg_diff_test, cycles_remaining_average);
    
    cycle++;
  }

  free(hidden_values_layers_train);
  free(hidden_values_layers_test);

  free(learning_rate_values);

  free(diff_values);
  free(prev_diff_values);
}

void test(int line_count, double *input_values, double *output_values, int layer_count, int *activate_values, int *hidden_sizes, int total_hidden_count, int bias_count, int weights_count, int input_count, int output_count, double *weights_values){
  double* hidden_values_layers = (double*) malloc((line_count * input_count + total_hidden_count + output_count) * size_of_double_A);
  int hidden_neuron_dist = line_count * input_count + total_hidden_count;

  for(int i = zero_A; i < line_count * input_count; i++) hidden_values_layers[i] = input_values[i];

  for (int line_num = zero_A; line_num < line_count; line_num++) {
    forward(line_count, line_num, activate_values, hidden_sizes, layer_count, bias_count, input_count, output_count, hidden_values_layers, weights_values);

    for (int i = zero_A; i < output_count; i++){
      output_values[line_num * output_count + i] = hidden_values_layers[hidden_neuron_dist + i];
    }
  }

  free(hidden_values_layers);
}