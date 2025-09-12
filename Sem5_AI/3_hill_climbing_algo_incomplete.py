# 8 puzzle problem

from typing import Callable
debug = True

def print_state(state: list[list[int]]):
    x_len = len(state[0])
    y_len = len(state)

    # find max digit len
    max_digit_len = 0
    for x_ind in range(x_len):
        for y_ind in range(y_len):
            digit_len = len(str(state[y_ind][x_ind]))
            if digit_len > max_digit_len:
                max_digit_len = digit_len

    # print state
    for x_ind in range(x_len):
        for y_ind in range(y_len):
            spaces = " "*(max_digit_len - len(str(state[y_ind][x_ind])))
            print(f"{spaces}{state[y_ind][x_ind]} ", end="")
        print() # for next line

def get_final_state(
    init_state: list[list[int]],
    goal_state: list[list[int]],
    heu_func: Callable,
):
    x_len = len(init_state[0])
    y_len = len(init_state)
    current_state = init_state

    # loop runs till heu of available states is more than current heu
    while True:
        
        # print current_states
        if debug:
            print("[DEBUG] current state:")
            print_state(current_state)

        # calc available states
        swappable_nums = []
        for x_ind in range(x_len):
            for y_ind in range(y_len):
                if current_state[y_ind][x_ind] == 0:
                    if y_ind > 0:       swappable_nums.append([x_ind, y_ind-1]) # top
                    if y_ind < y_len-1: swappable_nums.append([x_ind, y_ind-1]) # bottom
                    if x_ind > 0:       swappable_nums.append([x_ind-1, y_ind]) # left
                    if x_ind < x_len-1: swappable_nums.append([x_ind-1, y_ind]) # right
                    break
            if len(swappable_nums) > 0: break

        # print available states
        if debug:
            print(f"[DEBUG] swappable nums: {', '.join([str(i) for i in swappable_nums])}")
        return

        # get heu of available states
        # if heu of all available states is more than current heu, return current state
        # current state = available state with max heu


if __name__ == "__main__":
    final_state = get_final_state(
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
        heu_func=lambda x:x,
    )