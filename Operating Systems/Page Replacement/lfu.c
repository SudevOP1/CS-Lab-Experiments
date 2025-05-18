#include <stdio.h>
#define size 3
#define MAX 100
int n = 12;
int q[size] = {-1, -1, -1};
int freq[MAX] = {0};

void replacePage(int page) {
    int minFreq = MAX, minIndex = -1;
    // Find the frame with the page that has the lowest frequency
    for(int i = 0; i < size; i++) {
        if(freq[q[i]] < minFreq) {
            minFreq = freq[q[i]];
            minIndex = i;
        }
    }
    q[minIndex] = page;
    freq[page]++;
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

void lfu(int a[]) {
    for(int i = 0; i < n; i++) {
        int found = 0;
        for(int j = 0; j < size; j++) {
            if(q[j] == a[i]) {
                freq[a[i]]++;
                found = 1;
                break;
            }
        }
        if(!found) {
            int placed = 0;
            for(int j = 0; j < size; j++) {
                if(q[j] == -1) {
                    q[j] = a[i];
                    freq[a[i]]++;
                    placed = 1;
                    break;
                }
            }
            if(!placed) {
                replacePage(a[i]);
            }
        }
        printArr();
    }
}

int main() {
    int a[20] = {2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2};
    lfu(a);
    return 0;
}