//Implement polynomial addition using Linked List
#include<stdio.h>
// #include<conio.h>
#include<stdlib.h>

struct Node {
    int coeff;
    int power;
    struct Node *next;
} *start1, *start2, *start3;

struct Node *create(struct Node *start) {
    int n, i;
    struct Node *newnode, *temp;
    printf("Enter no of terms: ");
    scanf("%d", &n);
    for(i=0; i<n; i++) {
        newnode = (struct Node *)malloc(sizeof(struct Node));
        printf("Enter power: ");
        scanf("%d", &newnode->power);
        printf("Enter coeff of with power %d: ", newnode->power);
        scanf("%d", &newnode->coeff);
        if(start == NULL) {
            start = newnode;
        } else {
            temp = start;
            while(temp->next != NULL) {
                temp = temp -> next;
            }
            temp->next = newnode;
        }
    }
    return start;
}

void create_result(int coeff, int power) {
    struct Node *newnode, *temp;
    newnode = (struct Node *)malloc(sizeof(struct Node));
    newnode -> coeff = coeff;
    newnode -> power = power;

    if(start3 == NULL) {
        start3 = newnode;
    } else {
        temp = start3;
        while(temp -> next != NULL) {
            temp = temp -> next;
        }
        temp -> next = newnode;
    }
}

struct Node *add() {
    int coeff, power;
    struct Node *temp1 = start1, *temp2 = start2;
    while (temp1 != NULL && temp2 != NULL) {
        if (temp1->power > temp2->power) {
            coeff = temp1->coeff;
            power = temp1->power;
            temp1 = temp1->next;
        } else if (temp1->power < temp2->power) {
            coeff = temp2->coeff;
            power = temp2->power;
            temp2 = temp2->next;
        } else {
            coeff = (temp1->coeff) + (temp2->coeff);
            power = (temp1->power);
            temp1 = temp1->next;
            temp2 = temp2->next;
        }
        create_result(coeff, power);
    } while (temp1 != NULL) {
        create_result(temp1->coeff, temp1->power);
        temp1 = temp1->next;
    } while (temp2 != NULL) {
        create_result(temp2->coeff, temp2->power);
        temp2 = temp2->next;
    }
}

void print_polynomial(struct Node *start) {
    struct Node *temp;
    temp = start;
    while(temp != NULL) {
        printf("%dx^%d", temp->coeff, temp->power);
        temp = temp -> next;
       
        if(temp != NULL){
            printf(" + ");
        }
    }
    printf("\n");
}

int main() {
    // clrscr();

    printf(" ===== Enter polynomial-1 expression:\n");
    start1 = create(start1);
    printf("---------------------------------------------\n");
    printf(" ===== Enter polynomial-2 expression:\n");
    start2 = create(start2);
   
    printf("---------------------------------------------\n");
    printf(" ===== This is polynomial-1:\n");
    print_polynomial(start1);
    printf(" ===== This is polynomial-2:\n");
    print_polynomial(start2);
    printf("---------------------------------------------\n");

    add();
    printf(" ===== Addition of these polynomials is:\n");
    print_polynomial(start3);

    // getch();
    return 0;
}