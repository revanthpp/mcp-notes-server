# Security Policy and Threat Model

## The short version

Local tool access is powerful because it connects model output to real data and
side effects. It is dangerous for exactly the same reason. A polite tool
description is not a permission system, and a model promise is not sandboxing.

Configure the smallest notes directory you need. Do not point this server at your
home directory, repository root, or filesystem root.

## Supported versions

This project is pre-1.0. Security fixes are applied to the latest revision on the
default branch.

## Assets and trust boundaries

The protected assets are files outside the notes workspace, sensitive notes
inside it, and the integrity of existing notes. Inputs from the MCP client,
model-generated filenames, note content, and symlinks are treated as untrusted.

The configured workspace path is trusted administrator input. The local operating
system account and MCP host are partially trusted: either can already possess
authority beyond this process.

## Threats addressed here

- absolute path reads and writes
- `..` traversal
- hidden-file access such as `.env`
- access to non-Markdown files
- symlinks that resolve outside the workspace
- accidental overwrite during note creation
- protocol corruption from logs written to stdout
- sensitive note content copied into ordinary application logs

The server uses lexical rejection plus canonical path containment. Both matter:
blocking `..` makes policy clear, while resolving and checking the final target
protects against symlink and normalization tricks.

## Threats not fully addressed

- a compromised or malicious local OS account
- a workspace itself containing sensitive Markdown files
- prompt injection contained inside notes
- denial of service through huge files or many files
- concurrent writes, races, or filesystem changes between check and use
- backups, filesystem snapshots, model-provider retention, or host-side logs
- remote access, authentication, multi-tenancy, and network transport security

This is a local teaching server, not a hardened sandbox. OS-level process
isolation remains valuable.

## Safe operation

1. Create a dedicated notes directory with only the files you intend to expose.
2. Run the server as a low-privilege user.
3. Keep write actions visible and require confirmation in the host when possible.
4. Review logs and dependency updates, but never log note bodies or secrets.
5. Prefer local stdio. Do not expose this server directly to a network.
6. Back up important notes before allowing automated mutation.

## Reporting a vulnerability

Please do not open a public issue for an undisclosed vulnerability. Use GitHub's
private vulnerability reporting for `revanthpp/mcp-notes-server`. Include the
affected revision, reproduction steps, impact, and any suggested mitigation.
You should receive an acknowledgment within seven days.
