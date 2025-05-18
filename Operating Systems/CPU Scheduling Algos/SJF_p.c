// Preemptive SJF
#include<stdio.h>
// #include<conio.h>

int number_of_processes = 3;

int process_no[3];
int arrival_time[3];
int burst_time[3];
int completion_time[3];
int turnaround_time[3];
int waiting_time[3];

void get_input() {
    int i;
    for(i=0; i<number_of_processes; i++) {
        process_no[i] = i+1;
        printf("Enter arrival time of process %d: ", i);
        scanf("%d", &arrival_time[i]);
        printf("Enter burst   time of process %d: ", i);
        scanf("%d", &burst_time[i]);
    };
}

void calculate_arrays() {
    int i, current_time, remaining_burst_time[number_of_processes];
    int completed = 0;

    // initialize remaining_burst_time
    for(i=0; i<number_of_processes; i++) {
        remaining_burst_time[i] = burst_time[i];
    }
    
    // calc completion_time for all processes
    for(current_time=0; completed<number_of_processes; current_time++) {
        int idx = -1;
        int min_remaining_time = 10000;

        // find process with minimum remaining_burst_time
        for(i=0; i<number_of_processes; i++) {
            if(remaining_burst_time[i] > 0 && arrival_time[i] <= current_time) {
                if(remaining_burst_time[i] < min_remaining_time) {
                    min_remaining_time = remaining_burst_time[i];
                    idx = i;
                }
            }
        }

        // if no process is ready to run, increment the time
        if (idx == -1) {
            continue;
        }

        remaining_burst_time[idx]--;

        // if process has finished (remaining_burst_time is 0)
        if (remaining_burst_time[idx] == 0) {
            // assign completion_time for this process
            completion_time[idx] = current_time + 1;
            completed++;  // increment number of completed processes
        }
    }

    // calc TAT, WT
    for(i=0; i<number_of_processes; i++) {
        turnaround_time[i] = completion_time[i] - arrival_time[i];
        waiting_time[i] = turnaround_time[i] - burst_time[i];
    }
}

void print_details() {
    int i, avg_ta=0, avg_w=0;
    printf("P No.\t\tArrivalTime\t\tBurstTime\tCompTime\tTA Time\t\tWaiting Time\n");
    for(i=0; i<number_of_processes; i++) {
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
    avg_ta /= number_of_processes;
    avg_w  /= number_of_processes;
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
