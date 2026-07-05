from pathlib import Path

import pytest

from mcp_notes_server.note_store import NoteAlreadyExistsError, NoteStore


@pytest.fixture
def store(tmp_path: Path) -> NoteStore:
    (tmp_path / "welcome.md").write_text(
        "# Welcome\n\nMCP makes tool boundaries visible.\n", encoding="utf-8"
    )
    return NoteStore(tmp_path)


def test_create_note_slugifies_title(store: NoteStore) -> None:
    result = store.create_note("Agent Memory 101!", "Memory needs boundaries.")

    assert result.path == "agent-memory-101.md"
    assert store.read_note(result.path).content == (
        "# Agent Memory 101!\n\nMemory needs boundaries.\n"
    )


def test_create_note_does_not_overwrite(store: NoteStore) -> None:
    store.create_note("A New Note", "first")

    with pytest.raises(NoteAlreadyExistsError, match="already exists"):
        store.create_note("A New Note", "second")


def test_list_notes_returns_titles_and_relative_paths(store: NoteStore) -> None:
    nested = store.root / "topics"
    nested.mkdir()
    (nested / "tools.md").write_text("# Tool Calling\n\nDetails.", encoding="utf-8")

    notes = store.list_notes()

    assert [(note.title, note.path) for note in notes] == [
        ("Tool Calling", "topics/tools.md"),
        ("Welcome", "welcome.md"),
    ]


def test_read_note_returns_content(store: NoteStore) -> None:
    note = store.read_note("welcome.md")

    assert note.title == "Welcome"
    assert note.path == "welcome.md"
    assert "tool boundaries" in note.content


def test_search_is_case_insensitive_and_returns_snippet(store: NoteStore) -> None:
    matches = store.search_notes("BOUNDARIES")

    assert len(matches) == 1
    assert matches[0].path == "welcome.md"
    assert "boundaries" in matches[0].snippet.lower()


def test_search_rejects_empty_query(store: NoteStore) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        store.search_notes("  ")


def test_append_to_note_preserves_existing_content(store: NoteStore) -> None:
    result = store.append_to_note("welcome.md", "A safe append.")

    assert result.path == "welcome.md"
    assert store.read_note("welcome.md").content.endswith("\nA safe append.\n")
