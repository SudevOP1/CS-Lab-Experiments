// linear queue using array
#include <stdio.h>
// #include <conio.h>

#define max 5
int queue[5];
int front = -1, rear = -1;

void enqueue(int x)
{
    if (rear == max - 1)
    {
        printf("Queue Full\n");
    }
    else if (rear == -1)
    {
        front++;
        queue[++rear] = x;
    }
    else
    {
        queue[++rear] = x;
    }
}

void dequeue()
{
    if (front == -1)
    {
        printf("Queue Empty\n");
    }
    else if (front == rear)
    {
        printf("Deleted Element is %d\n", queue[front]);
        front = -1;
        rear = -1;
    }
    else
    {
        printf("Deleted element is %d\n", queue[front++]);
    }
}

void display()
{
    int i;
    if (front == -1)
    {
        printf("Queue Empty\n");
    }
    else
    {
        i = front;
        while (i <= rear)
        {
            printf("%d ", queue[i++]);
        }
        printf("\n");
    }
}

int main()
{
    // clrscr();

    int running = 1;
    int choice = -1;
    int val;

    while (running)
    {
        printf("********************\nChoices:\n1.Enqueue\n2.Dequeue\n3.Display\n4.Quit\n");
        printf("********************\nEnter choice: ");
        scanf("%d", &choice);
        if (choice == 1)
        {
            printf("Enter value to enqueue: ");
            scanf("%d", &val);
            enqueue(val);
        }
        else if (choice == 2)
        {
            dequeue();
        }
        else if (choice == 3)
        {
            display();
        }
        else if (choice == 4)
        {
            running = 0;
        }
    }

    // getch();
    return 0;
}