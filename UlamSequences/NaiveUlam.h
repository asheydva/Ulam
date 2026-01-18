#ifndef NAIVE_ULAM_ALGORITHM_H
#define NAIVE_ULAM_ALGORITHM_H

// Struct to hold Ulam sequence data
struct UlamOutput {
	std::vector<int> ulam_terms;
	std::set<int> unique_rep;
	std::unordered_set<int> mult_rep;
	int computed_terms{ 0 };
};

UlamOutput naive_Ulam_sequence(const int a, const int b, const int num_terms, UlamOutput& prior_state);

UlamOutput naive_Ulam_sequence(const int a, const int b, const int num_terms);

#endif#
