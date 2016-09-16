#include "func.h"

int main() {
    init();

    createThreads(parallelMax);
    waitAllThreads();

    max_      (maxT, NUM_THREADS);
    printArray(maxT, NUM_THREADS);
    printArray(bigArray, SIZE_ARRAY);

    return 0;
}
