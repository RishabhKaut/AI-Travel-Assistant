"""
Loads the FAISS vector store and exposes:

1. `get_retriever()` - a plain LangChain retriever, used by the RAG tool.
2. `retrieve_with_sources(query)` - convenience helper returning both the
   retrieved text and a de-duplicated list of source citations, used
   whenever we need to show "grounded in the following sources" to the user.

If the vector store has not been built yet, functions raise a clear error
telling the caller to run `python -m app.rag.ingest` first, rather than
silently fabricating an empty index.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.config import VECTORSTORE_DIR, EMBEDDING_MODEL, RAG_TOP_K

_store: FAISS | None = None


def _load_store() -> FAISS:
    global _store
    if _store is not None:
        return _store
    if not Path(VECTORSTORE_DIR).exists():
        raise RuntimeError(
            "Knowledge base vector store not found. Build it first with:\n"
            "  python -m app.rag.ingest"
        )
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    _store = FAISS.load_local(
        str(VECTORSTORE_DIR), embeddings, allow_dangerous_deserialization=True
    )
    return _store


def get_retriever(k: int = RAG_TOP_K):
    return _load_store().as_retriever(search_kwargs={"k": k})


def retrieve_with_sources(query: str, k: int = RAG_TOP_K) -> Tuple[str, List[str]]:
    """Returns (concatenated_context, list_of_citations). Empty context means
    the knowledge base has nothing relevant - callers must not invent facts
    in that case."""
    retriever = get_retriever(k=k)
    docs = retriever.invoke(query)
    if not docs:
        return "", []
    context_parts = []
    citations = []
    for doc in docs:
        citation = doc.metadata.get("citation", "Unknown source")
        context_parts.append(f"[Source: {citation}]\n{doc.page_content}")
        if citation not in citations:
            citations.append(citation)
    return "\n\n---\n\n".join(context_parts), citations
