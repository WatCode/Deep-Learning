#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "interface.cuh"

int size_of_float = sizeof(float);

float blockSize = 64.0;

float h_zero = 0;
float h_one = 1.0;

__device__ float e = 2.71828182845904523536028747135266;
__device__ float zero = 0;
__device__ float half = 0.5;
__device__ float one = 1.0;
__device__ float two = 2.0;
__device__ float four = 4.0;

__device__ float swish(float x) {
	return x / (one + pow(e, -x));
}

__device__ float dswish(float x) {
	float z = pow(e, x);

	return (z * (z + x + one)) / pow((z + one), two);
}

__device__ float relu(float x) {
	if (x > zero) {
		return x;
	}
	else {
		return zero;
	}
}

__device__ float drelu(float x) {
	if (x >= zero) {
		return one;
	}
	else {
		return zero;
	}
}

__device__ float lerelu(float x) {
	if (x >= zero) {
		return x;
	}
	else {
		return half * x;
	}
}

__device__ float dlerelu(float x) {
	if (x >= zero) {
		return one;
	}
	else {
		return half;
	}
}

__device__ float hyptan(float x) {
	float z1, z2, y;
	z1 = pow(e, x);
	z2 = pow(e, -x);

	y = (z1 - z2) / (z1 + z2);

	return y;
}

__device__ float dhyptan(float x) {
	float z = pow(e, x);

	float y = (z * four) / pow((z + one), two);

	return y;
}

__device__ float sigmoid(float x) {
	return one / (one + pow(e, -x));
}

__device__ float dsigmoid(float x) {
	float z = pow(e, x);

	return z / pow((z + one), two);
}

__device__ float softsign(float x){
	return x / (one + fabs(x));
}

__device__ float dsoftsign(float x){
	return one / pow((one + fabs(x)), two);
}

__device__ float elu(float x) {
	if(x < zero){
		return 0.1*(pow(e, x)-one);
	}
	else{
		return x;
	}
}

__device__ float delu(float x) {
	if (x >= zero){
		return one;
	}
	else{
		return 0.1*pow(e, x);
	}
}

__device__ float activate(int activation_value, float x) {
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

__device__ inline void protectedAddition(float* address, float value){
    float old = value; 
    float new_old;

    do{
        new_old = atomicExch(address, 0.0f);
        new_old += old;
    }
    while ((old = atomicExch(address, new_old))!=0.0f);
};

__global__ void varyfind(float *output_values, int offset_output, float *target_values, int offset_target, float *sum, int count){
    int index = blockIdx.x*blockDim.x + threadIdx.x;

    if(index < count){
        if(target_values[offset_target + index] != 0){
            protectedAddition(&sum[0], fabs((target_values[offset_target + index] - output_values[offset_output + index])/target_values[offset_target + index]));
        }
        else{
            protectedAddition(&sum[0], fabs(target_values[offset_target + index] - output_values[offset_output + index]));
        }
    }
}

__global__ void setValue(float *values, int offset, float value, int count){
    int index = blockIdx.x*blockDim.x + threadIdx.x;

    if(index < count){
        values[offset + index] = value;
    }
}

__global__ void activateValue(float *values, int offset, int activation_value, int count){
    int index = blockIdx.x*blockDim.x + threadIdx.x;

    if(index < count){
        values[offset + index] = activate(activation_value, values[offset + index]);
    }
}

__global__ void vectorMatrixMultiply(float *values, int offset_previous, int previous_count, int offset_current, int current_count, float *weight_values, int offset_weight, int weight_count, int bias_count, int inclusive_count){
    int weight_index = blockIdx.x*blockDim.x + threadIdx.x;
    int previous_index = weight_index%inclusive_count;
    int current_index = (weight_index - previous_index)/inclusive_count;

    if(current_index < current_count){
        if(weight_index < weight_count){
            if(previous_index < previous_count){
                protectedAddition(&values[offset_current + current_index], values[offset_previous + previous_index]*weight_values[offset_weight + weight_index]);
                //__syncthreads();
            }
            else{
                protectedAddition(&values[offset_current + current_index], weight_values[offset_weight + weight_index]);
                //__syncthreads();
            }
        }
    }
}

__global__ void vectorSubtract(float *target_values, int offset_target, float *output_values, int offset_output, float *derivative_sum_values, int offset_derivative, int count){
    int index = blockIdx.x*blockDim.x + threadIdx.x;

    if(index < count){
        derivative_sum_values[offset_derivative + index] = output_values[offset_output + index] - target_values[offset_target + index];
    }
}

__global__ void vectorActivateMultiply(float *values, int offset, float *derivative_sum_values, int offset_derivative, int activation_value, int count){
    int index = blockIdx.x*blockDim.x + threadIdx.x;

    if(index < count){
        derivative_sum_values[offset_derivative + index] *= activate(activation_value, values[offset + index]);
    }
}

__global__ void vectorMatrixAdjust(float *derivative_sum_values, int offset_derivative_next, int offset_derivative_current, float *weight_values, int offset_weight, int weight_count, float *values, int offset, int next_count, int current_count, int bias_count, int inclusive_count, float learning_rate){
    int weight_index = blockIdx.x*blockDim.x + threadIdx.x;
    int next_index = weight_index%inclusive_count;
    int current_index = (weight_index - next_index)/inclusive_count;

    if(current_index < current_count){
        if(weight_index < weight_count){
            if(next_index < next_count){
                if (offset_derivative_next >= zero) {
                    protectedAddition(&derivative_sum_values[offset_derivative_next + next_index], derivative_sum_values[offset_derivative_current + current_index]*weight_values[offset_weight + weight_index]);
                    //__syncthreads();
                }

                protectedAddition(&weight_values[offset_weight + weight_index], -(derivative_sum_values[offset_derivative_current + current_index]*values[offset + next_index]*learning_rate));
                //__syncthreads();
            }
            else{
                protectedAddition(&weight_values[offset_weight + weight_index], -(derivative_sum_values[offset_derivative_current + current_index]*learning_rate));
                //__syncthreads();
            }
        }
    }
}

__global__ void vectorCopy(float *source_values, int offset_source, float *dest_values, int offset_dest, int count){
    int index = blockIdx.x*blockDim.x + threadIdx.x;

    if(index < count){
        dest_values[offset_dest + index] = source_values[offset_source + index];
    }
}

__host__ void forward(int line_count, int line_num, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, float *values, float *weight_values){
    int previous_count, current_count;

    int previous_neuron_distance, current_neuron_distance;

	previous_neuron_distance = line_num*hidden_sizes[0];
	current_neuron_distance = line_count*hidden_sizes[0];

    int weight_distance, current_weight_count;

    weight_distance = h_zero;

    int vectorSize, matrixSize;

	for (int layer_num = h_zero; layer_num < layer_count+1; layer_num++) {
        previous_count = hidden_sizes[layer_num];
		current_count = hidden_sizes[layer_num+1];

        current_weight_count = (previous_count + bias_count)*current_count;

        vectorSize = ceil(current_count/blockSize);
        matrixSize = ceil(current_weight_count/blockSize);

        setValue<<<vectorSize, blockSize>>>(values, current_neuron_distance, h_zero, current_count);
        cudaDeviceSynchronize();

        vectorMatrixMultiply<<<matrixSize, blockSize>>>(values, previous_neuron_distance, previous_count, current_neuron_distance, current_count, weight_values, weight_distance, current_weight_count, bias_count, previous_count+bias_count);
        cudaDeviceSynchronize();

        activateValue<<<vectorSize, blockSize>>>(values, current_neuron_distance, activation_values[layer_num], current_count);
        cudaDeviceSynchronize();

        previous_neuron_distance = current_neuron_distance;
        current_neuron_distance += current_count;
        weight_distance += current_weight_count;
    }
}

__host__ void backward(int line_count, int line_num, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int hidden_count, int weight_count, float *derivative_sum_values, float *values, float *target_values, float *weight_values, float learning_rate){
	int current_count, next_count;

	int current_neuron_distance, next_neuron_distance;

	current_neuron_distance = line_count*hidden_sizes[0] + hidden_count;
	next_neuron_distance = current_neuron_distance;

	int derivative_neuron_distance;

	derivative_neuron_distance = hidden_count;

    int weight_distance, current_weight_count;

    weight_distance = weight_count;

    int vectorSize, matrixSize;

    vectorSize = ceil(hidden_sizes[layer_count+1]/blockSize);

	vectorSubtract<<<vectorSize, blockSize>>>(target_values, line_num*hidden_sizes[layer_count+1], values, current_neuron_distance, derivative_sum_values, hidden_count, hidden_sizes[layer_count+1]);
    cudaDeviceSynchronize();

	for (int layer_num = layer_count+1; layer_num > h_zero; layer_num--) {
		current_count = hidden_sizes[layer_num];
		next_count = hidden_sizes[layer_num-1];

		current_weight_count = (next_count + bias_count)*current_count;
		weight_distance -= current_weight_count;

        vectorSize = ceil(current_count/blockSize);
        matrixSize = ceil(current_weight_count/blockSize);

        if(layer_num == 1){
            next_neuron_distance = line_num*hidden_sizes[0];
        }
        else{
            next_neuron_distance -= next_count;

            setValue<<<vectorSize, blockSize>>>(derivative_sum_values, derivative_neuron_distance-next_count, h_zero, next_count);
            cudaDeviceSynchronize();
        }

		vectorActivateMultiply<<<vectorSize, blockSize>>>(values, current_neuron_distance, derivative_sum_values, derivative_neuron_distance, activation_values[layer_num-1]+1, current_count);
        cudaDeviceSynchronize();

		vectorMatrixAdjust<<<matrixSize, blockSize>>>(derivative_sum_values, derivative_neuron_distance-next_count, derivative_neuron_distance, weight_values, weight_distance, current_weight_count, values, next_neuron_distance, next_count, current_count, bias_count, next_count+bias_count, learning_rate);
        cudaDeviceSynchronize();

        current_neuron_distance -= next_count;
		derivative_neuron_distance -= next_count;
	}
}

__host__ void train(double min_diff, double learning_rate, int cycles, int line_count_train, float *input_values_train, float *target_values_train, int line_count_validate, float *input_values_validate, float *target_values_validate, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int hidden_count, int weight_count, float *weight_values) {
    int input_count = hidden_sizes[0];
    int output_count = hidden_sizes[layer_count+1];

    float *d_values_train, *d_values_validate;

    cudaMalloc(&d_values_train, (line_count_train * input_count + hidden_count + output_count)*size_of_float);
    cudaMalloc(&d_values_validate, (line_count_validate * input_count + hidden_count + output_count)*size_of_float);

    cudaMemcpy(d_values_train, input_values_train, line_count_train*input_count*size_of_float, cudaMemcpyHostToDevice);
    cudaMemcpy(d_values_validate, input_values_validate, line_count_validate*input_count*size_of_float, cudaMemcpyHostToDevice);

    float *d_target_values_train, *d_target_values_validate;

    cudaMalloc(&d_target_values_train, (line_count_train * output_count)*size_of_float);
    cudaMalloc(&d_target_values_validate, (line_count_validate * output_count)*size_of_float);

    cudaMemcpy(d_target_values_train, target_values_train, (line_count_train * output_count)*size_of_float, cudaMemcpyHostToDevice);
    cudaMemcpy(d_target_values_validate, target_values_validate, (line_count_validate * output_count)*size_of_float, cudaMemcpyHostToDevice);

    float *d_weight_values;

    cudaMalloc(&d_weight_values, weight_count*size_of_float);

    cudaMemcpy(d_weight_values, weight_values, weight_count*size_of_float, cudaMemcpyHostToDevice);

    float *derivative_sum_values;

    cudaMalloc(&derivative_sum_values, (hidden_count + output_count)*size_of_float);


    int output_offset_train = line_count_train*input_count + hidden_count;
    int output_offset_validate = line_count_validate*input_count + hidden_count;

    int target_offset;

    float *d_sum;

    cudaMalloc(&d_sum, size_of_float);

    float *sum = (float*) malloc(size_of_float);
    float diff_value;

    float avg_diff_train = min_diff;
    float avg_diff_validate = min_diff;

    float *prev_diff_values = (float*) malloc(line_count_train);
    float *prev_prev_diff_values = (float*) malloc(line_count_train);

    float *learning_rate_values = (float*) malloc(line_count_train);

    memset(learning_rate_values, ((float) learning_rate), line_count_train*size_of_float);

    float learning_rate_coefficient;


    int vectorSize = ceil(output_count/blockSize);


    int cycle = 0;

    while ((cycles == -1 || cycle < cycles) && avg_diff_train >= min_diff) {
        avg_diff_train = 0;

        for (int line_num_train = h_zero; line_num_train < line_count_train; line_num_train++) {
            forward(line_count_train, line_num_train, activation_values, hidden_sizes, layer_count, bias_count, d_values_train, d_weight_values);
            backward(line_count_train, line_num_train, activation_values, hidden_sizes, layer_count, bias_count, hidden_count, weight_count, derivative_sum_values, d_values_train, d_target_values_train, d_weight_values, learning_rate_values[line_num_train]);

            cudaMemset(d_sum, h_zero, size_of_float);
            target_offset = line_num_train*output_count;
            varyfind<<<vectorSize, blockSize>>>(d_values_train, output_offset_train, d_target_values_train, target_offset, d_sum, output_count);
            cudaDeviceSynchronize();
            cudaMemcpy(sum, d_sum, size_of_float, cudaMemcpyDeviceToHost);

            diff_value = sum[0]/output_count;
            avg_diff_train += diff_value;

            learning_rate_coefficient = fabs(((prev_diff_values[line_num_train]-prev_prev_diff_values[line_num_train])/prev_prev_diff_values[line_num_train])/((diff_value-prev_diff_values[line_num_train])/prev_diff_values[line_num_train]));

            if(cycle > h_one && diff_value != prev_diff_values[line_num_train] && prev_diff_values[line_num_train] != prev_prev_diff_values[line_num_train] && learning_rate_coefficient < 1.1){
                learning_rate_values[line_num_train] *= learning_rate_coefficient;
            }
            else{
                learning_rate_values[line_num_train] = learning_rate;
            }

            prev_prev_diff_values[line_num_train] = prev_diff_values[line_num_train];
            prev_diff_values[line_num_train] = diff_value;
        }

        avg_diff_train /= line_count_train;

        avg_diff_validate = 0;

        for(int line_num_validate = h_zero; line_num_validate < line_count_validate; line_num_validate++){
            forward(line_count_validate, line_num_validate, activation_values, hidden_sizes, layer_count, bias_count, d_values_validate, d_weight_values);

            cudaMemset(d_sum, h_zero, size_of_float);
            target_offset = line_num_validate*output_count;
            varyfind<<<vectorSize, blockSize>>>(d_values_validate, output_offset_validate, d_target_values_validate, target_offset, d_sum, output_count);
            cudaDeviceSynchronize();
            cudaMemcpy(sum, d_sum, size_of_float, cudaMemcpyDeviceToHost);

            diff_value = sum[0]/output_count;
            avg_diff_validate += diff_value;
        }

        avg_diff_validate /= line_count_validate;

        printf("%.16f : %.16f\n", avg_diff_train, avg_diff_validate);

        cycle++;
    }
    printf("%.16f\n", weight_values[0]);
    cudaMemcpy(weight_values, d_weight_values, weight_count*size_of_float, cudaMemcpyDeviceToHost);
    printf("%.16f\n", weight_values[0]);
    cudaFree(d_values_train);
    cudaFree(d_values_validate);

    cudaFree(d_target_values_train);
    cudaFree(d_target_values_validate);
    
    cudaFree(d_weight_values);

    cudaFree(derivative_sum_values);

    cudaFree(d_sum);

    free(prev_diff_values);
    free(prev_prev_diff_values);

    free(learning_rate_values);

    free(sum);
}


__host__ void test(int line_count, float *input_values, float *output_values, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int hidden_count, int weight_count, float *weight_values){
    int input_count = hidden_sizes[0];
    int output_count = hidden_sizes[layer_count+1];

    float *d_values;

    cudaMalloc(&d_values, (line_count*input_count + hidden_count + output_count)*size_of_float);

    cudaMemcpy(d_values, input_values, line_count*input_count*size_of_float, cudaMemcpyHostToDevice);

    float *d_weight_values;

    cudaMalloc(&d_weight_values, weight_count*size_of_float);

    cudaMemcpy(d_weight_values, weight_values, weight_count*size_of_float, cudaMemcpyHostToDevice);

    float *d_output_values;

    cudaMalloc(&d_output_values, line_count*output_count*size_of_float);

    int vectorSize = ceil(output_count/blockSize);

    for (int line_num = h_zero; line_num < line_count; line_num++) {
        forward(line_count, line_num, activation_values, hidden_sizes, layer_count, bias_count, d_values, d_weight_values);

        vectorCopy<<<vectorSize, blockSize>>>(d_values, line_count*input_count + hidden_count, d_output_values, line_num*output_count, output_count);
        cudaDeviceSynchronize();
    }

    cudaMemcpy(output_values, d_output_values, line_count*output_count*size_of_float, cudaMemcpyDeviceToHost);

    cudaFree(d_values);
    
    cudaFree(d_weight_values);

    cudaFree(d_output_values);
}