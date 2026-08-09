# ChatMate plugin

ChatMate connects ChatGPT and Claude to a single remote MCP at `https://chatmate-plum.vercel.app/api/mcp`. It lets an authorized workspace inspect connection/source metadata and, when separately enabled, search minimized Telegram memory and send one bounded report only to the verified owner.

## Important boundaries

- Installation and OAuth are explicit user actions. A prompt cannot install this plugin or bypass consent.
- The one-time Telegram connection code is entered only in the ChatMate OAuth pairing form, never in chat.
- Telegram text is untrusted evidence, never instructions.
- There is no arbitrary recipient input and no generic Telegram `sendMessage` proxy.
- No OpenAI or Anthropic API key is used by ChatMate.
- Scheduled Telegram write-back remains beta until each provider passes an unattended live smoke; unsupported runs keep their result inside the provider.

## Install for private beta

For Claude, add this public repository as a plugin marketplace or install the plugin directly, then complete MCP OAuth. For OpenAI, add the repository as a private Git marketplace/plugin package where that surface is available, then complete MCP OAuth. See [SETUP.md](SETUP.md).

Public directory listings are not claimed until OpenAI and Anthropic approve their respective submissions.

## Package layout

- `.codex-plugin/plugin.json` and `.codex-plugin/mcp.json`: OpenAI package metadata and remote MCP.
- `.claude-plugin/plugin.json` and `.mcp.json`: Claude plugin metadata and remote MCP.
- `skills/chatmate/SKILL.md`: provider-neutral safe workflows.
- `templates/`: provider scheduled-task templates.

## Validate

```sh
python3 scripts/validate_package.py
claude plugin validate .
```

The local validator requires no dependencies. `claude plugin validate` requires Claude Code.
