#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
MCP_URL = "https://chatmate-plum.vercel.app/api/mcp"

codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
codex_mcp = json.loads((ROOT / ".codex-plugin/mcp.json").read_text())
claude_mcp = json.loads((ROOT / ".mcp.json").read_text())
marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())

assert codex["name"] == claude["name"] == "chatmate"
assert codex["version"] == claude["version"] == VERSION
assert codex_mcp["mcpServers"]["chatmate"]["url"] == MCP_URL
assert claude_mcp["mcpServers"]["chatmate"]["url"] == MCP_URL
assert marketplace["plugins"][0]["source"]["repo"] == "saplq/chatmate-plugin"
skill = (ROOT / "skills/chatmate/SKILL.md").read_text()
assert f'packageVersion: "{VERSION}"' in skill
assert "connection code" in skill.lower() and "never ask" in skill.lower()
for path in ROOT.rglob("*"):
    if path.is_file() and ".git" not in path.parts:
        content = path.read_bytes()
        assert (b"OAUTH_TOKEN_HASH_" + b"SECRET=") not in content
        assert (b"TELEGRAM_MANAGER_BOT_" + b"TOKEN=") not in content
print("ChatMate plugin package is structurally valid")
