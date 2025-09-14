# 8 puzzle problem solved using hill climbing algo

from hill_climbing_algo import *

def get_next_states(state: list[list[int]]) -> tuple[bool, list[list[list[int]]]|str]:
    """
    returns: success_bool, (list_of_next_states or error_msg)
    """
    try:
        row_len = len(state)
        col_len = len(state[0])
        next_states = []
        directions = [
            [-1,  0], # top
            [ 1,  0], # bottom
            [ 0, -1], # left
            [ 0,  1], # right
        ]
        for row_ind in range(row_len):
            for col_ind in range(col_len):
                if state[row_ind][col_ind] == 0:
                    for [d_row, d_col] in directions:
                        new_row, new_col = row_ind + d_row, col_ind + d_col
                        if 0 <= new_row < row_len and 0 <= new_col < col_len:
                            new_state = [row[:] for row in state]
                            (
                                new_state[new_row][new_col],
                                new_state[row_ind][col_ind],
                            ) = (
                                new_state[row_ind][col_ind],
                                new_state[new_row][new_col],
                            )
                            next_states.append(new_state)
                    break
            if len(next_states) > 0: break
        return True, next_states
    except Exception as e:
        return False, str(e)

def print_state(state: list[list[int]], end: str="\n", tab_len: int=2) -> None:
    row_len = len(state)
    col_len = len(state[0])

    # find max digit len
    max_digit_len = 0
    for row_ind in range(row_len):
        for col_ind in range(col_len):
            digit_len = len(str(state[row_ind][col_ind]))
            if digit_len > max_digit_len:
                max_digit_len = digit_len

    # print state
    print("[")
    for row_ind in range(row_len):
        print(f"{' '*tab_len}", end="")
        print(state[row_ind], end=",\n")
    print("]", end=end)

def print_states(states: list[list[list[int]]], end: str="\n", tab_len: int=2) -> None:
    if isinstance(states[0][0], int):
        print_state(states, end=end, tab_len=tab_len)
    else:
        for i, state in enumerate(states):
            print_state(state, end=", " if i != len(states) - 1 else end, tab_len=tab_len)

def get_manhatten_heu_value(state: list[list[int]], goal_state: list[list[int]]) -> tuple[bool, int|str]:
    """
    returns: success_bool, (manhatten_heu_value or error_msg)
    """

    row_len = len(state)
    col_len = len(state[0])
    heu_value = 0
    if col_len != len(goal_state[0]) or row_len != len(goal_state):
        return False, "init and goal states should be of equal length"

    def find_elem(value: int) -> tuple[bool, tuple[int, int]|str]:
        for search_row_ind in range(row_len):
            for search_col_ind in range(col_len):
                if goal_state[search_row_ind][search_col_ind] == value:
                    return True, [search_row_ind, search_col_ind]
        if debug:
            print(f"[DEBUG] elem {value} not found in goal state: ", end="")
            print_state(goal_state)
        return False, "elem not found"

    for row_ind in range(row_len):
        for col_ind in range(col_len):
            found_ok, found = find_elem(state[row_ind][col_ind])
            if not found_ok:
                return False, found
            searched_row_ind, searched_col_ind = found
            heu_value += abs(row_ind - searched_row_ind) + abs(col_ind - searched_col_ind)
    return True, heu_value

def get_euclidean_heu_value(state: list[list[int]], goal_state: list[list[int]]) -> tuple[bool, float|str]:
    """
    returns: success_bool, (manhatten_heu_value or error_msg)
    """

    row_len = len(state)
    col_len = len(state[0])
    heu_value = 0
    if col_len != len(goal_state[0]) or row_len != len(goal_state):
        return False, "init and goal states should be of equal length"

    def find_elem(value: int) -> tuple[bool, tuple[int, int]|str]:
        for search_row_ind in range(row_len):
            for search_col_ind in range(col_len):
                if goal_state[search_row_ind][search_col_ind] == value:
                    return True, [search_row_ind, search_col_ind]
        if debug:
            print(f"[DEBUG] elem {value} not found in goal state: ", end="")
            print_state(goal_state)
        return False, "elem not found"

    for row_ind in range(row_len):
        for col_ind in range(col_len):
            found_ok, found = find_elem(state[row_ind][col_ind])
            if not found_ok:
                return False, found
            searched_row_ind, searched_col_ind = found
            heu_value += ((row_ind - searched_row_ind)**2 + (col_ind - searched_col_ind)**2)**0.5
    return True, heu_value

def solve_and_print_8_puzzle(
    init_state: list[list[int]],
    goal_state: list[list[int]],
    dist_function: str = "manhatten",
) -> None:
    
    def print_solution(success: bool, final_state: list[list[int]]|str):
        if not success:
            if debug:
                print("="*40)
            print(f"something went wrong: {final_state}")
        else:
            if debug:
                print("="*40)
            print("final state = ", end="")
            print_states(final_state)
    
    allowed_dist_functions = {
        "manhatten": get_manhatten_heu_value,
        "euclidean": get_euclidean_heu_value,
    }
    if dist_function not in allowed_dist_functions.keys():
        print_solution(False, f"invalid dist_function\nallowed_dist_functions = {", ".join(allowed_dist_functions.keys())}")
    
    final_state_ok, final_state = hill_climbing_algo(
        init_state=init_state,
        goal_state=goal_state,
        heu_func=allowed_dist_functions[dist_function],
        next_states_func=get_next_states,
        states_printer_func=print_states,
    )
    print_solution(final_state_ok, final_state)

if __name__ == "__main__":
    solve_and_print_8_puzzle(
        dist_function="manhatten",
        init_state=[
            [1, 2, 3],
            [4, 0, 6],
            [7, 5, 8],
        ],
        goal_state=[
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0],
        ],
    )

