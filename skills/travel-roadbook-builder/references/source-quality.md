# Source Quality

Use confidence labels:

- `high`: user-provided booking screenshot, fixed ticket time visible in a screenshot, official site copied by user, official page read through Agent Reach.
- `medium`: copied guide text, readable public guide page, user notes, widely known place information.
- `low`: unreadable link, inferred duration, ambiguous place, unverified opening hour, vague recommendation.

Use access labels on `sourceRecords`:

- `read`: the content was inspected directly through Agent Reach, pasted text, or screenshot review.
- `partial`: only part of the source was readable.
- `unreadable`: a URL was provided but the current environment could not access the source.
- `user-summary`: the user summarized a source but did not provide the original content.

Rules:

- Preserve source notes when possible.
- Preserve `sourceRecords[].id` and reference them through item-level `sourceIds`.
- Surface conflicts instead of silently resolving them.
- Mark unverified schedules as needing confirmation.
- Do not pretend a Xiaohongshu link was read if only the URL was provided.
- Ask for pasted text when a source is inaccessible.
- Do not store sensitive booking screenshot data such as full booking references, payment details, passenger IDs, QR codes, phone numbers, or emails.
- Treat engagement counts, likes, saves, or comments as context only. Do not use them as proof that a recommendation is correct.
