#include "testlib.h"
#include <bits/stdc++.h>

using namespace std;

const int MIN_N = 2;
const int MAX_N = 1e3;
const int MIN_M = 1;
const int MAX_M = 1e3-1;


int main(int argc, char* argv[]) {
    
    registerValidation(argc, argv);
    int n,m,s;
    n = inf.readInt(MIN_N,MAX_N,"N");
    inf.readSpace();
    m = inf.readInt(MIN_M,MAX_M,"M");
    inf.readEoln();
    
    for(int i=0;i<m-1;i++){
        s = inf.readInt(-n,n,"s");
        inf.readSpace();
    }
    s = inf.readInt(-n,n,"s");
    inf.readEoln();
    
    inf.readEof();
    return 0;
}
