class Grammar:
    lhs: str
    rhs: list[str]

    def __init__(self, lhs: str, rhs: list[str]) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self) -> str:
        return f"{self.lhs} -> {' '.join(self.rhs)}"


class TableEntry:

    words: list[str]
    table: list[list[dict[str, tuple]]]

    def __init__(self, words: list[str], table: list[list[dict[str, tuple]]]) -> None:
        self.words = words
        self.table = table


def build_tree(table_entry: TableEntry, i: int, j: int, symbol: str) -> str:
    probability, backpointer = table_entry.table[i][j][symbol]

    if isinstance(backpointer, str):
        return f"({symbol} {backpointer})"

    split, left, right = backpointer
    left_tree = build_tree(table_entry, i, split, left)
    right_tree = build_tree(table_entry, split + 1, j, right)
    return f"({symbol} {left_tree} {right_tree})"


def print_table_entry(table_entry: TableEntry) -> None:
    words = table_entry.words
    n = len(words)

    print("Sentence:", " ".join(words))
    print()

    # every cell rendered as its own block of lines
    cells: list[list[list[str]]] = [[[] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            cells[i][j] = [
                f"{symbol} {probability:.4g}"
                for symbol, (probability, _) in sorted(table_entry.table[i][j].items())
            ]

    # a column is as wide as the widest thing in it including header
    headers = [f"{j}: {words[j]}" for j in range(n)]
    widths = [len(headers[j]) for j in range(n)]
    for j in range(n):
        for i in range(j + 1):
            for line in cells[i][j]:
                widths[j] = max(widths[j], len(line))

    label_width = max(len(f"{i}: {words[i]}") for i in range(n))

    def rule(left: str, middle: str, right: str) -> str:
        return (
            left
            + middle.join("-" * (width + 2) for width in [label_width] + widths)
            + right
        )

    def row(label: str, columns: list[str]) -> str:
        parts = [f" {label:<{label_width}} "]
        parts += [f" {text:<{widths[j]}} " for j, text in enumerate(columns)]
        return "|" + "|".join(parts) + "|"

    print("CYK table (row = span start, column = span end):")
    print(rule("+", "+", "+"))
    print(row("", headers))
    print(rule("+", "+", "+"))

    for i in range(n):
        # tallest cell in this row decides how many lines the row needs
        height = max([len(cells[i][j]) for j in range(i, n)] + [1])
        for line in range(height):
            columns = []
            for j in range(n):
                if j < i:
                    columns.append("." * widths[j])
                elif line < len(cells[i][j]):
                    columns.append(cells[i][j][line])
                else:
                    columns.append("-" if line == 0 and not cells[i][j] else "")
            label = f"{i}: {words[i]}" if line == 0 else ""
            print(row(label, columns))
        print(rule("+", "+", "+"))

    print()
    root = table_entry.table[0][n - 1].get("S")
    if root is None:
        print("No parse found: S does not span the whole sentence.")
        return

    probability, _ = root
    print(f"Most probable parse (p = {probability:.10g}):")
    print(" ", build_tree(table_entry, 0, n - 1, "S"))


def create_table_entry(
    sentence: str,
    production_rules: list[Grammar],
    probabilities: dict,
) -> TableEntry:
    words = [word.strip(".,!?;:").lower() for word in sentence.split()]
    words = [word for word in words if word]
    n = len(words)

    # rhs (as a tuple) -> list of (lhs, probability), so a cell lookup is O(1)
    rules_by_rhs: dict[tuple, list[tuple[str, float]]] = {}
    for rule in production_rules:
        key = tuple(
            symbol.lower() if len(rule.rhs) == 1 else symbol for symbol in rule.rhs
        )
        rules_by_rhs.setdefault(key, []).append((rule.lhs, probabilities[rule]))

    table: list[list[dict[str, tuple]]] = [[{} for _ in range(n)] for _ in range(n)]

    # diagonal: unit productions A -> word
    for i, word in enumerate(words):
        for lhs, probability in rules_by_rhs.get((word,), []):
            current = table[i][i].get(lhs)
            if current is None or probability > current[0]:
                table[i][i][lhs] = (probability, word)

    # spans of increasing length: A -> B C, splitting the span every way
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for split in range(i, j):
                for left, (left_probability, _) in table[i][split].items():
                    for right, (right_probability, _) in table[split + 1][j].items():
                        for lhs, rule_probability in rules_by_rhs.get(
                            (left, right), []
                        ):
                            probability = (
                                rule_probability * left_probability * right_probability
                            )
                            current = table[i][j].get(lhs)
                            if current is None or probability > current[0]:
                                table[i][j][lhs] = (probability, (split, left, right))

    return TableEntry(words=words, table=table)


if __name__ == "__main__":

    grammar1 = Grammar(lhs="NP", rhs=["Det", "N"])
    grammar2 = Grammar(lhs="S", rhs=["NP", "VP"])
    grammar3 = Grammar(lhs="VP", rhs=["V", "NP"])
    grammar4 = Grammar(lhs="V", rhs=["includes"])
    grammar5 = Grammar(lhs="Det", rhs=["the"])
    grammar6 = Grammar(lhs="Det", rhs=["a"])
    grammar7 = Grammar(lhs="N", rhs=["price"])
    grammar8 = Grammar(lhs="N", rhs=["facemask"])

    production_rules = [
        grammar1,
        grammar2,
        grammar3,
        grammar4,
        grammar5,
        grammar6,
        grammar7,
        grammar8,
    ]

    probabilities = {
        grammar1: 0.8,
        grammar2: 0.3,
        grammar3: 0.25,
        grammar4: 0.05,
        grammar5: 0.4,
        grammar6: 0.4,
        grammar7: 0.01,
        grammar8: 0.02,
    }

    table_entry = create_table_entry(
        sentence="The price includes a facemask.",
        production_rules=production_rules,
        probabilities=probabilities,
    )
    print_table_entry(table_entry)
