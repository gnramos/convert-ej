/* Universidade de Brasilia (UnB)
   Departamento de Ciencia da Computacao (CIC)
   116319 - Estruturas de Dados
   Prof. Dr. Vinicius R. P. Borges
   Data: 30/05/2019 
   
   
   Template de TAD Fila para resolver problemas em Juizes On-line 
   
   Para compilar:
       gcc template_fila.c -o binario
       
   Para executar:
       ./binario
       
   Obs.: para verificar possiveis vazamentos de memoria, digite na linha de comando:
   
        valgrind --leak-check=full ./binario
*/

#include<stdio.h>
#include<stdlib.h>

struct node
{
    int elem;
    struct node *prox;
};

typedef struct node Fila;

Fila** cria_Fila()
{
    Fila **nova;
    
    nova = (Fila **) malloc (sizeof(Fila *));

    *nova = NULL;

    return nova;
}

int ehVazia_Fila(Fila **inicio)
{
    if(*inicio == NULL)
        return 1;
    return 0;
}

int desenfileira(Fila **inicio)
{
    Fila *aux;
    
    if(ehVazia_Fila(inicio) == 1)
    {
        return 0;
    }
    else
    {
        aux = *inicio;
        *inicio = (*inicio)->prox;
        free(aux);
    }
    return 1;
}

int enfileira(Fila **inicio, int valor)
{
    Fila *nodo,*aux;

    nodo = (Fila *) malloc(sizeof(Fila));
    nodo->elem = valor;
    nodo->prox = NULL;
    
    if(ehVazia_Fila(inicio) == 1)
    {
        *inicio = nodo;
    }
    else
    {
        aux = *inicio;
        while(aux->prox != NULL)
        {
            aux = aux->prox;
        }
        aux->prox = nodo;
    }
    return 1;
}

void libera_Fila(Fila **inicio)
{   
    while(ehVazia_Fila(inicio) == 0)
    {
        desenfileira(inicio);
    }
    free(inicio);
    inicio = NULL;
}

int verFrente(Fila **inicio)
{
    Fila *aux = *inicio;
    
    if(*inicio)
        return aux->elem;
    return -1;
}

int main()
{
    Fila **inicio;
    int n,elemento,fator,pesoLim,tempo,m;
    
    inicio = cria_Fila();
    
    scanf("%d %d %d",&n,&fator,&pesoLim);
    
    for(int i =0; i < n; i++)
    {
        scanf("%d",&elemento);
        enfileira(inicio,elemento);
    }
    
    tempo = 0;
    
    while(!ehVazia_Fila(inicio))
    {
        elemento = verFrente(inicio);
        desenfileira(inicio);
        if(elemento > pesoLim)
        {
            enfileira(inicio,elemento-2);
            tempo = tempo + 10;
        }
        else
        {
            tempo = tempo + 5;
        }
        m = 1;
        while(m < fator)
        {
            if(!ehVazia_Fila(inicio))
            {
                desenfileira(inicio);
                tempo++;
            }
            m++;
        }
    }
    
    printf("%d\n",tempo);
    
    libera_Fila(inicio);

    return 0;
}
