//Copyright (c) 2023 by Liam Roan Watson and Watcode. All rights reserved. For licensing, contact lrwatson@uwaterloo.ca or +1 437 688 3927

#include "interface.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

struct ThreadArguments {
    int shift_count;
    int line_count;
    int line_num;
    int layer_count;
    int bias_count;
    int input_count;
    int hidden_count;
    int output_count;
    int weight_count;
    int max_count;
    int target_offset;
	int target_shift_count;
    int *activation_values;
    int *hidden_sizes;
    double learning_rate;
    double *values;
    double *target_values;
    double *weight_values;
    double *delta_weight_values;
    double *derivative_sum;
    double *future_sum;
};

int size_of_double = sizeof(double);

int thread_count = 8;

pthread_t *thread_id_values;

double e = 2.71828182845904523536028747135266;
double zero = 0;
double half = 0.5;
double one = 1.0;
double two = 2.0;
double four = 4.0;

double swish(double x) {
	return x / (one + pow(e, -x));
}

double dswish(double x) {
	double z = pow(e, x);

	return (z * (z + x + one)) / pow((z + one), two);
}

double relu(double x) {
	if (x > zero) {
		return x;
	}
	else {
		return zero;
	}
}

double drelu(double x) {
	if (x >= zero) {
		return one;
	}
	else {
		return zero;
	}
}

double lerelu(double x) {
	if (x >= zero) {
		return x;
	}
	else {
		return half * x;
	}
}

double dlerelu(double x) {
	if (x >= zero) {
		return one;
	}
	else {
		return half;
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

	double y = (z * four) / pow((z + one), two);

	return y;
}

double sigmoid(double x) {
	return one / (one + pow(e, -x));
}

double dsigmoid(double x) {
	double z = pow(e, x);

	return z / pow((z + one), two);
}

double softsign(double x){
	return x / (one + fabs(x));
}

double dsoftsign(double x){
	return one / pow((one + fabs(x)), two);
}

double elu(double x) {
	if(x < zero){
		return 0.1*(pow(e, x)-one);
	}
	else{
		return x;
	}
}

double delu(double x) {
	if (x >= zero){
		return one;
	}
	else{
		return 0.1*pow(e, x);
	}
}

void softmax(int distance, int count, double *values){
	double z, s;
	s = 0;

	for(int i = 0; i < count; i++){
		z = fabs(values[distance + i]);
		values[distance + i] = z;
		s += z;
	}

	for(int i = 0; i < count; i++) values[distance + i] = fabs(values[distance + i]/s);
}

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

void vectoractivate(int activation_value, int distance, int count, double *values) {
	switch (activation_value) {
		case 100:
			softmax(distance, count, values);
	}
}

double varyfind(int target_offset, int shift_count, int line_count, int line_num, int input_count, int hidden_count, int output_count, double *target_values, double *values) {
	double sum = zero;
	int thread_num = line_num%thread_count;
	int hidden_neuron_distance = input_count + (line_count - 1) * shift_count + (hidden_count + output_count) * thread_num + hidden_count;

	for (int i = zero; i < output_count; i++) {
		if(target_values[target_offset + i] != 0) {
			sum += fabs((target_values[target_offset + i] - values[hidden_neuron_distance + i])/target_values[target_offset + i]);
		}
		else{
			sum += fabs(target_values[target_offset + i] - values[hidden_neuron_distance + i]);
		}
	}

	return sum / ((double) output_count);
}

void *forward(void *thread_arguments_void) {
	struct ThreadArguments *thread_arguments = (struct ThreadArguments*) thread_arguments_void;

	int shift_count, line_count, line_num, *activation_values, *hidden_sizes, layer_count, bias_count, input_count, hidden_count, output_count;
	double *values, *weight_values;

	shift_count = thread_arguments->shift_count;
	line_count = thread_arguments->line_count;
	for (int i = 0; i < thread_count; i++) if (thread_id_values[i] == pthread_self()) { 
		line_num = thread_arguments->line_num + i;
		break; 
	}
	activation_values = thread_arguments->activation_values;
	hidden_sizes = thread_arguments->hidden_sizes;
	layer_count = thread_arguments->layer_count;
	bias_count = thread_arguments->bias_count;
	input_count = thread_arguments->input_count;
	hidden_count = thread_arguments->hidden_count;
	output_count = thread_arguments->output_count;
	values = thread_arguments->values;
	weight_values = thread_arguments->weight_values;

	int current_count, prev_count, hidden_neuron_distance, hidden_weight_distance, prev_neuron_distance, thread_num;

	thread_num = line_num%thread_count;

	prev_neuron_distance = line_num * shift_count;
	hidden_neuron_distance = input_count + (line_count - 1) * shift_count + (hidden_count + output_count) * thread_num;
	hidden_weight_distance = zero;

	for (int layer_num = zero; layer_num < layer_count+1; layer_num++) {
		current_count = hidden_sizes[layer_num+1];
		prev_count = hidden_sizes[layer_num];

		for (int i = zero; i < current_count; i++) {
			values[hidden_neuron_distance + i] = zero;

			for (int j = zero; j < prev_count; j++) {
				values[hidden_neuron_distance + i] += values[prev_neuron_distance + j] * weight_values[hidden_weight_distance];
				hidden_weight_distance++;
			}

			for (int j = zero; j < bias_count; j++) {
				values[hidden_neuron_distance + i] += weight_values[hidden_weight_distance];
				hidden_weight_distance++;
			}

			if(activation_values[layer_num] < 100) values[hidden_neuron_distance + i] = activate(activation_values[layer_num], values[hidden_neuron_distance + i]);
		}

		if(activation_values[layer_num] >= 100) vectoractivate(activation_values[layer_num], hidden_neuron_distance, current_count, values);

		prev_neuron_distance = hidden_neuron_distance;
		hidden_neuron_distance += current_count;
	}

	pthread_exit(NULL);
}

void *backward(void *thread_arguments_void) {
	struct ThreadArguments *thread_arguments = (struct ThreadArguments*) thread_arguments_void;

	int shift_count, line_count, line_num, layer_count, bias_count, input_count, hidden_count, output_count, weight_count, max_count, target_offset, target_shift_count, *activation_values, *hidden_sizes;
	double learning_rate, *derivative_sum, *future_sum, *values, *target_values, *weight_values, *delta_weight_values;
	
	shift_count = thread_arguments->shift_count;
	line_count = thread_arguments->line_count;
	for (int i = 0; i < thread_count; i++) if (thread_id_values[i] == pthread_self()) { 
		line_num = thread_arguments->line_num + i;
		break; 
	}
	activation_values = thread_arguments->activation_values;
	hidden_sizes = thread_arguments->hidden_sizes;
	layer_count = thread_arguments->layer_count;
	bias_count = thread_arguments->bias_count;
	input_count = thread_arguments->input_count;
	hidden_count = thread_arguments->hidden_count;
	output_count = thread_arguments->output_count;
	weight_count = thread_arguments->weight_count;
	max_count = thread_arguments->max_count;
	target_offset = thread_arguments->target_offset;
	target_shift_count = thread_arguments->target_shift_count;
	values = thread_arguments->values;
	target_values = thread_arguments->target_values;
	weight_values = thread_arguments->weight_values;
	delta_weight_values = thread_arguments->delta_weight_values;
	learning_rate = thread_arguments->learning_rate;
	derivative_sum = thread_arguments->derivative_sum;
	future_sum = thread_arguments->future_sum;

	int current_count, next_count, hidden_neuron_distance, hidden_weight_distance, input_neuron_distance, thread_num;
	double part_delta;

	thread_num = line_num%thread_count;

	hidden_neuron_distance = input_count + (line_count - 1) * shift_count + (hidden_count + output_count) * thread_num + hidden_count;
	hidden_weight_distance = weight_count;
	input_neuron_distance = zero;

	for (int h = zero; h < output_count; h++) derivative_sum[thread_num*max_count + h] = (values[hidden_neuron_distance + h] - target_values[target_offset + thread_num*target_shift_count + h]);

	for (int layer_num = layer_count+1; layer_num > zero; layer_num--) {
		current_count = hidden_sizes[layer_num];
		next_count = hidden_sizes[layer_num-1];

		if(layer_num == 1) input_neuron_distance = (line_count - line_num - 1) * shift_count + (hidden_count + output_count) * thread_num;

		hidden_weight_distance -= current_count * (next_count + bias_count);

		if (layer_num > one) for (int h = zero; h < next_count; h++) future_sum[thread_num*max_count + h] = zero;

		for (int i = zero; i < current_count; i++) {
			part_delta = derivative_sum[thread_num*max_count + i];
			
			if(activation_values[layer_num-1] < 100) part_delta *= activate(activation_values[layer_num-1]+1, values[hidden_neuron_distance + i]);

			for (int j = zero; j < next_count; j++) {
				if (layer_num > one) future_sum[thread_num*max_count + j] += part_delta * weight_values[hidden_weight_distance + i * next_count + j];
				delta_weight_values[weight_count * thread_num + hidden_weight_distance + i * next_count + j] -= part_delta * values[hidden_neuron_distance - next_count - input_neuron_distance + j] * learning_rate;
			}

			for (int j = zero; j < bias_count; j++) {
				delta_weight_values[weight_count * thread_num + hidden_weight_distance + (i + 1) * next_count + j] -= part_delta * learning_rate;
			}
		}

		hidden_neuron_distance -= next_count;

		if (layer_num > one) for (int k = zero; k < next_count; k++) derivative_sum[thread_num*max_count + k] = future_sum[thread_num*max_count + k];
	}

	pthread_exit(NULL);
}

void train(double min_diff, double learning_rate, int cycles, int ignore_minimum, int batch_count, int stream_train, int shift_count_train, int line_count_train, double *input_values_train, double *target_values_train, int stream_validate, int shift_count_validate, int line_count_validate, double *input_values_validate, double *target_values_validate, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int hidden_count, int weight_count, double *weight_values) {
  int input_count = hidden_sizes[0];
  int output_count = hidden_sizes[layer_count+1];
  
  double* delta_weight_values = (double*) malloc(thread_count * weight_count * size_of_double);

  for (int i = zero; i < weight_count; i++) delta_weight_values[i] = zero;

  int max_count = zero;

  for (int i = zero; i < layer_count; i++) if (hidden_sizes[i+1] > max_count) max_count = hidden_sizes[i+1];

  double* derivative_sum = (double*) malloc(thread_count * max_count * size_of_double);
  double* future_sum = (double*) malloc(thread_count * max_count * size_of_double);

  int target_offset_train;
  int target_offset_validate;
  
  double* values_train = (double*) malloc((input_count + ((line_count_train - 1) * shift_count_train) + thread_count * (hidden_count + output_count)) * size_of_double);
  double* values_validate = (double*) malloc((input_count + ((line_count_validate - 1) * shift_count_validate) + thread_count * (hidden_count + output_count)) * size_of_double);

  memcpy(values_train, input_values_train, (input_count + ((line_count_train - 1) * shift_count_train))*size_of_double);
  memcpy(values_validate, input_values_validate, (input_count + ((line_count_validate - 1) * shift_count_validate))*size_of_double);

  double** pointer_target_values_train;
  double** pointer_target_values_validate;

  if (stream_train == 1) pointer_target_values_train = &input_values_train;
  else pointer_target_values_train = &target_values_train;

  if (stream_validate == 1) pointer_target_values_validate = &input_values_validate;
  else pointer_target_values_validate = &target_values_validate;

  double* learning_rate_values_train = (double*) malloc(line_count_train * size_of_double);
  double* learning_rate_values_validate = (double*) malloc(line_count_validate * size_of_double);

  double* diff_values_train = (double*) malloc(line_count_train * size_of_double);
  double* prev_diff_values_train = (double*) malloc(line_count_train * size_of_double);

  double* diff_values_validate = (double*) malloc(line_count_validate * size_of_double);
  double* prev_diff_values_validate = (double*) malloc(line_count_validate * size_of_double);

  double initial_learning_rate = learning_rate;

  double avg_learning_rate;
  double diff_train, avg_diff_train, prev_avg_diff_train;
  double diff_validate, avg_diff_validate, prev_avg_diff_validate;
  double change_coefficient, cycles_remaining_current;
  
  double cycles_remaining_sum1 = zero;
  double cycles_remaining_average1 = zero;
  double cycles_remaining_sum2 = zero;
  double cycles_remaining_average2 = zero;

  int average_size1 = 10;
  int average_size2 = 2;

  double* prev_cycles_remaining1 = (double*) malloc(average_size1 * size_of_double);
  double* prev_cycles_remaining2 = (double*) malloc(average_size2 * size_of_double);

  int minimum_reached = zero;

  int cycle = zero;

  int batch_num = zero;

  for (int i = zero; i < line_count_train; i++) learning_rate_values_train[i] = learning_rate;
  for (int i = zero; i < line_count_validate; i++) learning_rate_values_validate[i] = learning_rate;

  avg_diff_train = min_diff;

  struct ThreadArguments *thread_arguments = (struct ThreadArguments*) malloc(sizeof(struct ThreadArguments));

  thread_arguments->activation_values = activation_values;
  thread_arguments->hidden_sizes = hidden_sizes;
  thread_arguments->layer_count = layer_count;
  thread_arguments->bias_count = bias_count;
  thread_arguments->input_count = input_count;
  thread_arguments->hidden_count = hidden_count;
  thread_arguments->output_count = output_count;
  thread_arguments->weight_count = weight_count;
  thread_arguments->max_count = max_count;
  thread_arguments->weight_values = weight_values;
  thread_arguments->delta_weight_values = delta_weight_values;
  thread_arguments->derivative_sum = derivative_sum;
  thread_arguments->future_sum = future_sum;

  int line_num_train, line_num_validate;

  int thread_count_current;

  thread_id_values = malloc(thread_count * sizeof(pthread_t));

  int target_shift_count_train, target_shift_count_validate;

  if (stream_train == 1) target_shift_count_train = shift_count_train;
  else target_shift_count_train = output_count;

  if (stream_validate == 1) target_shift_count_validate = shift_count_validate;
  else target_shift_count_validate = output_count;

  while (avg_diff_train >= min_diff && (minimum_reached == zero || ignore_minimum == one) && (cycles == -1 || cycle < cycles)) {
    avg_learning_rate = zero;
    avg_diff_train = zero;
    avg_diff_validate = zero;

	if (stream_train == 1) target_offset_train = input_count;
	else target_offset_train = zero;

	if (stream_validate == 1) target_offset_validate = input_count;
	else target_offset_validate = zero;

	thread_arguments->shift_count = shift_count_train;
    thread_arguments->line_count = line_count_train;
	thread_arguments->values = values_train;
	thread_arguments->target_values = *pointer_target_values_train;
	thread_arguments->target_shift_count = target_shift_count_train;
	thread_arguments->learning_rate = learning_rate;

    for (int h = zero; h < line_count_train/thread_count+1; h++) {
	  for (thread_count_current = zero; thread_count_current < thread_count; thread_count_current++) if ((h * thread_count + thread_count_current) >= line_count_train) break;
	  
	  thread_arguments->target_offset = target_offset_train;
	  thread_arguments->line_num = h * thread_count;

	  for (int i = zero; i < thread_count_current; i++) pthread_create(&thread_id_values[i], NULL, forward, (void *) thread_arguments);

	  for (int i = zero; i < thread_count_current; i++) {
		pthread_join(thread_id_values[i], NULL);
		pthread_create(&thread_id_values[i], NULL, backward, (void *) thread_arguments);
	  }

	  for (int i = zero; i < thread_count_current; i++) pthread_join(thread_id_values[i], NULL);

	  for (int i = zero; i < thread_count_current; i++) {
		line_num_train = h * thread_count + i;

		diff_train = varyfind(target_offset_train, shift_count_train, line_count_train, line_num_train, input_count, hidden_count, output_count, *pointer_target_values_train, values_train);

		avg_diff_train += diff_train;

		change_coefficient = fabs(((diff_values_train[line_num_train]-prev_diff_values_train[line_num_train])/prev_diff_values_train[line_num_train])/((diff_train-diff_values_train[line_num_train])/diff_values_train[line_num_train]));

		if(change_coefficient > 1.01){
			change_coefficient = 1.01;
		}
		if(change_coefficient < 0.9){
			change_coefficient = 0.9;
		}
		
		if(cycle > one && diff_train != diff_values_train[line_num_train] && diff_values_train[line_num_train] != prev_diff_values_train[line_num_train]){
			learning_rate_values_train[line_num_train] *= change_coefficient;
		}
		else{
			learning_rate_values_train[line_num_train] = initial_learning_rate;
		}

		avg_learning_rate += learning_rate_values_train[line_num_train];

		prev_diff_values_train[line_num_train] = diff_values_train[line_num_train];
		diff_values_train[line_num_train] = diff_train;

		target_offset_train += target_shift_count_train;

		batch_num++;

		if (batch_num%batch_count == zero) {
			for (int i = zero; i < weight_count; i++) for (int j = zero; j < thread_count; j++) weight_values[i] += delta_weight_values[i * thread_count + j];

			memset(delta_weight_values, zero, thread_count * weight_count * size_of_double);
		}
	  }
    }

	thread_arguments->shift_count = shift_count_validate;
	thread_arguments->line_count = line_count_validate;
	thread_arguments->values = values_validate;
	thread_arguments->target_values = *pointer_target_values_validate;
	thread_arguments->target_shift_count = target_shift_count_validate;

	for (int h = zero; h < line_count_validate/thread_count+1; h++) {
	  for (thread_count_current = zero; thread_count_current < thread_count; thread_count_current++) if ((h * thread_count + thread_count_current) >= line_count_validate) break;

	  thread_arguments->target_offset = target_offset_validate;
	  thread_arguments->line_num = h * thread_count;

	  for (int i = zero; i < thread_count_current; i++) pthread_create(&thread_id_values[i], NULL, forward, (void *) thread_arguments);

	  for (int i = zero; i < thread_count_current; i++) pthread_join(thread_id_values[i], NULL);

	  for (int i = zero; i < thread_count_current; i++) {
		line_num_validate = h * thread_count + i;

		diff_validate = varyfind(target_offset_validate, shift_count_validate, line_count_validate, line_num_validate, input_count, hidden_count, output_count, *pointer_target_values_validate, values_validate);
		
		avg_diff_validate += diff_validate;

		change_coefficient = fabs(((diff_values_validate[line_num_validate]-prev_diff_values_validate[line_num_validate])/prev_diff_values_validate[line_num_validate])/((diff_validate-diff_values_validate[line_num_validate])/diff_values_validate[line_num_validate]));

		if(change_coefficient > 1.01){
			change_coefficient = 1.01;
		}
		if(change_coefficient < 0.9){
			change_coefficient = 0.9;
		}
		
		if(cycle > one && diff_validate != diff_values_validate[line_num_validate] && diff_values_validate[line_num_validate] != prev_diff_values_validate[line_num_validate]){
			learning_rate_values_validate[line_num_validate] = learning_rate*change_coefficient;
		}
		else{
			learning_rate_values_validate[line_num_validate] = initial_learning_rate;
		}

		avg_learning_rate += learning_rate_values_validate[line_num_validate];

		prev_diff_values_validate[line_num_validate] = diff_values_train[line_num_validate];
		diff_values_validate[line_num_validate] = diff_validate;

		target_offset_validate += target_shift_count_validate;
	  }
    }

    avg_learning_rate /= ((double) line_count_train + (double) line_count_validate);
    avg_diff_train /= (double) line_count_train;
    avg_diff_validate /= (double) line_count_validate;

	learning_rate = avg_learning_rate;

    if(cycle > average_size2){
      cycles_remaining_average2 = cycles_remaining_sum2/average_size2;
      cycles_remaining_sum2 -= prev_cycles_remaining2[0];
    }

    if(cycle > average_size1){
      cycles_remaining_average1 = cycles_remaining_sum1/average_size1;
	  cycles_remaining_sum1 -= prev_cycles_remaining1[0];

      if(cycles_remaining_average2 < cycles_remaining_average1 && cycles_remaining_average2 < one) minimum_reached = one;
    }

    if(cycle > zero){
      cycles_remaining_current = ((prev_avg_diff_train/avg_diff_train)+(prev_avg_diff_validate/avg_diff_validate))/two;
      cycles_remaining_sum1 += cycles_remaining_current;
      cycles_remaining_sum2 += cycles_remaining_current;

      for(int i = zero; i < average_size1-1; i++) prev_cycles_remaining1[i] = prev_cycles_remaining1[i+1];
      for(int i = zero; i < average_size2-1; i++) prev_cycles_remaining2[i] = prev_cycles_remaining2[i+1];

      prev_cycles_remaining1[average_size1-1] = cycles_remaining_current;
      prev_cycles_remaining2[average_size2-1] = cycles_remaining_current;
    }

    prev_avg_diff_train = avg_diff_train;
    prev_avg_diff_validate = avg_diff_validate;

    printf("%.16f : %.16f : %.16f : %.16f : %.16f\n", avg_diff_train, avg_diff_validate, cycles_remaining_average1, cycles_remaining_average2, avg_learning_rate);
    
    cycle++;
  }

  free(thread_arguments);

  free(delta_weight_values);

  free(derivative_sum);
  free(future_sum);

  free(values_train);
  free(values_validate);

  free(learning_rate_values_train);
  free(learning_rate_values_validate);

  free(diff_values_train);
  free(prev_diff_values_train);

  free(diff_values_validate);
  free(prev_diff_values_validate);

  free(prev_cycles_remaining1);
  free(prev_cycles_remaining2);
}

void test(int stream, int shift_count, int line_count, double *input_values, double *output_values, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int hidden_count, int weight_count, double *weight_values){
  int input_count = hidden_sizes[0];
  int output_count = hidden_sizes[layer_count+1];

  double* values = (double*) malloc((input_count + ((line_count - 1) * shift_count) + hidden_count + output_count) * size_of_double);
  int hidden_neuron_dist = input_count + ((line_count - 1) * shift_count) + hidden_count;

  memcpy(values, input_values, (input_count + ((line_count - 1) * shift_count))*size_of_double);

  struct ThreadArguments *thread_arguments = (struct ThreadArguments*) malloc(sizeof(struct ThreadArguments));

  thread_arguments->activation_values = activation_values;
  thread_arguments->hidden_sizes = hidden_sizes;
  thread_arguments->layer_count = layer_count;
  thread_arguments->bias_count = bias_count;
  thread_arguments->input_count = input_count;
  thread_arguments->hidden_count = hidden_count;
  thread_arguments->output_count = output_count;
  thread_arguments->weight_count = weight_count;
  thread_arguments->weight_values = weight_values;
  thread_arguments->shift_count = shift_count;
  thread_arguments->line_count = line_count;
  thread_arguments->values = values;

  thread_count = one;

  for (int line_num = zero; line_num < line_count; line_num++) {
	thread_arguments->line_num = line_num;

    forward((void *) thread_arguments);

    for (int i = zero; i < output_count; i++){
      output_values[line_num * output_count + i] = values[hidden_neuron_dist + i];
    }
  }

  free(thread_arguments);

  free(values);
}