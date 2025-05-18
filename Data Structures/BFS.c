// implement breadth first search
#include <stdio.h>
// #include<conio.h>

int num_of_vertices = 8;
int front = 0, rear = -1;
int visited[8], q[8];
int adjacency_matrix[8][8] = {
    0, 1, 1, 1, 0, 0, 0, 0,
    1, 0, 0, 0, 1, 1, 0, 0,
    1, 0, 0, 0, 0, 0, 1, 0,
    1, 0, 0, 0, 0, 0, 0, 1,
    0, 1, 0, 0, 0, 0, 0, 1,
    0, 1, 0, 0, 0, 0, 0, 1,
    0, 0, 1, 0, 0, 0, 0, 1,
    0, 0, 0, 1, 1, 1, 1, 0

};

void bfs(int vertex)
{
    int i;
    for (i = 0; i < num_of_vertices; i++)
    {
        if (adjacency_matrix[vertex][i] == 1 && visited[i] == 0)
        {
            q[++rear] = i;
            visited[i] = 1;
            printf("%c ", 65 + i);
        }
    }
    if (front <= rear)
    {
        bfs(q[front++]);
    }
}

int main()
{
    // clrscr();

    int i, j, vertex;

    // taking graph adjacency matrix input
    // printf("Enter adjacency matrix of the graph: ");
    // for(i = 0; i < num_of_vertices; i++) {
    //     for(j = 0; j < num_of_vertices; j++) {
    //         scanf("%d", &adjacency_matrix[i][j]);
    //     }
    // }

    for (i = 0; i < num_of_vertices; i++)
    {
        visited[i] = 0;
    }

    printf("Enter starting vertex: ");
    scanf("%d", &vertex);
    visited[vertex] = 1;

    printf("BFS:\n");
    printf("%c ", 65 + vertex);
    bfs(vertex);

    // getch();
    return 0;
}
