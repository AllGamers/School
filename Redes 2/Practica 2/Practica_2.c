#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NP 10000
#define PRO 4 // # productores
#define CON 3 // # consumidores
#define NZON 6// # zonas criticas

//Creacion de funciones

void *Productor(void *);
void *Consumidor(void *);
void Almacenar_Consumo(char *);

//Variable Globales
char Zona[18]; 
sem_t s_prod[NZON+1], s_cons[NZON+1]; // Arreglo de Semaforos
sem_t c_prod,c_cons;
sem_t s_archivo[PRO];
int i_prod=0,i_cons=0;
FILE * archivo[PRO];
typedef struct{
  int id;
  char producto[3];
}prod;


int main()
{

    // inicializacion de semaforos
    for (int i = 1; i < NZON+1; i++)
    {
       sem_init(&s_prod[i], 0, 1);
       sem_init(&s_cons[i], 0, 0);
    }

    for(int i=0;i<PRO;i++){
      sem_init(&s_archivo[i],0,1);
    }

    sem_init(&s_prod[0], 0, 6);
    sem_init(&s_cons[0], 0, 0);

    sem_init(&c_cons, 0, 1);
    sem_init(&c_prod, 0, 1);

    // Inicializacion de hilos
    pthread_t h_prod[PRO], h_cons[CON];
    prod productor[PRO];

    // Abrimos archivos
    archivo[0] = fopen ("aaa.txt", "w+");
    archivo[1] = fopen ("bbb.txt", "w+");
    archivo[2] = fopen ("ccc.txt", "w+");
    archivo[3] = fopen ("ddd.txt", "w+");
    // creacion de hilos productores
    for (int i = 0; i < PRO; i++)
    {
      switch (i){
        case 0:
          productor[i].id = 1;
          sprintf(productor[i].producto,"aaa");
          pthread_create(&h_prod[i], NULL, Productor, &productor[i]);
          break;
        case 1:
          productor[i].id = 2;
          sprintf(productor[i].producto,"bbb");
          pthread_create(&h_prod[i], NULL, Productor, &productor[i]);
          break;
        case 2:
          productor[i].id = 3;
          sprintf(productor[i].producto,"ccc");
          pthread_create(&h_prod[i], NULL, Productor, &productor[i]);
          break;
        case 3:
          productor[i].id = 4;
          sprintf(productor[i].producto,"ddd");
          pthread_create(&h_prod[i], NULL, Productor, &productor[i]);
          break;
      }
    }

    // creacion de hilos consumidores
    for (int i = 0; i < CON; i++)
    {
        switch (i){
        case 0:
          pthread_create(&h_cons[i], NULL, Consumidor,(void *) 1);
          break;
        case 1:
          pthread_create(&h_cons[i], NULL, Consumidor,(void *) 2);
          break;
        case 2:
          pthread_create(&h_cons[i], NULL, Consumidor,(void *) 3);
          break;
        }
    }

    // joiners
    for (int i = 0; i < PRO; i++)
    {
        pthread_join(h_prod[i], NULL);
    }

    for (int i = 0; i < CON; i++)
    {
        pthread_join(h_cons[i], NULL);
    }

    //Cerramos Archivos
    fclose(archivo[0]);
    fclose(archivo[1]);
    fclose(archivo[2]);
    fclose(archivo[3]);
    return 0;
}

void *Productor(void *a)
{
  prod *p = (prod *)a;
  int id = p->id;
  char *dato = p->producto;
  int val;
  int i,j,k;
    for ( i = 0; i < NP; i++)
    {
      sem_wait(&s_prod[0]);
      
      for (j = 0, k=0; j < NZON; j++,k+=3)
      {
        sem_getvalue(&s_prod[j+1],&val);
        if (val > 0 )
        {
          sem_wait(&s_prod[j+1]);
          printf("El Productor No. %i produjo %s en la fila %d de la Zona Critica: %d\n",id , dato,j+1,1);
          memcpy(Zona+k,dato,3);
          sem_post(&s_cons[j+1]);
          break; 
        }
      }
      
      sem_post(&s_cons[0]);
    }
    pthread_exit(NULL);
}

void *Consumidor(void *a)
{  
  int id = (int) a;
  int val;
  int j=0,k=0;
  char producto[3];
    while (1)
    {
      sem_wait(&c_cons);
      if(i_cons<NP * PRO){
        i_cons++;
      }else{
        sem_post(&c_cons);
        break;
      }
      sem_wait(&s_cons[0]);   
      for ( j = 0, k=0; j < NZON; j++, k+=3)
      {
        sem_getvalue(&s_cons[j+1],&val);
        if (val > 0 )
        {
          sem_wait(&s_cons[j+1]);
          memcpy(producto,Zona+k,3);
          printf("El Consumidor No. %i consumio %c%c%c en la fila %d de la Zona Critica: %d\n",id , producto[0], producto[1] ,producto[2],j+1,1);
          
          sem_post(&s_prod[j+1]);
          break;
        }
      }
      
      sem_post(&s_prod[0]);
      sem_post(&c_cons);
      Almacenar_Consumo(producto);
    }
    pthread_exit(NULL);
}

void Almacenar_Consumo(char *consumo){
  char aux[4];
  int file;
  if(!strncmp(consumo,"aaa",3))
    file = 0;
  else if(!strncmp(consumo,"bbb",3))
    file = 1;
  else if(!strncmp(consumo,"ccc",3))
    file = 2;
  else if(!strncmp(consumo,"ddd",3))
    file = 3;

  sem_wait(&s_archivo[file]);
    fprintf(archivo[file], "%s\n", consumo);
  sem_post(&s_archivo[file]);
}