#include "deeplearner.h"
#include "activation.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

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
			return softmax(distance, count, values);
	}
}

double varyfind(int line_count, int line_num, int input_count, int total_hidden_count, int output_count, double *target_values, double *hidden_values_layers) {
	double sum = zero_B;
	int hidden_neuron_distance = line_count * input_count + total_hidden_count;

	for (int i = zero_B; i < output_count; i++) {
		if(target_values[line_num * output_count + i] != 0) {
			sum += fabs((target_values[line_num * output_count + i] - hidden_values_layers[hidden_neuron_distance + i])/target_values[line_num * output_count + i]);
		}
		else{
			sum += fabs(target_values[line_num * output_count + i] - hidden_values_layers[hidden_neuron_distance + i]);
		}
	}

	return sum / ((double)output_count);
}

void forward(int line_count, int line_num, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int input_count, int output_count, double *hidden_values_layers, double *weights_values) {
	int current_count, prev_count, hidden_neuron_distance, hidden_weight_distance, prev_neuron_distance;

	prev_neuron_distance = line_num * input_count;
	hidden_neuron_distance = line_count * input_count;
	hidden_weight_distance = zero_B;

	for (int layer_num = zero_B; layer_num < layer_count+1; layer_num++) {
		current_count = hidden_sizes[layer_num+1];
		prev_count = hidden_sizes[layer_num];

		for (int h = zero_B; h < current_count; h++) hidden_values_layers[hidden_neuron_distance + h] = zero_B;

		for (int i = zero_B; i < current_count; i++) {
			for (int j = zero_B; j < prev_count; j++) {
				hidden_values_layers[hidden_neuron_distance + i] += hidden_values_layers[prev_neuron_distance + j] * weights_values[hidden_weight_distance];
				hidden_weight_distance++;
			}

			for (int j = zero_B; j < bias_count; j++) {
				hidden_values_layers[hidden_neuron_distance + i] += weights_values[hidden_weight_distance];
				hidden_weight_distance++;
			}

			if(activation_values[layer_num] < 100) hidden_values_layers[hidden_neuron_distance + i] = activate(activation_values[layer_num], hidden_values_layers[hidden_neuron_distance + i]);
		}

		if(activation_values[layer_num] >= 100) vector_activate(activation_values[layer_num], hidden_neuron_distance, current_count, hidden_values_layers);

		prev_neuron_distance = hidden_neuron_distance;
		hidden_neuron_distance += current_count;
	}
}

void backward(int line_count, int line_num, int *activation_values, int *hidden_sizes, int total_hidden_count, int bias_count, int weights_count, double learning_rate, int layer_count, int input_count, int output_count, double *hidden_values_layers, double *target_values, double *weights_values) {
	int current_count, next_count, hidden_neuron_distance, hidden_weight_distance, input_neuron_distance;
	double* derivative_sum = (double*)malloc(output_count * size_of_double_B);
	double* future_sum = (double*)malloc(size_of_double_B);
	double part_delta;

	hidden_neuron_distance = line_count * input_count + total_hidden_count;
	hidden_weight_distance = weights_count;
	input_neuron_distance = zero_B;

	for (int h = zero_B; h < output_count; h++) derivative_sum[h] = (hidden_values_layers[hidden_neuron_distance + h] - target_values[line_num * output_count + h]);

	for (int layer_num = layer_count+1; layer_num > zero_B; layer_num--) {
		current_count = hidden_sizes[layer_num];
		next_count = hidden_sizes[layer_num-1];

		if(layer_num == 1) input_neuron_distance = (line_count - line_num - 1) * next_count;

		hidden_weight_distance -= current_count * (next_count + bias_count);

		future_sum = (double*)realloc(future_sum, next_count * size_of_double_B);
		for (int h = zero_B; h < next_count; h++) future_sum[h] = zero_B;

		for (int i = zero_B; i < current_count; i++) {
			part_delta = derivative_sum[i];
			
			if(activation_values[layer_num-1] < 100) part_delta *= activate(activation_values[layer_num-1]+1, hidden_values_layers[hidden_neuron_distance + i]);

			for (int j = zero_B; j < next_count; j++) {
				future_sum[j] += part_delta * weights_values[hidden_weight_distance + i * next_count + j];
				weights_values[hidden_weight_distance + i * next_count + j] -= part_delta * hidden_values_layers[hidden_neuron_distance - next_count - input_neuron_distance + j] * learning_rate;
			}

			for (int j = zero_B; j < bias_count; j++) {
				weights_values[hidden_weight_distance + (i + 1) * next_count + j] -= part_delta * learning_rate;
			}
		}

		hidden_neuron_distance -= next_count;

		derivative_sum = (double*)realloc(derivative_sum, next_count * size_of_double_B);
		for (int k = zero_B; k < next_count; k++) derivative_sum[k] = future_sum[k];
	}

	free(derivative_sum);
	free(future_sum);
}
