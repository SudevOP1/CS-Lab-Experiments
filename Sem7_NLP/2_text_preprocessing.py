import re

import nltk
from nltk.corpus import gutenberg, stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


class Preprocessor:

    stop_words: set[str]
    lemmatizer: WordNetLemmatizer

    def __init__(self, language: str = "english") -> None:
        self.stop_words = set(stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess(self, text: str) -> list[str]:

        # lowercase so "Emma" and "emma" count as the same word.
        text = text.lower()

        # drop everything that is not a letter or whitespace.
        text = re.sub(r"[^a-z\s]", "", text)

        tokens = word_tokenize(text)

        # remove stop words like "the", "is", "and".
        filtered_tokens = [token for token in tokens if token not in self.stop_words]

        # reduce every word to its base form.
        return [self.lemmatizer.lemmatize(token) for token in filtered_tokens]


def load_corpus(file_id: str, length: int) -> str:
    return gutenberg.raw(file_id)[:length]


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

    # first 5000 characters of the corpus
    corpus = load_corpus(file_id="austen-emma.txt", length=5000)

    print("Raw Text (first 500 characters):")
    print(corpus[:500])
    print()

    preprocessor = Preprocessor()
    tokens = preprocessor.preprocess(corpus)

    # display result
    print(f"Total processed tokens: {len(tokens)}")
    print("Processed Tokens (first 20):", tokens[:20])
