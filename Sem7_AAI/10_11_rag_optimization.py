import os
import re
import time
import warnings
from functools import lru_cache

warnings.filterwarnings("ignore", category=DeprecationWarning)
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

from dotenv import load_dotenv
from fastembed.rerank.cross_encoder import TextCrossEncoder
from groq import RateLimitError
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
RERANK_MODEL = (
    "BAAI/bge-reranker-base"  # ~1 GB, "Xenova/ms-marco-MiniLM-L-6-v2" is ~80 MB
)

TOP_K = 4  # chunks given to the LLM
CANDIDATES = 8  # chunks fetched per query before fusion / re-ranking
NUM_EXPANSIONS = 3  # extra queries written by the LLM

llm = ChatGroq(
    model=MODEL,
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    reasoning_effort="low",
    max_retries=5,
).with_retry(  # wait out the free tier's tokens-per-minute limit
    retry_if_exception_type=(RateLimitError,),
    wait_exponential_jitter=True,
    stop_after_attempt=10,
)

WIDTH = 90
BOLD, DIM, RESET = "\033[1m", "\033[2m", "\033[0m"
GREEN, RED, YELLOW, CYAN = "\033[32m", "\033[31m", "\033[33m", "\033[36m"

os.system("")  # enables ANSI colours in the Windows terminal


def banner(text: str) -> None:
    print(f"\n{BOLD}{CYAN}{'=' * WIDTH}\n {text}\n{'=' * WIDTH}{RESET}")


def section(text: str) -> None:
    print(f"\n{BOLD}{text}{RESET}\n{DIM}{'-' * WIDTH}{RESET}")


def indent(text: str, prefix: str = "    | ", max_lines: int = 12) -> str:
    lines = [line for line in text.strip().splitlines() if line.strip()]
    hidden = len(lines) - max_lines
    if hidden > 0:
        lines = lines[:max_lines] + [f"... ({hidden} more lines)"]
    return "\n".join(prefix + line for line in lines)


def bar(fraction: float, width: int = 20) -> str:
    filled = round(fraction * width)
    colour = GREEN if fraction >= 0.75 else YELLOW if fraction >= 0.4 else RED
    return f"{colour}{'#' * filled}{DIM}{'.' * (width - filled)}{RESET}"


def shorten(text: str, length: int = 72) -> str:
    text = " ".join(text.split())
    return text if len(text) <= length else text[: length - 3] + "..."


# knowledge base (fictional, so the LLM cannot answer from what it already knows)

KNOWLEDGE_BASE = """## Library
The central library is open from 8:00 AM to 10:00 PM on weekdays and from 10:00 AM to 6:00 PM on Saturdays. It stays closed on Sundays and public holidays. During the two weeks before end-semester exams, the reading hall stays open 24 hours.

Undergraduate students can borrow up to 4 books at a time for a period of 14 days. Postgraduate students can borrow up to 6 books for 30 days. A book can be renewed twice, online or at the counter, as long as no other student has reserved it.

Books returned after the due date attract an overdue fine of Rs 5 per day for general books and Rs 20 per day for books from the reserve section. Lost books must be replaced with the same edition or paid for at twice the current price.

## Attendance
Every student must maintain at least 75% attendance in each course, counted separately for theory and practical sessions. Attendance is updated on the student portal every Friday.

Students whose attendance falls between 65% and 75% may apply for condonation on medical or other genuine grounds. The application has to be submitted to the Head of Department with supporting documents within 7 days of returning to college. Condonation is granted at most once per semester.

Students below 65% attendance in a course are detained in that course. A detained student cannot appear for the end-semester examination of that course and must re-register for it in the next academic year.

## Examinations
Each course is evaluated through 40 marks of internal assessment and 60 marks of the end-semester examination. Internal assessment consists of two unit tests of 15 marks each and 10 marks for assignments. A student must score at least 40% in the end-semester examination and 40% overall to pass the course.

The hall ticket for the end-semester examination is issued only to students who are not detained and have cleared all dues to the institute, including library fines and hostel fees.

Students who are unhappy with their result may apply for a photocopy of the answer sheet within 5 days of the result declaration, at a fee of Rs 300 per course. After viewing the photocopy, they may apply for re-evaluation at a fee of Rs 750 per course. If the re-evaluated marks differ by more than 10%, the revised marks are final and the re-evaluation fee is refunded.

## Hostel
The institute has two boys' hostels (Vega and Rigel) and one girls' hostel (Lyra), with a total capacity of 900 students. Rooms are allotted on a first-come, first-served basis, with priority given to first-year students and students whose homes are more than 100 km from campus.

The hostel fee is Rs 85,000 per year for a shared triple room and Rs 1,10,000 per year for a double room, which covers accommodation, electricity and Wi-Fi. The mess is billed separately at Rs 4,200 per month. A refundable security deposit of Rs 10,000 is collected at admission.

Hostel gates close at 10:30 PM. Students returning after that must make an entry in the late register, and three late entries in a month are reported to the warden and to parents. Visitors are allowed in the common room only, between 4:00 PM and 7:00 PM.

## Laboratory Safety
Students must wear a lab coat and closed-toe shoes in every laboratory. In the chemistry and biotechnology laboratories, safety goggles are also compulsory and long hair must be tied back.

Food, drinks, and personal electrical appliances such as phone chargers, kettles, and extension boards are not allowed inside the chemistry laboratory, because of the risk of fire near flammable solvents. Laptops may be used in the computer and electronics labs only.

Any spill, injury, or broken glassware must be reported to the lab assistant immediately, no matter how small. The nearest fire extinguisher and eye-wash station are marked in green on the floor plan displayed at the entrance of every lab.

## Scholarships
The Merit Scholarship waives 50% of the tuition fee for students who score a CGPA of 9.0 or above in the previous academic year. It is renewed every year as long as the student keeps a CGPA of at least 8.5 and has no backlogs.

The Need-Based Scholarship covers up to 100% of the tuition fee for students whose annual family income is below Rs 4,00,000. Applicants must submit an income certificate issued by a government authority along with their last year's marksheet before 31 August.

A student cannot hold both scholarships at the same time; if eligible for both, the one with the larger benefit is awarded. Scholarships are cancelled if the student is found guilty of academic dishonesty.

## Placements
The Training and Placement Cell conducts campus recruitment from August to March for final-year students. To register, a student must have a CGPA of at least 6.0 and no active backlogs at the time of the drive.

Each student can hold only one job offer through campus placements. Once a student accepts an offer, they are no longer eligible for further drives, except for dream companies offering a package of more than Rs 12 lakh per annum, where one additional attempt is allowed.

Students who skip a drive after registering for it, without informing the cell at least 24 hours in advance, are barred from the next two drives.
"""

# (question, reference answer, facts the retrieved context must contain)
# facts are copied word for word from the knowledge base
QUESTIONS = [
    (
        "What happens if I return a library book late?",
        "An overdue fine is charged: Rs 5 per day for general books and Rs 20 "
        "per day for books from the reserve section.",
        ["Rs 5 per day", "Rs 20 per day"],
    ),
    (
        "Can I charge my phone while working in the chemistry lab?",
        "No. Personal electrical appliances such as phone chargers are not "
        "allowed in the chemistry lab because of the fire risk near flammable "
        "solvents.",
        ["such as phone chargers"],
    ),
    (
        "I missed about 30% of my classes in a course because I was sick. Can "
        "I still write the end-sem exam?",
        "Attendance is about 70%, which is between 65% and 75%, so the student "
        "can apply to the Head of Department for condonation on medical grounds "
        "with supporting documents within 7 days of returning. If condonation is "
        "granted (at most once per semester) they can appear for the exam; "
        "otherwise they are below the 75% requirement.",
        ["between 65% and 75%", "within 7 days"],
    ),
    (
        "How much will it cost me per year to live on campus in a double room, "
        "including food?",
        "Rs 1,10,000 per year for the double room plus mess at Rs 4,200 per "
        "month (Rs 50,400 per year), about Rs 1,60,400 per year, plus a "
        "refundable Rs 10,000 security deposit at admission.",
        ["Rs 1,10,000 per year for a double room", "Rs 4,200 per month"],
    ),
    (
        "My marks look wrong. How do I get my paper rechecked and what does it "
        "cost?",
        "Apply for a photocopy of the answer sheet within 5 days of the result "
        "for Rs 300 per course, then apply for re-evaluation for Rs 750 per "
        "course. If the marks change by more than 10% the fee is refunded.",
        ["Rs 300 per course", "Rs 750 per course"],
    ),
    (
        "I have a 9.2 CGPA and my family earns 3 lakh a year. Can I get both "
        "scholarships?",
        "No. A student cannot hold both scholarships at the same time. Since "
        "they qualify for both, the one with the larger benefit is awarded, the "
        "Need-Based Scholarship (up to 100% of tuition) instead of the Merit "
        "Scholarship (50%).",
        ["cannot hold both scholarships", "below Rs 4,00,000"],
    ),
    (
        "I already accepted a job offer. Can I still sit for a company offering "
        "15 LPA?",
        "Yes. Dream companies offering more than Rs 12 lakh per annum allow one "
        "additional attempt even after accepting an offer.",
        ["more than Rs 12 lakh per annum"],
    ),
    (
        "What time do I need to be back at the hostel at night?",
        "Hostel gates close at 10:30 PM. Later arrivals must sign the late "
        "register, and three late entries in a month are reported to the warden "
        "and parents.",
        ["Hostel gates close at 10:30 PM"],
    ),
    (
        "Will unpaid library fines stop me from taking my exams?",
        "Yes. The end-semester hall ticket is only issued to students who have "
        "cleared all dues, including library fines.",
        ["including library fines"],
    ),
    (
        "Does the campus have a swimming pool?",
        "The handbook does not mention a swimming pool, so this cannot be "
        "answered from it.",
        [],  # not in the knowledge base, a grounded system should say so
    ),
]

GROUNDING_DEMO = 3  # index of the question used to compare LLM-only vs RAG
TRACE_QUESTION = 2  # index of the question whose retrieval is traced

# chunking strategies


def fixed_size_chunks(text: str) -> list[Document]:
    # naive: small fixed-size chunks with no overlap and no section info
    splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)
    return splitter.create_documents([text])


def section_chunks(text: str) -> list[Document]:
    # split on headings first so no chunk mixes two topics, then size-limit
    # each section with overlap and prefix the section name to every chunk
    by_section = MarkdownHeaderTextSplitter([("##", "section")]).split_text(text)
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    return [
        Document(
            f"[{doc.metadata['section']}] {doc.page_content}", metadata=doc.metadata
        )
        for doc in splitter.split_documents(by_section)
    ]


# retrieval strategies

expand_prompt = ChatPromptTemplate.from_template(
    """You help search a college student handbook.
Rewrite the student's question into {n} different search queries.
- use the formal words a handbook would use (e.g. "overdue fine" instead of "late")
- if the question has several parts or needs a calculation, write one query per fact needed
Return only the queries, one per line, with no numbering.

Question: {question}"""
)

expand_chain = expand_prompt | llm | StrOutputParser()


@lru_cache  # both expanded pipelines reuse the same rewrites
def expand_query(question: str) -> tuple[str, ...]:
    text = expand_chain.invoke({"question": question, "n": NUM_EXPANSIONS})
    lines = [re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line) for line in text.splitlines()]
    rewrites = [line.strip() for line in lines if line.strip()]
    return (question, *rewrites[:NUM_EXPANSIONS])


def plain_retrieve(store: FAISS, question: str) -> list[Document]:
    return store.similarity_search(question, k=TOP_K)


def fused_candidates(store: FAISS, question: str) -> list[Document]:
    # reciprocal rank fusion of the results for the original + rewritten queries
    scores, docs = {}, {}
    for query in expand_query(question):
        for rank, doc in enumerate(store.similarity_search(query, k=CANDIDATES)):
            docs[doc.page_content] = doc
            scores[doc.page_content] = scores.get(doc.page_content, 0) + 1 / (60 + rank)
    return [docs[key] for key in sorted(scores, key=scores.get, reverse=True)]


def expanded_retrieve(store: FAISS, question: str) -> list[Document]:
    return fused_candidates(store, question)[:TOP_K]


def reranked_retrieve(store: FAISS, question: str) -> list[Document]:
    # the cross-encoder reads question and chunk together, so it judges
    # relevance better than the embedding distance used to fetch candidates
    candidates = fused_candidates(store, question)
    scores = reranker.rerank(question, [doc.page_content for doc in candidates])
    ranked = sorted(zip(scores, candidates), key=lambda pair: pair[0], reverse=True)
    return [doc for _, doc in ranked[:TOP_K]]


# generation

answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You answer questions from students of Orion Institute of Technology "
            "using only the handbook excerpts below. If the excerpts do not "
            "contain the answer, say you could not find it in the handbook. Do "
            "not use outside knowledge. Answer in 2-4 sentences.\n\n"
            "Handbook excerpts:\n{context}",
        ),
        ("human", "{question}"),
    ]
)

answer_chain = answer_prompt | llm | StrOutputParser()
llm_only_chain = (
    ChatPromptTemplate.from_template("Answer in 2-4 sentences.\n\n{question}")
    | llm
    | StrOutputParser()
)


def format_context(docs: list[Document]) -> str:
    return "\n\n".join(f"[{i}] {doc.page_content}" for i, doc in enumerate(docs, 1))


def rag_answer(question: str, docs: list[Document]) -> str:
    return answer_chain.invoke({"question": question, "context": format_context(docs)})


# evaluation

judge_prompt = ChatPromptTemplate.from_template(
    """You are grading a question-answering system for a college handbook.
Compare the system answer with the reference answer and rate how relevant and
correct it is on a scale of 1 to 5:
5 = answers the question fully and agrees with the reference
4 = correct but misses a minor detail
3 = partly correct or misses an important part
2 = mostly wrong or vague
1 = wrong, irrelevant, or says it does not know when the reference has an answer
If the reference says the handbook does not cover it, give 5 only if the system
also says it could not find the answer, and 1 if it makes something up.

Question: {question}
Reference answer: {reference}
System answer: {answer}

Reply with only "Score: <n>"."""
)

judge_chain = judge_prompt | llm | StrOutputParser()
SCORE_RE = re.compile(r"Score:\s*([1-5])")


def judge(question: str, reference: str, answer: str) -> int:
    reply = judge_chain.invoke(
        {"question": question, "reference": reference, "answer": answer}
    )
    match = SCORE_RE.search(reply)
    return int(match.group(1)) if match else 1


def context_recall(docs: list[Document], facts: list[str]) -> float | None:
    if not facts:
        return None
    context = " ".join(" ".join(doc.page_content.split()) for doc in docs)
    return sum(fact in context for fact in facts) / len(facts)


def score_colour(score: int) -> str:
    return GREEN if score >= 4 else YELLOW if score == 3 else RED


def evaluate(name: str, store: FAISS, retrieve) -> dict:
    per_question = []
    print(f"  {name:<20}", end="", flush=True)
    for question, reference, facts in QUESTIONS:
        start = time.perf_counter()
        docs = retrieve(store, question)
        answer = rag_answer(question, docs)
        seconds = time.perf_counter() - start
        score = judge(question, reference, answer)
        per_question.append(
            {
                "docs": docs,
                "answer": answer,
                "score": score,
                "recall": context_recall(docs, facts),
                "context_chars": len(format_context(docs)),
                "seconds": seconds,
            }
        )
        print(f" {score_colour(score)}{score}{RESET}", end="", flush=True)
    print()

    recalls = [r["recall"] for r in per_question if r["recall"] is not None]
    n = len(per_question)
    return {
        "per_question": per_question,
        "avg_score": sum(r["score"] for r in per_question) / n,
        "full_marks": sum(r["score"] == 5 for r in per_question) / n,
        "recall": sum(recalls) / len(recalls),
        "context_chars": sum(r["context_chars"] for r in per_question) / n,
        "avg_seconds": sum(r["seconds"] for r in per_question) / n,
    }


# report


def show_chunks(chunkings: dict) -> None:
    section("Chunking strategies")
    for name, chunks in chunkings.items():
        sizes = [len(c.page_content) for c in chunks]
        print(
            f"  {BOLD}{name:<12}{RESET} {len(chunks):>3} chunks, "
            f"avg {sum(sizes) / len(sizes):.0f} chars, max {max(sizes)} chars"
        )
        print(DIM + indent(chunks[2].page_content, "    | ", max_lines=4) + RESET)


def show_grounding(store: FAISS) -> None:
    question, reference, _ = QUESTIONS[GROUNDING_DEMO]
    section("Grounding: LLM alone vs basic RAG")
    print(indent(question, "  Q: "))
    print(f"  {DIM}reference: {reference}{RESET}")

    print(f"\n  {BOLD}LLM alone{RESET} (no context, has to guess)")
    print(DIM + indent(llm_only_chain.invoke({"question": question})) + RESET)

    docs = plain_retrieve(store, question)
    print(f"\n  {BOLD}Basic RAG{RESET} (top {TOP_K} chunks from FAISS)")
    for i, doc in enumerate(docs, 1):
        print(f"    {DIM}[{i}] {shorten(doc.page_content)}{RESET}")
    print(DIM + indent(rag_answer(question, docs)) + RESET)


def show_trace(results: dict) -> None:
    question, _, facts = QUESTIONS[TRACE_QUESTION]
    section(f"Retrieval trace for Q{TRACE_QUESTION + 1}")
    print(indent(question, "  Q: "))
    print(f"\n  {BOLD}expanded queries{RESET}")
    for query in expand_query(question)[1:]:
        print(f"    - {query}")

    for name, res in results.items():
        run = res["per_question"][TRACE_QUESTION]
        print(f"\n  {BOLD}{name}{RESET}  (judge score {run['score']}/5)")
        for i, doc in enumerate(run["docs"], 1):
            text = " ".join(doc.page_content.split())
            hit = any(fact in text for fact in facts)
            mark = f"{GREEN}+{RESET}" if hit else f"{DIM}.{RESET}"
            print(f"    {mark} [{i}] {DIM}{shorten(text)}{RESET}")
        print(DIM + indent(run["answer"], "      | ", max_lines=6) + RESET)
    print(f"\n  {DIM}+ = chunk contains one of the facts needed for the answer{RESET}")


def show_matrix(results: dict) -> None:
    section("Judge score per question (out of 5) [context recall]")
    names = list(results)
    print(BOLD + f"  {'Q':<6}" + "".join(f"{n:>21}" for n in names) + RESET)
    for i in range(len(QUESTIONS)):
        row = f"  {'Q' + str(i + 1):<6}"
        for name in names:
            run = results[name]["per_question"][i]
            recall = "-" if run["recall"] is None else f"{run['recall']:.0%}"
            cell = f"{run['score']} [{recall}]"
            row += f"{score_colour(run['score'])}{cell:>21}{RESET}"
        print(row)
    print(f"\n  {DIM}[-] = question not covered by the knowledge base{RESET}")


def show_summary(results: dict) -> None:
    section("Summary (higher is better, except context size and time)")
    header = f"  {'pipeline':<20}{'score':>7}  {'':<20}{'5/5':>7}{'recall':>9}{'ctx chars':>11}{'sec':>7}"
    print(BOLD + header + RESET)
    for name, r in results.items():
        print(
            f"  {name:<20}{r['avg_score']:>7.2f}  {bar(r['avg_score'] / 5)}"
            f"{r['full_marks']:>7.0%}{r['recall']:>9.0%}"
            f"{r['context_chars']:>11.0f}{r['avg_seconds']:>7.2f}"
        )
    print(
        f"\n  {DIM}score     = average LLM-judge rating of answer relevance (1-5)\n"
        f"  5/5       = share of questions answered fully\n"
        f"  recall    = share of the needed facts present in the retrieved chunks\n"
        f"  ctx chars = size of the context sent to the LLM\n"
        f"  sec       = retrieval + generation time per question{RESET}"
    )


if __name__ == "__main__":
    banner(f"RAG: baseline vs optimized  |  model: {MODEL}")
    print(f"  embeddings: {EMBED_MODEL}  |  re-ranker: {RERANK_MODEL}")
    print(f"  {len(QUESTIONS)} questions, top {TOP_K} chunks per answer")

    print(f"\n  {DIM}loading embedding and re-ranker models...{RESET}")
    embeddings = FastEmbedEmbeddings(model_name=EMBED_MODEL)
    reranker = TextCrossEncoder(model_name=RERANK_MODEL)

    chunkings = {
        "fixed-size": fixed_size_chunks(KNOWLEDGE_BASE),
        "section": section_chunks(KNOWLEDGE_BASE),
    }
    show_chunks(chunkings)
    naive_store = FAISS.from_documents(chunkings["fixed-size"], embeddings)
    section_store = FAISS.from_documents(chunkings["section"], embeddings)

    # experiment 10: basic RAG
    banner("Part 1: Basic RAG (Experiment 10)")
    show_grounding(naive_store)

    # experiment 11: add one optimization at a time
    banner("Part 2: Query expansion and context optimization (Experiment 11)")
    pipelines = {
        "baseline": (naive_store, plain_retrieve),
        "+ chunking": (section_store, plain_retrieve),
        "+ query expansion": (section_store, expanded_retrieve),
        "+ re-ranking": (section_store, reranked_retrieve),
    }

    section("Running  (judge score per question, 1-5)")
    results = {name: evaluate(name, *pipe) for name, pipe in pipelines.items()}

    show_trace(results)
    show_matrix(results)
    show_summary(results)

    base, best = results["baseline"], results["+ re-ranking"]
    banner(
        f"Answer score {base['avg_score']:.2f} -> {best['avg_score']:.2f}  |  "
        f"context recall {base['recall']:.0%} -> {best['recall']:.0%}"
    )
