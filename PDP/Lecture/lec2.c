#include <stdio.h>
#include <pthread.h>
#include <time.h>

#define N   10
#define K   100000

pthread_mutex_t mutex;

int VAR = 0;

void* p_inc(void* arg) {
    //pthread_mutex_lock(&mutex);

    /*------------------------without lock------------------------------------*/
    
    // int res = pthread_mutex_tryock(&mutex);   // without lock
    // if (res == 0) {                 // free

    //     // blah - blah - code
    //     // ...
    //     // ...
    //     // finally unlock
    //     // pthread_mutex_unlock(&mutex);
    // } else if (res == EBUSY) {      // locked

    // }
    
    /*-------------------------------------------------------------------------*/
    /*------------------------timed lock, ex. 5sec-----------------------------*/

    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);     // 2arg = abstime
    ts.tv_sec += 5;
    ts.tv_nsec = 0;
    int res = pthread_mutex_timedlock(&mutex, &ts);

    /*-------------------------------------------------------------------------*/


    for (int i = 0; i < K; i++) {
        VAR++;
    }

    pthread_mutex_unlock(&mutex);
    return NULL;
}

void* p_dec(void* arg) {
    pthread_mutex_lock(&mutex);

    for (int i = 0; i < K; i++) {
        VAR--;
    }

    pthread_mutex_unlock(&mutex);
    return NULL;
} 

int main() {
    pthread_t thread_inc[N];
    pthread_t thread_dec[N];

    // init only main fucntion, once init
    pthread_mutex_init(&mutex, NULL);   // addr variable, other attr

    for (int i = 0; i < N; i++) {
        pthread_create(&thread_inc[i], NULL, p_inc, NULL);
        pthread_create(&thread_dec[i], NULL, p_dec, NULL);
    }

    for (int i = 0; i < N; i++) {
        pthread_join(thread_inc[i], NULL);
        pthread_join(thread_dec[i], NULL);
    }

    // also in func main()
    pthread_mutex_destroy(&mutex);

    printf("VAR = %d\n", VAR);

    return 0;
}