from pathlib import Path

import pytest

from mcp_notes_server.note_store import NoteStore, UnsafePathError


@pytest.fixture
def store(tmp_path: Path) -> NoteStore:
    notes = tmp_path / "notes"
    notes.mkdir()
    (notes / "safe.md").write_text("# Safe\n", encoding="utf-8")
    (tmp_path / "secret.md").write_text("outside", encoding="utf-8")
    (notes / ".env").write_text("TOKEN=secret", encoding="utf-8")
    return NoteStore(notes)


@pytest.mark.parametrize(
    "unsafe_path",
    [
        "../secret.md",
        "folder/../../secret.md",
        "./../secret.md",
        ".env",
        ".hidden/note.md",
    ],
)
def test_read_rejects_traversal_and_hidden_paths(
    store: NoteStore, unsafe_path: str
) -> None:
    with pytest.raises(UnsafePathError):
        store.read_note(unsafe_path)


def test_read_rejects_absolute_path(store: NoteStore, tmp_path: Path) -> None:
    with pytest.raises(UnsafePathError, match="Absolute paths"):
        store.read_note(str((tmp_path / "secret.md").resolve()))


@pytest.mark.parametrize("unsafe_path", ["../secret.md", "/tmp/escape.md", ".env"])
def test_append_rejects_unsafe_paths(store: NoteStore, unsafe_path: str) -> None:
    with pytest.raises(UnsafePathError):
        store.append_to_note(unsafe_path, "malicious append")


def test_read_rejects_non_markdown_files(store: NoteStore) -> None:
    with pytest.raises(UnsafePathError, match="Only Markdown"):
        store.read_note("notes.txt")


def test_symlink_to_outside_workspace_is_not_read(store: NoteStore, tmp_path: Path) -> None:
    link = store.root / "escape.md"
    try:
        link.symlink_to(tmp_path / "secret.md")
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks are unavailable on this platform")

    with pytest.raises(UnsafePathError, match="outside"):
        store.read_note("escape.md")

    assert "escape.md" not in [note.path for note in store.list_notes()]


def test_listing_ignores_hidden_directories_and_non_markdown_files(
    store: NoteStore,
) -> None:
    hidden = store.root / ".private"
    hidden.mkdir()
    (hidden / "secret.md").write_text("# Secret\n", encoding="utf-8")
    (store.root / "data.txt").write_text("not a note", encoding="utf-8")

    assert [note.path for note in store.list_notes()] == ["safe.md"]
