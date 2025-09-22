import random, time
from eight_puzzle import *

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0],
]

def is_global_maxima(state: list[list[int]]) -> bool:
    return state == goal_state

def create_random_state() -> list[list[int]]:
    order = random.sample(range(9), 9)
    state = [order[i:i+3] for i in range(0, 9, 3)]
    if is_global_maxima(state):
        return create_random_state()
    return state

def test_8_puzzle(num_tries: int, print_iterations: bool = True) -> None:
    num_global_maximas = 0
    num_local_maximas = 0

    for i in range(num_tries):
        print(f"iteration {i+1}: ", end="")
        random_state = create_random_state()

        s_time = time.time()
        final_state_ok, final_state = hill_climbing_algo(
            init_state=random_state,
            goal_state=goal_state,
            heu_func=get_manhatten_heu_value,
            next_states_func=get_next_states,
            states_printer_func=print_states,
        )
        f_time = time.time()

        if not final_state_ok:
            print(f"something went wrong: {final_state}")
            exit()

        if is_global_maxima(final_state):
            num_global_maximas += 1
            print("global, ", end="")
        else:
            num_local_maximas += 1
            print("local , ", end="")
        
        ms_time = (f_time-s_time) * 1000
        print(f"{ms_time:.3f}ms")

    print(f"out of {num_tries} tries:")
    print(f"num_global_maximas = {num_global_maximas}")
    print(f"num_local_maximas  = {num_local_maximas}")

if __name__ == "__main__":
    num_tries = 100
    test_8_puzzle(num_tries, True)
