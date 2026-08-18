#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.2.0"
MCP_URL = "https://chatmate-plum.vercel.app/api/mcp"

codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
mcp = json.loads((ROOT / ".mcp.json").read_text())

assert codex["name"] == "chatmate"
assert codex["version"] == VERSION
assert codex["mcpServers"] == "./.mcp.json"
assert mcp["mcpServers"]["chatmate"]["url"] == MCP_URL
assert set(mcp["mcpServers"]["chatmate"]) == {"type", "url"}
assert not (ROOT / ".claude-plugin/plugin.json").exists()
assert not (ROOT / ".claude-plugin/marketplace.json").exists()
skill = (ROOT / "skills/chatmate/SKILL.md").read_text()
assert f"Package version: `{VERSION}`" in skill
assert "connection_status" in skill and "empty input object" in skill
assert "fallback connection code" in skill.lower() and "never ask" in skill.lower()
assert "search_memory" not in skill and "get_memory_context" not in skill
for path in ROOT.rglob("*"):
    if path.is_file() and ".git" not in path.parts:
        content = path.read_bytes()
        assert (b"OAUTH_TOKEN_HASH_" + b"SECRET=") not in content
        assert (b"TELEGRAM_MANAGER_BOT_" + b"TOKEN=") not in content
print("ChatMate plugin package is structurally valid")
