#include<stdio.h>
#include<stdbool.h>
// #include<conio.h>

int n = 4;
int solution[4];
int solutions[100][4];
int count = 0;

int abs(int x) {
    return x >=0 ? x : (-x);
}

bool place(int k, int i) {
    int j;
    for(j=0; j<k; j++) {
        if(
            solution[j] == i ||
            abs(solution[j]-i) == abs(j-k)
        ) {
            return 0;
        }
    }
    return 1;
}

void getNQueensSoln(int k) {
    int i, l;
    for(i=0; i<n; i++) {
        if(place(k, i)) {
            solution[k] = i;
            if(k == n-1) {
                // store the solution
                for(l=0; l<n; l++) {
                    solutions[count][l] = solution[l];
                }
                count++;
            } else {
                getNQueensSoln(k+1);
            }
        }
    }
}

void printPattern(int solution[]) {
    int i, j;
    printf("\n");
    for(i=0; i<n; i++) {
        for(j=0; j<n; j++) {
            if(solution[i] == j) {
                printf("Q  ");
            } else {
                printf(".  ");
            }
        }
        printf("\n");
    }
    printf("\n");
}

void displaySoln() {
    printf("Total solutions = %d\n", count);
    for(int i=0; i<count; i++) {
        printf("Solution %d: ", i+1);
        printPattern(solutions[i]);
    }
}

int main() {
    // clrscr();

    getNQueensSoln(0);
    displaySoln();

    // getch();
    return 0;
}