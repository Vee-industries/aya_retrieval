"""The recall tool: AgentTune's search tool over the exchanges that have left the view."""

from __future__ import annotations

from pathlib import Path

from agenttune.rag.retrieval.corpus_loader import CorpusDocument, build_index
from agenttune.rag.retrieval.sqlite_fts import SQLiteFTSBackend
from agenttune.rag.tools.search_corpus import SearchCorpusTool

from aya_retrieval.conversations import RecallItem

TOP_K = 5
# Long enough that no single exchange is split, so one exchange is one search result.
CHUNK_SIZE = 400


def exchange_doc_id(index: int) -> str:
    """Return the document id of the exchange at ``index`` in the conversation."""
    return f"exchange_{index:04d}"


def build_recall_tool(item: RecallItem, db_path: Path, match_all: bool) -> SearchCorpusTool:
    """Index the item's older exchanges into a fresh database and return the search tool over it."""
    return build_search_tool(item.older(), db_path, match_all)


def build_search_tool(exchanges, db_path: Path, match_all: bool) -> SearchCorpusTool:
    """Index ``exchanges``, one passage each, into a fresh database and return the search tool."""
    db_path.unlink(missing_ok=True)
    backend = SQLiteFTSBackend(str(db_path), match_all=match_all)
    docs = [
        CorpusDocument(
            doc_id=exchange_doc_id(index),
            title=f"Exchange {index}",
            text=f"User: {user}\nAssistant: {assistant}",
            metadata={},
        )
        for index, (user, assistant) in enumerate(exchanges)
    ]
    build_index(backend, docs, chunk_size=CHUNK_SIZE, overlap=0)
    return SearchCorpusTool(backend, top_k=TOP_K)


def search_finds_fact(tool: SearchCorpusTool, item: RecallItem, query: str) -> bool:
    """Return True if the exchange holding the fact is among the results for ``query``."""
    results = tool.backend.search(query, top_k=TOP_K)
    fact_doc = exchange_doc_id(item.fact_index)
    return any(result["metadata"]["doc_id"] == fact_doc for result in results)
