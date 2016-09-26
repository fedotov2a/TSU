/* 
    Linux:
        gcc -std=c99 -pthread integrate_PI_2.c -o pi
        ./pi
*/
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_THREADS     4
#define STEP_COUNT      5000

#define LOWER_BOUND     0
#define UPPER_BOUND     1

pthread_t   threads[NUM_THREADS];
double      sumT[NUM_THREADS];

double func(double x) {
    return 4.0 / (1.0 + (double)x*x);
} 

double integrate(double a, double b, unsigned int step_count) {
    if (step_count == 0) {
        return 0.0;
    }

    double sum  = 0.0;
    double step = (b - a) / ( (double)step_count );

    for (int i = 1; i < step_count; i++ ) {
        sum += func((double)a + (double)i * (double)step);
    }

    sum += (func(a) + func(b)) / 2.0;
    sum *= step; 

    return sum;
}

/*
----------------Parallel functions-------------------
*/

void init() {
    for (int i = 0; i < NUM_THREADS; i++) {
        sumT[i] = 0.0;
    }
}

void* parallelIntegrate(void* idThread) {
    int id = (int) idThread;

    double step = (double) (UPPER_BOUND - LOWER_BOUND) / (double) STEP_COUNT;
    
    for (int i = id * STEP_COUNT / NUM_THREADS + 1; i < (id + 1) * STEP_COUNT / NUM_THREADS; i++) {
        sumT[id] += func((double)LOWER_BOUND + (double)i * (double)step);
    }

    sumT[id] += (func(LOWER_BOUND) + func(UPPER_BOUND)) / 2.0;
    sumT[id] *= step;
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

double totalSum() {
    double sum = 0.0;
    for (int i = 0; i < NUM_THREADS; i++) {
        sum += sumT[i];
    }
    return sum;
}
 
int main() {
    printf ("Integrate_[0, 1] F(x) = %.2lf\n", integrate(0, 1, 500));

    init();
    createThreads();
    waitAllThreads();

    double sum = totalSum();
    printf("Parallel integrate_[0, 1] F(x) = %.2lf\n", sum);

    return 0;
}
