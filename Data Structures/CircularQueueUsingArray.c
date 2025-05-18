// circular queue using array
#include<stdio.h>
// #include<conio.h>

int circularQueue[12];
int SIZE  = 12;
int front = -1;
int rear  = -1;

void enqueue(int val) {
    // Queue full
    if((rear+1) % SIZE == front) {
        printf("Queue Full\n");
    }
    // First time insertion
    else if(rear == -1) {
        rear  = 0;
        front = 0;
        circularQueue[rear] = val;
    }
    // Normal insertion
    else {
        rear = (rear+1) % SIZE;
        circularQueue[rear] = val;
    }

}

void dequeue() {
    if(front == -1) {
        printf("Queue Empty\n");
        return;
    }

    printf("Deleted element is %d\n", circularQueue[front]);
    // Queue becomes empty
    if(front == rear) {
        front = -1;
        rear  = -1;
        return;
    }
    // Queue doesnt become empty
    front = (front+1) % SIZE;
}

void display() {
    int i;
    if(front == -1) {
        printf("Queue Empty\n");
        return;
    }

    i = front;
    while(1) {
        printf("%d ", circularQueue[i]);
        if(i == rear) break;
        i = (i+1) % SIZE;
    }
    printf("\n");
}

int main() {
    // clrscr();

    int running = 1;
    int choice = -1;
    int val;
   
    while (running) {
        printf("********************\nChoices:\n1.Enqueue\n2.Dequeue\n3.Display\n4.Quit\n");
        printf("********************\nEnter choice: ");
        scanf("%d", &choice);
        if (choice == 1) {
            printf("Enter value to enqueue: ");
            scanf("%d", &val);
            enqueue(val);
        }
        else if(choice == 2) {
            dequeue();
        }
        else if(choice == 3) {
            display();
        }
        else if(choice == 4) {
            running = 0;
        }
    }

    // getch();
    return 0;
}
