"""Typed data returned by the note service and MCP tools."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class NoteSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    path: str


class NoteContent(NoteSummary):
    content: str


class SearchMatch(NoteSummary):
    snippet: str


class MutationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    message: str
