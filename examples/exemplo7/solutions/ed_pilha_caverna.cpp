#include <bits/stdc++.h>

using namespace std;

int main()
{
    stack<char> pilha;
    char str[201];
    int objs;

    scanf("%s",str);
    
    objs=0;
    for(int i =0; str[i] !='\0'; i++)
    {
        if(str[i] == '(')
        {
            pilha.push(str[i]);
        }
        if(str[i] == '*')
        {
            if(pilha.size() > 0)
                pilha.push(str[i]);
        }
        if(str[i] == ')')
        {
            while(pilha.size() && pilha.top() != '(')
            {
                objs++;
                pilha.pop();
            }
            if(pilha.size())
                pilha.pop();
        }
    }

    printf("%d\n",objs);
    return 0;
}
