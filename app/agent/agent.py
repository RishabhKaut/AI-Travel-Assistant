"""
Builds the travel-planning agent: a LangGraph ReAct-style agent equipped with

  - search_travel_knowledge_base   (RAG over the destination knowledge base)
  - get_weather_forecast           (MCP tool, via app/mcp/client.py)
  - convert_currency               (MCP tool, via app/mcp/client.py)

"""
from __future__ import annotations

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from app.config import CHAT_MODEL, DESTINATION_NAME
from app.agent.prompts import build_system_prompt
from app.agent.rag_tool import search_travel_knowledge_base
from app.mcp.client import get_mcp_tools

_agent = None
_checkpointer = MemorySaver()


async def get_agent():
    """Builds (and caches) the agent. Requires that
    app.mcp.client.start_mcp_client() has already been awaited during
    FastAPI startup, so the MCP tools are available synchronously here."""
    global _agent
    if _agent is not None:
        return _agent

    mcp_tools = get_mcp_tools()  # [get_weather_forecast, convert_currency]
    all_tools = [search_travel_knowledge_base, *mcp_tools]

    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0.2)

    _agent = create_react_agent(
        model=llm,
        tools=all_tools,
        state_modifier=SystemMessage(content=build_system_prompt(DESTINATION_NAME)),
        checkpointer=_checkpointer,
    )
    return _agent


async def ask(question: str, session_id: str) -> dict:
    """Runs one turn of the conversation for the given session_id (multi-turn
    memory is keyed on this via the LangGraph checkpointer) and returns the
    final answer plus which tools were invoked, for transparency in the UI."""
    agent = await get_agent()
    config = {"configurable": {"thread_id": session_id}}

    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]}, config=config)
    messages = result["messages"]

    final_answer = messages[-1].content

    tools_used = []
    for msg in messages:
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            for call in tool_calls:
                name = call.get("name") if isinstance(call, dict) else getattr(call, "name", None)
                if name and name not in tools_used:
                    tools_used.append(name)

    return {"answer": final_answer, "tools_used": tools_used}
