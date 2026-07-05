# Your AI Assistant Should Not Get Your Whole Hard Drive

There is a wonderfully bad way to make an AI assistant useful: give it access to
everything and hope it behaves.

Your tax returns? Available. That ancient `.env` file with a key you definitely
meant to rotate? Available. The folder named `final-final-v7-really-final`?
Tragically, also available.

Useful software needs access to things. Safe software needs boundaries around
that access. The tension between those statements is where the Model Context
Protocol, or MCP, becomes interesting.

## MCP is a protocol, not a wizard

MCP gives AI applications a standard way to discover and invoke tools, read
resources, and use reusable prompts. Think of it as a shared grammar between an
AI application and the systems that provide it with capabilities.

The application is the MCP host. It owns the chat experience and the model. An
MCP client inside that host connects to an MCP server. The server says, “Here are
the things I can do, here are the inputs they accept, and here are the results
they return.”

That is useful. It is not magical.

MCP does not make a dangerous tool safe. It does not determine whether the user
really intended a write. It does not turn model output into trusted input. It
standardizes the conversation so we can build and inspect those controls without
inventing a new integration every Tuesday.

## What we built

The MCP Notes Server is a small Python reference project. It exposes one
configured folder of Markdown notes through five tools:

1. list the available notes
2. read one note
3. search notes
4. create a note from a title and body
5. append text to an existing note

It also publishes a read-only note index and a reusable prompt for summarizing a
note. The official MCP Python SDK handles protocol registration and schema
discovery. A deliberately plain storage class handles files.

That separation is the lesson. The MCP layer knows how to speak MCP. The storage
layer knows which paths are legal. Neither needs to pretend it is the other.

## The architecture in one request

Suppose you ask your assistant, “What did I write about agent memory?”

The host sees that a `search_notes` tool exists. Its MCP client sends a tool call
to the notes server. The server validates the query, searches Markdown files
inside the configured workspace, and returns typed matches with short snippets.
The host gives that result to the model, which answers you.

For `read_note` and `append_to_note`, the filename goes through a stricter gate.
Absolute paths are rejected. Any `..` path component is rejected. Hidden paths
and non-Markdown extensions are rejected. The server resolves the final path,
including symlinks, and proves it still sits beneath the notes directory.

Only then does it touch the file.

This is defense in depth. A string check catches obvious traversal. Canonical path
resolution catches less obvious escapes. Centralizing the rule prevents one tool
from quietly inventing its own, weaker interpretation of “inside.”

## The most important configuration choice

The server reads `MCP_NOTES_DIR`. That directory is its world.

If you point it at a curated notes folder, the blast radius is understandable. If
you point it at your home directory, you have technically followed the setup
instructions while missing the point with impressive accuracy.

Least privilege is not an enterprise-only phrase. It can be as ordinary as
creating a folder called `ai-notes` and putting only the intended files in it.

## What can break

Path traversal is only one item on a longer list.

A note can contain prompt injection, such as instructions telling the model to
ignore its task. Retrieved text must remain untrusted data. A host can choose the
wrong tool. A user can approve a write without understanding it. Two appends can
race. A giant workspace can make naive search slow. Sensitive note text can end
up in model-provider or host logs even when the notes server logs no content.

Remote deployment adds another shelf of sharp objects: identity, per-user
authorization, TLS, session security, rate limits, tenant isolation, audit
retention, and incident response.

This project does not solve those problems by adding a padlock emoji to the
README. It names them, tests the boundary it does claim, and keeps the code small
enough to inspect.

## Why this matters in enterprise AI

Replace “Markdown folder” with a customer support system, document repository, or
finance platform. The pattern holds.

The MCP surface describes useful capabilities. Identity tells us who is calling.
Authorization decides which records and operations that identity may access. A
policy layer can require human approval for risky actions. The storage or API
layer enforces the final data boundary. Audit events preserve what happened
without spraying sensitive content through logs.

The model is one participant in that architecture. It is not the authorization
server, policy engine, database, or compliance program.

That framing makes agentic systems less mystical and more buildable. Tools become
APIs with schemas. Context becomes data with provenance. Autonomy becomes a set
of permitted operations, not a personality trait.

## A better first MCP project

A notes server is small enough to understand and real enough to expose the hard
questions. You can see discovery, invocation, structured results, local side
effects, error handling, and a security boundary in one repository.

Clone the project, point it at the sample notes, connect an MCP-compatible client,
and watch the calls. Then create a dedicated folder of your own. Inspect what the
assistant can see. Try an unsafe path and verify that it fails.

The goal is not to be impressed that an AI can read a file. Computers have been
crushing that demo for decades.

The goal is to understand exactly which file it can read, who decided that, and
what happens when it asks for another one.

Explore the project on GitHub at
[github.com/revanthpp/mcp-notes-server](https://github.com/revanthpp/mcp-notes-server)
and find more practical AI systems work at
[revanthpp.com](https://revanthpp.com).
