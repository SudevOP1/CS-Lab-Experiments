import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


if __name__ == "__main__":

    documents = [
        "Machine learning helps computers learn from data",
        "Artificial intelligence uses machine learning",
        "Natural language processing analyzes human language",
        "Deep learning is a branch of artificial intelligence",
    ]

    vectorizer = TfidfVectorizer()

    # rows = documents, columns = vocabulary words
    tfidf_matrix = vectorizer.fit_transform(documents).toarray()

    print("Vocabulary:")
    print(vectorizer.get_feature_names_out())

    print("\nDocument Vectors:")
    print(np.round(tfidf_matrix, 3))

    print("\nMatrix Shape:", tfidf_matrix.shape)

    # similarity of every document with every other document
    similarity = cosine_similarity(tfidf_matrix)

    print("\nCosine Similarity Matrix:")
    print(np.round(similarity, 3))

    # display result
    print("\nWord Features (tf-idf of each word across documents):")
    for word, index in vectorizer.vocabulary_.items():
        print(f"{word}: {np.round(tfidf_matrix[:, index], 3)}")
