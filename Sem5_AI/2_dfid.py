debug = True

def get_char_from_ascii(char):
    return chr(char + 65)

def input_adjacency_matrix(n: int):
    adj_matrix = []
    for i in range(n):
        adj_matrix.append([])
        for j in range(n):
            adj_matrix[i].append(int(input(f"Enter elem with index {i} {j}: ")))
    return adj_matrix

def get_dfid_order(adj_matrix: list[list[int]]):
    num_nodes = len(adj_matrix)
    dfid_order = []

    def depth_limited_dfs(
        node: int,
        depth_limit: int,
        visited: list[bool],
        depth_order: list[int]
    ):
        depth_order.append(node)
        visited[node] = True
        if depth_limit == 0: return
        for adjacent in range(num_nodes):
            if adj_matrix[node][adjacent] == 1 and not visited[adjacent]:
                depth_limited_dfs(adjacent, depth_limit - 1, visited, depth_order)

    # iterative deepening
    for depth in range(num_nodes): # worst case depth = number of nodes
        visited = [False] * num_nodes
        depth_order = []
        depth_limited_dfs(0, depth, visited, depth_order)

        # printing details
        if debug:
            print("="*30)
            print(f"[DEBUG] Depth Limit {depth}")
            print(f"[DEBUG] Visited Nodes : {' -> '.join([get_char_from_ascii(i) for i in depth_order])}")

        # add unique nodes to final dfid_order
        for node in depth_order:
            if node not in dfid_order:
                dfid_order.append(node)

        if len(dfid_order) == num_nodes:
            break

    return dfid_order

def print_dfid_order(dfid_order: list[int]):
    if debug:
        print("="*30)
    print(" -> ".join(map(str, [get_char_from_ascii(i) for i in dfid_order])))

if __name__ == "__main__":
    # print_dfid_order(get_dfid_order(input_adjacency_matrix(int(input("number of elems: ")))))
    print_dfid_order(get_dfid_order([
        [0, 1, 1, 0, 0, 1, 0], # A
        [1, 0, 0, 1, 0, 0, 1], # B
        [1, 0, 0, 0, 0, 1, 0], # C
        [0, 1, 0, 0, 1, 0, 1], # D
        [0, 0, 1, 0, 0, 0, 0], # E
        [1, 0, 1, 0, 0, 0, 0], # F
        [0, 1, 0, 1, 0, 0, 0], # G
    ]))
