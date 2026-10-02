# ChatMate plugin

Connect the Telegram chats you choose to your own AI. ChatMate supplies the messages and tools; your AI handles the work and can return answers to your personal ChatMate bot.

## Start in your bot

1. Open [@chatmate_aibot](https://t.me/chatmate_aibot?start=setup), create your personal bot and connect your chats.
2. Choose ChatGPT or Claude in that bot. It sends the complete setup prompt in a copyable code block, with options for ordinary Claude, local Claude Code and cloud Routines.
3. Open the selected AI and send the prompt yourself. ChatGPT and ordinary Claude need you to paste it; the Claude Routine option opens a composer draft without sending it.
4. Let the AI guide installation and connection. Confirm the installation source and scope, then complete Telegram sign-in and **Allow** yourself. Never paste credentials or tokens into an AI conversation. Verify `get_connection_status`, `list_chats` and one owner task before relying on the connection.

Full prompts and manual connection instructions are also available at [getchatmate.com/connect](https://www.getchatmate.com/connect).

## Choose an execution surface

- **ChatGPT Work:** web Work or desktop Work with Cloud can subscribe through MCP Events when the surface supports them. Monitoring starts only after subscription succeeds. Ordinary chats and clients without Events support manual requests.
- **Claude web, desktop or mobile:** connect the account connector to read chats and make manual requests. OAuth alone does not start tasks when a Telegram message arrives.
- **Local Claude Code:** install this plugin and authenticate its MCP connection. This connection is separate from your Claude web account and a cloud Routine environment.
- **Claude cloud Routine:** choose a repository, environment and required account connectors. This release has no Routine trigger adapter or token setup form. Use **Run now** manually; automatic Telegram triggering remains incomplete. Supply the canonical owner message UUID as task context before claiming it.

Use one active executor for Telegram tasks. Connecting two AIs does not configure automatic fallback.

## Claude Code installation

In Claude Code 2.1.275 or later:

```text
/plugin install chatmate --marketplace saplq/chatmate-plugin
```

Confirm the source and installation scope, then reload plugins or start a new session. Open `/mcp` and authenticate ChatMate; complete the Telegram login yourself.

For Codex, install this repository through its plugin marketplace and authenticate the ChatMate MCP connection. The repository retains its Codex compatibility manifest and marketplace.

## Manual connector fallback

Add an OAuth MCP connector named **ChatMate** with this server URL:

```text
https://www.getchatmate.com/api/connector/mcp
```

Complete Telegram sign-in and **Allow**. The connector provides tools; use the setup prompt to configure the execution surface separately.

## Answer updates and optional hooks

Use explicit `update_answer` calls by default. The packaged [Claude Code display-hook example](skills/chatmate/examples/claude-answer-hooks.json) is disabled. Enable it only after explicitly choosing a dedicated Telegram-only project/environment; never install it globally or in a general AI-chat environment. It forwards every assistant display delta from that environment, including unbound text.

## Telegram actions in 0.10.0

A specific owner request authorizes the requested action and recipient. No additional ChatMate send switch or mandatory confirmation card is required; your AI client's write permissions and Telegram rights still apply. ChatMate supports 18 typed actions: text/replies/quotes, stored photos/documents/video/audio/voice/video notes/animations/stickers, reactions, edits and deletion of its own registered sends, copy/forward, locations/venues/contacts/dice, polls/quizzes and closing them, Business checklists and editing them, and pin/unpin.

Native checklists require a Business private chat. Reactions and native copy/forward are available in ordinary bot chats/groups, not on behalf of a Business user. Business replies and edits require an active connection with reply rights and a recent incoming message. Media reuse is limited to currently accessible attachments for the same child bot; new arbitrary uploads are not supported. Static sticker previews are readable on demand.

The complete [feature map and implementation references](https://github.com/saplq/chatmate/blob/main/docs/features.md) include prior capabilities and known limits. The [live test register](https://github.com/saplq/chatmate/blob/main/docs/live-tests.md) keeps real Telegram/provider checks separate from code and deployment verification.

## Your data

History starts when a chat is connected; ChatMate keeps its latest 60 days. Earlier messages, Secret Chats and channels are unavailable. Manage connected chats, AI access, export and deletion at [My data](https://www.getchatmate.com/data-controls). Read the [privacy policy](https://www.getchatmate.com/en/privacy).
