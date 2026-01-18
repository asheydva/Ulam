#include <vector>
#include <set>
#include <unordered_set>
#include <iostream>
#include <cmath>
#include <numeric>
#include <cassert>
#include <string>

#include "NaiveUlam.h"
#include "SignalInitialization.h"

// Function to specify Ulam sequence inputs
std::vector<UlamInputs> specify_ulam_inputs(int depth) {
	std::vector<UlamInputs> inputs;

	// U(2,n) is regular for all odd n > 3, but U(2,3) is (to our knowledge) not
	inputs.push_back(UlamInputs{ 2, 3 });

	// U(4,n) and U(m,n) with m>5 are conjectured to be regular
	// So we only consider U(3,n) and U(5,n) here
	for (int i = 1; i < 3; i++) {
		int a = 2 * i + 1;

		// Group by residue classes mod a
		for (int res = (1 % a); res < a; res++) {
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


int main()
{   
	const int num_segments{ 1000 };
	const double error{ PI / num_segments };

	std::cout << "Ulam Sequence Lambda Computation\n\n";

	for (UlamInputs pair : specify_ulam_inputs(4)) {
		std::cout << to_string(pair) << ": ";

		IntermediateUlamState state{ initialize_Ulam_state(pair) };
		std::cout << state.lambda << " (+/- " << state.lambda_error << ")\n";
	}

    return 0;
}
