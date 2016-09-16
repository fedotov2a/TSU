#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <pthread.h>

#define NUM_THREADS     4

#define SIZE_ARRAY      20
#define LOWER_BOUND     0
#define UPPER_BOUND     10

int bigArray[SIZE_ARRAY];

pthread_t threads[NUM_THREADS];
int          sumT[NUM_THREADS];
int          minT[NUM_THREADS];
int          maxT[NUM_THREADS];

void init();

void sum_(int* array, int size);
void min_();
void max_();

void printArray(int* array, int size);
void fillArrayRandomNumbers(int* array, int size);

void createThreads();
void waitAllThreads();

void* parallelSum(void* idThread);
void* parallelMin(void* idThread);
void* parallelMax(void* idThread);

typedef void *(*func) (void* attr);