import re

import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity


class SenseDisambiguator:

    model: Word2Vec
    target_word: str
    sense_vectors: dict[str, np.ndarray]

    def __init__(self, model: Word2Vec, target_word: str, sense_examples: dict[str, list[str]]) -> None:
        self.model = model
        self.target_word = target_word

        # each sense is represented by the average context vector of its examples.
        self.sense_vectors = {
            sense: np.mean([self.context_vector(example) for example in examples], axis=0)
            for sense, examples in sense_examples.items()
        }

    def context_vector(self, sentence: str) -> np.ndarray:
        context_words = [
            word for word in tokenize(sentence)
            if word != self.target_word and word in self.model.wv
        ]

        if not context_words:
            return np.zeros(self.model.wv.vector_size)

        return np.mean([self.model.wv[word] for word in context_words], axis=0)

    def disambiguate(self, sentence: str) -> str | None:
        if self.target_word not in tokenize(sentence):
            print(f"Target word '{self.target_word}' is not in the sentence.")
            return None

        context = self.context_vector(sentence)

        print("\nInput sentence:", sentence)
        print("Target word:", self.target_word)
        print("\nSense similarity scores:")

        scores = {}
        for sense, prototype in self.sense_vectors.items():
            score = cosine_similarity(context.reshape(1, -1), prototype.reshape(1, -1))[0][0]
            scores[sense] = float(score)
            print(f"{sense}: {score:.4f}")

        predicted_sense = max(scores, key=scores.get)
        print("\nPredicted meaning:", predicted_sense)
        return predicted_sense


def tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-z]+\b", text.lower())


if __name__ == "__main__":

    corpus = [
        "she deposited money in the bank",
        "the bank approved the loan",
        "he opened a savings account at the bank",
        "the financial bank provides banking services",
        "they sat on the river bank",
        "the river bank was covered with grass",
        "fishermen stood along the bank of the river",
        "trees grew beside the river bank",
        "the dog chased the ball in the park",
        "the student reads a book in the library",
        "the company invested money in business",
        "water flowed along the river",
    ]

    # workers=1 and a fixed seed keep the embeddings reproducible.
    model = Word2Vec(
        sentences=[tokenize(sentence) for sentence in corpus],
        vector_size=50,
        window=4,
        min_count=1,
        workers=1,
        seed=42,
        epochs=200,
    )

    print("Word2Vec model trained successfully!")
    print("Vocabulary size:", len(model.wv))
    print("Embedding dimensions:", model.wv.vector_size)

    print("\nWORD EMBEDDINGS (first 10 dimensions)")
    for word in ["bank", "money", "river", "loan"]:
        print(f"{word}: {model.wv[word][:10]}")

    sense_examples = {
        "financial institution": [
            "she deposited money in the bank",
            "the bank approved the loan",
            "he opened a savings account at the bank",
        ],
        "land beside a river": [
            "they sat on the river bank",
            "the river bank was covered with grass",
            "fishermen stood along the bank of the river",
        ],
    }

    disambiguator = SenseDisambiguator(
        model=model,
        target_word="bank",
        sense_examples=sense_examples
    )

    test_sentences = [
        "she deposited money in the bank",
        "they sat on the river bank",
        "the bank approved the loan",
    ]

    # display result
    for sentence in test_sentences:
        disambiguator.disambiguate(sentence)
