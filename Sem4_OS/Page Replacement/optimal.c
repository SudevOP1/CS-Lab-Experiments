#include <stdio.h>

#define size 3
int n = 12;
int q[3] = {-1, -1, -1};

void replacePage(int index, int a[]) {
    int nextIndex[3] = {n + 1, n + 1, n + 1}; 

    for(int i = 0; i < size; i++) {
        for(int j = index + 1; j < n; j++) {
            if(q[i] == a[j]) {
                nextIndex[i] = j;
                break;
            }
        }
    }

    int maxIndex = 0;
    for(int i = 1; i < size; i++) {
        if(nextIndex[i] > nextIndex[maxIndex]) {
            maxIndex = i;
        }
    }

    q[maxIndex] = a[index];
}

void printArr() {
    for(int i = 0; i < size; i++) {
        if(q[i] == -1)
            printf("-\t");
        else
            printf("%d\t", q[i]);
    }
    printf("\n");
}

void opt(int a[]) {
    for(int i = 0; i < n; i++) {
        int flag = 0;
        for(int j = 0; j < size; j++) {
            if(q[j] == a[i]) {
                flag = 1; // Hit
                break;
            }
        }
        if(!flag) {
            int placed = 0;
            for(int j = 0; j < size; j++) {
                if(q[j] == -1) {
                    q[j] = a[i];
                    placed = 1;
                    break;
                }
            }
            if(!placed) {
                replacePage(i, a);
            }
        }
        printArr();
    }
}

int main() {
    int a[20] = {2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2};
    opt(a);
    return 0;
}
