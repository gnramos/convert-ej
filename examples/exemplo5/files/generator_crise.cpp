#include "testlib.h"
#include <bits/stdc++.h>

using namespace std;

const int MIN_N = 1;
const int MAX_N = 100;

const int number_of_rnd_tests = 100;

template <typename T> void append(vector<T> &dest, const vector<T> &orig) {
    dest.insert(dest.end(), orig.begin(), orig.end());
}

// Generate sample tests
vector<string> generate_sample_tests(void) {
    vector<string> tests = {"13\n",
                            "17\n",
                            "70\n"
    };
    return tests;
}

string random_test(int test_n) {
    
    ostringstream oss;
    
    oss << test_n << endl;
    
    return oss.str();
}



vector<string> generate_random_tests() {
    vector<string> v;
    for (int i = 13; i <= number_of_rnd_tests; i++) {
        v.push_back(random_test(i));
    }
    return v;
}


int main(int argc, char *argv[]) {
    
    registerGen(argc, argv, 1);
    vector<string> tests;
    size_t test = 0;
    //append(tests, generate_sample_tests());
    //append(tests, generate_min_test());
    append(tests, generate_random_tests());
    //append(tests, generate_max_test());

    for (const auto &t : tests) {
        startTest(++test);
        cout << t;
    }
    
    return 0;
}
