// calculate time for merge sort of 30,000 elems

#include<stdio.h>
// #include<conio.h>
#include<time.h>
#include<stdlib.h>

int n=30000;
int array[30000];
int temp[30000];

void create_random_array() {
    int i, min, max;
    min = 1;
    max = 30000;
    for(i=0; i<n; i++) {
        // Find a random number in the range [min, max]
        array[i] = rand() % (max - min + 1) + min;
    }
}

void print_arr() {
    int i;
    for(i=0; i<n; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");
}

void merge(int start, int mid, int end) {
    int i = start;
    int j = mid + 1;
    int k = start;

    while(i<=mid && j<=end) {
        if(array[i] < array[j]) {
            temp[k] = array[i];
            k++; i++;
        } else {
            temp[k] = array[j];
            k++; j++;
        }
    }

    while(i <= mid) {
        temp[k] = array[i];
        k++; i++;
    }

    while(j <= end) {
        temp[k] = array[j];
        k++; j++;
    }

    for(i=start; i<=end; i++) {
        array[i] = temp[i];
    }
}

void merge_sort(int start, int end) {
    if(start < end) {
        int mid = (start + end) / 2;
        merge_sort(start, mid);
        merge_sort(mid + 1, end);
        merge(start, mid, end);
    }
}

int main() {
    clock_t start_time, final_time;
    // clrscr();

    // create random array
    create_random_array();

    // calculate time for merge sort
    start_time = clock();
    merge_sort(0, n-1);
    final_time = clock();
    
    // print time for merge sort
    printf("Start Time = %d\n", start_time);
    printf("Final Time = %d\n", final_time);
    printf("Time for merge sort = %d\n", final_time - start_time);

    // getch();
    return 0;
}
