# Set up ChatMate

The plugin includes the `chatmate` skill and the remote MCP server at `https://www.getchatmate.com/api/connector/mcp`. The four English setup prompts are in [setup-prompts.json](setup-prompts.json).

## Start in the private bot chat

Choose your AI in your private ChatMate child bot. The primary choices are `chatgpt` (ChatGPT Work) and `claude_routine` (Claude tasks from Telegram); `claude_web` (ordinary chat) and `claude_code` (local Code) are advanced alternatives. The bot sends the full setup prompt in a code block and an Open button. Copy the full block, open your AI and send the prompt. The AI then guides installation and OAuth if ChatMate is not available yet; the owner confirms the installation and Telegram sign-in/Allow themselves. Verify access before configuring automatic tasks, then return to the bot's Done, check button.

| Surface | How to start | Execution after setup |
| --- | --- | --- |
| `chatgpt` | Open ChatGPT, select Work, paste and send the full prompt. A supported draft-prefill URL for ordinary ChatGPT web is not documented. | Work web or desktop Work with Cloud can subscribe to MCP Events; verify one real owner task. |
| `claude_routine` | The HTTPS `https://claude.ai/code/new?q=...` button opens a Claude Code composer with the full prompt; the owner presses Send. It requires Code access and does not create a Routine itself. | Configure an account connector and cloud Routine. The ChatMate trigger adapter is not implemented here: use Run now/manual execution. |
| `claude_web` | Open ordinary Claude, paste and send the full prompt. | Manual retrieval and requests; ordinary chat does not continuously monitor Telegram. |
| `claude_code` | Paste and send the installation prompt in Claude Code on your computer; the bot's guide button explains this path. | Local MCP access; installation does not configure the web account or a cloud trigger. |

The [connect page](https://www.getchatmate.com/connect) carries the same prompts, Copy/Open controls and manual connection options as a fallback. Visiting it before or after connecting is not required. Telegram's native CopyTextButton is limited to 256 characters, so it cannot carry the full setup prompt. No Open button sends the prompt automatically, and successful OAuth alone does not prove automatic execution.

## Installation and sign-in

- In Claude web/Desktop chat: Customize → Plugins → Add → Add marketplace → repository `saplq/chatmate-plugin`, then add ChatMate. Web-installed plugins belong to your account; local CLI-installed plugins do not sync back into it.
- In Claude Code 2.1.275+: `/plugin install chatmate --marketplace saplq/chatmate-plugin`. Confirm the source/scope, reload plugins or start a new session, then authenticate with `/mcp`. Earlier versions can add the marketplace first and install `chatmate@chatmate`.
- In ChatGPT: install/connect ChatMate through the available plugin settings or directory. Repository/local marketplaces depend on the client; do not claim a prompt silently installs a private plugin in consumer web. If unavailable, use the manual steps on the connect page.
- The owner signs in with Telegram and clicks Allow in the existing OAuth page. Do not ask them to give the AI a Telegram code, password, session or token. After sign-in, verify `get_connection_status` and `list_chats` before claiming access.

When executing a saved owner task, the setup prompts instruct the AI to call `begin_answer` before doing that task. Save its returned `answer_id` and keep the same `execution_id`: include both on every task-related `send_message`, `send_to_chat`, `request_approval` and `telegram_action` call. The server validates the pair and Stop blocks task actions that have not started. Standalone actions outside a claimed task omit both; never omit them to bypass Stop.

## ChatGPT Events

Use Work on ChatGPT web, or desktop Work with Cloud. The `chatgpt` prompt guides installation/authentication, verifies `get_connection_status` and `list_chats`, then asks ChatGPT to subscribe to `owner.message.created` and `approval.resolved` for the owner's bot chat. The provider supplies the callback and signing secret to MCP; the user does not copy these into chat. Monitoring is configured only after subscription succeeds and one owner task works. Unsupported clients can use the tools manually.

## Claude Routine

Use [Claude Code Routines](https://claude.ai/code/routines) with an eligible Claude subscription and cloud access. Select a GitHub repository, an environment, ChatMate and only the other connectors needed. Account connectors are separate from MCP servers installed only in local Code. A Routine's saved instructions must explicitly read the canonical owner message UUID from `routine-fire-payload` and claim it with `begin_answer` before acting.

In the web UI choose an API trigger, save the Routine, then Generate token. `/schedule` creates scheduled routines but cannot create or revoke the API token; the command is unavailable inside a cloud session. The user saves the fire URL and token through a protected integration form or secret store only when the ChatMate adapter is available. Never put the token in a chat, prompt, repository, screenshot or issue. This version has no Routine adapter or token setup form, so it cannot automatically trigger a Routine from Telegram: offer Run now/manual use and state automatic setup is incomplete. A manual run still needs the canonical owner message UUID as task context before `begin_answer`.

The fire API uses Claude Code subscription usage and returns a new session URL. It does not stream the answer and has no idempotency key; never retry an unknown fire blindly. Connecting GPT and Claude does not establish automatic fallback. Choose one executor; a reserve requires its own configured trigger and exclusive task claim.

## Claude Code answer hooks

Default installation has no display forwarding. Use explicit `update_answer` calls. The optional [example hooks](examples/claude-answer-hooks.json) are only for a dedicated Telegram-only Claude Code project/environment, after the user explicitly chooses it. Merge the example's `hooks` into that project's `.claude/settings.local.json`, preserving existing settings; never install it globally or in a general AI-chat environment. Enabling it sends every assistant display delta from that environment to ChatMate, including unbound text. Server binding restricts Telegram delivery but cannot prevent that initial transport. Claude documents no local conditional/stateful `mcp_tool` handler that filters MessageDisplay by a current task; `if` applies only to tool events, and MessageDisplay has no matchers.

In the opt-in example, PostToolUse matches only `begin_answer`; it binds the original canonical owner `message_id` and `execution_id` from `tool_input` to the provider `session_id` and current `prompt_id`. It does not guess the shape of `tool_response`. MessageDisplay sends the same session/prompt plus its documented display `turn_id`, assistant `message_id`, `index`, `final` and `delta` to `stream_answer`. This reuses the configured OAuth MCP, with no script or extra hook secret.

Only an accepted, current binding can update a Telegram answer. Other sessions/prompts are ignored for Telegram delivery; finish, stop, expiry or revoked access prevents it. Missing/invalid IDs must fail without Telegram forwarding. The first display turn is fenced by the binding and later turns cannot replace it. Message/index deduplicates batches. Claude's string interpolation may send `index` and `final` as strings; the server accepts only strict decimal indices and `true`/`false`.

Interactive Code provides completed-line batches, not individual tokens. Non-interactive Code can supply one whole assistant message after it completes. A MessageDisplay `final` does not complete the task; `finish_answer` does. Routine/cloud cadence and client support require a live test; otherwise use explicit `update_answer` phase/text calls.

Sources: [Telegram CopyTextButton](https://core.telegram.org/bots/api#copytextbutton), [Claude Code draft links](https://support.claude.com/en/articles/14898120-open-the-claude-mobile-app-with-a-link), [Claude plugin installation](https://code.claude.com/docs/en/discover-plugins), [common hook inputs](https://code.claude.com/docs/en/hooks#common-input-fields), [MessageDisplay/MCP hooks](https://code.claude.com/docs/en/hooks#messagedisplay), [Routines](https://code.claude.com/docs/en/routines), [Routine fire API](https://platform.claude.com/docs/en/api/claude-code/routines-fire), [ChatGPT Events](https://developers.openai.com/plugins/build/mcp-events), [ChatGPT plugins](https://learn.chatgpt.com/docs/plugins).
