#include <vector>
#include <set>
#include <unordered_set>
#include <iostream>
#include <cmath>
#include <numeric>
#include <cassert>
#include <string>
#include <chrono>

#include "NaiveUlam.h"
#include "SignalProcessing.h"

// Function to specify Ulam sequence inputs
std::vector<UlamInputs> specify_ulam_inputs(int depth) {
	std::vector<UlamInputs> inputs;

	// U(2,n) is regular for all odd n > 3, U(2,3) is (to our knowledge) not
	inputs.push_back(UlamInputs{ 2, 3 });

	// U(4,n) and U(m,n) with m>5 are conjectured to be regular
	// So we only consider U(3,n) and U(5,n) here
	for (int i = 1; i < 3; i++) {
		int a = 2 * i + 1;

		// Group by residue classes mod a
		for (int res = 1; res < a; res++) {
			for (int k = 1; k <= depth; k++) {
				int b = a * k + res;

				// Exclude U(5,6) which is conjectured to be regular
				if (a != 5 or b != 6) {
					inputs.push_back(UlamInputs{ a,b });
				}
			}
		}
	}
	return inputs;
}

inline int positive_modulo(int i, int n) {
	return (i % n + n) % n;
}

// Main class for storing Ulam sequences using the magic number
using Arc = std::pair<int, int>;
using Bins=std::vector<std::unordered_set<long>>;

class UlamBins {
private:
	int numerator{};
	int denominator{};
	long num_terms{};
	long last_tested{};
	long num_outliers{};
	Bins bins{};

	int key(long n) const {
		return positive_modulo(n * denominator, numerator);
	}

	bool is_outlier(int bin_index) const {
		const int lower_third = numerator / 3;
		const int upper_third = 2 * numerator / 3;
		return (bin_index < lower_third or bin_index > upper_third);
	}

	void add_term(long term) {
		int bin_index = key(term);
		bins[bin_index].insert(term);

		num_terms++;

		if (is_outlier(bin_index)) {
			num_outliers++;
		}
	}

	Arc compute_arc(int target_key) const {
		const int half{ target_key / 2 };
		const int antihalf{ ((target_key + numerator) / 2)};
		const int antiparity{ (target_key + numerator) % 2 };

		const int corrected_antihalf{ positive_modulo(antihalf + antiparity, numerator) };

		if ((3 * target_key) / numerator < 2) {
			return Arc{ half, corrected_antihalf };
		}
		return Arc{ corrected_antihalf, half };
	}

public:
	UlamBins(IntermediateUlamState& state)
		: numerator{ state.numerator }, denominator{ state.denominator }, num_terms{ static_cast<long>(state.ulam_terms.size()) }, last_tested{ state.ulam_terms.back() }, num_outliers{ 0 }
	{
		// Initialize bins
		bins.resize(numerator);
		for (long term : state.ulam_terms) {
			int bin_index{ key(term) };
			bins[bin_index].insert(term);

			if (is_outlier(bin_index)) {
				num_outliers++;
			}
		}
	}

	long get_last_tested() const {
		return last_tested;
	}

	long get_num_terms() const {
		return num_terms;
	}

	float outlier_proportion() const {
		return static_cast<float>(num_outliers) / static_cast<float>(num_terms);
	}

	bool test_next_term() {
		// Define the candidate term and its key
		const long candidate = last_tested + 1;
		const int target_key = key(candidate);

		// Compute the arc for the target key and determine search direction
		const Arc arc{ compute_arc(target_key) };
		const int start{ arc.first };
		const int end{ arc.second };
		const int direction{ (start < end) ? -1 : 1 };

		int unique_sum_count{ 0 };

		int bin_index{ start };

		while (bin_index != end + direction) {
			for (long u : bins[bin_index]) {
				const long v{ candidate - u };


				// Check if v exists in the appropriate bin
				const int v_key{ key(v) };
				if (v_key != bin_index or u < v) {
					// Ensure u < v to avoid double counting, if u and v are in the same bin
					if (bins[v_key].contains(v)) {
						unique_sum_count++;

						// If more than one representation is found, exit early
						if (unique_sum_count > 1) {
							last_tested = candidate;
							return false;
						}
					}
				}
			}

			bin_index += direction;
			bin_index = positive_modulo(bin_index, numerator);
		}

		last_tested = candidate;

		// If exactly one representation is found, add the candidate term
		if (unique_sum_count == 1) {
			add_term(candidate);
			return true;
		}

		return false;
	}
};

double log2_cutoff(double outlier_proportion) {
	double exponent{ std::log(outlier_proportion) / std::log(2) };
	return std::pow(2.0, std::ceil(exponent));
}

double log3_cutoff(double outlier_proportion) {
	double exponent{ std::log(outlier_proportion) / std::log(3) };
	return std::pow(3.0, std::ceil(exponent));
}

double balanced_cutoff(double outlier_proportion) {
	return std::min(log2_cutoff(outlier_proportion), log3_cutoff(outlier_proportion));
}

int main()
{   
	const int num_segments{ 1000 };
	const double error{ PI / num_segments };

	std::cout << "Ulam Sequence Lambda Computation\n\n";

	int total_terms{ 0 };
	auto start{ std::chrono::system_clock::now() };

	for (UlamInputs pair : specify_ulam_inputs(4)) {
		std::cout << to_string(pair) << ": ";

		IntermediateUlamState state{ initialize_Ulam_state(pair) };
		std::cout << state.lambda << " (+/- " << state.lambda_error << ")\n";

		UlamBins ulam_bins{ state };
		std::cout << "Outlier Proportion: " << ulam_bins.outlier_proportion() << "\n";

		double cutoff{ balanced_cutoff(ulam_bins.outlier_proportion()) };
		std::cout << "Cutoff: " << cutoff << "\n";

		bool outlier_limit_reached{ false };

		for (int i = 0; i < 100000; i++) {
			if (ulam_bins.test_next_term()) {
				if (ulam_bins.outlier_proportion() >= cutoff) {
					outlier_limit_reached = true;
					break;
				}
			}
		}

		std::cout << "Computed " << ulam_bins.get_num_terms() << " terms.\n";
		total_terms += ulam_bins.get_num_terms();
		std::cout << "Last term computed: " << ulam_bins.get_last_tested() << "\n";
		std::cout << "Outlier limit" << (outlier_limit_reached ? " ":" not ") << "reached.\n";
		std::cout << "-----------------------------------\n";
	}

	auto end{ std::chrono::system_clock::now() };
	std::chrono::duration<double, std::milli> duration{ end - start };
	std::cout << "Time per term: " << duration / total_terms << "\n";

    return 0;
}