"""
Builds the FAISS vector store from the markdown knowledge-base documents in
app/data/raw/.

That front matter is parsed and attached to every chunk's metadata, so the
retriever can always show which document (and, where available, which URL)
an answer was grounded in - satisfying the "display the source title or
source link used for the answer" requirement.

Run directly to (re)build the index:

    python -m app.rag.ingest
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.config import RAW_DOCS_DIR, VECTORSTORE_DIR, EMBEDDING_MODEL, RAG_CHUNK_SIZE, RAG_CHUNK_OVERLAP

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def _parse_front_matter(text: str) -> tuple[dict, str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    raw_meta, body = match.groups()
    meta = {}
    for line in raw_meta.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, body


def load_raw_documents(raw_dir: Path = RAW_DOCS_DIR) -> List[Document]:
    documents = []
    for path in sorted(raw_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = _parse_front_matter(text)
        meta["file"] = path.name
        documents.append(Document(page_content=body, metadata=meta))
    if not documents:
        raise RuntimeError(f"No knowledge-base documents found in {raw_dir}")
    return documents


def chunk_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=RAG_CHUNK_SIZE,
        chunk_overlap=RAG_CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(documents)
    # Keep a short human-readable citation string on every chunk.
    for chunk in chunks:
        title = chunk.metadata.get("title", chunk.metadata.get("file", "Unknown source"))
        url = chunk.metadata.get("url", "")
        chunk.metadata["citation"] = f"{title}" + (f" ({url})" if url else "")
    return chunks


def build_vectorstore(raw_dir: Path = RAW_DOCS_DIR, out_dir: Path = VECTORSTORE_DIR) -> FAISS:
    documents = load_raw_documents(raw_dir)
    chunks = chunk_documents(documents)
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    store = FAISS.from_documents(chunks, embeddings)
    out_dir.mkdir(parents=True, exist_ok=True)
    store.save_local(str(out_dir))
    print(f"Indexed {len(chunks)} chunks from {len(documents)} documents into {out_dir}")
    return store


if __name__ == "__main__":
    build_vectorstore()
