#include <vector>
#include <set>
#include <unordered_set>
#include <cassert>

#include "NaiveUlam.h"

// The basic O(n^2) algorithm for generating Ulam sequences U(a,b) with prior state
UlamOutput naive_Ulam_sequence(const int a, const int b, const int num_terms, UlamOutput& prior_state)
{
	// If prior state has enough terms already computed, return it
	if (prior_state.computed_terms >= num_terms) {
		return prior_state;
	}

	// Create copy of prior Ulam terms
	std::vector<long> ulam_terms{ prior_state.ulam_terms };
	ulam_terms.resize(num_terms);

	// Create copies of prior unique and multiple representation sets
	std::set<long> unique_rep{ prior_state.unique_rep };
	std::unordered_set<long> mult_rep{ prior_state.mult_rep };

	// Compute Ulam terms iteratively
	for (int i = prior_state.computed_terms; i < num_terms; i++) {
		// Get latest Ulam number
		const long u{ ulam_terms[i - 1] };

		// Find all sums with previous Ulam terms
		for (int j = 0; j < i - 1; j++) {
			const long v{ u + ulam_terms[j] };

			// If the element has multiple representations do nothing
			// If the element has one representation, move it from unique_rep to mult_rep
			// If the element has no representations, and it to unique_rep
			if (!mult_rep.contains(v)) {
				if (unique_rep.erase(v) == 1) {
					mult_rep.insert(v);
				}
				else {
					unique_rep.insert(v);
				}
			}
		}

		// Smallest element with one rep moved to Ulam sequence
		assert(!unique_rep.empty());
		auto first_term = unique_rep.cbegin();
		ulam_terms[i] = *first_term;
		unique_rep.erase(first_term);
	}

	return UlamOutput{ ulam_terms,unique_rep,mult_rep,num_terms };
}

// The basic O(n^2) algorithm for generating Ulam sequences U(a,b)
UlamOutput naive_Ulam_sequence(const int a, const int b, const int num_terms) {
	// Initialize UlamOutput struct
	std::vector<long> ulam_terms(num_terms);
	ulam_terms[0] = a;
	ulam_terms[1] = b;

	std::set<long> unique_rep{};
	std::unordered_set<long> mult_rep{};

	UlamOutput output{ ulam_terms, unique_rep, mult_rep, 2 };

	return naive_Ulam_sequence(a, b, num_terms, output);
}