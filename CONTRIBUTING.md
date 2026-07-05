# Contributing

Thanks for helping make MCP easier to understand through a practical, approachable
reference project.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
ruff check .
```

Create a focused branch and keep pull requests small. Add tests for behavior
changes, especially any change involving paths, files, or permissions. Update the
README when commands or MCP capabilities change.

## Design principles

- Keep the storage boundary independent from the MCP transport.
- Prefer obvious code over framework cleverness.
- Treat all tool arguments and note content as untrusted.
- Never weaken a security check merely to make a demo easier.
- Keep examples approachable to a developer who is new to MCP.

Do not include real secrets, private notes, generated environments, or vendor
directories. By contributing, you agree that your work is licensed under the
project's MIT License.
