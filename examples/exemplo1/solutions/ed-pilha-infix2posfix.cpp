#include<bits/stdc++.h>

using namespace std;

map<char,int> op;

void prioridade()
{
	op['+']=1;
	op['-']=1;
	op['/']=2;
	op['*']=2;
	op['^']=3;
}

void convertInfixa2PosFixa(char exp[])
{
    stack<char> pilha;

    for(int i=0; exp[i] != '\0';i++)
    {
        if((exp[i] >= 'a' && exp[i] <= 'z') || (exp[i] >= '0' && exp[i] <= '9'))
        {
            printf("%c",exp[i]);
        }
        else
        {
            if(exp[i] == '+' || exp[i]== '-' || exp[i]== '*' || exp[i]== '/' || exp[i]== '^')
            {
                if(!pilha.empty())
                {
                    while(op[exp[i]] <= op[pilha.top()])
                    {
                        printf("%c",(char) pilha.top());
                        
                        pilha.pop();
                        
                        if(pilha.empty())
                            break;
                    }
                }
		pilha.push(exp[i]);
            }
            else
            {
                if(exp[i]=='(')
                {
                    pilha.push('(');
                }
                else
                {
                    if(exp[i]==')')
                    {
                        while(pilha.top()!='(')
                        {
                            printf("%c",(char) pilha.top());
                            pilha.pop();
                        }
                        pilha.pop();
                    }
                }
            }
        }
    }
    
    while(!pilha.empty())
    {
        printf("%c",(char) pilha.top());
        pilha.pop();
    }

    printf("\n");
}

int main()
{
    
    prioridade();

    char exp[101];
    
    scanf("%s",exp);

    convertInfixa2PosFixa(exp);

    return 0;
}
