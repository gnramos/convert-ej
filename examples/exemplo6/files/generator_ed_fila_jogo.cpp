#include "testlib.h"
#include <bits/stdc++.h>

using namespace std;

const int MIN_N = 2;
const int MAX_N = 1e3;
const int MIN_M = 1;
const int MAX_M = 1e3-1;

const int number_of_rnd_tests = 45;

template <typename T> void append(vector<T> &dest, const vector<T> &orig) {
    dest.insert(dest.end(), orig.begin(), orig.end());
}

// Generate sample tests
vector<string> generate_sample_tests(void) {
    vector<string> tests = {"6 2\n2 2\n",
                            "6 4\n3 -1 -1 -1\n",
                            "5 3\n1 2 3\n"
    };
    return tests;
}

string random_test(int test_n) {

    int min_n = MIN_N;
    int max_n = MAX_N;
    int max_m = MAX_M;
    int min_m = MIN_M;
    int s;
    if (test_n < number_of_rnd_tests / 3) {
        // Easy
        max_n = 30;
        min_n = 2;
        
    } else if (test_n < 2 * number_of_rnd_tests / 3) {
        // Medium
        max_n = 400;
        min_n = 40;
    }
    
    ostringstream oss;
    
    int n = rnd.next(min_n, max_n);
    int m = rnd.next(min_m,n-1);
    
    oss << n << " " << m << endl;
    
    for (int i = 0; i < m-1; i++){
        
        s = rnd.next(-n,n);
        while(s==0)
            s = rnd.next(-n,n);
        
        if(s<=0)
            s=-1;
        
        oss << s << " " ;
        //cout << l << " " << r << " " << v << endl;
    }
    
    s = rnd.next(-n,n);
    while(s==0)
        s = rnd.next(-n,n);
    
    if(s<=0)
            s=-1;
    
    oss << s << endl;
    return oss.str();
}


string max_test(int test_n) {

    ostringstream oss;
    
    int n = MAX_N;
    int m = MAX_M;
    int s;
    
    oss << n << " " << m << endl;
    
    for (int i = 0; i < m-1; i++){
        
        s = rnd.next(-n,n);
        while(s==0)
            s = rnd.next(-n,n);
        
        if(s<=0)
            s=-1;
        
        oss << s << " " ;
        //cout << l << " " << r << " " << v << endl;
    }
    
    s = rnd.next(-n,n);
    while(s==0)
        s = rnd.next(-n,n);
    
    if(s<=0)
            s=-1;
        
    oss << s << endl;
    
    return oss.str();
}

string min_test(int test_n) {

    ostringstream oss;
    int n = 2;
    int m = 1;
    
    oss << n << " " << m << endl;
    oss << "1" << endl ;
    
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
    v.push_back(max_test(49));
    return v;
}

vector<string> generate_min_test() {
    vector<string> v;
    v.push_back(min_test(50));
    return v;
}

int main(int argc, char *argv[]) {
    
    registerGen(argc, argv, 1);
    vector<string> tests;
    size_t test = 0;
    append(tests, generate_sample_tests());
    append(tests, generate_min_test());
    append(tests, generate_random_tests());
    append(tests, generate_max_test());

    for (const auto &t : tests) {
        startTest(++test);
        cout << t;
    }
    
    return 0;
}
