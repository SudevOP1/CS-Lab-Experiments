from collections import defaultdict

import spacy


class HMMTagger:

    states: list[str]
    start_probabilities: dict[str, float]
    transition_probabilities: dict[str, dict[str, float]]
    emission_probabilities: dict[str, dict[str, float]]

    # probability used for unseen transitions / emissions
    SMOOTHING: float = 1e-6

    def __init__(self, train_data: list[list[tuple[str, str]]]) -> None:
        self.train(train_data)

    def train(self, train_data: list[list[tuple[str, str]]]) -> None:
        start_counts = defaultdict(int)
        transition_counts = defaultdict(lambda: defaultdict(int))
        emission_counts = defaultdict(lambda: defaultdict(int))
        tag_counts = defaultdict(int)

        for sentence in train_data:
            prev_tag = None
            for i, (word, tag) in enumerate(sentence):
                tag_counts[tag] += 1
                emission_counts[tag][word] += 1

                if i == 0:
                    start_counts[tag] += 1
                else:
                    transition_counts[prev_tag][tag] += 1
                prev_tag = tag

        self.states = list(tag_counts.keys())
        self.start_probabilities = normalize(start_counts)
        self.transition_probabilities = {
            tag: normalize(counts) for tag, counts in transition_counts.items()
        }
        self.emission_probabilities = {
            tag: normalize(counts) for tag, counts in emission_counts.items()
        }

    def transition(self, prev_tag: str, tag: str) -> float:
        return self.transition_probabilities.get(prev_tag, {}).get(tag, self.SMOOTHING)

    def emission(self, tag: str, word: str) -> float:
        return self.emission_probabilities.get(tag, {}).get(word, self.SMOOTHING)

    def viterbi(self, words: list[str]) -> list[str]:

        # V[t][state] = probability of the best path ending in state at position t
        V: list[dict[str, float]] = [{}]
        path: dict[str, list[str]] = {}

        for state in self.states:
            V[0][state] = self.start_probabilities.get(state, 0) * self.emission(state, words[0])
            path[state] = [state]

        for t in range(1, len(words)):
            V.append({})
            new_path = {}

            for state in self.states:
                probability, prev_state = max(
                    (
                        V[t - 1][prev] * self.transition(prev, state) * self.emission(state, words[t]),
                        prev,
                    )
                    for prev in self.states
                )
                V[t][state] = probability
                new_path[state] = path[prev_state] + [state]

            path = new_path

        _, final_state = max((V[-1][state], state) for state in self.states)
        return path[final_state]


def normalize(counts: dict[str, int]) -> dict[str, float]:
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}


def spacy_pos_tagging(text: str) -> None:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    print("Original Text:", text)
    print("PoS Tagging Result:")
    for token in doc:
        print(f"{token.text}: {token.pos_}")


if __name__ == "__main__":

    # part 1: pos tagging using spacy
    print("POS Tagging using spaCy")
    spacy_pos_tagging("SpaCy is a popular natural language processing library.")

    # part 2: pos tagging using hmm + viterbi
    train_data = [
        [
            ("the", "DT"),
            ("students", "NN"),
            ("pass", "VB"),
            ("the", "DT"),
            ("test", "NN"),
        ],
        [
            ("the", "DT"),
            ("students", "NN"),
            ("wait", "VB"),
            ("for", "PP"),
            ("the", "DT"),
            ("result", "NN"),
        ],
        [
            ("Teachers", "NN"),
            ("test", "VB"),
            ("students", "NN"),
        ],
    ]

    tagger = HMMTagger(train_data=train_data)

    print("\nPOS Tagging using HMM (Viterbi)")
    print("Start Probabilities:", tagger.start_probabilities)
    print("Transition Probabilities:", tagger.transition_probabilities)
    print("Emission Probabilities:", tagger.emission_probabilities)

    sentence = ["the", "students", "wait", "for", "the", "test"]
    predicted_tags = tagger.viterbi(sentence)

    # display result
    print("\nSentence:", sentence)
    print("Predicted Tags:", predicted_tags)
    for word, tag in zip(sentence, predicted_tags):
        print(f"{word}: {tag}")
