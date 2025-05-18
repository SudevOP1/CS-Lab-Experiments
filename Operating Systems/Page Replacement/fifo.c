#include <stdio.h>

#define size 3
int hit = 0;
int next = 0; // points to the next frame to be replaced
int q[size] = {-1, -1, -1};

int isHit(int page) {
    for(int i = 0; i < size; i++) {
        if(q[i] == page) {
            return 1; // Hit
        }
    }
    return 0; // Fault
}

void printArr() {
    for(int i = 0; i < size; i++) {
        if(q[i] == -1) {
            printf("-\t");
        }
        else {
            printf("%d\t", q[i]);
        }
    }
    printf("\n");
}

void fifo(int a[], int n) {
    for(int i = 0; i < n; i++) {
        if(isHit(a[i])) {
            hit++;
            printArr();
        }
        else {
            q[next] = a[i];
            next = (next + 1) % size; // Move to the next position in array
            printArr();
        }
    }
}

int main() {
    int n, a[20];
    printf("Enter the number of processes:");
    scanf("%d", &n);
    printf("Enter the sequence:");
    for(int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }
    fifo(a, n);
    printf("Hits # : %d\n", hit);
    printf("Faults # : %d\n", n - hit);
    printf("Hits ratio : %d/%d\n", hit, n);
    return 0;
}