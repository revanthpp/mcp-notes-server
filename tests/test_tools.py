from pathlib import Path

from mcp_notes_server.note_store import NoteStore
from mcp_notes_server.tools import NoteTools


def test_tool_workflow(tmp_path: Path) -> None:
    tools = NoteTools(NoteStore(tmp_path))

    created = tools.create_note("MCP Basics", "A protocol, not magic.")
    listed = tools.list_notes()
    read = tools.read_note(created.path)
    found = tools.search_notes("protocol")
    appended = tools.append_to_note(created.path, "Tools have schemas.")

    assert created.path == "mcp-basics.md"
    assert [note.path for note in listed] == ["mcp-basics.md"]
    assert read.title == "MCP Basics"
    assert [match.path for match in found] == ["mcp-basics.md"]
    assert appended.message == "Appended to note: mcp-basics.md"
    assert "Tools have schemas." in tools.read_note(created.path).content
