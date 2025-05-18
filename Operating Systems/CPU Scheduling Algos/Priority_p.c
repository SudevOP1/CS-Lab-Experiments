#include <stdio.h>
#include <conio.h>
struct Process
{
    int id, arrival, burst, priority, remaining, completion, waiting, turnaround;
};
int main()
{
    int n, time = 0, completed = 0, min_priority, i, shortest;
    float total_waiting = 0, total_turnaround = 0;
    // clrscr();

    printf("Enter number of processes: ");
    scanf("%d", &n);
    struct Process p[n];
    for (i = 0; i < n; i++)
    {
        printf("Enter Arrival Time, Burst Time, and Priority for process %d: ", i + 1);
        scanf("%d %d %d", &p[i].arrival, &p[i].burst, &p[i].priority);
        p[i].id = i + 1;
        p[i].remaining = p[i].burst;
    }
    while (completed != n)
    {
        min_priority = 9999;
        shortest = -1;

        for (i = 0; i < n; i++)
        {
            if (p[i].arrival <= time && p[i].remaining > 0 && p[i].priority < min_priority)
            {
                min_priority = p[i].priority;
                shortest = i;
            }
        }
        if (shortest == -1)
        {
            time++;
            continue;
        }
        p[shortest].remaining--;
        time++;

        if (p[shortest].remaining == 0)
        {
            completed++;
            p[shortest].completion = time;
            p[shortest].turnaround = p[shortest].completion - p[shortest].arrival;
            p[shortest].waiting = p[shortest].turnaround - p[shortest].burst;
            total_waiting += p[shortest].waiting;
            total_turnaround += p[shortest].turnaround;
        }
    }
    printf("\nProcess\tAT\tBT\tP\tCT\tTAT\tWT\n");

    for (i = 0; i < n; i++)
    {
        printf(
            "%d\t\t%d\t%d\t%d\t%d\t%d\t%d\n",
            p[i].id, p[i].arrival, p[i].burst, p[i].priority,
            p[i].completion, p[i].turnaround, p[i].waiting);
    }

    printf("\nAverage Turnaround Time: %.2f\n", total_turnaround / n);
    printf("Average Waiting Time: %.2f\n", total_waiting / n);

    // getch();
    return 0;
}