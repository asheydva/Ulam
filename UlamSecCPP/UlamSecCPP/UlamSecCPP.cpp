// UlamSecCPP.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <iostream>
#include <string>
#include <vector>
#include <unordered_set>
#include <algorithm>    // std::min_element, std::max_element

using namespace std;

int min_element(unordered_set<int> set)
{
    // quick and dirty
    int curMit = INT_MAX;
    for (int elem : set)
        if (elem < curMit)
            curMit = elem;
    return curMit;
}

// Adds/removes the element. Returns True if removes, False otherwise
bool removeOrAdd(unordered_set<int> &set, int elem)
{
    // try to remove
    if (set.erase(elem))
        return true;
    // otherwise insert
    set.insert(elem);
    return false;
}

int ulam_sequence(int n, int X)
{
    vector<int> ulam_seq{ 1, n };
    unordered_set<int> unique_set{ n + 1 };
    unordered_set<int> non_unique_set;

    int largest_elem = n + 1;
    
    cout << "1\n" << n << '\n';

    while (true)
    {
        int smallest_unique = min_element(unique_set);

        for (int elem : ulam_seq)
        {
            int u = smallest_unique + elem;

            // Look in non_unique_set to see if u is in there
            if (!non_unique_set.count(u))
            {
                if (removeOrAdd(unique_set, u))
                {
                    // If already in unique_set, add to non_unique_set
                    non_unique_set.insert(u);
                }
            }

        }

        smallest_unique = min_element(unique_set);
        unique_set.erase(smallest_unique);

        int largest_elem = smallest_unique;
        if (largest_elem > X)
            break;

        ulam_seq.push_back(largest_elem);
        cout << largest_elem << '\n';
    }

    return ulam_seq.size();
}

int main(int argc, char *argv[])
{
    for (int count = 0; count < argc; ++count)
        cout << "command line arguments: " << count << " " << argv[count] << '\n';

    int n = 2;
    int X = 1000;
    string fileName = "";

    int nMembers = ulam_sequence(n, X);
    cout << "ulam_sequence(" << n << "," << X << ") has " << nMembers << " members\n";
}
