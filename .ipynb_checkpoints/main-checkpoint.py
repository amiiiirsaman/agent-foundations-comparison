from time import perf_counter
from tabulate import tabulate  # pip install tabulate[web:962]

from src.langgraph_version.agent import run_langgraph_once
from src.crewai_version.agent import run_crewai_once


def main():
    print("--- Agent Foundations: LangGraph vs CrewAI ---\n")

    ticker = input("Enter stock ticker (e.g., NVDA, AAPL, MSFT): ").strip().upper()
    question = f"What is the current price of {ticker}?"

    # LangGraph
    print("\n[LangGraph] Running...")
    lg_answer, lg_latency = run_langgraph_once(question)
    print(f"[LangGraph] Answer: {lg_answer}")

    # CrewAI
    print("\n[CrewAI] Running...")
    crew_answer, crew_latency = run_crewai_once(question)
    print(f"[CrewAI] Answer: {crew_answer}")

    # Summary table
    print("\n=== Summary ===")
    table = [
        ["Framework", "Ticker", "Answer", "Latency (ms)"],
        ["LangGraph", ticker, str(lg_answer), f"{lg_latency:.1f}"],
        ["CrewAI", ticker, str(crew_answer), f"{crew_latency:.1f}"],
    ]
    print(tabulate(table[1:], headers=table[0], tablefmt="github"))
    print()


if __name__ == "__main__":
    main()
