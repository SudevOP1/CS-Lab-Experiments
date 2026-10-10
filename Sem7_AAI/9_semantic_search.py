import json
import os
import time
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

MODEL = "all-MiniLM-L6-v2"  # small sentence-transformers model, runs on CPU
TOP_K = 3

STORE_DIR = Path(__file__).parent / "9_vector_store"
INDEX_PATH = STORE_DIR / "docs.index"
DOCS_PATH = STORE_DIR / "docs.json"

WIDTH = 90
BOLD, DIM, RESET = "\033[1m", "\033[2m", "\033[0m"
GREEN, RED, YELLOW, CYAN = "\033[32m", "\033[31m", "\033[33m", "\033[36m"

os.system("")  # enables ANSI colours in the Windows terminal


def banner(text: str) -> None:
    print(f"\n{BOLD}{CYAN}{'=' * WIDTH}\n {text}\n{'=' * WIDTH}{RESET}")


def section(text: str) -> None:
    print(f"\n{BOLD}{text}{RESET}\n{DIM}{'-' * WIDTH}{RESET}")


def shorten(text: str, width: int = 60) -> str:
    return text if len(text) <= width else text[: width - 3] + "..."


def bar(fraction: float, width: int = 20) -> str:
    filled = round(max(fraction, 0) * width)
    colour = GREEN if fraction >= 0.75 else YELLOW if fraction >= 0.4 else RED
    return f"{colour}{'#' * filled}{DIM}{'.' * (width - filled)}{RESET}"


# the document corpus

DOCS = [  # (category, text)
    (
        "space",
        "The James Webb telescope observes infrared light from the earliest galaxies formed after the Big Bang.",
    ),
    (
        "space",
        "Mars has the largest volcano in the solar system, Olympus Mons, which is about three times the height of Everest.",
    ),
    (
        "space",
        "A black hole is a region where gravity is so strong that not even light can escape its event horizon.",
    ),
    (
        "space",
        "Astronauts on the International Space Station experience sixteen sunrises and sunsets every day.",
    ),
    (
        "health",
        "Drinking enough water helps regulate body temperature and keeps joints lubricated.",
    ),
    (
        "health",
        "Adults need seven to nine hours of sleep each night to support memory and immune function.",
    ),
    (
        "health",
        "Regular aerobic exercise such as running or cycling strengthens the heart and lowers blood pressure.",
    ),
    (
        "health",
        "Vitamin D is produced by the skin when exposed to sunlight and is important for bone strength.",
    ),
    (
        "cooking",
        "To make fluffy rice, rinse the grains until the water runs clear and let it rest after cooking.",
    ),
    (
        "cooking",
        "Searing meat on a very hot pan creates a brown crust through the Maillard reaction.",
    ),
    (
        "cooking",
        "Bread dough must be kneaded to develop gluten, which gives the loaf its chewy structure.",
    ),
    (
        "cooking",
        "Adding a pinch of salt to desserts balances sweetness and enhances the other flavours.",
    ),
    (
        "programming",
        "Python lists are dynamic arrays that can grow and shrink, while tuples are immutable.",
    ),
    (
        "programming",
        "Git lets developers track changes to source code and collaborate using branches and merges.",
    ),
    (
        "programming",
        "A REST API exposes resources over HTTP using methods like GET, POST, PUT and DELETE.",
    ),
    (
        "programming",
        "Recursion is when a function calls itself, and it needs a base case to stop.",
    ),
    (
        "finance",
        "Compound interest means you earn interest on both your savings and the interest already earned.",
    ),
    (
        "finance",
        "Diversifying investments across stocks, bonds and other assets reduces overall risk.",
    ),
    (
        "finance",
        "Inflation reduces the purchasing power of money as the prices of goods rise over time.",
    ),
    (
        "finance",
        "An emergency fund should cover three to six months of essential living expenses.",
    ),
    ("sports", "In cricket, a bowler delivers six legal balls in one over."),
    ("sports", "A marathon is a long distance running race of about 42 kilometres."),
    (
        "sports",
        "In football, a player is offside if they are nearer to the goal line than the second last defender when the ball is played.",
    ),
    ("sports", "Tennis scoring goes love, fifteen, thirty, forty and then game."),
]

# queries are paraphrased so they share few or no words with the answer doc
QUERIES = [  # (query, index of the relevant doc)
    ("Which planet has the tallest mountain?", 1),
    ("What happens if something gets too close to a collapsed star?", 2),
    ("How does the space station crew see the day and night cycle?", 3),
    ("Why should I stay hydrated?", 4),
    ("How long should a grown-up rest at night?", 5),
    ("What workouts are good for cardiovascular health?", 6),
    ("Why does a steak turn golden when fried?", 9),
    ("Why do bakers work the dough with their hands?", 10),
    ("Difference between mutable and immutable sequences in Python", 12),
    ("Tool for version control of code", 13),
    ("A function that invokes itself", 15),
    ("How can my savings grow faster over the years?", 16),
    ("Why do things cost more every year?", 18),
    ("How much cash should I keep aside for unexpected situations?", 19),
    ("How many deliveries make up a set in cricket?", 20),
    ("How far do runners go in a 26 mile race?", 21),
]


# embeddings


def embed(model: SentenceTransformer, texts: list[str]) -> np.ndarray:
    # normalised vectors, so inner product == cosine similarity
    vectors = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    return vectors.astype("float32")


def show_embedding_demo(model: SentenceTransformer) -> None:
    section("1. What an embedding looks like")
    sentences = [
        "The cat sat on the mat.",
        "A kitten is resting on the rug.",
        "The stock market fell sharply today.",
    ]
    vectors = embed(model, sentences)
    print(f"  model: {MODEL}  |  dimensions: {vectors.shape[1]}")
    preview = ", ".join(f"{v:+.3f}" for v in vectors[0][:8])
    print(f"  '{sentences[0]}'\n    -> [{preview}, ...]\n")

    print(f"  {BOLD}Cosine similarity between sentences{RESET}")
    sims = vectors @ vectors.T
    for i, s in enumerate(sentences):
        print(f"  S{i + 1} = {s}")
    print(
        BOLD
        + f"\n  {'':<6}"
        + "".join(f"{'S' + str(j + 1):>8}" for j in range(3))
        + RESET
    )
    for i in range(3):
        row = "".join(f"{sims[i, j]:>8.3f}" for j in range(3))
        print(f"  {'S' + str(i + 1):<6}{row}")
    print(
        f"\n  {DIM}S1 and S2 share almost no words but mean the same thing, so they are\n"
        f"  close in vector space. S3 is about something else and is far away.{RESET}"
    )


# vector store


def build_store(model: SentenceTransformer) -> faiss.Index:
    vectors = embed(model, [text for _, text in DOCS])
    index = faiss.IndexFlatIP(vectors.shape[1])  # exact cosine search
    index.add(vectors)

    STORE_DIR.mkdir(exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))
    docs = [{"id": i, "category": c, "text": t} for i, (c, t) in enumerate(DOCS)]
    DOCS_PATH.write_text(json.dumps(docs, indent=2), encoding="utf-8")
    return index


def load_store() -> tuple[faiss.Index, list[dict]]:
    index = faiss.read_index(str(INDEX_PATH))
    docs = json.loads(DOCS_PATH.read_text(encoding="utf-8"))
    return index, docs


def semantic_search(
    model: SentenceTransformer,
    index: faiss.Index,
    query: str,
    k: int = TOP_K,
    allowed_ids: list[int] | None = None,
) -> list[tuple[int, float]]:
    params = None
    if allowed_ids is not None:  # metadata filter, only search these vectors
        selector = faiss.IDSelectorBatch(np.array(allowed_ids, dtype="int64"))
        params = faiss.SearchParameters(sel=selector)
    scores, ids = index.search(embed(model, [query]), k, params=params)
    return [(int(i), float(s)) for i, s in zip(ids[0], scores[0]) if i != -1]


# keyword baseline


class KeywordSearch:
    """TF-IDF search, only matches on shared words."""

    def __init__(self, texts: list[str]):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query: str, k: int = TOP_K) -> list[tuple[int, float]]:
        scores = (self.matrix @ self.vectorizer.transform([query]).T).toarray().ravel()
        top = np.argsort(-scores)[:k]
        return [(int(i), float(scores[i])) for i in top]


# evaluation


def evaluate(name: str, search) -> dict:
    hits_1 = hits_k = rr = 0
    ranked = []
    print(f"  {name:<10}", end="", flush=True)
    for query, expected in QUERIES:
        results = search(query)
        ids = [i for i, _ in results]
        rank = ids.index(expected) + 1 if expected in ids else None
        hits_1 += rank == 1
        hits_k += rank is not None
        rr += 1 / rank if rank else 0
        ranked.append((results, rank))
        mark = (
            f"{GREEN}+{RESET}"
            if rank == 1
            else f"{YELLOW}~{RESET}" if rank else f"{RED}x{RESET}"
        )
        print(mark, end="", flush=True)
    print()
    n = len(QUERIES)
    return {
        "ranked": ranked,
        "hit@1": hits_1 / n,
        f"hit@{TOP_K}": hits_k / n,
        "mrr": rr / n,
    }


# report


def show_search(docs: list[dict], query: str, results: list[tuple[int, float]]) -> None:
    print(f"\n  {BOLD}Q: {query}{RESET}")
    for rank, (i, score) in enumerate(results, start=1):
        doc = docs[i]
        print(
            f"    {rank}. {score:.3f}  {DIM}[{doc['category']:<11}]{RESET} {shorten(doc['text'], 62)}"
        )


def show_comparison(docs: list[dict], results: dict) -> None:
    section(f"5. Rank of the correct doc per query (top {TOP_K}, - = not found)")
    names = list(results)
    print(BOLD + f"  {'query':<52}" + "".join(f"{n:>11}" for n in names) + RESET)
    for q_index, (query, _) in enumerate(QUERIES):
        row = f"  {shorten(query, 50):<52}"
        for name in names:
            rank = results[name]["ranked"][q_index][1]
            colour = GREEN if rank == 1 else YELLOW if rank else RED
            row += f"{colour}{rank or '-':>11}{RESET}"
        print(row)


def show_summary(results: dict) -> None:
    section("6. Summary (higher is better)")
    print(
        BOLD
        + f"  {'method':<12}{'hit@1':>8}  {'':<20}{f'hit@{TOP_K}':>8}{'MRR':>8}"
        + RESET
    )
    for name, r in results.items():
        print(
            f"  {name:<12}{r['hit@1']:>8.0%}  {bar(r['hit@1'])}"
            f"{r[f'hit@{TOP_K}']:>8.0%}{r['mrr']:>8.2f}"
        )
    print(
        f"\n  {DIM}hit@1  = correct doc ranked first\n"
        f"  hit@{TOP_K}  = correct doc somewhere in the top {TOP_K}\n"
        f"  MRR    = mean reciprocal rank (1 / rank of the correct doc){RESET}"
    )


if __name__ == "__main__":
    banner(f"Embeddings and semantic search  |  model: {MODEL}  |  store: FAISS")

    start = time.perf_counter()
    model = SentenceTransformer(MODEL)
    print(f"  loaded embedding model in {time.perf_counter() - start:.1f}s")

    show_embedding_demo(model)

    section("2. Build and persist the vector store")
    start = time.perf_counter()
    build_store(model)
    print(f"  embedded {len(DOCS)} docs in {time.perf_counter() - start:.2f}s")
    print(f"  saved index -> {INDEX_PATH.relative_to(Path(__file__).parent)}")
    print(f"  saved docs  -> {DOCS_PATH.relative_to(Path(__file__).parent)}")

    index, docs = load_store()  # reload from disk, like a real vector db
    print(f"  reloaded index: {index.ntotal} vectors of {index.d} dimensions")

    section(f"3. Semantic search (top {TOP_K}, score = cosine similarity)")
    for query, _ in QUERIES[:4]:
        show_search(docs, query, semantic_search(model, index, query))

    section("4. Search with a metadata filter")
    query = "Is running long distances good for me?"
    show_search(
        docs, query + "  (all categories)", semantic_search(model, index, query)
    )
    health_ids = [d["id"] for d in docs if d["category"] == "health"]
    show_search(
        docs,
        query + "  (category = health)",
        semantic_search(model, index, query, allowed_ids=health_ids),
    )

    section("Evaluating  (+ rank 1, ~ in top k, x missed, one mark per query)")
    keyword = KeywordSearch([d["text"] for d in docs])
    results = {
        "keyword": evaluate("keyword", keyword.search),
        "semantic": evaluate("semantic", lambda q: semantic_search(model, index, q)),
    }

    show_comparison(docs, results)
    show_summary(results)

    best = max(results, key=lambda n: (results[n]["hit@1"], results[n]["mrr"]))
    banner(f"Best method: {best}  ({results[best]['hit@1']:.0%} hit@1)")
