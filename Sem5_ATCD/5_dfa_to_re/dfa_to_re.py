

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
        # TODO
        return True

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

    if not dfa.is_valid(): return "dfa invalid"
    cache_dict = {}
    visited = []
    
    def dfa_to_re_of_node(node: int) -> str:

        if node in cache_dict.keys() and cache_dict[node]["q"] is not None:
            return cache_dict[node]["p"] + cache_dict[node]["q"]
        
        cache_dict[node] = { "p": None, "q": None }
        p_stack = []
        q_stack = []

        # get p and q stack
        incoming_transitions_of_node = [t for t in dfa.transitions if t["f"] == node]
        for transition in incoming_transitions_of_node:
            if transition["s"] == node:
                p_stack.append(transition)
            else:
                q_stack.append(transition)

        # solve p stack
        p_expr: str
        if node in visited:
            p_expr = cache_dict["p"]
        else:
            p_expr = "(" + "+".join([f"({t['expr']})" for t in p_stack]) + ")*"
            cache_dict["p"] = p_expr

        # solve q stack
        q_expr = "(" + "+".join([f"({dfa_to_re_of_node(t['s'])}{t['expr']})" for t in q_stack]) + ")"
        cache_dict["q"] = q_expr

        return q_expr + p_expr

    def clean_re(re: str) -> str:
        return re

    return clean_re(dfa_to_re_of_node(dfa.final))


if __name__ == "__main__":
    
    # test case
    my_dfa = DFA(start=1, final=3, transitions=[
        {"s": 1, "f": 1, "expr": "a"},
        {"s": 1, "f": 2, "expr": "b"},
        {"s": 2, "f": 2, "expr": "a"},
        {"s": 2, "f": 3, "expr": "b"},
        {"s": 3, "f": 3, "expr": "a"},
        {"s": 3, "f": 3, "expr": "b"},
    ])
    print(dfa_to_re(my_dfa))