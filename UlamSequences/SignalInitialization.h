#ifndef INITIAL_SIGNAL
#define INITIAL_SIGNAL

const double PI{ std::atan(1.0) * 4.0 };
const double EPSILON{ 1e-10 };

// Struct to hold continued fraction data
struct ContinuedFraction {
	std::vector<int> terms;
	int numerator;
	int denominator;
};

// Struct to hold convergents data
struct Convergent {
	int a_current;
	int a_previous;
	int b_current;
	int b_previous;
};

// Struct to hold data needed to initialize efficient Ulam sequence computation
struct IntermediateUlamState {
	std::vector<int> ulam_terms;
	double lambda;
	double lambda_error;
	int numerator;
	int denominator;
};

// Struct to hold Ulam sequence input pairs
struct UlamInputs {
	int a;
	int b;
};


// Printing functions
std::string to_string(const ContinuedFraction& cf);
std::string to_string(const UlamInputs& inputs);

//
// All following functions are templates to allow for different integer types in Ulam sequences
// They are static as they are subroutines for initialize_Ulam_state

// Fourier helper function
template <typename T>
static double fourier_sum(const std::vector<T>& ulam_seq, const double x) {
	double sum{ 0 };

	for (T u : ulam_seq) {
		sum += std::cos(u * x);
	}

	return sum;
}

// Fourier helper function
template <typename T>
static double fourier_derivative_sum(const std::vector<T>& ulam_seq, const double x) {
	double sum{ 0 };

	for (T u : ulam_seq) {
		sum -= u * std::sin(u * x);
	}

	return sum;
}

// Rough approximation of signal using Fourier series and search
template <typename T>
static double fourier_approximation(const std::vector<T>& ulam_seq, const int num_steps) {
	const double min_step{ PI / num_steps };

	double min_x{ 0 };
	double min_y{ fourier_sum(ulam_seq, min_x) };

	for (int i = 1; i <= num_steps; i++) {
		const double x{ min_step * i };
		const double y{ fourier_sum(ulam_seq, x) };

		if (y < min_y) {
			min_x = x;
			min_y = y;
		}
	}

	return min_x;
}

// Refine approximation of signal using gradient descent
template <typename T>
static double fourier_refinement(const double min_x, const std::vector<T>& ulam_seq, const double learning_rate, const int num_iterations) {
	double x{ min_x };
	for (int i = 0; i < num_iterations; i++) {
		const double gradient{ fourier_derivative_sum(ulam_seq, x) };
		x = x - learning_rate * gradient;
	}
	return x;
}

// Non-template functions
// Functions for manipulating convergents

// Update convergent with next term in continued fraction
void update_convergent(Convergent& conv, int term);

// Get quotient from convergent
double get_quotient(Convergent conv);

//
// All functions below are templates to allow for different integer types in Ulam sequences
//

// Function to compute continued fraction, accurate up to given error
template <typename T>
ContinuedFraction compute_continued_fraction(const T value, const T error) {
	T remainder{ value };
	int term{ static_cast<int>(remainder) };

	std::vector<int> terms{ term };

	Convergent conv{ term, 1,1,0 };

	double cf_approx{ get_quotient(conv) };
	double cf_error{ std::abs(value - cf_approx) };

	while (cf_error > error) {
		remainder = remainder - term;
		if (remainder < EPSILON) {
			// Terminating continued fraction
			break;
		}

		remainder = 1 / remainder;
		term = static_cast<int>(remainder);
		terms.push_back(term);

		update_convergent(conv, term);

		cf_approx = get_quotient(conv);
		cf_error = std::abs(value - cf_approx);
	}

	return ContinuedFraction{ terms,conv.a_current,conv.b_current };
}


// Function to compute proportion of Ulam elements in the middle third mod lambda
template <typename T>
double middle_third_proportion(const std::vector<T>& ulam_terms, double lambda) {
	long count{ 0 };

	for (T u : ulam_terms) {
		double mod_value{ std::fmod(u, lambda) };
		if (mod_value > lambda / 3.0 && mod_value < 2.0 * lambda / 3.0) {
			count += 1;
		}
	}

	return static_cast<double>(count) / static_cast<double>(ulam_terms.size());
}

// Function to produce initial data needed to compute Ulam sequences efficiently
IntermediateUlamState initialize_Ulam_state(const UlamInputs& pair);

#endif#