#include "testlib.h"
#include <bits/stdc++.h>

using namespace std;

const int MIN_N = 0;
const int MAX_N = 2147483647;


const int number_of_rnd_tests = 0;

template <typename T> void append(vector<T> &dest, const vector<T> &orig) {
    dest.insert(dest.end(), orig.begin(), orig.end());
}

// Generate sample tests
vector<string> generate_sample_tests(void) {
    vector<string> tests = {"a+b\n","a*2+b\n","b/(c+1)\n","(a+b)/(c-3)\n","(a*2+c-d)/2\n","(2*4/a^b)/(2*c)\n","a*b-c*d^e/f+g*h\n","a*(b+c)*(d-g)*h\n","a+b*c^d-e\n","(a+b)*c/(2-r)/2\n","(a*(b+3*(w-7/(a+b))))\n","(((t^2*a/b)-e)*2)+3-r\n","t^3^5^7^c+p\n","a*(2+3)\n","b*(2/3+1)\n","(2*(4/a)^b*1+2*(3+5))/(2*(c-3))\n","((b+2)^3)/4^4*(3+1)\n","(a)\n","(a+1)\n","b*(1)\n","6+4/b^3\n","a+b*a/d-u/b\n","(a+2)^5-(b*c)/6+(a+2)^5-(b*c)/6-(a+2)^5-(b*c)/6+(a+2)^5-(b*c)/6+(2/3+x+1)\n","a-b/c^d-e-f-g^h*i/j*k^l/m*n^o*p+q*r+s+t+u^v*w/x+y+z\n","a-b^c/d+e-f^g^h-i+j+k+l*m*n^o*p^q/r+s/t^u^v/w-x-y/z\n","a/b-c*d/e*f/g+h+i-j+k/l/m-n^o^p^q^r+s+t/u*v+w/x*y+z\n","((a+b)*4-(1-e))^(f-g)\n","((a+t)*((b+(a+c))^(c+d)))\n","a^b+c^d+e*f-g^h-i+j-k/l*m^n+o+p+q+r+s/t/u/v-w*x^y/z\n","(a*b+1)/(d+c*7)^(a-2+1+t*(a+b))+6-i^2^(t+3)-a*(c+d/2)\n"};
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

    oss << "(" <<  endl;
    
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
    //append(tests, generate_random_tests());
    //append(tests, generate_max_test());
    //append(tests, generate_min_test());

    for (const auto &t : tests) {
        startTest(++test);
        cout << t;
    }
    
    return 0;
}
