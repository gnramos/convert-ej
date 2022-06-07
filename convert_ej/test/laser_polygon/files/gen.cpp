#include "testlib.h"
#include <bits/stdc++.h>

#ifndef DEBUG
#define endl '\n'
#endif

using namespace std;

#define ll long long
#define ld long double

const ld EPS = 1e-8;

typedef ld cod;
bool eq(cod a, cod b){ return abs(a - b) <= EPS; }

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
    return (tmp > EPS) - (tmp < -EPS);
}

point mirror(point m1, point m2, point p){
    // mirror point p around segment m1m2
    point seg = m2-m1;
    ld t0 = ((p-m1)*seg) / (seg*seg);
    point ort = m1 + seg*t0;
    point pm = ort-(p-ort);
    return pm;
}

int main(int argc, char* argv[]) {
    cin.tie(0)->sync_with_stdio(false); // pode colocar isso né?

    registerGen(argc, argv, 1);

    int min_T = atoi(argv[1]);
    int max_T = atoi(argv[2]);
    int min_X = atoi(argv[3]);
    int max_X = atoi(argv[4]);
    int min_Y = atoi(argv[5]);
    int max_Y = atoi(argv[6]);

    int T = rnd.next(min_T, max_T);
    
    cout << T << endl;

    for (int tid = 0; tid < T; tid++) {

        int while_iterations = 0;

        bool found = false;

        point L, A, E1, E2;

        // Encontra aleatoriamente quatro pontos diferentes L, A, E1 e E2
        // com A e L no mesmo semi-plano e não colineares a E1E2.
        // As chances de não encontrar em poucas iterações são baixas, eu acho :)
        while(!found){
            while_iterations++;
            L.x = rnd.next(min_X, max_X);
            L.y = rnd.next(min_Y, max_Y);
            A.x = rnd.next(min_X, max_X);
            A.y = rnd.next(min_Y, max_Y);
            E1.x = rnd.next(min_X, max_X);
            E1.y = rnd.next(min_Y, max_Y);
            E2.x = rnd.next(min_X, max_X);
            E2.y = rnd.next(min_Y, max_Y);

            if(A!=L and E1!=E2 and
               ccw(E1, E2, A) != 0 and
               ccw(E1, E2, L) != 0 and
               ccw(E1, E2, A) == ccw(E1, E2, L))
                found = true;
        }

        ensuref(while_iterations<=100, "While loop took more than 100 iterations");

        cout << L.x << " " << L.y << " " << A.x << " " << A.y << endl;
        cout << E1.x << " " << E1.y << " " << E2.x << " " << E2.y << endl;

    }

    return 0;
}