"""
Exposes the knowledge base as a LangChain @tool, so the agent selects it the
same way it selects the MCP tools (per requirement: "select the appropriate
tool based on user request").
"""
from __future__ import annotations

from langchain_core.tools import tool

from app.rag.retriever import retrieve_with_sources


@tool
def search_travel_knowledge_base(query: str) -> str:
    """Search the destination travel knowledge base (attractions,
    neighbourhoods, transportation, culture, food, and sample itineraries).
    Use this for any question about the destination itself. Do NOT use this
    for weather or currency questions - those have their own tools.

    Returns retrieved passages prefixed with their source, or a message
    stating that no relevant content was found.
    """
    context, citations = retrieve_with_sources(query)
    if not context:
        return (
            "NO_RELEVANT_CONTENT: The knowledge base has no relevant "
            "information for this query. Tell the user this clearly instead "
            "of inventing destination facts."
        )
    sources_line = "Sources: " + "; ".join(citations)
    return f"{context}\n\n{sources_line}"
