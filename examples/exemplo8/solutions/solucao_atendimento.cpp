#include<bits/stdc++.h>
#define pii pair<int,int>
using namespace std;

int main()
{
    int n,m,total,aux,client,atend;
    queue<int> pq;
    //priority_queue<pii> cashiers;
    priority_queue<pii, vector<pii>, greater<pii> > cashiers; 
    pii cashier;
    vector<int> tempcash;

    scanf("%d %d",&n,&m);
    
    for(int i = 0; i < n;i++)
    {
        scanf("%d",&aux);
        cashiers.push(make_pair(0,i));
        tempcash.push_back(aux);
    }
    
    for(int i =0; i < m; i++)
    {
        scanf("%d",&client);
        pq.push(client);
    }
    
    total = 0;
    
    while(pq.size())
    {
        client = pq.front();
        pq.pop();
        
        cashier = cashiers.top();
        cashiers.pop();
        
        atend = client*tempcash[cashier.second];
        
        total = max(total,cashier.first + atend);
        
        cashiers.push(make_pair(cashier.first + atend,cashier.second));
    }

    printf("%d\n",total);
    return 0;
}
