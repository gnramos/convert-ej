#include "testlib.h"
#include <bits/stdc++.h>

using namespace std;

const int MIN_N = 1;
const int MAX_N = 1e4;
const int MIN_M = 1;
const int MAX_M = 1e4;
const int MIN_EC = 1;
const int MAX_EC = 100;

const int number_of_rnd_tests = 66;

template <typename T> void append(vector<T> &dest, const vector<T> &orig) {
    dest.insert(dest.end(), orig.begin(), orig.end());
}

// Generate sample tests
vector<string> generate_sample_tests(void) {
    vector<string> tests = {"1 1\n3\n6\n",
                            "1 2\n1\n5 3\n",
                            "2 3\n1 2\n10 5 3\n"
    };
    return tests;
}

string random_test(int test_n) {

    int min_n = MIN_N;
    int max_n = MAX_N;
    int min_m = MIN_M;
    int max_m = MAX_M;
    int min_ec = MIN_EC;
    int max_ec= MAX_EC;
    
    if (test_n < number_of_rnd_tests / 3) {
        // Easy
        max_n = 20;
        min_n = 1;
        max_m = 20;
        min_m = 1;
        min_ec = 1;
        max_ec= 20;
    } else if (test_n < 2 * number_of_rnd_tests / 3) {
        // Medium
        max_n = 100;
        min_n = 1;
        max_m = 100;
        min_m = 1;
        min_ec = 1;
        max_ec= 100;
    }
    
    ostringstream oss;
    
    int nvar = rnd.next(min_n, max_n);
    int mvar = rnd.next(min_m,max_m);
    
    oss << nvar << " " << mvar << endl;
    //cout << n << " " << qvar << " " << tvar << endl;
    
    for (int i = 0; i < nvar-1; i++){
        oss << rnd.next(min_ec,max_ec) << " ";
    }
    oss << rnd.next(min_ec,max_ec) << endl;
    
    for (int i = 0; i < mvar-1; i++){
        oss << rnd.next(min_ec,max_ec) << " ";
    }
    oss << rnd.next(min_ec,max_ec) << endl;
    
    return oss.str();
}


string max_test(int test_n) {

    ostringstream oss;
    int max_n = MAX_N;
    int max_m = MAX_M;
    int min_ec = MIN_EC;
    int max_ec= MAX_EC;

    oss << max_n << " " << max_m << endl;
    
    oss << min_ec << " ";
    for (int i = 1; i < max_n-1; i++){
        oss << rnd.next(min_ec,max_ec) << " ";
    }
    oss << max_ec << endl;
    
    oss << min_ec << " ";
    for (int i = 1; i < max_m-1; i++){
        oss << rnd.next(min_ec,max_ec) << " ";
    }
    oss << max_ec << endl;
    
    return oss.str();
}


string min_test(int test_n) {

    ostringstream oss;
    /*
    int n = 1;
    int m =1;
    int min_n = 1;
    int max_n = 1;
    int qvar = 1;
    int min_tt = MIN_T;
    int max_tt = MAX_T;
    int tvar = rnd.next(min_tt,max_tt);
    int max_x = MAX_X;
    int min_x = MIN_X;
    int min_r = MIN_R;

    oss << n << " " << qvar << " " << tvar << endl;
    
    for (int i = 0; i < qvar; i++){
        int r = rnd.next(min_r,n);
        int l = rnd.next(1,r);
        oss << l << " " << r << " " << rnd.next(1,tvar/2) << endl;
    }*/
    
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
    v.push_back(max_test(69));
    return v;
}

vector<string> generate_min_test() {
    vector<string> v;
    v.push_back(min_test(70));
    return v;
}

int main(int argc, char *argv[]) {
    
    registerGen(argc, argv, 1);
    vector<string> tests;
    size_t test = 0;
    append(tests, generate_sample_tests());
    append(tests, generate_random_tests());
    append(tests, generate_max_test());
    //append(tests, generate_min_test());

    for (const auto &t : tests) {
        startTest(++test);
        cout << t;
    }
    
    return 0;
}
