#include <vector>
#include <set>
#include <unordered_set>
#include <iostream>
#include <cmath>
#include <numeric>

const double PI{ std::atan(1.0) * 4.0 };
const double EPSILON{ 1e-10 };

// Struct to hold Ulam sequence data
struct UlamOutput {
	std::vector<int> ulam_terms;
	std::set<int> unique_rep;
	std::unordered_set<int> mult_rep;
	int computed_terms{ 0 };
};

// The basic O(n^2) algorithm for generating Ulam sequences U(a,b) with prior state
UlamOutput naive_Ulam_sequence(const int a, const int b, const int num_terms, UlamOutput& prior_state)
{
	// Create copy of prior Ulam terms
	std::vector<int> ulam_terms{prior_state.ulam_terms};
	ulam_terms.resize(num_terms);

	// Create copies of prior unique and multiple representation sets
	std::set<int> unique_rep{prior_state.unique_rep};
	std::unordered_set<int> mult_rep{prior_state.mult_rep};

	// Compute Ulam terms iteratively
	for (int i = prior_state.computed_terms; i < num_terms; i++) {
		// Get latest Ulam number
		const int u{ ulam_terms[i-1] };

		// Find all sums with previous Ulam terms
		for (int j = 0; j < i-1; j++) {
			const int v{ u + ulam_terms[j] };

			// If the element has multiple representations do nothing
			// If the element has one representation, move it from unique_rep to mult_rep
			// If the element has no representations, and it to unique_rep
			if (mult_rep.find(v) == mult_rep.end()) {
				if (unique_rep.erase(v) == 1) {
					mult_rep.insert(v);
				}
				else {
					unique_rep.insert(v);
				}
			}
		}

		// Smallest element with one rep moved to Ulam sequence
		auto first_term = unique_rep.cbegin();
		ulam_terms[i] = *first_term;
		unique_rep.erase(first_term);
	}

	return UlamOutput{ulam_terms,unique_rep,mult_rep,num_terms};
}

// The basic O(n^2) algorithm for generating Ulam sequences U(a,b)
UlamOutput naive_Ulam_sequence(const int a, const int b, const int num_terms) {
	// Initialize UlamOutput struct
	std::vector<int> ulam_terms(num_terms);
	ulam_terms[0] = a;
	ulam_terms[1] = b;

	std::set<int> unique_rep{};
	std::unordered_set<int> mult_rep{};

	UlamOutput output{ ulam_terms, unique_rep, mult_rep, 2 };

	return naive_Ulam_sequence(a, b, num_terms, output);
}

// Fourier helper function
template <typename T>
static double fourier_sum(const std::vector<T>& ulam_seq, const double x) {
	double sum{ 0 };

	for (T u : ulam_seq) {
		sum += std::cos(u * x);
	}

	return sum;
}

// Rough approximation of signal using Fourier series
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

// Struct to hold magic numbers
struct MagicNumber {
	int a_current;
	int b_current;
	int a_previous;
	int b_previous;
};

// Function to create new magic number with new term in continued fraction expansion
static MagicNumber extend_continued_fraction(const MagicNumber magic, const int term) {
	MagicNumber new_magic;
	new_magic.a_current = term * magic.a_current + magic.a_previous;
	new_magic.b_current = term * magic.b_current + magic.b_previous;
	new_magic.a_previous = magic.a_current;
	new_magic.b_previous = magic.b_current;
	return new_magic;
}

// Function to update magic number with new term in continued fraction expansion
static void extend_continued_fraction(MagicNumber* pMagic, const int term) {
	const int a = pMagic->a_current;
	const int b = pMagic->b_current;
	const int c = pMagic->a_previous;
	const int d = pMagic->b_previous;

	pMagic->a_current = term * a + c;
	pMagic->b_current = term * b + d;
	pMagic->a_previous = a;
	pMagic->b_previous = b;
}

void print(const MagicNumber* pMagic) {
	std::cout << "MagicNumber(" << pMagic->a_current << ", " << pMagic->b_current << "; "
		<< pMagic->a_previous << ", " << pMagic->b_previous << ")\n";
}

// Function to compute MagicNumber from fourier approximation
static MagicNumber compute_magic_number(const double fourier_approximation, const int max_terms) {
	double lambda{ 2 * PI / fourier_approximation };

	// Initialize MagicNumber with first term of continued fraction
	MagicNumber magic{ static_cast<int>(lambda),1,1,0};

	for (int i = 1; i < max_terms; i++) {
		// Get fractional part of lambda
		double remainder{ lambda - std::floor(lambda) };
		
		if (remainder < EPSILON) {
			// Terminating continued fraction

			std::cout << "WARNING: Continued fraction terminated early at term " << i << "\n";
			return magic;
		}

		lambda = 1 / remainder;
		int term = static_cast<int>(std::floor(lambda));

		extend_continued_fraction(&magic, term);
	}

	return magic;
}


// Function to compute accuracy of MagicNumber against Ulam sequence data
template <typename T>
double compute_magic_accuracy(const MagicNumber* pMagic, const std::vector<T>& ulam_seq) {
	const int a{ pMagic->a_current };
	const int b{ pMagic->b_current };

	double total_error{ 0.0 };

	const int min_third{ a / 3 };
	const int max_twothird{ (2 * a) / 3 };

	for (T u : ulam_seq) {
		int remainder{ (static_cast<long>(b) * u) % a };

		if (remainder < min_third or remainder >= max_twothird) {
			total_error += 1.0;
		}
	}

	return 1-total_error / static_cast<double>(ulam_seq.size());
}

// Function to refine MagicNumber using Ulam sequence data
// Returns whether refinement was successful
template <typename T>
bool refine_magic_number(MagicNumber* pMagic, const std::vector<T>& ulam_seq, const int breadth) {
	bool refined{ false };
	double current_accuracy{ compute_magic_accuracy(pMagic, ulam_seq) };

	for (int term=1; term <= breadth; term++) {
		MagicNumber candidate{ *pMagic };
		extend_continued_fraction(&candidate, term);
		double candidate_accuracy{ compute_magic_accuracy(&candidate, ulam_seq) };
		
		if (candidate_accuracy > current_accuracy) {
			*pMagic = candidate;
			current_accuracy = candidate_accuracy;
			refined = true;
		}
	}
	return refined;
}

int main()
{
	for (int i = 1; i < 3; i++) {
		int a = 2 * i + 1;

		for (int res = (1 % a); res < a; res++) {
			for (int k = 1; k < 6; k++) {		
				int b = a * k + res;

				if (a!=5 or b!=6) {
					UlamOutput ulam_data{ naive_Ulam_sequence(a,b,200) };
					double alpha{ fourier_approximation(ulam_data.ulam_terms, 13860) };
					MagicNumber magic{ compute_magic_number(alpha, 4) };

					if (compute_magic_accuracy(&magic, ulam_data.ulam_terms) < .7) {
						refine_magic_number(&magic, ulam_data.ulam_terms, 100);
					}

					std::cout << a << " " << b << " ";
					std::cout << "Initial Accuracy: " << compute_magic_accuracy(&magic, ulam_data.ulam_terms) << "\n";
					ulam_data = naive_Ulam_sequence(a, b, 1000, ulam_data);
					std::cout << "Initial Accuracy (extended): " << compute_magic_accuracy(&magic, ulam_data.ulam_terms) << "\n";
					if (refine_magic_number(&magic, ulam_data.ulam_terms, 100)) {
						refine_magic_number(&magic, ulam_data.ulam_terms, 100);
						std::cout << "Updated Accuracy (extended): " << compute_magic_accuracy(&magic, ulam_data.ulam_terms) << "\n";
					}
					std::cout << "\n";
				}
			}
		}
	}
    
    return 0;
}
