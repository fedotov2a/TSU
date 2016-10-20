#include <stdio.h>
#include <pthread.h>
#include <time.h>

#define NUM_THREADS         5
#define EATING_TIME         2
#define THINKING_TIME       3
#define TIME_DAY            10

pthread_t           philosophers[NUM_THREADS];
pthread_mutex_t     forks[NUM_THREADS];

void* dining(void* idThread) {
    int id = (int) idThread;
    // time_t rawtime;
    // struct tm* timeinfo;

    // time (&rawtime);
    // timeinfo = localtime(&rawtime);
    // printf ("Current local time and date: %s\n", asctime(timeinfo));
    // printf("%d\n", timeinfo->tm_sec);

    // int start_day = timeinfo->tm_sec;
    // int end_day   = timeinfo->tm_sec;

    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    ts.tv_sec += 3;
    ts.tv_nsec = 0;

    int left_fork  = id;
    int right_fork = (id + 1) % NUM_THREADS;

    while (1) {
        printf("Philosopher #%d try to take right fork %d\n", id, right_fork);
        if ( !pthread_mutex_timedlock(&forks[right_fork], &ts) ) {
            printf("Philosopher #%d took right fork %d\n", id, right_fork);
            printf("Philosopher #%d try to take left fork %d\n", id, left_fork);
            if ( !pthread_mutex_timedlock(&forks[left_fork], &ts) ) {
                printf("Philosopher #%d took both forks %d %d\n", id, left_fork, right_fork);
                printf("Philosopher #%d eats\n", id);
                sleep(EATING_TIME);
                printf("Philosopher #%d finished eating\n", id);
                pthread_mutex_unlock(&forks[left_fork]);
            } else {
                printf("Philosopher #%d didn't take left fork %d\n", id, left_fork);
            }
            pthread_mutex_unlock(&forks[right_fork]);
        } else {
            printf("Philosopher #%d didn't take right fork %d\n", id, right_fork);
        }
        printf("Philosopher #%d thinks..\n", id);
        sleep(THINKING_TIME);
    }
    return NULL;
}

void createThreads() {
    int i;
    for (i = 0; i < NUM_THREADS; i++){
        pthread_mutex_init(&forks[i], NULL);
    }

    for (i = 0; i < NUM_THREADS; i++){
        pthread_create(&philosophers[i], NULL, dining, (void *)i);
    }
}

void destroyAllMutex() {
    int i;
    for (i = 0; i < NUM_THREADS; i++){
        pthread_mutex_destroy(&forks[i]);
    }
}

void timeWaitsForNoOne() {
    while ( clock() / CLOCKS_PER_SEC < TIME_DAY );
}

int main() {
    createThreads();
    timeWaitsForNoOne();
    destroyAllMutex();
    return 0;
}