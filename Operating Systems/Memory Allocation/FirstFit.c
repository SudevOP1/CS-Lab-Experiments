#include<stdio.h>
#include<conio.h>

int num_of_processes = 4;
int process[];
int memory[];
int allocation[num_of_processes];
int proc_allocation[num_of_processes];

void input_memory() {
    printf("Enter memory blocks:\n");
    for(int i=0; i<num_of_processes; i++) {
        printf("Enter memory block %d: ", i+1);
        scanf("%d", &memory[i]);
    }
    printf("\n");
}

void input_process() {
    printf("Enter process memories:\n");
    for(int i=0; i<num_of_processes; i++) {
        printf("Enter process memory %d: ", i+1);
        scanf("%d", &process[i]);
    }
    printf("\n");
}

void calc_memory() {
    for(int i=0; i<num_of_processes; i++){
        proc_allocation[i] = -1;
        for(int j=0; j<num_of_processes; j++){
            if(process[i] <= memory[j] && allocation[j] == 0) {
                allocation[j] = 1;
                proc_allocation[i] = j;
                break;
            }
        }
    }
}

void disp_memories() {
    for(int i=0; i<num_of_processes; i++){
        printf("Process %d = %d", i, proc_allocation[i]);
    }
}

int main() {
    // clrscr();

    input_memories();
    input_process();
    calc_memories();    
    disp_memories();

    // getch();
    return 0;
}