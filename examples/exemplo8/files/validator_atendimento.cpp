#include "testlib.h"
#include <bits/stdc++.h>

using namespace std;

const int MIN_N = 1;
const int MAX_N = 1e4;
const int MIN_M = 1;
const int MAX_M = 1e4;
const int MIN_EC = 1;
const int MAX_EC = 100;


int main(int argc, char* argv[]) {
    registerValidation(argc, argv);
    int n,m;
    n = inf.readInt(MIN_N,MAX_N,"N");
    inf.readSpace();
    m = inf.readInt(MIN_M,MAX_M,"M");
    inf.readEoln();

    for(int i=0;i<n;i++){
        inf.readInt(MIN_EC,MAX_EC,"v[i]");
        if(i<n-1){
            inf.readSpace();
        }
    }
    inf.readEoln();

    for(int i=0;i<m;i++){
        inf.readInt(MIN_EC,MAX_EC,"c[j]");
        if(i<m-1){
            inf.readSpace();
        }
    }
    inf.readEoln();
    inf.readEof();
    return 0;
}
