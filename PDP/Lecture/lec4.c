// Win
// VS since ver. 2010
// gcc 4.2
#include <stdio.h>
#include <omp.h>

int main() {

    // #pragma omp parallel num_threads(6)
    // {
    //  printf("Hello\n");
    // }

    // omp_set_num_threads(3);
    // #pragma omp parallel
    // {
    //     printf("Hello\n");
    // }

    // #pragma omp parallel
    // {
    //  printf("Hi\n");
    // }

    // int i = 0;

    // #pragma omp parallel num_threads(4)
    // {
    //     int count_th = omp_get_num_threads();
    //     int num_th   = omp_get_thread_num();
    //     printf("Hello\n%d %d\n", count_th, num_th);
    // }

    // int x = 12345;

    // #pragma omp parallel firstprivate(x)
    // //                   private(x)
    // {
    //     x = omp_get_thread_num();
    //     printf("%d\n", x);
    // }

    int x = 12345;
    int y = 11111;
    int z = 22222;

    #pragma omp parallel private(x) shared(y, z)
    {
        x = omp_get_thread_num();
        printf("Hello\n");
    }

    return 0;
}