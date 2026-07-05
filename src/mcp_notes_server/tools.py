"""Application service functions shared by MCP handlers and tests."""

from __future__ import annotations

import logging

from .note_store import NoteStore
from .schemas import MutationResult, NoteContent, NoteSummary, SearchMatch

logger = logging.getLogger(__name__)


class NoteTools:
    """Small, explicit tool layer over the filesystem store."""

    def __init__(self, store: NoteStore) -> None:
        self.store = store

    def list_notes(self) -> list[NoteSummary]:
        result = self.store.list_notes()
        logger.info(
            "Listed notes",
            extra={"operation": "list_notes", "result_count": len(result)},
        )
        return result

    def read_note(self, filename: str) -> NoteContent:
        result = self.store.read_note(filename)
        logger.info("Read note", extra={"operation": "read_note", "note_path": result.path})
        return result

    def search_notes(self, query: str) -> list[SearchMatch]:
        result = self.store.search_notes(query)
        logger.info(
            "Searched notes",
            extra={"operation": "search_notes", "result_count": len(result)},
        )
        return result

    def create_note(self, title: str, content: str) -> MutationResult:
        result = self.store.create_note(title, content)
        logger.info("Created note", extra={"operation": "create_note", "note_path": result.path})
        return result

    def append_to_note(self, filename: str, content: str) -> MutationResult:
        result = self.store.append_to_note(filename, content)
        logger.info(
            "Appended to note",
            extra={"operation": "append_to_note", "note_path": result.path},
        )
        return result
