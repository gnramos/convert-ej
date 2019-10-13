#include<stdio.h>
#include<stdlib.h>

struct node{
    int value;
    struct node *prox;
};

typedef struct node Pilha;

int ehVazia_Pilha(Pilha **topo)
{
    if(*topo == NULL)
        return 1;
    return 0;
}

int verTopo_Pilha(Pilha **topo, int *elem)
{
    if(ehVazia_Pilha(topo))
        return 0;
    
    *elem = (*topo)->value;
    return 1;
}

int empilha(Pilha **topo, int elem)
{
    Pilha *node;

    node = (Pilha *)malloc(sizeof(Pilha));
    node->value = elem;
    node->prox = *topo;
    *topo = node;
    return 1;
}

int desempilha(Pilha **topo)
{
    Pilha *aux;

    if(ehVazia_Pilha(topo))
        return 0;

    aux = *topo;
    *topo = (*topo)->prox;
    free(aux);

    return 1;
}

void limpa_Pilha(Pilha **topo)
{
    Pilha *aux;
    
    while(*topo != NULL)
    {
        aux = *topo;
        *topo = (*topo)->prox;
        free(aux);
        aux = NULL;
    }
}

void libera_Pilha(Pilha **topo)
{
    Pilha *aux;
    
    while(*topo != NULL)
    {
        aux = *topo;
        *topo = (*topo)->prox;
        free(aux);
        aux = NULL;
    }
    free(topo);
}

int main()
{
    Pilha **topo;
    int bin,dec,res;
    
    topo = (Pilha **) malloc (sizeof(Pilha *));
    *topo = NULL;

    scanf("%d",&dec);
    
    if(dec == 0)
        printf("0\n");
    else
    {
        while(dec>0)
        {
            res = dec%2;
            dec = dec/2;
            empilha(topo,res);
        }
        
        while(!ehVazia_Pilha(topo))
        {
            verTopo_Pilha(topo,&bin);
            printf("%d",bin);
            desempilha(topo);
        }
    }
    
    libera_Pilha(topo);

    return 0;
}

