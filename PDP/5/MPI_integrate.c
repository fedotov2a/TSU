/*
    mpicc MPI_integrate.c -std=c99 -o integrate
    mpirun -n 6 integrate
*/

#include <mpi.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>

#define SIZE_ARRAY  1000000

double x[SIZE_ARRAY];
double y[SIZE_ARRAY];

void generateRandom(double* array, int size, int ub) {
    sleep(1);
    srand(time(NULL));

    for (int i = 0; i < size; i++) {
        array[i] = (double) rand() / (double) RAND_MAX * (double) ub;
    }
}

int isInsideArea(double x, double y) {
    if ( (double)y - (4.0 / (1.0 + (double)x*x)) <= 0.0 ) {     // y = 4 / (1+x^2)  | x: [0, 1], y: [0, 4]
    // if ( x*x + y*y - 1.0 <= 0.0 ) {                          // x^2 + y^2 = 1    | x: 0[0, 1], y: [0, 1]
        return 1;
    }
    return 0;
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank;
    int size;

    generateRandom(x, SIZE_ARRAY, 1);
    generateRandom(y, SIZE_ARRAY, 4);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    //printf("rank = %d size = %d\n", rank, size);

    int countPoint = 0;
    for (int i = rank * SIZE_ARRAY / size; i < (rank + 1) * SIZE_ARRAY / size; i++) {
        if ( isInsideArea(x[i], y[i]) ) {
            countPoint++;
        }
    }

    printf("rank = %d sum = %d\n", rank, countPoint);

    MPI_Finalize();
    return 0;
}