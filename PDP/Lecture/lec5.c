#include <stdio.h>
#include <omp.h>

#define N   10

int main() {
    int x = 12345;
    int y = 11111;
    int z = 22222;

    int i;

    /*------for------*/

    // #pragma omp parallel num_threads(4)
    // {
    //     #pragma omp for private(i)
    //         for (i = 0; i < N; i++) {
    //             printf("#thread = %d  i = %d\n", i, omp_get_thread_num());
    //         }

    //     // #pragma omp for private(i)
    //     //     for (i = 0; i < 2 * N; i++) {
    //     //         printf("#thread2 = %d  i2 = %d\n", i, omp_get_thread_num());
    //     //     }
    // }

    // #pragma omp parallel for num_threads(4) private(i)
    //     for (i = 0; i < N; i++) {
    //         printf("#thread = %d  i = %d\n", i, omp_get_thread_num());
    //     }


    /*------sections-------*/

    // #pragma omp parallel num_threads(3)
    // {
    //     #pragma omp sections
    //     {
    //         #pragma omp section
    //         {
    //             printf("sec1 #thread = %d \n", omp_get_thread_num());
    //         }

    //         #pragma omp section
    //         {
    //             printf("sec2 #thread = %d \n", omp_get_thread_num());
    //         }

    //         #pragma omp section
    //         {
    //             printf("sec3 #thread = %d \n", omp_get_thread_num());
    //         }
    //     }
    // }

    // #pragma omp parallel sections num_threads(3)
    // {
    //     #pragma omp section
    //     {
    //         printf("sec1 #thread = %d \n", omp_get_thread_num());
    //     }

    //     #pragma omp section
    //     {
    //         printf("sec2 #thread = %d \n", omp_get_thread_num());
    //     }

    //     #pragma omp section
    //     {
    //         printf("sec3 #thread = %d \n", omp_get_thread_num());
    //     }
    // }

    /*------single-------*/

    // #pragma omp parallel num_threads(5)
    // {
    //     #pragma omp single
    //     {
    //         printf("%d\n", omp_get_thread_num());
    //     }

    //     #pragma omp single
    //     {
    //         printf("%d\n", omp_get_thread_num());
    //     }

    //     #pragma omp single
    //     {
    //         printf("%d\n", omp_get_thread_num());
    //     }
    // }

    // #pragma omp parallel num_threads(5)
    // {
    //     #pragma omp single
    //     {
    //         printf("%d\n", omp_get_thread_num());
    //     }

    //     #pragma omp single
    //     {
    //         printf("%d\n", omp_get_thread_num());
    //     }

    //     #pragma omp master
    //     {
    //         printf("%d\n", omp_get_thread_num());
    //     }
    // }

    // #pragma omp parallel for private(i) num_threads(2) schedule(dynamic, 4)
    //     for (i = 0; i < N; i++) {
    //         printf("%d i = %d\n", omp_get_thread_num(), i);
    //     }

    /*------reduction-------*/

    int s = 0;
    // #pragma omp parallel num_threads(N) reduction(*: s)
    #pragma omp parallel for private(i) num_threads(4) reduction(+: s)
        for (i = 0; i < 1001; i++) {
            s += i;
        }

    printf("s = %d\n", s);


    return 0;
}