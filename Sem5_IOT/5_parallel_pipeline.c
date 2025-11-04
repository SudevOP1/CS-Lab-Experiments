#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

#define SIZE 1000000
#define NUM_THREADS 4
int data[SIZE];

void *read_data(void *arg) {
    long start = (long)arg;
    long end = start + SIZE / NUM_THREADS;
    for (long i = start; i < end; i++) {
        data[i] = i + 1;
    }
    return NULL;
}

void *process_data(void *arg) {
    long start = (long)arg;
    long end = start + SIZE / NUM_THREADS;
    for (long i = start; i < end; i++) {
        data[i] = data[i] * 2;
    }
    return NULL;
}

void *display_data(void *arg) {
    if ((long)arg == 0) {
        printf("First 10 processed numbers: ");
        for (int i = 0; i < 10; i++) {
            printf("%d ", data[i]);
        }
        printf("\n");
    }
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];
    clock_t start, end;
    double time_taken;

    printf("\n===== PARALLEL PIPELINE =====\n");
    start = clock();

    for (long i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, read_data, (void *)(i * (SIZE / NUM_THREADS)));
    }
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    for (long i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, process_data, (void *)(i * (SIZE / NUM_THREADS)));
    }
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    for (long i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, display_data, (void *)i);
    }
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    end = clock();
    time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Processor Time (Parallel): %.6f seconds\n", time_taken);
    return 0;
}
