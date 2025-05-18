// linear linked list
#include<stdio.h>
// #include<conio.h>
#include<stdlib.h>

struct Node {
    int data;
    struct Node *next;
} *start;

void create() {
    struct Node *newnode, *temp;
    for(int i=0; i<5; i++) {
        if(start == NULL) {
            newnode = (struct Node*)malloc(sizeof(struct Node));
            printf("Enter data: ");
            scanf("%d", &newnode -> data);
            start = newnode;
        }
        else {
            newnode = (struct Node*)malloc(sizeof(struct Node));
            printf("Enter data: ");
            scanf("%d", &newnode -> data);
            temp = start;
            while(temp -> next != NULL) {
                temp = temp -> next;
            }
            temp -> next = newnode;
        }
    }
}

void insert_before() {
    int x;
    struct Node *temp, *p, *newnode;
    newnode = (struct Node*)malloc(sizeof(struct Node));
    printf("Enter value before which you want to insert: ");
    scanf("%d", &x);
    printf("Enter data to insert: ");
    scanf("%d", &newnode -> data);
    temp = start;
    while(temp -> data != x) {
        p = temp;
        temp = temp -> next;
    }
    if(temp == start) {
        newnode -> next = start;
        start = newnode;
    }
    else {
        p -> next = newnode;
        newnode -> next = temp;
    }
}

void insert_after() {
    int x;
    struct Node *temp, *newnode;
    newnode = (struct Node*)malloc(sizeof(struct Node));
    printf("Enter value after which you want to insert: ");
    scanf("%d", &x);
    printf("Enter data to insert: ");
    scanf("%d", &newnode -> data);
    temp = start;
    while(temp -> data != x) {
        temp = temp -> next;
    }
    newnode -> next = temp -> next;
    temp -> next = newnode;
}

void delete_data() {
    struct Node *temp, *p;
    int val;
    printf("Enter value to be deleted: ");
    scanf("%d", &val);
    temp = start;
    while(temp != NULL && temp -> data != val) {
        p = temp;
        temp = temp -> next;
    }
    if(temp == start) {
        start = start -> next;
        free(temp);
    }
    else if(temp == NULL) {
        printf("Value not found\n");
    }
    else {
        p -> next = temp -> next;
        free(temp);
    }
}

void display() {
    struct Node *temp;
    temp = start;
    while(temp != NULL) {
        printf("%d ", temp -> data);
        temp = temp -> next;
    }
    printf("\n");
}

int main() {
    // clrscr();

    int choice, running = 1;
    create();

    while(running) {
        printf("******************************************************\n");
        printf("1. Insert Before\n");
        printf("2. Insert After \n");
        printf("3. Delete       \n");
        printf("4. Display      \n");
        printf("5. Quit         \n");
        printf("******************************************************\n");
        printf("Enter choice: ");
        scanf("%d", &choice);
       
        switch(choice){
            case 1 : insert_before(); break;
            case 2 : insert_after();  break;
            case 3 : delete_data();   break;
            case 4 : display();       break;
            case 5 : running = 0;     break;
            default: printf("Enter correct choice!");
        }
    }

    // getch();
    return 0;
}