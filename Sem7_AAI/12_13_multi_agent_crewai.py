import os
import sys
import time

from crewai import LLM, Agent, Crew, Process, Task
from crewai.flow.flow import Flow, listen, or_, router, start
from crewai.tools import tool
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from tavily import TavilyClient

sys.stdout.reconfigure(encoding="utf-8")  # LLM output has chars cp1252 cannot encode
load_dotenv()

MODEL = "qwen/qwen3.8-27b"  # gpt-oss on Groq breaks CrewAI tool calls (hallucinated browser tool)
llm = LLM(  # Groq exposes an OpenAI-compatible endpoint
    model=MODEL,
    provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_tokens=900,  # Groq free tier caps output at 1000 tokens/min for this model
    max_retries=5,
)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

TASK = (
    "Compare CrewAI, LangGraph and AutoGen for building multi-agent LLM systems "
    "and recommend one for a final year student project."
)
MAX_SUBTASKS = 4
MAX_RPM = 3  # Groq free tier allows ~7k input tokens/min, so keep calls slow
MAX_SEARCHES = 2  # per task, keeps the agent context small

WIDTH = 90
if sys.stdout.isatty():  # no colour codes when output is redirected to a file
    BOLD, DIM, RESET = "\033[1m", "\033[2m", "\033[0m"
    GREEN, RED, YELLOW, CYAN = "\033[32m", "\033[31m", "\033[33m", "\033[36m"
else:
    BOLD = DIM = RESET = GREEN = RED = YELLOW = CYAN = ""

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


# tools


@tool("Tavily Search")  # "web_search" clashes with gpt-oss built-in browser tool
def tavily_search(query: str) -> str:
    """Search the web for up-to-date information. Input is a short search query."""
    print(f"      {DIM}[tavily_search] {query}{RESET}")
    results = tavily.search(query, max_results=2)["results"]
    return "\n\n".join(
        f"{r['title']} ({r['url']})\n{r['content'][:300]}" for r in results
    )


def log_step(step) -> None:
    # shows tool calls (incl. delegation between agents) while a crew runs
    name = getattr(step, "tool", None)
    if name:
        colour = YELLOW if "coworker" in name.lower() else DIM
        print(f"      {colour}[{name}]{RESET}")


# agents (role, goal and backstory define each agent's specialisation)

planner = Agent(
    role="Project Planner",
    goal="Break a complex task into a few small, ordered, independent sub-tasks",
    backstory=(
        "You are an experienced technical lead. You never do the work yourself; "
        "you split it into clear steps that someone else can execute."
    ),
    llm=llm,
    allow_delegation=False,
    verbose=False,
)

researcher = Agent(  # also acts as the executor in the planner-executor workflow
    role="Research Analyst",
    goal="Find accurate, current, well-sourced facts for the assigned question",
    backstory=(
        "You are a careful analyst who always checks the web before answering "
        "and reports only facts you can back with a source."
    ),
    llm=llm,
    tools=[tavily_search],
    allow_delegation=False,
    max_iter=MAX_SEARCHES + 1,
    verbose=False,
)

writer = Agent(
    role="Technical Writer",
    goal="Turn research notes into a clear, well-structured report for students",
    backstory=(
        "You write concise technical reports. You do not search the web yourself; "
        "if a fact is missing you ask the Research Analyst."
    ),
    llm=llm,
    allow_delegation=True,  # lets the writer delegate / ask the researcher
    verbose=False,
)


# shared state between planner and executor


class SubTask(BaseModel):
    id: int = Field(description="Step number starting at 1")
    title: str = Field(description="Short title of the sub-task")
    instruction: str = Field(description="What exactly the executor should find out")


class Plan(BaseModel):
    subtasks: list[SubTask]


class SharedState(BaseModel):
    task: str = TASK
    plan: list[SubTask] = []
    results: dict[int, str] = {}  # sub-task id -> executor output
    log: list[str] = []  # who did what, in order
    report: str = ""


def pending(state: SharedState) -> list[SubTask]:
    return [s for s in state.plan if s.id not in state.results]


# planner-executor workflow


class PlannerExecutorFlow(Flow[SharedState]):
    suppress_flow_events: bool = True  # hide the built-in flow panels, we print our own

    @start()
    def make_plan(self):
        section("Planner: decomposing the task")
        plan_task = Task(
            description=(
                f"Task: {self.state.task}\n\n"
                f"Split this task into at most {MAX_SUBTASKS} research sub-tasks. "
                "Each sub-task must be answerable with a quick web search. "
                "Do not include a 'write the report' step, that is done later."
            ),
            expected_output="An ordered list of sub-tasks.",
            agent=planner,
            output_pydantic=Plan,
        )
        result = Crew(agents=[planner], tasks=[plan_task], max_rpm=MAX_RPM).kickoff()
        self.state.plan = result.pydantic.subtasks[:MAX_SUBTASKS]
        self.state.log.append(f"planner   created {len(self.state.plan)} sub-tasks")
        for s in self.state.plan:
            print(f"  {BOLD}{s.id}. {s.title}{RESET}")
            print(DIM + indent(s.instruction, "       ") + RESET)

    @router(or_(make_plan, "execute_next"))
    def check_progress(self):
        left = pending(self.state)
        print(
            f"\n  {CYAN}shared state: {len(self.state.results)}/{len(self.state.plan)} done{RESET}"
        )
        return "execute" if left else "done"

    @listen("execute")
    def execute_next(self):
        subtask = pending(self.state)[0]
        section(f"Executor: sub-task {subtask.id} - {subtask.title}")

        # the executor reads earlier results from the shared state
        done = (
            "\n\n".join(f"[{i}] {r}" for i, r in self.state.results.items())
            or "None yet."
        )
        exec_task = Task(
            description=(
                f"Overall goal: {self.state.task}\n\n"
                f"Your sub-task: {subtask.instruction}\n"
                f"Use at most {MAX_SEARCHES} searches.\n\n"
                f"Findings from earlier sub-tasks (do not repeat them):\n{done}"
            ),
            expected_output=(
                "3-5 bullet points of facts relevant to the sub-task, under 120 "
                "words, with the source URL at the end of each bullet."
            ),
            agent=researcher,
        )
        start_time = time.perf_counter()
        result = Crew(
            agents=[researcher],
            tasks=[exec_task],
            step_callback=log_step,
            max_rpm=MAX_RPM,
        ).kickoff()
        seconds = time.perf_counter() - start_time

        self.state.results[subtask.id] = result.raw
        self.state.log.append(
            f"executor  finished sub-task {subtask.id} ({seconds:.1f}s)"
        )
        print(indent(result.raw))
        return "execute_next"

    @listen("done")
    def write_report(self):
        section("Researcher + Writer crew: writing the final report")
        notes = "\n\n".join(
            f"## {s.title}\n{self.state.results[s.id]}" for s in self.state.plan
        )
        write_task = Task(
            description=(
                f"Task: {self.state.task}\n\n"
                f"Research notes collected so far:\n{notes}\n\n"
                "Write a short report: a comparison table (ease of use, control "
                "over flow, multi-agent support, community), 2-3 lines on each "
                "framework, and a final recommendation with reasons. If you need "
                "a fact that is not in the notes, ask the Research Analyst."
            ),
            expected_output="A markdown report under 350 words.",
            agent=writer,
        )
        crew = Crew(
            agents=[researcher, writer],
            tasks=[write_task],
            process=Process.sequential,
            step_callback=log_step,
            max_rpm=MAX_RPM,
        )
        result = crew.kickoff()
        self.state.report = result.raw
        self.state.log.append("writer    wrote the final report")
        return result.raw


# two-agent collaboration on its own (researcher -> writer handoff)


def two_agent_crew(topic: str) -> str:
    research_task = Task(
        description=(
            f"Research this topic using the web: {topic}. "
            f"Use at most {MAX_SEARCHES} searches."
        ),
        expected_output="5 bullet points of key facts with source URLs.",
        agent=researcher,
    )
    write_task = Task(
        description=(
            f"Using the research, write a short explainer on: {topic}. "
            "Ask the Research Analyst if something is unclear."
        ),
        expected_output=(
            "Only the final 120-150 word paragraph for a student audience, "
            "with no drafts, notes or word counts."
        ),
        agent=writer,
        context=[research_task],  # writer receives the researcher's output
    )
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        step_callback=log_step,
        max_rpm=MAX_RPM,
    )
    result = crew.kickoff()
    for task_output in result.tasks_output:
        print(f"\n  {BOLD}{task_output.agent}{RESET}")
        print(indent(task_output.raw))
    return result.raw


if __name__ == "__main__":
    banner(f"Exp 12: Two-agent collaborative crew  |  model: {MODEL}")
    section("Researcher -> Writer on a shared task")
    two_agent_crew("What is the Model Context Protocol (MCP) and why does it matter?")

    banner("Exp 13: Planner-Executor workflow with shared state")
    print(indent(TASK, "  task: "))
    flow = PlannerExecutorFlow()
    report = flow.kickoff()

    section("Final report")
    print(report)

    section("Shared state after the run")
    state = flow.state
    print(f"  sub-tasks planned : {len(state.plan)}")
    print(f"  sub-tasks done    : {len(state.results)}")
    print(f"  report length     : {len(state.report.split())} words")
    print(f"\n  {BOLD}timeline{RESET}")
    for i, entry in enumerate(state.log, start=1):
        print(f"  {i:>2}. {entry}")

    missing = pending(state)
    status = (
        f"{GREEN}all sub-tasks completed{RESET}"
        if not missing
        else f"{RED}{len(missing)} sub-tasks missing{RESET}"
    )
    banner(f"Done  |  {status}")
