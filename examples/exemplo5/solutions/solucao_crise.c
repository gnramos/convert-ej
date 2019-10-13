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

void limpa_Fila(Fila **inicio)
{   
    while(ehVazia_Fila(inicio) == 0)
    {
        desenfileira(inicio);
    }
    *inicio = NULL;
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
    int desliga,i,n,m,mm;
    
    inicio = cria_Fila();
    
    scanf("%d",&n);
       
    for(m = 1; m <= 10000; m++)
    {
        
        for(i = 1; i <=n;i++)
        {
            enfileira(inicio,i);
        }
        
        //printf("\nM = %d\n",m);
        
        while(ehVazia_Fila(inicio) == 0)
        {
            desliga = verFrente(inicio);
            desenfileira(inicio);
            //printf("desliga: %d\n",desliga);
            
            for(mm = 1; mm < m && ehVazia_Fila(inicio)!=1; mm++)
            {
                desliga = verFrente(inicio);
                desenfileira(inicio);
                enfileira(inicio,desliga);
            }        
        }

        if(desliga == 13)
        {
            break;
        }
        else
        {
            limpa_Fila(inicio);
        }
    }
    
    printf("%d\n",m);
    
    libera_Fila(inicio);

    return 0;
}
