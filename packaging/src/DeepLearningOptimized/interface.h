//Copyright (c) 2023 by Liam Roan Watson and Watcode. All rights reserved. For licensing, contact lrwatson@uwaterloo.ca or +1 437 688 3927

void train(double min_diff, double learning_rate, int cycles, int ignore_minimum, int batch_count, int stream_train, int shift_count_train, int line_count_train, double *input_values_train, double *target_values_train, int stream_validate, int shift_count_validate, int line_count_validate, double *input_values_validate, double *target_values_validate, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int hidden_count, int weight_count, double *weight_values);
void test(int stream, int shift_count, int line_count, double *input_values, double *output_values, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int hidden_count, int weight_count, double *weight_values);

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