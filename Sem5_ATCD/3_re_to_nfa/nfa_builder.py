eps = "ε"
debug = False

class NFA():
    def __init__(
        self,
        start: int = None,
        final: int = None,
        transitions: list[dict] = None,
    ) -> None:
        self.start = start
        self.final = final
        self.transitions = transitions if transitions is not None else []
        
    def add_transition(
        self,
        start: int,
        final: int,
        expr: str,
    ) -> None:
        t = {
            "s": start,
            "f": final,
            "expr": expr,
        }
        if t in self.transitions and debug:
            print(f"[DEBUG] duplicate transition avoided: {t}")
            return
        self.transitions.append(t)

    def print_transitions(self) -> None:
        if self.transitions:
            max_s_len = max(len(str(t["s"])) for t in self.transitions)
            max_expr_len = max(len(t["expr"]) for t in self.transitions)
            sorted_transitions = sorted(self.transitions, key=lambda x: (x["s"], x["f"], x["expr"]))

            print(f"start node = {self.start}")
            for t in sorted_transitions:
                print(f'{t["s"]}{" "*(max_s_len-len(str(t["s"])))} -- {t["expr"]}{" "*(max_expr_len-len(t["expr"]))} -> {t["f"]}')
            print(f"final node = {self.final}")

# helper functions 👇
def remove_outer_paranthesis(expr: str) -> str:
    if expr.startswith("(") and expr.endswith(")"):
        bracket_count = 0
        can_remove = True
        for i, char in enumerate(expr[1:-1]):
            if char == "(":
                bracket_count += 1
            elif char == ")":
                bracket_count -= 1
                if bracket_count < 0:
                    can_remove = False
                    break
        if can_remove and bracket_count == 0:
            expr = expr[1:-1]
    return expr

def split_expr(expr: str, separator: str) -> tuple[str|None, str|None]:

    # find index of separator at the top level (not inside parentheses)
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

    if separator_index is None:
        return None, None

    # return left and right part of separator
    expr1 = remove_outer_paranthesis(expr[:separator_index])
    expr2 = remove_outer_paranthesis(expr[separator_index + 1:])
    return expr1, expr2

def add_explicit_concats(expr: str) -> str:
    new_expr = ""
    n = len(expr)
    for i in range(n):
        new_expr += expr[i]
        # check if '.' is needed
        if i < n - 1:
            c1 = expr[i]
            c2 = expr[i + 1]
            # if c1 is a letter, ')', '*' or 'ε'
            c1_valid = c1.isalnum() or c1 in [')', '*', eps]
            # if c2 is a letter, '(', 'ε'
            c2_valid = c2.isalnum() or c2 == '(' or c2 == eps

            if c1_valid and c2_valid: new_expr += '.'
    if new_expr != expr and debug:
        print(f"[DEBUG] added explicit concats \"{expr}\" to \"{new_expr}\"")
    return new_expr

def build_and_print_nfa(expr: str) -> tuple[bool, NFA|None]:
    nfa_ok, nfa, _ = build_nfa(expr)
    if not nfa_ok:
        print(f"something went wrong: {nfa}")
    else:
        if debug:
            print(f"[DEBUG] transitions: {nfa.transitions}")
        nfa.print_transitions()
    return nfa_ok, nfa

def print_eps_closures(nfa: NFA) -> None:
    states = list(set([t["s"] for t in nfa.transitions] + [t["f"] for t in nfa.transitions]))
    for state in states:
        closure = eps_closure(state, nfa.transitions)
        print(f"{eps}-closure({state}) = {closure}")

def print_nfa_and_eps_closure(exprs:list[str]) -> None:
    print("="*50)
    for expr in exprs:
        print("="*50)

        # printing expr
        print(f"\"{expr}\"")
        print("="*10)

        # printing nfa
        print("nfa:")
        nfa_ok, nfa = build_and_print_nfa(expr)
        print("="*10)

        # printing eps closure
        if nfa_ok:
            print("epsilon closures:")
            print_eps_closures(nfa)

        print("="*50)
    print("="*50)

# main functions 👇
def build_nfa(expr: str, num_states: int = 0) -> tuple[bool, NFA|str, int]:
    """
    returns: success_bool, (nfa_obj or error_msg), num_states
    """
    try:
        if len(expr) == 0:
            return False, "expression cannot be null", num_states
        expr = expr.replace("|", "+")
        expr = remove_outer_paranthesis(expr) if expr.startswith("(") and expr.endswith(")") else expr
        expr = add_explicit_concats(expr)
        
        def get_nfa_single_letter(char: str):
            nonlocal num_states

            # create two states s, f
            s_state = num_states + 1
            f_state = num_states + 2
            num_states += 2
            
            # add transition (s --expr--> f)
            # return NFA(start=s, accept=f, transitions)
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
            
            # creating new final_nfa (to be returned)
            final_nfa = NFA(s_state, f_state, nfa1.transitions[:])
            
            # add ε-transition (S → NFA1.start), (S → F)
            final_nfa.add_transition(s_state, nfa1.start, eps)
            final_nfa.add_transition(s_state, f_state, eps)
            
            # add ε-transition (NFA1.final → NFA1.start), (NFA1.final → F)
            final_nfa.add_transition(nfa1.final, nfa1.start, eps)
            final_nfa.add_transition(nfa1.final, f_state, eps)
            
            # return NFA(start=S, accept=F)
            return True, final_nfa, num_states

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
            
            # add all transitions from both nfas
            for t in nfa1.transitions[:] + nfa2.transitions[:]:
                final_nfa.add_transition(t["s"], t["f"], t["expr"])
            
            # add ε-transition (S → NFA1.start), (S → NFA2.start)
            final_nfa.add_transition(s_state, nfa1.start, eps)
            final_nfa.add_transition(s_state, nfa2.start, eps)
            
            # add ε-transition (NFA1.final → F), (NFA2.final → F)
            final_nfa.add_transition(nfa1.final, f_state, eps)
            final_nfa.add_transition(nfa2.final, f_state, eps)
            
            # return NFA(start=S, accept=F)
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
            
            # add all transitions from both nfas
            for t in nfa1.transitions[:] + nfa2.transitions[:]:
                final_nfa.add_transition(t["s"], t["f"], t["expr"])

            # add ε-transition (NFA1.final → NFA2.start)
            final_nfa.add_transition(nfa1.final, nfa2.start, eps)

            return True, final_nfa, num_states

        # kleene star: "(expr)*"
        if expr.endswith("*"):
            # for (expr)*
            if expr.startswith("("):
                num_brackets = 1
                i = 1
                while num_brackets != 0 and i < len(expr):
                    if expr[i] == "(":
                        num_brackets += 1
                    elif expr[i] == ")":
                        num_brackets -= 1
                    i += 1
                if i == len(expr) - 1:
                    return get_nfa_kleene_star(expr[1:i-1])
            # for a*
            else:
                if len(expr) == 2:
                    return get_nfa_kleene_star(expr[0])
        
        # union (+)
        # eg: "(a)+(b)" or "(ab)+(cd)" or "ab+cd"
        if "+" in expr:
            expr1, expr2 = split_expr(expr, "+")
            if expr1 is not None:
                return get_nfa_union(expr1, expr2)
        
        # concatenation (.)
        # eg: "(a).(b)" or "(ab).(cd)" or "a.b"
        if "." in expr:
            expr1, expr2 = split_expr(expr, ".")
            if expr1 is not None:
                return get_nfa_concat(expr1, expr2)
        
        # single letter
        if len(expr) == 1 and expr not in "*()+.":
            return get_nfa_single_letter(expr)
        
        return False, f"invalid expression: {expr}", num_states
    except Exception as e:
        return False, str(e), num_states

def eps_closure(state: int, transitions: list[dict]) -> list[int]:
    closure = [state,]
    queue = [state,] # bfs
    visited = []
    while len(queue) != 0:
        current_state = queue[0]
        queue = queue[1:]
        for transition in transitions:
            s_state = transition["s"]
            f_state = transition["f"]
            expr = transition["expr"]
            if (
                s_state == current_state
                and expr == eps
                and f_state not in visited
            ):
                closure.append(f_state)
                queue.append(f_state)
    return closure

if __name__ == "__main__":
    print_nfa_and_eps_closure([
        "(ab|ba)*",
        "(a|b)*(aba)(a|b)*",
        "(0|1)*01(0|1)*10",
        "(a|b)(a|b)*(aa|bb)",
        "(0|1)*0(0|1)*0(0|1)*",

        "a",
        "(a+b)*",
        "(a|b)*abb",
        "0(0|1)*1",
        "ε",
    ])
