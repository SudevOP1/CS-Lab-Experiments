#include<stdio.h>
// #include<conio.h>

int total_tracks = 200;
int request_queue[] = {82, 170, 43, 140, 24, 16, 190};
int no_of_requests = 7;
int initial_track = 50;

void print_sequence(int sequence[], int size) {
    int total_movement = 0, i;

    printf("%d", sequence[0]);
    for(i=1; i<size; i++) {
        printf(" -> %d", sequence[i]);
        total_movement += abs(sequence[i] - sequence[i-1]);
    }
    printf("\nTotal head movement: %d\n\n", total_movement);
}

void sort(int arr[], int size) {
    int i, j, temp;
    for(i=0; i<size-1; i++) {
        for(j=i+1; j<size; j++) {
            if(arr[j] < arr[i]) {
                temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }
}

void calc_fcfs() {
    int sequence[no_of_requests + 1];
    int i;

    sequence[0] = initial_track;
    for(i=0; i<no_of_requests; i++) {
        sequence[i+1] = request_queue[i];
    }
    printf("FCFS:\n");
    print_sequence(sequence, no_of_requests + 1);
}

void calc_sstf() {
    int visited[no_of_requests] = {0};
    int sequence[no_of_requests + 1];
    int current = initial_track;
    int min, i, j, index;
    sequence[0] = current;


    for(i=1; i<=no_of_requests; i++) {
        min = 1000000000, index = -1;
        for(j=0; j<no_of_requests; j++) {
            if(!visited[j] && abs(request_queue[j] - current) < min) {
                min = abs(request_queue[j] - current);
                index = j;
            }
        }
        visited[index] = 1;
        current = request_queue[index];
        sequence[i] = current;
    }
    printf("SSTF:\n");
    print_sequence(sequence, no_of_requests + 1);
}

void calc_scan() {
    int sorted[no_of_requests];
    int i=0, j=1, k;
    int sequence[no_of_requests + 2];
    sequence[0] = initial_track;

    for(int i=0; i<no_of_requests; i++) {
        sorted[i] = request_queue[i];
    }
    sort(sorted, no_of_requests);

    while(i<no_of_requests && sorted[i]<initial_track) {
        i++;
    }

    for(k=i; k<no_of_requests; k++) {
        sequence[j++] = sorted[k];
    }
    if(sorted[no_of_requests-1] != total_tracks-1) {
        sequence[j++] = total_tracks-1;
    }
    for(k = i-1; k>=0; k--) {
        sequence[j++] = sorted[k];
    }

    printf("SCAN:\n");
    print_sequence(sequence, j);
}

void calc_cscan() {
    int sorted[no_of_requests];
    int i=0, j=1, k;
    int sequence[no_of_requests + 3];
    sequence[0] = initial_track;

    for(int i=0; i<no_of_requests; i++) {
        sorted[i] = request_queue[i];
    }
    sort(sorted, no_of_requests);
    while(i<no_of_requests && sorted[i]<initial_track) {
        i++;
    }

    for(k=i; k<no_of_requests; k++) {
        sequence[j++] = sorted[k];
    }
    sequence[j++] = total_tracks-1;
    sequence[j++] = 0;
    for(k=0; k<i; k++) {
        sequence[j++] = sorted[k];
    }

    printf("C-SCAN:\n");
    print_sequence(sequence, j);
}

void calc_look() {
    int sorted[no_of_requests];
    int i=0, j=1, k;
    int sequence[no_of_requests + 1];
    sequence[0] = initial_track;

    for(i=0; i<no_of_requests; i++) {
        sorted[i] = request_queue[i];
    }
    sort(sorted, no_of_requests);

    
    while(i<no_of_requests && sorted[i]<initial_track) {
        i++;
    }
    for(k=i; k<no_of_requests; k++) {
        sequence[j++] = sorted[k];
    }
    for(k=i-1; k>=0; k--) {
        sequence[j++] = sorted[k];
    }

    printf("LOOK:\n");
    print_sequence(sequence, j);
}

void calc_clook() {
    int sorted[no_of_requests];
    int i=0, j=1, k;
    int sequence[no_of_requests + 1];
    sequence[0] = initial_track;

    for(i=0; i<no_of_requests; i++) {
        sorted[i] = request_queue[i];
    }
    sort(sorted, no_of_requests);

    while(i<no_of_requests && sorted[i]<initial_track) {
        i++;
    }
    for(k=i; k<no_of_requests; k++) {
        sequence[j++] = sorted[k];
    }
    for(k=0; k<i; k++) {
        sequence[j++] = sorted[k];
    }

    printf("C-LOOK:\n");
    print_sequence(sequence, j);
}

int main() {
    // clrscr();

    printf("Initial Track Position: %d\n\n", initial_track);
    calc_fcfs();
    calc_sstf();
    calc_scan();
    calc_cscan();
    calc_look();
    calc_clook();
    
    // getch();
    return 0;
}
