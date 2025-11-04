#include <stdio.h>
#include <time.h>
#define SIZE 1000000

int main() {
    int data[SIZE];
    clock_t start, end;
    double time_taken;

    printf("===== SEQUENTIAL PIPELINE =====\n");

    start = clock();

    for (int i = 0; i < SIZE; i++) {
        data[i] = i + 1;
    }
    for (int i = 0; i < SIZE; i++) {
        data[i] = data[i] * 2;
    }

    printf("First 10 processed numbers: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", data[i]);
    }
    printf("\n");

    end = clock();
    time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Processor Time (Sequential): %.6f seconds\n", time_taken);
    return 0;
}
