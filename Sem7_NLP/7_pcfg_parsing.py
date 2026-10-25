from nltk import PCFG
from nltk.parse import ViterbiParser


def parse(grammar: PCFG, sentence: str) -> None:
    parser = ViterbiParser(grammar)
    words = sentence.split()

    print(f"Input Sentence: {sentence}\n")

    best_tree = parser.parse_one(words)
    if best_tree is None:
        print("No valid parse tree found for the sentence.")
        return

    print("Most Likely Parse Tree (Viterbi Best Tree):")
    print(best_tree)

    print("\nAll Valid Parse Trees and Probabilities:")
    for tree in parser.parse(words):
        print(f"Probability: {tree.prob():.6f}")
        print(tree)
        print("-" * 30)


if __name__ == "__main__":

    # probabilities of all rules with the same lhs must sum to 1.
    grammar = PCFG.fromstring("""
        S   -> NP VP        [1.0]
        NP  -> Det N        [0.6]
        NP  -> Det N PP     [0.4]
        PP  -> P NP         [1.0]
        VP  -> V NP         [0.7]
        VP  -> V NP PP      [0.3]
        Det -> 'the'        [0.8]
        Det -> 'a'          [0.2]
        N   -> 'man'        [0.5]
        N   -> 'dog'        [0.3]
        N   -> 'park'       [0.2]
        V   -> 'saw'        [1.0]
        P   -> 'in'         [1.0]
    """)

    print("Probabilistic Parsing (PCFG) Results")
    parse(
        grammar=grammar,
        sentence="the man saw the dog in the park"
    )
