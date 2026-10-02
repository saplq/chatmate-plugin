# ChatMate data reference

## Contents
- Message fields
- People
- Service event types
- Coverage and gap reasons
- Sending and statuses
- Errors
- Limits and paging

## Message fields

| Field | Meaning |
|---|---|
| `chat_title` | Group name, the other person's name in a private chat, or "My ChatMate" for the user's chat with the bot |
| `author.display_name`, `author.username` | Who wrote it. `author.is_owner` is true for the user |
| `author.person_id` | The same person in every connected chat of this user (an opaque id, not a Telegram id). Use it with `get_messages` and `search_messages` |
| `text`, `caption` | What was written; a caption belongs to media. `text_truncated` with `text_cursor` means there is more |
| `links`, `links_truncated` | Complete HTTP(S) destinations with `location` (`text`, `caption`, `preview`, `rich`); query parameters are preserved. More than 64 links or the 8192-byte link budget is marked partial; the backend never opens these URLs |
| `reply_preview` | The message this one answers: `author`, `is_owner`, `excerpt`, `quote` (the selected part), `quote_manual`, `quote_position`, `origin_type`, `media`, `from_other_chat` |
| `reply_to_id`, `reply_missing` | The stored original, or `reply_missing: true` when it is not stored (older than ChatMate or not available) |
| `forwarded_from` | Original sender name, date and `origin_type` of a forwarded message; hidden names do not prove a person's identity |
| `service` | Chat event instead of a message, see below |
| `shared` | `poll` (question/options and available received counts/anonymity/time), `location`, `venue` (title, address), `contact` (name, phone), `dice`, `checklist` (task IDs, text, done and available completion time/actor) |
| `rich` | Simple `tables`; `partial` and `reasons` flag omitted/limited rich content. Readable text is in `text`; rich links are in `links` |
| `attachments` | `type` (photo, video, animation, sticker, voice, video_note, audio, document, unsupported), `filename`, `mime`, `size` in bytes, `duration` in seconds, `width`, `height`, sticker `emoji`, audio `title`. Use its `id` and `version` with `get_attachment` when content is needed |
| `automated` | Away message or a reply sent by a business bot |
| `edited_at`, `edit_history` | When the text was last edited, and up to 5 earlier versions (`text`, `caption`, `edited_at` of that version, `replaced_at`), oldest first. Long versions are cut at 1000 characters with `text_truncated` |
| `reactions` | Per emoji (`emoji`, `custom_emoji_id` for a custom one, or `paid`): `count` and up to 10 people in `by` (`person_id`, `display_name`, `is_owner`). Anonymous reactions have a count only. Groups only, and only while the bot is an administrator |
| `deleted`, `deleted_at` | The message was deleted in a private chat; author, text and attachments are gone. `deleted_at` is when ChatMate learned of it |
| `album_id`, `thread_id`, `thread_title` | Media sent together; forum topic and its name |

## People

`list_people` returns people who wrote or reacted in the connected chats in the latest 60 days of stored history, most recently active first: `person_id`, `display_name`, `username`, `is_owner`, `is_bot`, `messages` and `reactions` counts, `first_seen`, `last_seen`, and up to 20 `chats` with their own counts. `query` matches part of a name or @username. Names are what Telegram showed at the time and can repeat; telling people apart by `username` and `chats` is more reliable. Chat events such as joins are not counted as messages. `next_cursor` continues a people list: pass it as `cursor` and repeat the same `query` and `chat_ids`; you can omit `limit` on continuation.

## Service event types

`members_joined` and `member_left` (with `names`), `title_changed` (new `title`), `photo_changed`, `photo_removed`, `chat_created`, `migrated_to_supergroup`, `migrated_from_group`, `pinned` (with `excerpt`), `topic_created`, `topic_edited`, `topic_closed`, `topic_reopened`, `auto_delete_changed`, `video_chat`. Other Telegram events keep their Telegram name.

## Coverage and gap reasons

- `observed_from` and `observed_through`: the period ChatMate has messages for in the scope.
- `known_gaps[].reason`:
  - `content_denied`: the chat was not allowed when the message came (for example before a group was connected, or after the user turned the chat off);
  - `source_revoked`, `consent_revoked`, `privacy_revoke`, `access_closed`: the user turned off the chat, storage or access;
  - `business_reconnect`, `generation_closed`: the bot or Chat Automation was reconnected;
  - `raw_expired`, `retries_exhausted`: ChatMate could not process the message in time.
- `unprocessed_media_count`: photos, videos, voice messages and files without retained derivative text. On-demand reads are not cached and do not decrease this count.
- Deleted private-chat messages stay in place as `deleted: true`. Telegram does not tell bots about deletions in groups, so a deleted group message keeps its last text.
- Reactions arrive only from groups where the bot is an administrator; private (Business) chats have none.

## Sending and statuses

- `send_message` goes only to the user's chat with their bot. `send_to_chat` goes to one business chat (as the user, through Chat Automation) or one group (as the user's ChatMate bot).
- `send_message`, `send_to_chat`, `request_approval` and `telegram_action` accept optional paired `answer_id` and `execution_id` UUIDs. Include both on every action for a claimed Telegram task, using its returned answer ID and original execution ID. The server checks the current grant, ownership and task state before accepting or starting the action; Stop blocks queued task actions that have not started. Standalone actions omit both. One without the other is invalid; never omit the pair to bypass Stop. An action already started or sent cannot be undone by stopping the task.
- Text is plain, up to 4000 characters per call. `reply_to_message_id` is a Telegram message number in that chat, not a ChatMate UUID. An owner event's `data.message_id` is the canonical UUID for `begin_answer`/`get_message_context`; never pass it as a Telegram reply number. For task answers use `finish_answer`, which resolves the original reply on the server; otherwise leave the reply number out unless explicitly provided by the tool.
- Statuses: `pending` (queued), `sent`, `awaiting_owner` (a confirmation request waits for the user), `approved`, `declined`, `failed` (Telegram refused, nothing was sent), `unknown` (Telegram did not answer: do not send again, tell the user to check the chat).

## Owner task answers (0.9)

- `begin_answer`: `{message_id, execution_id}`. Both are UUIDs; the message must be the owner's accessible private bot task. Keep the execution UUID on retries. Competing execution returns `ANSWER_CLAIMED`; stopped/unavailable execution must not continue.
- The result includes `answer_id`, `execution_id`, `status` (`active`, `finishing`, `finished`, `stopped`), `sequence`, `expires_at` and nullable `action`. Only `active` permits new preview updates. Delivery lives in `action.status`; `finished` alone does not prove Telegram delivery.
- `update_answer`: `{answer_id, execution_id, sequence, text?, phase?}`. Provide text or phase. Sequence is a non-negative increasing integer; old updates cannot roll the preview back. Text is accumulated, at most 4000 characters. Phases are `thinking`, `reading_conversation`, `checking_document`, `preparing_answer`.
- `finish_answer`: `{answer_id, execution_id, text, idempotency_key}`. Final text is 1–4000 characters. This sends one durable reply to the original owner message; preserve the key and inspect `answer_status` (`{answer_id}`). Never silently cut a longer result or repeat a finish through another send tool; give a short complete answer plus a supporting document/link when needed.
- The optional dedicated-environment hook example uses `bind_answer` (`message_id`, `execution_id`, provider `session_id`, `prompt_id`) and `stream_answer` (same session/prompt, display `turn_id`, assistant `message_id`, `index`, `final`, `delta`). Default installation uses explicit `update_answer` calls and does not forward display text. With the example enabled, even unbound deltas reach ChatMate; a missing binding ignores them for Telegram delivery, and `final` does not call finish. See [setup.md](setup.md) for the opt-in scope and client limits.

## Typed Telegram actions (0.9)

`telegram_action` accepts `{chat_id, idempotency_key, payload, answer_id?, execution_id?}`. Include the two task IDs together for a claimed task, as described above. `chat_id` is the connected ChatMate source UUID from `list_chats`; Telegram destinations are resolved by the server. Sending must be enabled and the user must approve the exact action/content/recipient. Read delivery with `get_approval_status` (`{action_id}`). Keep the idempotency key; after `unknown` never repeat it through a new key.

| `payload.operation` | Other payload fields |
|---|---|
| `send_poll` | `question` (1–300 chars), `options` (1–12 strings, 1–100 chars), optional `is_anonymous`, `allows_multiple_answers` |
| `stop_poll` | `action_id` of this bot's registered create-poll action |
| `send_checklist` | `checklist` with `title` (1–255 chars), 1–30 tasks (`id` 1–999999999, unique; `text` 1–100 chars); optional `others_can_add_tasks`, `others_can_mark_tasks_as_done` |
| `edit_checklist` | Original registered `action_id` and replacement `checklist` |
| `pin` | Accessible canonical `message_id`, optional `disable_notification` |
| `unpin` | Accessible canonical `message_id` |

Native checklist create/edit requires a Business connection; ordinary child/group checklist creation is unsupported. Poll and pin actions depend on source/Telegram permissions and can be rejected. No generic Bot API payload, editPoll, checklist done toggle, unpin-all or arbitrary message editing.

## Errors

| Code | Meaning | What to do |
|---|---|---|
| `INVALID_TOKEN` | The AI connection expired or was turned off | Ask the user to reconnect ChatMate |
| `CONSENT_REQUIRED` | Storage or writing is not allowed yet | Point the user to their ChatMate bot or getchatmate.com/data-controls |
| `SEND_DISABLED` | Sending to chats is off | The user turns it on: bot, /menu, AI |
| `FORBIDDEN`, `NOT_FOUND` | The chat or message is not available to this connection | Use `list_chats` again; the chat may be turned off |
| `CURSOR_INVALID`, `CURSOR_EXPIRED` | A page cursor no longer matches | Repeat the request without the cursor |
| `INVALID_ARGUMENT` | Wrong input, for example an end date before the start date | Fix the input |
| `TEMPORARY_UNAVAILABLE` | ChatMate could not answer | Retry once, then tell the user |
| `ANSWER_CLAIMED`, `ANSWER_STOPPED` | Another execution owns the task, or it was stopped | Stop work and new delivery; do not use a different send tool to bypass it |

## Attachment errors and limits

- `MEDIA_UNAVAILABLE`: Telegram did not provide the file, or decoding failed; ask for a resend or a link.
- `MEDIA_TOO_LARGE`: download exceeds 18 MiB (below the hosted Telegram API limit); ask for a smaller copy/link.
- `ORIGINAL_TOO_LARGE`: binary original exceeds the 2 MiB MCP result budget; use `auto` for supported pages/text.
- `MEDIA_TOO_COMPLEX`: file exceeds parser, pixel, page or time limits; ask for a smaller/simpler document.
- `UNSUPPORTED_MEDIA`: no reader for this format. `DOCUMENT_LOCKED`: encrypted/password-protected copy.
- `get_attachment`: `attachment_id`, `version`, optional `representation` (`auto`, `text`, `image`, `original`), PDF `page` (1–2000), text `offset`. Follow returned `next_offset` before `next_page`; never assume one call reads a whole document.
- JPEG/PNG/WebP are returned as JPEG at up to 2400 pixels on the long edge and 2 MiB; `image_scaled` indicates reduced dimensions. Each PDF `auto` page includes its text and visual rendition. PDF `text` explicitly omits visuals.
- DOCX paragraphs/tables/headers/notes and XLSX sheet names/cell addresses/stored values are read; embedded pictures/charts/layout are excluded. CSV/TXT/TSV/MD/JSON must use UTF-8 or BOM-marked UTF-16. Text is delivered in parts of at most 12000 UTF-16 units.
- Office ZIP: at most 2048 entries, 8 MiB per selected XML part, 24 MiB total; external relationships/DTDs/macros are not executed. Parsing is isolated and stops after 20 seconds.
- A file is accessible only while the source message is retained and this connection has current access. Telegram IDs belong to the original bot. Replacing/deleting the bot can make a file unavailable; no independent archive is promised.

## Limits and paging

- Up to 50 items and 64 KB per call; `next_cursor` continues the same query, `truncated: true` means there is more.
- History keeps the latest 60 days, starting at connection. Without dates, reads cover that available history in bounded pages. A wider date range is clipped to the current 60-day window.
- To finish a long message call `get_messages` with `message_id` and `text_cursor`.

## Conversation and participant retrieval (0.8)

- `get_messages.thread_id` filters one forum topic and requires `chat_id`. It combines with author/date filters and pagination; omit `person_id` to read both sides. Message text continuation cannot include topic or page filters.
- `get_message_context` returns a bounded window, the accessible explicit reply parent, and album members. Neighbours/album members stay in the anchor topic. Expand a truncated window with paged `get_messages` in the same chat/topic/period; ordinary groups have no reliable automatic episode boundaries.
- `reply_preview.person_id` comes only from an accessible stored parent, never an external reply snapshot. `mentions` is at most 64 `{person_id, location, offset, length}` entries for complete text/caption bodies. Offsets count UTF-16 units, as Telegram does. Raw Telegram IDs are not exposed; ambiguous usernames have no resolved link.
- `list_people` matches current and earlier names/usernames from retained accessible messages and reactions, and returns the latest accessible profile. Revoked/deleted/expired sources cannot supply an alias.
- `search_messages.mode` defaults to `exact`. `expanded` requires explicit `person_id` or `chat_ids`, `from`, `to`, and 1–8 `query_variants` (complete queries, each at most 256 characters). Your AI supplies word forms; ChatMate runs the same lexical/literal search for each. Duplicate variants are collapsed. An empty variant or no distinct alternative is invalid.
- Original-query hits precede every expanded-only hit, including later pages. `expanded: true` marks an alternative-query hit; `matched_query` is its winning query and drives `snippet`/`matched_in`. Keep mode, variants, scope and period unchanged with the cursor. Matches are candidate evidence, not proof of an active agreement.

## Rich conversation context (0.9, retrieval contract 5)

- Existing contracts 1–4 retain their previous shape. In the current tool output, `reply_preview.quote_manual` is the supplied manual-quote flag and `quote_position` is Telegram's approximate UTF-16 position in the original. External/forward `origin_type` distinguishes `user`, `hidden_user`, `chat`, `channel` or a future type; a display name alone is not a person ID.
- Reply chains use existing `reply_to_id` plus repeated `get_message_context`, at most five accessible parents. Keep visited IDs and explicitly report a missing link, cycle or depth limit. There is no recursive `reply_chain` response field. Normal forum context remains within the anchor topic; an explicit stored parent can explain the reply.
- Pin/checklist service events can carry accessible `target_message_id` (canonical UUID), or `target_missing`. Read the target with `get_message_context`; a missing target reveals no source or content. `auto_delete_seconds`, including zero, is a received timer event rather than the current live setting.
- `shared.checklist.tasks` entries retain `{id?, text, done, completed_at?, completed_by?}`. An actor is `{type: "user" | "chat", display_name?, person_id?}`; absent fields are unknown. Service events add `done_task_ids`, `undone_task_ids`, `added_tasks` and optional `partial`. IDs refer to checklist items, not messages.
- `shared.poll` can include `anonymous`, `total_voter_count`, `option_voter_counts` (aligned with options; null is unknown), `snapshot_at` and `partial`. This is Telegram's received snapshot, not a new query of current voting or proof of every voter's identity.
- An exact HTTP(S) preview URL has `links.location: "preview"`; it can differ from every text/caption link. Rich links have `location: "rich"`. The same 64-link/8192-byte budget applies; no URL fetch happens on the backend.
- Incoming rich text is searchable `text` with no inherited Telegram entity offsets. `rich.tables` holds up to four simple tables, each up to eight rows/eight cells and 120 characters per cell. `partial`/`reasons` (`unknown_block`, `malformed`, `limit`, `complex_table`) identify missing representation. Do not claim full formatting/content when partial.
