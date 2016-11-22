#include <mpi.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank;
    int size;

    // MPI_COMM_WORLD - коммуникатор. Отвечает за все процессы

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);   // номер процесса
    MPI_Comm_size(MPI_COMM_WORLD, &size);   // общее число запущенных процессов

    //printf("rank = %d size = %d\n", rank, size);

    /* -- отослать
    MPI_Send(
            void*        buf,       // void* - адрес, которой хотим отослать буффера в памяти
            int          count,     // int - количество(не размер) элементов в сообщении
            MPI_Datatype type,      // MPI_Datatype - тип пересылаемых данных (char, byte, int ...)
            int          dest,      // Destination - номер процесса, которому отправляем данные [0..size-1]
            int          tag,       // Tag - идентификация сообщения (для кодера)
            MPI_COMM_WORLD          // Глобальный коммуникатор
    );
    */

    /* -- прием, блокирующая функция
    MPI_Recv(
            void* buf,              // адрес куда положим данные
            int count,              // количестов принимаемых данных
            MPI_Datatype type,      // тип
            int source,             // номер процесса, от которого принимаем данные
            int tag,                // идентификация сообщения
            MPI_COMM_WORLD,
            MPI_Status status       // статус
    );
    */
    
    // if (rank == 1) {
    //     // MPI_Send(&rank, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    //     int snd = 12345;
    //     MPI_Send(&snd, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    // }
    // if (rank == 2) {
    //     // MPI_Send(&rank, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    //     int snd = 54321;
    //     MPI_Send(&snd, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    // }
    // if (rank == 0) {
    //     int rcv;
    //     MPI_Status status;
        
    //     MPI_Recv(&rcv, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
    //     printf("rcv = %d from = %d\n", rcv, status.MPI_SOURCE);

    //     MPI_Recv(&rcv, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
    //     printf("rcv = %d from = %d\n", rcv, status.MPI_SOURCE);
    // }
    
    /*------------------------------------------------------------------------*/

    // if ( rank == 0 ) {
    //     MPI_Status status;
    //     int rcv;
    //     int s = 0;
    //     for (int i = 1; i < size; i++) {    // [1..size-1]
    //         MPI_Recv(&rcv, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
    //         s += rcv;
    //     }
    //     printf("%d\n", s);
    // } else {
    //     MPI_Send(&rank, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    // }

    /*---------------------------------------------------------------*/

    /* 1 -> all. Выполняется на всех процессах
    MPI_Bcast(
            void* buf,      // адрес, где лежит информация
            int count,
            Datatype type,
            int root,       // ранк процесса, с которого осуществляется широковещательная рассылка [0..size-1]
            MPI_COMM_WORLD
    );
    */
    
    // int x = 0;

    // if ( rank == 0 ) {
    //     x = 12345;
    // }

    // printf("rank = %d | before Bcast: x = %d\n", rank, x);
    // MPI_Bcast(&x, 1, MPI_INT, 0, MPI_COMM_WORLD);
    // printf("rank = %d | after Bcast: x = %d\n", rank, x);
    
    /* операция редукции | all -> 1 with operation = {+, -, *, min, max, and, or...}
    MPI_Reduce(
            void* send_buf,
            void* recv_buf,
            int count,
            MPI_Datatype type,
            MPI_Op operation,       // операция редукции
            int root,               // процесс, на который приходят данные
            MPI_Comm MPI_COMM_WORLD
    );
    */
    
    int rcv = 0;
    rank++;
    printf("Before: rank = %d | rcv = %d\n", rank, rcv);
    MPI_Barrier(MPI_COMM_WORLD); // ждет все процессы | fflush(stdout); - ???

    MPI_Reduce(&rank, &rcv, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD); // 0-процесс и шлет и собирает информация
    //MPI_Reduce(&rank, &rcv, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    printf("After: rank = %d | rcv = %d\n", rank, rcv);
    MPI_Barrier(MPI_COMM_WORLD); // ждет все процессы

    MPI_Finalize();
    return 0;
}