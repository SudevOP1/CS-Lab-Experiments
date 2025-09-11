from fsm_validator import validate_and_print_fsms

if __name__ == "__main__":
    
    init_state = "qs"
    final_state = "qbab"
    valid_states = {
        "qs":   [1, 2],
        "qa":   [1, 2],
        "qb":   [3, 2],
        "qba":  [1, 4],
        "qbab": [3, 2],
    }
    list_mapper = {
        "a": 0,
        "b": 1,
    }
    fsms = [
        "abab",
        "bab",
        "babab",
        "baa",
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
    