// Queue using LL
#include <stdio.h>
// #include<conio.h>
#include <stdlib.h>

struct Node
{
    int data;
    struct Node *next;
};
struct Node *front = NULL, *rear = NULL;

void enqueue()
{
    struct Node *newnode;

    newnode = (struct Node *)malloc(sizeof(struct Node));
    printf("Enter data to enqueue: ");
    scanf("%d", &newnode->data);
    newnode->next = NULL;

    if (front == NULL)
    {
        rear = newnode;
        front = newnode;
    }
    else
    {
        rear->next = newnode;
        rear = newnode;
    }
}

int dequeue()
{
    struct Node *temp;
    int x;

    if (front == NULL)
    {
        return -99999;
    }
    else
    {
        temp = front;
        x = temp->data;
        front = front->next;
        free(temp);
        return x;
    }
}

void display()
{
    struct Node *temp;
    temp = front;

    if (front == NULL)
    {
        printf("Queue is empty");
    }
    else
    {
        while (temp != rear)
        {
            printf("%d ", temp->data);
            temp = temp->next;
        }
        printf("%d", temp->data);
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
        printf("********************\nChoices:\n1.Enqueue\n2.Dequeue\n3.Display\n4.Quit\n");
        printf("********************\nEnter choice: ");
        scanf("%d", &choice);
        if (choice == 1)
        {
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

    return 0;
    // getch();
}