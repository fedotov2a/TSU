#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define NUM_THREADS     4
#define SIZE            100000

pthread_t threads[NUM_THREADS];

int countPoint[NUM_THREADS];

double x[SIZE];
double y[SIZE];

void init() {
    for (int i = 0; i < NUM_THREADS; i++) {
        countPoint[i] = 0;
    }
}

/*
    generate double numbers from segment [0, ub)
*/
void generateRandom(double* array, int size, int ub) {
    sleep(1);
    srand(time(NULL));

    for (int i = 0; i < size; i++) {
        array[i] = (double) rand() / (double) RAND_MAX * (double) ub;
    }
}

int isInsideArea(double x, double y) {
    if ( (double)y - (4.0 / (1.0 + (double)x*x)) <= 0.0 ) {     // y = 4 / (1+x^2)  | x: [0, 1], y: [0, 4]
    // if ( x*x + y*y - 1.0 <= 0.0 ) {                          // x^2 + y^2 = 1    | x: [0, 1], y: [0, 1]
        return 1;
    }
    return 0;
}

double integrate(double* x, double* y) {
    int k = 0;
    for (int i = 0; i < SIZE; i++) {
        if ( isInsideArea(x[i], y[i]) ) {
            k++;
        }
    }

    return 4.0 * (double) k / (double) SIZE;
}

/*
------------------------------------------------
------------------PARALLEL----------------------
------------------------------------------------
*/

void* parallelIntegrate(void* idThread) {
    int id = (int) idThread;

    for (int i = id * SIZE / NUM_THREADS; i < (id + 1) * SIZE / NUM_THREADS; i++) {
        if ( isInsideArea(x[i], y[i]) ) {
            countPoint[id]++;
        }
    }
}

void createThreads() {
    int rc;
    for (int t = 0; t < NUM_THREADS; t++) {
        rc = pthread_create(&threads[t], NULL, parallelIntegrate, (void*) t);
        if (rc) {
            printf("ERROR; return code from pthread_create() is %d\n", rc);
            exit(-1);
        }
    }
}

void waitAllThreads() {
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
}

int totalCountPoints() {
    int res = 0;
    for (int i = 0; i < NUM_THREADS; i++) {
        res += countPoint[i];
    }

    return res;
}

int main() {
    generateRandom(x, SIZE, 1);
    generateRandom(y, SIZE, 4);

    printf("PI = %.2lf\n", integrate(x, y));

    init();
    createThreads();
    waitAllThreads();

    int k = totalCountPoints();
    printf("Parallel PI = %.2lf\n", 4.0 * (double) k / (double) SIZE);

    return 0;
}