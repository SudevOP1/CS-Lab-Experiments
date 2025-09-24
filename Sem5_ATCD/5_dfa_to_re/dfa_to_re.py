

class DFA:
    def __init__(
        self,
        transitions: list[dict] = [],
        start: int = None,
        final: int = None,
    ):
        self.transitions = transitions if transitions else []
        self.start = start if start else None
        self.final = final if final else None
            
    def __repr__(self) -> str:
        return f"start={self.start}\nfinal={self.final}\ntransitions={self.transitions}"
    
    def add_transition(self, transition: dict) -> None:
        self.transitions.append(transition)
            
    def print_transitions(self) -> None:
        for t in self.transitions:
            print(f"{t['s']} -- {t['expr']} -> {t['f']}")
    
    def is_valid(self) -> bool:
        pass

def take_dfa_input() -> DFA:
    return DFA(
        start=int(input("enter start state: ")),
        final=int(input("enter final state: ")),
        transitions=[
            {
                "s": int(input(f"enter transition {i+1} start node: ")),
                "f": int(input(f"enter transition {i+1} final node: ")),
                "expr": input(f"enter transition {i+1} expr: "),
            } for i in range(int(input("enter num transitions: ")))
        ]
    )

def dfa_to_re(dfa: DFA) -> str:

    # cache to store computed REs between states
    # cache[from][to] = RE from state.from to state.to
    cache = {}
    
    def get_direct_transitions(from_state: int, to_state: int) -> list[str]:
        expressions = []
        for t in dfa.transitions:
            if t["s"] == from_state and t["f"] == to_state:
                expressions.append(t["expr"])
        return expressions
    
    def get_all_states() -> set[int]:
        states = {dfa.start, dfa.final}
        for t in dfa.transitions:
            states.add(t["s"])
            states.add(t["f"])
        return states
    
    def compute_regex(
        from_state: int,
        to_state: int,
        visited: set[int] = None
    ) -> str:

        if visited is None:
            visited = set()
            
        # first check in cache
        if (from_state, to_state) in cache:
            return cache[(from_state, to_state)]
        
        # simplest case: direct transitions
        direct_exprs = get_direct_transitions(from_state, to_state)
        
        # self loop case
        if from_state == to_state:
            if direct_exprs:
                direct_result = "(" + "+".join(direct_exprs) + ")*"
            else:
                direct_result = ""

        # different states
        else:
            if direct_exprs:
                direct_result = "+".join(direct_exprs)
                if len(direct_exprs) > 1:
                    direct_result = "(" + direct_result + ")"
            else:
                direct_result = ""
        
        # if we're already computing this state pair,
        # return direct_result to avoid infinite recursion
        if (from_state, to_state) in visited:
            return direct_result
        
        # add current state pair to visited
        new_visited = visited | {(from_state, to_state)}
        
        # find all intermediate states, excluding from_state and to_state
        all_states = get_all_states()
        intermediate_states = all_states - {from_state, to_state}
        
        # compute paths through intermediate states
        indirect_exprs = []
        for intermediate in intermediate_states:

            # from_state -> intermediate -> to_state
            path1 = compute_regex(from_state, intermediate, new_visited)
            path2 = compute_regex(intermediate, to_state, new_visited)
            self_loop = compute_regex(intermediate, intermediate, new_visited)
            
            if path1 and path2:
                if self_loop:
                    # from -> intermediate(self_loop)* -> to
                    indirect_expr = path1 + self_loop + path2
                else:
                    indirect_expr = path1 + path2
                indirect_exprs.append(indirect_expr)
        
        # combine direct and indirect paths
        all_exprs = []
        if direct_result:
            all_exprs.append(direct_result)
        all_exprs.extend(indirect_exprs)
        
        if not all_exprs:
            result = ""
        elif len(all_exprs) == 1:
            result = all_exprs[0]
        else:
            result = "(" + "+".join(all_exprs) + ")"
        
        # save in cache
        cache[(from_state, to_state)] = result
        return result
    
    # compute regex from start to final state
    result = compute_regex(dfa.start, dfa.final)
    return clean_re(result)

def clean_re(re: str) -> str:
    if not re:
        return ""
    
    for keyword in [
        "()*",
        "()",
    ]: re = re.replace(keyword, "")
    
    return re

if __name__ == "__main__":
    
    # test case
    print(dfa_to_re(
        DFA(start=1, final=3, transitions=[
            {"s": 1, "f": 1, "expr": "0"},
            {"s": 1, "f": 2, "expr": "1"},
            {"s": 2, "f": 2, "expr": "0"},
            {"s": 2, "f": 3, "expr": "1"},
            {"s": 3, "f": 3, "expr": "0"},
            {"s": 3, "f": 3, "expr": "1"},
        ])
    ))