// gcc brutforce.c -lcrypto -pthread -std=c99 -lm -o bf
// ./bf `echo -n w0rd | md5sum | cut -b 1-32`

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <openssl/md5.h>
#include <math.h>

#define NUM_THREADS            10
#define SIZE                   36
#define LEN_PASSWORD           4
#define COUNT_COMBINATION      (int) pow(SIZE, LEN_PASSWORD)

unsigned char* alfabet = "abcdefghijklmnopqrstuvwxyz0123456789";
unsigned char  input[2 * MD5_DIGEST_LENGTH + 1];

pthread_t threads[NUM_THREADS];

unsigned char* getNextWord(int number) {
    unsigned char* result = malloc (sizeof (unsigned char) * (LEN_PASSWORD + 1));

    int i = 1;
    for (; i < LEN_PASSWORD; i++) {
        result[i-1] = alfabet[ (number / (int) pow(SIZE, LEN_PASSWORD - i)) % SIZE ];
    }
    result[i-1] = alfabet[ number % SIZE ];

    return result;
}

void* hack_parallel(void* idThread) {
    int id = (int) idThread;

    unsigned char* word;
    unsigned char md5_word[MD5_DIGEST_LENGTH + 1];
    unsigned char md5_res[2 * MD5_DIGEST_LENGTH + 1];

    for (int i = id * COUNT_COMBINATION / NUM_THREADS; i < (id + 1) * COUNT_COMBINATION / NUM_THREADS; i++) {
        word = getNextWord(i);
        
        MD5(word, LEN_PASSWORD, md5_word);
        
        for (int j = 0; j < MD5_DIGEST_LENGTH; j++) {
            sprintf(&md5_res[j * 2], "%02x", md5_word[j]);
        }

        if ( !strcmp(md5_res, input) ) {
            printf("\nOK\n");
            printf("Thread #%d found the word!\n", id + 1);
            printf("word = %s\n", word);
            printf("MD5  = %s\n", md5_res);
            free(word);
            return NULL;
        }
    }
    free(word);
    return NULL;
}

void createThreads() {
    int rc;
    for (int t = 0; t < NUM_THREADS; t++) {
        rc = pthread_create(&threads[t], NULL, hack_parallel, (void*) t);
        if (rc) {
            printf("ERROR; return code from pthread_create() is %d\n", rc);
            exit(-1);
        }
    }
}

void waitAllThreads() {
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
}

int main(int argc, char** argv) {
    printf("input MD5 = %s\n", argv[1]);
    strcpy(input, argv[1]);
    createThreads();
    waitAllThreads();

    return 0;
}