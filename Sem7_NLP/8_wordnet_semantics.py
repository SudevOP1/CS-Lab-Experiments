import nltk
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import Synset


class SenseRelations:

    synset: Synset
    synonyms: list[str]
    antonyms: list[str]
    hypernyms: list[str]
    hyponyms: list[str]

    def __init__(self, synset: Synset) -> None:
        self.synset = synset

        # synonymy: other lemmas in the same synset
        self.synonyms = sorted({lemma.name() for lemma in synset.lemmas()})

        # antonymy: defined on lemmas, not on synsets
        self.antonyms = sorted({
            antonym.name()
            for lemma in synset.lemmas()
            for antonym in lemma.antonyms()
        })

        # hypernymy: broader concepts, hyponymy: narrower concepts
        self.hypernyms = [h.name().split(".")[0] for h in synset.hypernyms()]
        self.hyponyms = [h.name().split(".")[0] for h in synset.hyponyms()[:3]]


def analyze_word(word: str, max_senses: int = 2) -> None:
    print(f"Semantic Analysis for Target Word: '{word}'")

    synsets = wordnet.synsets(word)
    if not synsets:
        print(f"No synsets found for '{word}' in WordNet.")
        return

    for i, synset in enumerate(synsets[:max_senses], 1):
        relations = SenseRelations(synset)

        print(f"\n[Sense {i}] ID: {synset.name()}")
        print(f"Definition: {synset.definition()}")
        print(f"Example Usage: {synset.examples()}")
        print(f"  Synonyms: {relations.synonyms}")
        print(f"  Antonyms: {relations.antonyms or 'None explicitly listed for this sense'}")
        print(f"  Hypernyms (Broader): {relations.hypernyms or 'None (Root concept)'}")
        if relations.hyponyms:
            print(f"  Hyponyms (Narrower sample): {relations.hyponyms}")


if __name__ == "__main__":

    nltk.download("wordnet", quiet=True)

    test_words = ["happy", "car", "dog"]

    for word in test_words:
        analyze_word(word)
        print("\n")
