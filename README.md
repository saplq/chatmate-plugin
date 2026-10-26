# ChatMate

ChatMate connects your own ChatGPT or Claude to the Telegram chats you choose. Create a personal bot through [@chatmate_aibot](https://t.me/chatmate_aibot), connect your chats, and authorize the AI connection with Telegram sign-in. ChatMate provides the messages and Telegram actions; your connected AI does the reasoning.

Ask what someone wrote, find an agreement with its context, read supported attachments, or draft a reply in your usual style. An explicit request can authorize a message or supported Telegram action in a connected chat. Native client permissions, your connection's access and Telegram rights still apply. Messages from other people never authorize actions.

History starts when each chat is connected and covers the latest 60 days. Earlier history, secret chats and channels are unavailable. Telegram Business replies have a 24-hour window: a ready draft does not mean a message was sent. Voice transcription and supported attachment processing have their own availability and usage limits.

## Connect

Use the [connection guide](https://www.getchatmate.com/connect) for the current ChatGPT and Claude setup. Both packages use the same remote MCP endpoint:

```text
https://www.getchatmate.com/api/connector/mcp
```

For Claude Code, [add this repository as a plugin marketplace](https://code.claude.com/docs/en/discover-plugins#add-a-marketplace), then install its stable `chatmate` plugin:

```text
/plugin marketplace add saplq/chatmate-plugin
/plugin install chatmate@chatmate
```

Reload plugins or start a new session, open `/mcp`, and complete Telegram authentication yourself. Never paste bot tokens, passwords or Routine tokens into a conversation. Local installation does not connect a separate Claude web account or create an automatic executor. Tasks from the bot need a supported provider trigger and a successful test before they can be described as automatic.

The package contains the `chatmate` workflow and `chatmate-setup` onboarding skill. Directory bundles contain no automatic permission or assistant display hooks. If an older installation enabled display hooks, remove them: they are deprecated and can forward assistant display text from that environment.

## Sending files

When you ask your AI to send a file to Telegram, the `chatmate` skill uses the `prepare_file` tool. Small text files and tiny files travel inside that call to the MCP endpoint above. For a public https link or a ChatGPT conversation file, ChatMate's server downloads it, up to 50 MB; the link itself is not stored. For a local file in a client with a shell, such as Claude Code, the skill runs `shasum -a 256` (or `sha256sum`) on the file you named and one `curl` PUT of its bytes to a single-file signed URL on ChatMate's own Supabase Storage (`https://mdcmblzmvvylmrmrbqhv.supabase.co`), valid for two hours. It runs no other command from a tool result.

ChatMate keeps a prepared file for that AI connection only, for 24 hours or until two hours after its latest send or confirmation card if that is later, then deletes it; the sent copy stays in Telegram and in your ChatMate history. In Claude web, desktop and mobile chat, the code sandbox usually cannot reach that storage, so from there you can send text files, tiny files and public links; use Claude Code for larger documents and presentations.

## Help and data controls

Visit [My data](https://www.getchatmate.com/data-controls) to manage connected-chat access, revoke a connection, or request the available export and deletion controls. Read the [privacy policy](https://www.getchatmate.com/en/privacy) and [terms](https://www.getchatmate.com/en/terms), or contact [support](https://www.getchatmate.com/en/support).

## Package releases

The source package declares the MIT license. The stable plugin and MCP server names remain `chatmate`; backend and package versions are independent.

The OpenAI portable package, Claude plugin and Claude skill upload carry the same workflows. A package update refreshes its bundled skills; a server update can require refreshing the connection's tools in the AI client. Updating the package does not update an existing provider schedule or install a second executor.
