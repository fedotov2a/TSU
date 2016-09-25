#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <openssl/md5.h>

int main(int argc, char** argv) {
    unsigned char* alfabet = "abcdefghijklmnopqrstuvwxyz";
    unsigned char hash[MD5_DIGEST_LENGTH];
    unsigned char password[2 * MD5_DIGEST_LENGTH];

    printf("%s", argv[1]);
    printf("\n");

    for (int i = 0; i < 26; i++) {
        MD5(&alfabet[i], 1, hash);

        for (int j = 0; j < MD5_DIGEST_LENGTH; j++) {
            sprintf(&password[j * 2], "%02x", hash[j]);
            //printf("%02x", hash[j]);
        }
        //printf("\n");


        if ( !strcmp(password, argv[1]) ) { /* == 0*/
            printf("%c\n", alfabet[i]);
            printf("%s\n", password);
        }
    }

    // MD5("0123456789", 10, hash);
    // for (int i = 0; i < MD5_DIGEST_LENGTH; i++) {
    //     printf("%02x", hash[i]);
    // }
    // printf("\n");

    return 0;
}