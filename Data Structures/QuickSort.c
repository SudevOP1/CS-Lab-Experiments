// Quick Sort
#include <stdio.h>
// #include<conio.h>

int n = 10;
int array[10];

void quick_sort(int low, int high)
{
    int partition_index, pivot, i, j, temp;

    if (low < high)
    {
        // Choosing the last element as pivot
        pivot = array[high];
        i = low - 1;

        for (j = low; j < high; j++)
        {
            if (array[j] <= pivot)
            {
                i++;
                // Swap array[i] and array[j]
                temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }

        // Swap pivot element with element at i+1
        temp = array[i + 1];
        array[i + 1] = array[high];
        array[high] = temp;

        partition_index = i + 1;

        // Recursively sort elements before and after partition
        quick_sort(low, partition_index - 1);
        quick_sort(partition_index + 1, high);
    }
}

int main()
{
    int i;
    // clrscr();

    printf("Enter array: ");

    for (i = 0; i < n; i++)
    {
        scanf("%d", &array[i]);
    }

    printf("\nBefore Quick Sort: ");
    for (i = 0; i < n; i++)
    {
        printf("%d ", array[i]);
    }

    quick_sort(0, n - 1);

    printf("\nAfter Quick Sort: ");
    for (i = 0; i < n; i++)
    {
        printf("%d ", array[i]);
    }

    // getch();
    return 0;
}