inf = 10000 # (infinity)
debug = True

def input_adjacency_matrix(n: int):
    adj_matrix = []
    for i in range(n):
        adj_matrix.append([])
        for j in range(n):
            adj_matrix[i].append(int(input(f"Enter elem with index {i} {j}: ")))
    return adj_matrix

def input_heuristic_matrix(n: int):
    return [input(f"Enter heuristic value of node {i}: ") for i in range(n)]

def get_a_star_order(adj_mat: list[list[int]], heu_mat: list[int], start_ind: int, goal_ind: int):
    try:
        num_nodes = len(adj_mat)
        if num_nodes != len(heu_mat):
            return False, "invalid heuristic or adjacency matrix"
        if goal_ind >= num_nodes or goal_ind < 0:
            return False, "invalid goal_ind"
        if start_ind >= num_nodes or start_ind < 0:
            return False, "invalid start_ind"

        g_costs = [inf] * num_nodes
        g_costs[start_ind] = 0

        # f(n) = g(n) + h(n)
        f_costs = [inf] * num_nodes
        f_costs[start_ind] = heu_mat[start_ind]

        open_set = {start_ind}
        came_from = {}

        while open_set:
            # node with minimum f_cost
            current = min(open_set, key=lambda x: f_costs[x])
            if debug:
                print(f"[DEBUG] current: {current}, f={f_costs[current]}, g={g_costs[current]}, h={heu_mat[current]}")

            if current == goal_ind:
                a_star_path = []
                while current in came_from:
                    a_star_path.append(current)
                    current = came_from[current]
                a_star_path.append(start_ind)
                a_star_path.reverse()
                return True, a_star_path

            open_set.remove(current)

            for neighbor in range(num_nodes):
                if adj_mat[current][neighbor] == inf:
                    continue # not connected

                tentative_g = g_costs[current] + adj_mat[current][neighbor]
                if tentative_g < g_costs[neighbor]:
                    came_from[neighbor] = current
                    g_costs[neighbor] = tentative_g
                    f_costs[neighbor] = tentative_g + heu_mat[neighbor]
                    open_set.add(neighbor)

        return False, "no path found"

    except Exception as e:
        return False, f"something went wrong: {e}"

def print_a_star_order(a_star_order: list[int]):
    print(" -> ".join(map(str, a_star_order)))

if __name__ == "__main__":
    # num_nodes = int(input("number of nodes: "))
    # a_star_order_ok, a_star_order = get_a_star_order(
    #     input_adjacency_matrix(num_nodes),
    #     input_heuristic_matrix(num_nodes),
    # )
    a_star_order_ok, a_star_order = get_a_star_order(
        start_ind=0, goal_ind=5,
        heu_mat=[8, 8, 8, 4, 4, 0],
        adj_mat=[
            [  0,   3,   4, inf, inf, inf],
            [inf,   0, inf,   6,  10, inf],
            [inf,   5,   0, inf,   8, inf],
            [inf, inf, inf,   0,   7,   3],
            [inf, inf, inf, inf,   0,   9],
            [inf, inf, inf, inf, inf,   0],
        ],
    )

    if not a_star_order_ok: print(a_star_order)
    else:
        if debug:
            print("="*40)
            print("Final Asnwer:")
        print_a_star_order(a_star_order)
