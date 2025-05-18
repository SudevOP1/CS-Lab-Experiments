// Selection Sort
#include <stdio.h>
// #include<conio.h>

int n = 10;
int array[10];

void selection_sort()
{
    int i, j, min, temp;

    for (i = 0; i < n - 1; i++)
    {

        min = i;

        // find index of min value
        for (j = i + 1; j < n; j++)
        {
            if (array[j] < array[min])
            {
                min = j;
            }
        }

        // swap array[i] and array[min]
        temp = array[i];
        array[i] = array[min];
        array[min] = temp;
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

    printf("\nBefore Selection Sort: ");
    for (i = 0; i < n; i++)
    {
        printf("%d ", array[i]);
    }

    selection_sort();

    printf("\nAfter Selection Sort: ");
    for (i = 0; i < n; i++)
    {
        printf("%d ", array[i]);
    }

    // getch();
    return 0;
}