import asyncio
from pathlib import Path

from mcp_notes_server.config import Settings
from mcp_notes_server.server import create_server


def test_mcp_capabilities_are_discoverable_and_callable(tmp_path: Path) -> None:
    (tmp_path / "hello.md").write_text("# Hello\n\nMCP works.\n", encoding="utf-8")
    server = create_server(Settings(notes_dir=tmp_path, log_level="INFO"))

    async def exercise_server() -> None:
        tools = await server.list_tools()
        resources = await server.list_resources()
        prompts = await server.list_prompts()
        _, structured_result = await server.call_tool(
            "read_note", {"filename": "hello.md"}
        )

        assert [tool.name for tool in tools] == [
            "list_notes",
            "read_note",
            "search_notes",
            "create_note",
            "append_to_note",
        ]
        assert [str(resource.uri) for resource in resources] == ["notes://index"]
        assert [prompt.name for prompt in prompts] == ["summarize_note"]
        assert structured_result is not None
        assert structured_result["path"] == "hello.md"

    asyncio.run(exercise_server())
