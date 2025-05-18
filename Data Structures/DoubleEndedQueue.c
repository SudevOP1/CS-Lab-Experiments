// double-ended queue using array
#include <stdio.h>
// #include <conio.h>

#define SIZE 5
int queue[SIZE];
int front = -1, rear = -1;

void insert_rear(int val)
{
    // Queue full
    if ((rear + 1) % SIZE == front)
    {
        printf("Queue Full\n");
    }
    // First time insertion
    else if (rear == -1)
    {
        rear = 0;
        front = 0;
        queue[rear] = val;
    }
    // Normal insertion
    else
    {
        rear = (rear + 1) % SIZE;
        queue[rear] = val;
    }
}

void delete_front()
{
    if (front == -1)
    {
        printf("Queue Empty\n");
    }
    else
    {
        printf("Deleted element is %d\n", queue[front]);
        // Queue becomes empty
        if (front == rear)
        {
            front = -1;
            rear = -1;
        }
        else
        {
            front = (front + 1) % SIZE;
        }
    }
}

void insert_front(int val)
{
    // Queue full
    if (front == (rear + 1) % SIZE)
    {
        printf("Queue Full\n");
    }
    // First time insertion
    else if (front == -1)
    {
        rear = 0;
        front = 0;
        queue[front] = val;
    }
    // Normal insertion
    else
    {
        front = (front + SIZE - 1) % SIZE;
        queue[front] = val;
    }
}

void delete_rear()
{
    if (rear == -1)
    {
        printf("Queue Empty\n");
    }
    else
    {
        printf("Deleted element is %d\n", queue[front]);
        // Queue becomes empty
        if (front == rear)
        {
            front = -1;
            rear = -1;
        }
        else
        {
            rear = (rear + SIZE - 1) % SIZE;
        }
    }
}

void display()
{
    if (front == -1)
    {
        printf("Queue Empty\n");
        return;
    }

    int i = front;
    while (1)
    {
        printf("%d ", queue[i]);
        if (i == rear)
            break;
        i = (i + 1) % SIZE;
    }
    printf("\n");
}

int main()
{
    // clrscr();

    int running = 1;
    int choice = -1;
    int val;

    while (running)
    {

        printf("********************\nChoices:\n");
        printf("1. Insert from Front\n2. Insert from Rear\n3. Delete from Front\n4. Delete from Rear\n5. Display\n6. Quit\n");
        printf("********************\nEnter choice: ");
        scanf("%d", &choice);

        if (choice == 1)
        {
            printf("Enter value to insert from front: ");
            scanf("%d", &val);
            insert_front(val);
        }
        else if (choice == 2)
        {
            printf("Enter value to insert from rear: ");
            scanf("%d", &val);
            insert_rear(val);
        }
        else if (choice == 3)
        {
            delete_front();
        }
        else if (choice == 4)
        {
            delete_rear();
        }
        else if (choice == 5)
        {
            display();
        }
        else if (choice == 6)
        {
            running = 0;
        }
    }

    // getch();
    return 0;
}
