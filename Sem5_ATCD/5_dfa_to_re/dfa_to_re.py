

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
    pass

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