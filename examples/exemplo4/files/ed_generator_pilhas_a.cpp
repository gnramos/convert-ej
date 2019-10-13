#include "testlib.h"
#include <bits/stdc++.h>

using namespace std;

const int MIN_N = 0;
const int MAX_N = 2147483647;


const int number_of_rnd_tests = 99;

template <typename T> void append(vector<T> &dest, const vector<T> &orig) {
    dest.insert(dest.end(), orig.begin(), orig.end());
}

// Generate sample tests
vector<string> generate_sample_tests(void) {
    vector<string> tests = {"2\n","6\n","13\n"};
    return tests;
}

string random_test(int test_n) {

    int min_n = MIN_N;
    int max_n = MAX_N;
    
    if (test_n < number_of_rnd_tests / 3) {
        // Easy
        max_n = 1000;
        min_n = 16;
    } else if (test_n < 2 * number_of_rnd_tests / 3) {
        // Medium
        max_n = 20000;
        min_n = 2000;
    }
    
    ostringstream oss;
    
    int nvar = rnd.next(min_n, max_n);
    
    oss << nvar << endl;
    
    return oss.str();
}


string max_test(int test_n) {

    ostringstream oss;
    int max_n = MAX_N;

    oss << max_n <<  endl;
    
    return oss.str();
}

string min_test(int test_n) {

    ostringstream oss;
    int min_n = MIN_N;

    oss << min_n <<  endl;
    
    return oss.str();
}


vector<string> generate_random_tests() {
    vector<string> v;
    for (int i = 0; i < number_of_rnd_tests; i++) {
        v.push_back(random_test(i));
    }
    return v;
}

vector<string> generate_max_test() {
    vector<string> v;
    v.push_back(max_test(104));
    return v;
}

vector<string> generate_min_test() {
    vector<string> v;
    v.push_back(min_test(103));
    return v;
}

int main(int argc, char *argv[]) {
    
    registerGen(argc, argv, 1);
    vector<string> tests;
    size_t test = 0;
    append(tests, generate_sample_tests());
    append(tests, generate_random_tests());
    append(tests, generate_max_test());
    append(tests, generate_min_test());

    for (const auto &t : tests) {
        startTest(++test);
        cout << t;
    }
    
    return 0;
}
