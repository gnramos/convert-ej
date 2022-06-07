#include <bits/stdc++.h>
#define ll long long

using namespace std;

typedef ll cod;

struct point{
    // struct de ponto
    cod x, y;
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
};

cod escalar(point a, point b){
    // produto escalar
    return a.x*b.x + a.y*b.y;
}

cod vetorial(point a, point b){
    // produto vetorial
    return a.x*b.y - a.y*b.x;
}

cod norm(point a){
    // módulo ao quadrado
    return a.x*a.x + a.y*a.y;
}

point mirror(point m1, point m2, point p){
    // espelha o ponto p em relação ao segmento m1m2
    point e = m2-m1;
    ll t0 = (escalar((p-m1), e));
    point proj = m1*norm(e) + e*t0;
    point ort = p*norm(e)-proj;
    point pm = proj - ort;
    return pm;
}

int esq(point a, point b, point e){
    // -1=direita // 0=colinear // 1=esquerda
    cod tmp = vetorial((b-a), (e-a));
    if(tmp > 0) return 1;
    if(tmp < 0) return -1;
    return 0; // if tmp == 0
}

int main()
{
    int T;
    cin >> T;
    while(T--){
        point L, A;
        point E1, E2;

        cin >> L.x >> L.y >> A.x >> A.y;
        cin >> E1.x >> E1.y >> E2.x >> E2.y;

        ll scale = norm(E1-E2);

        point Am = mirror(E1, E2, A);

        L = L * scale;
        E1 = E1 * scale;
        E2 = E2 * scale;

        if(esq(L, E1, Am) == esq(L, E2, Am))
            cout << "Leo, eu estou te vendo..." << endl;
        else
            cout << "De onde veio isso?" << endl;        
    }

    return 0;
}