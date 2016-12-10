// CUDA  sc11-cuda-c-basic.pdf
// nvcc
#include <stdio.h>

#define N   16
#define M   1

// __global__ - функция, которая будет выполняться графическим процессором (функция ядра)
__global__ void mykernel(void) {
    printf("Hello, World!\n");
}

__global__ void add(int a, int b, int* c) {  // параметры содержаться в графическом устройстве
    *c = a + b;
}

__global__ void add2(int* a, int* b, int* c) {
    // blockIdx = [0..N-1]  трехмерный массив
    c[blockIdx.x] = a[blockIdx.x] + b[blockIdx.x];
}

int main(void) {

    // mykernel<<<1,1>>>(); // вызов функции mykernel()

    // int c;
    // int* dev_c;

    // //Выделение памяти на графическом устройстве
    // cudaMalloc( (void**) &dev_c, sizeof(int) );

    // add<<<1, 1>>>(3, 5, dev_c);      // <<<N, M>>> N - blocks, M - threads

    // // копируем из GPU в ОЗУ
    // cudaMemcpy(&c, dev_c, sizeof(int), cudaMemcpyDeviceToHost);

    // printf("%d\n", c);

    // cudaFree( dev_c );


    int* a;
    int* b;
    int* c;
    int* d_a;
    int* d_b;
    int* d_c;
    int size = N * sizeof(int);


    // Выделение памяти на GPU
    cudaMalloc( (void**) &d_a, size);
    cudaMalloc( (void**) &d_b, size);
    cudaMalloc( (void**) &d_c, size);


    // Выделение памяти в ОЗУ
    a = (int*) malloc(size);
    b = (int*) malloc(size);
    c = (int*) malloc(size);

    for (int i = 0; i < N; i++) {
        a[i] = i;
        b[i] = i * i;
    }

    cudaMemcpy(d_a, a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, b, size, cudaMemcpyHostToDevice);

    add2<<<N, M>>>(d_a, d_b, d_c);

    cudaMemcpy(c, d_c, size, cudaMemcpyDeviceToHost);

    for (int i = 0; i < N; i++) {
        printf("%d\n", c[i]);
    }

    free(a);
    free(b);
    free(c);
    cudaFree( d_a );
    cudaFree( d_b );
    cudaFree( d_c );


    return 0;
}