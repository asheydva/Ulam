#include <vector>
#include <set>
#include <unordered_set>
#include <cassert>
#include <string>

#include "NaiveUlam.h"
#include "SignalInitialization.h"

// Function to print continued fraction
std::string to_string(const ContinuedFraction& cf) {
	std::string result{ "[" };
	for (size_t i = 0; i < cf.terms.size(); i++) {
		result += std::to_string(cf.terms[i]);
		if (i < cf.terms.size() - 1) {
			result += ", ";
		}
	}
	result += "]";
	return result;
}

// Function to convert UlamInputs to string
std::string to_string(const UlamInputs& inputs) {
	return "U(" + std::to_string(inputs.a) + "," + std::to_string(inputs.b) + ")";
}

void update_convergent(Convergent& conv, int term) {
	int a_next{ term * conv.a_current + conv.a_previous };
	int b_next{ term * conv.b_current + conv.b_previous };

	conv.a_previous = conv.a_current;
	conv.b_previous = conv.b_current;
	conv.a_current = a_next;
	conv.b_current = b_next;
}

double get_quotient(Convergent conv) {
	double numerator{ static_cast<double>(conv.a_current) };
	double denominator{ static_cast<double>(conv.b_current) };

	return numerator / denominator;
}

// Function to produce initial data needed to compute Ulam sequences efficiently
IntermediateUlamState initialize_Ulam_state(const UlamInputs& pair) {
	// Empirically determined parameters
	const int num_segments{ 1000 };
	const double error{ PI / num_segments };
	const int num_terms{ 100 };
	const double learning_rate_factor{ 0.01 };

	const int a{ pair.a };
	const int b{ pair.b };

	// Compute initial Ulam sequence using naive algorithm
	UlamOutput ulam_output{ naive_Ulam_sequence(a, b, 100) };

	// Rough approximation of signal using Fourier series
	double signal_approx{ fourier_approximation(ulam_output.ulam_terms, num_segments) };

	double learning_rate{ learning_rate_factor / static_cast<double>(ulam_output.ulam_terms.back() * num_terms) };

	// Refine signal using gradient descent
	double signal_refinement{ fourier_refinement(signal_approx, ulam_output.ulam_terms, learning_rate, 10) };

	// Compute lambda and its error
	double lambda{ 2 * PI / signal_refinement };
	double lambda_error{ (2 * PI / (signal_refinement * signal_refinement)) * error };

	// Check whether lambda corresponds to a middle-thirds signal
	assert(2 * middle_third_proportion(ulam_output.ulam_terms, lambda) > 0.5);

	// Compute continued fraction representation of lambda
	ContinuedFraction cf{ compute_continued_fraction(lambda, lambda_error) };

	return IntermediateUlamState{ ulam_output.ulam_terms, lambda, lambda_error, cf.numerator, cf.denominator };
}