// implement binary search tree
#include<stdio.h>
// #include<conio.h>
#include<stdlib.h>

struct Node {
    int data;
    struct Node *left;
    struct Node *right;
} *root;

void insert_element() {
    struct Node *temp, *par, *newnode;
    newnode = (struct Node *)malloc(sizeof(struct Node));
    printf("Enter data to insert: ");
    scanf("%d", &newnode->data);
    newnode -> left  = NULL;
    newnode -> right = NULL;

    if(root == NULL) {
        root = newnode;
    } else {
        temp = root;
        // Traversal (finding the parent)
        while(temp != NULL) {
            if(newnode -> data >= temp -> data) {
                par = temp;
                temp = temp -> right;
            } else {
                par = temp;
                temp = temp -> left;
            }
        }
        // Insertion
        if(newnode -> data >= par -> data) {
            par -> right = newnode;
        } else {
            par -> left  = newnode;
        }
    }
}

void inorder  (struct Node *par) { // A+B LVR
    if(par != NULL) {
        inorder(par -> left);
        printf("%d ", par->data);
        inorder(par -> right);
    }
}

void postorder(struct Node *par) { // AB+ LRV
    if(par != NULL) {
        postorder(par -> left);
        postorder(par -> right);
        printf("%d ", par->data);
    }
}

void preorder (struct Node *par) { // +AB VLR
    if(par != NULL) {
        printf("%d ", par->data);
        preorder(par -> left);
        preorder(par -> right);
    }
}

void delete_element() {
    struct Node *temp, *par, *psucc, *succ;
    int val;
    printf("Enter data to delete: ");
    scanf("%d", &val);

    if(root == NULL) {
        printf("Tree Empty!\n");
        return;
    } else {
        temp = root;
        // Traversal (finding the parent)
        while(temp != NULL && temp -> data != val) {
            par = temp;
            if(val >= temp -> data) {
                temp = temp -> right;
            } else {
                temp = temp -> left;
            }
        }
        // Deletion
        if(temp == NULL) {
            printf("Value not found!\n");
        }
        else if(temp -> left == NULL && temp -> right == NULL) { // No children
            if(par -> left == NULL) {
                par -> left = NULL;
            } else {
                par -> right = NULL;
            }
            free(temp);
            printf("%d deleted successfully!", val);
        }
        else if(temp -> left != NULL) { // Only one child (left)
            if(par -> right == temp) {
                par -> right = temp -> left;
            } else {
                par -> left = temp -> left;
            }
            free(temp);
        }
        else if(temp -> right != NULL) { // Only one child (right)
            if(par -> left == temp) {
                par -> left = temp -> right;
            } else {
                par -> right = temp -> right;
            }
            free(temp);
        }
        else { // Two children
            psucc = temp;
            succ = temp -> left;
            while(succ -> right != NULL) {
                psucc = succ;
                succ = succ -> right;
            }
            temp -> data = succ -> data;
            psucc -> right = succ -> left;
            free(succ);
        }
    }
    
}

void search() {
    struct Node *temp;
    int val, count = 0;
    printf("Enter data to search: ");
    scanf("%d", &val);

    if(root == NULL) {
        printf("Tree Empty!\n");
        return;
    } else {
        temp = root;
        // Traversal
        while(temp != NULL && temp -> data != val) {
            if(val >= temp -> data) {
                temp = temp -> right;
            } else {
                temp = temp -> left;
            }
        }
        // Printing result
        if(temp == NULL) {
            printf("Value not found!\n");
        }
        else if(temp -> data == val) {
            count = 1;
            while(temp -> right -> data == val) {
                temp = temp -> right;
                count++;
            }
            if(count == 1) {
                printf("%d found once!\n", val);
            } else {
                printf("%d found %d times!\n", val, count);
            }
        }
    }
}

int main() {
    // clrscr();

    int option  = 0;
    int running = 1;
    while(running) {
        printf("************************************************************\n");
        printf("1. Insert Element\n2. Print Inorder\n3. Print Postorder\n4. Print Preorder\n5. Delete Element\n6. Exit\nEnter your option: ");
        scanf ("%d", &option);
        switch(option) {
            case 1 : insert_element();                break;
            case 2 : inorder  (root); printf("\n");   break;
            case 3 : postorder(root); printf("\n");   break;
            case 4 : preorder (root); printf("\n");   break;
            case 5 : delete_element();                break;
            case 6 : running = 0;                     break;
            default: printf("Enter valid option!\n"); break;
        } 
    }

    return 0;
    // getch();
}
