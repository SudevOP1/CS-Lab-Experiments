from fsm_validator import validate_and_print_fsms

if __name__ == "__main__":
    
    init_state = "qs"
    final_state = "q011"
    valid_states = {
        "qs":   [1, 2],
        "q0":   [1, 3],
        "q1":   [1, 2],
        "q01":  [1, 4],
        "q011": [4, 4],
    }
    list_mapper = {
        "0": 0,
        "1": 1,
    }
    fsms = [
        "1101",
        "111",
        "0001",
        "1010",
        "111111111011",
        "011",
    ]
    
    print()
    validate_and_print_fsms(
        fsms,
        init_state,
        final_state,
        valid_states,
        list_mapper,
    )
    print()
    