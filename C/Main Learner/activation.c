#include "activation.h"
#include <math.h>

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