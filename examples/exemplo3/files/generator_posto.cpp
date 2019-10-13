#include "testlib.h"
#include <bits/stdc++.h>

using namespace std;

const int MIN_N = 1;
const int MAX_N = 10000;
const int MIN_F = 1;
const int MAX_F = 100;
const int MIN_P = 1;
const int MAX_P = 1000;
const int MIN_A = 1;
const int MAX_A = 1000;

const int number_of_rnd_tests = 62;

template <typename T> void append(vector<T> &dest, const vector<T> &orig) {
    dest.insert(dest.end(), orig.begin(), orig.end());
}

// Generate sample tests
vector<string> generate_sample_tests(void) {
    vector<string> tests = {"5 1 7\n4 2 6 3 9\n",
                            "2 1 5\n7 4\n",
                            "4 2 8\n2 6 1 3\n",
                            "5 1 10\n4 12 8 13 10\n"
    };
    return tests;
}

string random_test(int test_n) {

    int min_n = MIN_N;
    int max_n = MAX_N;
    int min_f = MIN_F;
    int max_f = MAX_F;
    int min_p = MIN_P;
    int max_p = MAX_P;
    int min_a = MIN_A;
    int max_a = MAX_A;
    int a;

    if (test_n < number_of_rnd_tests / 3) {
        // Easy
        max_n = 30;
        max_f = 5;
        max_p = 20;
        max_a = 50;
        
    } else if (test_n < 2 * number_of_rnd_tests / 3) {
        // Medium
        max_n = 200;
        max_f = 20;
        max_p = 140;
        max_a = 200;
    }
    
    ostringstream oss;
    
    int n = rnd.next(min_n, max_n);
    int f = rnd.next(min_f, max_f);
    int p = rnd.next(min_p, max_p);
    
    oss << n << " " << f << " " << p << endl;
    
    for(int i = 1; i < n; i++)
    {
        a = rnd.next(min_a,max_a);
        oss << a <<  " ";
    }
    
    a = rnd.next(min_a,max_a);
    oss << a <<  endl;

    return oss.str();
}

string max_test1(int test_n) {

    ostringstream oss;
    
    int n = MAX_N;
    int min_a = MIN_A;
    int max_a = MAX_A;
    int min_f = MIN_F;
    int max_f = MAX_F;
    int min_p = MIN_P;
    int max_p = MAX_P;
    int a;

    int p = rnd.next(min_p,max_p);
    int f = rnd.next(min_f, max_f);
    
    oss << n << " " << f << " " << p << endl;
    
    for(int i = 1; i < n; i++)
    {
        a = rnd.next(min_a,max_a);
        oss << a <<  " ";
    }
    
    a = rnd.next(min_a,max_a);
    oss << a <<  endl;
    
    return oss.str();
}


string max_test2(int test_n) {

    ostringstream oss;
    
    int min_p = MIN_P;
    int max_p = MAX_P;
    
    int a;
    int n = MAX_N;
    int f = MAX_F;
    int p = rnd.next(min_p,max_p);
    int min_a = p-2;
    int max_a = MAX_A;
    
    oss << n << " " << f << " " << p << endl;
    
    for(int i = 1; i < n-1; i++)
    {
        a = rnd.next(min_a,max_a);
        oss << a <<  " ";
    }
    
    a = MAX_A;
    oss << a << " ";
    
    a = MIN_A;
    oss << a <<  endl;
    
    return oss.str();
}


string min_test(int test_n) {

    ostringstream oss;
    
    oss << "1 1 1" << endl << "1" << endl;
    
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
    v.push_back(max_test1(67));
    v.push_back(max_test2(68));
    return v;
}

vector<string> generate_min_test() {
    vector<string> v;
    v.push_back(min_test(69));
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
