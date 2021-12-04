#include "deeplearner.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int size_of_double_A = sizeof(double);
double zero_A = 0;
double one_A = 1.0;
double two_A = 2.0;

void train(double min_diff, double learning_rate, int cycles, int line_count_train, double *input_values_train, double *target_values_train, int line_count_validate, double *input_values_validate, double *target_values_validate, int layer_count, int *activate_values, int *hidden_sizes, int hidden_count, int bias_count, int weight_count, double *weights_values) {
  int input_count = hidden_sizes[0];
  int output_count = hidden_sizes[layer_count+1];
  
  double* hidden_values_layers_train = (double*) malloc((line_count_train * input_count + hidden_count + output_count) * size_of_double_A);
  double* hidden_values_layers_validate = (double*) malloc((line_count_validate * input_count + hidden_count + output_count) * size_of_double_A);

  double* learning_rate_values = (double*) malloc(line_count_train * size_of_double_A);

  double* diff_values = (double*) malloc(line_count_train * size_of_double_A);
  double* prev_diff_values = (double*) malloc(line_count_train * size_of_double_A);

  double avg_learning_rate;
  double diff_train, avg_diff_train, prev_avg_diff_train;
  double diff_validate, avg_diff_validate, prev_avg_diff_validate;
  double change_coefficient, cycles_remaining_current;
  
  double cycles_remaining_sum1 = zero_A;
  double cycles_remaining_average1 = zero_A;
  double cycles_remaining_sum2 = zero_A;
  double cycles_remaining_average2 = zero_A;

  int average_size1 = 50;
  int average_size2 = 10;

  double* prev_cycles_remaining1 = (double*) malloc(average_size1 * size_of_double_A);
  double* prev_cycles_remaining2 = (double*) malloc(average_size2 * size_of_double_A);

  int minimum_reached = zero_A;

  int cycle = zero_A;

  memcpy(hidden_values_layers_train, input_values_train, line_count_train*input_count*size_of_double_A);
  memcpy(hidden_values_layers_validate, input_values_validate, line_count_validate*input_count*size_of_double_A);

  for(int i = zero_A; i < line_count_train; i++) learning_rate_values[i] = learning_rate;

  avg_diff_train = min_diff;

  while (avg_diff_train >= min_diff && (minimum_reached == zero_A && (cycles == -1 || cycle < cycles))) {
    avg_learning_rate = zero_A;
    avg_diff_train = zero_A;
    avg_diff_validate = zero_A;

    for (int line_num_train = zero_A; line_num_train < line_count_train; line_num_train++) {
      forward(line_count_train, line_num_train, activate_values, hidden_sizes, layer_count, bias_count, input_count, output_count, hidden_values_layers_train, weights_values);
      backward(line_count_train, line_num_train, activate_values, hidden_sizes, hidden_count, bias_count, weight_count, learning_rate_values[line_num_train], layer_count, input_count, output_count, hidden_values_layers_train, target_values_train, weights_values);
      
      diff_train = varyfind(line_count_train, line_num_train, input_count, hidden_count, output_count, target_values_train, hidden_values_layers_train);
      avg_diff_train += diff_train;

      change_coefficient = fabs(((diff_values[line_num_train]-prev_diff_values[line_num_train])/prev_diff_values[line_num_train])/((diff_train-diff_values[line_num_train])/diff_values[line_num_train]));

      if(cycle > one_A && diff_train < diff_values[line_num_train] && diff_values[line_num_train] <= prev_diff_values[line_num_train] && change_coefficient < two_A){
        learning_rate_values[line_num_train] *= change_coefficient;
      }
      else{
        learning_rate_values[line_num_train] = learning_rate;
      }

      avg_learning_rate += learning_rate_values[line_num_train];

      prev_diff_values[line_num_train] = diff_values[line_num_train];
      diff_values[line_num_train] = diff_train;
    }

    for(int line_num_validate = zero_A; line_num_validate < line_count_validate; line_num_validate++){
      forward(line_count_validate, line_num_validate, activate_values, hidden_sizes, layer_count, bias_count, input_count, output_count, hidden_values_layers_validate, weights_values);
      
      diff_validate = varyfind(line_count_validate, line_num_validate, input_count, hidden_count, output_count, target_values_validate, hidden_values_layers_validate);
      avg_diff_validate += diff_validate;
    }

    avg_learning_rate /= (double) line_count_train;
    avg_diff_train /= (double) line_count_train;
    avg_diff_validate /= (double) line_count_validate;

    if(cycle > average_size2){
      cycles_remaining_average2 = cycles_remaining_sum2/average_size2;
      cycles_remaining_sum2 -= prev_cycles_remaining2[0];
    }

    if(cycle > average_size1){
      cycles_remaining_average1 = cycles_remaining_sum1/average_size1;

      if(cycles_remaining_average2 < 0.999*cycles_remaining_average1 && cycles_remaining_average2 < one_A){
        minimum_reached = one_A;
      }

      cycles_remaining_sum1 -= prev_cycles_remaining1[0];
    }

    if(cycle > zero_A){
      cycles_remaining_current = ((prev_avg_diff_train/avg_diff_train)+(prev_avg_diff_validate/avg_diff_validate))/two_A;
      cycles_remaining_sum1 += cycles_remaining_current;
      cycles_remaining_sum2 += cycles_remaining_current;

      for(int i = zero_A; i < average_size1-1; i++) prev_cycles_remaining1[i] = prev_cycles_remaining1[i+1];
      for(int i = zero_A; i < average_size2-1; i++) prev_cycles_remaining2[i] = prev_cycles_remaining2[i+1];

      prev_cycles_remaining1[average_size1-1] = cycles_remaining_current;
      prev_cycles_remaining2[average_size2-1] = cycles_remaining_current;
    }

    prev_avg_diff_train = avg_diff_train;
    prev_avg_diff_validate = avg_diff_validate;

    printf("%.16f : %.16f : %.16f : %.16f : %.16f\n", avg_diff_train, avg_diff_validate, cycles_remaining_average1, cycles_remaining_average2, avg_learning_rate);
    
    cycle++;
  }

  free(hidden_values_layers_train);
  free(hidden_values_layers_validate);

  free(learning_rate_values);

  free(diff_values);
  free(prev_diff_values);

  free(prev_cycles_remaining1);
  free(prev_cycles_remaining2);
}

void test(int line_count, double *input_values, int layer_count, int *activate_values, int *hidden_sizes, int hidden_count, int bias_count, int weight_count, double *weights_values, double *output_values){
  int input_count = hidden_sizes[0];
  int output_count = hidden_sizes[layer_count+1];

  double* hidden_values_layers = (double*) malloc((line_count * input_count + hidden_count + output_count) * size_of_double_A);
  int hidden_neuron_dist = line_count * input_count + hidden_count;

  for(int i = zero_A; i < line_count * input_count; i++) hidden_values_layers[i] = input_values[i];

  for (int line_num = zero_A; line_num < line_count; line_num++) {
    forward(line_count, line_num, activate_values, hidden_sizes, layer_count, bias_count, input_count, output_count, hidden_values_layers, weights_values);

    for (int i = zero_A; i < output_count; i++){
      output_values[line_num * output_count + i] = hidden_values_layers[hidden_neuron_dist + i];
    }
  }

  free(hidden_values_layers);
}