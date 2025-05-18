// circular linked list
#include <stdio.h>
// #include<conio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
} *start = NULL;

void create() {
    struct Node *newnode, *temp;
    int i, n;
    printf("Enter how many nodes to create: ");
    scanf("%d", &n);

    for (i = 0; i < n; i++) {
        newnode = (struct Node *)malloc(sizeof(struct Node));
        printf("Enter data: ");
        scanf("%d", &newnode->data);
        newnode->next = NULL; // Initialize next to NULL

        if (start == NULL) {
            start = newnode;
            temp = newnode;
        } else {
            temp->next = newnode;
            temp = newnode;
        }
    }
    // Complete the circular linkage
    if (temp != NULL) {
        temp->next = start; // Point last node to the first node
    }
}

void insert_before() {
    int val;
    struct Node *newnode, *temp, *pre = NULL;
    printf("Enter value before which you want to insert: ");
    scanf("%d", &val);
    newnode = (struct Node *)malloc(sizeof(struct Node));
    printf("Enter data to insert: ");
    scanf("%d", &newnode->data);
    newnode->next = NULL;

    if (start == NULL) {
        start = newnode; // If the list is empty, set newnode as start
        newnode->next = start; // Circular link
        return;
    }

    temp = start;
    while (temp->next != start && temp->data != val) {
        pre = temp;
        temp = temp->next;
    }

    if (temp == start && temp->data == val) { // Insert before first node
        newnode->next = start;
        // Find the last node to update its next
        while (temp->next != start) {
            temp = temp->next;
        }
        temp->next = newnode;
        start = newnode;
    } else if (temp->data == val) { // Insert before temp
        pre->next = newnode;
        newnode->next = temp;
    } else {
        printf("Value not found!\n");
        free(newnode); // Free the allocated node
    }
}

void insert_after() {
    int val;
    struct Node *newnode, *temp;
    printf("Enter value after which you want to insert: ");
    scanf("%d", &val);
    newnode = (struct Node *)malloc(sizeof(struct Node));
    printf("Enter data to insert: ");
    scanf("%d", &newnode->data);
    newnode->next = NULL;

    if (start == NULL) {
        start = newnode; // If the list is empty, set newnode as start
        newnode->next = start; // Circular link
        return;
    }

    temp = start;
    while (temp->data != val && temp->next != start) {
        temp = temp->next;
    }

    if (temp->data == val) { // If we found the value
        newnode->next = temp->next;
        temp->next = newnode;
    } else {
        printf("Value not found!\n");
        free(newnode); // Free the allocated node
    }
}

void delete_value() {
    int val;
    struct Node *temp, *pre = NULL;
    printf("Enter value to delete: ");
    scanf("%d", &val);

    if (start == NULL) {
        printf("Linked List Empty!\n");
        return;
    }

    temp = start;
    do {
        if (temp->data == val) {
            if (temp == start) { // Deleting the first node
                if (temp->next == start) { // Only one node
                    free(start);
                    start = NULL;
                } else {
                    pre = start;
                    while (pre->next != start) {
                        pre = pre->next; // Find the last node
                    }
                    pre->next = temp->next;
                    start = temp->next; // Update start
                    free(temp);
                }
            } else {
                pre->next = temp->next;
                free(temp);
            }
            return;
        }
        pre = temp;
        temp = temp->next;
    } while (temp != start);

    printf("Value not found!\n");
}

void display() {
    struct Node *temp;
    if (start != NULL) {
        temp = start;
        do {
            printf("%d ", temp->data);
            temp = temp->next;
        } while (temp != start);
        printf("\n");
    } else {
        printf("Linked List Empty\n");
    }
}

int main() {
    // clrscr();

    int choice, running = 1;
    create();

    while (running) {
        printf("******************************************************\n");
        printf("1. Insert Before \n");
        printf("2. Insert After  \n");
        printf("3. Delete Element\n");
        printf("4. Display       \n");
        printf("5. Quit          \n");
        printf("******************************************************\n");
        printf("Enter choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: insert_before(); break;
            case 2: insert_after(); break;
            case 3: delete_value(); break;
            case 4: display(); break;
            case 5: running = 0; break;
            default: printf("Enter correct choice!\n");
        }
    }

    // getch();
    return 0;
}