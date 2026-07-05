from pathlib import Path

import pytest

from mcp_notes_server.config import Settings


def test_settings_load_from_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("MCP_NOTES_DIR", str(tmp_path))
    monkeypatch.setenv("MCP_NOTES_LOG_LEVEL", "debug")

    settings = Settings.from_env()

    assert settings.notes_dir == tmp_path
    assert settings.log_level == "DEBUG"


def test_settings_require_notes_directory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MCP_NOTES_DIR", raising=False)

    with pytest.raises(RuntimeError, match="MCP_NOTES_DIR is required"):
        Settings.from_env()


def test_settings_reject_invalid_log_level(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("MCP_NOTES_DIR", str(tmp_path))
    monkeypatch.setenv("MCP_NOTES_LOG_LEVEL", "LOUD")

    with pytest.raises(RuntimeError, match="MCP_NOTES_LOG_LEVEL"):
        Settings.from_env()
