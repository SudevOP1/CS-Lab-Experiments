import ast
import json
import os
import re
import time

from dotenv import load_dotenv
from groq import Groq, RateLimitError
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
JUDGE_MODEL = MODEL
client = Groq(api_key=os.getenv("GROQ_API_KEY"), max_retries=5)

TEMPERATURE = 0.2
TOP_K = 2  # documents retrieved per search
MAX_AGENT_STEPS = 5

# USD per 1M tokens (input, output), approximate Groq list prices
PRICES = {
    "openai/gpt-oss-120b": (0.15, 0.60),
    "openai/gpt-oss-20b": (0.075, 0.30),
    "llama-3.3-70b-versatile": (0.59, 0.79),
    "llama-3.1-8b-instant": (0.05, 0.08),
}
PRICE_IN, PRICE_OUT = PRICES.get(MODEL, (0.15, 0.60))

WIDTH = 100
BOLD, DIM, RESET = "\033[1m", "\033[2m", "\033[0m"
GREEN, RED, YELLOW, CYAN = "\033[32m", "\033[31m", "\033[33m", "\033[36m"

os.system("")  # enables ANSI colours in the Windows terminal


def banner(text: str) -> None:
    print(f"\n{BOLD}{CYAN}{'=' * WIDTH}\n {text}\n{'=' * WIDTH}{RESET}")


def section(text: str) -> None:
    print(f"\n{BOLD}{text}{RESET}\n{DIM}{'-' * WIDTH}{RESET}")


def indent(text: str, prefix: str = "    | ", max_lines: int = 8) -> str:
    lines = [line for line in text.strip().splitlines() if line.strip()]
    hidden = len(lines) - max_lines
    if hidden > 0:
        lines = lines[:max_lines] + [f"... ({hidden} more lines)"]
    return "\n".join(prefix + line for line in lines)


def bar(fraction: float, width: int = 15) -> str:
    filled = round(fraction * width)
    colour = GREEN if fraction >= 0.75 else YELLOW if fraction >= 0.4 else RED
    return f"{colour}{'#' * filled}{DIM}{'.' * (width - filled)}{RESET}"


def cost(tokens_in: int, tokens_out: int) -> float:
    return (tokens_in * PRICE_IN + tokens_out * PRICE_OUT) / 1_000_000


# knowledge base (a fictional handbook, so the model cannot answer from memory)

DOCS = {
    "leave": "Leave policy: Every full-time employee at Orbit Labs gets 24 paid "
    "leaves per calendar year. At most 5 unused leaves can be carried forward "
    "to the next year. Leave must be applied for at least 3 working days in "
    "advance through the HR portal called Pulse.",
    "remote": "Remote work policy: Employees may work remotely for up to 2 days "
    "per week. Core collaboration hours are 11:00 to 16:00 IST, during which "
    "everyone must be reachable on chat.",
    "expenses": "Expense reimbursement: Claims must be filed within 30 days of "
    "the expense. Meal expenses are capped at Rs 800 per day for domestic travel "
    "and Rs 2,500 per day for international travel. Any single claim above "
    "Rs 10,000 needs approval from the reporting manager.",
    "laptops": "Laptop policy: Laptops are refreshed every 3 years. Engineers get "
    "a MacBook Pro and all other roles get a ThinkPad. A lost or stolen laptop "
    "must be reported within 24 hours to it-help@orbitlabs.example.",
    "onboarding": "Onboarding: Every new joiner is assigned an onboarding buddy "
    "for their first month. The probation period is 90 days, after which the "
    "manager confirms the employee.",
    "allowance": "Internet allowance: Employees who work remotely receive an "
    "internet allowance of Rs 1,500 per month, paid along with the salary.",
    "security": "Security policy: Passwords must be changed every 90 days and "
    "two-factor authentication is mandatory on all accounts. Company systems "
    "must only be accessed from outside the office through the Tunnel VPN.",
    "learning": "Learning budget: Each employee has a learning budget of "
    "Rs 40,000 per year for courses and books. Certification exam fees are "
    "reimbursed only if the employee passes the exam.",
}

# test set: (question, reference answer, gold doc or None if unanswerable)

TEST_SET = [
    (
        "How many paid leaves do employees get per year, and how many can be carried forward?",
        "24 paid leaves per year, of which at most 5 can be carried forward.",
        "leave",
    ),
    (
        "What are the core collaboration hours?",
        "11:00 to 16:00 IST.",
        "remote",
    ),
    (
        "On a 4-day domestic trip I spent Rs 3,000 on meals each day. How much of "
        "the meal cost will be reimbursed in total?",
        "Rs 3,200 (capped at Rs 800 per day x 4 days).",
        "expenses",
    ),
    (
        "I have taken a Rs 12,500 course and a Rs 9,000 course this year. How much "
        "of my learning budget is left?",
        "Rs 18,500 (40,000 - 12,500 - 9,000).",
        "learning",
    ),
    (
        "My laptop got stolen. Within how much time and to whom should I report it?",
        "Within 24 hours, to it-help@orbitlabs.example.",
        "laptops",
    ),
    (
        "How much internet allowance does a remote employee receive in a full year?",
        "Rs 18,000 (Rs 1,500 per month x 12 months).",
        "allowance",
    ),
    (
        "Does a single expense claim of Rs 12,000 need any approval?",
        "Yes, claims above Rs 10,000 need approval from the reporting manager.",
        "expenses",
    ),
    (
        "What is the company policy on bringing pets to the office?",
        "The handbook does not cover this, so the system should say it does not know.",
        None,
    ),
]

# llm call wrapper (tracks latency and token usage)


def chat(messages: list[dict], usage: dict, model: str = MODEL, **kwargs):
    for attempt in range(10):
        try:
            response = client.chat.completions.create(
                model=model, messages=messages, **kwargs
            )
            break
        except RateLimitError:  # free tier has a tokens-per-minute cap
            usage["wait"] += 10 * (attempt + 1)
            time.sleep(10 * (attempt + 1))
    else:
        raise RuntimeError("Still rate limited after 10 retries.")
    usage["calls"] += 1
    usage["in"] += response.usage.prompt_tokens
    usage["out"] += response.usage.completion_tokens
    return response.choices[0].message


def new_usage() -> dict:
    return {"calls": 0, "in": 0, "out": 0, "wait": 0}  # wait = rate-limit sleep


# retriever (TF-IDF over the handbook)

DOC_IDS = list(DOCS)
vectorizer = TfidfVectorizer(stop_words="english")
doc_matrix = vectorizer.fit_transform(DOCS.values())


def retrieve(query: str, k: int = TOP_K) -> list[str]:
    scores = cosine_similarity(vectorizer.transform([query]), doc_matrix)[0]
    ranked = sorted(range(len(DOC_IDS)), key=lambda i: scores[i], reverse=True)
    return [DOC_IDS[i] for i in ranked[:k] if scores[i] > 0]


def format_docs(doc_ids: list[str]) -> str:
    return "\n\n".join(f"[{d}] {DOCS[d]}" for d in doc_ids) or "No documents found."


# systems under test

SYSTEM_PROMPT = (
    "You are an HR assistant for Orbit Labs. Answer in 1-2 short sentences. "
    "If the handbook does not contain the answer, say you don't know."
)


# each system returns (answer, retrieved doc ids, context the answer was based on)


def run_llm_only(question: str, usage: dict) -> tuple[str, list[str], str]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    answer = chat(messages, usage, temperature=TEMPERATURE, max_tokens=800).content
    return answer, [], ""


def run_rag(question: str, usage: dict) -> tuple[str, list[str], str]:
    doc_ids = retrieve(question)
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + " Use only the handbook context given.",
        },
        {
            "role": "user",
            "content": f"Handbook context:\n{format_docs(doc_ids)}\n\nQuestion: {question}",
        },
    ]
    answer = chat(messages, usage, temperature=TEMPERATURE, max_tokens=800).content
    return answer, doc_ids, format_docs(doc_ids)


def calculator(expression: str) -> str:
    if not re.fullmatch(r"[\d\s+\-*/().%]+", expression):
        return "Error: only numbers and + - * / ( ) % are allowed."
    try:
        return str(eval(compile(ast.parse(expression, mode="eval"), "", "eval"), {}))
    except Exception as e:
        return f"Error: {e}"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_handbook",
            "description": "Search the Orbit Labs employee handbook.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate an arithmetic expression, e.g. '800 * 4'.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
]


def run_agent(question: str, usage: dict) -> tuple[str, list[str], str]:
    # tool-calling agent: decides itself when to search and when to calculate
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
            + " Always search the handbook before answering and use the "
            "calculator for any arithmetic.",
        },
        {"role": "user", "content": question},
    ]
    seen_docs, tool_outputs = [], []
    for _ in range(MAX_AGENT_STEPS):
        msg = chat(
            messages, usage, temperature=TEMPERATURE, max_tokens=800, tools=TOOLS
        )
        if not msg.tool_calls:
            return msg.content, seen_docs, "\n\n".join(tool_outputs)
        messages.append(
            {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            }
        )
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments or "{}")
            if tc.function.name == "search_handbook":
                doc_ids = retrieve(args.get("query", ""))
                seen_docs += [d for d in doc_ids if d not in seen_docs]
                result = format_docs(doc_ids)
            else:
                result = calculator(args.get("expression", ""))
                result = f"calculator({args.get('expression', '')}) = {result}"
            tool_outputs.append(result)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    return "Agent stopped: step limit reached.", seen_docs, "\n\n".join(tool_outputs)


SYSTEMS = {
    "llm-only": run_llm_only,
    "rag": run_rag,
    "agent": run_agent,
}

# automated evaluation (LLM-as-a-judge)

GRADE_PROMPT = """You are grading an AI assistant's answer against a reference answer.

Question: {question}
Reference answer: {reference}
Assistant's answer: {answer}

Return JSON with these keys:
- "success": true if the answer contains the same key facts / final values as the reference (wording may differ). If the reference says the question is not covered, success is true only if the assistant says it does not know.
- "relevance": an integer 1-5 for how directly the answer addresses the question (5 = fully on point, 1 = off topic), regardless of correctness.
- "reason": one short sentence."""

FAITHFULNESS_PROMPT = """Break the answer into short atomic factual claims, then check each claim against the context.
A claim is supported only if it can be directly inferred from the context (arithmetic on numbers from the context counts as supported).
Statements like "I don't know" are not claims.

Context:
{context}

Answer: {answer}

Return JSON: {{"claims": [{{"claim": "...", "supported": true or false}}]}}"""


def judge(prompt: str, usage: dict) -> dict:
    msg = chat(
        [{"role": "user", "content": prompt}],
        usage,
        model=JUDGE_MODEL,
        temperature=0,
        max_tokens=1500,
        response_format={"type": "json_object"},
    )
    try:
        return json.loads(msg.content)
    except (json.JSONDecodeError, TypeError):
        match = re.search(r"\{.*\}", msg.content or "", re.DOTALL)
        return json.loads(match.group()) if match else {}


def score_faithfulness(question: str, answer: str, context: str, usage: dict):
    # the question is part of the context, numbers given by the user are facts too
    context = f"User's question: {question}\n\n{context}"
    claims = judge(
        FAITHFULNESS_PROMPT.format(context=context, answer=answer), usage
    ).get("claims", [])
    if not claims:  # nothing asserted, so nothing unfaithful
        return 1.0, claims
    return sum(bool(c.get("supported")) for c in claims) / len(claims), claims


def evaluate(name: str, run) -> dict:
    rows = []
    print(f"  {name:<10}", end="", flush=True)
    for question, reference, gold in TEST_SET:
        usage, judge_usage = new_usage(), new_usage()
        start = time.perf_counter()
        answer, doc_ids, context = run(question, usage)
        seconds = time.perf_counter() - start - usage["wait"]
        answer = (answer or "").strip()

        grade = judge(
            GRADE_PROMPT.format(question=question, reference=reference, answer=answer),
            judge_usage,
        )
        # an llm without retrieval has no context to be faithful to
        faithfulness, claims = (
            score_faithfulness(question, answer, context, judge_usage)
            if name != "llm-only"
            else (None, [])
        )
        rows.append(
            {
                "answer": answer,
                "docs": doc_ids,
                "success": bool(grade.get("success")),
                "relevance": (min(max(int(grade.get("relevance", 1)), 1), 5) - 1) / 4,
                "reason": grade.get("reason", ""),
                "faithfulness": faithfulness,
                "claims": claims,
                "recall": None if gold is None else float(gold in doc_ids),
                "precision": (
                    None
                    if not doc_ids or gold is None
                    else doc_ids.count(gold) / len(doc_ids)
                ),
                "seconds": seconds,
                "usage": usage,
                "judge_usage": judge_usage,
            }
        )
        print(
            f" Q{len(rows)}"
            + (f"{GREEN}+{RESET}" if rows[-1]["success"] else f"{RED}x{RESET}"),
            end="",
            flush=True,
        )
    print()

    def mean(key: str) -> float | None:
        values = [r[key] for r in rows if r[key] is not None]
        return sum(values) / len(values) if values else None

    n = len(rows)
    tokens_in = sum(r["usage"]["in"] for r in rows)
    tokens_out = sum(r["usage"]["out"] for r in rows)
    return {
        "rows": rows,
        "success": mean("success"),
        "faithfulness": mean("faithfulness"),
        "relevance": mean("relevance"),
        "recall": mean("recall"),
        "precision": mean("precision"),
        "avg_seconds": mean("seconds"),
        "avg_calls": sum(r["usage"]["calls"] for r in rows) / n,
        "avg_tokens": (tokens_in + tokens_out) / n,
        "avg_cost": cost(tokens_in, tokens_out) / n,
        "judge_in": sum(r["judge_usage"]["in"] for r in rows),
        "judge_out": sum(r["judge_usage"]["out"] for r in rows),
    }


# report


def pct(value: float | None, width: int) -> str:
    return f"{'n/a':>{width}}" if value is None else f"{value:>{width}.0%}"


def show_sample(results: dict, q_index: int = 2) -> None:
    question, reference, _ = TEST_SET[q_index]
    section(f"Sample answers for Q{q_index + 1}")
    print(indent(question, "  "))
    print(f"  {DIM}reference: {reference}{RESET}")
    for name, res in results.items():
        row = res["rows"][q_index]
        status = f"{GREEN}SUCCESS{RESET}" if row["success"] else f"{RED}FAIL{RESET}"
        faith = "n/a" if row["faithfulness"] is None else f"{row['faithfulness']:.0%}"
        print(
            f"\n  {BOLD}{name}{RESET}  ->  {status}  faithfulness: {faith}  "
            f"docs: {row['docs'] or '-'}  {row['seconds']:.2f}s"
        )
        print(DIM + indent(row["answer"]) + RESET)
        for c in row["claims"]:
            mark = f"{GREEN}+{RESET}" if c.get("supported") else f"{RED}x{RESET}"
            print(f"      {mark} {c.get('claim', '')}")


def show_matrix(results: dict) -> None:
    section("Per-question results  (S = task success, F = faithfulness, t = latency)")
    names = list(results)
    print(
        BOLD
        + f"  {'Q':<4}{'gold doc':<11}"
        + "".join(f"{n:>25}" for n in names)
        + RESET
    )
    for i, (_, _, gold) in enumerate(TEST_SET):
        row = f"  {'Q' + str(i + 1):<4}{gold or '(none)':<11}"
        for name in names:
            r = results[name]["rows"][i]
            faith = (
                "  - " if r["faithfulness"] is None else f"{r['faithfulness']:>4.0%}"
            )
            cell = f"S:{'Y' if r['success'] else 'N'} F:{faith} t:{r['seconds']:>5.2f}s"
            row += f"{GREEN if r['success'] else RED}{cell:>25}{RESET}"
        print(row)


def show_failures(results: dict) -> None:
    section("Failed tasks (judge's reason)")
    failures = [
        (name, i, r)
        for name, res in results.items()
        for i, r in enumerate(res["rows"])
        if not r["success"]
    ]
    if not failures:
        print(f"  {GREEN}none{RESET}")
    for name, i, r in failures:
        print(f"  {RED}{name:<10}{RESET} Q{i + 1}: {r['reason']}")
        print(DIM + indent(r["answer"], "      | ", max_lines=3) + RESET)


def show_summary(results: dict) -> None:
    section("Summary")
    header = (
        f"  {'system':<10}{'success':>9}  {'':<15}{'faithful':>10}{'relevance':>11}"
        f"{'ctx recall':>12}{'ctx prec':>10}{'latency':>9}{'calls':>7}{'tokens':>8}{'$/query':>10}"
    )
    print(BOLD + header + RESET)
    for name, r in results.items():
        print(
            f"  {name:<10}{r['success']:>9.0%}  {bar(r['success'])}"
            f"{pct(r['faithfulness'], 10)}{pct(r['relevance'], 11)}"
            f"{pct(r['recall'], 12)}{pct(r['precision'], 10)}"
            f"{r['avg_seconds']:>8.2f}s{r['avg_calls']:>7.1f}{r['avg_tokens']:>8.0f}"
            f"{r['avg_cost']:>10.6f}"
        )
    judge_in = sum(r["judge_in"] for r in results.values())
    judge_out = sum(r["judge_out"] for r in results.values())
    print(
        f"\n  {DIM}success    = judge says the answer matches the reference answer\n"
        f"  faithful   = share of answer claims supported by the retrieved context\n"
        f"  relevance  = judge's 1-5 on-topic score, rescaled to 0-100%\n"
        f"  ctx recall = gold document was retrieved, ctx prec = share of retrieved docs that are gold\n"
        f"  latency, calls, tokens and $ are averages per query "
        f"(${PRICE_IN}/${PRICE_OUT} per 1M in/out tokens)\n"
        f"  evaluation itself used {judge_in + judge_out} judge tokens "
        f"(~${cost(judge_in, judge_out):.4f}){RESET}"
    )


if __name__ == "__main__":
    banner(f"Agent & RAG evaluation  |  model: {MODEL}  |  judge: {JUDGE_MODEL}")
    print(
        f"  {len(TEST_SET)} questions x {len(SYSTEMS)} systems, "
        f"knowledge base of {len(DOCS)} handbook documents, top-{TOP_K} TF-IDF retrieval"
    )

    section("Running  (+ task success, x failure)")
    results = {name: evaluate(name, run) for name, run in SYSTEMS.items()}

    show_sample(results)
    show_matrix(results)
    show_failures(results)
    show_summary(results)

    best = max(
        results,
        key=lambda n: (
            results[n]["success"],
            results[n]["faithfulness"] or 0,
            -results[n]["avg_cost"],
        ),
    )
    banner(
        f"Best system: {best}  ({results[best]['success']:.0%} task success, "
        f"{results[best]['avg_seconds']:.2f}s, ${results[best]['avg_cost']:.6f} per query)"
    )
