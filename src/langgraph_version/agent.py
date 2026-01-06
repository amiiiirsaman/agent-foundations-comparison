from langchain_core.tools import tool
from langchain_aws import ChatBedrock
from langgraph.prebuilt import chat_agent_executor

from src.shared_tools import get_stock_price

import time
import botocore.exceptions


def build_langgraph_agent():
    """Build a LangGraph agent that calls get_stock_price via Nova Pro."""
    stock_tool = tool(get_stock_price)

    llm = ChatBedrock(
        model_id="amazon.nova-pro-v1:0",
        region_name="us-east-1",
    )

    app = chat_agent_executor.create_tool_calling_executor(
        model=llm,
        tools=[stock_tool],
    )
    return app


from time import perf_counter  # add at top

def run_langgraph_once(question: str):
    app = build_langgraph_agent()
    inputs = {"messages": [("human", question)]}

    start = perf_counter()
    final_answer = None

    for step in app.stream(inputs):
        if "agent" in step:
            msgs = step["agent"]["messages"]
            if msgs:
                final_answer = msgs[-1].content
    end = perf_counter()

    latency_ms = (end - start) * 1000.0
    return final_answer, latency_ms


