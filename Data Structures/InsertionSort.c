// Insertion Sort
#include <stdio.h>
// #include<conio.h>

int n = 10;
int array[10];

void insertion_sort()
{
    int i, j, key;

    for (i = 1; i < n; i++)
    {
        key = array[i];
        j = i - 1;
        while (j >= 0 && array[j] > key)
        {
            array[j + 1] = array[j];
            j--;
        }
        array[j + 1] = key;
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

    printf("\nBefore Insertion Sort: ");
    for (i = 0; i < n; i++)
    {
        printf("%d ", array[i]);
    }

    insertion_sort();

    printf("\nAfter Insertion Sort: ");
    for (i = 0; i < n; i++)
    {
        printf("%d ", array[i]);
    }

    // getch();
    return 0;
}