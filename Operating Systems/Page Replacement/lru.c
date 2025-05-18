#include <stdio.h>

#define size 3
int hit = 0;
int time[100]; // stores the last used time of each frame
int q[size] = {-1, -1, -1};

int findLRU() {
    int min = time[0], pos = 0;
    for(int i = 1; i < size; i++) {
        if(time[i] < min) {
            min = time[i];
            pos = i;
        }
    }
    return pos;
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

void lru(int a[], int n) {
    int t = 0;
    for(int i = 0; i < n; i++) {
        int flag = 0;
        for(int j = 0; j < size; j++) {
            if(q[j] == a[i]) { // check for hit
                t++;
                time[j] = t;
                hit++;
                flag = 1;
                break;
            }
        }
        if(!flag) {
            int pos = -1;
            for(int j = 0; j < size; j++) { // empty space available
                if(q[j] == -1) {
                    pos = j;
                    break;
                }
            }
            if(pos == -1) { // queue full, replace page
                pos = findLRU();
            }
            t++;
            q[pos] = a[i];
            time[pos] = t;
        }
        printArr();
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
    lru(a, n);
    printf("Hits # : %d\n", hit);
    printf("Faults # : %d\n", n - hit);
    printf("Hits ratio : %d/%d\n", hit, n);
    return 0;
}