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
| `reply_preview` | The message this one answers: `author`, `is_owner`, `excerpt`, `quote` (the part the person selected), `media`, `from_other_chat` |
| `reply_to_id`, `reply_missing` | The stored original, or `reply_missing: true` when it is not stored (older than ChatMate or not available) |
| `forwarded_from` | Original sender name and date of a forwarded message |
| `service` | Chat event instead of a message, see below |
| `shared` | `poll` (question, options), `location`, `venue` (title, address), `contact` (name, phone), `dice`, `checklist` (tasks with `done`) |
| `attachments` | `type` (photo, video, animation, sticker, voice, video_note, audio, document, unsupported), `filename`, `mime`, `size` in bytes, `duration` in seconds, `width`, `height`, sticker `emoji`, audio `title`. Content is not available |
| `automated` | Away message or a reply sent by a business bot |
| `edited_at`, `edit_history` | When the text was last edited, and up to 5 earlier versions (`text`, `caption`, `edited_at` of that version, `replaced_at`), oldest first. Long versions are cut at 1000 characters with `text_truncated` |
| `reactions` | Per emoji (`emoji`, `custom_emoji_id` for a custom one, or `paid`): `count` and up to 10 people in `by` (`person_id`, `display_name`, `is_owner`). Anonymous reactions have a count only. Groups only, and only while the bot is an administrator |
| `deleted`, `deleted_at` | The message was deleted in a private chat; author, text and attachments are gone. `deleted_at` is when ChatMate learned of it |
| `album_id`, `thread_id`, `thread_title` | Media sent together; forum topic and its name |

## People

`list_people` returns people who wrote or reacted in the connected chats in all available stored history, most recently active first: `person_id`, `display_name`, `username`, `is_owner`, `is_bot`, `messages` and `reactions` counts, `first_seen`, `last_seen`, and up to 20 `chats` with their own counts. `query` matches part of a name or @username. Names are what Telegram showed at the time and can repeat; telling people apart by `username` and `chats` is more reliable. Chat events such as joins are not counted as messages. `next_cursor` continues a people list: pass it as `cursor` and repeat the same `query` and `chat_ids`; you can omit `limit` on continuation.

## Service event types

`members_joined` and `member_left` (with `names`), `title_changed` (new `title`), `photo_changed`, `photo_removed`, `chat_created`, `migrated_to_supergroup`, `migrated_from_group`, `pinned` (with `excerpt`), `topic_created`, `topic_edited`, `topic_closed`, `topic_reopened`, `auto_delete_changed`, `video_chat`. Other Telegram events keep their Telegram name.

## Coverage and gap reasons

- `observed_from` and `observed_through`: the period ChatMate has messages for in the scope.
- `known_gaps[].reason`:
  - `content_denied`: the chat was not allowed when the message came (for example before a group was connected, or after the user turned the chat off);
  - `source_revoked`, `consent_revoked`, `privacy_revoke`, `access_closed`: the user turned off the chat, storage or access;
  - `business_reconnect`, `generation_closed`: the bot or Chat Automation was reconnected;
  - `raw_expired`, `retries_exhausted`: ChatMate could not process the message in time.
- `unprocessed_media_count`: photos, videos, voice messages and files whose content was not read.
- Deleted private-chat messages stay in place as `deleted: true`. Telegram does not tell bots about deletions in groups, so a deleted group message keeps its last text.
- Reactions arrive only from groups where the bot is an administrator; private (Business) chats have none.

## Sending and statuses

- `send_message` goes only to the user's chat with their bot. `send_to_chat` goes to one business chat (as the user, through Chat Automation) or one group (as the user's ChatMate bot).
- Text is plain, up to 4000 characters per call. `reply_to_message_id` is a Telegram message number in that chat, not a ChatMate `id`; you get one only from a bot event (`data.message_id`), otherwise leave it out.
- Statuses: `pending` (queued), `sent`, `awaiting_owner` (a confirmation request waits for the user), `approved`, `declined`, `failed` (Telegram refused, nothing was sent), `unknown` (Telegram did not answer: do not send again, tell the user to check the chat).

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

## Limits and paging

- Up to 50 items and 64 KB per call; `next_cursor` continues the same query, `truncated: true` means there is more.
- Stored history has no time limit at this stage. Without dates, reads cover all available stored history, with bounded pages; date ranges have no duration ceiling.
- To finish a long message call `get_messages` with `message_id` and `text_cursor`.
