#include "testlib.h"
#include <bits/stdc++.h>
using namespace std;

typedef long long cod;
bool eq(cod a, cod b){ return (a==b); }

struct point{
    cod x, y;
    int id;
    point(cod x=0, cod y=0): x(x), y(y){}


    point operator+(const point &o) const{
        return {x+o.x, y+o.y};
    }
    point operator-(const point &o) const{
        return {x-o.x, y-o.y};
    }
    point operator*(cod t) const{
        return {x*t, y*t};
    }
    point operator/(cod t) const{
        return {x/t, y/t};
    }
    cod operator*(const point &o) const{ // dot
        return x * o.x + y * o.y;
    }
    cod operator^(const point &o) const{ // cross
        return x * o.y - y * o.x;
    }
    bool operator<(const point &o) const{
        if(!eq(x, o.x)) return x < o.x;
        return y < o.y;
    }
    bool operator==(const point &o) const{
        return eq(x, o.x) and eq(y, o.y);
    }
    bool operator!=(const point &o) const{
        return !eq(x, o.x) or !eq(y, o.y);
    }

};

int ccw(point a, point b, point e){ //-1=dir; 0=collinear; 1=esq;
    cod tmp = (b-a)^(e-a); // from a to b
    if(tmp > 0) return 1;
    if(tmp < 0) return -1;
    return 0; // if tmp == 0
}

const int MIN_T = 1;
const int MAX_T = 1e4;
const int MIN_X = -500;
const int MAX_X = 500;
const int MIN_Y = -500;
const int MAX_Y = 500;

int main(int argc, char* argv[]) {

    registerValidation(argc, argv);

    int T = inf.readInt(MIN_T, MAX_T, "T");
    inf.readEoln();

    for (int tid = 0; tid < T; tid++) {
        point L, A, E1, E2;

        L.x = inf.readInt(MIN_X, MAX_X, "L.x");
        inf.readSpace();
        L.y = inf.readInt(MIN_Y, MAX_Y, "L.y");
        inf.readSpace();

        A.x = inf.readInt(MIN_X, MAX_X, "A.x");
        inf.readSpace();
        A.y = inf.readInt(MIN_Y, MAX_Y, "A.y");
        inf.readEoln();

        E1.x = inf.readInt(MIN_X, MAX_X, "E1.x");
        inf.readSpace();
        E1.y = inf.readInt(MIN_Y, MAX_Y, "E1.y");
        inf.readSpace();

        E2.x = inf.readInt(MIN_X, MAX_X, "E2.x");
        inf.readSpace();
        E2.y = inf.readInt(MIN_Y, MAX_Y, "E2.y");
        inf.readEoln();

        ensuref(L!=A && L!=E1 && L!=E2 && A!=E1 && A!=E2 && E1!=E2,
                "Points are not pairwise different");
        ensuref(ccw(E1, E2, L) != 0 && ccw(E1, E2, A) != 0,
                "Points are collinear with the mirror segment");
        ensuref(ccw(E1, E2, L) == ccw(E1, E2, A),
                "Points are in the same half-plane");
    }

    inf.readEof();

    return 0;
}