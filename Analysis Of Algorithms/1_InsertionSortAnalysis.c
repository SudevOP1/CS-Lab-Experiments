// calculate time for insertion sort of 30,000 elems

#include<stdio.h>
// #include<conio.h>
#include<time.h>
#include<stdlib.h>

int n=30000;
int array[30000];

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

void insertion_sort() {
    int i, j, key;

    for (i=1; i<n; i++) {
        key = array[i];
        j = i-1;
        while(j>=0 && array[j]>key) {
            array[j+1] = array[j];
            j--;
        }
        array[j+1] = key;
    }
}

int main() {
    clock_t start_time, final_time;
    // clrscr();

    // create random array
    create_random_array();

    // calculate time for insertion sort
    start_time = clock();
    insertion_sort();
    final_time = clock();
    
    // print time for insertion sort
    printf("Start Time = %d\n", start_time);
    printf("Final Time = %d\n", final_time);
    printf("Time for insertion sort = %d\n", final_time - start_time);

    // getch();
    return 0;
}
