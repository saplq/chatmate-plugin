# Set up ChatMate Secretary

## Normal connection

1. Install or enable the published ChatMate plugin in ChatGPT.
2. In your personal Mate in Telegram, choose ChatGPT and open the connection page.
3. Complete OAuth consent for connection status, sources, memory search, owner-only report delivery, and secretary settings.
4. Paste the one-use `mate_…` code only into the ChatMate pairing page. The code expires after 10 minutes and is invalid after one successful exchange.
5. Return to Telegram and choose **Check connection**.
6. Choose **Copy setup** and paste that text once into ChatGPT.

The skill saves language and timezone, builds one structured style profile, and creates two scheduled tasks at 09:00 and 18:00 Monday through Friday. It does not copy raw writing samples into the profile.

If owner-only delivery permission is missing, search and report generation continue in ChatGPT. Reconnect only when you want reports delivered to the private Mate.

## Developer mode

Raw MCP URL entry is for Developer mode only:

`https://chatmate-plum.vercel.app/api/mcp`

Do not search for that URL in the public plugin catalog. The catalog resolves published plugin packages, not arbitrary MCP endpoints.
