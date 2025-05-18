#include <stdio.h>
#include <stdlib.h>
#include <conio.h> // Required for clrscr() and getch()

#define TABLE_SIZE 10

typedef struct Node
{
    int data;
    struct Node *next;
} Node;

// Global hash table
int hashTable[TABLE_SIZE];
Node *chain[TABLE_SIZE];

// Function prototypes
void initHashTableLinear();
void initHashTableChaining();
int hashFunction(int key);
void insertLinear(int key);
void deleteLinear(int key);
int searchLinear(int key);
void displayLinear();
void insertChaining(int key);
void deleteChaining(int key);
int searchChaining(int key);
void displayChaining();

int main()
{
    int choice, key, searchResult;
    int mode;

    clrscr(); // Clear screen for DOSBox

    printf("Choose Hashing Technique:\n");
    printf("1. Linear Probing\n");
    printf("2. Chaining\n");
    printf("Enter your choice: ");
    scanf("%d", &mode);

    if (mode == 1)
    {
        initHashTableLinear();
    }
    else if (mode == 2)
    {
        initHashTableChaining();
    }
    else
    {
        printf("Invalid choice!\n");
        getch();
        return 1;
    }

    do
    {
        printf("\nMenu:\n");
        printf("1. Insert\n");
        printf("2. Delete\n");
        printf("3. Search\n");
        printf("4. Display\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
        case 1:
            printf("Enter the key to insert: ");
            scanf("%d", &key);
            if (mode == 1)
            {
                insertLinear(key);
            }
            else
            {
                insertChaining(key);
            }
            break;

        case 2:
            printf("Enter the key to delete: ");
            scanf("%d", &key);
            if (mode == 1)
            {
                deleteLinear(key);
            }
            else
            {
                deleteChaining(key);
            }
            break;

        case 3:
            printf("Enter the key to search: ");
            scanf("%d", &key);
            if (mode == 1)
            {
                searchResult = searchLinear(key);
            }
            else
            {
                searchResult = searchChaining(key);
            }
            if (searchResult)
                printf("Key found in the hash table.\n");
            else
                printf("Key not found in the hash table.\n");
            break;

        case 4:
            if (mode == 1)
            {
                displayLinear();
            }
            else
            {
                displayChaining();
            }
            break;

        case 5:
            printf("Exiting program.\n");
            break;

        default:
            printf("Invalid choice! Please try again.\n");
        }
    } while (choice != 5);

    getch(); // Wait for user input before exiting
    return 0;
}

// Initialize hash table for linear probing
void initHashTableLinear()
{
    int i;
    for (i = 0; i < TABLE_SIZE; i++)
    {
        hashTable[i] = -1; // -1 indicates empty slot
    }
}

// Initialize hash table for chaining
void initHashTableChaining()
{
    int i;
    for (i = 0; i < TABLE_SIZE; i++)
    {
        chain[i] = NULL;
    }
}

// Hash function
int hashFunction(int key)
{
    return key % TABLE_SIZE;
}

// Linear Probing: Insert
void insertLinear(int key)
{
    int index, originalIndex;
    index = hashFunction(key);
    originalIndex = index;

    while (hashTable[index] != -1 && hashTable[index] != -2)
    { // -2 indicates deleted slot
        index = (index + 1) % TABLE_SIZE;
        if (index == originalIndex)
        {
            printf("Hash table is full! Cannot insert key.\n");
            return;
        }
    }
    hashTable[index] = key;
    printf("Key %d inserted.\n", key);
}

// Linear Probing: Delete
void deleteLinear(int key)
{
    int index, originalIndex;
    index = hashFunction(key);
    originalIndex = index;

    while (hashTable[index] != -1)
    {
        if (hashTable[index] == key)
        {
            hashTable[index] = -2; // Mark slot as deleted
            printf("Key %d deleted.\n", key);
            return;
        }
        index = (index + 1) % TABLE_SIZE;
        if (index == originalIndex)
        {
            break;
        }
    }
    printf("Key %d not found!\n", key);
}

// Linear Probing: Search
int searchLinear(int key)
{
    int index, originalIndex;
    index = hashFunction(key);
    originalIndex = index;

    while (hashTable[index] != -1)
    {
        if (hashTable[index] == key)
        {
            return 1; // Key found
        }
        index = (index + 1) % TABLE_SIZE;
        if (index == originalIndex)
        {
            break;
        }
    }
    return 0; // Key not found
}

// Display hash table for linear probing
void displayLinear()
{
    int i;
    printf("Hash Table:\n");
    for (i = 0; i < TABLE_SIZE; i++)
    {
        if (hashTable[i] == -1)
        {
            printf("[%d]: Empty\n", i);
        }
        else if (hashTable[i] == -2)
        {
            printf("[%d]: Deleted\n", i);
        }
        else
        {
            printf("[%d]: %d\n", i, hashTable[i]);
        }
    }
}

// Chaining: Insert
void insertChaining(int key)
{
    int index;
    Node *newNode;
    index = hashFunction(key);
    newNode = (Node *)malloc(sizeof(Node));
    newNode->data = key;
    newNode->next = chain[index];
    chain[index] = newNode;
    printf("Key %d inserted.\n", key);
}

// Chaining: Delete
void deleteChaining(int key)
{
    int index;
    Node *current, *prev;
    index = hashFunction(key);
    current = chain[index];
    prev = NULL;

    while (current != NULL)
    {
        if (current->data == key)
        {
            if (prev == NULL)
            {
                chain[index] = current->next; // Delete head node
            }
            else
            {
                prev->next = current->next;
            }
            free(current);
            printf("Key %d deleted.\n", key);
            return;
        }
        prev = current;
        current = current->next;
    }
    printf("Key %d not found!\n", key);
}

// Chaining: Search
int searchChaining(int key)
{
    int index;
    Node *current;
    index = hashFunction(key);
    current = chain[index];

    while (current != NULL)
    {
        if (current->data == key)
        {
            return 1; // Key found
        }
        current = current->next;
    }
    return 0; // Key not found
}

// Display hash table for chaining
void displayChaining()
{
    int i;
    printf("Hash Table:\n");
    for (i = 0; i < TABLE_SIZE; i++)
    {
        printf("[%d]: ", i);
        Node *current = chain[i];
        if (current == NULL)
        {
            printf("Empty\n");
        }
        else
        {
            while (current != NULL)
            {
                printf("%d -> ", current->data);
                current = current->next;
            }
            printf("NULL\n");
        }
    }
}
