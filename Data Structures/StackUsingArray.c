// stack using array
#include <stdio.h>
// #include<conio.h>
#include <stdlib.h>

int stack[5];
int top = -1;

void push()
{
    if (top == 4)
    {
        printf("Stack Full");
    }
    else
    {
        printf("Enter value to push: ");
        scanf("%d", &stack[++top]);
        printf("%d pushed successfully!\n", stack[top]);
    }
}

void pop()
{
    if (top == -1)
    {
        printf("Stack empty :(\n");
    }
    else
    {
        top--;
        printf("Top element popped!\n");
    }
}

void display()
{
    if (top == -1)
        printf("Stack empty :(\n");
    else
    {
        int i = top;
        printf("Stack elements are: ");
        for (i = top; i != -1; i--)
            printf(" %d", stack[i]);
    }
    printf("\n");
}

void peek()
{
    if (top == -1)
    {
        printf("Stack empty :(\n");
    }
    else
    {
        printf("Top element is: %d\n", stack[top]);
    }
}

int main()
{
    // clrscr();

    int option = 0;
    int running = 1;
    while (running)
    {
        printf("************************************************************\n");
        printf("1. Push\n2. Pop\n3. Display\n4. Peek\n5. Exit\nEnter your option: ");
        scanf("%d", &option);
        switch (option)
        {
        case 1:
            push();
            break;
        case 2:
            pop();
            break;
        case 3:
            display();
            break;
        case 4:
            peek();
            break;
        case 5:
            running = 0;
            break;
        default:
            printf("Enter valid option!");
            break;
        }
    }

    // getch();
    return 0;
}