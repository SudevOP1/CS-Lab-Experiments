import re
from collections import Counter, defaultdict

import nltk
from nltk.corpus import gutenberg, stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.util import ngrams


class NgramModel:

    n: int
    vocab: set[str]
    ngram_counts: dict[tuple, Counter]

    def __init__(self, n: int, sentences: list[list[str]]) -> None:
        self.n = n
        self.vocab = set()
        self.ngram_counts = defaultdict(Counter)
        self.train(sentences)

    def train(self, sentences: list[list[str]]) -> None:
        for sentence in sentences:
            self.vocab.update(sentence)
            for i in range(len(sentence) - self.n + 1):
                context = tuple(sentence[i : i + self.n - 1])
                next_word = sentence[i + self.n - 1]
                self.ngram_counts[context][next_word] += 1

    def predict_next(
        self, context_words: list[str], top_k: int = 3
    ) -> list[tuple[str, float]]:

        # only the last n - 1 words matter for an n-gram model.
        context = tuple(context_words[-(self.n - 1) :]) if self.n > 1 else ()
        counts = self.ngram_counts.get(context, Counter())
        total = sum(counts.values())
        V = len(self.vocab)

        # laplace (add-one) smoothing so unseen words do not get zero probability.
        scored = [(word, (counts[word] + 1) / (total + V)) for word in self.vocab]
        # ties are broken alphabetically so the output is the same on every run.
        scored.sort(key=lambda pair: (-pair[1], pair[0]))

        # a sentence start marker can never be the next word.
        scored = [(word, p) for word, p in scored if word != "<s>"]
        return scored[:top_k]


def preprocess(text: str) -> list[str]:
    text = re.sub(r"[^a-z\s]", "", text.lower())
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    return [
        lemmatizer.lemmatize(token)
        for token in word_tokenize(text)
        if token not in stop_words
    ]


def load_sentences(text: str) -> list[list[str]]:
    sentences = []
    for line in text.strip().splitlines():
        line = line.strip().lower()
        if not line:
            continue
        tokens = re.findall(r"[a-z']+", line)
        sentences.append(["<s>"] + tokens + ["</s>"])
    return sentences


def format_predictions(predictions: list[tuple[str, float]]) -> str:
    return ", ".join(f"{word} ({p:.3f})" for word, p in predictions) or "(no data)"


if __name__ == "__main__":

    for resource in [
        "gutenberg",
        "punkt",
        "punkt_tab",
        "stopwords",
        "wordnet",
        "omw-1.4",
    ]:
        nltk.download(resource, quiet=True)

    # part 1: n-gram frequencies on a real corpus
    tokens = preprocess(gutenberg.raw("austen-emma.txt")[:5000])

    print("N-gram Frequencies (austen-emma.txt, first 5000 characters)")
    for n, name in [(1, "Unigrams"), (2, "Bigrams"), (3, "Trigrams")]:
        grams = list(ngrams(tokens, n))
        frequency = Counter(grams)
        print(f"\nSample {name}:", grams[:5])
        print(f"Most common {name.lower()}:", frequency.most_common(10))

    # part 2: next word prediction on a small corpus
    corpus = """
    the quick brown fox jumps over the lazy dog
    the dog barks at the quick fox
    the fox runs into the deep forest
    the forest is dark and quiet at night
    a quick fox and a lazy dog become friends
    the lazy dog sleeps under the old tree
    the old tree stands near the deep forest
    birds sing in the forest every morning
    the quick brown fox loves to run in the forest
    the dog and the fox play near the old tree
    every night the forest becomes quiet and dark
    the quick fox jumps over the sleeping dog
    in the morning the birds sing near the tree
    the lazy dog and the quick fox are best friends
    the deep forest is home to many quiet animals
    """

    sentences = load_sentences(corpus)

    unigram = NgramModel(n=1, sentences=sentences)
    bigram = NgramModel(n=2, sentences=sentences)
    trigram = NgramModel(n=3, sentences=sentences)

    test_contexts = [
        ["the", "quick"],
        ["the", "lazy"],
        ["the", "deep"],
        ["a", "quick"],
        ["the", "old", "tree"],
        ["the", "dog", "and", "the"],
    ]

    print("\n\nNext Word Prediction")
    print(f"Corpus: {len(sentences)} sentences\n")

    # display result
    for context in test_contexts:
        print(f"Context: {' '.join(context)!r}")
        print(f"  Unigram  -> {format_predictions(unigram.predict_next(context))}")
        print(f"  Bigram   -> {format_predictions(bigram.predict_next(context))}")
        print(f"  Trigram  -> {format_predictions(trigram.predict_next(context))}")
        print()
