#include "interface.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int size_of_double = sizeof(double);

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
		z = pow(e, values[distance + i]);
		values[distance + i] = z;
		s += z;
	}

	for(int i = 0; i < count; i++) values[distance + i] /= s;
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

void vectorctivate(int activation_value, int distance, int count, double *values) {
	switch (activation_value) {
		case 100:
			softmax(distance, count, values);
	}
}

double varyfind(int lineount, int line_num, int inputount, int hiddenount, int outputount, double *target_values, double *values) {
	double sum = zero;
	int hidden_neuron_distance = lineount * inputount + hiddenount;

	for (int i = zero; i < outputount; i++) {
		if(target_values[line_num * outputount + i] != 0) {
			sum += fabs((target_values[line_num * outputount + i] - values[hidden_neuron_distance + i])/target_values[line_num * outputount + i]);
		}
		else{
			sum += fabs(target_values[line_num * outputount + i] - values[hidden_neuron_distance + i]);
		}
	}

	return sum / ((double)outputount);
}

void forward(int lineount, int line_num, int *activation_values, int *hidden_sizes, int layerount, int biasount, int inputount, int outputount, double *values, double *weight_values) {
	int currentount, prevount, hidden_neuron_distance, hidden_weight_distance, prev_neuron_distance;

	prev_neuron_distance = line_num * inputount;
	hidden_neuron_distance = lineount * inputount;
	hidden_weight_distance = zero;

	for (int layer_num = zero; layer_num < layerount+1; layer_num++) {
		currentount = hidden_sizes[layer_num+1];
		prevount = hidden_sizes[layer_num];

		for (int h = zero; h < currentount; h++) values[hidden_neuron_distance + h] = zero;

		for (int i = zero; i < currentount; i++) {
			for (int j = zero; j < prevount; j++) {
				values[hidden_neuron_distance + i] += values[prev_neuron_distance + j] * weight_values[hidden_weight_distance];
				hidden_weight_distance++;
			}

			for (int j = zero; j < biasount; j++) {
				values[hidden_neuron_distance + i] += weight_values[hidden_weight_distance];
				hidden_weight_distance++;
			}

			if(activation_values[layer_num] < 100) values[hidden_neuron_distance + i] = activate(activation_values[layer_num], values[hidden_neuron_distance + i]);
		}

		if(activation_values[layer_num] >= 100) vectorctivate(activation_values[layer_num], hidden_neuron_distance, currentount, values);

		prev_neuron_distance = hidden_neuron_distance;
		hidden_neuron_distance += currentount;
	}
}

void backward(int lineount, int line_num, int *activation_values, int *hidden_sizes, int layerount, int biasount, int inputount, int hiddenount, int outputount, int weightount, double *values, double *target_values, double *weight_values, double learning_rate) {
	int currentount, nextount, hidden_neuron_distance, hidden_weight_distance, input_neuron_distance;
	double* derivative_sum = (double*)malloc(outputount * size_of_double);
	double* future_sum = (double*)malloc(size_of_double);
	double part_delta;

	hidden_neuron_distance = lineount * inputount + hiddenount;
	hidden_weight_distance = weightount;
	input_neuron_distance = zero;

	for (int h = zero; h < outputount; h++) derivative_sum[h] = (values[hidden_neuron_distance + h] - target_values[line_num * outputount + h]);

	for (int layer_num = layerount+1; layer_num > zero; layer_num--) {
		currentount = hidden_sizes[layer_num];
		nextount = hidden_sizes[layer_num-1];

		if(layer_num == 1) input_neuron_distance = (lineount - line_num - 1) * nextount;

		hidden_weight_distance -= currentount * (nextount + biasount);

		future_sum = (double*)realloc(future_sum, nextount * size_of_double);
		for (int h = zero; h < nextount; h++) future_sum[h] = zero;

		for (int i = zero; i < currentount; i++) {
			part_delta = derivative_sum[i];
			
			if(activation_values[layer_num-1] < 100) part_delta *= activate(activation_values[layer_num-1]+1, values[hidden_neuron_distance + i]);

			for (int j = zero; j < nextount; j++) {
				future_sum[j] += part_delta * weight_values[hidden_weight_distance + i * nextount + j];
				weight_values[hidden_weight_distance + i * nextount + j] -= part_delta * values[hidden_neuron_distance - nextount - input_neuron_distance + j] * learning_rate;
			}

			for (int j = zero; j < biasount; j++) {
				weight_values[hidden_weight_distance + (i + 1) * nextount + j] -= part_delta * learning_rate;
			}
		}

		hidden_neuron_distance -= nextount;

		derivative_sum = (double*)realloc(derivative_sum, nextount * size_of_double);
		for (int k = zero; k < nextount; k++) derivative_sum[k] = future_sum[k];
	}

	free(derivative_sum);
	free(future_sum);
}

void train(double min_diff, double learning_rate, int cycles, int lineount_train, double *input_values_train, double *target_values_train, int lineount_validate, double *input_values_validate, double *target_values_validate, int *activation_values, int *hidden_sizes, int layerount, int biasount, int hiddenount, int weightount, double *weight_values) {
  int inputount = hidden_sizes[0];
  int outputount = hidden_sizes[layerount+1];
  
  double* values_train = (double*) malloc((lineount_train * inputount + hiddenount + outputount) * size_of_double);
  double* values_validate = (double*) malloc((lineount_validate * inputount + hiddenount + outputount) * size_of_double);

  double* learning_rate_values = (double*) malloc(lineount_train * size_of_double);

  double* diff_values = (double*) malloc(lineount_train * size_of_double);
  double* prev_diff_values = (double*) malloc(lineount_train * size_of_double);

  double avg_learning_rate;
  double diff_train, avg_diff_train, prevvg_diff_train;
  double diff_validate, avg_diff_validate, prevvg_diff_validate;
  double changeoefficient, cycles_remainingurrent;
  
  double cycles_remaining_sum1 = zero;
  double cycles_remainingverage1 = zero;
  double cycles_remaining_sum2 = zero;
  double cycles_remainingverage2 = zero;

  int average_size1 = 50;
  int average_size2 = 5;

  double* prevycles_remaining1 = (double*) malloc(average_size1 * size_of_double);
  double* prevycles_remaining2 = (double*) malloc(average_size2 * size_of_double);

  int minimum_reached = zero;

  int cycle = zero;

  memcpy(values_train, input_values_train, lineount_train*inputount*size_of_double);
  memcpy(values_validate, input_values_validate, lineount_validate*inputount*size_of_double);

  for(int i = zero; i < lineount_train; i++) learning_rate_values[i] = learning_rate;

  avg_diff_train = min_diff;

  while (avg_diff_train >= min_diff && (minimum_reached == zero && (cycles == -1 || cycle < cycles))) {
    avg_learning_rate = zero;
    avg_diff_train = zero;
    avg_diff_validate = zero;

    for (int line_num_train = zero; line_num_train < lineount_train; line_num_train++) {
      forward(lineount_train, line_num_train, activation_values, hidden_sizes, layerount, biasount, inputount, outputount, values_train, weight_values);
      backward(lineount_train, line_num_train, activation_values, hidden_sizes, layerount, biasount, inputount, hiddenount, outputount, weightount, values_train, target_values_train, weight_values, learning_rate_values[line_num_train]);
      
      diff_train = varyfind(lineount_train, line_num_train, inputount, hiddenount, outputount, target_values_train, values_train);
      avg_diff_train += diff_train;

      changeoefficient = fabs(((diff_values[line_num_train]-prev_diff_values[line_num_train])/prev_diff_values[line_num_train])/((diff_train-diff_values[line_num_train])/diff_values[line_num_train]));

      if(diff_train > diff_values[line_num_train]){
        changeoefficient = 0.1;
      }

      if(changeoefficient > 1.2){
        changeoefficient = 1.2;
      }

      if(cycle > one && diff_train != diff_values[line_num_train] && diff_values[line_num_train] != prev_diff_values[line_num_train]){
        learning_rate_values[line_num_train] *= changeoefficient;
      }
      else{
        learning_rate_values[line_num_train] = learning_rate;
      }

      avg_learning_rate += learning_rate_values[line_num_train];

      prev_diff_values[line_num_train] = diff_values[line_num_train];
      diff_values[line_num_train] = diff_train;
    }

    for(int line_num_validate = zero; line_num_validate < lineount_validate; line_num_validate++){
      forward(lineount_validate, line_num_validate, activation_values, hidden_sizes, layerount, biasount, inputount, outputount, values_train, weight_values);
      
      diff_validate = varyfind(lineount_validate, line_num_validate, inputount, hiddenount, outputount, target_values_validate, values_validate);
      avg_diff_validate += diff_validate;
    }

    avg_learning_rate /= (double) lineount_train;
    avg_diff_train /= (double) lineount_train;
    avg_diff_validate /= (double) lineount_validate;

    if(cycle > average_size2){
      cycles_remainingverage2 = cycles_remaining_sum2/average_size2;
      cycles_remaining_sum2 -= prevycles_remaining2[0];
    }

    if(cycle > average_size1){
      cycles_remainingverage1 = cycles_remaining_sum1/average_size1;

      if(cycles_remainingverage2 < 0.999*cycles_remainingverage1 && cycles_remainingverage2 < one){
        minimum_reached = one;
      }

      cycles_remaining_sum1 -= prevycles_remaining1[0];
    }

    if(cycle > zero){
      cycles_remainingurrent = ((prevvg_diff_train/avg_diff_train)+(prevvg_diff_validate/avg_diff_validate))/two;
      cycles_remaining_sum1 += cycles_remainingurrent;
      cycles_remaining_sum2 += cycles_remainingurrent;

      for(int i = zero; i < average_size1-1; i++) prevycles_remaining1[i] = prevycles_remaining1[i+1];
      for(int i = zero; i < average_size2-1; i++) prevycles_remaining2[i] = prevycles_remaining2[i+1];

      prevycles_remaining1[average_size1-1] = cycles_remainingurrent;
      prevycles_remaining2[average_size2-1] = cycles_remainingurrent;
    }

    prevvg_diff_train = avg_diff_train;
    prevvg_diff_validate = avg_diff_validate;

    printf("%.16f : %.16f : %.16f : %.16f : %.16f\n", avg_diff_train, avg_diff_validate, cycles_remainingverage1, cycles_remainingverage2, avg_learning_rate);
    
    cycle++;
  }

  free(values_train);
  free(values_validate);

  free(learning_rate_values);

  free(diff_values);
  free(prev_diff_values);

  free(prevycles_remaining1);
  free(prevycles_remaining2);
}

void test(int lineount, double *input_values, double *output_values, int *activation_values, int *hidden_sizes, int layerount, int biasount, int hiddenount, int weightount, double *weight_values){
  int inputount = hidden_sizes[0];
  int outputount = hidden_sizes[layerount+1];

  double* values = (double*) malloc((lineount * inputount + hiddenount + outputount) * size_of_double);
  int hidden_neuron_dist = lineount * inputount + hiddenount;

  for(int i = zero; i < lineount * inputount; i++) values[i] = input_values[i];

  for (int line_num = zero; line_num < lineount; line_num++) {
    forward(lineount, line_num, activation_values, hidden_sizes, layerount, biasount, inputount, outputount, values, weight_values);

    for (int i = zero; i < outputount; i++){
      output_values[line_num * outputount + i] = values[hidden_neuron_dist + i];
    }
  }

  free(values);
}