def input_adjacency_matrix(n: int):
    adj_matrix = []
    for i in range(n):
        adj_matrix.append([])
        for j in range(n):
            adj_matrix[i].append(int(input(f"Enter elem with index {i} {j}: ")))
    return adj_matrix

def get_bfs_order(adj_matrix: list[list[int]]):
    num_nodes = len(adj_matrix)
    current_node = 0
    queue = [current_node,]
    bfs_order = []
    visited = [False for i in range(num_nodes)]
    visited[current_node] = True
    
    while len(queue) > 0:
        current_node = queue[0]
        queue = queue[1:]
        bfs_order.append(current_node)
        
        for adjacent_node in range(num_nodes):
            if adj_matrix[current_node][adjacent_node] == 1 and not visited[adjacent_node]:
                queue.append(adjacent_node)
                visited[adjacent_node] = True
        
    return bfs_order

def print_bfs_order(bfs_order: list[int]):
    print(" -> ".join(map(str, bfs_order)))

if __name__ == "__main__":
    print_bfs_order(get_bfs_order(input_adjacency_matrix(int(input("number of elems: ")))))
    # print_bfs_order(get_bfs_order([
    #     [0, 1, 1, 0, 0, 1, 0],
    #     [1, 0, 0, 1, 0, 0, 1],
    #     [1, 0, 0, 0, 0, 1, 0],
    #     [0, 1, 0, 0, 1, 0, 1],
    #     [0, 0, 1, 0, 0, 0, 0],
    #     [1, 0, 1, 0, 0, 0, 0],
    #     [0, 1, 0, 1, 0, 0, 0],
    # ]))