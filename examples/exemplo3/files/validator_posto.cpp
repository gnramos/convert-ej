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

int main(int argc, char* argv[]) {
    
    registerValidation(argc, argv);
    int n,f,p,a;
    n = inf.readInt(MIN_N,MAX_N,"N");
    inf.readSpace();
    f = inf.readInt(MIN_F,MAX_F,"F");
    inf.readSpace();
    p = inf.readInt(MIN_P,MAX_P,"P");
    inf.readEoln();
    for(int i = 1; i < n; i++)
    {
        a = inf.readInt(MIN_A,MAX_A,"A");
        inf.readSpace();
    }
    a = inf.readInt(MIN_A,MAX_A,"A");
    inf.readEoln();
    inf.readEof();
    return 0;
}
