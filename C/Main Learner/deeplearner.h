double activate(int activate_value, double x);
void vector_activate(int activate_value, int distance, int count, double *values);
double varyfind(int line_count, int line_num, int input_neuron_count, int hidden_total_neurons, int output_neuron_count, double target_values[], double hidden_values_layers[]);
void forward(int line_count, int line_num, int *activate_num, int *hidden_sizes, int layer_count, int bias_count, int input_neuron_count, int output_neuron_count, double *hidden_values_layers, double *hidden_layers);
void backward(int line_count, int line_num, int *activate_num, int *hidden_sizes, int hidden_total_neurons, int bias_count, int hidden_total_weights, double learning_rate, int layer_count, int input_neuron_count, int output_neuron_count, double *hidden_values_layers, double *target_values, double *hidden_layers);
