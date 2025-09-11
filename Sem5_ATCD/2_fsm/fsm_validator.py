debugging = False

def mapper(
    current_state: str,
    transition: str,
    valid_states: dict,
    list_mapper: dict,
):
    if current_state not in valid_states.keys():
        raise Exception("Not a valid state")
    state_index = valid_states[current_state][list_mapper[transition]]
    return list(valid_states.keys())[state_index]

def is_valid_final_state(
    state: str,
    final_state: str,
):
    return state == final_state

def validate_fsm(
    fsm_str: str,
    init_state: str,
    final_state: str,
    valid_states: dict,
    list_mapper: dict,
):
    current_state = init_state
    for char in fsm_str:
        current_state = mapper(current_state, char, valid_states, list_mapper)
        if debugging:
            print(f"[DEBUG]: {current_state}")
    return is_valid_final_state(current_state, final_state)

def validate_and_print_fsm(
    fsm_str: str,
    init_state: str,
    final_state: str,
    valid_states: dict,
    list_mapper: dict,
):
    if validate_fsm(fsm_str, init_state, final_state, valid_states, list_mapper):
        print(f"Valid  : {fsm_str}")
    else:
        print(f"Invalid: {fsm_str}")

def validate_and_print_fsms(
    fsms: list[str],
    init_state: str,
    final_state: str,
    valid_states: dict,
    list_mapper: dict,
):
    for fsm_str in fsms:
        validate_and_print_fsm(fsm_str, init_state, final_state, valid_states, list_mapper)
    