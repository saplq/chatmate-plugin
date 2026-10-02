# ChatMate data reference

## Contents
- Message fields
- Service event types
- Coverage and gap reasons
- Limits and paging

## Message fields

| Field | Meaning |
|---|---|
| `chat_title` | Group name, the other person's name in a private chat, or "My ChatMate" for the user's chat with the bot |
| `author.display_name`, `author.username` | Who wrote it. `author.is_owner` is true for the user |
| `text`, `caption` | What was written; a caption belongs to media. `text_truncated` with `text_cursor` means there is more |
| `reply_preview` | The message this one answers: `author`, `is_owner`, `excerpt`, `quote` (the part the person selected), `media`, `from_other_chat` |
| `reply_to_id`, `reply_missing` | The stored original, or `reply_missing: true` when it is not stored (older than ChatMate or not available) |
| `forwarded_from` | Original sender name and date of a forwarded message |
| `service` | Chat event instead of a message, see below |
| `shared` | `poll` (question, options), `location`, `venue` (title, address), `contact` (name, phone), `dice`, `checklist` (tasks with `done`) |
| `attachments` | `type` (photo, video, animation, sticker, voice, video_note, audio, document, unsupported), `filename`, `mime`, `size` in bytes, `duration` in seconds, `width`, `height`, sticker `emoji`, audio `title`. Content is not available |
| `automated` | Away message or a reply sent by a business bot |
| `edited_at` | The text was edited; only the latest version is stored |
| `album_id`, `thread_id` | Media sent together; forum topic |

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
- Deleted messages are not returned.

## Limits and paging

- Up to 50 items and 64 KB per call; `next_cursor` continues the same query, `truncated: true` means there is more.
- A date range covers at most 90 days per call; without dates, reads cover the last 90 days.
- To finish a long message call `get_messages` with `message_id` and `text_cursor`.
