"""Environment-backed server configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings for the notes server."""

    notes_dir: Path
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> Settings:
        """Load settings without silently granting access to the current directory."""
        raw_notes_dir = os.getenv("MCP_NOTES_DIR")
        if not raw_notes_dir:
            raise RuntimeError(
                "MCP_NOTES_DIR is required. Set it to the directory containing your notes."
            )

        level = os.getenv("MCP_NOTES_LOG_LEVEL", "INFO").upper()
        allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if level not in allowed_levels:
            raise RuntimeError(
                f"MCP_NOTES_LOG_LEVEL must be one of {sorted(allowed_levels)}; got {level!r}."
            )

        return cls(notes_dir=Path(raw_notes_dir).expanduser(), log_level=level)
