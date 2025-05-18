#include <stdio.h>
#include <conio.h>

int number_of_process = 3;

int process_no[3];
int arrival_time[3];
int burst_time[3];
int completion_time[3];
int turnaround_time[3];
int waiting_time[3];

void get_input() {
    int i;
    for(i=0; i<number_of_process; i++) {
        process_no[i] = i+1;
        printf("Enter arrival time of process %d: ", i);
        scanf("%d", &arrival_time[i]);
        printf("Enter burst   time of process %d: ", i);
        scanf("%d", &burst_time[i]);
    }
}

void calculate_arrays() {
    int i;
    completion_time[0] = arrival_time[0] + burst_time[0];

    // completion time
    for (i=1; i<number_of_process; i++) {
        if(arrival_time[i] > completion_time[i-1]) {
            completion_time[i] = arrival_time[i]      + burst_time[i];
        } else {
            completion_time[i] = completion_time[i-1] + burst_time[i];
        }
    }
    for(i=0; i<number_of_process; i++) {
        // turnaround times
        turnaround_time[i] = completion_time[i] - arrival_time[i];
        // waiting times
        waiting_time[i] = turnaround_time[i] - burst_time[i];
    }
}

void print_details() {
    int i, avg_ta=0, avg_w=0;
    printf("P No.\t\tArrivalTime\t\tBurstTime\tCompTime\tTA Time\t\tWaiting Time\n");
    for(i=0; i<number_of_process; i++) {
        avg_ta += turnaround_time[i];
        avg_w  += waiting_time[i];
        printf("P No. %d\t\t%d\t\t\t\t%d\t\t\t%d\t\t\t%d\t\t\t%d\n", 
            process_no[i],
            arrival_time[i],
            burst_time[i],
            completion_time[i],
            turnaround_time[i],
            waiting_time[i]
        );
    }
    avg_ta /= number_of_process;
    avg_w  /= number_of_process;
    printf("\nAvg Turnaround Time = %d", avg_ta);
    printf("\nAvg Waiting Time    = %d", avg_w);
}

int main() {
    // clrscr();

    get_input();
    calculate_arrays();
    
    printf("\n");
    print_details();
    
    // getch();
    return 0;
}

