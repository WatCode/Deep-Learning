//Copyright (c) 2023 by Liam Roan Watson and Watcode. All rights reserved. For licensing, contact lrwatson@uwaterloo.ca or +1 437 688 3927

extern "C" {
    void __declspec(dllexport) train(double min_diff, double learning_rate, int cycles, int line_count_train, float *input_values_train, float *target_values_train, int line_count_validate, float *input_values_validate, float *target_values_validate, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int hidden_count, int weight_count, float *weight_values);
    void __declspec(dllexport) test(int line_count, float *input_values, float *output_values, int *activation_values, int *hidden_sizes, int layer_count, int bias_count, int hidden_count, int weight_count, float *weight_values);
}