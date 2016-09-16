#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

#define N 10

void* fun(void* arg) {
    int id = (int) arg;
    printf("Hello from thread #%d\n", id);

    //double d = 123.456;     // not
    double* d = (double*) malloc(sizeof(double));
    *d = id + 123.456;

    //pthread_exit((void*) &d);     // return
    pthread_exit((void*) d);     // return
    return NULL;
}

int main() {
    double result[N];

    pthread_t thread_ids[N];
    pthread_t thread_id;

    // int rc = 0;
    // int k = 0;
    // while (rc == 0) {
    //  rc = pthread_create(&th, NULL, fun, (void*) k++);
    // }
    // printf("%d", k);

    for(int i = 0; i < N; i++) {
        pthread_create(&thread_ids[i], NULL, fun, (void*) i);
    }
    
    // pthread_create(&thread_id, NULL, fun, (void*) 0);
    // void* res;
    // pthread_join(thread_id, &res);

    // //printf("%lf\n", (double) res);
    // printf("%lf\n", *(double*) res);

    void* res;
    for (int i = 0; i < N; i++) {
        pthread_join(thread_ids[i], &res);
        printf("%lf\n", *(double*) res);
    }

    printf("Hello from main\n");

    return 0;
}