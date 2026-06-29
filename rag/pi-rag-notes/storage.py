"""Small JSON storage layer for the local RAG demo."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonChunkStorage:
    """Persist chunks to a JSON file so the app survives restarts."""

    def __init__(self, path: str | Path = "knowledge_base.json") -> None:
        self.path = Path(path)

    def load_chunks(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

        chunks = data.get("chunks", [])
        if not isinstance(chunks, list):
            return []
        return [chunk for chunk in chunks if isinstance(chunk, dict)]

    def save_chunks(self, chunks: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"chunks": chunks}
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def reset(self) -> None:
        self.save_chunks([])
