#include <stdio.h>
#include <stdlib.h>

int lock1 = 0;
int lock2 = 0;

void transaction1() {
    printf("\nTransaction 1: Trying to acquire locks...\n");
    if(lock1 == 0 && lock2 == 0) {
        lock1 = 1;
        printf("Transaction 1: Acquired Lock 1\n");
        lock2 = 1;
        printf("Transaction 1: Acquired Lock 2\n");
        printf("Transaction 1: Performing operations...\n");
    }
    else {
        printf("Transaction 1: Cannot acquire locks! They are already in use.\n");
    }
}

void transaction2() {
    printf("\nTransaction 2: Trying to acquire locks...\n");
    if(lock1 == 0 && lock2 == 0) {
        lock1 = 1;
        printf("Transaction 2: Acquired Lock 1\n");
        lock2 = 1;
        printf("Transaction 2: Acquired Lock 2\n");
        printf("Transaction 2: Performing operations...\n");
    }
    else {
        printf("Transaction 2: Cannot acquire locks! They are already in use.\n");
    }
}

void releaseLocks() {
    if(lock1 == 1 || lock2 == 1) {
        printf("\nReleasing all locks...\n");
        lock1 = 0;
        lock2 = 0;
    }
    else {
        printf("\nNo locks to release.\n");
    }
}

void checkLockStatus() {
    printf("\nLock Status:\n");
    printf("Lock 1: %s\n", (lock1 == 1) ? "Locked" : "Available");
    printf("Lock 2: %s\n", (lock2 == 1) ? "Locked" : "Available");
}

void displayMenu() {
    printf("\n----- Menu -----\n");
    printf("1. Execute Transaction 1\n");
    printf("2. Execute Transaction 2\n");
    printf("3. Check Lock Status\n");
    printf("4. Release Locks\n");
    printf("5. Exit\n");
}

int main()
{
    int choice;
    int running=1;
    displayMenu();
    while(running == 1) {
        printf("\nEnter your choice: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                transaction1();
                break;
            case 2:
                transaction2();
                break;
            case 3:
                checkLockStatus();
                break;
            case 4:
                releaseLocks();
                break;
            case 5:
                printf("\nExiting program...\n");
                running = 0;
            default:
                printf("\nInvalid choice! Please enter a valid option.\n");
        }
    }
}