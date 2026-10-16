# Set up ChatMate

The plugin includes the `chatmate` skill and the remote MCP server at `https://www.getchatmate.com/api/connector/mcp`. The four English setup prompts are in [setup-prompts.json](setup-prompts.json).

## Start in the private bot chat

Choose your AI in your private ChatMate child bot. The primary choices are `chatgpt` (ChatGPT Work) and `claude_routine` (Claude tasks from Telegram); `claude_web` (ordinary chat) and `claude_code` (local Code) are advanced alternatives. The bot sends one short setup request with Copy/Open controls. It invokes `chatmate-setup`; if a native Setup button is available it runs the same skill. Start by checking status, reuse working OAuth and a ready executor. The full setup prompt is an advanced fallback, not an additional required step. The AI then guides installation and OAuth if ChatMate is not available yet; the owner confirms the installation and Telegram sign-in/Allow themselves. Verify access before configuring automatic tasks, then return to the bot's Done, check button.

| Surface | How to start | Execution after setup |
| --- | --- | --- |
| `chatgpt` | Send the short setup request in Work on the web, or choose Setup if available. The setup checks actual Events capability. A supported draft-prefill URL for ordinary ChatGPT web is not documented. | Work web or desktop Work with Cloud can subscribe to MCP Events; verify one real owner task. |
| `claude_routine` | The HTTPS `https://claude.ai/code/new?q=...` button opens a Claude Code composer with the short setup request; the owner presses Send. It requires Code access and does not create a Routine itself. | Configure an account connector and cloud Routine. Save the API trigger through the protected ChatMate form and verify one owner task. |
| `claude_web` | Open ordinary Claude, paste and send the full prompt. | Manual retrieval and requests; ordinary chat does not continuously monitor Telegram. |
| `claude_code` | Paste and send the installation prompt in Claude Code on your computer; the bot's guide button explains this path. | Local MCP access; installation does not configure the web account or a cloud trigger. |

The [connect page](https://www.getchatmate.com/connect) carries the same prompts, Copy/Open controls and manual connection options as a fallback. Visiting it before or after connecting is not required. The short request fits Telegram's native CopyTextButton (256 characters); detailed protocol instructions remain in the skill/advanced fallback. No Open button sends the prompt automatically, and successful OAuth alone does not prove automatic execution.

## Installation and sign-in

- In Claude web/Desktop chat: Customize → Plugins → Add → Add marketplace → repository `saplq/chatmate-plugin`, then add ChatMate. Web-installed plugins belong to your account; local CLI-installed plugins do not sync back into it.
- In Claude Code 2.1.275+: `/plugin install chatmate --marketplace saplq/chatmate-plugin`. Confirm the source/scope, reload plugins or start a new session, then authenticate with `/mcp`. Earlier versions can add the marketplace first and install `chatmate@chatmate`.
- In ChatGPT: install/connect ChatMate through the available plugin settings or directory. Repository/local marketplaces depend on the client; do not claim a prompt silently installs a private plugin in consumer web. If unavailable, use the manual steps on the connect page.
- The owner signs in with Telegram and clicks Allow in the existing OAuth page. Do not ask them to give the AI a Telegram code, password, session or token. After sign-in, verify `get_connection_status` and `list_chats` before claiming access.

When executing a saved owner task, the setup prompts instruct the AI to call `begin_answer` before doing that task. Save its returned `answer_id` and keep the same `execution_id`: include both on every task-related `send_message`, `send_to_chat`, `request_approval`, `telegram_action` and `propose_action` call. In ChatGPT Work a task's send to another chat goes through `propose_action`: the owner confirms the card in the bot and ChatMate sends it. The server validates the pair and Stop blocks task actions that have not started. Standalone actions outside a claimed task omit both; never omit them to bypass Stop.

## ChatGPT Events

The portable manifest declares `extensions.com.openai.onboardingSkill`. In supported Work clients the owner chooses Setup or sends the short setup request; this provider-aware skill connects OAuth and subscribes in the same Work chat. The manifest does not guarantee a Setup button in every surface. Installation alone does not silently create an executor. The full prompt remains a fallback, not an additional required step.

Use Work on ChatGPT web; desktop Cloud requires an actual Events capability check. The setup skill (or full fallback prompt) guides installation/authentication, verifies `get_connection_status` and `list_chats`, then asks ChatGPT to subscribe to `owner.message.created` and `approval.resolved` for the owner's bot chat. The provider supplies the callback and signing secret to MCP; the user does not copy these into chat. Monitoring is configured only after subscription succeeds and one owner task works. Unsupported clients can use the tools manually.

## Claude Routine

Use [Claude Code Routines](https://claude.ai/code/routines) with an eligible Claude subscription and cloud access. Select a GitHub repository, an environment, ChatMate and only the other connectors needed. Account connectors are separate from MCP servers installed only in local Code. A Routine's saved instructions must explicitly read the canonical owner message UUID from `routine-fire-payload` and claim it with `begin_answer` before acting.

In the web UI choose an API trigger, save the Routine, then Generate token. `/schedule` creates scheduled routines but cannot create or revoke the API token; the command is unavailable inside a cloud session. The user saves the fire URL and token at [Connect Routine](https://www.getchatmate.com/connect/claude), after owner sign-in. The page supplies the saved Routine instructions and selects one executor for the private bot. The bearer token stays in Supabase Vault; only the canonical message UUID is sent to the Routine fire API. Never put the token in a chat, prompt, repository, screenshot or issue. After saving, new permitted owner messages trigger the Routine through the durable event outbox. Send one short task from Telegram and check readiness after its answer. `automation.status=needs_test` means configured, while `ready` requires an event-correlated delivered answer. Unknown API outcomes are terminal and are never automatically fired again; explicit 429 rejection is retried after Retry-After. A manual run still needs the canonical owner message UUID as task context before `begin_answer`.

The fire API uses Claude Code subscription usage and returns a new session URL. It does not stream the answer and has no idempotency key; never retry an unknown fire blindly. Connecting GPT and Claude does not establish automatic fallback. Choose one executor; a reserve requires its own configured trigger and exclusive task claim.

## Morning list (0.16)

The owner can get a weekday list of who is waiting for their reply, what they promised and what they are waiting for. Sections are separated by a blank line, empty ones are left out, and times are local. The schedule lives at the AI provider and the owner controls it there; ChatMate sends nothing on its own. Copyable prompt (translate it, keep the tool names):

```text
Каждый будний день в 08:30 присылай мне в бот утренний список одним сообщением через send_message. Сначала вызови catch_up за последние 24 часа, в нём ждущие ответа, обещания и новости всех чатов. Без catch_up ждущих бери из list_owner_asks за последние 24 часа, обещания и оплаты из list_loops, если он есть, иначе из переписки. Разделы «Ждут ответа», «Ты обещал», «Ты ждёшь» через пустую строку, пустые не пиши. У каждого имя и местное время из sent_at_local, а без него «3 часа назад», ниже одна строка, что нужно. Не объясняй, что проверил или пропустил. Если ничего не нужно, одна короткая строка. На каждую просьбу, где ответ очевиден из переписки, предложи карточку через propose_action.
```

In Claude it is a cloud Routine with a schedule trigger (Pro and up; Weekdays at 08:30 in local time, at least one hour apart) at [Claude Code Routines](https://claude.ai/code/routines) or `/schedule`, with the ChatMate connector and no unneeded connectors. In ChatGPT it is a scheduled task where that surface offers one with ChatMate. Setup works only when one run delivers the list in the bot.

## Claude Code answer hooks

Deprecated. The server draws the Thinking draft itself (a status line and the elapsed time), and `stream_answer` no longer shows display text in Telegram, so the [example hooks](examples/claude-answer-hooks.json) have no visible effect. Do not install them, and remove them from a project that has them: while enabled they still send every assistant display delta from that environment to ChatMate. `bind_answer` and `stream_answer` stay accepted so existing setups do not fail.

Sources: [Telegram CopyTextButton](https://core.telegram.org/bots/api#copytextbutton), [Claude Code draft links](https://support.claude.com/en/articles/14898120-open-the-claude-mobile-app-with-a-link), [Claude plugin installation](https://code.claude.com/docs/en/discover-plugins), [common hook inputs](https://code.claude.com/docs/en/hooks#common-input-fields), [MessageDisplay/MCP hooks](https://code.claude.com/docs/en/hooks#messagedisplay), [Routines](https://code.claude.com/docs/en/routines), [Routine fire API](https://platform.claude.com/docs/en/api/claude-code/routines-fire), [ChatGPT Events](https://developers.openai.com/plugins/build/mcp-events), [ChatGPT plugins](https://learn.chatgpt.com/docs/plugins).
