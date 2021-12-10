#include "interfaceC.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double e = 2.71828182845904523536028747135266;
double zero_C = 0;
double half_C = 0.5;
double one_C = 1.0;
double two_C = 2.0;
double four_C = 4.0;

double swish(double x) {
	return x / (one_C + pow(e, -x));
}

double dswish(double x) {
	double z = pow(e, x);

	return (z * (z + x + one_C)) / pow((z + one_C), two_C);
}

double relu(double x) {
	if (x > zero_C) {
		return x;
	}
	else {
		return zero_C;
	}
}

double drelu(double x) {
	if (x >= zero_C) {
		return one_C;
	}
	else {
		return zero_C;
	}
}

double lerelu(double x) {
	if (x >= zero_C) {
		return x;
	}
	else {
		return half_C * x;
	}
}

double dlerelu(double x) {
	if (x >= zero_C) {
		return one_C;
	}
	else {
		return half_C;
	}
}

double hyptan(double x) {
	double z1, z2, y;
	z1 = pow(e, x);
	z2 = pow(e, -x);

	y = (z1 - z2) / (z1 + z2);

	return y;
}

double dhyptan(double x) {
	double z = pow(e, x);

	double y = (z * four_C) / pow((z + one_C), two_C);

	return y;
}

double sigmoid(double x) {
	return one_C / (one_C + pow(e, -x));
}

double dsigmoid(double x) {
	double z = pow(e, x);

	return z / pow((z + one_C), two_C);
}

double softsign(double x){
	return x / (one_C + fabs(x));
}

double dsoftsign(double x){
	return one_C / pow((one_C + fabs(x)), two_C);
}

double elu(double x) {
	if(x < zero_C){
		return 0.1*(pow(e, x)-one_C);
	}
	else{
		return x;
	}
}

double delu(double x) {
	if (x >= zero_C){
		return one_C;
	}
	else{
		return 0.1*pow(e, x);
	}
}

void softmax(int distance, int count, double *values){
	double z, s;
	s = 0;

	for(int i = 0; i < count; i++){
		z = pow(e, values[distance + i]);
		values[distance + i] = z;
		s += z;
	}

	for(int i = 0; i < count; i++) values[distance + i] /= s;
}

int size_of_double_B = sizeof(double);
double zero_B = 0;

double activate(int activation_value, double x) {
	switch (activation_value) {
		case 0:
			return swish(x);
		case 1:
			return dswish(x);
		case 2:
			return relu(x);
		case 3:
			return drelu(x);
		case 4:
			return lerelu(x);
		case 5:
			return dlerelu(x);
		case 6:
			return hyptan(x);
		case 7:
			return dhyptan(x);
		case 8:
			return sigmoid(x);
		case 9:
			return dsigmoid(x);
		case 10:
			return softsign(x);
		case 11:
			return dsoftsign(x);
		case 12:
			return elu(x);
		case 13:
			return delu(x);
		default:
			return x;
	}
}

void vector_activate(int activation_value, int distance, int count, double *values) {
	switch (activation_value) {
		case 100:
			softmax(distance, count, values);
	}
}

double varyfind(int line_count, int line_num, int input_count, int hidden_count, int output_count, double *target_values, double *values) {
	double sum = zero_B;
	int hidden_neuron_distance = line_count * input_count + hidden_count;

	for (int i = zero_B; i < output_count; i++) {
		if(target_values[line_num * output_count + i] != 0) {
			sum += fabs((target_values[line_num * output_count + i] - values[hidden_neuron_distance + i])/target_values[line_num * output_count + i]);
		}
		else{
			sum += fabs(target_values[line_num * output_count + i] - values[hidden_neuron_distance + i]);
		}
	}

	return sum / ((double)output_count);
}

void forward(int line_count, int line_num, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int input_count, int output_count, double *values, double *weight_values) {
	int current_count, prev_count, hidden_neuron_distance, hidden_weight_distance, prev_neuron_distance;

	prev_neuron_distance = line_num * input_count;
	hidden_neuron_distance = line_count * input_count;
	hidden_weight_distance = zero_B;

	for (int layer_num = zero_B; layer_num < layer_count+1; layer_num++) {
		current_count = hidden_sizes[layer_num+1];
		prev_count = hidden_sizes[layer_num];

		for (int h = zero_B; h < current_count; h++) values[hidden_neuron_distance + h] = zero_B;

		for (int i = zero_B; i < current_count; i++) {
			for (int j = zero_B; j < prev_count; j++) {
				values[hidden_neuron_distance + i] += values[prev_neuron_distance + j] * weight_values[hidden_weight_distance];
				hidden_weight_distance++;
			}

			for (int j = zero_B; j < bias_count; j++) {
				values[hidden_neuron_distance + i] += weight_values[hidden_weight_distance];
				hidden_weight_distance++;
			}

			if(activation_values[layer_num] < 100) values[hidden_neuron_distance + i] = activate(activation_values[layer_num], values[hidden_neuron_distance + i]);
		}

		if(activation_values[layer_num] >= 100) vector_activate(activation_values[layer_num], hidden_neuron_distance, current_count, values);

		prev_neuron_distance = hidden_neuron_distance;
		hidden_neuron_distance += current_count;
	}
}

void backward(int line_count, int line_num, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int input_count, int hidden_count, int output_count, int weight_count, double *values, double *target_values, double *weight_values, double learning_rate) {
	int current_count, next_count, hidden_neuron_distance, hidden_weight_distance, input_neuron_distance;
	double* derivative_sum = (double*)malloc(output_count * size_of_double_B);
	double* future_sum = (double*)malloc(size_of_double_B);
	double part_delta;

	hidden_neuron_distance = line_count * input_count + hidden_count;
	hidden_weight_distance = weight_count;
	input_neuron_distance = zero_B;

	for (int h = zero_B; h < output_count; h++) derivative_sum[h] = (values[hidden_neuron_distance + h] - target_values[line_num * output_count + h]);

	for (int layer_num = layer_count+1; layer_num > zero_B; layer_num--) {
		current_count = hidden_sizes[layer_num];
		next_count = hidden_sizes[layer_num-1];

		if(layer_num == 1) input_neuron_distance = (line_count - line_num - 1) * next_count;

		hidden_weight_distance -= current_count * (next_count + bias_count);

		future_sum = (double*)realloc(future_sum, next_count * size_of_double_B);
		for (int h = zero_B; h < next_count; h++) future_sum[h] = zero_B;

		for (int i = zero_B; i < current_count; i++) {
			part_delta = derivative_sum[i];
			
			if(activation_values[layer_num-1] < 100) part_delta *= activate(activation_values[layer_num-1]+1, values[hidden_neuron_distance + i]);

			for (int j = zero_B; j < next_count; j++) {
				future_sum[j] += part_delta * weight_values[hidden_weight_distance + i * next_count + j];
				weight_values[hidden_weight_distance + i * next_count + j] -= part_delta * values[hidden_neuron_distance - next_count - input_neuron_distance + j] * learning_rate;
			}

			for (int j = zero_B; j < bias_count; j++) {
				weight_values[hidden_weight_distance + (i + 1) * next_count + j] -= part_delta * learning_rate;
			}
		}

		hidden_neuron_distance -= next_count;

		derivative_sum = (double*)realloc(derivative_sum, next_count * size_of_double_B);
		for (int k = zero_B; k < next_count; k++) derivative_sum[k] = future_sum[k];
	}

	free(derivative_sum);
	free(future_sum);
}

int size_of_double_A = sizeof(double);
double zero_A = 0;
double one_A = 1.0;
double two_A = 2.0;

void train(double min_diff, double learning_rate, int cycles, int line_count_train, double *input_values_train, double *target_values_train, int line_count_validate, double *input_values_validate, double *target_values_validate, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int hidden_count, int weight_count, double *weight_values) {
  int input_count = hidden_sizes[0];
  int output_count = hidden_sizes[layer_count+1];
  
  double* values_train = (double*) malloc((line_count_train * input_count + hidden_count + output_count) * size_of_double_A);
  double* values_validate = (double*) malloc((line_count_validate * input_count + hidden_count + output_count) * size_of_double_A);

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
  int average_size2 = 5;

  double* prev_cycles_remaining1 = (double*) malloc(average_size1 * size_of_double_A);
  double* prev_cycles_remaining2 = (double*) malloc(average_size2 * size_of_double_A);

  int minimum_reached = zero_A;

  int cycle = zero_A;

  memcpy(values_train, input_values_train, line_count_train*input_count*size_of_double_A);
  memcpy(values_validate, input_values_validate, line_count_validate*input_count*size_of_double_A);

  for(int i = zero_A; i < line_count_train; i++) learning_rate_values[i] = learning_rate;

  avg_diff_train = min_diff;

  while (avg_diff_train >= min_diff && (minimum_reached == zero_A && (cycles == -1 || cycle < cycles))) {
    avg_learning_rate = zero_A;
    avg_diff_train = zero_A;
    avg_diff_validate = zero_A;

    for (int line_num_train = zero_A; line_num_train < line_count_train; line_num_train++) {
      forward(line_count_train, line_num_train, activation_values, hidden_sizes, layer_count, bias_count, input_count, output_count, values_train, weight_values);
      backward(line_count_train, line_num_train, activation_values, hidden_sizes, layer_count, bias_count, input_count, hidden_count, output_count, weight_count, values_train, target_values_train, weight_values, learning_rate_values[line_num_train]);
      
      diff_train = varyfind(line_count_train, line_num_train, input_count, hidden_count, output_count, target_values_train, values_train);
      avg_diff_train += diff_train;

      change_coefficient = fabs(((diff_values[line_num_train]-prev_diff_values[line_num_train])/prev_diff_values[line_num_train])/((diff_train-diff_values[line_num_train])/diff_values[line_num_train]));

      if(diff_train > diff_values[line_num_train]){
        change_coefficient = 0.1;
      }

      if(change_coefficient > 1.2){
        change_coefficient = 1.2;
      }

      if(cycle > one_A && diff_train != diff_values[line_num_train] && diff_values[line_num_train] != prev_diff_values[line_num_train]){
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
      forward(line_count_validate, line_num_validate, activation_values, hidden_sizes, layer_count, bias_count, input_count, output_count, values_train, weight_values);
      
      diff_validate = varyfind(line_count_validate, line_num_validate, input_count, hidden_count, output_count, target_values_validate, values_validate);
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

  free(values_train);
  free(values_validate);

  free(learning_rate_values);

  free(diff_values);
  free(prev_diff_values);

  free(prev_cycles_remaining1);
  free(prev_cycles_remaining2);
}

void test(int line_count, double *input_values, double *output_values, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int hidden_count, int weight_count, double *weight_values){
  int input_count = hidden_sizes[0];
  int output_count = hidden_sizes[layer_count+1];

  double* values = (double*) malloc((line_count * input_count + hidden_count + output_count) * size_of_double_A);
  int hidden_neuron_dist = line_count * input_count + hidden_count;

  for(int i = zero_A; i < line_count * input_count; i++) values[i] = input_values[i];

  for (int line_num = zero_A; line_num < line_count; line_num++) {
    forward(line_count, line_num, activation_values, hidden_sizes, layer_count, bias_count, input_count, output_count, values, weight_values);

    for (int i = zero_A; i < output_count; i++){
      output_values[line_num * output_count + i] = values[hidden_neuron_dist + i];
    }
  }

  free(values);
}