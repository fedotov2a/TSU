#include "func.h"

void init() {
    // memset(sumT,    0,               NUM_THREADS);
    // memset(maxT,    0,               sizeof(maxT) * sizeof(int));
    // memset(minT,    UPPER_BOUND + 1, sizeof(minT) * sizeof(int));
    for (int i = 0; i < NUM_THREADS; i++) {
        sumT[i] = 0;
        maxT[i] = 0;
        minT[i] = UPPER_BOUND + 1;
    }
    fillArrayRandomNumbers(bigArray, SIZE_ARRAY);
}

void sum_(int* array, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += array[i];
    }
    printf("sum = %d\n", sum);
}

void min_(int* array, int size) {
    int min = minT[0];
    for (int i = 1; i < size; i++) {
        if (minT[i] < min) {
            min = minT[i];
        }
    }
    printf("min = %d\n", min);
}

void max_(int* array, int size) {
    int max = maxT[0];
    for (int i = 1; i < size; i++) {
        if (maxT[i] > max) {
            max = maxT[i];
        }
    }
    printf("max = %d\n", max);
}

void printArray(int* array, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");
}

void fillArrayRandomNumbers(int* array, int size) {
    time_t t;
    srand((unsigned) time(&t));

    for (int i = 0; i < size; i++) {
        array[i] = rand() % UPPER_BOUND + LOWER_BOUND;
    }
}

/*
-----------------------------------------
----------PARALLEL FUNCTIONS-------------
-----------------------------------------
*/

void* parallelSum(void* idThread) {
    int id = (int) idThread;
    printf("%d %d\n", id, sumT[id]);
    for (int i = id * SIZE_ARRAY / NUM_THREADS; i < (id + 1) * SIZE_ARRAY / NUM_THREADS; i++) {
        sumT[id] += bigArray[i];
    }

    return NULL;
}

void* parallelMin(void* idThread) {
    int id = (int) idThread;

    for (int i = id * SIZE_ARRAY / NUM_THREADS; i < (id + 1) * SIZE_ARRAY / NUM_THREADS; i++) {
        if (bigArray[i] < minT[id]) {
            minT[id] = bigArray[i];
        }
    }

    return NULL;
}

void* parallelMax(void* idThread) {
    int id = (int) idThread;

    for (int i = id * SIZE_ARRAY / NUM_THREADS; i < (id + 1) * SIZE_ARRAY / NUM_THREADS; i++) {
        if (bigArray[i] > maxT[id]) {
            maxT[id] = bigArray[i];
        }
    }

    return NULL;
}

void createThreads(func f) {
    int rc;
    for (int t = 0; t < NUM_THREADS; t++) {
        rc = pthread_create(&threads[t], NULL, f, (void*) t);
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
