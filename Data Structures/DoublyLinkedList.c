// implement doubly linked list
#include<stdio.h>
// #include<conio.h>
#include<stdlib.h>

struct Node {
    int data;
    struct Node *next;
    struct Node *prev;
} *start;

void create() {
    struct Node *newnode, *temp;
    int i;

    for (i = 0; i < 5; i++) {
        newnode = (struct Node *)malloc(sizeof(struct Node));
        printf("Enter data: ");
        scanf("%d", &newnode->data);
        newnode->next = NULL; // Initialize next to NULL
        newnode->prev = NULL; // Initialize prev to NULL

        if (start == NULL) {
            start = newnode;
            temp = newnode;
        } else {
            temp->next = newnode;
            newnode->prev = temp;
            temp = newnode;
        }
    }
}

void insert_before() {
    struct Node *newnode, *temp;
    int value;
    newnode = (struct Node *)malloc(sizeof(struct Node));
    printf("Enter data to insert: ");
    scanf("%d", &newnode->data);
    printf("Enter data before which you want to insert: ");
    scanf("%d", &value);
    newnode -> next = NULL;
    newnode -> prev = NULL;
    temp = start;
    while(temp != NULL && temp -> data != value) {
        temp = temp -> next;
    }
    if(start == NULL) {
        start = newnode;
        return;
    } else if(temp == NULL) {
        printf("Value not found!\n");
    } else if(temp == start) {
        newnode -> next = temp;
        temp -> prev = newnode;
        start = newnode;
    } else {
        newnode -> next = temp;
        newnode -> prev = temp -> prev;
        newnode -> prev -> next = newnode;
        temp -> prev = newnode;
    }
}

void insert_after() {
    struct Node *newnode, *temp;
    int value;
    newnode = (struct Node *)malloc(sizeof(struct Node));
    printf("Enter data to insert: ");
    scanf("%d", &newnode->data);
    printf("Enter data after which you want to insert: ");
    scanf("%d", &value);
    newnode -> next = NULL;
    newnode -> prev = NULL;
    temp = start;
    while(temp != NULL && temp -> data != value) {
        temp = temp -> next;
    }
    if(start == NULL) {
        start = newnode;
        return;
    } else if(temp == NULL) {
        printf("Value not found!\n");
    } else {
        if(temp -> next != NULL) {
            temp -> next -> prev = newnode;
        }
        newnode -> next = temp -> next;
        newnode -> prev = temp;
        temp -> next = newnode;
    }
}

void delete_element() {
    struct Node *temp;
    int value;
    printf("Enter data to delete: ");
    scanf("%d", &value);

    temp = start;
    while(temp != NULL && temp -> data != value) {
        temp = temp -> next;
    }

    if(temp == NULL) {
        printf("Value not found!\n");
    } else if(temp == start && temp -> next == NULL) {
        start = NULL;
        free(temp);
    } else {
        if (temp == start) {
            start = start->next;
            if (start != NULL) {
                start->prev = NULL;
            }
        } else {
            if (temp->next != NULL) {
                temp->next->prev = temp->prev;
            }
            if (temp->prev != NULL) {
                temp->prev->next = temp->next;
            }
        }
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

    int option  = 0;
    int running = 1;

    create();

    while(running) {
        printf("************************************************************\n");
        printf("1. Insert Before\n2. Insert After\n3. Delete Element\n4. Display\n5. Exit\nEnter your option: ");
        scanf ("%d", &option);
        switch(option) {
            case 1 : insert_before();                   break;
            case 2 : insert_after();                    break;
            case 3 : delete_element();                  break;
            case 4 : display();                         break;
            case 5 : running = 0;                       break;
            default: printf("Enter valid option!\n");   break;
        } 
    }

    return 0;
    // getch();
}