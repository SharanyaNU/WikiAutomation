"""Course content. Module 1 is written; the other nine are planned (see README roadmap)."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Lesson:
    title: str
    body: str  # HTML, trusted: written by the course authors
    code: str = ""


@dataclass(frozen=True)
class Module:
    number: int
    slug: str
    title: str
    summary: str
    lessons: tuple[Lesson, ...] = field(default_factory=tuple)

    @property
    def ready(self) -> bool:
        return bool(self.lessons)


COURSE = {
    "title": "AI Engineer Course",
    "subtitle": "Build agents and multi-agent workflows with Microsoft Agent Framework",
    "level": "Intermediate Python",
    "duration_weeks": 10,
}

FIRST_WORKFLOW = '''import asyncio
from typing import Never

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler


class Upper(Executor):
    def __init__(self):
        super().__init__(id="upper")

    @handler
    async def run(self, text: str, ctx: WorkflowContext[str]) -> None:
        await ctx.send_message(text.upper())


class Exclaim(Executor):
    def __init__(self):
        super().__init__(id="exclaim")

    @handler
    async def run(self, text: str, ctx: WorkflowContext[Never, str]) -> None:
        await ctx.yield_output(text + "!")


async def main():
    upper, exclaim = Upper(), Exclaim()
    workflow = WorkflowBuilder(start_executor=upper).add_edge(upper, exclaim).build()
    async for event in workflow.run("hello agents", stream=True):
        if event.type == "output":
            print(event.data)  # HELLO AGENTS!


asyncio.run(main())
'''

MODULES: tuple[Module, ...] = (
    Module(
        1,
        "introduction",
        "What is an AI agent?",
        "Agents, tools and workflows, and where Microsoft Agent Framework fits.",
        (
            Lesson(
                "From a model call to an agent",
                "<p>A single model call turns a prompt into text. An <strong>agent</strong> wraps that call in a loop: "
                "it keeps instructions and conversation state, decides when to call <strong>tools</strong> (functions you "
                "provide), and returns a result once the task is done.</p>"
                "<p>In this course you will build agents that read data, call APIs and hand work to each other, and you "
                "will learn when <em>not</em> to use an agent: a fixed sequence of steps is often a plain function.</p>",
            ),
            Lesson(
                "Microsoft Agent Framework in one picture",
                "<p>Microsoft Agent Framework gives you two building blocks:</p><ul>"
                "<li><strong>Agents</strong>: a chat client plus instructions and tools.</li>"
                "<li><strong>Workflows</strong>: a graph of <strong>executors</strong> connected by edges. Each executor "
                "handles one kind of message and sends results onward or yields the workflow's output.</li></ul>"
                "<p>Workflows can pause for a person with <code>ctx.request_info(...)</code> and resume when the answer "
                "arrives. That is how you add human review to an automated process.</p>",
            ),
            Lesson(
                "Your first workflow",
                "<p>Two executors: the first upper-cases the text, the second adds an exclamation mark and yields the "
                "result. No model is needed, so you can run it straight away after "
                "<code>pip install agent-framework-core</code>.</p>",
                FIRST_WORKFLOW,
            ),
        ),
    ),
    Module(2, "chat-clients", "Models and chat clients", "Connect agents to Azure OpenAI and other providers."),
    Module(3, "tools", "Tools and function calling", "Give agents functions to call, safely."),
    Module(4, "state", "Conversation state and memory", "Sessions, history and long-term memory."),
    Module(5, "workflows", "Workflows and executors", "Edges, conditions and fan-out between executors."),
    Module(6, "human-in-the-loop", "Human in the loop", "Pause with request_info and resume with a reviewer's answer."),
    Module(7, "multi-agent", "Multi-agent patterns", "Sequential, concurrent and hand-off orchestration."),
    Module(8, "ag-ui", "Agents in the browser with AG-UI", "Stream agent runs to a web front end."),
    Module(9, "evaluation", "Evaluation and observability", "Tracing, tests and quality checks for agents."),
    Module(10, "capstone", "Capstone project", "Design, build and ship an agentic application."),
)


def find(slug: str) -> Module | None:
    return next((m for m in MODULES if m.slug == slug), None)
