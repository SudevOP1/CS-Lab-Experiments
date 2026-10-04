# Apply and evaluate zero-shot, few-shot, chain-of-thought, and role-based
# prompting strategies, observing their effect on agent reasoning quality and
# output reliability.

import os
import re
import time

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "allam-2-7b"
client = Groq(api_key=os.getenv("GROQ_API_KEY"), max_retries=5)

RUNS_PER_QUESTION = 5  # repeat each prompt to measure consistency
TEMPERATURE = 0.7

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


# the task set

QUESTIONS = [  # multi-step / trick questions with one exact answer each
    (
        "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than "
        "the ball. How much does the ball cost in dollars?",
        "0.05",
    ),
    (
        "If 5 machines take 5 minutes to make 5 widgets, how many minutes "
        "would 100 machines take to make 100 widgets?",
        "5",
    ),
    (
        "A shop sells pens at 3 for $4. Riya buys 12 pens and pays with a "
        "$20 note. How much change in dollars does she get?",
        "4",
    ),
    (
        "Tom is 4 years older than Sara. In 6 years, the sum of their ages "
        "will be 40. How old is Sara now?",
        "12",
    ),
    (
        "A lily pad patch doubles in size every day. It covers the whole lake "
        "on day 30. On which day did it cover half the lake?",
        "29",
    ),
    (
        "A train leaves at 9:45 and the trip takes 2 hours 35 minutes. At "
        "what time does it arrive? Give the time as HH:MM.",
        "12:20",
    ),
]

ANSWER_FORMAT = (
    "End your response with a final line of the form 'Answer: <answer>', "
    "where <answer> is only the final value, with no units or words."
)

# prompting strategies

FEW_SHOT_EXAMPLES = """Question: A notebook costs $3 and a pen costs $2. How much do 2 notebooks and 3 pens cost in dollars?
Answer: 12

Question: If 3 workers paint 3 walls in 3 hours, how many hours do 6 workers take to paint 6 walls?
Answer: 3

Question: Ana is twice as old as Ben. Ben is 7. How old will Ana be in 5 years?
Answer: 19"""

COT_EXAMPLE = """Question: Ana is twice as old as Ben. Ben is 7. How old will Ana be in 5 years?
Reasoning: Ben is 7, so Ana is 2 * 7 = 14 now. In 5 years she will be 14 + 5 = 19.
Answer: 19"""

ROLE = (
    "You are a meticulous mathematics professor who is known for never "
    "falling for trick questions. You read every question carefully and "
    "verify your answer before giving it."
)

STRATEGIES = {
    "zero-shot": lambda q: [
        {"role": "user", "content": f"{q}\n\n{ANSWER_FORMAT}"},
    ],
    "few-shot": lambda q: [
        {
            "role": "user",
            "content": f"{FEW_SHOT_EXAMPLES}\n\nQuestion: {q}\n\n{ANSWER_FORMAT}",
        },
    ],
    "chain-of-thought": lambda q: [
        {
            "role": "user",
            "content": (
                f"{COT_EXAMPLE}\n\nQuestion: {q}\n"
                "Let's think step by step. Write your reasoning first, then "
                f"the answer.\n\n{ANSWER_FORMAT}"
            ),
        },
    ],
    "role-based": lambda q: [
        {"role": "system", "content": ROLE},
        {"role": "user", "content": f"{q}\n\n{ANSWER_FORMAT}"},
    ],
}

# evaluation

ANSWER_RE = re.compile(r"Answer:\s*\**\s*(.+)", re.IGNORECASE)
VALUE_RE = re.compile(r"\d{1,2}:\d{2}|-?\d+(?:\.\d+)?")  # a time or a number
BARE_RE = re.compile(r"^\$?(\d{1,2}:\d{2}|-?\d+(\.\d+)?)$")


def ask(messages: list[dict]) -> str:
    return (
        client.chat.completions.create(
            model=MODEL, messages=messages, temperature=TEMPERATURE, max_tokens=600
        )
        .choices[0]
        .message.content
    )


def extract_answer(response: str) -> tuple[str | None, bool]:
    lines = ANSWER_RE.findall(response)
    if not lines:
        return None, False
    line = lines[-1].strip().strip("*.").replace(",", "")
    values = VALUE_RE.findall(line)
    return (values[-1] if values else None), bool(BARE_RE.match(line))


def normalise(value: str | None) -> str:
    if value is None:
        return "?"
    if ":" in value:
        hours, minutes = value.split(":")
        return f"{int(hours)}:{minutes}"
    return f"{float(value):g}"


def is_correct(value: str | None, expected: str) -> bool:
    return value is not None and normalise(value) == normalise(expected)


def evaluate(name: str, build_prompt) -> dict:
    per_question = []
    print(f"  {name:<18}", end="", flush=True)
    for question, expected in QUESTIONS:
        runs = []
        for _ in range(RUNS_PER_QUESTION):
            start = time.perf_counter()
            response = ask(build_prompt(question))
            answer, strict = extract_answer(response)
            runs.append(
                {
                    "response": response,
                    "answer": answer,
                    "strict": strict,
                    "correct": is_correct(answer, expected),
                    "seconds": time.perf_counter() - start,
                }
            )
        per_question.append(runs)
        marks = "".join(
            f"{GREEN}+{RESET}" if r["correct"] else f"{RED}x{RESET}" for r in runs
        )
        print(f" Q{len(per_question)}[{marks}]", end="", flush=True)
    print()

    all_runs = [r for runs in per_question for r in runs]
    consistent = sum(
        len({normalise(r["answer"]) for r in runs}) == 1 for runs in per_question
    )
    return {
        "per_question": per_question,
        "accuracy": sum(r["correct"] for r in all_runs) / len(all_runs),
        "format_ok": sum(r["strict"] for r in all_runs) / len(all_runs),
        "consistency": consistent / len(per_question),
        "avg_words": sum(len(r["response"].split()) for r in all_runs) / len(all_runs),
        "avg_seconds": sum(r["seconds"] for r in all_runs) / len(all_runs),
    }


# report


def show_sample(results: dict, q_index: int = 0) -> None:
    question, expected = QUESTIONS[q_index]
    section(f"Sample responses for Q{q_index + 1} (expected: {expected})")
    print(indent(question, "  "))
    for name, res in results.items():
        run = res["per_question"][q_index][0]
        status = f"{GREEN}CORRECT{RESET}" if run["correct"] else f"{RED}WRONG{RESET}"
        print(
            f"\n  {BOLD}{name}{RESET}  ->  parsed answer: {normalise(run['answer'])}  {status}"
        )
        print(DIM + indent(run["response"]) + RESET)


def show_summary(results: dict) -> None:
    section("Summary (higher is better, except words and time)")
    header = f"  {'strategy':<18}{'accuracy':>10}  {'':<20}{'format':>8}{'consistent':>12}{'words':>8}{'sec':>7}"
    print(BOLD + header + RESET)
    for name, r in results.items():
        print(
            f"  {name:<18}{r['accuracy']:>10.0%}  {bar(r['accuracy'])}"
            f"{r['format_ok']:>8.0%}{r['consistency']:>12.0%}"
            f"{r['avg_words']:>8.0f}{r['avg_seconds']:>7.2f}"
        )
    print(
        f"\n  {DIM}format     = final line was exactly 'Answer: <value>' as asked\n"
        f"  consistent = all {RUNS_PER_QUESTION} runs of a question gave the same answer\n"
        f"  words/sec  = average response length and latency{RESET}"
    )


def show_matrix(results: dict) -> None:
    section(f"Correct runs per question (out of {RUNS_PER_QUESTION})")
    names = list(results)
    print(
        BOLD
        + f"  {'Q':<6}{'expected':>10}"
        + "".join(f"{n:>18}" for n in names)
        + RESET
    )
    for i, (_, expected) in enumerate(QUESTIONS):
        row = f"  {'Q' + str(i + 1):<6}{expected:>10}"
        for name in names:
            runs = results[name]["per_question"][i]
            score = sum(r["correct"] for r in runs)
            colour = GREEN if score == len(runs) else YELLOW if score else RED
            answers = [normalise(r["answer"]) for r in runs]
            common = max(set(answers), key=answers.count)
            cell = f"{score}/{len(runs)} [{common}]"
            row += f"{colour}{cell:>18}{RESET}"
        print(row)
    print(
        f"\n  {DIM}[x] = the answer given most often across the runs, ? = no answer found{RESET}"
    )


if __name__ == "__main__":
    banner(f"Prompting techniques  |  model: {MODEL}  |  temperature: {TEMPERATURE}")
    print(
        f"  {len(QUESTIONS)} reasoning questions x {len(STRATEGIES)} strategies x "
        f"{RUNS_PER_QUESTION} runs = {len(QUESTIONS) * len(STRATEGIES) * RUNS_PER_QUESTION} calls"
    )

    section("Running  (+ correct, x wrong, one mark per run)")
    results = {name: evaluate(name, build) for name, build in STRATEGIES.items()}

    show_sample(results)
    show_matrix(results)
    show_summary(results)

    best = max(
        results, key=lambda n: (results[n]["accuracy"], results[n]["consistency"])
    )
    banner(f"Best strategy: {best}  ({results[best]['accuracy']:.0%} accuracy)")
