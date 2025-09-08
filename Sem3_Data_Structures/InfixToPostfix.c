// infix to postfix conversion using stack
#include <stdio.h>
// #include<conio.h>

#define LENGTH 100
char infix[LENGTH];
char postfix[LENGTH];
float st[LENGTH];
int top = -1;

void push(char num)
{
    if (top == LENGTH - 1)
        printf("Stack Full\n");
    else
        st[++top] = num;
}

char pop()
{
    if (top == -1)
    {
        printf("Stack Empty\n");
        return '\0';
    }
    return st[top--];
}

int prec(char x)
{
    if (x == '(')
        return 0;
    if (x == '+' || x == '-')
        return 1;
    if (x == '*' || x == '/')
        return 2;
    if (x == '^' || x == '%')
        return 3;
    return -1;
}

void infixtopostfix()
{
    int i = 0, j = 0;
    char x = infix[i];

    while (x != '\0')
    {

        // '(' : push
        if (x == '(')
            push(x);

        // 'operand' : push
        else if ((x >= 'A' && x <= 'Z') || (x >= 'a' && x <= 'z') || (x >= '0' && x <= '9'))
            postfix[j++] = x;

        // ')' : pop till '('
        else if (x == ')')
        {
            while (top != -1 && st[top] != '(')
                postfix[j++] = pop();
            if (top != -1)
                pop();
        }

        // 'operator' : check precedence
        else if (
            x == '+' ||
            x == '-' ||
            x == '*' ||
            x == '/' ||
            x == '^' ||
            x == '%')
        {
            while (top != -1 && prec(x) <= prec(st[top]))
                postfix[j++] = pop();
            push(x);
        }
        else
        {
            printf("Invalid Expression!\n");
            return;
        }
        x = infix[++i];
    }

    while (top != -1)
        postfix[j++] = pop();
    postfix[j] = '\0';
}

int main()
{
    // clrscr();

    int i = 0;
    printf("Enter infix expression: ");
    scanf("%99[^\n]", infix);

    infixtopostfix();

    while (postfix[i] != '\0')
    {
        printf("%c", postfix[i++]);
    }
    printf("\n");

    // getch();
    return 0;
}