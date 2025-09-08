#include<stdio.h>
// #include<conio.h>
#include<stdlib.h>

int array[100];
int min, max, min1, max1, n = 100;
int count = 0;

void find_minmax(int i, int j) {
    int mid;
    if(i == j) {
        count++;
        min = array[i];
        max = array[i];
    }
    else if(i == j-1) {
        if(array[i] < array[j]) {
            min = array[i];
            max = array[j];
        } else {
            min = array[j];
            max = array[i];
        }
        count++;
    }
    else {
        mid = (i+j)/2;
        find_minmax(i, mid);
        min1 = min;
        max1 = max;
        find_minmax(mid+1, j);
        count++;
        if(max < max1) {
            max = max1;
        }
        count++;
        if(min > min1) {
            min = min1;
        }
    }
}

void create_random_array() {
    int i, min_no, max_no;
    min_no = 1;
    max_no = 30000;
    for(i=0; i<n; i++) {
        // Find a random number in the range [min_no, max_no]
        array[i] = rand() % (max_no - min_no + 1) + min_no;
    }
}

int main() {
    int i;
    // clrscr();

    create_random_array();
    find_minmax(0, n-1);
    
    printf("Min         = %d\n", min);
    printf("Max         = %d\n", max);
    printf("n           = %d\n", n);
    printf("Comparisons = %d", count);

    // getch();
    return 0;
}

