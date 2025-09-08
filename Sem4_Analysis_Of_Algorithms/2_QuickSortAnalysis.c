// calculate time for quick sort of 30,000 elems

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

void swap(int* a, int* b) {
    int temp;
    temp = *a;
    *a = *b;
    *b = temp;
}

void quick_sort(int start, int end) {
    int i = start;
    int j = end - 1;
    int pivot = array[end];
    if(start >= end) return; // ending case

    while(i <= j) {
        while(i <= j && array[i] < pivot) {
            i++;
        }
        while(i <= j && array[j] > pivot) {
            j--;
        }
        if(i <= j) {
            swap(&array[i], &array[j]);
            i++; j--;
        }
    }

    swap(&array[i], &array[end]);
    quick_sort(start, i-1);
    quick_sort(i+1, end);
}

int main() {
    clock_t start_time, final_time;
    // clrscr();

    // create random array
    create_random_array();

    // calculate time for quick sort
    start_time = clock();
    quick_sort(0, n-1);
    final_time = clock();
    
    // print time for quick sort
    printf("Start Time = %d\n", start_time);
    printf("Final Time = %d\n", final_time);
    printf("Time for quick sort = %d\n", final_time - start_time);

    // getch();
    return 0;
}
