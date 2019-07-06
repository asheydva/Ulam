// UlamSecCPP.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <iostream>
#include<string> // for string class 
using namespace std;

string ulam_sequence(int n, int X)
{
    return "not implemented\n";
}

int main(int argc, char *argv[])
{
    for (int count = 0; count < argc; ++count)
        cout << "command line arguments: " << count << " " << argv[count] << '\n';

    int n = 2;
    int X = 1000;
    string fileName = "";

    cout << "ulam_sequence(" << n << "," << X << ")\n" << ulam_sequence(n, X);
}

