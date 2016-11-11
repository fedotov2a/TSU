#include <mpi.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank;
    int size;

    // MPI_COMM_WORLD - коммуникатор. Отвечает за все процессы

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);   // номер процесса
    MPI_Comm_size(MPI_COMM_WORLD, &size);   // общее число запущенных процессов

    printf("rank = %d size = %d\n", rank, size);

    MPI_Finalize();
    return 0;
}