eps = "ε"

class NFA():
    def __init__(
        self,
        start: int,
        final: int,
        transitions: str = [],
    ):
        self.start = start
        self.final = final
        self.transitions = transitions
        
    def add_transition(
        self,
        start: int,
        final: int,
        expr: str,
    ):
        self.transitions.append({
            "s": start,
            "f": final,
            "expr": expr,
        })

    def print_transitions(self):
        if self.transitions:
            max_s_len = len(max([str(t["s"]) for t in self.transitions]))
            max_expr_len = len(max([t["expr"] for t in self.transitions]))
            print(f"start node --> {self.start}")
            for t in self.transitions:
                print(f'{t["s"]}{" "*(max_s_len-1)} -- {t["expr"]}{" "*(max_expr_len-1)} -> {t["f"]}')
            print(f"final node --> {self.final}")

def build_nfa(expr: str, num_states: int = 0):
    try:
        if len(expr) == 0:
            return False, "expression cannot be null", num_states
        
        # kleene star
        num_brackets = 1
        i = 1
        if expr[0] == "(":
            while num_brackets != 0 and i < len(expr):
                if expr[i] == "(":
                    num_brackets += 1
                if expr[i] == ")":
                    num_brackets -= 1
                i += 1
        if i < len(expr) and expr[i] == "*":
            
            # NFA1 = buildNFA(expr1)
            kleene_star_expr = expr[1:i-1]
            nfa1_ok, nfa1, num_states = build_nfa(kleene_star_expr, num_states)
            if not nfa1_ok:
                return False, nfa1, num_states
            
            # create new start S and new accept F
            s_state = num_states + 1
            f_state = num_states + 2
            num_states += 2
            
            # add ε-transition (S → NFA1.start), (S → F)
            nfa1.add_transition(s_state,    nfa1.start, eps)
            nfa1.add_transition(s_state,    f_state,    eps)
            
            # add ε-transition (NFA1.accept → NFA1.start), (NFA1.accept → F)
            nfa1.add_transition(nfa1.final, nfa1.start, eps)
            nfa1.add_transition(nfa1.final, f_state,    eps)
            
            # return NFA(start=S, accept=F)
            return True, NFA(s_state, f_state, nfa1.transitions), num_states
        
        # union
        
        # concatenation
        
        # most basic case
        if len(expr) == 1:
            
            # create two states s, f
            s_state = num_states + 1
            f_state = num_states + 2
            num_states += 2
            
            # add transition (s --expr--> f)
            # return NFA(start=s, accept=f, transitions)
            return True, NFA(s_state, f_state, [{
                "s":s_state,
                "f":f_state,
                "expr":expr,
            }]), num_states
        
        return False, f"invalid expression: {expr}", num_states
    except Exception as e:
        return False, str(e), num_states
    
if __name__ == "__main__":
    nfa_ok, nfa, num_states = build_nfa("(ab)*")
    if not nfa_ok:
        print(f"something went wrong: {nfa}")
    else:
        print(f"[DEBUG] transitions: {nfa.transitions}")
        nfa.print_transitions()