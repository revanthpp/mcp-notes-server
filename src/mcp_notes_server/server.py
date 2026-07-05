"""MCP transport and capability registration."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from .config import Settings
from .logging_config import configure_logging
from .note_store import NoteStore
from .schemas import MutationResult, NoteContent, NoteSummary, SearchMatch
from .tools import NoteTools


def create_server(settings: Settings | None = None) -> FastMCP:
    """Build a configured server without starting a transport."""
    active_settings = settings or Settings.from_env()
    configure_logging(active_settings.log_level)
    note_tools = NoteTools(NoteStore(active_settings.notes_dir))

    mcp = FastMCP(
        "MCP Notes Server",
        instructions=(
            "Use these tools only for Markdown notes in the configured workspace. "
            "Ask before creating or modifying a note when user intent is ambiguous."
        ),
    )

    @mcp.tool()
    def list_notes() -> list[NoteSummary]:
        """List note titles and workspace-relative Markdown paths."""
        return note_tools.list_notes()

    @mcp.tool()
    def read_note(filename: str) -> NoteContent:
        """Read one Markdown note by its workspace-relative filename."""
        return note_tools.read_note(filename)

    @mcp.tool()
    def search_notes(query: str) -> list[SearchMatch]:
        """Search note titles and contents, returning short matching snippets."""
        return note_tools.search_notes(query)

    @mcp.tool()
    def create_note(title: str, content: str = "") -> MutationResult:
        """Create a Markdown note using a safe filename derived from its title."""
        return note_tools.create_note(title, content)

    @mcp.tool()
    def append_to_note(filename: str, content: str) -> MutationResult:
        """Append text to an existing workspace-relative Markdown note."""
        return note_tools.append_to_note(filename, content)

    @mcp.resource("notes://index")
    def notes_index() -> str:
        """Return a read-only JSON index of the notes available to this server."""
        return json.dumps(
            [note.model_dump() for note in note_tools.list_notes()],
            ensure_ascii=False,
            indent=2,
        )

    @mcp.prompt(title="Summarize a note")
    def summarize_note(filename: str) -> str:
        """Create a reusable instruction for summarizing a note."""
        return (
            f"Read the note {filename!r} with the read_note tool. Summarize its main ideas, "
            "decisions, and open questions. Do not invent details that are not in the note."
        )

    return mcp


def main() -> None:
    """Run the server over stdio for local MCP clients."""
    create_server().run(transport="stdio")


if __name__ == "__main__":
    main()
