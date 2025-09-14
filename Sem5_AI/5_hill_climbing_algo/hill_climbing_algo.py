# 8 puzzle problem

from typing import Callable
debug = True

def hill_climbing_algo(
    init_state: list[list[int]],
    goal_state: list[list[int]],
    heu_func: Callable,
    next_states_func: Callable,
    states_printer_func: Callable,
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
