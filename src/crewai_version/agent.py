from crewai import Agent as CrewAgent, Task, Crew, LLM
from crewai.tools import BaseTool
from time import perf_counter  # reuse

from src.shared_tools import get_stock_price

import time
import botocore.exceptions


class StockPriceTool(BaseTool):
    name: str = "Stock Price Tool"
    description: str = "Gets the current stock price for a given ticker."

    def _run(self, ticker: str) -> str:
        price = get_stock_price(ticker)
        return f"The price of {ticker} is ${price}"


def build_crewai_agent(question: str):
    llm = LLM(
        model="bedrock/amazon.nova-pro-v1:0",
        temperature=0.1,
    )

    agent = CrewAgent(
        role="Financial Analyst",
        goal="Find the current stock price of a given company",
        backstory="An expert financial analyst.",
        tools=[StockPriceTool()],
        llm=llm,
        memory=False,
    )

    task = Task(
        description=question,
        expected_output="The current stock price as a single number.",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False,
        memory=False,
    )
    return crew


def run_crewai_once(question: str):
    crew = build_crewai_agent(question)

    start = perf_counter()
    result = crew.kickoff()
    end = perf_counter()

    # result is often a string or object; cast to string for display
    answer = str(result)
    latency_ms = (end - start) * 1000.0
    return answer, latency_ms

