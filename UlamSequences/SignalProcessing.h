#ifndef INITIAL_SIGNAL
#define INITIAL_SIGNAL

const double PI{ std::atan(1.0) * 4.0 };
const double EPSILON{ 1e-10 };
const double GOLDEN_RATIO{(1.0+std::sqrt(5.0))/2.0};

using UlamVector = std::vector<long>;

// Struct to hold setting for Fourier search
struct FourierSettings {
	double xmin;
	double xmax;
};

// Struct to hold signal data
struct Signal {
	double lower_bound;
	double peak;
	double upper_bound;
};

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
	UlamVector ulam_terms;
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

// Static subroutines for initialize_Ulam_state

static double next_uniform_point();

// Fourier helper functions
static double fourier_sum(const UlamVector& ulam_seq, const double x);
static double fourier_derivative_sum(const UlamVector& ulam_seq, const double x);

// Rough approximation of signal using Fourier series and search
static double fourier_approximation(const UlamVector& ulam_seq, const int num_steps);
static Signal fourier_approximation(const UlamVector& ulam_seq, const FourierSettings& settings);

// Refine approximation of signal using gradient descent
static double fourier_refinement(const double min_x, const UlamVector& ulam_seq, const double learning_rate, const int num_iterations);

// Functions for manipulating convergents

// Update convergent with next term in continued fraction
void update_convergent(Convergent& conv, int term);

// Get quotient from convergent
double get_quotient(Convergent conv);

// Function template to compute continued fraction, accurate up to given error
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
double middle_third_proportion(const UlamVector& ulam_terms, double lambda);

// Function to produce initial data needed to compute Ulam sequences efficiently
IntermediateUlamState initialize_Ulam_state(const UlamInputs& pair);

#endif#