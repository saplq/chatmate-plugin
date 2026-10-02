# ChatMate plugin

ChatMate connects the Telegram chats of your personal ChatMate bot to Claude. Ask what people wrote, find a message or a person, and get a reply or an approval request in your bot.

## Before you start

Open [@chatmate_aibot](https://t.me/chatmate_aibot?start=setup), create your bot and connect your chats there. History starts when a chat is connected.

## Claude (web, desktop, mobile)

Add the connector in one click: [Add ChatMate to Claude](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=ChatMate&connectorUrl=https%3A%2F%2Fwww.getchatmate.com%2Fapi%2Fconnector%2Fmcp). Click **Add**, then **Connect**, log in with Telegram and click **Allow**.

## Claude Code

```
claude plugin marketplace add saplq/chatmate-plugin
claude plugin install chatmate@chatmate
```

## Codex

```
codex plugin marketplace add saplq/chatmate-plugin
codex plugin add chatmate@chatmate
codex mcp login chatmate
```

The first connection opens the same Telegram login.

## Other MCP clients

Server: `https://www.getchatmate.com/api/connector/mcp` (OAuth 2.1 with PKCE).

## Privacy

The AI sees only chats connected to your bot. Turn off a chat, disconnect an AI, export or delete your data at [getchatmate.com/data-controls](https://www.getchatmate.com/data-controls). Privacy policy: [getchatmate.com/en/privacy](https://www.getchatmate.com/en/privacy).
