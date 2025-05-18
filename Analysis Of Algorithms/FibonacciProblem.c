#include<stdio.h>
// #include<conio.h>
#include<time.h>
#include<stdlib.h>

int n = 40;

// recursive
// O(2^n) time complexity
int fib1(int n) {
    if(n==1 || n==2) {
        return 1;
    }
    return fib1(n-2) + fib1(n-1);
}

// dynamic programming
// O(n) time complexity
int fib2(int n) {
    int i, n1, n2, n3;
    
    n1 = 1;
    n2 = 1;
    n3 = 1;
    for(i=2; i<n; i++) {
        n3 = n1 + n2;
        n1 = n2;
        n2 = n3;
    }
    return n3;
}

int main() {
    clock_t start_time, final_time;
    float time_taken;
    // clrscr();
    
    start_time = clock();
    fib1(n);
    final_time = clock();
    time_taken = ((float)(final_time - start_time)) / CLOCKS_PER_SEC;
    printf("Time for recursive fib1: %f\n", time_taken);
    
    start_time = clock();
    fib2(n);
    final_time = clock();
    time_taken = ((float)(final_time - start_time)) / CLOCKS_PER_SEC;
    printf("Time for dynamic   fib2: %f\n", time_taken);
    
    // getch();
    return 0;
}
