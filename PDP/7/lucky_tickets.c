/*
    mpicc lucky_tickets.c -std=c99 -o lt
    mpirun -np 5 ./lt
*/

#include <mpi.h>
#include <stdio.h>
#include <math.h>

#define N                4
#define COUNT_TICKETS   (pow(10, 2*N))

int ticket[2*N];

void initNumber(unsigned long long num) {
    int i = 2*N - 1;
    while ( num ) {
        ticket[i] = num % 10;
        num /= 10;
        i--;
    }
}

void getNextNumber() {
    int flag = 0;
    for (int i = 0; i < 2*N; i++) {
        if (ticket[i] == 9) {
            flag++;
        }
    }
    if (flag == 2*N) {
        return;
    }

    int carry = 0;
    for (int i = 2*N - 1; i > 0; ) {
        if (carry == 0) {
            ticket[i]++;
        }
        
        if (ticket[i] >= 10) {
            carry = 1;
            ticket[i] = 0;
            ticket[i-1]++;
            if (ticket[i-1] >= 10) {
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

    unsigned long long num_begin = (unsigned long long) (  rank      * COUNT_TICKETS / size ); 
    unsigned long long num_end   = (unsigned long long) ( (rank + 1) * COUNT_TICKETS / size );
    //printf("%d %lld\n", rank, num);
    initNumber(num_begin);

    int sum_left  = 0;
    int sum_right = 0;
    unsigned int count_lucky_tickets = 0;
    for (unsigned long long i = 0; i < num_end - num_begin; i++) {
        // for (int k = 0; k < 2*N; k++) {
        //     printf("%d", ticket[k]);
        // }
        sum_left  = 0;
        sum_right = 0;
        for (int j = 0; j < N; j++) {
            sum_left  += ticket[j];
            sum_right += ticket[N+j];
        }

        if (sum_left == sum_right) {
            count_lucky_tickets++;
            //printf(" - lucky\n");
        }
        //printf("\n");
        getNextNumber();
    }
    // printf("%d %d\n", rank, count_lucky_tickets);

    int clt = 0;
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Reduce(&count_lucky_tickets, &clt, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        printf("Count lucky %d-digit tickets = %d\n", 2*N, clt);
    }

    MPI_Finalize();
    return 0;
}