# AI Travel Planning Assistant — Singapore

**Submitted by:** [Rishabh Kaut]
**Date:** [20-09-2026]
**Assignment:** AI Travel Planning Assistant 

> A context-aware travel assistant I built that combines a document-based
> knowledge base with current information retrieved through MCP tools. I
> used LangGraph's ReAct agent to let the model decide, per question,
> whether to pull from the Singapore knowledge base (RAG), call a live
> weather/currency MCP tool, or both — with every answer labeling where
> each piece of information came from.

---

A context-aware travel assistant that combines a document-based knowledge
base (RAG) with live, current information retrieved through MCP tools
(weather forecast and currency conversion), built with **LangChain /
LangGraph** and served over a **FastAPI** backend.

---

## 1. Architecture

```
┌─────────────────────┐        ┌──────────────────────────────┐
│   Browser (static/   │  HTTP  │         FastAPI (app/main.py) │
│   index.html chat UI)│───────▶│  POST /chat  { message,       │
└─────────────────────┘        │               session_id }    │
                                └───────────────┬────────────────┘
                                                │
                                                ▼
                                 ┌──────────────────────────────┐
                                 │  LangGraph ReAct Agent         │
                                 │  (app/agent/agent.py)          │
                                 │  - system prompt (prompts.py)  │
                                 │  - MemorySaver checkpointer     │
                                 │    (multi-turn memory, keyed    │
                                 │    on session_id)               │
                                 └───────┬───────────────┬────────┘
                                         │               │
                    ┌────────────────────┘               └─────────────────┐
                    ▼                                                      ▼
       ┌─────────────────────────┐                     ┌────────────────────────────┐
       │ search_travel_knowledge_ │                     │  MCP tools (stdio client)   │
       │ base  (LangChain @tool)  │                     │  app/mcp/client.py          │
       │ app/agent/rag_tool.py    │                     │  ──▶ app/mcp/server.py      │
       └───────────┬─────────────┘                     │      (FastMCP server)       │
                    ▼                                    │  - get_weather_forecast     │
       ┌─────────────────────────┐                       │    (Open-Meteo API)         │
       │ FAISS vector store        │                     │  - convert_currency         │
       │ app/rag/retriever.py      │                     │    (exchangerate.host API)  │
       │ built by app/rag/ingest.py│                     └────────────────────────────┘
       │ from app/data/raw/*.md    │
       └───────────────────────────┘
```

- **RAG side**: `app/rag/ingest.py` chunks the markdown knowledge-base files
  in `app/data/raw/`, embeds them, and stores them in a local FAISS index.
  `app/rag/retriever.py` loads that index and returns both the retrieved
  text and a citation list. `app/agent/rag_tool.py` wraps this as a
  LangChain tool the agent can call.
- **MCP side**: `app/mcp/server.py` is a real Model Context Protocol server
  (built with the official `mcp` SDK's `FastMCP`) exposing two tools,
  `get_weather_forecast` and `convert_currency`, each backed by a free
  public API. `app/mcp/client.py` connects to that server over stdio using
  `langchain-mcp-adapters` and exposes the tools as LangChain `BaseTool`
  objects. The connection is opened once at FastAPI startup (see the
  `lifespan` handler in `app/main.py`) and closed at shutdown, rather than
  reconnecting per request.
- **Agent**: `app/agent/agent.py` builds a LangGraph `create_react_agent`
  with all three tools (`search_travel_knowledge_base`,
  `get_weather_forecast`, `convert_currency`) and a `MemorySaver`
  checkpointer keyed by `session_id`, giving the assistant multi-turn
  conversational memory. The agent decides for itself, per turn, which
  tool(s) to call based on the user's question.
- **API**: `app/main.py` exposes `POST /chat`, `POST /admin/reindex`, and
  serves the static chat UI at `/`.

---

## 2. Knowledge-base sources

Five markdown files in `app/data/raw/` cover the required categories, each
carrying `title` / `source` / `url` front matter so the retriever can cite
its sources:

| File | Covers | Adapted from |
|---|---|---|
| `01_attractions_neighbourhoods.md` | Attractions, neighbourhoods, indoor/outdoor tagging | Wikivoyage — Singapore |
| `02_transportation.md` | MRT, buses, taxis/ride-hailing, walking, Sentosa access | Wikivoyage — Singapore |
| `03_culture_practical_tips.md` | Climate, language, etiquette, currency, family travel, safety | Visit Singapore — Essential Travel Information |
| `04_food_experiences.md` | Hawker centres, local dishes, food districts | Visit Singapore — Things to Do |
| `05_sample_itineraries.md` | 3-day classic itinerary, family itinerary, rainy-day swaps | Visit Singapore — Sample Itineraries |

These files contain **original summaries written for this project**, not
verbatim copies of the source pages. Before using this in production,
replace/extend them with the actual source documents (converted to
markdown/text/PDF) per your organisation's copyright and reuse-terms
review — the recommended source URLs are:

- Wikivoyage Singapore Travel Guide — https://en.wikivoyage.org/wiki/Singapore
- Visit Singapore: Essential Travel Information — https://www.visitsingapore.com/travel-guide-tips/essential-info/
- Visit Singapore: Sample Itineraries — https://www.visitsingapore.com/see-do-singapore/uniquely-singapore/itineraries/
- Visit Singapore: Things to Do — https://www.visitsingapore.com/see-do-singapore/

To add more/real content: drop additional `.md` files (with the same front
matter format) into `app/data/raw/` and re-run the ingestion step below.

---

## 3. RAG workflow

1. **Load** — `load_raw_documents()` reads every `.md` file in
   `app/data/raw/`, parsing the front matter into metadata.
2. **Chunk** — `chunk_documents()` splits each document with a
   `RecursiveCharacterTextSplitter` (800 chars, 120 overlap, splitting on
   markdown headers first) and stamps a `citation` string onto every chunk.
3. **Embed** — pluggable via `app/rag/embeddings.py`: local
   `sentence-transformers` (`all-MiniLM-L6-v2`, free, default) or
   `OpenAIEmbeddings` (`text-embedding-3-small`) if `EMBEDDING_PROVIDER=openai`.
4. **Store** — a local FAISS index saved to `app/data/vectorstore/`.
5. **Retrieve** — `retrieve_with_sources(query)` does a top-k similarity
   search (`RAG_TOP_K=4`) and returns concatenated context plus a
   de-duplicated citation list.
6. **Generate** — the LLM answers using only the retrieved context (see
   prompt strategy below); it is instructed to state clearly when nothing
   relevant was retrieved instead of inventing destination facts.
7. **Cite** — every RAG-grounded answer ends with a "Sources:" line listing
   the document title(s) and URL(s) actually retrieved.

---

## 4. MCP tools

| Tool | Purpose | Backing API | Failure handling |
|---|---|---|---|
| `get_weather_forecast(days, location)` | Current conditions + up to 7-day forecast | [Open-Meteo](https://open-meteo.com/) (free, no API key) | Raises a clear `RuntimeError` on failure; the agent is instructed to tell the user live weather could not be retrieved rather than guessing |
| `convert_currency(amount, from_currency, to_currency)` | FX conversion between two ISO codes | [exchangerate.host](https://exchangerate.host/) (free, no API key) | Same — raises rather than fabricating a rate |

Both tools live in `app/mcp/server.py`, a standalone **MCP server**
(stdio transport, built with `mcp.server.fastmcp.FastMCP`) that can be run
and inspected independently:

```bash
python -m app.mcp.server
```

The FastAPI app connects to it as an MCP **client** via
`langchain-mcp-adapters` (`app/mcp/client.py`), not by importing the
functions directly — this is what makes the tools genuinely available over
MCP rather than as ordinary in-process Python calls, and means the same
agent code would work unchanged against a different/remote MCP weather or
currency server.

The system prompt explicitly tells the model not to use these tools for
questions the knowledge base already answers (e.g. "what's Singapore's
climate like generally" is RAG; "what's the forecast for the next 3 days"
is the weather tool).

---

## 5. Combined RAG + MCP responses

For a request like *"Plan a three-day trip to Singapore and adjust the
activities based on the weather forecast"*, the agent (autonomously, via
ReAct-style reasoning):

1. Calls `search_travel_knowledge_base` for attractions, indoor/outdoor
   tags, transportation, and sample itineraries.
2. Calls `get_weather_forecast(days=3)` for the live forecast.
3. Produces a day-by-day itinerary, swapping outdoor activities for indoor
   alternatives on days flagged with high rain probability.
4. Labels each piece of information inline (see prompt strategy) so the
   response visibly distinguishes:
   - `[Knowledge base]` — retrieved destination facts (with a Sources line)
   - `[Live tool result]` — the weather/currency figures actually returned
   - `[Suggestion]` — the LLM's own recommendation/reasoning

The same pattern applies to the other combined scenarios in the assignment
brief (budget conversion + itinerary, outdoor→indoor swap on rain, family
trip + latest forecast, cultural itinerary + budget in local currency) —
no special-casing is needed since the agent picks tools per request.

---

## 6. Prompt & context strategy

See `app/agent/prompts.py` for the full system prompt. Summary of the
design decisions:

- **Tool-first, not memory-first**: the model is explicitly told destination
  facts must come from `search_travel_knowledge_base` and current facts
  from the MCP tools — never from its own training data.
- **Explicit provenance tags** (`[Knowledge base]`, `[Live tool result]`,
  `[Suggestion]`) in every answer, directly satisfying the requirement to
  distinguish factual vs. AI-generated content.
- **Honest gaps**: if the retriever returns nothing relevant, the tool
  result itself is prefixed `NO_RELEVANT_CONTENT:` so the model states this
  to the user instead of inventing an answer; if an MCP tool call fails
  (service down), the exception message flows back to the model so it can
  say the live data couldn't be fetched.
- **Tool boundaries**: the prompt tells the model not to call the weather/
  currency tools for questions the knowledge base already covers, and vice
  versa, satisfying "appropriate tool selection based on user intent."
- **Context/preference retention**: a `MemorySaver` checkpointer keyed by
  `session_id` gives the LangGraph agent full message-history memory across
  turns, and the prompt additionally instructs the model to reuse
  previously stated preferences (dates, budget, party size, interests)
  without re-asking, unless the user changes them.

---

## 7. Setup instructions

### Option A — 100% free, fully local (default, no API key needed)

This is the default configuration (`LLM_PROVIDER=ollama`,
`EMBEDDING_PROVIDER=local`): the chat model runs locally via
[Ollama](https://ollama.com), and embeddings run locally via
`sentence-transformers`. No account, no API key, no per-call cost.

```bash
# 1. Install Ollama (one-time) and pull a model
#    macOS/Linux: curl -fsSL https://ollama.com/install.sh | sh
#    Windows: download the installer from https://ollama.com/download
ollama pull llama3.1        # ~5GB; or `ollama pull llama3.2` / `qwen2.5:3b` for a lighter model
ollama serve                 # starts the local server on http://localhost:11434 (often auto-starts)

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# defaults in .env.example already point at Ollama + local embeddings -
# no edits needed unless you want a different Ollama model

# 5. Build the knowledge-base vector store (downloads the small embedding
#    model from Hugging Face the first time, then runs fully offline)
python -m app.rag.ingest

# 6. Run the application
uvicorn app.main:app --reload --port 8000
```

If `CHAT_MODEL` in `.env` doesn't match a model you've pulled, Ollama will
return a clear "model not found" error - just `ollama pull <model>` and
retry.

### Option B — OpenAI (paid, requires an API key)

```
LLM_PROVIDER=openai
CHAT_MODEL=gpt-4o-mini
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=sk-...
```

Then follow steps 2-6 above (skip the Ollama install). Rebuilding the index
after switching providers is required, since embeddings from different
providers/models aren't compatible with each other.

### Using it

Open http://localhost:8000 for the chat UI, or call the API directly:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Plan a three-day trip to Singapore and adjust the activities based on the weather forecast."}'
```

The response includes `session_id` — pass it back on subsequent requests to
continue the same conversation with retained context:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Now convert a 60,000 INR budget to SGD for that trip.", "session_id": "<the returned id>"}'
```

To rebuild the index after editing the knowledge base without restarting
the server: `POST /admin/reindex`.

---

## 8. Sample questions and expected behaviour

See `SAMPLE_QA.md` for worked examples covering pure RAG, pure MCP,
combined RAG+MCP, missing-knowledge handling, and multi-turn context
retention.

---

## 9. Notes / possible extensions

- Swap providers by editing `.env` (`LLM_PROVIDER`, `EMBEDDING_PROVIDER`) -
  the factories in `app/agent/llm.py` and `app/rag/embeddings.py` handle
  the rest. Adding a third provider (e.g. Anthropic, Google) means adding a
  branch to those two files.
- The MCP server currently runs as a local stdio subprocess; in
  `app/mcp/client.py` the same `MultiServerMCPClient` can instead be pointed
  at an `sse`/remote MCP server with no changes to the agent code.
- Additional MCP tools (e.g. public-transport routing, event listings) can
  be added to `app/mcp/server.py` as further `@mcp.tool()` functions and
  will be picked up automatically by `get_mcp_tools()`.
