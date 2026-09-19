"""
FastAPI entrypoint for the AI Travel Planning Assistant.

Endpoints:
  GET  /                 -> serves the simple chat UI (static/index.html)
  POST /chat             -> {message, session_id} -> {answer, tools_used}
  POST /admin/reindex    -> rebuilds the FAISS vector store from app/data/raw
  GET  /health           -> basic liveness check

Multi-turn context is kept per `session_id` (any client-generated string,
e.g. a UUID stored in the browser) via the LangGraph checkpointer used in
app/agent/agent.py.
"""
from __future__ import annotations

import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.agent.agent import ask, get_agent
from app.rag.ingest import build_vectorstore
from app.config import BASE_DIR
from app.mcp.client import start_mcp_client, stop_mcp_client


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Start the MCP server subprocess and load its tools once, then build
    # the agent, so the first /chat request doesn't pay that startup cost.
    await start_mcp_client()
    await get_agent()
    yield
    await stop_mcp_client()


app = FastAPI(title="AI Travel Planning Assistant", lifespan=lifespan)

STATIC_DIR = BASE_DIR.parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    tools_used: list[str]
    session_id: str


@app.get("/")
def index():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message must not be empty")
    session_id = req.session_id or str(uuid.uuid4())
    try:
        result = await ask(req.message, session_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ChatResponse(answer=result["answer"], tools_used=result["tools_used"], session_id=session_id)


@app.post("/admin/reindex")
def reindex():
    try:
        build_vectorstore()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"status": "reindexed"}
