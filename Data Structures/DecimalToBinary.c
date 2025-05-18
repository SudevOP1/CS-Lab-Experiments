// decimal to binary using stack
#include<stdio.h>
// #include<conio.h>
#include<math.h>

int stack[100];
int top = -1;
   
void push(int num) {
    stack[++top] = num;
}

void display() {
    int i;
    for (i=top; i>=0; i--) {
        printf("%d", stack[i]);
    }
}

int main() {
    // clrscr();

    int decimal_num = 0;
    int decimal_num_= 0;
    int rem         = 0;
    printf("Enter positive integer to convert to binary: ");
    scanf("%d", &decimal_num);
    decimal_num_ = decimal_num;
    while(decimal_num_ != 0) {
        rem = decimal_num_ % 2;
        decimal_num_ /= 2;
        push(rem);
    }
    display();
    
    // getch();
    return 0;
}