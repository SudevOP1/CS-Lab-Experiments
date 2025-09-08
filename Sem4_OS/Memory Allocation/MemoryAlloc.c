#include <stdio.h>
#include <limits.h>
void firstfit(int n, int partitionSize[], int m, int processSize[]) {
    int i, j, alloc[m];
    int ogpartition[n];
    for(i = 0; i < n; i++) {
        ogpartition[i] = partitionSize[i];
    }
    for(i = 0; i < m; i++) {
        alloc[i] = -1;
        for(j = 0; j < n; j++) {
            if(partitionSize[j] >= processSize[i]) {
                alloc[i] = j;
                partitionSize[j] = -1;
                break;
            }
        }
    }
    printf("\nProcess no\tProcess size\tPartition allocated\tHole created\tCan utilize hole?\n");
    for(i = 0; i < m; i++) {
        printf("%d\t\t%d\t\t", i + 1, processSize[i]);
        if(alloc[i] != -1) {
            int hole = ogpartition[alloc[i]] - processSize[i];
            printf("%d\t\t\t%d\t\t", alloc[i] + 1, hole);
            int found = 0;
            for(j = 0; j < m; j++) {
                if(alloc[j] == -1 && processSize[j] <= hole) {
                    printf("Yes (Process %d)", j + 1);
                    found = 1;
                    break;
                }
            }
            if(!found) {
                printf("No");
            }
        }
        else {
            printf("Not allocated\t\t-\t\t-");
        }
        printf("\n");
    }
}

void bestfit(int n, int partitionSize[], int m, int processSize[]) {
    int i, j, alloc[m];
    int ogpartition[n];
    for(i = 0; i < n; i++) {
        ogpartition[i] = partitionSize[i];
    }
    for(i = 0; i < m; i++) {
        int min = INT_MAX;
        int bestIndex = -1;
        for(j = 0; j < n; j++) {
            int diff = partitionSize[j] - processSize[i];
            if(diff >= 0 && diff < min) {
                min = diff;
                bestIndex = j;
            }
        }
        if(bestIndex != -1) {
            alloc[i] = bestIndex;
            partitionSize[bestIndex] = INT_MAX; // mark as allocated
        }
        else {
            alloc[i] = -1; // not allocated
        }
    }
    printf("\nProcess No.\tProcess Size\tPartition Allocated\tHole Created\tCan Utilize Hole?\n");
    for(int i = 0; i < m; i++) {
        printf("%d\t\t%d\t\t", i + 1, processSize[i]);
        if(alloc[i] != -1) {
            int hole = ogpartition[alloc[i]] - processSize[i];
            printf("%d\t\t\t%d\t\t", alloc[i] + 1, hole);
            int found = 0;
            for(int j = 0; j < m; j++) {
                if(alloc[j] == -1 && processSize[j] <= hole) {
                    printf("Yes (Process %d)", j + 1);
                    found = 1;
                    break;
                }
            }
            if(!found)
                printf("No");
        }
        else {
            printf("Not allocated\t\t-\t\t-");
        }
        printf("\n");
    }
}

void worstfit(int n, int partitionSize[], int m, int processSize[]) {
    int i, j, alloc[m];
    int ogpartition[n];
    for(i = 0; i < n; i++) {
        ogpartition[i] = partitionSize[i];
    }
    for(i = 0; i < m; i++) {
        int max = -1;
        int bestIndex = -1;
        for(j = 0; j < n; j++) {
            int diff = partitionSize[j] - processSize[i];
            if(diff > max) {
                max = diff;
                bestIndex = j;
            }
        }
        if(bestIndex != -1) {
            alloc[i] = bestIndex;
            partitionSize[bestIndex] = -1; // mark as allocated
        }
        else {
            alloc[i] = -1; // not allocated
        }
    }
    printf("\nProcess No.\tProcess Size\tPartition Allocated\tHole Created\tCan Utilize Hole?\n");
    for(int i = 0; i < m; i++) {
        printf("%d\t\t%d\t\t", i + 1, processSize[i]);
        if(alloc[i] != -1) {
            int hole = ogpartition[alloc[i]] - processSize[i];
            printf("%d\t\t\t%d\t\t", alloc[i] + 1, hole);
            int found = 0;
            for(int j = 0; j < m; j++) {
                if(alloc[j] == -1 && processSize[j] <= hole) {
                    printf("Yes (Process %d)", j + 1);
                    found = 1;
                    break;
                }
            }
            if(!found)
                printf("No");
        }
        else {
            printf("Not allocated\t\t-\t\t-");
        }
        printf("\n");
    }
}

void nextfit(int n, int partitionSize[], int m, int processSize[]) {
    int i, j, alloc[m];
    int ogpartition[n];
    for(i = 0; i < n; i++) {
        ogpartition[i] = partitionSize[i];
    }
    for(i = 0; i < m; i++) {
        alloc[i] = -1;
        for(j = 0; j < n; j++) {
            if(partitionSize[j] >= processSize[i]) {
                alloc[i] = j;
                partitionSize[j] = -1;
                break;
            }
            partitionSize[j] = -1;
        }
    }
    printf("\nProcess no\tProcess size\tPartition allocated\tHole created\tCan utilize hole?\n");
    for(i = 0; i < m; i++) {
        printf("%d\t\t%d\t\t", i + 1, processSize[i]);
        if(alloc[i] != -1) {
            int hole = ogpartition[alloc[i]] - processSize[i];
            printf("%d\t\t\t%d\t\t", alloc[i] + 1, hole);
            int found = 0;
            for(j = 0; j < m; j++) {
                if(alloc[j] == -1 && processSize[j] <= hole) {
                    printf("Yes (Process %d)", j + 1);
                    found = 1;
                    break;
                }
            }
            if(!found) {
                printf("No");
            }
        }
        else {
            printf("Not allocated\t\t-\t\t-");
        }
        printf("\n");
    }
}

int main() {
    int i, n, partitionSize[100], m, processSize[100], tempPartition[100];
    printf("Enter the no. of partitions: ");
    scanf("%d", &n);
    printf("Enter the size of partitions: ");
    for(i = 0; i < n; i++) {
        scanf("%d", &partitionSize[i]);
    }
    printf("Enter the no. of processes: ");
    scanf("%d", &m);
    printf("Enter the size of processes: ");
    for(i = 0; i < m; i++) {
        scanf("%d", &processSize[i]);
    }
    int choice;
    printf("Choose the placement algorithm: 1.First fit 2.Best fit 3. Worst fit 4. Next fit 5.Exit: ");
    do {
        printf("Enter choice: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                for(i = 0; i < n; i++)
                    tempPartition[i] = partitionSize[i]; // reset partition
                firstfit(n, tempPartition, m, processSize);
                break;
            case 2:
                for(i = 0; i < n; i++)
                    tempPartition[i] = partitionSize[i]; // reset partition
                bestfit(n, tempPartition, m, processSize);
                break;
            case 3:
                for(i = 0; i < n; i++)
                    tempPartition[i] = partitionSize[i]; // reset partition
                worstfit(n, tempPartition, m, processSize);
                break;
            case 4:
                for(i = 0; i < n; i++)
                    tempPartition[i] = partitionSize[i]; // reset partition
                nextfit(n, tempPartition, m, processSize);
                break;
            case 5:
                printf("Exiting...");
                break;
        }
    } while (choice != 5);
    return 0;
}
