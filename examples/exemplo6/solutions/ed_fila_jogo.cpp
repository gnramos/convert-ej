#include<bits/stdc++.h>

using namespace std;

int main()
{
    int n,m,num;
    queue<int> fila;

    scanf("%d %d",&n,&m);

    for(int i =1; i <= n; i++)
    {
        fila.push(i);
    }

    for(int s = 1; s <= m; s++)
    {
        scanf("%d",&num);
        if(num > 0)
        {
            while(num)
            {
                int elem = fila.front();
                fila.pop();
                fila.push(elem);
                num--;
            }
        }
        else
        {
            fila.pop();
        }
    }
    
    printf("%d\n",fila.front());

    return 0;
}
