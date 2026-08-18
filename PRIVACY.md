# Privacy

ChatMate processes only data from Telegram sources that the workspace owner explicitly connected. MCP access is workspace-scoped and OAuth-protected. Retrieved Telegram text is minimized and treated as untrusted evidence. The plugin package contains no customer data, backend credentials, access tokens, Telegram identities, or connection codes.

The normal connection flow uses Telegram OIDC through Supabase Auth. Telegram may return a verified numeric ID plus basic profile claims such as name, username and photo, and Supabase Auth may retain those claims in its identity record. ChatMate uses only the verified numeric ID to match the existing Telegram owner; it does not use the other profile claims for authorization and does not send them to ChatGPT.

ChatMate does not use customer content for model training or evaluation without separate lawful opt-in. Provider processing is governed by the user's chosen AI provider and account settings.

For privacy requests during private beta, open a private support request through the ChatMate Telegram manager rather than posting customer data in a public GitHub issue.
