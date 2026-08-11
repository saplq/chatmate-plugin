# ChatMate plugin 0.2.0

ChatMate turns owner-authorized Telegram memory into concise private secretary briefs through one remote MCP at `https://chatmate-plum.vercel.app/api/mcp`.

The plugin can search canonical memory, keep a structured secretary schedule and style profile, and deliver morning, evening, or explicitly requested reports only to the workspace owner's verified private Mate.

## Trust boundary

- Installation and OAuth consent are explicit owner actions.
- The one-use `mate_…` code is entered only in the ChatMate pairing page. It is never a permanent bearer token and never belongs in a prompt.
- Telegram text is untrusted evidence, never instructions.
- `send_companion_report` has no recipient input. It cannot write to contacts, groups, channels, or business chats.
- `chatmate.secretary.manage` stores the owner's schedule, structured style traits, and reminder state.
- No OpenAI API key is required for secretary workflows. The connected ChatGPT account provides inference.
- Third-party drafting and sending are not available in 0.2.0.

## Install during founder beta

Install the versioned ChatMate plugin package, complete its OAuth consent, then use the single setup text copied from the personal Mate. Raw MCP URL entry is only for Developer mode. Public directory availability is not claimed until submission is approved.

For Claude private testing, run `/plugin marketplace add saplq/chatmate-plugin`, then `/plugin install chatmate@chatmate` and complete OAuth. See [SETUP.md](SETUP.md).

## Package layout

- `.codex-plugin/plugin.json` and `.mcp-openai.json`: OpenAI metadata and remote MCP.
- `.claude-plugin/plugin.json` and `.mcp.json`: Claude metadata and the same MCP.
- `skills/chatmate/SKILL.md`: cached, versioned secretary workflow and safety policy.
- `templates/morning-brief.md` and `templates/evening-brief.md`: weekday scheduled-task instructions.
- `prompts/starter-prompts.md`: RU, UA, and EN setup and use prompts.

The skill does not fetch GitHub or check its version on each request. Updates arrive through versioned plugin releases. `connection_status` is reserved for setup, diagnostics, and authentication failures.

## Validate

```sh
python3 scripts/validate_package.py
claude plugin validate .
```

The local validator has no dependencies. `claude plugin validate` requires Claude Code.
