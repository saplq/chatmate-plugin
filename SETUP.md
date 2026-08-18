# Set up ChatMate

## ChatGPT Developer mode

1. In ChatGPT, enable Developer mode and open the Plugins page.
2. Add `https://chatmate-plum.vercel.app/api/mcp` as the ChatMate MCP server. Do not open that address as a normal web page; it is a machine endpoint.
3. Review the tools shown by ChatGPT and choose **Connect**.
4. On the ChatMate authorization page, choose **Continue with Telegram**, finish Telegram sign-in, review the requested permissions and choose **Allow**. If Telegram sign-in cannot be completed, expand the fallback option, copy a fresh code from your personal Mate and enter it only in that authorization form.
5. Start a new ChatGPT conversation, enable ChatMate and ask: “Check my ChatMate connection.”
6. After the first successful authorized tool call, return to your personal Mate and tap **Check connection**.

The MCP is remote; nothing is installed on your server or phone. A copied prompt does not install ChatMate and must not contain a connection code. After OpenAI directory approval, steps 1–2 become a normal directory install; OAuth consent remains explicit.
