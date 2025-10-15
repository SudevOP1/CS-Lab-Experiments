from collections import deque

eps = "ε"


class CFG:

    def __init__(self, grammar: dict, start_sym: str):
        self.grammar = grammar
        self.start_sym = start_sym

    def print_grammar(self) -> None:
        for lhs, rhs_list in self.grammar.items():
            prods = []
            for rhs in rhs_list:
                prod = "".join(sym if sym != eps else eps for sym in rhs)
                prods.append(prod if prod else eps)
            print(f"{lhs} -> {" | ".join(prods)}")


def simplify_grammar(cfg: CFG) -> CFG:

    def remove_useless_productions() -> None:
        reachable = set()
        productive = set()

        # find productive symbols
        changed = True
        while changed:
            changed = False
            for lhs in cfg.grammar:
                for prod in cfg.grammar[lhs]:
                    if all(sym in productive or sym.islower() for sym in prod):
                        if lhs not in productive:
                            productive.add(lhs)
                            changed = True

        # remove unproductive
        cfg.grammar = {
            lhs: [
                prod
                for prod in rhs
                if all(sym in productive or sym.islower() for sym in prod)
            ]
            for lhs, rhs in cfg.grammar.items()
            if lhs in productive
        }

        # find reachable symbols
        reachable.add(cfg.start_sym)
        queue = deque([cfg.start_sym])
        while queue:
            current = queue.popleft()
            for prod in cfg.grammar.get(current, []):
                for sym in prod:
                    if sym.isupper() and sym not in reachable:
                        reachable.add(sym)
                        queue.append(sym)

        # remove unreachable
        cfg.grammar = {lhs: rhs for lhs, rhs in cfg.grammar.items() if lhs in reachable}

    def remove_epsilon_productions() -> None:
        nullable = set()

        changed = True
        while changed:
            changed = False
            for lhs, rhs in cfg.grammar.items():
                for prod in rhs:
                    if (
                        all(sym in nullable or sym == "" for sym in prod)
                        and lhs not in nullable
                    ):
                        nullable.add(lhs)
                        changed = True

        new_grammar = {}
        for lhs, rhs in cfg.grammar.items():
            for prod in rhs:
                if prod == [""]:
                    continue
                if lhs not in new_grammar:
                    new_grammar[lhs] = []
                n = len(prod)
                for i in range(1 << n):
                    new_prod = [
                        prod[j]
                        for j in range(n)
                        if not ((i >> j) & 1 and prod[j] in nullable)
                    ]
                    if new_prod and new_prod not in new_grammar[lhs]:
                        new_grammar[lhs].append(new_prod)
                if all(sym in nullable for sym in prod):
                    new_grammar[lhs].append([""])

        # if the start symbol is nullable, keep eps
        if cfg.start_sym in nullable:
            new_grammar[cfg.start_sym].append([""])
        cfg.grammar = new_grammar

    def remove_unit_productions() -> None:
        new_grammar = {}
        unit_pairs = set()
        for lhs in cfg.grammar:
            unit_pairs.add((lhs, lhs))

        # find all unit pairs (A -> B)
        changed = True
        while changed:
            changed = False
            for lhs, rhs in cfg.grammar.items():
                for prod in rhs:
                    if (
                        len(prod) == 1
                        and prod[0].isupper()
                        and (lhs, prod[0]) not in unit_pairs
                    ):
                        unit_pairs.add((lhs, prod[0]))
                        changed = True

        # build new grammar without unit productions
        for A, B in unit_pairs:
            for prod in cfg.grammar.get(B, []):
                if A not in new_grammar:
                    new_grammar[A] = []
                if (
                    len(prod) != 1
                    or not prod[0].isupper()
                    and prod not in new_grammar[A]
                ):
                    new_grammar[A].append(prod)
        cfg.grammar = new_grammar

    for lhs in cfg.grammar:
        cfg.grammar[lhs] = [
            [symbol if symbol != eps else "" for symbol in prod]
            for prod in cfg.grammar[lhs]
        ]

    remove_useless_productions()
    remove_epsilon_productions()
    remove_unit_productions()
    return cfg


def simplifiy_and_print(cfg: CFG) -> None:
    print("og cfg " + "*" * 20)
    cfg.print_grammar()
    print("simplified cfg " + "*" * 20)
    simplify_grammar(cfg).print_grammar()


if __name__ == "__main__":
    simplifiy_and_print(
        CFG(
            start_sym="S",
            grammar={
                "S": [["A", "B"], ["A", "C"]],
                "A": [["a"], [eps]],
                "B": [["b"], [eps]],
                "C": [["C"]],
            },
        )
    )
