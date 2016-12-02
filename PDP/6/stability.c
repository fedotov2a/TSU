/*
    mpicc stability.c -std=c99 -o st
    mpirun -np 5 ./st
*/

#include <mpi.h>
#include <stdio.h>
#include <math.h>

#define N                3
#define COUNT_NUMBERS    (9 * (pow(10, N - 1)) - 1)

int number[N];

void initNumber(long long num) {
    int i = N - 1;
    while ( num ) {
        number[i] = num % 10;
        num /= 10;
        i--;
    }
}

void getNextNumber() {
    int flag = 0;
    for (int i = 0; i < N; i++) {
        if (number[i] == 9) {
            flag++;
        }
    }
    if (flag == N) {
        return;
    }

    int carry = 0;
    for (int i = N - 1; i > 0; ) {
        if (carry == 0) {
            number[i]++;
        }
        
        if (number[i] >= 10) {
            carry = 1;
            number[i] = 0;
            number[i-1]++;
            if (number[i-1] >= 10) {
                i--;
            } else {
                break;
            }
        } else {
            break;
        }
    }
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank;
    int size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    long long num_begin = (long long) (( rank * COUNT_NUMBERS / size ) + (long long) pow(10, N - 1));
    long long num_end   = (long long) (( (rank + 1) * COUNT_NUMBERS / size ) + (long long) pow(10, N - 1));
    //printf("%d %lld\n", rank, num);
    initNumber(num_begin);

    int max_stability = 0;
    int pr = 1;
    int k = 0;
    for (long long i = 0; i <= num_end - num_begin; i++) {
        pr = 1;
        k = 0;
        for (int j = 0; j < N; j++) {
            pr = pr * number[j] % 10;
            k++;
            if (pr == 0) {
                break;
            }
        }
        if (max_stability <= k) {
            max_stability = k;
        }
        getNextNumber();
    }

    int max_stab = 0;
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Reduce(&max_stability, &max_stab, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);

    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Bcast(&max_stab, 1, MPI_INT, 0, MPI_COMM_WORLD);

    initNumber(num_begin);
    for (long long i = 0; i <= num_end - num_begin; i++) {
        pr = 1;
        k = 0;
        for (int j = 0; j < N; j++) {
            pr = pr * number[j] % 10;
            k++;
            if (pr == 0) {
                break;
            }
        }
        if (k == max_stab) {
            printf("%d ", rank);
            for (int j = 0; j < N; j++) {
                printf("%d", number[j]);
            }
            printf("\n");

        }
        getNextNumber();
    }

    MPI_Finalize();
    return 0;
}
