extern "C" {
    void __declspec(dllexport) train(float min_diff, float learning_rate, int line_count_train, float *input_values_train, float *target_values_train, int line_count_test, float *input_values_test, float *target_values_test, int layer_count, int *activate_values, int *hidden_sizes, int hidden_count, int bias_count, int weight_count, float *weight_values);
    void __declspec(dllexport) test(int line_count, float *input_values, int layer_count, int *activate_values, int *hidden_sizes, int hidden_count, int bias_count, int weight_count, float *weight_values, float *output_values);
}