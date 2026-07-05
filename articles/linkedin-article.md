# Your AI Assistant Should Not Get Your Whole Hard Drive

The fastest way to make an AI assistant look capable is to give it broad access.
The fastest way to make an AI system indefensible is often the same thing.

I built the **MCP Notes Server** to make one idea concrete: MCP is not magic. It
is a standard way for AI applications to discover and use tools, resources, and
context. The security still comes from the architecture around those tools.

The project exposes a local Markdown workspace through five operations: list,
read, search, create, and append. An MCP-compatible host can discover each tool
and its schema through the official Python SDK.

The more important feature is the boundary. The server rejects absolute paths,
`..` traversal, hidden files, non-Markdown files, and symlinks that escape the
configured directory. Creation slugifies titles and refuses to overwrite an
existing note.

This makes the architecture easy to see:

- The host owns the model, user experience, and consent.
- The MCP client connects the host to a server.
- The server exposes a narrow contract.
- The storage layer enforces what “narrow” actually means.

In an enterprise system, the same pattern might sit in front of a document
repository or customer platform. The folder boundary becomes tenant and
record-level authorization. Local configuration becomes identity and policy.
Simple logs become redacted audit events. Stdio may become authenticated remote
transport.

The model remains one participant. It does not become the policy engine because
it asked nicely.

The repository includes tests, Mermaid diagrams, a threat model, sample notes,
and beginner-friendly documentation. It is intentionally simple code with
serious boundaries.

GitHub: [github.com/revanthpp/mcp-notes-server](https://github.com/revanthpp/mcp-notes-server)

More practical AI systems work: [revanthpp.com](https://revanthpp.com)
