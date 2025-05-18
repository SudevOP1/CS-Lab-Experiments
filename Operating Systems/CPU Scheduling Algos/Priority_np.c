#include <stdio.h>
#define n 3
void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}
void priority(int prio[], int bt[], int process[])
{

    for (int i = 0; i < n; i++)
    {

        int a = prio[i];
        int m = i;

        for (int j = i; j < n; j++)
        {
            if (a < prio[j])
            {
                a = prio[j];
                m = j;
            }
        }

        swap(&prio[i], &prio[m]);
        swap(&bt[i], &bt[m]);
        swap(&process[i], &process[m]);
    }
}
int completionTime(int bt[], int ct[], int at[])
{
    int temp = 0;

    for (int i = 0; i < n; i++)
    {
        temp += bt[i];
        ct[i] = at[i] + temp;
    }
}
int turnAroundTime(int ct[], int at[], int tat[])
{
    for (int i = 0; i < n; i++)
    {
        tat[i] = ct[i] - at[i];
    }
}
int waitingTime(int tat[], int bt[], int wt[])
{
    for (int i = 0; i < n; i++)
    {
        wt[i] = tat[i] - bt[i];
    }
}
int main()
{
    int process[n] = {1, 2, 3};
    int at[n] = {0, 0, 0};
    int prio[n] = {4, 2, 3};
    int bt[n] = {24, 3, 3};
    int ct[n];
    int tat[n];
    int wt[n];

    // clrscr();

    priority(prio, bt, process);
    completionTime(bt, ct, at);
    turnAroundTime(ct, at, tat);
    waitingTime(tat, bt, wt);

    printf("Process\t\tPriority\tAT\t\tBT\t\tCT\t\tTAT\t\tWT\n");
    for (int i = 0; i < n; i++)
    {
        printf(" %d\t\t\t%d\t\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\n", process[i], prio[i], at[i], bt[i], ct[i], tat[i],
               wt[i]);
    }
    int totalTAT = 0, totalWT = 0;
    for (int i = 0; i < n; i++)
    {
        totalTAT += tat[i];
        totalWT += wt[i];
    }
    float avgTAT = (float)totalTAT / (float)n;
    float avgWT = (float)totalWT / (float)n;
    printf("Average turn around time = %f \n", avgTAT);
    printf("Average waiting time     = %f", avgWT);

    // getch();
    return 0;
}
