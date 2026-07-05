"""Filesystem-backed Markdown note storage with a strict directory boundary."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path, PurePath

from .schemas import MutationResult, NoteContent, NoteSummary, SearchMatch


class NoteStoreError(ValueError):
    """Base class for errors safe to show to an MCP client."""


class UnsafePathError(NoteStoreError):
    """Raised when a requested path violates the workspace boundary."""


class NoteNotFoundError(NoteStoreError):
    """Raised when a requested note does not exist."""


class NoteAlreadyExistsError(NoteStoreError):
    """Raised when create_note would overwrite a note."""


def slugify(title: str) -> str:
    """Convert a human title into a conservative Markdown filename."""
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title).strip("-")
    if not slug:
        raise NoteStoreError("Title must contain at least one letter or number.")
    return f"{slug[:80].rstrip('-')}.md"


class NoteStore:
    """Read and mutate Markdown files under exactly one configured root."""

    def __init__(self, root: Path) -> None:
        root.mkdir(parents=True, exist_ok=True)
        self.root = root.resolve(strict=True)
        if not self.root.is_dir():
            raise NoteStoreError(f"Notes workspace is not a directory: {self.root}")

    def _safe_path(self, filename: str, *, must_exist: bool) -> Path:
        if not isinstance(filename, str) or not filename.strip():
            raise UnsafePathError("A non-empty relative Markdown filename is required.")

        candidate_name = filename.strip()
        pure = PurePath(candidate_name)
        if pure.is_absolute() or Path(candidate_name).is_absolute():
            raise UnsafePathError("Absolute paths are not allowed.")
        if ".." in pure.parts:
            raise UnsafePathError("Path traversal using '..' is not allowed.")
        if any(part.startswith(".") for part in pure.parts):
            raise UnsafePathError("Hidden files and directories are not available.")
        if pure.suffix.lower() != ".md":
            raise UnsafePathError("Only Markdown (.md) notes are available.")

        candidate = self.root.joinpath(*pure.parts)
        try:
            resolved = candidate.resolve(strict=must_exist)
            resolved.relative_to(self.root)
        except FileNotFoundError as exc:
            raise NoteNotFoundError(f"Note not found: {candidate_name}") from exc
        except (OSError, RuntimeError, ValueError) as exc:
            raise UnsafePathError("Requested path is outside the notes workspace.") from exc

        # resolve(strict=False) still resolves existing symlink parents.
        if not resolved.is_relative_to(self.root):
            raise UnsafePathError("Requested path is outside the notes workspace.")
        return resolved

    @staticmethod
    def _title(path: Path, content: str) -> str:
        for line in content.splitlines():
            if line.startswith("# "):
                return line[2:].strip() or path.stem.replace("-", " ").title()
        return path.stem.replace("-", " ").title()

    def list_notes(self) -> list[NoteSummary]:
        notes: list[NoteSummary] = []
        for path in sorted(self.root.rglob("*")):
            if path.is_symlink() or not path.is_file():
                continue
            relative_parts = path.relative_to(self.root).parts
            if path.suffix.lower() != ".md" or any(
                part.startswith(".") for part in relative_parts
            ):
                continue
            resolved = path.resolve()
            if not resolved.is_relative_to(self.root):
                continue
            relative = resolved.relative_to(self.root).as_posix()
            content = resolved.read_text(encoding="utf-8")
            notes.append(NoteSummary(title=self._title(resolved, content), path=relative))
        return notes

    def read_note(self, filename: str) -> NoteContent:
        path = self._safe_path(filename, must_exist=True)
        if not path.is_file():
            raise NoteNotFoundError(f"Note not found: {filename}")
        content = path.read_text(encoding="utf-8")
        return NoteContent(
            title=self._title(path, content),
            path=path.relative_to(self.root).as_posix(),
            content=content,
        )

    def search_notes(self, query: str) -> list[SearchMatch]:
        cleaned_query = query.strip()
        if not cleaned_query:
            raise NoteStoreError("Search query must not be empty.")
        needle = cleaned_query.casefold()
        matches: list[SearchMatch] = []
        for summary in self.list_notes():
            note = self.read_note(summary.path)
            position = note.content.casefold().find(needle)
            if position < 0 and needle not in note.title.casefold():
                continue
            if position < 0:
                position = 0
            start = max(0, position - 60)
            end = min(len(note.content), position + len(cleaned_query) + 100)
            snippet = " ".join(note.content[start:end].split())
            if start:
                snippet = f"…{snippet}"
            if end < len(note.content):
                snippet = f"{snippet}…"
            matches.append(SearchMatch(title=note.title, path=note.path, snippet=snippet))
        return matches

    def create_note(self, title: str, content: str) -> MutationResult:
        clean_title = title.strip()
        if not clean_title:
            raise NoteStoreError("Title must not be empty.")
        filename = slugify(clean_title)
        path = self._safe_path(filename, must_exist=False)
        if path.exists():
            raise NoteAlreadyExistsError(
                f"Note already exists: {filename}. Choose a different title."
            )
        body = content.strip()
        document = f"# {clean_title}\n"
        if body:
            document += f"\n{body}\n"
        path.write_text(document, encoding="utf-8")
        return MutationResult(path=filename, message=f"Created note: {filename}")

    def append_to_note(self, filename: str, content: str) -> MutationResult:
        if not content.strip():
            raise NoteStoreError("Content to append must not be empty.")
        path = self._safe_path(filename, must_exist=True)
        if not path.is_file():
            raise NoteNotFoundError(f"Note not found: {filename}")
        existing = path.read_text(encoding="utf-8")
        separator = "" if not existing or existing.endswith("\n\n") else "\n"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(f"{separator}{content.strip()}\n")
        relative = path.relative_to(self.root).as_posix()
        return MutationResult(path=relative, message=f"Appended to note: {relative}")
