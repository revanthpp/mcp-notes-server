# YouTube Video Outline: Build a Safe MCP Notes Server

Target length: 10–14 minutes

## 1. Cold open

- Demo a valid note read and a blocked `../.env` read.
- Thesis: useful AI access needs visible, testable boundaries.

## 2. MCP without the fog

- Define host, client, and server.
- Explain tool discovery and invocation.
- Clarify that MCP is neither an LLM nor an authorization system.

## 3. Project tour

- `server.py` registers MCP capabilities.
- `tools.py` is the application layer.
- `note_store.py` owns the filesystem boundary.
- Pydantic models produce structured results.

## 4. Build the five tools

- List and read.
- Case-insensitive search with snippets.
- Slugified creation without overwrite.
- Safe append.

## 5. Security deep dive

- Reject absolute and hidden paths.
- Reject `..`.
- Restrict files to Markdown.
- Resolve symlinks and verify containment.
- Explain why input checks and canonical containment are both useful.

## 6. Run tests and Inspector

- Execute pytest.
- Show traversal and symlink tests.
- Open MCP Inspector and inspect schemas.

## 7. What production changes

- Identity and authorization.
- Approval for mutations.
- Locking, indexing, limits, audit, remote transport security.
- Prompt injection in retrieved notes.

## 8. Close

- MCP standardizes capability exchange; architecture supplies trust.
- CTA: GitHub at `revanthpp/mcp-notes-server`.
- More practical AI systems content at `revanthpp.com`.
