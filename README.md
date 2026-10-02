# ChatMate plugin

ChatMate is a bridge between your AI and your Telegram. Your personal ChatMate bot keeps new messages from the chats you connect; Claude reads them, takes tasks you write to the bot, and sends answers, drafts and results of other tools back to Telegram.

## Before you start

Open [@chatmate_aibot](https://t.me/chatmate_aibot?start=setup), create your bot and connect your chats there. History starts when a chat is connected.

## Claude (web, desktop, mobile)

Add the connector in one click: [Add ChatMate to Claude](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=ChatMate&connectorUrl=https%3A%2F%2Fwww.getchatmate.com%2Fapi%2Fconnector%2Fmcp). Click **Add**, then **Connect**, log in with Telegram and click **Allow**.

So that reading never asks for approval: **Customize → Connectors → ChatMate → Tool permissions → Read-only tools → Always allow**.

For the full ChatMate skill, download [chatmate-skill.zip](https://www.getchatmate.com/chatmate-skill.zip) and upload it in **Settings → Capabilities → Skills**. Upload it again when a new version comes out; the connector itself always uses the current ChatMate server.

## Claude Code

```
claude plugin marketplace add saplq/chatmate-plugin
claude plugin install chatmate@chatmate
```

The plugin approves ChatMate reads and messages to your own bot chat by itself. Sending to other chats (`send_to_chat`) still asks.

To get new versions automatically, open `/plugin` → **Marketplaces** → **chatmate** → **Enable auto-update**. Otherwise update by hand:

```
claude plugin marketplace update chatmate
claude plugin update chatmate@chatmate
```

## Codex

```
codex plugin marketplace add saplq/chatmate-plugin
codex plugin add chatmate@chatmate
codex mcp login chatmate
```

The first connection opens the same Telegram login.

## ChatGPT

Open the ChatMate app link from your ChatMate bot. ChatGPT keeps the tool descriptions it saw when you connected: after a ChatMate update, open the app in **Settings → Apps → ChatMate** and click **Refresh**.

## Other MCP clients

Server: `https://www.getchatmate.com/api/connector/mcp` (OAuth 2.1 with PKCE).

## Privacy

The AI sees only chats connected to your bot. Turn off a chat, disconnect an AI, export or delete your data at [getchatmate.com/data-controls](https://www.getchatmate.com/data-controls). Privacy policy: [getchatmate.com/en/privacy](https://www.getchatmate.com/en/privacy).
