# 45–60 Second Short-Form Script

**Hook (0–5s)**

Visual: A file picker zooms out from a notes folder to an entire hard drive.

Narration: “Your AI assistant does not need your whole hard drive just to read
three notes.”

**Setup (5–17s)**

Visual: Simple animation: AI Host → MCP Client → Notes Server → Notes Folder.

Narration: “That is where MCP helps. It gives AI applications a standard way to
discover and call tools. It is a protocol, not a magic permission shield.”

**Demo moment (17–40s)**

Visual: Show `list_notes`, then `read_note("mcp-basics.md")`. Next, try
`read_note("../.env")` and show the rejection.

Narration: “I built a Python MCP notes server that can list, read, search,
create, and append Markdown notes. Every path stays inside one configured
workspace. Absolute paths, dot-dot traversal, hidden files, and escaping
symlinks are rejected.”

**Takeaway (40–50s)**

Visual: Highlight “MCP contract” and “security boundary” as separate layers.

Narration: “MCP standardizes the tool contract. Your code still has to enforce
the boundary. That distinction is the whole lesson.”

**CTA (50–60s)**

Visual: GitHub repository and revanthpp.com URLs.

Narration: “Clone the full beginner-friendly project on GitHub at revanthpp slash
mcp-notes-server, and find more practical AI systems work at revanthpp.com.”
