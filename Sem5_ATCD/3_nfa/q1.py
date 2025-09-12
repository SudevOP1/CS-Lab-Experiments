eps = "ε"
debug = False

class NFA():
    def __init__(
        self,
        start: int = None,
        final: int = None,
        transitions: list[dict] = None,
    ):
        self.start = start
        self.final = final
        self.transitions = transitions if transitions is not None else []
        
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
            print(f"start node = {self.start}")
            for t in self.transitions:
                print(f'{t["s"]}{" "*(max_s_len-1)} -- {t["expr"]}{" "*(max_expr_len-1)} -> {t["f"]}')
            print(f"final node = {self.final}")

def build_nfa(expr: str, num_states: int = 0):
    """
    returns: success_bool, (nfa_obj or error_msg), num_states
    """
    try:
        def split_expr(expr: str, separator: chr):

            # find index of separator
            num_brackets = 0
            separator_index = None
            for i, char in enumerate(expr):
                if char == "(":
                    num_brackets += 1
                elif char == ")":
                    num_brackets -= 1
                elif char == separator and num_brackets == 0:
                    separator_index = i
                    break

            # find left and right part of separator
            expr1 = expr[:separator_index]
            expr2 = expr[separator_index + 1:]

            # remove extra outer paranthesis
            if expr1[0] == "(" and expr1[-1] == ")":
                expr1 = expr1[1:-1]
            if expr2[0] == "(" and expr2[-1] == ")":
                expr2 = expr2[1:-1]
            return expr1, expr2

        def get_nfa_single_letter(char: chr):
            nonlocal num_states

            # create two states s, f
            s_state = num_states + 1
            f_state = num_states + 2
            num_states += 2
            
            # add transition (s --expr--> f)
            # return NFA(start=s, final=f, transitions)
            return True, NFA(s_state, f_state, [{
                "s"     : s_state,
                "f"     : f_state,
                "expr"  : char,
            }]), num_states

        def get_nfa_kleene_star(expr: str):
            nonlocal num_states

            # NFA1 = buildNFA(expr1)
            nfa1_ok, nfa1, num_states = build_nfa(expr, num_states)
            if not nfa1_ok:
                return False, nfa1, num_states
            
            # create new start S and new final F
            s_state = num_states + 1
            f_state = num_states + 2
            num_states += 2
            
            # add ε-transition (S → NFA1.start), (S → F)
            nfa1.add_transition(s_state,    nfa1.start, eps)
            nfa1.add_transition(s_state,    f_state,    eps)
            
            # add ε-transition (NFA1.final → NFA1.start), (NFA1.final → F)
            nfa1.add_transition(nfa1.final, nfa1.start, eps)
            nfa1.add_transition(nfa1.final, f_state,    eps)
            
            # return NFA(start=S, final=F)
            return True, NFA(s_state, f_state, nfa1.transitions), num_states

        def get_nfa_union(expr1: str, expr2: str):
            nonlocal num_states
            
            # NFA1 = buildNFA(expr1)
            nfa1_ok, nfa1, num_states = build_nfa(expr1, num_states)
            if not nfa1_ok:
                return False, nfa1, num_states
            
            # NFA2 = buildNFA(expr2)
            nfa2_ok, nfa2, num_states = build_nfa(expr2, num_states)
            if not nfa2_ok:
                return False, nfa2, num_states
            
            # create new start S and new final F
            s_state = num_states + 1
            f_state = num_states + 2
            num_states += 2
            
            # creating new final_nfa (to be returned)
            final_nfa = NFA(start=s_state, final=f_state)
            for t in nfa1.transitions + nfa2.transitions:
                final_nfa.add_transition(t["s"], t["f"], t["expr"])
            
            # add ε-transition (S → NFA1.start), (S → NFA2.start)
            final_nfa.add_transition(s_state, nfa1.start, eps)
            final_nfa.add_transition(s_state, nfa2.start, eps)
            
            # add ε-transition (NFA1.final → F), (NFA2.final → F)
            final_nfa.add_transition(nfa1.final, f_state, eps)
            final_nfa.add_transition(nfa2.final, f_state, eps)
            
            # return NFA(start=S, final=F)
            return True, final_nfa, num_states

        def get_nfa_concat(expr1: str, expr2: str):
            nonlocal num_states
            
            # NFA1 = buildNFA(expr1)
            nfa1_ok, nfa1, num_states = build_nfa(expr1, num_states)
            if not nfa1_ok:
                return False, nfa1, num_states
            
            # NFA2 = buildNFA(expr2)
            nfa2_ok, nfa2, num_states = build_nfa(expr2, num_states)
            if not nfa2_ok:
                return False, nfa2, num_states
            
            # creating new final_nfa (to be returned)
            final_nfa = NFA(start=nfa1.start, final=nfa2.final)
            for t in nfa1.transitions + nfa2.transitions:
                final_nfa.add_transition(t["s"], t["f"], t["expr"])

            # add ε-transition (NFA1.final → NFA2.start)
            final_nfa.add_transition(nfa1.final, nfa2.start, eps)

            # return NFA(start=NFA1.start, final=NFA2.final)
            return True, final_nfa, num_states

        if len(expr) == 0:
            return False, "expression cannot be null", num_states
        
        # kleene star: "(expr)*"
        if expr[0] == "(":
            num_brackets = 1
            i = 1
            while num_brackets != 0 and i < len(expr):
                if expr[i] == "(":
                    num_brackets += 1
                if expr[i] == ")":
                    num_brackets -= 1
                i += 1
            if i < len(expr) and expr[i] == "*":
                return get_nfa_kleene_star(expr[1:i-1])
        
        # concatenation (.)
        # eg: "(a).(b)" or "(ab).(cd)"
        if "." in expr:
            expr1, expr2 = split_expr(expr, ".")
            return get_nfa_concat(expr1, expr2)
        
        # union (+)
        # eg: "(a)+(b)" or "(ab)+(cd)"
        if "+" in expr:
            expr1, expr2 = split_expr(expr, "+")
            return get_nfa_union(expr1, expr2)

        # multiple letters
        if (
            not any(char in set("*()+.") for char in expr)
            and len(expr) > 1
        ): return build_nfa(".".join(expr))
        
        # single letter
        if len(expr) == 1:
            return get_nfa_single_letter(expr)
        
        return False, f"invalid expression: {expr}", num_states
    except Exception as e:
        return False, str(e), num_states
    
def build_and_print_nfa(expr: str):
    print("="*30)
    print(f"NFA for \"{expr}\":")
    nfa_ok, nfa, num_states = build_nfa(expr)
    if not nfa_ok:
        print(f"something went wrong: {nfa}")
    else:
        if debug:
            print(f"[DEBUG] transitions: {nfa.transitions}")
        nfa.print_transitions()
    print("="*30)

if __name__ == "__main__":
    for expr in [
        # "aa",
        # "ab",
        # "a",
        # "(a)*",
        # "a+b",
        # "a.b",
        # "a.b.c",
        "((a.b+c)*).d",
    ]: build_and_print_nfa(expr)

