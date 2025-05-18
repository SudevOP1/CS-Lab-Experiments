// implement mirror_tree and find_height functions of a BST
#include <stdio.h>
#include <stdlib.h>
// #include<conio.h>

struct Node
{
    int data;
    struct Node *left;
    struct Node *right;
} *root;

struct Node *create_node(int value)
{
    struct Node *newnode = (struct Node *)malloc(sizeof(struct Node));
    newnode->data = value;
    newnode->left = NULL;
    newnode->right = NULL;
    return newnode;
}

struct Node *mirror_tree(struct Node *node)
{
    struct Node *temp;
    if (node != NULL)
    {
        mirror_tree(node->left);
        mirror_tree(node->right);
        temp = node->left;
        node->left = node->right;
        node->right = temp;
    }
    return node;
}

void inorder_print(struct Node *node)
{
    if (node != NULL)
    {
        inorder_print(node->left);
        printf("%d ", node->data);
        inorder_print(node->right);
    }
}

int find_height(struct Node *node)
{
    int left_child_height;
    int right_child_height;
    if (node == NULL)
    {
        return 0; // height = 0
    }
    left_child_height = find_height(node->left);
    right_child_height = find_height(node->right);
    return (left_child_height > right_child_height ? left_child_height : right_child_height) + 1;
}

int main()
{
    // clrscr();

    // Creating tree manually
    root = create_node(100);
    root->left = create_node(80);
    root->right = create_node(120);
    root->left->left = create_node(70);
    root->left->right = create_node(90);
    root->right->left = create_node(110);
    root->right->right = create_node(130);
    root->left->left->left = create_node(65);
    root->left->left->right = create_node(75);
    //                  100
    //         80                 120
    //     70      90         110     130
    //   65  75

    // find_height function
    printf("Height of tree: %d\n", find_height(root));

    // mirror_tree function
    printf("\nBefore Mirroring:\n");
    inorder_print(root);
    printf("\nAfter Mirroring:\n");
    inorder_print(mirror_tree(root));

    // getch();
    return 0;
}