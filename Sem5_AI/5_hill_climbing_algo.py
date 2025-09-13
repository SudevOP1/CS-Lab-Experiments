# 8 puzzle problem

from typing import Callable
debug = True

# helper functions 👇

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
        print(f"{' '*tab_len}[", end="")
        for col_ind in range(col_len):
            spaces = " "*(max_digit_len - len(str(state[row_ind][col_ind])))
            print(f"{spaces}{state[row_ind][col_ind]}{', ' if col_ind != col_len-1 else ''}", end="")
        print("],")
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

def get_euclidean_heu_value(state: list[list[int]], goal_state: list[list[int]]) -> tuple[bool, int|str]:
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

# main function 👇

def hill_climbing_algo(
    init_state: list[list[int]],
    goal_state: list[list[int]],
    heu_func: Callable,
    next_states_func: Callable,
    states_printer_func: Callable
) -> tuple[bool, list[list[int]]|str]:
    """
    returns: success_bool, (final_state or error_msg)
    """
    
    row_len = len(init_state)
    col_len = len(init_state[0])
    current_state = init_state
    iteration = 0
    if col_len != len(goal_state[0]) or row_len != len(goal_state):
        return False, "init and goal states should be of equal length"

    # loop runs till heu of next_states is more than current heu
    while True:
        
        # print iteration and current_states
        iteration += 1
        if debug:
            print("="*40)
            print(f"[DEBUG] iteration {iteration}")
            print(f"[DEBUG] current state = ", end="")
            states_printer_func(current_state)

        # calc next_states
        next_states_ok, next_states = next_states_func(current_state)
        if not next_states_ok:
            return False, next_states

        # print next_states
        if debug:
            print(f"[DEBUG] next states = ", end="")
            states_printer_func(next_states)

        # get heu of next_states
        heu_values = []
        for state in next_states:
            heu_value_ok, heu_value = heu_func(state, goal_state)
            if not heu_value_ok:
                return False, heu_value
            heu_values.append(heu_value)
        if debug:
            print(f"[DEBUG] heu_values = {heu_values}")
        
        # if heu of all next_states is more than current heu, return current state
        current_state_heu_ok, current_state_heu = heu_func(current_state, goal_state)
        if not current_state_heu_ok:
            return False, current_state_heu
        if debug:
            print(f"[DEBUG] current state heu = {current_state_heu}")
        min_hue = min(heu_values)
        if min_hue > current_state_heu:
            if debug:
                print("="*40)
            return True, current_state

        # current state = next state with max heu
        current_state_ind = heu_values.index(min_hue)
        current_state = next_states[current_state_ind]
        if debug:
            print(f"[DEBUG] selecting next step with index {current_state_ind}")

if __name__ == "__main__":
    final_state_ok, final_state = hill_climbing_algo(
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
        heu_func=get_manhatten_heu_value,
        next_states_func=get_next_states,
        states_printer_func=print_states,
    )
    if not final_state_ok:
        if debug:
            print("="*40)
        print(f"something went wrong: {final_state}")
    else:
        if debug:
            print("="*40)
            print("final state = ", end="")
        print_states(final_state)

