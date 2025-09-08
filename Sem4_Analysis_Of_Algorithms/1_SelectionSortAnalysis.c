// calculate time for selection sort of 30,000 elems

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

void selection_sort() {
    int i, j, min, temp;
    for(i=0; i<n-1; i++) {
        min = i;

        // find index of min value
        for(j=i+1; j<n; j++) {
            if(array[j] < array[min]){
                min = j;
            }
        }

        // swap array[i] and array[min]
        temp = array[i];
        array[i] = array[min];
        array[min] = temp;
    }
}

int main() {
    clock_t start_time, final_time;
    // clrscr();

    // create random array
    create_random_array();

    // calculate time for selection sort
    start_time = clock();
    selection_sort();
    final_time = clock();
    
    // print time for selection sort
    printf("Start Time = %d\n", start_time);
    printf("Final Time = %d\n", final_time);
    printf("Time for selection sort = %d\n", final_time - start_time);

    // getch();
    return 0;
}
