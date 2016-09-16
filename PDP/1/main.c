#include "func.h"

int main() {
    init();

    createThreads(parallelSum);
    waitAllThreads();

    sum_      (sumT, NUM_THREADS);
    printArray(sumT, NUM_THREADS);

    return 0;
}
