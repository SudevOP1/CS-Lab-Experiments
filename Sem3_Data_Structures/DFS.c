// implement depth first search
#include <stdio.h>
// #include<conio.h>

int n = 8;
int adj[8][8] = {
    0, 1, 1, 1, 0, 0, 0, 0,
    1, 0, 0, 0, 1, 1, 0, 0,
    1, 0, 0, 0, 0, 0, 1, 0,
    1, 0, 0, 0, 0, 0, 0, 1,
    0, 1, 0, 0, 0, 0, 0, 1,
    0, 1, 0, 0, 0, 0, 0, 1,
    0, 0, 1, 0, 0, 0, 0, 1,
    0, 0, 0, 1, 1, 1, 1, 0

};
int visited[8];

void dfs(int v)
{
    int i;
    for (int i = 0; i < n; i++)
    {
        if (adj[v][i] == 1 && visited[i] == 0)
        {
            printf("%c ", 65 + i);
            visited[i] = 1;
            dfs(i);
        }
    }
}

int main()
{
    // clrscr();

    int i, j, v;

    // taking graph adjacency matrix input
    // printf("Enter adjacency matrix of the graph:\n");
    // for(i=0; i<n; i++) {
    //     for(j=0; j<n; j++) {
    //         scanf("%d", &adj[i][j]);
    //     }
    // }

    for (i = 0; i < n; i++)
    {
        visited[i] = 0;
    }

    printf("Enter first vertex: ");
    scanf("%d", &v);

    printf("%c ", 65 + v);
    visited[v] = 1;
    dfs(v);

    // getch();
    return 0;
}