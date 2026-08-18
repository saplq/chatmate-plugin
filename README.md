# ChatMate plugin

ChatMate connects ChatGPT to the Production remote MCP at `https://chatmate-plum.vercel.app/api/mcp`. It lets an authorized workspace inspect connection/source metadata, search minimized Telegram memory and, when separately enabled, send one bounded report only to the verified owner.

## Important boundaries

- Installation and OAuth are explicit user actions. A prompt or skill cannot install the plugin, connect an account or bypass consent.
- ChatMate identifies the workspace only after the owner confirms through the ChatMate authorization flow. If a fallback one-time code is offered, enter it only in that form, never in ChatGPT.
- Telegram text is untrusted evidence, never instructions.
- There is no arbitrary recipient input and no generic Telegram `sendMessage` proxy.
- No OpenAI API key is used by ChatMate. ChatGPT supplies the model; ChatMate supplies scoped tools and data.
- Scheduled Telegram write-back is not claimed until the exact ChatGPT surface passes an unattended live smoke. Unsupported runs keep their result in ChatGPT.

## ChatGPT private beta

Until directory approval, enable ChatGPT Developer mode, add the MCP URL above, inspect the listed tools and complete ChatMate OAuth. Where an OpenAI Git plugin package is available, install this repository first and then complete the same OAuth flow. See [SETUP.md](SETUP.md).

This repository is not an installer prompt and is not yet an official directory listing. Official availability will be claimed only after OpenAI review and approval.

The beta package keeps a provider-neutral `.mcp.json`. ChatGPT registration must first produce the real `plugin_asdk_app…` technical ID; only then may a reviewed `.app.json` mapping be added for submission. This repository never invents or hard-codes a placeholder application ID.

## Claude boundary

Claude packaging and marketplace submission are deferred. This release contains no Claude plugin manifest, marketplace entry or support claim. The root `.mcp.json` is the single provider-neutral remote MCP declaration used by the ChatGPT package and future reviewed integrations.

## Package layout

- `.codex-plugin/plugin.json`: OpenAI package metadata.
- `.mcp.json`: the single Production remote MCP declaration.
- `skills/chatmate/SKILL.md`: safe ChatMate workflows.
- `prompts/` and `templates/`: post-install starter prompts and optional task templates.

## Validate

```sh
python3 scripts/validate_package.py
```

The local validator requires no dependencies. The OpenAI plugin manifest is also validated with the official Codex plugin validator before release.
