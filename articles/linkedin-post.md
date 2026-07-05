Your AI assistant should not get your whole hard drive.

I built a beginner-friendly MCP Notes Server to show what safe tool access
actually looks like.

It lets an MCP-compatible AI app:

• list Markdown notes
• read and search them
• create safely named notes
• append to existing notes

The real feature is the boundary.

Absolute paths? Rejected.
`..` traversal? Rejected.
Hidden files and `.env`? Rejected.
Symlinks escaping the workspace? Also rejected.

MCP standardizes how applications discover and invoke tools. It does not replace
permissions, validation, user consent, or security design.

The repo includes Python code, pytest coverage, architecture diagrams, a threat
model, sample notes, and a plain-English walkthrough.

GitHub: https://github.com/revanthpp/mcp-notes-server
More: https://revanthpp.com

#MCP #Python #AISecurity #AgenticAI #OpenSource
