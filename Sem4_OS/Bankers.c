#include <stdio.h>

int main(){ 
    int m, n, i, j, k, y, flag, ind = 0; 
    int ans[20], f[20], avail[20], alloc[20][20], max[20][20], need[20][20]; 
    printf("Enter the no. of processes: "); 
    scanf("%d", &n); 
    printf("Enter the no. of resources: "); 
    scanf("%d", &m); 
    printf("Enter the allocation matrix: "); 
    for(i=0; i<n; i++){ 
        for(j=0; j<m; j++){ 
            scanf("%d", &alloc[i][j]); 
        } 
    } 
    printf("Enter the maximum matrix: "); 
    for(i=0; i<n; i++){ 
        for(j=0; j<m; j++){ 
            scanf("%d", &max[i][j]); 
        } 
    } 
    printf("Enter the available resources: "); 
    for(j=0; j<m; j++){ 
        scanf("%d", &avail[j]); 
    } 
    for(i=0; i<n; i++){ 
        for(j=0; j<m; j++){ 
            need[i][j] = max[i][j] - alloc[i][j]; 
        } 
    } 
    for(i=0; i<n; i++){  
        f[i] = 0;  // initialising all flags as 0, since no process is completed yet 
    } 
    int count = 0; 
    while(count < n){ 
        int found = 0; 
        for(i=0; i<n; i++){ 
            if(f[i] == 0){ 
                flag = 0; 
                for(j=0; j<m; j++){ 
                    if(need[i][j] > avail[j]){  //Check if processes can be satisfied by available resources 
                        flag = 1; 
                        break; 
                    } 
                } 
                if(flag == 0){  // if resources available, release them  
                    for(y=0; y<m; y++){ 
                        avail[y] = avail[y] + alloc[i][y]; 
                    } 
                    ans[ind++] = i; 
                    f[i] = 1;  // mark  process as completed 
                    found = 1; 
                    count++; 
                } 
            } 
        } 
        if(found == 0){ 
            break;  //No progress made -> unsafe state 
        } 
    } 
    if(count == n){  //to check if all processes were able to finish 
        printf("The system is in safe state\n"); 
        for(i=0; i<n-1; i++){ 
            printf("P%d->", ans[i]); 
        } 
        printf("P%d", ans[n-1]); 
    } 
    else{ 
        printf("The system is in unsafe state\n"); 
    } 
    return 0;
}