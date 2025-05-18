// stack using LL
#include<stdio.h>
// #include<conio.h>
#include<stdlib.h>

struct Node {
    int data;
    struct Node *next;
};
struct Node *top = NULL;

void push() {
    struct Node *newnode;
    newnode = (struct Node *)malloc(sizeof(struct Node));
    printf("Enter data to push: ");
    scanf("%d", &newnode->data);
    
    if(top == NULL) {
        top = newnode;
    } else {
        newnode->next = top;
        top = newnode;
    }
}

int pop(){
    struct Node *temp;
    int x;
    temp = top;

    if(top==NULL) {
        return -999999;
    } else {
        x = temp->data;
        top = temp->next;
        free(temp);
        return x;
    }
}

void display(){
    struct Node *temp;
    temp = top;

    if(top == NULL) {
        printf("Stack Empty");
    } else {
        while(temp != NULL){
            printf("%d ", temp->data);
            temp = temp->next;
        }
    }
}

void peek() {
    if(top != NULL) {
        printf("Top element is %d", top -> data);
    } else {
        printf("Stack Empty!\n");
    }
}

int main(){
    // clrscr();

    int option  = 0;
    int running = 1;
    while(running) {
        printf("************************************************************\n");
        printf("1. Push\n2. Pop\n3. Display\n4. Peek\n5. Exit\nEnter your option: ");
        scanf ("%d", &option);
        switch(option) {
            case 1 : push();    break;
            case 2 : pop();     break;
            case 3 : display(); break;
            case 4 : peek();    break;
            case 5 : running=0; break;
            default: printf("Enter valid option!"); break;
        }
    }
    
    // getch();
    return 0;
}