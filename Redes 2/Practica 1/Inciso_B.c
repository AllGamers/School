#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <sys/time.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>

//Funciones uwu

void * trabajoHilo(void *arh);
int verificacionArgumentos(int argc,char **argv);
void asignarMemoria(int *matriz[], int n_filas, int n_columnas);
void creacionMatriz(int *matriz[], int n_filas, int n_columnas);
void imprimirMatriz(int *matriz[], int n_filas, int n_columnas);
void liberarMatriz(int *matriz[], int n_filas, int n_columnas);

//Variable compartida
int **mA,**mB,**mR;

//Estructura
typedef struct{
  int inicio;
  int fin;
  int n_c1;
  int n_c2;
}op_hilos;

int main(int argc, char *argv[]) {
  srand(time(NULL));
  
  if(!verificacionArgumentos(argc,argv)){
    printf("Ejecucion mal lograda.\n");
    return 0;
  }

  int filas_1=atoi(argv[1]), columnas_1=atoi(argv[2]);
  int filas_2=atoi(argv[3]), columnas_2=atoi(argv[4]);
  int n_hilos=atoi(argv[5]);
  int *m1[filas_1], *m2[filas_2], *mF[filas_1];
  int rango = filas_1/n_hilos;
  int sobrante = filas_1%n_hilos;
  int fin=rango;
  int inicio=0;
  pthread_t hilos[n_hilos];
  op_hilos job[n_hilos];
  int err;

  asignarMemoria(m1,filas_1,columnas_1);
  asignarMemoria(m2,filas_2,columnas_2);
  
  creacionMatriz(m1,filas_1,columnas_1);
  creacionMatriz(m2,filas_2,columnas_2);

  printf("Matriz 1:\n");
  imprimirMatriz(m1,filas_1,columnas_1);

  printf("Matriz 2:\n");
  imprimirMatriz(m2,filas_2,columnas_2);

  mA=m1;
  mB=m2;
  
  asignarMemoria(mF,filas_1,columnas_2);  
  mR=mF;
  for(int i=0;i<n_hilos;i++){
    if(i==n_hilos-1){
      job[i].inicio=inicio;
      job[i].fin=fin+sobrante;
      job[i].n_c1=columnas_1;
      job[i].n_c2=columnas_2;
      err = pthread_create(&hilos[i], NULL, trabajoHilo,&job[i]);
    }else{
      job[i].inicio=inicio;
      job[i].fin=fin;
      job[i].n_c1=columnas_1;
      job[i].n_c2=columnas_2;
      err = pthread_create(&hilos[i], NULL, trabajoHilo,&job[i]);
    }
    if (err != 0){
      printf ("can't create thread: %s\n", strerror(err));
    }
    inicio += rango;
		fin += rango;
  }

  for(int i=0;i<n_hilos;i++){
    err = pthread_join(hilos[i], NULL);
    if (err != 0){
      printf ("can't create thread: %s\n", strerror(err));
    }
  }
  
  printf("Matriz Resultante:\n");
  imprimirMatriz(mR,filas_1,columnas_2);
  
  //printf("1.- %i %i\n",filas_1,columnas_1);
  liberarMatriz(m1,filas_1,columnas_1);

  //printf("2.- %i %i\n",filas_2,columnas_2);
  liberarMatriz(m2,filas_2,columnas_2);

  //printf("3.-%i %i\n",filas_1,columnas_2);
  liberarMatriz(mF,filas_1,columnas_2);
  return 0;
}

void * trabajoHilo(void *arg){
  op_hilos *aux = (op_hilos *)arg;
  int c1 = aux->n_c1;
  int c2 = aux->n_c2;
  int inicio = aux->inicio;
  int fin = aux->fin;
  int i, j, n, val;
	for( i = inicio ; i < fin ; i++ ){
		for( n = 0 ; n < c2 ; n++ ){
			val = 0;
			for( j = 0 ; j < c1 ; j++ ){
        val += mA[i][j] * mB[j][n];
      }
		  mR[i][n] = val;
		}
	}
  pthread_exit(NULL);
}

int verificacionArgumentos(int argc, char **argv){
  if(argc!=6){
    printf("Ejecucion con parametros inexactos no_filas_m1, no_columnas_m1, " 
    "no_filas_m2, no_columnas_m2, no_hilos\n");
    return 0;
  }
  if(atoi(argv[2])!=atoi(argv[3])){
    printf("Las matrices no cumplen con el tamanio adecuado no_columnas_m1 = no_filas_m2\n");
    return 0;
  }
  if(atoi(argv[1])<atoi(argv[5])){
    printf("De momento no podemos permitir que el numero de hilos supere el numero de filas\n");
    return 0;
  }
  return 1;
}

void asignarMemoria(int *matriz[], int n_filas, int n_columnas){
  int i;
  for(int i=0; i<n_filas; i++){
    matriz[i]=(int *)malloc (sizeof(int)*n_columnas);
  }
}

void creacionMatriz(int *matriz[], int n_filas, int n_columnas){
  for(int i=0;i<n_filas;i++){
    for(int j=0;j<n_columnas;j++){
      matriz[i][j]=(rand() % 5)+1;
    }
  }
}

void imprimirMatriz(int *matriz[], int n_filas, int n_columnas){
  for(int i=0;i<n_filas;i++){
    for(int j=0;j<n_columnas;j++){
      printf(" %i ",matriz[i][j]);
    }
    printf("\n");
  }
}

void liberarMatriz(int *matriz[], int n_filas, int n_columnas){
  for(int i=0; i<n_filas; i++){
    free(matriz[i]);
  }
}