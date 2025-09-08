// merge sort
#include<stdio.h>
// #include<conio.h>

int n = 10;
// int arr[10];
int arr[10] = {30, 70, 100, 60, 80, 40, 10, 90, 50, 20};

void merge(int arr[], int low, int mid, int high) {
    int i, j, k;
    int n1 = high - low; // size of left array
    int n2 = high - mid; // size of right array
    int left[n1], right[n2];
    
    for(i=0; i<n1; i++) left[i] = arr[low + i];
    for(i=0; i<n2; i++) right[i] = arr[mid+1 + i];
    
    i = 0;
    j = 0;
    k = low;
    
    // merge the left and right into main array
    while (i<n1 && j<n2) {
        if(left[i] <= right[j]) {
            arr[k] = left[i];
            i++;
        } else {
            arr[k] = right[j];
            j++;
        }
        k++;
    }

    // copy remaining elems of left if any
    while(i < n1) {
        arr[k] = left[i];
        i++;
        k++;
    }
    // copy remaining elems of right if any
    while(j < n2) {
        arr[k] = right[j];
        j++;
        k++;
    }
}

void merge_sort(int arr[], int low, int high) {
    int mid;
    if(low < high) {
        mid = low + (high-low)/2;
        // sort the first and second halves
        merge_sort(arr, low, mid);
        merge_sort(arr, mid+1, high);
        // merge the first and second halves
        merge(arr, low, mid, high);
    }
}

int main() {
    int i;
    // clrscr();

    // printf("Enter arr: ");
    // for (i=0; i<n; i++) {
    //     scanf("%d", &arr[i]);
    // }

    printf("\nBefore Radix Sort: ");
    for (i=0; i<n; i++) {
        printf("%d ", arr[i]);
    }

    merge_sort(arr, 0, n-1);

    printf("\nAfter Radix Sort: ");
    for (i=0; i<n; i++) {
        printf("%d ", arr[i]);
    }
    
    // getch();
    return 0;
}
